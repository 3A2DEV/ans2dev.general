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
module: udevadm_trigger
short_description: Trigger udev rules.
description:
  - Trigger udev rules using C(udevadm trigger) command.
version_added: "0.2.0"
options:
  quiet:
    description:
      - Set or not C(--quiet) option.
    required: true
    type: bool
  type:
    description:
      - Set the type of events to trigger.
    required: true
    type: str
    choices: [ all, devices, subsystems ]
requirements:
  - C(udevadm trigger) command with C(--quiet) and C(--type) options.
author:
  - Marco Noce (@NomakCooper)
notes:
  - Module requires C(register) function in order to access to the collected info.
  - Module return RV(udevtrigger.stdout) and RV(udevtrigger.stderr) from C(udevadm trigger) command.
'''

EXAMPLES = r'''
---
# Trigger all events
- name: Trigger all events
  ans2dev.general.udevadm_trigger:
    quiet: true
    type: all
  register: result

# Trigger devices events without quiet
- name: Trigger all events
  ans2dev.general.udevadm_trigger:
    quiet: false
    type: devices
  register: result

# Trigger subsystems events
- name: Trigger all events
  ans2dev.general.udevadm_trigger:
    quiet: true
    type: subsystems
  register: result
'''

RETURN = r'''
udevtrigger:
  description:
    - C(udevadm trigger) output.
  returned: always
  type: dict
  elements: dict
  contains:
    stdout:
      description:
        - C(udevadm trigger) stdout command.
      returned: always
      type: str
      sample: ""
    stderr:
      description:
        - C(udevadm trigger) stderr command.
      returned: always
      type: str
      sample: ""
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


def build_command(binary, quiet, event_type):
    cmd = [binary, 'trigger']
    if quiet:
        cmd.append('-q')
    cmd.append(f"--type={event_type}")
    return cmd


def run_trigger(module, binary, quiet, event_type):
    cmd = build_command(binary, quiet, event_type)
    rc, out, err = module.run_command(cmd)
    return rc, out, err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            type=dict(required=True, type='str', choices=['all', 'devices', 'subsystems']),
            quiet=dict(required=True, type='bool'),
        ),
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(changed=False)

    event_type = module.params['type']
    quiet = module.params['quiet']
    binary = module.get_bin_path('udevadm', required=True)

    try:
        rc, out, err = run_trigger(module, binary, quiet, event_type)
        if rc != 0:
            module.fail_json(msg="udevadm trigger command failed", rc=rc, stdout=out, stderr=err)

        module.exit_json(changed=True, udevtrigger={'stdout': out, 'stderr': err})
    except Exception as e:
        module.fail_json(msg="Unexpected error: %s" % to_native(e))


if __name__ == '__main__':
    main()
