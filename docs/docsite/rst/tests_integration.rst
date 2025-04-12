..
  Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.ans2dev.general.docsite.tests_integration:

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