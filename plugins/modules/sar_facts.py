#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2025 Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: sar_facts
short_description: Collect info from sar.
description:
  - Retrieves SAR data using the C(sar) command from system logs.
  - Supports filtering by date range, time range, and partition details.
  - Returns performance metrics such as CPU utilization, memory usage, disk activity, and network statistics.
  - ans2dev.general.sar_facts only supports sar data with a V(12H) time format and automatically converts format to V(24H).
version_added: "0.1.0"
options:
  date_start:
    description: Start date for collecting SAR data (format YYYY-MM-DD).
    required: false
    type: str
  date_end:
    description: End date for collecting SAR data (format YYYY-MM-DD).
    required: false
    type: str
  time_start:
    description: Start time for collecting SAR data (format HH:MM:SS).
    required: false
    type: str
  time_end:
    description: End time for collecting SAR data (format HH:MM:SS).
    required: false
    type: str
  type:
    description: Type of SAR data to retrieve.
    choices: [ cpu, memory, swap, network, disk, load ]
    required: true
    type: str
  average:
    description: Whether to retrieve only the average values.
    required: false
    type: bool
    default: false
  partition:
    description: Whether to retrieve partition-specific disk statistics.
    required: false
    type: bool
    default: false
author:
  - Marco Noce (@NomakCooper)
'''

EXAMPLES = r'''
# Gather CPU performance metrics for a specific date and time range.
- name: Gather CPU SAR facts between 08:00 and 10:00
  ans2dev.general.sar_facts:
    date_start: "2025-05-01"
    date_end: "2025-05-01"
    time_start: "08:00:00"
    time_end: "10:00:00"
    type: cpu

# Gather memory usage SAR data for a single day.
- name: Retrieve memory usage data for a day
  ans2dev.general.sar_facts:
    date_start: "2025-05-01"
    type: memory

# Retrieve disk statistics with partition details.
- name: Gather disk usage statistics with partition information
  ans2dev.general.sar_facts:
    date_start: "2025-05-01"
    type: disk
    partition: true

# Retrieve average load statistics.
- name: Gather average load statistics
  ans2dev.general.sar_facts:
    date_start: "2025-05-01"
    type: load
    average: true
'''

RETURN = r'''
ansible_facts:
  description:
    - A dictionary containing the SAR data collected.
    - The value is a list of dictionaries where each dictionary represents a single data point.
    - V(date) The date for the measurement.
    - V(time) The time for the measurement in 24-hour format.
    - Additional keys corresponding to the performance metrics output from the C(sar) command.
  returned: always
  type: complex
  contains:
    sar_cpu:
      description:
        - Dictionary that contains C(cpu) data from C(sar).
        - It contains V(date), V(time) and all others keys from C(sar) data.
        - Most common keys are V(%user), V(%nice), V(%system), V(%idle) and others.
      returned: when O(type) is V(cpu).
      type: dict
    sar_mem:
      description:
        - Dictionary that contains C(memory) data from C(sar).
        - It contains V(date), V(time) and all others keys from C(sar) data.
        - Most common keys are V(%memused), V(%commit) and others.
      returned: when O(type) is V(memory).
      type: dict
    sar_swap:
      description:
        - Dictionary that contains C(swap) data from C(sar).
        - It contains V(date), V(time) and all others keys from C(sar) data.
        - Most common keys are V(%swpused), V(%swpcad) and others.
      returned: when O(type) is V(swap).
      type: dict
    sar_net:
      description:
        - Dictionary that contains C(network) data from C(sar).
        - It contains V(date), V(time) and all others keys from C(sar) data.
        - Most common keys are V(IFACE), V(rxpck/s), V(txpck/s), V(%ifutil) and others.
      returned: when O(type) is V(network).
      type: dict
    sar_disk:
      description:
        - Dictionary that contains C(disk) data from C(sar).
        - It contains V(date), V(time) and all others keys from C(sar) data.
        - Most common keys are V(DEV), V(%util), V(await), V(rkB/s), V(wkB/s) and others.
      returned: when O(type) is V(disk).
      type: dict
    sar_load:
      description:
        - Dictionary that contains C(load) data from C(sar).
        - It contains V(date), V(time) and all others keys from C(sar) data.
        - Most common keys are V(ldavg-1), V(ldavg-5), V(ldavg-15) and others.
      returned: when O(type) is V(load).
      type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from datetime import datetime, timedelta
import os

SAR_LOG_PATHS = ["/var/log/sa/", "/var/log/sysstat/"]

SAR_FACT_MAPPING = {
    "cpu": "sar_cpu",
    "memory": "sar_mem",
    "swap": "sar_swap",
    "network": "sar_net",
    "disk": "sar_disk",
    "load": "sar_load"
}


def find_sar_file(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        day = date_obj.strftime("%d")
        for path in SAR_LOG_PATHS:
            file_path = os.path.join(path, f"sa{day}")
            if os.path.exists(file_path):
                return file_path
    except ValueError:
        return None
    return None


def run_sar_command(module, sar_bin, sar_file, sar_type, time_start, time_end, partition, average, date_str):
    command = [sar_bin, "-f", sar_file]

    sar_flags = {
        "cpu": ["-u"],
        "memory": ["-r"],
        "swap": ["-S"],
        "network": ["-n", "DEV"],
        "disk": ["-d", "-p"] if partition else ["-d"],
        "load": ["-q"],
    }

    if sar_type in sar_flags:
        command.extend(sar_flags[sar_type])

    if time_start:
        command.extend(["-s", time_start])
    if time_end:
        command.extend(["-e", time_end])

    rc, stdout, stderr = module.run_command(command)
    if rc != 0:
        module.fail_json(msg=f"Failed to execute SAR command: {stderr}")
    return parse_sar_output(stdout, sar_type, average, date_str)


def convert_to_24h(time_str, am_pm):
    return datetime.strptime(f"{time_str} {am_pm}", "%I:%M:%S %p").strftime("%H:%M:%S")


def parse_sar_output(output, sar_type, average, date_str):
    import re
    parsed_data = []
    header = None

    def is_valid_time(token):
        return re.match(r'^\d{1,2}:\d{2}:\d{2}$', token)

    for line in output.splitlines():
        if re.search(r'\b(Linux|restart)\b', line, flags=re.IGNORECASE):
            continue

        parts = line.split()
        if not parts:
            continue

        if parts[0] == "Average:":
            parts = parts[1:]
            if not average:
                continue

        if header is None:
            if len(parts) >= 2 and is_valid_time(parts[0]) and parts[1] in ["AM", "PM"]:
                header = parts
            continue

        if len(parts) >= 2 and is_valid_time(parts[0]) and parts[1] in ["AM", "PM"]:
            converted = convert_to_24h(parts[0], parts[1])
            data_entry = {"date": date_str, "time": converted}
            for idx in range(1, min(len(header), len(parts))):
                data_entry[header[idx]] = parts[idx]
            parsed_data.append(data_entry)
        else:
            continue

    return parsed_data


def main():
    """Main execution of the Ansible module."""
    module_args = dict(
        date_start=dict(type="str", required=False, default=None),
        date_end=dict(type="str", required=False, default=None),
        time_start=dict(type="str", required=False, default=None),
        time_end=dict(type="str", required=False, default=None),
        type=dict(type="str", required=True, choices=['cpu', 'memory', 'swap', 'network', 'disk', 'load']),
        average=dict(type="bool", required=False, default=False),
        partition=dict(type="bool", required=False, default=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    params = module.params
    sar_type = params["type"]
    date_start = params["date_start"]
    date_end = params["date_end"]
    time_start = params["time_start"]
    time_end = params["time_end"]
    average = params["average"]
    partition = params["partition"]

    date_list = []
    if date_start and date_end:
        start_date = datetime.strptime(date_start, "%Y-%m-%d")
        end_date = datetime.strptime(date_end, "%Y-%m-%d")
        delta = (end_date - start_date).days

        if delta < 0:
            module.fail_json(msg="date_end cannot be before date_start.")

        date_list = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta + 1)]
    else:
        date_list = [date_start] if date_start else []

    collected_data = []

    sar_bin = module.get_bin_path("sar", required=True)

    for date in date_list:
        sar_file = find_sar_file(date)
        if sar_file:
            collected_data.extend(
                run_sar_command(
                    module,
                    sar_bin,
                    sar_file,
                    sar_type,
                    time_start,
                    time_end,
                    partition,
                    average,
                    date
                )
            )

    fact_name = SAR_FACT_MAPPING.get(sar_type, f"sar_{sar_type}")
    result = {'ansible_facts': {fact_name: collected_data}}
    module.exit_json(**result)


if __name__ == "__main__":
    main()
