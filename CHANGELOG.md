Changelog
=========

[1.5.3] - 2023-01-20
--------------------

### New Features

- none

### Bug Fixes

- Clean up non-inclusive words.
- ansible-lint 6.x fixes (#86)

### Other Changes

- Add check for non-inclusive language (#82)
- Add CodeQL workflow for GitHub code scanning (#83)
- update ignore files for ansible-test 2.14 (#89)

[1.5.2] - 2022-11-21
--------------------

### New Features

- none

### Bug Fixes

- only check for firewall ipsec service if managing firewall (#76)

Some systems use `firewalld` by default.  We should only expect the
`ipsec` service is present if the test tells the vpn role to manage
firewall or selinux.

### Other Changes

- none

[1.5.1] - 2022-11-14
--------------------

### New Features

- none

### Bug Fixes

- none

### Other Changes

- fix markdown to adoc conversion (#73)

long heading causes problems with md to adoc conversion

The long heading causes problems with md to adoc conversion.  Shorten
the length by using abbreviations.

[1.5.0] - 2022-11-01
--------------------

### New Features

- Use the firewall role and the selinux role from the vpn role (#70)

- Introduce vpn_manage_firewall to enable the firewall role to manage
  the ipsec service. vpn_manage_firewall is set to false, by default.
  If the variable is set to false, the firewall configuration is
  disabled.

- Introduce vpn_manage_selinux to enable the selinux role to manage
  the ports defined in the firewall ipsec service. vpn_manage_selinux
  is set to false, by default. If the variable is set to false, the
  selinux configuration is disabled.

- Add the test check task check_firewall_selinux.yml for verify the
  ports status.

- Add meta/collection-requirements.yml

### Bug Fixes

- none

### Other Changes

- none

[1.4.0] - 2022-09-19
--------------------

### New Features

- Various improvements required to connect to a managed remote host (#65)

Add support for the parameters shared_key_content, leftid, rightid, ike, esp, type, ikelifetime, salifetime, retransmit_timeout, dpddelay, dpdtimeout, dpdaction, leftupdown

### Bug Fixes

- Check for /usr/bin/openssl on controller - do not use package_facts (#66)

Check for existence of openssl without using sudo on the controller
Basically, any task, even package_facts:, will use sudo if using
become=true - so just use "exists" test to check for /usr/bin/openssl

### Other Changes

- Fix a bash bug in changelog_to_tag.yml, which unexpectedly expanded "*" (#62)

- changelog_to_tag action - github action ansible test improvements

- Use GITHUB_REF_NAME as name of push branch; fix error in branch detection [citest skip] (#64)

We need to get the name of the branch to which CHANGELOG.md was pushed.

[1.3.5] - 2022-07-19
--------------------

### New Features

- none

### Bug Fixes

- none

### Other Changes

- gather network facts default_ipv4 default_ipv6 (#56)

    * Gather fact subset `network` instead of `min`
    * Ensure facts `default_ipv4` and `default_ipv6`
    * Ensure all tests work when using ANSIBLE_GATHERING=explicit

- make min_ansible_version a string in meta/main.yml (#57)

The Ansible developers say that `min_ansible_version` in meta/main.yml
must be a `string` value like `"2.9"`, not a `float` value like `2.9`.

- Add CHANGELOG.md (#58)

[1.3.4] - 2022-05-06
--------------------

### New Features

- none

### Bug Fixes

- none

### Other Changes

- bump tox-lsr version to 2.11.0; remove py37; add py310
- Add tests::no\_serialization tag

[1.3.3] - 2022-04-13
--------------------

### New Features

- support gather\_facts: false; support setup-snapshot.yml

### Bug Fixes

- none

### Other Changes

- bump tox-lsr version to 2.10.1

[1.3.2] - 2022-02-09
--------------------

### New Features

- System Roles should consistently use ansible\_managed in configuration files it manages

### Bug Fixes

- none

### Other Changes

- none

[1.3.1] - 2022-02-08
--------------------

### New Features

- script to convert vpn\_ipaddr to FQCN

### Bug Fixes

- none

### Other Changes

- bump tox-lsr version to 2.9.1

[1.3.0] - 2022-01-10
--------------------

### New Features

- use custom vpn\_ipaddr filter

### Bug Fixes

- none

### Other Changes

- bump tox-lsr version to 2.8.3
- change recursive role symlink to individual role dir symlinks
- Run the new tox test

[1.2.2] - 2021-11-08
--------------------

### New Features

- support python 39, ansible-core 2.12, ansible-plugin-scan

### Bug Fixes

- none

### Other Changes

- update tox-lsr version to 2.7.1
- add netaddr dep for qemu
- Add meta/requirements.yml; support ansible-core 2.11
- Modifications and clarifications to the readme

[1.2.1] - 2021-09-15
--------------------

### New Features

- none

### Bug Fixes

- do not use json\_query - not needed here
- use wait\_for\_connection instead of wait\_for with ssh

### Other Changes

- use apt-get install -y
- use tox-lsr version 2.5.1

[1.2.0] - 2021-08-10
--------------------

### New Features

- Drop support for Ansible 2.8 by bumping the Ansible version to 2.9

### Bug Fixes

- none

### Other Changes

- none

[1.1.0] - 2021-05-13
--------------------

### New Features

- Remove RHEL6/CentOS6 files from vars directory
- Add support for rhel7 managed hosts
- Update conn naming scheme and leftid/rightid values
- VPN role v2 \(mesh encryption use case\).

### Bug Fixes

- Cleaning up ansible-lint errors
- Bugfix/leftid ip for certs
- fix ansible-test issues

### Other Changes

- Remove python-26 environment from tox testing
- update to tox-lsr 2.4.0 - add support for ansible-test with docker
- CI: Add support for RHEL-9

[1.0.0] - 2021-02-11
--------------------

### Initial Release
