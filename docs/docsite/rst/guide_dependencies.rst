..
  Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.ans2dev.general.docsite.guide_dependencies:

Install Modules Dependencies
============================

Some modules and plugins require external libraries.

Please check the requirements for each plugin or module you use in the documentation to find out which requirements are needed.

You can install all python dependencies via ``install_dep`` role:

Role requirements
-----------------

* `ansible.builtin.slurp <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/slurp_module.html>`_
* `ansible.builtin.set_fact <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html>`_ 
* `ansible.builtin.pip <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/pip_module.html>`_

Usage
-----

.. code-block:: yaml+jinja

  - name: Install Dependencies on CN
    hosts: all
    gather_facts: no
    roles:
      - role: ans2dev.general.install_dep

You can olso install in ``pre_tasks`` with ``become: false``

.. code-block:: yaml+jinja

  - name: Install Dependencies on CN
    hosts: all
    gather_facts: no

    pre_tasks:

      - name: install dependencies
        block:
          - include_role:
              name: ans2dev.general.install_dep
        become: false
