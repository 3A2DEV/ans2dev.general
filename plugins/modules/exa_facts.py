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
module: exa_facts
author:
    - Marco Noce (@NomakCooper)
description:
    - Gathers facts about Oracle Exadata Machine.
    - This module currently supports Oracle Exadata Machine.
version_added: "0.1.0"
requirements:
  - /usr/local/bin/imageinfo
  - /usr/sbin/exadata.img.hw
  - /usr/sbin/dmidecode
  - /opt/oracle.SupportTools/onecommand/databasemachine.xml
short_description: Gathers facts about Oracle Exadata Machine and rack.
notes:
  - |
    This module shows imageinfo attribute, exadata img hw, dmidecode system info and content of databasemachine.xml.
'''

EXAMPLES = r'''
- name: Gather exa info
  a2dev.general.exa_facts:
'''

RETURN = r'''
ansible_facts:
  description: Dictionary containing exadata machine info
  returned: always
  type: complex
  contains:
    exa_img:
      description: imageinfo parameter.
      returned: always
      type: list
      contains:
        Image image type:
          description: The image type.
          returned: always
          type: str
          sample: "production"
        Kernel version:
          description: Kernel Version.
          returned: always
          type: str
          sample: "4.14.35-2047.518.4.2.el7uek.x86_64..."
        Image created:
          description: Image creation date and time.
          returned: always
          type: str
          sample: "2023-03-02 03:40:44 -0800"
        Image status:
          description: Image status.
          returned: always
          type: str
          sample: "success"
        Uptrack kernel version:
          description: Uptrack kernel version.
          returned: always
          type: str
          sample: "4.14.35-2047.522.3.el7uek.x86_64..."
        Node type:
          description: Node type.
          returned: always
          type: str
          sample: "GUEST"
        Image version:
          description: Image version.
          returned: always
          type: str
          sample: "22.1.9.0.0.230302"
        System partition on device:
          description: System partition volume.
          returned: always
          type: str
          sample: "/dev/mapper/VGExaDb-LVDbSys2"
        Image label:
          description: Image label.
          returned: always
          type: str
          sample: "OSS_22.1.9.0.0_LINUX.X64_230302"
        Image kernel version:
          description: Image kernel version.
          returned: always
          type: str
          sample: "4.14.35-2047.518.4.2.el7uek"
        Install type:
          description: Install type.
          returned: always
          type: str
          sample: "XEN Guest with InfiniBand"
        Image activated:
          description: Image activated date and time.
          returned: always
          type: str
          sample: "2023-09-02 04:02:42 +0200"
    exa_hw:
      description: value from exadata.img.hw command.
      returned: always
      type: list
      contains:
        model:
          description: Machine Model.
          returned: always
          type: str
          sample: "HVM domU"
    system_info:
      description: paramenter from dmidecode command.
      returned: always
      type: list
      contains:
        SKU Number:
          description: SKU Number.
          returned: always
          type: str
          sample: "B88854"
        UUID:
          description: UUID.
          returned: always
          type: str
          sample: "089271ba-b91f-4230-acce-be01a22fab09"
        Family:
          description: Family.
          returned: always
          type: str
          sample: "Not Specified"
        Serial Number:
          description: Family.
          returned: always
          type: str
          sample: "089271ba-b91f-4230-acce-be01a22fab09"
        Version:
          description: Version.
          returned: always
          type: str
          sample: "4.4.4OVM"
        Product Name:
          description: Product Name.
          returned: always
          type: str
          sample: "HVM domU"
        Wake-up Type:
          description: Wake-up Type.
          returned: always
          type: str
          sample: "Power Switch"
        Manufacturer:
          description: Manufacturer.
          returned: always
          type: str
          sample: "Xen"
    databasemachine:
      description: Complex dict created by databasemachine.xml file.
      returned: always
      type: list
      contains:
        ORACLE_CLUSTER:
          description: All item in xml file.
          returned: always
          type: dict
'''

import sys
if sys.version_info < (3, 3):
    FileNotFoundError = IOError

import platform
import os
import xml.etree.ElementTree as ET
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.basic import AnsibleModule


def which(binary_name):
    for path in os.environ.get("PATH", "").split(os.pathsep):
        full_path = os.path.join(path, binary_name)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    raise FileNotFoundError("Binary '{}' not found in PATH or not executable.".format(binary_name))


def locate_binary(binary_name):
    return which(binary_name)


def img_parse(raw):
    results = {}
    for line in raw.splitlines():
        if line.strip():
            param, _unused, value = line.partition(":")
            param = param.strip()
            value = value.strip()
            if param and value:
                results[param] = value
    return results


def hw_parse(raw):
    results = {}
    for line in raw.splitlines():
        if line.strip():
            value = line
            results['model'] = value
    return results


def parse_xml_to_dict(xml_file, module):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        def element_to_dict(element):
            result = {}
            for child in element:
                child_dict = element_to_dict(child) if len(child) else child.text
                if child.tag in result:
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(child_dict)
                else:
                    result[child.tag] = child_dict
            return result

        return {root.tag: element_to_dict(root)}

    except ET.ParseError:
        module.fail_json(msg="Error parsing XML file.")
    except FileNotFoundError:
        module.fail_json(msg="XML file not found.")
    except Exception:
        module.fail_json(msg="Error processing XML file.")


def dmidecode_parse(raw):
    in_system_info = False
    results = {}
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("System Information"):
            in_system_info = True
            continue
        if in_system_info:
            if not line or line.startswith("Handle "):
                break
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                results[key] = value
    return results


def main():
    imageinfo_args = ['-all']
    hw_args = ['--get', 'model']
    dmidecode_args = ['-t', 'system']

    module = AnsibleModule(
        argument_spec={},
        supports_check_mode=True,
    )

    if platform.system() != 'Linux':
        module.fail_json(msg='Module not supported on this platform')

    result = {
        'changed': False,
        'ansible_facts': {
            'exa_img': [],
            'exa_hw': [],
            'databasemachine': {},
            'system_info': {}
        }
    }

    try:

        bin_path_imageinfo = "/usr/local/bin/imageinfo"
        bin_path_hw = "/usr/sbin/exadata.img.hw"
        bin_path_dmidecode = "/usr/sbin/dmidecode"

        if not os.path.isfile(bin_path_imageinfo) or not os.access(bin_path_imageinfo, os.X_OK):
            bin_path_imageinfo = locate_binary("imageinfo")

        if not os.path.isfile(bin_path_hw) or not os.access(bin_path_hw, os.X_OK):
            bin_path_hw = locate_binary("exadata.img.hw")

        if not os.path.isfile(bin_path_dmidecode) or not os.access(bin_path_dmidecode, os.X_OK):
            bin_path_dmidecode = locate_binary("dmidecode")

        rc, stdout, stderr = module.run_command([bin_path_imageinfo] + imageinfo_args)
        if rc == 0:
            result['ansible_facts']['exa_img'] = img_parse(stdout)

        rc, stdout, stderr = module.run_command([bin_path_hw] + hw_args)
        if rc == 0:
            result['ansible_facts']['exa_hw'] = hw_parse(stdout)

        xml_file = '/opt/oracle.SupportTools/onecommand/databasemachine.xml'
        if os.path.exists(xml_file):
            databasemachine_info = parse_xml_to_dict(xml_file, module)
            result['ansible_facts']['databasemachine'] = databasemachine_info
        else:
            result['ansible_facts']['databasemachine'] = None

        rc, stdout, stderr = module.run_command([bin_path_dmidecode] + dmidecode_args)
        if rc == 0:
            system_info = dmidecode_parse(stdout)
            result['ansible_facts']['system_info'] = system_info

    except Exception as e:
        module.fail_json(msg=to_native(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
