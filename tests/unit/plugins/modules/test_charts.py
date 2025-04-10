# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="kaleido.scopes.base")

import unittest
from unittest.mock import patch, MagicMock


# Helper functions to simulate AnsibleModule behavior.
def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestChartsModule(unittest.TestCase):
    @patch("ansible_collections.ans2dev.general.plugins.modules.charts.os.makedirs")
    def test_line_chart(self, mock_makedirs):
        # Define parameters for a line chart operation.
        test_params = {
            'titlechart': 'Test Line Chart',
            'type': 'line',
            'xaxis': ['Jan', 'Feb', 'Mar'],
            'xaxisname': 'Month',
            'yaxis': [[10, 20, 30]],
            'yaxisname': ['Sales'],
            'yaxiscolor': ['blue'],
            'imgwidth': 800,
            'imgheight': 600,
            'shape_line': 'spline',
            'format': 'png',
            'path': '/tmp',
            'filename': 'test_chart',
            'fontsize': 20,
            'fontcolor': '#000000',
            'titlelegend': 'Legend',
            # For a line chart these are not used:
            'slicedata': [],
            'slicelabel': [],
            'slicecolor': [],
            'sizehole': 0.5
        }

        # Patch AnsibleModule on the charts module.
        from ansible_collections.ans2dev.general.plugins.modules import charts  # type: ignore
        with patch.object(charts, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = test_params
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            # Call the module's main() function.
            with self.assertRaises(Exception) as context:
                charts.main()

            result_str = str(context.exception)
            # Check that exit_json was called and that the result indicates success.
            self.assertIn("exit_json called", result_str)
            self.assertIn("'changed': True", result_str)


if __name__ == '__main__':
    unittest.main()
