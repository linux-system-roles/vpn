Changelog
=========

[1.6.11] - 2025-07-02
--------------------

### Other Changes

- ci: Bump sclorg/testing-farm-as-github-action from 3 to 4 (#195)
- ci: bump tox-lsr to 3.8.0; rename qemu/kvm tests (#196)
- ci: Add Fedora 42; use tox-lsr 3.9.0; use lsr-report-errors for qemu tests (#197)
- ci: Add support for bootc end-to-end validation tests (#198)
- ci: Use ansible 2.19 for fedora 42 testing; support python 3.13 (#199)
- refactor: Ansible 2.19 support (#200)

[1.6.10] - 2025-04-23
--------------------

### Other Changes

- ci: ansible-plugin-scan is disabled for now (#182)
- ci: bump ansible-lint to v25; provide collection requirements for ansible-lint (#185)
- ci: Check spelling with codespell (#186)
- ci: Add test plan that runs CI tests and customize it for each role (#187)
- ci: In test plans, prefix all relate variables with SR_ (#188)
- ci: Fix bug with ARTIFACTS_URL after prefixing with SR_ (#189)
- tests: for vpn_connections, use specific nodes instead of all (#190)
- ci: several changes related to new qemu test, ansible-lint, python versions, ubuntu versions (#191)
- ci: use tox-lsr 3.6.0; improve qemu test logging (#192)
- ci: skip storage scsi, nvme tests in github qemu ci (#193)

[1.6.9] - 2025-01-09
--------------------

### Other Changes

- ci: Bump codecov/codecov-action from 4 to 5 (#178)
- ci: Use Fedora 41, drop Fedora 39 (#179)
- ci: Use Fedora 41, drop Fedora 39 - part two (#180)

[1.6.8] - 2024-11-05
--------------------

### Other Changes

- docs: vpn_ipaddr filter requires vpn_ipaddr.yml for docs (#176)

[1.6.7] - 2024-10-30
--------------------

### Other Changes

- ci: Add tft plan and workflow (#162)
- ci: Update fmf plan to add a separate job to prepare managed nodes (#164)
- ci: Bump sclorg/testing-farm-as-github-action from 2 to 3 (#165)
- ci: Add workflow for ci_test bad, use remote fmf plan (#166)
- ci: Fix missing slash in ARTIFACTS_URL (#167)
- ci: Add tags to TF workflow, allow more [citest bad] formats (#170)
- ci: ansible-test action now requires ansible-core version (#171)
- ci: add YAML header to github action workflow files (#172)
- refactor: Use vars/RedHat_N.yml symlink for CentOS, Rocky, Alma wherever possible (#174)

[1.6.6] - 2024-07-02
--------------------

### Bug Fixes

- fix: add support for EL10 (#160)

### Other Changes

- test: stop firewall after tests that use firewall (#158)
- ci: ansible-lint action now requires absolute directory (#159)

[1.6.5] - 2024-06-11
--------------------

### Other Changes

- ci: use tox-lsr 3.3.0 which uses ansible-test 2.17 (#153)
- ci: tox-lsr 3.4.0 - fix py27 tests; move other checks to py310 (#155)
- ci: Add supported_ansible_also to .ansible-lint (#156)

[1.6.4] - 2024-04-04
--------------------

### Other Changes

- ci: Bump codecov/codecov-action from 3 to 4 (#147)
- ci: fix python unit test - copy pytest config to tests/unit (#148)
- ci: Bump ansible/ansible-lint from 6 to 24 (#149)
- ci: Bump mathieudutour/github-tag-action from 6.1 to 6.2 (#151)

[1.6.3] - 2024-01-16
--------------------

### Other Changes

- ci: Bump actions/setup-python from 4 to 5 (#142)
- ci: support ansible-lint and ansible-test 2.16 (#144)
- ci: Use supported ansible-lint action; run ansible-lint against the collection (#145)

[1.6.2] - 2023-12-08
--------------------

### Other Changes

- ci: bump actions/github-script from 6 to 7 (#139)
- refactor: get_ostree_data.sh use env shebang - remove from .sanity* (#140)

[1.6.1] - 2023-11-30
--------------------

### Other Changes

- tests: do not remove iproute when cleaning up (#137)

[1.6.0] - 2023-11-29
--------------------

### New Features

- feat: support for ostree systems (#134)

### Other Changes

- Bump actions/checkout from 3 to 4 (#126)
- ci: ensure dependabot git commit message conforms to commitlint (#129)
- ci: tox-lsr version 3.1.1 (#133)
- tests: add cleanup after each test (#135)

[1.5.9] - 2023-09-07
--------------------

### Other Changes

- ci: Add markdownlint, test_converting_readme, and build_docs workflows (#46)

  - markdownlint runs against README.md to avoid any issues with
    converting it to HTML
  - test_converting_readme converts README.md > HTML and uploads this test
    artifact to ensure that conversion works fine
  - build_docs converts README.md > HTML and pushes the result to the
    docs branch to publish dosc to GitHub pages site.
  - Fix markdown issues in README.md
  
  Signed-off-by: Sergei Petrosian <spetrosi@redhat.com>

- docs: Make badges consistent, run markdownlint on all .md files (#47)

  - Consistently generate badges for GH workflows in README RHELPLAN-146921
  - Run markdownlint on all .md files
  - Add custom-woke-action if not used already
  - Rename woke action to Woke for a pretty badge
  
  Signed-off-by: Sergei Petrosian <spetrosi@redhat.com>

- ci: Remove badges from README.md prior to converting to HTML (#48)

  - Remove thematic break after badges
  - Remove badges from README.md prior to converting to HTML
  
  Signed-off-by: Sergei Petrosian <spetrosi@redhat.com>

- docs: Make supported versions and README consistent (#49)

  - Add Postgresql version 15 into README
  
- ci: fix mode of vars/main.yml for ansible-test (#50)

[1.5.8] - 2023-07-19
--------------------

### Bug Fixes

- fix: facts being gathered unnecessarily (#120)

### Other Changes

- ci: Add pull request template and run commitlint on PR title only (#114)
- ci: Rename commitlint to PR title Lint, echo PR titles from env var (#115)
- ci: fix python 2.7 CI tests by manually installing python2.7 package (#116)
- ci: ansible-lint - ignore var-naming[no-role-prefix] (#117)
- ci: ansible-test ignores file for ansible-core 2.15 (#118)
- ci: ansible-lint - skip var-naming[read-only] (#119)

[1.5.7] - 2023-05-26
--------------------

### Other Changes

- docs: Consistent contributing.md for all roles - allow role specific contributing.md section
- docs: add Collection requirements section to README

[1.5.6] - 2023-04-27
--------------------

### Other Changes

- test: check generated files for ansible_managed, fingerprint
- ci: Add commitlint GitHub action to ensure conventional commits with feedback

[1.5.5] - 2023-04-13
--------------------

### Other Changes

- ansible-lint - use changed_when for conditional tasks (#104)

[1.5.4] - 2023-04-06
--------------------

### Other Changes

- Fix issues found by CodeQL (#93)
- Add README-ansible.md to refer Ansible intro page on linux-system-roles.github.io (#101)
- Fingerprint RHEL System Role managed config files (#102)

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
