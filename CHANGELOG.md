Changelog
=========

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
- update to tox-lsr 2.4.0 - add support for ansible-test sanity with docker
- CI: Add support for RHEL-9

[1.0.0] - 2021-02-11
--------------------

### Initial Release
