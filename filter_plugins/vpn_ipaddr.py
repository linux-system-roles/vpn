# SPDX-License-Identifier: GPL-3.0-or-later
# (c) 2014, Maciej Delmanowski <drybjed@gmail.com>
# (c) 2021, Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This file was copied from https://github.com/ansible-collections/ansible.netcommon/blob/ea48d0a5b8130bdba3361b5e3f758b552240ef58/plugins/filter/ipaddr.py

# Make coding more python3-ish
# Converted from ansible.netcommon to use ipaddress instead of netaddr
# need unicode_literals for ipaddress on python2 - otherwise get errors like this:
# ValueError: '192.168.122.1' does not appear to be an IPv4 or IPv6 interface
from __future__ import absolute_import, division, print_function, unicode_literals

__metaclass__ = type

from ansible.utils.display import Display
from functools import partial
import types

ipaddress = None
try:
    import ipaddress

except ImportError:
    ipaddress = None
    # in this case, we'll make the filters return error messages (see bottom)

from ansible import errors

display = Display()


# ---- IP address and network query helpers ----
def ip_interface(value):
    return ipaddress.ip_interface(value)


def ip_int_to_network(value, version):
    if not version:
        return ipaddress.ip_interface(value)
    elif version == 4:
        return ipaddress.IPv4Interface(value)
    else:  # assume 6
        return ipaddress.IPv6Interface(value)


def ip_num_cidr_to_network(value):
    # this section will raise an exception if value
    # is not a string with a "/", or if the parts of
    # the string are not ints
    address, prefix = value.split("/")
    address = int(address)
    prefix = int(prefix)
    return ip_interface((address, prefix))


def _empty_ipaddr_query(v, vtype):
    # We don't have any query to process, so just check what type the user
    # expects, and return the IP address in a correct format
    if v:
        if vtype == "address":
            return str(v.ip)
        elif vtype == "network":
            return str(v)
        else:
            return None
    else:
        return None


def _bool_ipaddr_query(v):
    if v:
        return True
    else:
        return None


def is_single_host(v):
    # see if the given network has only 1 address
    # assume that means it is a single host
    return v.network.num_addresses == 1


def _cidr_lookup_query(v, net, value):
    if hasattr(net.network, "supernet_of"):
        if net.network.supernet_of(v.network):
            return value
    elif not is_single_host(v):
        if (
            net.network.network_address <= v.network.network_address
            and net.network.broadcast_address >= v.network.broadcast_address
        ):
            return value
    elif v.ip in net.network:
        return value
    return False


def _network_query(v):
    """Return the network of a given IP or subnet"""
    return str(v.network.network_address)


def _subnet_query(v):
    return str(v.network)


def _version_query(v):
    return v.version


# ---- IP address and network filters ----


def ipaddr(value, query="", version=False, alias="ipaddr"):
    """Check if string is an IP address or network and filter it"""

    query_func_extra_args = {
        "": ("vtype",),
        "cidr_lookup": ("net", "value"),
    }

    query_func_map = {
        "": _empty_ipaddr_query,
        "bool": _bool_ipaddr_query,
        "cidr_lookup": _cidr_lookup_query,
        "network": _network_query,
        "subnet": _subnet_query,
        "version": _version_query,
    }

    vtype = None

    # Check if value is a list and parse each element
    if isinstance(value, (list, tuple, types.GeneratorType)):
        _ret = [ipaddr(element, str(query), version) for element in value]
        return [item for item in _ret if item]

    elif not value or value is True:
        # TODO: Remove this check in a major version release of collection with porting guide
        # TODO: and raise exception commented out below
        display.warning(
            "The value '%s' is not a valid IP address or network, passing this value to ipaddr filter"
            " might result in breaking change in future." % value
        )
        return False
        # raise errors.AnsibleFilterError(
        #     "{0!r} is not a valid IP address or network".format(value)
        # )

    # Check if value is a number and convert it to an IP address
    elif str(value).isdigit():
        try:
            v = ip_int_to_network(value, version)
        except Exception:
            return False
        # We got an IP address, let's mark it as such
        value = str(v)
        vtype = "address"

    # value has not been recognized, check if it's a valid IP string
    else:
        try:
            v = ip_interface(value)

            # value is a valid IP string, check if user specified
            # CIDR prefix or just an IP address, this will indicate default
            # output format
            try:
                address, prefix = value.split("/")
                vtype = "network"
            except Exception:
                vtype = "address"

        # value hasn't been recognized, maybe it's a numerical CIDR?
        except Exception:
            try:
                v = ip_num_cidr_to_network(value)
            except Exception:
                return False

            # We have a valid CIDR, so let's write it in correct format
            value = str(v)
            vtype = "network"

    # We have a query string but it's not in the known query types. Check if
    # that string is a valid subnet, if so, we can check later if given IP
    # address/network is inside that specific subnet
    try:
        if (
            query
            and (query not in query_func_map or query == "cidr_lookup")
            and not str(query).isdigit()
            and ipaddr(query, "network")
        ):
            net = ip_interface(query)
            query = "cidr_lookup"
    except Exception:
        # We will check the query below.
        pass

    # This code checks if value matches the IP version the user wants, ie. if
    # it's any version ("ipaddr()"), IPv4 ("ipv4()") or IPv6 ("ipv6()")
    # If version does not match, return False
    if version and v.version != version:
        return False

    extras = []
    for arg in query_func_extra_args.get(query, tuple()):
        extras.append(locals()[arg])
    try:
        return query_func_map[query](  # pylint: disable=no-value-for-parameter
            v, *extras
        )
    except KeyError:
        try:
            int(query)
            if v.network.num_addresses == 1:
                if vtype == "address":
                    return str(v.ip)
                elif vtype == "network":
                    return str(v)

            elif v.network.num_addresses > 1:
                try:
                    return str(v.network[int(query)]) + "/" + str(v.network.prefixlen)
                except Exception:
                    return False

            else:
                return value

        except Exception:
            raise errors.AnsibleFilterError(alias + ": unknown filter type: %s" % query)

    return False


def _need_ipaddress(f_name, *args, **kwargs):
    raise errors.AnsibleFilterError(
        "The %s filter requires python 3.3 or later with built-in ipaddress "
        "module, or python's ipaddress be installed on the ansible controller" % f_name
    )


# ---- Ansible filters ----
class FilterModule(object):
    """IP address and network manipulation filters

    Detailed documentation available at https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters_ipaddr.html
    This module implements only the 'ipaddr' filter called 'vpn_ipaddr', and only provides a small subset of that
    functionality required for the vpn role.
    """

    filter_map = {
        "vpn_ipaddr": ipaddr,
    }

    def filters(self):
        if ipaddress:
            return self.filter_map
        else:
            return dict((f, partial(_need_ipaddress, f)) for f in self.filter_map)
