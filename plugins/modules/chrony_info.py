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
  - Retrieves C(chrony) information using C(chronyd) and C(chronyc) commands.
  - Collects C(configuration), C(sources), C(sourcestat) and C(ntpdata) info based on O(mode) option.
  - Pay attention to the requirements section before using this module.
version_added: "0.2.0"
options:
  mode:
    description:
      - This option specifies which type of chrony data the module should collect.
      - V(conf) Returns the C(chronyd) configuration, as obtained from the C(chronyd -p) command.
      - V(sources) Returns a flat list of dict representing the NTP sources table, as collected from the C(chronyc -n sources) command.
      - V(sourcestats) Returns a flat list of dict representing the NTP source statistics, as gathered via the C(chronyc -n sourcestats) command.
      - V(ntpdata) Returns detailed NTP testing data from C(chronyc ntpdata) command for the configured servers.
    required: true
    type: str
    choices: ['conf', 'sources', 'sourcestats', 'ntpdata']
  IP:
    description:
      - This option is only applicable when O(mode) is V(ntpdata).
      - It allows you to limit the data collection to a single NTP server by specifying its IP address.
      - When used with V(ntpdata) in O(mode) module collects only the data for the provided NTP server IP.
    required: false
    type: str
requirements:
  - C(chronyd) command with C(-p) option.
  - C(chronyc) command with C(-n) C(sources), C(sourcestats) and C(ntpdata) options.
  - C(chronyd.service) must be C(running) to use V(sources), V(sourcestats) and V(ntpdata) in O(mode) option.
author:
  - Marco Noce (@NomakCooper)
notes:
  - Module requires C(register) function in order to access to the collected info.
  - Module commands require C(chronyd.service) in C(running) state.
'''

EXAMPLES = r'''
---
# Collect chronyd configuration
- name: Get chrony configuration info
  ans2dev.general.chrony_info:
    mode: conf
  register: result

# Collect sources data
- name: Get chrony sources table
  ans2dev.general.chrony_info:
    mode: sources
  register: result

# Collect sourcestats data
- name: Get chrony sourcestats table
  ans2dev.general.chrony_info:
    mode: sourcestats
  register: result

# Collect all ntpdata information from all configured servers
- name: Get chrony ntpdata info for all servers
  ans2dev.general.chrony_info:
    mode: ntpdata
  register: result

# Collect ntpdata only for a specific server
- name: Get chrony ntpdata info for a specific server
  ans2dev.general.chrony_info:
    mode: ntpdata
    IP: "100.110.92.1"
  register: result
'''

RETURN = r'''
conf:
  description:
    - Dictionary of C(chronyd) configuration from C(chronyd -p) command.
    - Additional fields will be returned depending on configuration file.
  returned: when O(mode) is V(conf).
  type: dict
  elements: dict
  contains:
    driftfile:
      description:
        - This file stores the measured clock drift of the system.
        - C(chrony) uses the drift value to make continuous adjustments to the local clock.
      returned: if RV(conf.driftfile) is in the configuration.
      type: str
      sample: /var/lib/chrony/drif
    keyfile:
      description:
        - This file contains authentication keys.
        - It helps secure NTP exchanges.
      returned: if RV(conf.keyfile) is in the configuration.
      type: str
      sample: /etc/chrony.keys
    leapsectz:
      description:
        - This setting specifies the time zone context used when applying leap second corrections.
      returned: if RV(conf.leapsectz) is in the configuration.
      type: str
      sample: right/UTC
    logdir:
      description:
        - This directory is where C(chrony) writes its log files.
      returned: if RV(conf.logdir) is in the configuration.
      type: str
      sample: /var/log/chrony
    makestep:
      description:
        -  The makestep directive controls when C(chrony) will step the system clock rather than slowly slewing it.
      returned: if RV(conf.makestep) is in the configuration.
      type: str
      sample: 1.0 3
    ntsdumpdir:
      description:
        - This directory is used by C(chrony) to store a dump of NTP data.
      returned: if RV(conf.ntsdumpdir) is in the configuration.
      type: str
      sample: /var/lib/chrony
    rtcsync:
      description:
        - When set to true, this option instructs C(chrony) to synchronize the Real Time Clock C(RTC) with the system clock.
      returned: if RV(conf.rtcsync) is in the configuration.
      type: bool
      sample: true
    server:
      description:
        - This is a list of NTP servers chrony uses to obtain the correct time.
        - The IP addresses are provided along with an additional option C(iburst).
        - Depending on configuration it return C(hostname) and not C(ip) server.
      returned: if RV(conf.server) is in the configuration.
      type: list
      elements: str
      sample: ["100.110.92.1 iburst", "91.149.253.184 iburst" ]
    sourcedir:
      description:
        - This directory contains additional configuration files or sources provided dynamically.
      returned: if RV(conf.sourcedir) is in the configuration.
      type: str
      sample: /run/chrony-dhcp
sources:
  description:
    - Dictionary of C(chronyd) from C(chronyc -n sources) command.
    - Additional fields will be returned depending on C(chrony) or C(OS Distribution).
  returned: when O(mode) is V(sources).
  type: list
  elements: dict
  contains:
    MS:
      description:
        - This field contains a status indicator for the source.
      returned: always
      type: str
      sample: '^?'
    Name/IP address:
      description:
        - This field contains the hostname or IP address of the NTP source.
      returned: always
      type: str
      sample: 100.110.92.1
    Stratum:
      description:
        - This field represents the stratum level of the NTP server.
      returned: always
      type: str
      sample: 0
    Poll:
      description:
        - This is the polling interval, expressed typically as a power-of-two exponent in seconds.
      returned: always
      type: str
      sample: 8
    Reach:
      description:
        - This represents the reachability register for the source.
        - It is an 8-bit shift register that records the success or failure of recent attempts to contact the time server.
      returned: always
      type: str
      sample: 0
    LastRx:
      description:
        - This field indicates how long ago the last valid packet was received from the source.
      returned: always
      type: str
      sample: '-'
    Last sample:
      description:
        - This column reports the most recent time measurement information received from the source.
      returned: always
      type: str
      sample: '+0ns[ +0ns] +/- 0ns'
sourcestat:
  description:
    - Dictionary of C(chronyd) from C(chronyc -n sourcestats) command.
    - Additional fields will be returned depending on C(chrony) or C(OS Distribution).
  returned: when O(mode) is V(sourcestats).
  type: list
  elements: dict
  contains:
    Name/IP Address:
      description:
        - The hostname or IP address of the NTP source from which measurements are taken.
      returned: always
      type: str
      sample: 100.110.92.1
    NP:
      description:
        - Often represents the number of measurement samples or packets that have been successfully collected and used for statistical analysis.
      returned: always
      type: str
      sample: 0
    NR:
      description:
        - Indicates the number of rejected measurements.
      returned: always
      type: str
      sample: 0
    Span:
      description:
        - Represents the time span in seconds between the oldest and newest measurement sample used to compute the statistics.
      returned: always
      type: str
      sample: 0
    Frequency:
      description:
        - Reflects the average frequency offset or error of the local clock relative to the reference provided by the source.
        - It is expressed in a way that indicates how far off and in which direction the clock might be running.
      returned: always
      type: str
      sample: +0.000
    Freq Skew:
      description:
        - This value represents the variability or statistical dispersion of the measured frequency offsets.
      returned: always
      type: str
      sample: 2000.000
    Offset:
      description:
        - The average offset is the measured difference in time between the local system clock and the remote NTP source.
      returned: always
      type: str
      sample: +0ns
    Std Dev:
      description:
        - This is the standard deviation of the offset measurements.
        - The standard deviation gives a sense of the spread or dispersion of the offset values.
      returned: always
      type: str
      sample: 4000ms
ntpdata:
  description:
    - Dictionary of C(chronyd) from C(chronyc ntpdata) command for every configured server.
    - It is a complex dictionary that contains a dictionary for each configured IP.
    - If O(IP) is used it return only RV(ntpdata) info for the selected IP Address.
    - Additional fields will be returned depending on C(chrony) or C(OS Distribution).
  returned: when O(mode) is V(ntpdata).
  type: dict
  elements: dict
  contains:
    Authenticated:
      description:
        - Indicates whether the NTP data received from the server is authenticated.
      returned: always
      type: str
      sample: No
    Interleaved:
      description:
        - Shows whether the server is using interleaved from for packet exchange.
      returned: always
      type: str
      sample: No
    Jitter asymmetry:
      description:
        - Represents the asymmetry in network jitter between transmit and receive paths.
      returned: always
      type: str
      sample: +0.00
    Leap status:
      description:
        - Reports the leap second status.
      returned: always
      type: str
      sample: Normal
    Local address:
      description:
        - Provides the local network address and additional numeric code that the system is using for communicating with the remote NTP server.
      returned: always
      type: str
      sample: '[UNSPEC] (00000000)'
    Mode:
      description:
        - Indicates the NTP mode in which the server is operating.
      returned: always
      type: str
      sample: Invalid
    NTP tests:
      description:
        - Displays the results of various NTP internal tests.
        - The string consists of multiple sets of digits, with each group representing a particular outcome test.
      returned: always
      type: str
      sample: '000 000 0000'
    Offset:
      description:
        - Reflects the measured time difference between the local system clock and the remote NTP server clock.
      returned: always
      type: str
      sample: '+0.000000000 seconds'
    Peer delay:
      description:
        - Measures the delay between the local system and the peer.
      returned: always
      type: str
      sample: '0.000000000 seconds'
    Peer dispersion:
      description:
        - Represents the dispersion in delay measurements to the remote server.
      returned: always
      type: str
      sample: '0.000000000 seconds'
    Poll interval:
      description:
        - Shows the polling interval used by C(chrony).
      returned: always
      type: str
      sample: '0 (1 seconds)'
    Precision:
      description:
        - Indicates the precision of the system clock as measured by C(chrony).
      returned: always
      type: str
      sample: '0 (1.000000000 seconds)'
    RX timestamping:
      description:
        - Specifies the method used for timestamping incoming received packets.
      returned: always
      type: str
      sample: 'Invalid'
    Reference ID:
      description:
        - Identifies the reference clock or time source that the server uses as its basis.
      returned: always
      type: str
      sample: '00000000 ()'
    Reference time:
      description:
        - Shows the time at which the server last synchronized with its reference clock.
      returned: always
      type: str
      sample: 'Thu Jan 01 00:00:00 1970'
    Remote address:
      description:
        - Displays the remote NTP server IP address along with an accompanying numeric code.
      returned: always
      type: str
      sample: '100.110.92.1 (646E5C01)'
    Remote port:
      description:
        - Indicates the network port number used by the remote NTP server for communication.
      returned: always
      type: str
      sample: 123
    Response time:
      description:
        - Captures the round-trip time from when a request was sent to the remote server and when the response was received.
      returned: always
      type: str
      sample: '0.000000000 seconds'
    Root delay:
      description:
        - Represents the total round-trip delay to the primary reference clock.
      returned: always
      type: str
      sample: '0.000000 seconds'
    Root dispersion:
      description:
        - The dispersion associated with the root delay.
      returned: always
      type: str
      sample: '0.000000 seconds'
    Stratum:
      description:
        - Denotes the stratum level of the server.
        - Stratum 0 is reserved for high-precision timekeeping devices.
      returned: always
      type: str
      sample: 0
    TX timestamping:
      description:
        - Indicates the method used for timestamping outgoing transmitted packets.
      returned: always
      type: str
      sample: Invalid
    Total HW RX:
      description:
        - Reflects the total count of received packets that were processed using hardware timestamping.
      returned: always
      type: str
      sample: 0
    Total HW TX:
      description:
        - Indicates the total count of transmitted packets that were processed using hardware timestamping.
      returned: always
      type: str
      sample: 0
    Total RX:
      description:
        - The total number of packets received.
      returned: always
      type: str
      sample: 0
    Total TX:
      description:
        - The total number of packets transmitted to the server.
      returned: always
      type: str
      sample: 9
    Total good RX:
      description:
        - The number of received packets that passed internal validation checks.
      returned: always
      type: str
      sample: 0
    Total kernel RX:
      description:
        - Represents the number of packets received at the kernel level.
      returned: always
      type: str
      sample: 0
    Total kernel TX:
      description:
        - Represents the number of packets transmitted at the kernel level.
      returned: always
      type: str
      sample: 9
    Total valid RX:
      description:
        - The number of received packets that have been validated and considered correct by the NTP protocol criteria.
      returned: always
      type: str
      sample: 0
    Version:
      description:
        - Denotes the NTP protocol version used in the communication.
      returned: always
      type: str
      sample: 0
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
        if not line or ("MS" in line and "Name/IP address" in line):
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
        if not line or ("Name/IP Address" in line and "NP" in line):
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
            module.fail_json(msg="Failed to run chronyc ntpdata for server {}".format(server_ip), stderr=err)

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
        argument_spec=dict(
            mode=dict(required=True, type='str', choices=['conf', 'sources', 'sourcestats', 'ntpdata']),
            IP=dict(required=False, type='str'),
        ),
        supports_check_mode=True
    )

    data_mode = module.params.get('mode')
    ip_param = module.params.get('IP')

    chronyd_path = module.get_bin_path("chronyd", required=True)
    chronyc_path = module.get_bin_path("chronyc", required=True)

    result = None

    if data_mode == "conf":
        result = get_conf(module, chronyd_path)
        module.exit_json(changed=False, conf=result)

    elif data_mode == "sources":
        result = get_sources(module, chronyc_path)
        module.exit_json(changed=False, sources=result)

    elif data_mode == "sourcestats":
        result = get_sourcestat(module, chronyc_path)
        module.exit_json(changed=False, sourcestat=result)

    elif data_mode == "ntpdata":

        if ip_param:
            result = get_ntpdata(module, chronyc_path, [ip_param])
        else:

            conf = get_conf(module, chronyd_path)
            servers = conf.get("server", [])
            if not isinstance(servers, list):
                servers = [servers]
            result = get_ntpdata(module, chronyc_path, servers)
        module.exit_json(changed=False, ntpdata=result)

    else:
        module.fail_json(msg="Invalid option for 'mode': {}".format(data_mode))


if __name__ == "__main__":
    main()
