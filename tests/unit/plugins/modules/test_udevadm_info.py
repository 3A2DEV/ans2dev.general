# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from unittest.mock import patch, MagicMock

from ansible_collections.ans2dev.general.plugins.modules import udevadm_info  # type: ignore


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestUdevadmInfoModule(unittest.TestCase):
    def run_udev_test(self, test_params, fake_output, expected_fact_key, expected_sample_value):
        with patch('ansible_collections.ans2dev.general.plugins.modules.udevadm_info.AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = test_params
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            fake_module.run_command.return_value = (0, fake_output, "")
            fake_module.get_bin_path.return_value = "/usr/sbin/udevadm"
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                udevadm_info.main()
            result_str = str(context.exception)
            self.assertIn(expected_fact_key, result_str)
            self.assertIn(expected_sample_value, result_str)

    def test_full_info(self):
        fake_output = (
            "DEVPATH='/devices/pci0000:00/0000:00:03.0/virtio0/host0/target0:0:1/0:0:1:0/block/sda'\n"
            "DEVNAME='/dev/sda'\n"
            "DEVTYPE='disk'\n"
            "DEVLINKS='/dev/disk/by-path/path1 /dev/disk/by-id/id1'\n"
        )
        test_params = {"device": "/dev/sda"}
        self.run_udev_test(
            test_params,
            fake_output,
            "DEVPATH",
            "/devices/pci0000:00/0000:00:03.0/virtio0/host0/target0:0:1/0:0:1:0/block/sda"
        )

    def test_specific_property(self):
        fake_output = "DEVTYPE='disk'\n"
        test_params = {"device": "/dev/sda", "property": "DEVTYPE"}
        self.run_udev_test(test_params, fake_output, "DEVTYPE", "disk")

    def test_multivalued_property(self):
        fake_output = "DEVLINKS='/dev/disk/by-path/path1 /dev/disk/by-id/id1 /dev/disk/by-id/id2'\n"
        test_params = {"device": "/dev/sda", "property": "DEVLINKS"}
        with patch('ansible_collections.ans2dev.general.plugins.modules.udevadm_info.AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = test_params
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            fake_module.run_command.return_value = (0, fake_output, "")
            fake_module.get_bin_path.return_value = "/usr/sbin/udevadm"
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                udevadm_info.main()
            result_str = str(context.exception)

            self.assertIn("DEVLINKS", result_str)
            self.assertIn("['/dev/disk/by-path/path1', '/dev/disk/by-id/id1', '/dev/disk/by-id/id2']", result_str)

    def test_fail_command(self):
        fake_output = ""
        test_params = {"device": "/dev/sda"}
        with patch('ansible_collections.ans2dev.general.plugins.modules.udevadm_info.AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = test_params
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            fake_module.run_command.return_value = (1, fake_output, "Error executing command")
            fake_module.get_bin_path.return_value = "/usr/sbin/udevadm"
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                udevadm_info.main()
            result_str = str(context.exception)
            self.assertIn("fail_json called", result_str)
            self.assertIn("Error executing command", result_str)


if __name__ == '__main__':
    unittest.main()
