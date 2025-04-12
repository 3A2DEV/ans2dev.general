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

GitHub Action workflow run ansible unit tests on ``ansible core 2.17``, ``ansible core 2.18`` and ``devel``

.. code-block:: yaml+jinja

    units:
      runs-on: ubuntu-latest

      name: Units (Ⓐ${{ matrix.ansible }})
      strategy:
        fail-fast: true
        matrix:
          ansible:
            - stable-2.17
            - stable-2.18
            - devel

      steps:
        - name: >-
            Perform unit testing against
            Ansible version ${{ matrix.ansible }}
          id: units_tests
          uses: ansible-community/ansible-test-gh-action@release/v1
          with:
            ansible-core-version: ${{ matrix.ansible }}
            codecov-token: ${{ secrets.CODECOV_TOKEN }}
            coverage: ${{ github.event_name == 'schedule' && 'always' || 'never' }}
            testing-type: units
            test-deps: >-
              ansible.netcommon
              ansible.utils
            pull-request-change-detection: true