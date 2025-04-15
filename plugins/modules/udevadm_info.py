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
module: udevadm_info
short_description: Collect udevadm device information.
description:
  - Retrieves C(udevadm) information using C(udevadm info) commands.
  - Collects all properties avaible in udevadm for the selected device.
version_added: "0.2.0"
options:
  device:
    description:
      - Device full name.
      - O(device) is passed as an argument to the C(udevadm) command, so the name must be complete.
      - For example for C(sda) disk you must use the full name V(/dev/sda).
    required: true
    type: str
  property:
    description:
      - This option is used if you want to collect only a specific property of the specified O(device).
      - For example you can collect only the V(DEVTYPE) property.
    required: false
    type: str
requirements:
  - C(udevadm info) command with C(-x), C(--query), C(--property) and C(--name) options.
author:
  - Marco Noce (@NomakCooper)
notes:
  - Module requires C(register) function in order to access to the collected info.
  - Some device properties, like V(DEVLINKS), can have multiple values,
    so the module will report the values of that specific property as a C(list) rather than as a C(string).
'''

EXAMPLES = r'''
---
# Get full udevadm info for /dev/sda
- name: Get full udevadm info for /dev/sda
  ans2dev.general.udevadm_info:
    device: "/dev/sda"
  register: result

# Print SCSI_VENDOR from example above
- name: Print SCSI_VENDOR of /dev/sda
  ansible.builtin.debug:
    var: result.udevinfo.SCSI_VENDOR

# Get only DEVPATH property from udevadm info for /dev/sda
- name: Get only DEVPATH property from udevadm info for /dev/sda
  ans2dev.general.udevadm_info:
    device: "/dev/sda"
    property: "DEVPATH"
  register: result
'''

RETURN = r'''
udevinfo:
  description:
    - Dictionary of C(udevadm info) properties.
    - Additional fields will be returned depending on C(udevadm) version or OS distribution.
  returned: success
  type: dict
  elements: dict
  contains:
    DEVPATH:
      description:
        - The C(sysfs) path of the device in the Linux device tree.
        - Indicates its physical location.
      returned: always
      type: str
      sample: "/devices/pci0000:00/0000:00:03.0/virtio0/host0/target0:0:1/0:0:1:0/block/sda"
    DEVNAME:
      description:
        - The device node name in /dev used for interacting with the device.
      returned: always
      type: str
      sample: "/dev/sda"
    DEVTYPE:
      description:
        - Specifies the type of device.
      returned: always
      type: str
      sample: "disk"
    DISKSEQ:
      description:
        - A sequence number assigned to the disk, which can be used for ordering.
      returned: always
      type: str
      sample: "9"
    MAJOR:
      description:
        - The major device number identifying the kernel driver associated with the device.
      returned: always
      type: str
      sample: "8"
    MINOR:
      description:
        - The minor device number that distinguishes between devices handled by the same driver.
      returned: always
      type: str
      sample: "0"
    SUBSYSTEM:
      description:
        - Indicates the kernel subsystem to which the device belongs.
      returned: always
      type: str
      sample: "block"
    USEC_INITIALIZED:
      description:
        - A microsecond timestamp indicating when udev initialized the device.
      returned: always
      type: str
      sample: "3900986"
    SCSI_TPGS:
      description:
        - Indicates SCSI Target Port Group Support.
      returned: always
      type: str
      sample: "0"
    SCSI_TYPE:
      description:
        - Specifies the SCSI device type.
      returned: always
      type: str
      sample: "disk"
    SCSI_VENDOR:
      description:
        - The vendor name of the SCSI device.
      returned: always
      type: str
      sample: "Google"
    SCSI_VENDOR_ENC:
      description:
        - Encoded vendor name of the SCSI device, with escape sequences for special characters.
      returned: always
      type: str
      sample: "Google\\x20\\x20"
    SCSI_MODEL:
      description:
        - The model identifier of the SCSI device.
      returned: always
      type: str
      sample: "PersistentDisk"
    SCSI_MODEL_ENC:
      description:
        - Encoded version of the SCSI model, including escape sequences where needed.
      returned: always
      type: str
      sample: "PersistentDisk\\x20\\x20"
    SCSI_REVISION:
      description:
        - Specifies the hardware or firmware revision of the SCSI device.
      returned: always
      type: str
      sample: "1"
    ID_SCSI:
      description:
        - A flag confirming that the device was identified by the SCSI subsystem.
      returned: always
      type: str
      sample: "1"
    ID_SCSI_INQUIRY:
      description:
        - Indicates that a SCSI inquiry command was successfully executed on the device.
      returned: always
      type: str
      sample: "1"
    SCSI_IDENT_LUN_VENDOR:
      description:
        - Combines SCSI identification details and LUN vendor information to aid in device grouping.
      returned: always
      type: str
      sample: "workspace"
    ID_VENDOR:
      description:
        - Provides the vendor identifier for the device, similar to RV(udevinfo.SCSI_VENDOR).
      returned: always
      type: str
      sample: "Google"
    ID_VENDOR_ENC:
      description:
        - Encoded vendor identifier, with escape sequences for any special characters.
      returned: always
      type: str
      sample: "Google\\x20\\x20"
    ID_MODEL:
      description:
        - Identifies the device model, analogous to RV(udevinfo.SCSI_MODEL).
      returned: always
      type: str
      sample: "PersistentDisk"
    ID_MODEL_ENC:
      description:
        - Encoded version of the device model, including escape sequences if necessary.
      returned: always
      type: str
      sample: "PersistentDisk\\x20\\x20"
    ID_REVISION:
      description:
        - The revision number, firmware or hardware, of the device.
      returned: always
      type: str
      sample: "1"
    ID_TYPE:
      description:
        - Specifies the general type of the device.
      returned: always
      type: str
      sample: "disk"
    ID_BUS:
      description:
        - Indicates the bus type used by the device.
      returned: always
      type: str
      sample: "scsi"
    ID_SERIAL:
      description:
        - A unique serial number assigned to the device for identification purposes.
      returned: always
      type: str
      sample: "0Google_PersistentDisk_workspace"
    ID_SERIAL_SHORT:
      description:
        - A shortened version of the device serial number for simpler reference.
      returned: always
      type: str
      sample: "workspace"
    MPATH_SBIN_PATH:
      description:
        - Specifies the path to the multipath binaries, used in environments managing multipath storage.
      returned: always
      type: str
      sample: "/sbin"
    DM_MULTIPATH_DEVICE_PATH:
      description:
        - Indicates the status or state of the device under device-mapper multipath management.
      returned: always
      type: str
      sample: "0"
    ID_PATH:
      description:
        - Provides a unique, stable path to the device based on its physical bus location.
      returned: always
      type: str
      sample: "pci-0000:00:03.0-scsi-0:0:1:0"
    ID_PATH_TAG:
      description:
        - A sanitized version of RV(udevinfo.ID_PATH) that is safe for use as a tag or filename.
      returned: always
      type: str
      sample: "pci-0000_00_03_0-scsi-0_0_1_0"
    ID_PART_TABLE_UUID:
      description:
        - The universally unique identifier C(UUID) of the disk partition table, critical for GPT disks.
      returned: always
      type: str
      sample: "942239ee-556f-4244-af35-7f6516dba76f"
    ID_PART_TABLE_TYPE:
      description:
        - pecifies the type of partition table, such as GPT or MBR.
      returned: always
      type: str
      sample: "gpt"
    DEVLINKS:
      description:
        - A list of symlink paths generated by udev for stable device naming.
      returned: always
      type: list
      elements: str
      sample:
        - "/dev/disk/by-path/pci-0000:00:03.0-scsi-0:0:1:0"
        - "/dev/disk/by-id/scsi-0Google_PersistentDisk_workspace"
        - "/dev/disk/by-diskseq/9"
        - "/dev/disk/by-id/google-workspace"
    TAGS:
      description:
        - Metadata tags applied to the device by udev, used for classification and rule matching.
      returned: always
      type: str
      sample: ":systemd:"
    CURRENT_TAGS:
      description:
        - The set of currently active tags on the device, indicating its runtime state.
      returned: always
      type: str
      sample: ":systemd:"
'''

from ansible.module_utils.basic import AnsibleModule
import re


def run_udevadm(module, device, prop, udevadm_cmd):

    cmd = [udevadm_cmd, "info", "-x", "--no-pager", "--query=property"]
    if prop:
        cmd.append("--property=" + prop)
    cmd.append("--name=" + device)

    rc, stdout, stderr = module.run_command(cmd)

    if rc != 0:
        module.fail_json(msg="Error running udevadm", rc=rc, stderr=stderr, cmd=' '.join(cmd))

    return parse_output(stdout)


def parse_output(output):
    info = {}

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        m = re.match(r"^(\S+)=['\"](.*)['\"]$", line)

        if m:
            key = m.group(1)
            value = m.group(2)
            values = [v for v in value.split() if v]

            if len(values) == 1:
                info[key] = values[0]
            elif len(values) > 1:
                info[key] = values
            else:
                info[key] = value
    return info


def main():
    module = AnsibleModule(
        argument_spec=dict(
            device=dict(required=True, type='str'),
            property=dict(required=False, type='str')
        ),
        supports_check_mode=True
    )

    device = module.params.get("device")
    prop = module.params.get("property")
    udevadm_cmd = module.get_bin_path('udevadm', required=True)

    udevinfo = run_udevadm(module, device, prop, udevadm_cmd)
    module.exit_json(changed=False, udevinfo=udevinfo)


if __name__ == "__main__":
    main()
