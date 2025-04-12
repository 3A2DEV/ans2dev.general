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

.. code-block:: yaml

    integration:
      runs-on: ubuntu-latest

      name: Integration (Ⓐ${{ matrix.ansible }}+py${{ matrix.python }})
      strategy:
        fail-fast: false
        matrix:
          ansible:
            - devel
          python:
            - '3.8'
            - '3.9'
            - '3.10'
            - '3.11'
            - '3.12'
            - '3.13'
          include:
            - ansible: stable-2.17
              python: '3.7'
            - ansible: stable-2.17
              python: '3.8'
            - ansible: stable-2.17
              python: '3.9'
            - ansible: stable-2.17
              python: '3.10'
            - ansible: stable-2.17
              python: '3.11'
            - ansible: stable-2.17
              python: '3.12'
            # ansible-core 2.18
            - ansible: stable-2.18
              python: '3.8'
            - ansible: stable-2.18
              python: '3.9'
            - ansible: stable-2.18
              python: '3.10'
            - ansible: stable-2.18
              python: '3.11'
            - ansible: stable-2.18
              python: '3.12'
            - ansible: stable-2.18
              python: '3.13'


      steps:
        - name: >-
            Perform integration testing against
            Ansible version ${{ matrix.ansible }}
            under Python ${{ matrix.python }}
          id: integration_tests
          uses: ansible-community/ansible-test-gh-action@release/v1
          with:
            ansible-core-version: ${{ matrix.ansible }}
            codecov-token: ${{ secrets.CODECOV_TOKEN }}
            coverage: ${{ github.event_name == 'schedule' && 'always' || 'never' }}
            target-python-version: ${{ matrix.python }}
            testing-type: integration
            test-deps: ansible.netcommon
            pull-request-change-detection: true

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

.. code-block:: yaml

    docker-integration:
      runs-on: ubuntu-latest

      name: Docker Integration (Ⓐ${{ matrix.ansible }}+image-${{ matrix.image }})
      strategy:
        fail-fast: false
        matrix:
          ansible:
            - stable-2.18
          # - milestone
          image:
            - alpine320
            - fedora40
            - ubuntu2204
            - ubuntu2404


      steps:
        - name: >-
            Perform integration testing against
            Ansible version ${{ matrix.ansible }}
            on Docker image ${{ matrix.image }}
          id: docker_integration_tests
          uses: ansible-community/ansible-test-gh-action@release/v1
          with:
            ansible-core-version: ${{ matrix.ansible }}
            docker-image: ${{ matrix.image }}
            codecov-token: ${{ secrets.CODECOV_TOKEN }}
            coverage: ${{ github.event_name == 'schedule' && 'always' || 'never' }}
            testing-type: integration
            test-deps: ansible.netcommon
            pull-request-change-detection: true