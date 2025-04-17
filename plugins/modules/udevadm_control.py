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
module: udevadm_control
short_description: Reload udev rules.
description:
  - Reload udev rules using C(udevadm control) command.
version_added: "0.2.0"
options:
  log_level:
    description:
      - Set C(--log-level) option value.
    required: false
    type: str
    choices: [ emerg, alert, crit, err, warning, notice, info, debug ]
requirements:
  - C(udevadm control) command with C(--reload) and C(--log-level) options.
author:
  - Marco Noce (@NomakCooper)
notes:
  - Module requires C(register) function in order to access to the collected info.
  - Module return RV(udevcontrol.stdout) and RV(udevcontrol.stderr) from C(udevadm control) command.
'''

EXAMPLES = r'''
---
# Reload udev rules
- name: Reload udev rules
  ans2dev.general.udevadm_control:
    log_level: debug
  register: result

# Reload udev rules with debug level
- name: Reload with debug log_level
  ans2dev.general.udevadm_control:
    log_level: debug
  register: result
'''

RETURN = r'''
udevcontrol:
  description:
    - C(udevadm control) output.
  returned: always
  type: dict
  elements: dict
  contains:
    stdout:
      description:
        - C(udevadm control) stdout command.
      returned: always
      type: str
      sample: ""
    stderr:
      description:
        - C(udevadm control) stderr command.
      returned: always
      type: str
      sample: ""
'''

from ansible.module_utils.basic import AnsibleModule


def build_command(udevadm_path, log_level):
    cmd = [udevadm_path, 'control', '--reload']
    if log_level:
        cmd.extend(['--log-level', log_level])
    return cmd


def run_udevadm_control(module, udevadm_path, log_level):
    cmd = build_command(udevadm_path, log_level)
    rc, out, err = module.run_command(cmd, check_rc=False)

    if rc != 0:
        module.fail_json(
            msg="udevadm control command failed",
            rc=rc,
            stdout=out,
            stderr=err
        )

    return {'stdout': out, 'stderr': err}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            log_level=dict(
                required=False,
                type='str',
                choices=['emerg', 'alert', 'crit', 'err', 'warning', 'notice', 'info', 'debug']
            ),
        ),
        supports_check_mode=True
    )

    log_level = module.params.get('log_level')
    udevadm = module.get_bin_path('udevadm', required=True)

    if module.check_mode:
        module.exit_json(changed=True, udevcontrol={'stdout': '', 'stderr': ''})

    result = run_udevadm_control(module, udevadm, log_level)

    module.exit_json(changed=True, udevcontrol=result)


if __name__ == "__main__":
    main()
