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
module: udevadm_verify
short_description: Verify udev rules file.
description:
  - Verify udev rules file using C(udevadm verify) command.
version_added: "0.2.0"
options:
  src:
    description:
      - Udev rules file path to check.
      - Use full name like C(/etc/udev/rules.d/70-snap.snapd.rules)
    required: true
    type: str
  no_style:
    description:
      - This option is used to add or not the C(--no-style) option to C(udevadm verify) command.
    required: true
    type: bool
  resolve_names:
    description:
      - This option is used to indicate when to resolve names.
    required: true
    type: str
    choices: [ early, never ]
requirements:
  - C(udevadm verify) command with C(--resolve-names) and C(--no-style) options.
author:
  - Marco Noce (@NomakCooper)
notes:
  - Module requires C(register) function in order to access to the collected info.
'''

EXAMPLES = r'''
---
# Verify udev rules file
- name: Verify udev rules file
  ans2dev.general.udevadm_verify:
    src: "/etc/udev/rules.d/70-snap.snapd.rules"
    no_style: True
    resolve_names: "early"
  register: result

# Verify udev rules file without no-style and resolve_names=never
- name: Verify udev rules file
  ans2dev.general.udevadm_verify:
    src: "/etc/udev/rules.d/70-snap.snapd.rules"
    no_style: False
    resolve_names: "never"
  register: result
'''

RETURN = r'''
verify:
  description:
    - C(udevadm verify) dictionary result.
  returned: always
  type: dict
  elements: dict
  contains:
    Success:
      description:
        - Success check count.
      returned: always
      type: str
      sample: "1"
    Fail:
      description:
        - Failed check count.
      returned: always
      type: str
      sample: "0"
    stdout:
      description:
        - Errors from C(udevadm verify).
      returned: when errors are found in file.
      type: list
      elements: dict
      contains:
        file:
          description:
            - File name
          returned: always
          type: str
          sample: "/etc/udev/rules.d/70-snap.snapd.rules"
        line:
          description:
            - Line number in which the error occurs.
          returned: always
          type: str
          sample: "224"
        type:
          description:
            - The error Type.
          returned: always
          type: str
          sample: "style"
        error:
          description:
            - The error occurs.
          returned: always
          type: str
          sample: "whitespace after comma is expected."
'''

import re
from ansible.module_utils.basic import AnsibleModule


def build_command(udevadm_path, src, no_style, resolve_names):
    cmd = [udevadm_path, 'verify', f'--resolve-names={resolve_names}']
    if no_style:
        cmd.append('--no-style')
    cmd.append(src)
    return cmd


def parse_output(output):
    errors = []
    success_count = '0'
    fail_count = '0'

    err_pattern = re.compile(r'^(?P<file>[^:]+):(?P<line>\d+) (?P<type>\w+): (?P<error>.+)$')
    success_pattern = re.compile(r'^\s*Success:\s*(\d+)', re.IGNORECASE)
    fail_pattern = re.compile(r'^\s*Fail:\s*(\d+)', re.IGNORECASE)

    for line in output.splitlines():

        m = err_pattern.match(line)
        if m:
            errors.append({
                'file': m.group('file'),
                'line': m.group('line'),
                'type': m.group('type'),
                'error': m.group('error').strip(),
            })
            continue

        m = success_pattern.search(line)
        if m:
            success_count = m.group(1)
            continue

        m = fail_pattern.search(line)
        if m:
            fail_count = m.group(1)
            continue

    return {
        'Success': success_count,
        'Fail': fail_count,
        'stdout': errors,
    }


def run_verification(module, udevadm_path, src, no_style, resolve_names):
    cmd = build_command(udevadm_path, src, no_style, resolve_names)
    rc, out, err = module.run_command(cmd)

    full_output = ''
    if out:
        full_output += out
    if err:
        full_output += '\n' + err

    result = parse_output(full_output)

    if rc > 1:
        module.fail_json(msg='udevadm verify failed', rc=rc, stderr=err)

    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type='str', required=True),
            no_style=dict(type='bool', required=True),
            resolve_names=dict(type='str', required=True, choices=['early', 'never']),
        ),
        supports_check_mode=True
    )

    src = module.params['src']
    no_style = module.params['no_style']
    resolve_names = module.params['resolve_names']

    if module.check_mode:
        module.exit_json(changed=False)

    udevadm_path = module.get_bin_path('udevadm', required=True)

    try:
        udev_data = run_verification(module, udevadm_path, src, no_style, resolve_names)
    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=False, verify=udev_data)


if __name__ == '__main__':
    main()
