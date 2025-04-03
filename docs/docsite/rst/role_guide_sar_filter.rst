..
  Copyright (c) Ansible Project
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.ans2dev.general.docsite.role_guide_sar_filter:

ans2dev.general sar_filter role
===============================

``sar_filter`` is a role designed to independently filter the data exported by the ``ans2dev.general.sar_facts`` module.

This role is designed to create lists with standard and simple filters.

With ``sar_filter``, you can autonomously create lists to pass to the ``ans2dev.general.charts`` module.

The role generate simple filters and not complex condition.

Role requirements
-----------------

* `ansible.builtin.fail <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fail_module.html>`_
* `ansible.builtin.set_fact <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html>`_ 
* `ans2dev.general.sar_facts <https://3a2dev.github.io/collectiondocs/sar_facts_module.html#ansible-collections-ans2dev-general-sar-facts-module>`_

Role Variables
--------------

+------------------+------------+----------+----------+---------------------------------------------------------------------------------------------------------------------------+
| Parameter        | Type       | Required | Default  | Description                                                                                                               |
+==================+============+==========+==========+===========================================================================================================================+
| ``source``       | ``string`` | Yes      | ``None`` | The SAR fact source to filter (e.g., ``sar_cpu``, ``sar_mem``, ``sar_net``, ``sar_disk``, ``sar_swap``).                  |
+------------------+------------+----------+----------+---------------------------------------------------------------------------------------------------------------------------+
| ``filter_by``    | ``string`` | Yes      | ``None`` | Defines if the filtering is by ``timestamp`` or ``datavalue``.                                                            |
+------------------+------------+----------+----------+---------------------------------------------------------------------------------------------------------------------------+
| ``result_fact``  | ``string`` | Yes      | ``None`` | Name of the fact that will store the filtered data.                                                                       |
+------------------+------------+----------+----------+---------------------------------------------------------------------------------------------------------------------------+
| ``datavalue_key``| ``string`` | No       | ``None`` | The key of the SAR fact to extract (e.g., ``%usr``, ``%memused``, ``rxpck/s``). Required if ``filter_by == "datavalue"``. |
+------------------+------------+----------+----------+---------------------------------------------------------------------------------------------------------------------------+
| ``iface_filter`` | ``string`` | No       | ``None`` | Defines which network interface (``IFACE``) to filter when using ``sar_net``. Required if ``source == "sar_net"``.        |
+------------------+------------+----------+----------+---------------------------------------------------------------------------------------------------------------------------+
| ``dev_filter``   | ``string`` | No       | ``None`` | Defines which disk device (``DEV``) to filter when using ``sar_disk``. Required if ``source == "sar_disk"``.              |
+------------------+------------+----------+----------+---------------------------------------------------------------------------------------------------------------------------+

Dependencies
------------

Before using this role, it is necessary to use the ``ans2dev.general.sar_facts`` module.
This role is based on its data collected.

Usage
-----

Filter data from ``ans2dev.general.sar_facts`` and pass it to ``ans2dev.general.charts``:

.. code-block:: yaml+jinja

    # ========================= CPU USAGE CHART =========================
    - name: Extract CPU Usage Data (Timestamp)
      include_role:
        name: ans2dev.general.sar_filter
      vars:
        source: "sar_cpu"
        filter_by: "timestamp"
        result_fact: "cpu_usage"

    - name: Extract CPU % User
      include_role:
        name: ans2dev.general.sar_filter
      vars:
        source: "sar_cpu"
        filter_by: "datavalue"
        datavalue_key: "%user"
        result_fact: "cpu_usr"

    - name: Extract CPU % System
      include_role:
        name: ans2dev.general.sar_filter
      vars:
        source: "sar_cpu"
        filter_by: "datavalue"
        datavalue_key: "%system"
        result_fact: "cpu_sys"

    - name: Extract CPU % IO Wait
      include_role:
        name: ans2dev.general.sar_filter
      vars:
        source: "sar_cpu"
        filter_by: "datavalue"
        datavalue_key: "%iowait"
        result_fact: "cpu_iowait"

    - name: Generate CPU Usage Chart
      ans2dev.general.charts:
        titlechart: "CPU Usage Over Time"
        type: "line"
        xaxis: "{{ cpu_usage_timestamp }}"
        xaxisname: "Timestamp"
        yaxis:
          - "{{ cpu_usr_values }}"
          - "{{ cpu_sys_values }}"
          - "{{ cpu_iowait_values }}"
        yaxisname: ["User %", "System %", "IO Wait %"]
        yaxiscolor: ["red", "blue", "orange"]
        path: "/tmp"
        filename: "cpu_usage"
        format: "png"

.. code-block:: yaml+jinja

    # ========================= NETWORK USAGE CHART =========================
    - name: Extract Network Data (eth0)
      include_role:
        name: ans2dev.general.sar_filter
      vars:
        source: "sar_net"
        filter_by: "timestamp"
        iface_filter: "eth0"
        result_fact: "net_eth0"

    - name: Extract Packets Received (eth0)
      include_role:
        name: ans2dev.general.sar_filter
      vars:
        source: "sar_net"
        filter_by: "datavalue"
        datavalue_key: "rxpck/s"
        iface_filter: "eth0"
        result_fact: "net_eth0_rx"

    - name: Extract Packets Sent (eth0)
      include_role:
        name: ans2dev.general.sar_filter
      vars:
        source: "sar_net"
        filter_by: "datavalue"
        datavalue_key: "txpck/s"
        iface_filter: "eth0"
        result_fact: "net_eth0_tx"

    - name: Generate Network Packets Chart (eth0)
      ans2dev.general.charts:
        titlechart: "Network Packets Received & Sent (eth0)"
        type: "bar"
        xaxis: "{{ net_eth0_timestamp }}"
        xaxisname: "Timestamp"
        yaxis:
          - "{{ net_eth0_rx_values }}"
          - "{{ net_eth0_tx_values }}"
        yaxisname: ["RX Packets", "TX Packets"]
        yaxiscolor: ["blue", "orange"]
        path: "/tmp"
        filename: "net_eth0"
        format: "png"