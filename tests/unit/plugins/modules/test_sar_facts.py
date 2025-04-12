# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from unittest.mock import patch, MagicMock

from ansible_collections.ans2dev.general.plugins.modules import sar_facts  # type: ignore


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestSarFactsModule(unittest.TestCase):
    def run_sar_fact_test(self, test_params, fake_sar_output, expected_fact_key, expected_sample_value):
        with patch.object(sar_facts, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = test_params
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            fake_module.run_command.return_value = (0, fake_sar_output, "")
            fake_module.get_bin_path.return_value = "/usr/bin/sar"
            mock_AnsibleModule.return_value = fake_module

            with patch.object(sar_facts, 'find_sar_file', return_value="/dummy/sa01"):
                with self.assertRaises(Exception) as context:
                    sar_facts.main()
                result_str = str(context.exception)

                self.assertIn(expected_fact_key, result_str)
                self.assertIn(expected_sample_value, result_str)
                self.assertIn("2025-05-01", result_str)

    def test_sar_cpu(self):
        fake_sar_output = (
            "08:00:00 AM %user %system %idle\n"
            "08:00:00 AM 5.00 2.00 93.00\n"
            "08:10:00 AM 6.00 3.00 91.00\n"
        )
        test_params = {
            'date_start': '2025-05-01',
            'date_end': '2025-05-01',
            'time_start': '08:00:00',
            'time_end': '10:00:00',
            'type': 'cpu',
            'average': False,
            'partition': False
        }
        self.run_sar_fact_test(test_params, fake_sar_output, "sar_cpu", "5.00")

    def test_sar_memory(self):
        fake_sar_output = (
            "08:00:00 AM %memused %commit\n"
            "08:00:00 AM 75.00 60.00\n"
            "08:10:00 AM 76.00 59.50\n"
        )
        test_params = {
            'date_start': '2025-05-01',
            'date_end': '2025-05-01',
            'time_start': '08:00:00',
            'time_end': '10:00:00',
            'type': 'memory',
            'average': False,
            'partition': False
        }
        self.run_sar_fact_test(test_params, fake_sar_output, "sar_mem", "75.00")

    def test_sar_swap(self):
        fake_sar_output = (
            "08:00:00 AM %swpused %swpcad\n"
            "08:00:00 AM 10.00 0.50\n"
            "08:10:00 AM 11.00 0.60\n"
        )
        test_params = {
            'date_start': '2025-05-01',
            'date_end': '2025-05-01',
            'time_start': '08:00:00',
            'time_end': '10:00:00',
            'type': 'swap',
            'average': False,
            'partition': False
        }
        self.run_sar_fact_test(test_params, fake_sar_output, "sar_swap", "10.00")

    def test_sar_network(self):
        fake_sar_output = (
            "08:00:00 AM IFACE rxpck/s txpck/s %ifutil\n"
            "08:00:00 AM eth0 100.00 200.00 0.50\n"
            "08:10:00 AM eth0 110.00 210.00 0.55\n"
        )
        test_params = {
            'date_start': '2025-05-01',
            'date_end': '2025-05-01',
            'time_start': '08:00:00',
            'time_end': '10:00:00',
            'type': 'network',
            'average': False,
            'partition': False
        }
        self.run_sar_fact_test(test_params, fake_sar_output, "sar_net", "100.00")

    def test_sar_disk(self):
        fake_sar_output = (
            "08:00:00 AM DEV %util await rkB/s wkB/s\n"
            "08:00:00 AM sda 90.00 5.00 100.00 200.00\n"
            "08:10:00 AM sda 91.00 5.10 101.00 201.00\n"
        )
        test_params = {
            'date_start': '2025-05-01',
            'date_end': '2025-05-01',
            'time_start': '08:00:00',
            'time_end': '10:00:00',
            'type': 'disk',
            'average': False,
            'partition': False
        }
        self.run_sar_fact_test(test_params, fake_sar_output, "sar_disk", "90.00")

    def test_sar_load(self):
        fake_sar_output = (
            "08:00:00 AM ldavg-1 ldavg-5 ldavg-15\n"
            "08:00:00 AM 0.50 0.60 0.70\n"
            "08:10:00 AM 0.55 0.65 0.75\n"
        )
        test_params = {
            'date_start': '2025-05-01',
            'date_end': '2025-05-01',
            'time_start': '08:00:00',
            'time_end': '10:00:00',
            'type': 'load',
            'average': False,
            'partition': False
        }
        self.run_sar_fact_test(test_params, fake_sar_output, "sar_load", "0.50")


if __name__ == '__main__':
    unittest.main()
