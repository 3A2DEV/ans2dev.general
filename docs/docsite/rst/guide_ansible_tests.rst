..
  Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.ans2dev.general.docsite.guide_ansible_tests:

Ansible Tests
=============

Each module is tested with the current ``ansible-core 2.17`` and ``ansible-core 2.18`` releases and the current development version of ansible-core. 

.. warning::
    Ansible-core versions before ``2.16.0`` are not supported. This includes all ansible-base ``2.10`` and Ansible ``2.9`` releases.

Each Ansible test is executed through a ``GitHub Actions`` workflow following a specific strategy and matrix for Ansible version and Python version.

Ansible Sanity
==============

Sanity tests are made up of scripts and tools used to perform static code analysis. 

The primary purpose of these tests is to enforce Ansible coding standards and requirements.

To run sanity tests in a container:

.. code-block:: bash

    ansible-test sanity --docker -v plugins/modules/$MODULE_NAME.py

GitHub Action workflow run ansible sanity tests on ``ansible core 2.17`` and ``ansible core 2.18``

Ansible Units
=============

Unit tests are small isolated tests that target a specific library or module.

Unit tests in Ansible are currently the only way of driving tests from python within Ansible’s continuous integration process. 

This means that in some circumstances the tests may be a bit wider than just units.

To run units tests in a container:

.. code-block:: bash

    ansible-test units --docker -v $MODULE_NAME

GitHub Action workflow run ansible unit tests on ``ansible core 2.17`` and ``ansible core 2.18``

Ansible Integration
===================

Integration tests are functional tests of modules and plugins. 

With integration tests, we check if a module or plugin satisfies its functional requirements. 

Simply put, we check that features work as expected and users get the outcome described in the module or plugin documentation.

To run integration tests in a container:

.. code-block:: bash

    ansible-test integration --docker -v $MODULE_NAME

To run integration tests in a specific docker image :

.. code-block:: bash

    ansible-test integration --docker $DOCKER_IMAGE -v $MODULE_NAME

GitHub Action workflow run ansible integration tests on the following matrix:

+----------------------+----------------+
| Ansible core version | Python version |
+======================+================+
| Stable 2.17          | 3.7            |
+----------------------+----------------+
| Stable 2.17          | 3.8            |
+----------------------+----------------+
| Stable 2.17          | 3.9            |
+----------------------+----------------+
| Stable 2.17          | 3.10           |
+----------------------+----------------+
| Stable 2.17          | 3.11           |
+----------------------+----------------+
| Stable 2.17          | 3.12           |
+----------------------+----------------+
| Stable 2.18          | 3.8            |
+----------------------+----------------+
| Stable 2.18          | 3.9            |
+----------------------+----------------+
| Stable 2.18          | 3.10           |
+----------------------+----------------+
| Stable 2.18          | 3.11           |
+----------------------+----------------+
| Stable 2.18          | 3.12           |
+----------------------+----------------+
| Stable 2.18          | 3.13           |
+----------------------+----------------+

Ansible Integration tests olso run on the following Official Docker Image:

+----------------------+--------------+----------------+
| Ansible core version | Docker Image | Python version |
+======================+==============+================+
| Stable 2.18          | alpine320    | 3.12           |
+----------------------+--------------+----------------+
| Stable 2.18          | fedora40     | 3.12           |
+----------------------+--------------+----------------+
| Stable 2.18          | ubuntu2204   | 3.10           |
+----------------------+--------------+----------------+
| Stable 2.18          | ubuntu2404   | 3.12           |
+----------------------+--------------+----------------+

