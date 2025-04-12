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

.. toctree::

   tests_sanity
   tests_unit
   tests_integration
