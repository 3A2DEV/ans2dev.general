..
  Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.ans2dev.general.docsite.guide_install:

Install Collection
========================

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

.. code-block:: bash

    ansible-galaxy collection install ans2dev.general

You can also include it in a ``requirements.yml`` file and install it with the command below:

.. code-block:: bash

    ansible-galaxy collection install -r requirements.yml

using the format:

.. code-block:: yaml+jinja

    ---
    collections:
    - name: ans2dev.general

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the ``ansible`` package.

To upgrade the collection to the latest available version, run the following command:

.. code-block:: bash

    ansible-galaxy collection install ans2dev.general --upgrade

You can also install a specific version of the collection.
Use the following syntax to install version ``0.1.0``:

.. code-block:: bash

    ansible-galaxy collection install ans2dev.general:==0.1.0

