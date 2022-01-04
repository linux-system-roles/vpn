# SPDX-License-Identifier: GPL-3.0-or-later
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

# This file was copied from https://github.com/ansible-collections/ansible.netcommon/blob/ea48d0a5b8130bdba3361b5e3f758b552240ef58/tests/unit/plugins/filter/test_ipaddr.py  # noqa: E501

# Make coding more python3-ish
# need unicode_literals for ipaddress on python2 - otherwise get errors like this:
# ValueError: '192.168.122.1' does not appear to be an IPv4 or IPv6 interface
from __future__ import absolute_import, division, print_function, unicode_literals

__metaclass__ = type

import unittest

import vpn_ipaddr as ipaddr


class TestIpFilter(unittest.TestCase):
    def test_ipaddr_empty_query(self):
        self.assertEqual(ipaddr.ipaddr("192.0.2.230"), "192.0.2.230")
        self.assertEqual(ipaddr.ipaddr("192.0.2.230/30"), "192.0.2.230/30")
        self.assertEqual(ipaddr.ipaddr([]), [])

        self.assertEqual(ipaddr.ipaddr(True), False)
        self.assertEqual(ipaddr.ipaddr(""), False)

        # #TODO: Add these test after the check value check for None and True is removed
        # #TODO: from ipaddr filter
        # with pytest.raises(
        #     AnsibleFilterError,
        #     match="True is not a valid IP address or network",
        # ):
        #     ipaddr.ipaddr(True)
        # with pytest.raises(
        #     AnsibleFilterError, match="'' is not a valid IP address or network"
        # ):
        #     ipaddr.ipaddr("")

    def test_ipaddr_bool_query(self):
        self.assertTrue(ipaddr.ipaddr("192.0.2.20", "bool"))
        self.assertFalse(ipaddr.ipaddr("192.900.2.20", "bool"))

    def test_network(self):
        address = "1.12.1.34/32"
        self.assertEqual(ipaddr.ipaddr(address, "network"), "1.12.1.34")
        address = "1.12.1.34/255.255.255.255"
        self.assertEqual(ipaddr.ipaddr(address, "network"), "1.12.1.34")
        address = "1.12.1.34"
        self.assertEqual(ipaddr.ipaddr(address, "network"), "1.12.1.34")
        address = "1.12.1.35/31"
        self.assertEqual(ipaddr.ipaddr(address, "network"), "1.12.1.34")
        address = "1.12.1.34/24"
        self.assertEqual(ipaddr.ipaddr(address, "network"), "1.12.1.0")

    def test_cidr_lookup(self):
        big_network = "1.12.1.0/24"
        small_network = "1.12.1.0/28"
        ip_in_big = "1.12.1.192"
        ip_not_in_big = "192.168.122.1"
        # test identity - x contains x
        self.assertTrue(ipaddr.ipaddr(big_network, big_network))
        self.assertTrue(ipaddr.ipaddr(small_network, small_network))
        self.assertTrue(ipaddr.ipaddr(ip_in_big, ip_in_big))
        self.assertTrue(ipaddr.ipaddr(ip_not_in_big, ip_not_in_big))
        # test ip containment - X contains y
        self.assertTrue(ipaddr.ipaddr(ip_in_big, big_network))
        self.assertTrue(ipaddr.ipaddr(small_network, big_network))
        # test not contained - X does not contain a
        self.assertFalse(ipaddr.ipaddr(ip_not_in_big, big_network))
        self.assertFalse(ipaddr.ipaddr(ip_not_in_big, small_network))
        self.assertFalse(ipaddr.ipaddr(ip_in_big, small_network))
        self.assertFalse(ipaddr.ipaddr(big_network, small_network))
        self.assertFalse(ipaddr.ipaddr(big_network, ip_in_big))
        self.assertFalse(ipaddr.ipaddr(small_network, ip_in_big))

    def test_subnet(self):
        address = "1.12.1.34/29"
        self.assertEqual(ipaddr.ipaddr(address, "subnet"), "1.12.1.32/29")
        address = "1.12.1.34/32"
        self.assertEqual(ipaddr.ipaddr(address, "subnet"), "1.12.1.34/32")
        address = "1.12.1.34/23"
        self.assertEqual(ipaddr.ipaddr(address, "subnet"), "1.12.0.0/23")
