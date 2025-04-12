..
  Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.ans2dev.general.docsite.tests_unit:

Ansible Units
=============

Unit tests are small isolated tests that target a specific library or module.

Unit tests in Ansible are currently the only way of driving tests from python within Ansible continuous integration process. 

This means that in some circumstances the tests may be a bit wider than just units.

To run units tests in a container:

.. code-block:: bash

    ansible-test units --docker -v $MODULE_NAME

GitHub Action workflow run ansible unit tests on ``ansible core 2.17`` and ``ansible core 2.18``