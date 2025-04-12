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

GitHub Action workflow run ansible sanity tests on ``ansible core 2.17``, ``ansible core 2.18`` and ``devel``

.. code-block:: yaml+jinja

    sanity:
      name: Sanity (Ⓐ${{ matrix.ansible }})
      strategy:
        matrix:
          ansible:
            - stable-2.17
            - stable-2.18
            - devel

      runs-on: ubuntu-latest

      steps:
        - name: Perform sanity testing
          id: sanity_tests
          uses: ansible-community/ansible-test-gh-action@release/v1
          with:
            ansible-core-version: ${{ matrix.ansible }}
            testing-type: sanity
            codecov-token: ${{ secrets.CODECOV_TOKEN }}
            coverage: ${{ github.event_name == 'schedule' && 'always' || 'never' }}
            pull-request-change-detection: true