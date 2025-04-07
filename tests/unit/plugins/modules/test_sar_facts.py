# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from unittest.mock import patch, MagicMock
import subprocess

# Import the sar_facts module from the collection.
from ansible_collections.ans2dev.general.plugins.modules import sar_facts  # type: ignore


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestSarFactsModule(unittest.TestCase):
    def test_sar_cpu(self):
        # Simulated output for the 'sar' command.
        fake_sar_output = (
            "08:00:00 AM %user %system %idle\n"
            "08:00:00 AM 5.00 2.00 93.00\n"
            "08:10:00 AM 6.00 3.00 91.00\n"
        )

        # Parameters for a SAR facts call (CPU type).
        test_params = {
            'date_start': '2025-05-01',
            'date_end': '2025-05-01',
            'time_start': '08:00:00',
            'time_end': '10:00:00',
            'type': 'cpu',
            'average': False,
            'partition': False
        }

        # Patch AnsibleModule in sar_facts.
        with patch.object(sar_facts, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = test_params
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            fake_module.run_command.return_value = (0, fake_sar_output, "")
            mock_AnsibleModule.return_value = fake_module

            # Patch file-check and external command functions.
            with patch.object(sar_facts, 'find_sar_file', return_value="/dummy/sa01"), \
                 patch.object(sar_facts, 'subprocess') as mock_subprocess:

                # Simulate a successful subprocess.run call.
                mock_subprocess.run.return_value = subprocess.CompletedProcess(
                    args=["/usr/bin/sar", "-f", "/dummy/sa01"],
                    returncode=0,
                    stdout=fake_sar_output
                )

                with self.assertRaises(Exception) as context:
                    sar_facts.main()

                result_str = str(context.exception)
                # Verify that exit_json output contains expected SAR fact keys and values.
                self.assertIn("sar_cpu", result_str)
                self.assertIn("9.00", result_str)
                self.assertIn("2025-05-01", result_str)
                self.assertIn("exit_json called", result_str)


if __name__ == '__main__':
    unittest.main()
