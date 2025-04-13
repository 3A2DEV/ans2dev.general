#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: chrony_info
short_description: Collect C(chrony) configuration and server info.
description:
  - Retrieves C(chrony) information using C(chronyd) and C(chronyc) command.
  - Collects C(configuration), C(sources), C(sourcestat) and C(ntpdata) info.
version_added: "0.2.0"
requirements:
  - C(chronyd) command.
  - C(chronyc) command.
author:
  - Marco Noce (@NomakCooper)
notes:
  - Module requires C(register) function in order to access to the collected info.
'''

EXAMPLES = r'''
---
# Collect Chrony information
- name: Collect chrony info
  ans2dev.general.chrony_info:
  register: result

# Print first server in configuration
- name: Print first server in configuration
  ansible.builtin.debug:
    var: result.conf.server[0]

# Set first server IP
- name: Set first server IP
  ansible.builtin.set_fact:
    server: "{{ (result.conf.server | first).split(' ')[0] }}"

# Get the poll value for the first server from sources
- name: Get the poll value for the first server from sources
  ansible.builtin.set_fact:
    first_server_poll: >-
      {{
        result.sources
        | selectattr('Name/IP address', 'equalto', server)
        | map(attribute='Poll')
        | first
      }}

# Get Offset for first server from sourcestat
- name: Get Offset for first server from sourcestat
  ansible.builtin.set_fact:
    first_server_offset: >-
      {{
        result.sourcestat
        | selectattr('Name/IP Address', 'equalto', server)
        | map(attribute='Offset')
        | first
      }}

# Print Precision for first server
- name: Print Precision for first server
  ansible.builtin.debug:
    var: result.ntpdata[server].Precision

# Print Peer dispersion for first server
- name: Print Peer dispersion for first server
  ansible.builtin.debug:
    var: result.ntpdata[server]['Peer dispersion']
'''

from ansible.module_utils.basic import AnsibleModule
import re


def get_conf(module, chronyd_path):
    rc, out, err = module.run_command([chronyd_path, "-p"])
    if rc != 0:
        module.fail_json(msg="Failed to run chronyd -p", stderr=err)

    conf = {}

    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        key = parts[0]
        value = " ".join(parts[1:]) if len(parts) > 1 else True

        if key in conf:
            if isinstance(conf[key], list):
                conf[key].append(value)
            else:
                conf[key] = [conf[key], value]
        else:
            conf[key] = value
    return conf


def parse_sources(output):
    rows = []

    for line in output.splitlines():
        line = line.strip()

        if not line or "MS" in line and "Name/IP address" in line:
            continue
        if re.match(r'^[\s=-]+$', line):
            continue
        tokens = re.split(r'\s+', line)

        if len(tokens) < 7:
            continue

        row = {
            "MS": tokens[0],
            "Name/IP address": tokens[1],
            "Stratum": tokens[2],
            "Poll": tokens[3],
            "Reach": tokens[4],
            "LastRx": tokens[5],
            "Last sample": " ".join(tokens[6:])
        }
        rows.append(row)
    return rows


def parse_sourcestat(output):
    header = ["Name/IP Address", "NP", "NR", "Span", "Frequency", "Freq Skew", "Offset", "Std Dev"]
    rows = []

    for line in output.splitlines():
        line = line.strip()

        if not line or "Name/IP Address" in line and "NP" in line:
            continue
        if re.match(r'^[\s=-]+$', line):
            continue
        tokens = re.split(r'\s+', line)
        if len(tokens) < len(header):
            continue
        row = dict(zip(header, tokens))
        rows.append(row)
    return rows


def get_sources(module, chronyc_path):
    rc, out, err = module.run_command([chronyc_path, "-n", "sources"])
    if rc != 0:
        module.fail_json(msg="Failed to run chronyc -n sources", stderr=err)

    return parse_sources(out)


def get_sourcestat(module, chronyc_path):
    rc, out, err = module.run_command([chronyc_path, "-n", "sourcestats"])
    if rc != 0:
        module.fail_json(msg="Failed to run chronyc -n sourcestats", stderr=err)

    return parse_sourcestat(out)


def get_ntpdata(module, chronyc_path, servers):
    ntpdata = {}
    if not isinstance(servers, list):
        servers = [servers]
    for server in servers:
        if server is True:
            continue

        server_ip = server.split()[0]
        rc, out, err = module.run_command([chronyc_path, "ntpdata", server_ip])
        if rc != 0:
            ntpdata[server_ip] = {
                "error": "Failed to run chronyc ntpdata for server {}".format(server_ip),
                "stderr": err
            }
            continue

        data = {}

        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
        ntpdata[server_ip] = data
    return ntpdata


def main():
    module = AnsibleModule(
        argument_spec={},
        supports_check_mode=True
    )

    chronyd_path = module.get_bin_path("chronyd", required=True)
    chronyc_path = module.get_bin_path("chronyc", required=True)

    conf = get_conf(module, chronyd_path)
    sources = get_sources(module, chronyc_path)
    sourcestat = get_sourcestat(module, chronyc_path)

    servers = conf.get("server", [])
    if not isinstance(servers, list):
        servers = [servers]
    ntpdata = get_ntpdata(module, chronyc_path, servers)

    module.exit_json(
        changed=False,
        conf=conf,
        sources=sources,
        sourcestat=sourcestat,
        ntpdata=ntpdata
    )


if __name__ == "__main__":
    main()
