..
  Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.ans2dev.general.docsite.tests_sanity:

Ansible Sanity
==============

Sanity tests are made up of scripts and tools used to perform static code analysis. 

The primary purpose of these tests is to enforce Ansible coding standards and requirements.

To run sanity tests in a container:

.. code-block:: bash

    ansible-test sanity --docker -v plugins/modules/$MODULE_NAME.py

GitHub Action workflow run ansible sanity tests on ``ansible core 2.17`` and ``ansible core 2.18``
