# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from unittest.mock import patch, MagicMock

from ansible_collections.ans2dev.general.plugins.modules import udevadm_control  # type: ignore


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestUdevadmControlModule(unittest.TestCase):
    def setUp(self):
        patcher = patch(
            'ansible_collections.ans2dev.general.plugins.modules.udevadm_control.AnsibleModule'
        )
        self.mock_module_class = patcher.start()
        self.addCleanup(patcher.stop)

        self.fake_module = MagicMock()
        self.fake_module.exit_json.side_effect = exit_json
        self.fake_module.fail_json.side_effect = fail_json
        self.mock_module_class.return_value = self.fake_module

    def run_main(self):
        with self.assertRaises(Exception) as exc:
            udevadm_control.main()
        return str(exc.exception)

    def test_no_log_level(self):
        self.fake_module.params = {'log_level': None}
        self.fake_module.check_mode = False
        self.fake_module.get_bin_path.return_value = '/usr/bin/udevadm'
        self.fake_module.run_command.return_value = (0, 'reloaded', '')

        result = self.run_main()

        self.assertIn("'stdout': 'reloaded'", result)
        self.assertIn("'stderr': ''", result)
        self.fake_module.get_bin_path.assert_called_with('udevadm', required=True)
        self.fake_module.run_command.assert_called_with(['/usr/bin/udevadm', 'control', '--reload'], check_rc=False)

    def test_with_log_level(self):
        self.fake_module.params = {'log_level': 'debug'}
        self.fake_module.check_mode = False
        self.fake_module.get_bin_path.return_value = '/usr/bin/udevadm'
        self.fake_module.run_command.return_value = (0, 'reloaded debug', '')

        result = self.run_main()
        self.assertIn("'stdout': 'reloaded debug'", result)
        self.fake_module.run_command.assert_called_with(
            ['/usr/bin/udevadm', 'control', '--reload', '--log-level', 'debug'],
            check_rc=False
        )

        def test_check_mode(self):
            self.fake_module.params = {'log_level': 'info'}
            self.fake_module.check_mode = True
            result = self.run_main()
            self.assertIn("'changed': True", result)
            self.assertIn("'udevcontrol': {'stdout': '', 'stderr': ''}", result)
            self.fake_module.run_command.assert_not_called()

    def test_failure(self):
        self.fake_module.params = {'log_level': None}
        self.fake_module.check_mode = False
        self.fake_module.get_bin_path.return_value = '/usr/bin/udevadm'
        self.fake_module.run_command.return_value = (2, '', 'error occurred')

        result = self.run_main()
        self.assertIn('fail_json called', result)
        self.assertIn("'stderr': 'error occurred'", result)


if __name__ == '__main__':
    unittest.main()
