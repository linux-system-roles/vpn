# linux-system-roles.vpn

[![citest.yml](https://github.com/linux-system-roles/vpn/actions/workflows/citest.yml/badge.svg)](https://github.com/linux-system-roles/vpn/actions/workflows/citest.yml)

The vpn role allows you to configure VPN tunnels using Libreswan.
It supports host-to-host tunnels between inventory hosts and opportunistic mesh configurations with policy-based encryption.
The role can generate pre-shared keys, manage firewall and SELinux settings for IPsec ports, and configure certificates for tunnel authentication.

## Supported Platforms

This role supports managed nodes running the following operating systems:
RHEL and CentOS 7, 8, 9, 10, Fedora.

This role requires Ansible version 2.9 or newer.

### Additional Requirements

The Ansible controller requires the python `ipaddress` package on EL7 systems, or other systems that use python 2.7.
On python 3.x systems, the VPN role uses the python3 built-in `ipaddress` module.

The role requires the `firewall` role and the `selinux` role from the `fedora.linux_system_roles` collection, if [`vpn_manage_firewall`](#vpn_manage_firewall) and [`vpn_manage_selinux`](#vpn_manage_selinux) are set to `true`, respectively.

## Collection Requirements

The role requires additional collections to manage `rpm-ostree` systems.
Please run the following command to install them:

```bash
ansible-galaxy collection install -r meta/collection-requirements.yml
```

## Verifying a Successful Startup

### Verifying Libreswan

To confirm that a connection is successfully loaded:

```bash
ipsec status | grep <connectionname>
```

To confirm that a connection is successfully started:

```bash
ipsec trafficstatus | grep <connectionname>
```

To verify that a certificate has been imported:

```bash
ipsec whack --listcerts
```

If a connection did not successfully load, try to manually add it:

```bash
ipsec auto --add <connectionname>
```

Errors can be found in `/var/log/pluto.log` in RHEL 8, or by issuing `journalctl -u ipsec` in RHEL 7.

## Use Cases

The following are common VPN deployment topologies that this role can configure.
See the example playbooks above for how to set up each scenario.

* **Host-to-Host (openstack)**: Encrypt traffic between specific nodes, such as OpenStack instances using IP failover.
  Useful when individual hosts need dedicated encrypted channels without affecting the rest of the network.

* **Host-to-Host (data centers)**: Connect two systems across different data centers with encrypted communication, using either FreeIPA certificates or pre-shared keys.

* **Host-to-Host (single remote peer)**: Set up an encrypted tunnel from one managed system to an existing device (e.g. a Cisco appliance) in another organization using pre-shared keys.

* **Network-to-Network (site-to-site)**: Link two distinct networks through their routers so that hosts on each side can communicate as if they were on the same network.

* **VPN Remote Access Server (roadwarrior)**: Configure a single server to accept incoming VPN connections from multiple remote clients using FreeIPA certificates.

* **Mesh VPN**: Build a fully connected mesh where each node independently establishes host-to-host tunnels with all other nodes.
  Adding or removing a node does not require reconfiguring the others.
  Nodes authenticate using a PKI (e.g. FreeIPA).

## Configuring General VPN Settings

These global variables apply to every tunnel unless overridden in a specific connection definition.

### Variables

<a id="vpn_provider"></a>**vpn_provider** (`str`) - The VPN software provider used to configure tunnels.
Currently only `libreswan` is supported.
Choices: `libreswan`.
Default: `libreswan`.

<a id="vpn_auth_method"></a>**vpn_auth_method** (`str`) - The default VPN authentication method for tunnels.
Use `psk` for pre-shared key authentication or `cert` for certificate-based authentication.
Choices: `psk`, `cert`.
Default: `psk`.

<a id="vpn_regen_keys"></a>**vpn_regen_keys** (`bool`) - Whether pre-shared keys should be regenerated for host pairs that already have secrets files.
Default: `false`.

<a id="vpn_opportunistic"></a>**vpn_opportunistic** (`bool`) - Whether opportunistic mesh configuration should be used by default for connections that do not override this setting.
Default: `false`.

<a id="vpn_default_policy"></a>**vpn_default_policy** (`str`) - Default opportunistic mesh policy group applied to target machines.
Use `private` for encrypted traffic, `private-or-clear` for opportunistic encryption, or `clear` for unencrypted traffic.
Choices: `private`, `private-or-clear`, `clear`.
Default: `private-or-clear`.

### Example Playbooks

#### Basic VPN Mesh Between Hosts

This example sets up VPN tunnels between each pair of hosts using pre-shared key authentication with auto-generated keys.

```yaml
all:
  hosts:
    bastion1.example.com: {}
    bastion2.example.com: {}
    bastion3.example.com: {}
  vars:
    vpn_connections:
      - hosts:
          bastion1.example.com:
          bastion2.example.com:
          bastion3.example.com:
```

## Configuring VPN Connections

The [`vpn_connections`](#vpn_connections) variable is a list of connection specifications.
Each connection defines either a host-to-host tunnel between named hosts or an opportunistic mesh configuration.

In addition to the global variables, you may provide a number of connection-specific variables.
All time fields (for example `ikelifetime` and others) accept the time as a number + unit e.g.
`13h` for 13 hours, `10s` for 10 seconds.

### Variables

<a id="vpn_connections"></a>**vpn_connections** (`list` / `dict`) - List of VPN connection specifications.
Each item defines either a host-to-host tunnel between named hosts or an opportunistic mesh configuration.
Default: `[]`.

> **name** (`str`) - An optional prefix added to auto-generated connection names.
>
> **hosts** (`dict`) - Dictionary of hosts participating in a host-to-host tunnel. Each key is an inventory host name. Each value is an optional dictionary of host-specific settings, or a scalar value such as an empty string or null when no host-specific options are needed.
>
> **auth_method** (`str`) - Authentication method for this connection. Overrides [`vpn_auth_method`](#vpn_auth_method) when set. Use `psk` for pre-shared key authentication or `cert` for certificate-based authentication. Choices: `psk`, `cert`.
>
> **auto** (`raw`) - The Libreswan `auto` setting for this connection. Accepts `add`, `ondemand`, `start`, or `ignore`, or null when no automatic startup operation should be configured.
>
> **opportunistic** (`bool`) - Whether this connection uses an opportunistic mesh configuration instead of explicit host-to-host tunnels.
>
> **policies** (`list` / `dict`) - List of opportunistic mesh policy rules for this connection.
>
> > **policy** (`str`) - The policy group applied to the corresponding CIDR. Use `private` for encrypted traffic, `private-or-clear` for opportunistic encryption, or `clear` for unencrypted traffic. Choices: `private`, `private-or-clear`, `clear`.
> >
> > **cidr** (`str`) - The CIDR to which the policy applies. Use `default` to apply the policy to hosts not matched by other rules.
>
> **shared_key_content** (`str`) - A pre-defined pre-shared key for this connection. When not set, the role generates a key using `openssl`.
>
> **ike** (`str`) - IKE encryption and authentication algorithms for phase 1 of this connection.
>
> **esp** (`str`) - ESP algorithms offered or accepted for Child SA negotiation on this connection.
>
> **type** (`str`) - The Libreswan connection type, such as `tunnel` or `transport`.
>
> **ikelifetime** (`str`) - How long the IKE SA should remain valid before renegotiation, using Libreswan time notation such as `8h` or `28800s`.
>
> **salifetime** (`str`) - How long a Child SA instance should remain valid before expiry, using Libreswan time notation such as `8h` or `28800s`.
>
> **retransmit_timeout** (`str`) - Maximum time allowed for a packet and its retransmits before the IKE attempt is aborted, using Libreswan time notation.
>
> **dpddelay** (`str`) - Delay between Dead Peer Detection or IKEv2 liveness keepalives, using Libreswan time notation. Requires `dpdtimeout` when set.
>
> **dpdtimeout** (`str`) - Idle time after which a DPD-enabled peer is declared dead. Requires `dpddelay` when set.
>
> **dpdaction** (`str`) - Action taken when a DPD-enabled peer is declared dead.
>
> **leftupdown** (`raw`) - The updown script executed when connection status changes. Accepts a command string or null to disable the default Libreswan updown script.

### Example Playbooks

#### Host-to-Host with One Externally Managed Host

Sets up tunnels between inventory hosts and an external host not managed by Ansible.
The `hostname` field provides the IP for the unmanaged host.

```yaml
all:
  hosts:
    bastion_east:
      ansible_host: bastion1.example.com
    bastion_west:
      ansible_host: bastion2.example.com
  vars:
    vpn_connections:
      - ike: aes256-sha2;dh19
        esp: aes-sha2_512+sha2_256
        ikelifetime: 11h
        salifetime: 9h
        type: transport
        hosts:
          bastion_east:
          bastion_west:
          bastion_north:
            hostname: 192.168.122.103
```

#### Host-to-Host with Multiple NICs

Hosts with multiple VPN connections associated with multiple NICs, e.g. separate control plane and data plane networks.

```yaml
all:
  hosts:
    bastion_east: {}
    bastion_west: {}
    bastion_north: {}
  vars:
    vpn_connections:
      - name: control_plane_vpn
        hosts:
          bastion_east:
            hostname: 192.168.122.101
          bastion_west:
            hostname: 192.168.122.102
          bastion_north:
            hostname: 192.168.122.103
      - name: data_plane_vpn
        hosts:
          bastion_east:
            hostname: 10.0.0.1
          bastion_west:
            hostname: 10.0.0.2
          bastion_north:
            hostname: 10.0.0.3
```

#### Host-to-Host Using Certificates

Sets up tunnels using certificate-based authentication between all hosts.

```yaml
all:
  hosts:
    bastion1.example.com: {}
    bastion2.example.com: {}
    bastion3.example.com: {}
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

#### Managed Host to Unmanaged Host

Sets up a tunnel to a remote host not managed by Ansible, like an appliance.
The shared key should come from Vault.

```yaml
all:
  vars:
    vpn_connections:
      - auth_method: psk
        auto: start
        shared_key_content: !vault |
          $ANSIBLE_VAULT;1.2;AES256;dev
          ....
        hosts:
          this_host:
            leftid: idoftheclient
          nfsserver:
            hostname: nfsserver.example.com
            rightid: idoftheserver
```

## Configuring Opportunistic Mesh VPN

You can configure an opportunistic mesh VPN by setting `opportunistic` to `true` on a connection.
This includes all hosts in the Ansible inventory in the mesh configuration.

**Note:** When configuring an opportunistic mesh VPN using a control node that shares the same CIDR as one or more mesh CIDRs, add a `clear` policy entry for the control node CIDR to prevent SSH connection loss during the play.

### Variables

<a id="vpn_opportunistic"></a>**vpn_opportunistic** (`bool`) - Whether opportunistic mesh configuration should be used by default for connections that do not override this setting.
Default: `false`.

<a id="vpn_default_policy"></a>**vpn_default_policy** (`str`) - Default opportunistic mesh policy group applied to target machines.
Use `private` for encrypted traffic, `private-or-clear` for opportunistic encryption, or `clear` for unencrypted traffic.
Choices: `private`, `private-or-clear`, `clear`.
Default: `private-or-clear`.

### Example Playbooks

#### Opportunistic Mesh VPN Configuration

This example overrides the default policy to `private` and adds a `clear` exception for the controller machine.

```yaml
all:
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

## Firewall and SELinux

The firewall must be configured to allow traffic on 500/UDP, 4500/UDP, and 4500/TCP ports for the IKE, ESP, and AH protocols.

**NOTE:** [`vpn_manage_firewall`](#vpn_manage_firewall) and [`vpn_manage_selinux`](#vpn_manage_selinux) are limited to *adding* ports and policy, respectively.
They cannot be used for *removing* them.
If you want to remove ports or policy, use the firewall or selinux role directly.

### Variables

<a id="vpn_manage_firewall"></a>**vpn_manage_firewall** (`bool`) - Whether the role should manage IPsec firewall ports 500/UDP, 4500/UDP, and 4500/TCP using the firewall role.
Default: `false`.

<a id="vpn_manage_selinux"></a>**vpn_manage_selinux** (`bool`) - Whether the role should manage IPsec port SELinux settings using the selinux role.
Default: `false`.

<a id="vpn_secure_logging"></a>**vpn_secure_logging** (`bool`) - Whether to suppress potentially sensitive output from tasks that handle credentials, secrets, and other sensitive data.
Default: `true`.

## rpm-ostree

See README-ostree.md

## License

MIT
