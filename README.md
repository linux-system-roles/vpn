# VPN System Role

A Role for managing setup and configuration of VPN tunnels.

Basic usage:

```yaml
all:
  hosts:
    bastion1.example.com: {...}
    bastion2.example.com: {...}
    bastion3.example.com: {...}
  vars:
    vpn_connections:
      - hosts:
          bastion1.example.com:
          bastion2.example.com:
          bastion3.example.com:
```

The role will set up a vpn tunnel between each pair of hosts in the list of `vpn_connections`, using the default parameters, including generating keys as needed.  This role assumes that the names of the hosts under `hosts` are the same as the names of the hosts used in the Ansible inventory, and that you can use those names to configure the tunnels (i.e. they are real FQDNs that resolve correctly).

## Requirements

The Ansible controller requires the python `ipaddress` package on EL7 systems,
or other systems that use python 2.7.  On python 3.x systems, the VPN role
uses the python3 built-in `ipaddress` module.

## Top-level variables

These global variables should be applied to the configuration for every tunnel (unless the user overrides them in the configuration of a particular tunnel).

| Parameter                            | Description                                                                                   | Type        | Required | Default                 |
|--------------------------------------|-----------------------------------------------------------------------------------------------|:-----------:|:--------:|-------------------------|
| vpn\_provider                        | VPN provider used (e.g. libreswan, wireguard, etc.)                                         | str         | no       | libreswan               |
| [vpn\_auth\_method](#vpn_auth_method)| VPN authentication method used.                                                             | str         | no       | psk                     |
| vpn\_regen\_keys                     | Whether pre-shared keys should be regenerated for sets of hosts with existing keys.                | bool        | no       | false                   |
| vpn\_opportunistic                   | Whether an opportunistic mesh configuration should be used.                                        | bool        | no       | false                   |
| vpn\_default\_policy                 | The default policy group to add target machines to under a mesh configuration.                | str         | no       | `private-or-clear`      |
| [vpn\_ensure\_openssl](#vpn_ensure_openssl)    | Ensure the `openssl` package is installed on the controller.                          | bool        | no       | true      |
| [vpn\_connections](#vpn_connections) | List of VPN connections to make.                                                              | list        | yes      | -                       |

### vpn_auth_method

The value specified in this variable will determine the value of the `authby` field for the Libreswan tunnels opened.
Acceptable values:
* `psk` for pre-shared key (PSK) authentication
* `cert` for authentication using certificates

### vpn_ensure_openssl

The role uses `openssl` to generate PSKs.  It requires this to be installed on the controller node.
The default value is `true`.  If you have pre-generated your PSKs, or you are not using PSKs, then
set `vpn_ensure_openssl: false`.

### vpn_connections

`vpn_connections` is a list of connections. Each connection is either:

* A list of hosts specified by `hosts`. In this host-to-host use case, the role creates tunnels between each pair of hosts. At least one tunnel must be defined in this list.

* A mesh configuration consisting of one or more subnets and profiles. In this mesh use case, the role deploys an opportunistic mesh configuration using the `policy`/`cidr` pairs that you define in the `policies`.

## Connection-specific variables

In addition to the global variables, you may provide a number of other variables that will be applied to the configuration for each tunnel.

| Parameter                                 | Description                                                                           | Type        | Required | Default                 | Libreswan Equivalent    |
|-------------------------------------------|---------------------------------------------------------------------------------------|:-----------:|:--------:|-------------------------|:-----------------------:|
| [name](#name)                             | A unique, arbitrary name used to prefix the connection name.                      | str         | no       | See [name](#name).      | conn `<name>`           |
| [hosts](#hosts)                           | A VPN tunnel will be constructed between each pair of hosts in this dictionary.       | dict        | yes      | -                       | -                       |
| [auth_method](#auth_method)               | Authentication method to be used for this connection.                                 | str         | no       | vpn\_auth\_method       | authby                  |
| [auto](#auto)                             | What operation, if any, should be done automatically at startup.                      | str         | no       | -                       | auto                    |
| [opportunistic](#opportunistic)           | Whether an opportunistic mesh configuration should be used.                                | bool        | no       | vpn\_opportunistic      | -                       |
| [policies](#policies)                     | List of policy settings to use for an opportunistic mesh configuration.               | list        | no       | -                   | -                       |

### name

By default, the role generates a descriptive name for each tunnel it creates from the perspective of each system. For example, when creating a tunnel between `bastion1` and `bastion2`, the descriptive name of this connection on `bastion1` is `bastion1-to-bastion2` but on `bastion2` the connection is named `bastion2-to-bastion1`. You may add a prefix to these auto-generated names by specifying a value in the `name` field.

### auth_method

Optionally, you can define an authentication method to use at the connection level. If `auth_method` is not defined, the role uses the global variable `vpn_auth_method`. The value of `auth_method`, or `vpn_auth_method`, determines the value of the `authby` field for the Libreswan tunnel opened for this connection. Acceptable values:
* `psk` for pre-shared key (PSK) authentication
* `cert` for authentication using certificates

### auto

What operation, if any, should be done automatically at IPsec startup. Currently accepted values are **add**, **ondemand**, **start**, and **ignore**. The default value is null, which means no automatic startup operation.

### opportunistic

By default, the VPN System Role creates a host-to-host tunnel between each pair of nodes specified within a `vpn_connection`. You can instead configure an opportunistic mesh VPN by setting `opportunistic` to `true`, which will include all hosts in the Ansible inventory in the opportunistic mesh configuration.

**Note:** When configuring an opportunistic mesh VPN using a control node that shares the same CIDR as one or more of mesh CIDRs used for encryption, add a clear policy entry for the control node CIDR in order to prevent an SSH connection loss during the play. See [example](#opportunistic-mesh-vpn-configuration).

### policies

In this dictionary, you can set policy rules related to opportunistic encryption. If no policy rules are set, the default policy rule is `private-or-clear`. To override this default policy rule, see [cidr](#cidr). Note that the default policy does not add a `0.0.0.0/0` entry into a policy file. Instead, individual classless inter-domain routing (CIDR) values are added to policy files based on the CIDRs of the managed nodes. The default policy rule will be applied to CIDRs of all the hosts over which this role is run, unless you specify in this section a different policy rule for the CIDR of a particular managed node or group of managed nodes. If users wish to add a `0.0.0.0/0` entry to a particular policy file, they may add an item to this list where the policy value is the desired policy to be applied, and the CIDR value is `0.0.0.0/0`.

| Parameter                                 | Description                                                                           | Type        | Required |
|-------------------------------------------|---------------------------------------------------------------------------------------|:-----------:|:--------:|
| [policy](#policy)                         | A valid policy connection group.                                                      | str         | no       |
| [cidr](#cidr)                             | A valid CIDR to which this policy rule is applied.                                            | str         | no       |

#### policy

Valid values are `private`, `private-or-clear`, and `clear`.

#### cidr

In addition to any valid CIDR value, you may specify `default` in this field to apply the corresponding policy to all hosts that do not fit into one of the other specified policy groups, thereby overriding the default private-or-clear policy rule.

### hosts
Each key in this dictionary is the unique name of a host. If a host is listed in `hosts` and not in the inventory file, the host will not be managed by the inventory. In such case, the `hostname` parameter is required because it is necessary for setting up the local ends of such a tunnel.

If the host key in the hosts list of your inventory is not the fully qualified domain name (FQDN) you want to use, you must use the `hostname` field under each host in this `vpn_connections` hosts dictionary to specify the actual FQDN or IP address you want the VPN role to use for setting up the tunnel. If you do not specify `hostname`, then the role will use `ansible_host` if defined, or the host key in your hosts list if neither `ansible_host` nor `hostname` is defined. 

For each host key in this dictionary, the following host-specific parameters can be specified.  

| Parameter                         | Description                                                                                   | Type        | Required | Default                 | Libreswan Equivalent         |
|-----------------------------------|-----------------------------------------------------------------------------------------------|:-----------:|:--------:|-------------------------|:----------------------------:|
| [hostname](#hostname)             | Host name or IP address to use for setting up a VPN connection.                                            | str         | no       | -                       | left/right                   |
| [cert_name](#cert_name)           | Certificate nickname of this host's certificate in the NSS database.                          | str         | no       | -                       | leftcert/rightcert           |
| subnets                           | A list of the subnets that should be available via the VPN connection.                        | list        | no       | -                       | leftsubnets/rightsubnets     |

#### hostname

Can hold a host name or IP address. Specified only when overriding host names used by Ansible for SSH. Note that if a host name is specified, it must be fully qualified to ensure that DNS resolution works correctly on host machines. This parameter is required when the host is not part of the inventory list of hosts.

#### cert_name
It is assumed that the `cert_name` provided by the user exists in the IPSec NSS cert database. Users may use the certificate system role to issue these certificates.

## Verifying a successful startup

### Libreswan

To confirm that a connection is successfully loaded:
```
ipsec status | grep <connectionname>
```

To confirm that a connection is successfully started:
```
ipsec trafficstatus | grep <connectionname>
```

To verify that a certificate has been imported (requires that the connection has loaded successfully). Note that if the same certificate is used for multiple connections, it may show up in the output for this command, even though there was an error on the connection being checked:
```
ipsec whack --listcerts
```

If a connection did not successfully load, it is recommended to run the following command to manually try to add the connection. This will give more specific information indicating why the connection failed to establish:

```
ipsec auto --add <connectionname>
```

Any errors that may have occurred during the process of loading and starting the connection are in the logs, which can be found in `/var/log/pluto.log` in RHEL 8, or by issuing the command `journalctl -u ipsec` in RHEL 7. Since these logs can be verbose and contain old entries, it is generally recommended to try to manually add the connection to obtain log messages from the standard output instead.

## Firewall

The firewall must be configured to allow traffic on 500 and 4500/UDP ports for the IKE, ESP, and AH protocols. In the future, the firewall system role may be used for this configuration, however in the meantime these settings will need to be manually configured.

### RHEL 8 and 9

The following commands configure the firewall for RHEL 8 and 9 systems, and other systems which use `firewalld`:

```
firewall-cmd --add-service="ipsec"
firewall-cmd --runtime-to-permanent

```

## Use Cases

- Host-to-Host (openstack): Specific nodes connecting to each other. Use IPsec for IP failover between these nodes (so all other nodes don't need to be aware of anything happening). Keys are FreeIPA certificates, and pre-shared keys
- Host-to-Host (data centers): Two systems in different data centers communicate encrypted with each other using FreeIPA certificates, and pre-shared keys
- Host-to-Host (one host): One system communicating with an existing system (e.g., cisco) in an other organization that uses pre-shared keys
- Network-to-Network (two routers): One organization router connecting to a second one bringing together two distinct networks. Keys are FreeIPA certificates, and pre-shared keys.
- VPN Remote Access Server / Roadwarrior: One organization router accepting connections from multiple clients. Clients connect to a single router using FreeIPA certificates.
- MESH: node independent configurations. When adding/removing a node, you don't need to reconfigure all other nodes. They all attempt to setup individual host-to-host connections. A PKI is used to authenticate nodes (FreeIPA, potentially in the future DNSSEC)

Note that for a couple of these use cases, you cannot use host-scoped settings (e.g. global settings specified in `all.hosts`).

## Examples

### Host-to-host (multiple VPN tunnels with one externally managed host)

This playbook sets up the tunnel `bastion_east-to-bastion_west` using pre-shared key authentication with keys auto-generated by the system role. Additionally, the local ends of two more tunnels are set up: `bastion_east-to-bastion_north` and `bastion_west-to-bastion_north`. In this case, one of the hosts, `bastion_north`, is external to the inventory e.g. in a remote datacenter, and only the local ends of the tunnels can be set up. The `hostname` field contains all the information necessary to ensure that the local ends of the tunnel are set up correctly.

```yaml
all:
  hosts:
    bastion_east:
      ansible_host: bastion1.example.com
    bastion_west:
      ansible_host: bastion2.example.com
  vars:
    vpn_connections:
      - hosts:
          bastion_east:
          bastion_west:
          bastion_north: # not in the hosts list
            hostname: 192.168.122.103
```

### Host-to-host (multiple VPN tunnels with multiple NICS)

In this case, the hosts have multiple vpn connections associated with multiple NICs e.g. some OpenStack and OpenShift use cases.

```yaml
all:
  hosts:
    bastion_east: {...}
    bastion_west: {...}
    bastion_north: {...}
  vars:
    vpn_connections:
      - name: control_plane_vpn
        hosts:
          bastion_east:
            hostname: 192.168.122.101 # IP for control plane
          bastion_west:
            hostname: 192.168.122.102
          bastion_north:
            hostname: 192.168.122.103
      - name: data_plane_vpn
        hosts:
          bastion_east:
            hostname: 10.0.0.1 # IP for data plane
          bastion_west:
            hostname: 10.0.0.2
          bastion_north:
            hostname: 10.0.0.3
```

### Host-to-host (multiple VPN tunnels using certificates)

This playbook sets up host-to-host tunnels between each pair of hosts in the list of `hosts` using certificates for authentication.

```yaml
  hosts:
    bastion1.example.com: {...}
    bastion2.example.com: {...}
    bastion3.example.com: {...}
  vars:
    vpn_connections:
      - name: vpn-tunnel-x
        auth_method: cert
        auto: start
        hosts:
          bastion1.example.com:
            cert_name: bastion1cert
          bastion2.example.com:
            cert_name: bastion2cert
          bastion3.example.com:
            cert_name: bastion3cert
```

### Opportunistic Mesh VPN configuration

This playbook sets up an opportunistic mesh VPN configuration on each host in the list of `hosts`, using certificates for authentication. In this example, the controller machine shares the same CIDR as both of the target machines (`192.168.110.0/24`) and has IP address `192.168.110.7`. Therefore the controller machine will fall under a `private` policy which will automatically be created for the CIDR `192.168.110.0/24`. To prevent an SSH connection loss during the play, a `clear` policy for the controller machine has been added to the list of  `policies`. Note that there is also an item in the `policies` list where the `cidr` is equal to `default`. This is because this playbook is overriding the default policy rule to make it `private` instead of `private-or-clear`.

```yaml
  hosts:
    bastion1.example.com:
      cert_name: bastion1cert
    bastion2.example.com:
      cert_name: bastion2cert
    bastion3.example.com:
      cert_name: bastion3cert
  vars:
    vpn_connections:
      - opportunistic: true
        auth_method: cert
        policies:
          - policy: private
            cidr: default
          - policy: private-or-clear
            cidr: 192.168.122.0/24
          - policy: private
            cidr: 192.168.110.0/24
          - policy: clear
            cidr: 192.168.110.7/32         
```

## To be added in a future release

The following global variables will be added. Additionally, `pubkey` will be added as a valid option under `vpn_auth_method` to perform public key authentication without certificates (enforces SHA-2).

| Parameter                            | Description                                                                                   | Type        | Required | Default                 |
|--------------------------------------|-----------------------------------------------------------------------------------------------|:-----------:|:--------:|-------------------------|
| vpn\_enc\_alg                        | VPN encryption algorithm to use. See [Algorithms section](#algorithms) for acceptable values. | str         | no       | -                       |
| vpn\_auth\_alg                       | VPN authentication algorithm to use.                                                          | str         | no       | SHA-2                   |
| vpn\_wait                            | If tasks should wait for the VPN tunnel to be started up.                                     | bool        | no       | false                   |
| [vpn\_lifetime](#vpn_lifetime)       | How long a VPN instance should last before being renegotiated. Acceptable values are an integer optionally followed by **s** (a time in seconds) or a decimal number followed by **m**, **h**, or **d** (a time in minutes, hours, or days respectively). | int         | no       | -                       |
| vpn\_public\_key\_src                | Path to file on the controller host containing public key used by default.                    | str         | no       | -                       |
| vpn\_public\_key\_content            | Contains the public key used by default for public key authentication without certificates.   | str         | no       | -                       |

Two dictionaries (`ike` and `ipsec`) will be added to the `vpn_connections` dictionary:

| Parameter                                 | Description                                                                           | Type        | Required | Default                 | Libreswan Equivalent    |
|-------------------------------------------|---------------------------------------------------------------------------------------|:-----------:|:--------:|-------------------------|-------------------------|
| ike                                       | Defines information specific to setting up the IKE protocol.                          | dict        | no       | -                       | -                       |
| ike.enc_alg                               | Which encryption algorithm to use for IKE.                                            | str         | no       | vpn\_enc\_alg           | ike                     |
| ike.enc_keysize                           | Size of encryption key to use for IKE.                                                | str         | no       | -                       | ike                     |
| ike.auth_alg                              | Which authentication algorithm to use for IKE.                                        | str         | no       | vpn\_auth\_alg          | ike                     |
| ike.dh_group                              | Which Diffie-Hellman group to use for IKE.                                            | str         | no       | -                       | ike                     |
| ike.lifetime                              | How long keying channel of an IKE connection should last before being renegotiated.   | str         | no       | vpn\_lifetime           | ikelifetime             |
| ipsec                                     | Defines information specific to setting up IPSec protocol.                            | dict        | no       | -                       | -                       |
| ipsec.enc_alg                             | Which encryption algorithm to use for IPSec.                                          | str         | no       | vpn\_enc\_alg           | esp                     |
| ipsec.enc_keysize                         | Size of the encryption key used for IPSec.                                            | str         | no       | -                       | esp                     |
| ipsec.auth_alg                            | Which authentication algorithm to use for IPSec.                                      | str         | no       | vpn\_auth\_alg          | esp                     |
| ipsec.dh_group                            | Which Diffie-Hellman group to use for IPSec.                                          | str         | no       | -                       | esp                     |
| ipsec.lifetime                            | How long keying channel of an IPSec connection should last before being renegotiated. | str         | no       | vpn\_lifetime           | salifetime              |
| ipsec.mode                                | The type of the connection. User can specify `tunnel` or `transport`, however Libreswan defaults this value to `tunnel` if not specified. If the hosts are behind NAT, the user should specify `transport`. | str         | no       | `tunnel`                | type                    |
| [shared_key_src](#shared_key_src)         | **Not recommended.** Path to file on the controller host containing a PSK.            | str         | no       | -                       | From ipsec.secrets file |
| [shared_key_content](#shared_key_content) | **Not recommended.** The actual PSK in a vault secret or base64 encoded string.       | str         | no       | -                       | From ipsec.secrets file |

The following variables will be added under the [`hosts`](#hosts) dictionary:

| Parameter                         | Description                                                                                   | Type        | Required | Default                 | Libreswan Equivalent         |
|-----------------------------------|-----------------------------------------------------------------------------------------------|:-----------:|:--------:|-------------------------|:----------------------------:|
| [public_key_src](#public_key)     | Path to file on the controller host containing public key used by this host.                  | str         | no       | -                       | leftrsasigkey/rightrsasigkey |
| [public_key_content](#public_key) | Contains the public key used by this host for public key authentication without certificates. | str         | no       | -                       | leftrsasigkey/rightrsasigkey |

### shared_key

`shared_key_src` indicates the path to a file on the controller host containing a PSK to be copied to the `ipsec.secrets` file on the managed node.

`shared_key_content` contains the actual PSK in a vault secret or base64 encoded string. This will also be copied to the `ipsec.secrets` file on the managed node.

**Notes: It is not recommended to populate either of these two fields, since the role will automatically generate a secure pre-shared key if none is provided by the user. If the user does wish to provide their own pre-shared key, the recommendation is to vault encrypt the value. See https://docs.ansible.com/ansible/latest/user_guide/vault.html. Also, since it is still unclear how the role will allow users to specific pre-shared keys for each pair of hosts in a tunnel, it is reiterated that users should rely on the role's abilty to generate secure pre-shared keys automatically.**

### public_key

`public_key_src` specifies a path to a file on the controller host containing the public key used by this host for public key authentication without certificates. Otherwise, the user can directly specify the public key for this host by populating `public_key_content`. `public_key_content` can also accept a CKAID or nickname for a public key in the NSS database.

Note that `public_key_src` and `public_key_content` may also be specified as host-scoped Ansible variables. The variable names in this case will be `vpn_public_key_src` and `vpn_public_key_content`..

If neither `public_key_src` nor `public_key_content` is populated, the role will generate key pairs for each host.

### Algorithms

#### Libreswan
Minimum acceptable algorithms are AES, MODP2048 and SHA2.

## License

MIT.
