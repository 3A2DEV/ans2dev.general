# 3A2DEV General Collection for Ansible
<!-- Add CI and code coverage badges here. Samples included below. -->
![collection](https://img.shields.io/badge/ansible-collection-blue?logo=ansible&logoColor=white)
![automation](https://img.shields.io/badge/ansible-automation-blue?logo=ansible&logoColor=white)
![galaxy](https://img.shields.io/badge/ansible-galaxy-blue?logo=ansible&logoColor=white)
![module](https://img.shields.io/badge/ansible-module-blue?logo=ansible&logoColor=white)
![roles](https://img.shields.io/badge/ansible-roles-blue?logo=ansible&logoColor=white)

[![collection-release](https://img.shields.io/github/v/release/3A2DEV/a2dev.general?display_name=release&logo=ansible&logoColor=white)](https://galaxy.ansible.com/ui/repo/published/3A2DEV/a2dev.general/) [![CI](https://github.com/3A2DEV/a2dev.general/actions/workflows/ansible-test.yml/badge.svg?event=push)](https://github.com/3A2DEV/a2dev.general/actions) [![Codecov](https://img.shields.io/codecov/c/github/3A2DEV/a2dev.general?logo=codecov)](https://codecov.io/gh/3A2DEV/a2dev.general)

<!-- Describe the collection and why a user would want to use it. What does the collection do? -->

This repository contains the `a2dev.general` Ansible Collection and includes some modules and plugins supported by **3A2DEV** which are not part of more specialized collections.

## Code of Conduct

Although this collection is not part of the Ansible community, we adhere to their Code of Conduct for a better experience for everyone.

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Contributing to this collection

Don't know how to start? Refer to the [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html)!

Want to submit code changes? Take a look at the [Quick-start development guide](https://docs.ansible.com/ansible/devel/community/create_pr_quick_start.html).

We also use the following guidelines:

* [Collection review checklist](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_reviewing.html)
* [Ansible development guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible collection development guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Collection maintenance

The current maintainers are listed in the [MAINTAINERS](MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

## Governance

<!--Describe how the collection is governed. Here can be the following text:-->

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!

## Tested with Ansible

Tested with the current `ansible-core 2.17` and `ansible-core 2.18` releases and the current development version of ansible-core. Ansible-core versions before `2.16.0` are not supported. This includes all ansible-base `2.10` and Ansible `2.9` releases.

## External requirements

Some modules and plugins require external libraries. Please check the requirements for each plugin or module you use in the documentation to find out which requirements are needed.

## Included content

Please check the included content on the Ansible Galaxy page for this collection

## Using this collection

<!--Include some quick examples that cover the most common use cases for your collection content. It can include the following examples of installation and upgrade (change NAMESPACE.COLLECTION_NAME correspondingly):-->

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install a2dev.general
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: a2dev.general
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install a2dev.general --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `0.1.0`:

```bash
ansible-galaxy collection install a2dev.general:==0.1.0
```

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

You can olso install all python dependencies via role:

```yaml
  - name: Install Dependencies on CN
    hosts: all
    gather_facts: no
    roles:
      - role: a2dev.general.install_dep
```
```yaml
  # install in pre_tasks with become: false
  - name: Install Dependencies on CN
    hosts: all
    gather_facts: no

    pre_tasks:

      - name: install dependencies
        block:
          - include_role:
              name: a2dev.general.install_dep
        become: false
```

## Release notes

See the [changelog](https://github.com/3A2DEV/a2dev.general/tree/main/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## Licensing

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
