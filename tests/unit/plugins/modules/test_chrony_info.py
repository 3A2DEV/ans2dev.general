# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import unittest
from unittest.mock import patch, MagicMock

from ansible_collections.ans2dev.general.plugins.modules import chrony_info  # type: ignore


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestChronyInfoModule(unittest.TestCase):

    def run_module_test(self, params, run_command_return, expected_key, expected_value_substr):
        with patch.object(chrony_info, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = params
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            fake_module.run_command.return_value = run_command_return

            fake_module.get_bin_path.side_effect = lambda cmd, required: "/usr/bin/" + cmd
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                chrony_info.main()
            result_str = str(context.exception)
            self.assertIn(expected_key, result_str)
            self.assertIn(expected_value_substr, result_str)

    def test_conf(self):
        fake_conf_output = (
            "driftfile /var/lib/chrony/drift\n"
            "keyfile /etc/chrony.keys\n"
            "leapsectz right/UTC\n"
            "logdir /var/log/chrony\n"
            "makestep 1.0 3\n"
            "ntsdumpdir /var/lib/chrony\n"
            "rtcsync\n"
            "server 100.110.92.1 iburst\n"
            "server 91.149.253.184 iburst\n"
            "sourcedir /run/chrony-dhcp\n"
        )
        params = {'mode': 'conf'}
        self.run_module_test(params, (0, fake_conf_output, ""), "driftfile", "/var/lib/chrony/drift")

    def test_sources(self):
        fake_sources_output = (
            "MS Name/IP address         Stratum Poll Reach LastRx Last sample\n"
            "^? 100.110.92.1              0       8    0     -      +0ns[ +0ns] +/- 0ns\n"
            "^? 91.149.253.184            0       8    0     -      +0ns[ +0ns] +/- 0ns\n"
        )
        params = {'mode': 'sources'}
        self.run_module_test(params, (0, fake_sources_output, ""), "MS", "100.110.92.1")

    def test_sourcestats(self):
        fake_sourcestat_output = (
            "Name/IP Address NP NR Span Frequency Freq Skew Offset Std Dev\n"
            "100.110.92.1 0 0 0 +0.000 2000.000 +0ns 4000ms\n"
            "91.149.253.184 0 0 0 +0.000 2000.000 +0ns 4000ms\n"
        )
        params = {'mode': 'sourcestats'}
        self.run_module_test(params, (0, fake_sourcestat_output, ""), "Name/IP Address", "4000ms")

    def test_ntpdata_all(self):
        fake_conf_output = (
            "server 100.110.92.1 iburst\n"
            "server 91.149.253.184 iburst\n"
        )
        fake_ntpdata_output = (
            "Authenticated: No\n"
            "Interleaved: No\n"
            "Jitter asymmetry: +0.00\n"
            "Leap status: Normal\n"
            "Local address: [UNSPEC] (00000000)\n"
            "Mode: Invalid\n"
            "NTP tests: 000 000 0000\n"
            "Offset: +0.000000000 seconds\n"
            "Peer delay: 0.000000000 seconds\n"
            "Peer dispersion: 0.000000000 seconds\n"
            "Poll interval: 0 (1 seconds)\n"
            "Precision: 0 (1.000000000 seconds)\n"
            "RX timestamping: Invalid\n"
            "Reference ID: 00000000 ()\n"
            "Reference time: Thu Jan 01 00:00:00 1970\n"
            "Remote address: 100.110.92.1 (646E5C01)\n"
            "Remote port: 123\n"
            "Response time: 0.000000000 seconds\n"
            "Root delay: 0.000000 seconds\n"
            "Root dispersion: 0.000000 seconds\n"
            "Stratum: 0\n"
            "TX timestamping: Invalid\n"
            "Total HW RX: 0\n"
            "Total HW TX: 0\n"
            "Total RX: 0\n"
            "Total TX: 9\n"
            "Total good RX: 0\n"
            "Total kernel RX: 0\n"
            "Total kernel TX: 9\n"
            "Total valid RX: 0\n"
            "Version: 0\n"
        )

        def fake_run_command(cmd):
            if cmd[0] == "/usr/bin/chronyd":

                return (0, fake_conf_output, "")
            elif cmd[0] == "/usr/bin/chronyc" and cmd[1] == "ntpdata":

                return (0, fake_ntpdata_output, "")
            else:
                return (0, "", "")
        with patch.object(chrony_info, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = {'mode': 'ntpdata'}
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            fake_module.run_command.side_effect = fake_run_command
            fake_module.get_bin_path.side_effect = lambda cmd, required: "/usr/bin/" + cmd
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                chrony_info.main()
            result_str = str(context.exception)
            self.assertIn("100.110.92.1", result_str)
            self.assertIn("Offset", result_str)

    def test_ntpdata_specific(self):
        fake_ntpdata_output = (
            "Authenticated: No\n"
            "Interleaved: No\n"
            "Jitter asymmetry: +0.00\n"
            "Leap status: Normal\n"
            "Local address: [UNSPEC] (00000000)\n"
            "Mode: Invalid\n"
            "NTP tests: 000 000 0000\n"
            "Offset: +0.000000000 seconds\n"
            "Peer delay: 0.000000000 seconds\n"
            "Peer dispersion: 0.000000000 seconds\n"
            "Poll interval: 0 (1 seconds)\n"
            "Precision: 0 (1.000000000 seconds)\n"
            "RX timestamping: Invalid\n"
            "Reference ID: 00000000 ()\n"
            "Reference time: Thu Jan 01 00:00:00 1970\n"
            "Remote address: 100.110.92.1 (646E5C01)\n"
            "Remote port: 123\n"
            "Response time: 0.000000000 seconds\n"
            "Root delay: 0.000000 seconds\n"
            "Root dispersion: 0.000000 seconds\n"
            "Stratum: 0\n"
            "TX timestamping: Invalid\n"
            "Total HW RX: 0\n"
            "Total HW TX: 0\n"
            "Total RX: 0\n"
            "Total TX: 9\n"
            "Total good RX: 0\n"
            "Total kernel RX: 0\n"
            "Total kernel TX: 9\n"
            "Total valid RX: 0\n"
            "Version: 0\n"
        )
        params = {'mode': 'ntpdata', 'IP': "100.110.92.1"}
        with patch.object(chrony_info, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = params
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            fake_module.run_command.return_value = (0, fake_ntpdata_output, "")
            fake_module.get_bin_path.side_effect = lambda cmd, required: "/usr/bin/" + cmd
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                chrony_info.main()
            result_str = str(context.exception)
            self.assertIn("100.110.92.1", result_str)
            self.assertIn("Authenticated", result_str)


if __name__ == '__main__':
    unittest.main()
