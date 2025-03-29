# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import patch, MagicMock
from openpyxl import Workbook

# Import the open_xl module from the collection.
from ansible_collections.a2dev.general.plugins.modules import open_xl


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestOpenXLModule(unittest.TestCase):

    @patch("ansible_collections.a2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_read_excel(self, mock_load_workbook):
        # Create a dummy workbook with one sheet ("Sheet1").
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        # Header row.
        ws.cell(row=1, column=1, value="Name")
        ws.cell(row=1, column=2, value="Age")
        # Data rows.
        ws.cell(row=2, column=1, value="Alice")
        ws.cell(row=2, column=2, value=30)
        ws.cell(row=3, column=1, value="Bob")
        ws.cell(row=3, column=2, value=25)
        mock_load_workbook.return_value = wb

        # Patch AnsibleModule in open_xl.
        with patch.object(open_xl, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = {
                'src': '/tmp/dummy.xlsx',
                'op': 'r',
                'sheet_name': 'Sheet1',
                'index_by_name': True,
                'read_range': {}
            }
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                open_xl.main()
            result_str = str(context.exception)

            # Check that the result contains the expected sheet data.
            self.assertIn("exit_json called", result_str)
            self.assertIn("'Sheet1': [{'Name': 'Alice'", result_str)
            self.assertIn("'Age': 30", result_str)
            self.assertIn("'Name': 'Bob'", result_str)

    @patch("ansible_collections.a2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_write_excel(self, mock_load_workbook):
        # Create a dummy workbook with one sheet ("Sheet1").
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        # Prepopulate a header and a row.
        ws.cell(row=1, column=1, value="Header")
        ws.cell(row=2, column=1, value="Old Value")
        # Patch the workbook's save method.
        wb.save = MagicMock()
        mock_load_workbook.return_value = wb

        # Patch AnsibleModule in open_xl.
        with patch.object(open_xl, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = {
                'src': '/tmp/dummy.xlsx',
                'dest': '/tmp/dummy_updated.xlsx',
                'op': 'w',
                'sheet_name': 'Sheet1',
                'index_by_name': True,
                'read_range': {},
                'updates_matrix': [
                    {'cell_row': 2, 'cell_col': 1, 'cell_value': 'New Value'}
                ],
                'cell_style': {}
            }
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                open_xl.main()
            result_str = str(context.exception)

            # Check that exit_json was called and that the workbook was saved correctly.
            self.assertIn("exit_json called", result_str)
            self.assertIn("result': {}", result_str)
            wb.save.assert_called_with('/tmp/dummy_updated.xlsx')


if __name__ == '__main__':
    unittest.main()