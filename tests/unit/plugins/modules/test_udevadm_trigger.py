# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import unittest
from unittest.mock import patch, MagicMock

from ansible_collections.ans2dev.general.plugins.modules import udevadm_trigger  # type: ignore


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestUdevadmTriggerModule(unittest.TestCase):
    def setUp(self):
        patcher = patch(
            'ansible_collections.ans2dev.general.plugins.modules.udevadm_trigger.AnsibleModule'
        )
        self.mock_module_class = patcher.start()
        self.addCleanup(patcher.stop)

        self.fake_module = MagicMock()
        self.fake_module.exit_json.side_effect = exit_json
        self.fake_module.fail_json.side_effect = fail_json
        self.mock_module_class.return_value = self.fake_module

    def run_main(self):
        with self.assertRaises(Exception) as context:
            udevadm_trigger.main()
        return str(context.exception)

    def test_with_quiet(self):
        self.fake_module.params = {'type': 'all', 'quiet': True}
        self.fake_module.check_mode = False
        self.fake_module.get_bin_path.return_value = '/usr/bin/udevadm'
        self.fake_module.run_command.return_value = (0, 'triggered', '')

        result = self.run_main()
        self.assertIn("'changed': True", result)
        self.assertIn("'stdout': 'triggered'", result)
        self.assertIn("'stderr': ''", result)

    def test_without_quiet(self):
        self.fake_module.params = {'type': 'devices', 'quiet': False}
        self.fake_module.check_mode = False
        self.fake_module.get_bin_path.return_value = '/usr/bin/udevadm'
        self.fake_module.run_command.return_value = (0, 'done', '')

        result = self.run_main()
        self.assertIn("'changed': True", result)
        self.assertIn("'stdout': 'done'", result)
        self.assertIn("'stderr': ''", result)

    def test_fail_nonzero(self):
        self.fake_module.params = {'type': 'subsystems', 'quiet': False}
        self.fake_module.check_mode = False
        self.fake_module.get_bin_path.return_value = '/usr/bin/udevadm'
        self.fake_module.run_command.return_value = (2, '', 'error')

        result = self.run_main()
        self.assertIn('fail_json called', result)
        self.assertIn('error', result)

    def test_check_mode(self):
        self.fake_module.params = {'type': 'all', 'quiet': False}
        self.fake_module.check_mode = True

        result = self.run_main()
        self.assertIn("'changed': False", result)


if __name__ == '__main__':
    unittest.main()
