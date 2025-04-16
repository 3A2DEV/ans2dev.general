# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from unittest.mock import patch, MagicMock

from ansible_collections.ans2dev.general.plugins.modules import udevadm_verify  # type: ignore


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestUdevadmVerifyModule(unittest.TestCase):
    def setUp(self):
        patcher = patch(
            'ansible_collections.ans2dev.general.plugins.modules.udevadm_verify.AnsibleModule'
        )
        self.mock_module_class = patcher.start()
        self.addCleanup(patcher.stop)

        self.fake_module = MagicMock()
        self.fake_module.exit_json.side_effect = exit_json
        self.fake_module.fail_json.side_effect = fail_json
        self.mock_module_class.return_value = self.fake_module

    def run_main(self):
        with self.assertRaises(Exception) as context:
            udevadm_verify.main()
        return str(context.exception)

    def test_no_style_true(self):
        sample_output = (
            "/etc/udev/rules.d/70-snap.snapd.rules:224 style: whitespace after comma is expected.\n"
            "/etc/udev/rules.d/70-snap.snapd.rules:225 style: whitespace after comma is expected.\n"
            "\n"
            "1 udev rules files have been checked.\n"
            "  Success: 1\n"
            "  Fail:    0\n"
        )
        self.fake_module.params = {
            'src': '/etc/udev/rules.d/70-snap.snapd.rules',
            'no_style': True,
            'resolve_names': 'early',
        }
        self.fake_module.check_mode = False
        self.fake_module.run_command.return_value = (0, sample_output, "")
        self.fake_module.get_bin_path.return_value = "/usr/sbin/udevadm"

        result = self.run_main()
        self.assertIn("'verify':", result)
        self.assertIn("'Success': '1'", result)
        self.assertIn("'Fail': '0'", result)
        self.assertIn("'line': '224'", result)
        self.assertIn("whitespace after comma is expected", result)

    def test_default_style(self):
        sample_output = (
            "/etc/udev/rules.d/70-snap.snapd.rules:224 style: whitespace after comma is expected.\n"
            "/etc/udev/rules.d/70-snap.snapd.rules:225 style: whitespace after comma is expected.\n"
            "/etc/udev/rules.d/70-snap.snapd.rules: udev rules have style issues.\n"
            "\n"
            "1 udev rules files have been checked.\n"
            "  Success: 0\n"
            "  Fail:    1\n"
        )
        self.fake_module.params = {
            'src': '/etc/udev/rules.d/70-snap.snapd.rules',
            'no_style': False,
            'resolve_names': 'early',
        }
        self.fake_module.check_mode = False
        self.fake_module.run_command.return_value = (1, sample_output, "")
        self.fake_module.get_bin_path.return_value = "/usr/sbin/udevadm"

        result = self.run_main()
        self.assertIn("'Success': '0'", result)
        self.assertIn("'Fail': '1'", result)
        self.assertNotIn('ud ... have style issues', result)

    def test_never_no_style(self):
        sample_output = (
            "/etc/udev/rules.d/70-snap.snapd.rules:224 style: whitespace after comma is expected.\n"
            "/etc/udev/rules.d/70-snap.snapd.rules:225 style: whitespace after comma is expected.\n"
            "\n"
            "1 udev rules files have been checked.\n"
            "  Success: 1\n"
            "  Fail:    0\n"
        )
        self.fake_module.params = {
            'src': '/etc/udev/rules.d/70-snap.snapd.rules',
            'no_style': True,
            'resolve_names': 'never',
        }
        self.fake_module.check_mode = False
        self.fake_module.run_command.return_value = (0, sample_output, "")
        self.fake_module.get_bin_path.return_value = "/usr/sbin/udevadm"

        result = self.run_main()
        self.assertIn("'Success': '1'", result)
        self.assertIn("'Fail': '0'", result)

    def test_exec_error(self):
        self.fake_module.params = {
            'src': '/etc/udev/rules.d/70-snap.snapd.rules',
            'no_style': True,
            'resolve_names': 'early',
        }
        self.fake_module.check_mode = False
        self.fake_module.run_command.return_value = (2, "", "execution error")
        self.fake_module.get_bin_path.return_value = "/usr/sbin/udevadm"

        result = self.run_main()
        self.assertIn("fail_json called", result)
        self.assertIn("execution error", result)


if __name__ == '__main__':
    unittest.main()
