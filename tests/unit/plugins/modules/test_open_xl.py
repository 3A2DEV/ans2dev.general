# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from unittest.mock import patch, MagicMock
from openpyxl import Workbook


from ansible_collections.ans2dev.general.plugins.modules import open_xl  # type: ignore


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestOpenXLModule(unittest.TestCase):

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
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

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_write_excel(self, mock_load_workbook):

        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"

        ws.cell(row=1, column=1, value="Header")
        ws.cell(row=2, column=1, value="Old Value")

        wb.save = MagicMock()
        mock_load_workbook.return_value = wb

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

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_append_excel(self, mock_load_workbook):
        # Create a dummy workbook with one sheet ("Sheet1") and one data row.
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.cell(row=1, column=1, value="Header")
        ws.cell(row=2, column=1, value="Existing")
        wb.save = MagicMock()
        mock_load_workbook.return_value = wb

        with patch.object(open_xl, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = {
                'src': '/tmp/dummy.xlsx',
                'dest': '/tmp/dummy_updated.xlsx',
                'op': 'a',
                'sheet_name': 'Sheet1',
                'index_by_name': True,
                'read_range': {},
                'updates_matrix': [{'cell_col': 1, 'cell_value': 'Appended'}],
                'cell_style': {}
            }
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                open_xl.main()
            result_str = str(context.exception)
            self.assertIn("exit_json called", result_str)

            # The new row should be at the end.
            new_row = ws.max_row
            appended_value = ws.cell(row=new_row, column=1).value
            self.assertEqual(appended_value, 'Appended')
            wb.save.assert_called_with('/tmp/dummy_updated.xlsx')

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_insert_excel(self, mock_load_workbook):
        # Create a dummy workbook with one sheet ("Sheet1") and two rows.
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.cell(row=1, column=1, value="Header")
        ws.cell(row=2, column=1, value="Row1")
        ws.cell(row=3, column=1, value="Row2")
        wb.save = MagicMock()
        mock_load_workbook.return_value = wb

        with patch.object(open_xl, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = {
                'src': '/tmp/dummy.xlsx',
                'dest': '/tmp/dummy_updated.xlsx',
                'op': 'i',
                'sheet_name': 'Sheet1',
                'index_by_name': True,
                'read_range': {},
                'updates_matrix': [{'cell_row': 2, 'cell_col': 1, 'cell_value': 'Inserted'}],
                'cell_style': {}
            }
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                open_xl.main()
            result_str = str(context.exception)
            self.assertIn("exit_json called", result_str)
            # After insertion, the new row should be at row 2.
            inserted_value = ws.cell(row=2, column=1).value
            self.assertEqual(inserted_value, 'Inserted')
            wb.save.assert_called_with('/tmp/dummy_updated.xlsx')

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_invalid_sheet(self, mock_load_workbook):
        # Create a dummy workbook with a sheet that does not match the provided sheet name.
        wb = Workbook()
        ws = wb.active
        ws.title = "ExistingSheet"
        mock_load_workbook.return_value = wb

        with patch.object(open_xl, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = {
                'src': '/tmp/dummy.xlsx',
                'op': 'r',
                'sheet_name': 'NonExistentSheet',
                'index_by_name': True,
                'read_range': {}
            }
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                open_xl.main()
            result_str = str(context.exception)
            self.assertIn("fail_json called", result_str)
            self.assertIn("Sheet name 'NonExistentSheet' not found", result_str)

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_empty_updates_matrix_for_insert(self, mock_load_workbook):
        # Create a dummy workbook with one sheet.
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        mock_load_workbook.return_value = wb

        with patch.object(open_xl, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = {
                'src': '/tmp/dummy.xlsx',
                'dest': '/tmp/dummy_updated.xlsx',
                'op': 'i',
                'sheet_name': 'Sheet1',
                'index_by_name': True,
                'read_range': {},
                'updates_matrix': [],  # empty updates_matrix
                'cell_style': {}
            }
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                open_xl.main()
            result_str = str(context.exception)
            self.assertIn("fail_json called", result_str)
            self.assertIn("No updates_matrix provided for insert operation", result_str)

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_invalid_cell_in_write(self, mock_load_workbook):
        # Create a dummy workbook with one sheet.
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        mock_load_workbook.return_value = wb

        with patch.object(open_xl, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            # Provide invalid cell_row (0) for write operation.
            fake_module.params = {
                'src': '/tmp/dummy.xlsx',
                'dest': '/tmp/dummy_updated.xlsx',
                'op': 'w',
                'sheet_name': 'Sheet1',
                'index_by_name': True,
                'read_range': {},
                'updates_matrix': [{'cell_row': 0, 'cell_col': 1, 'cell_value': 'Invalid'}],
                'cell_style': {}
            }
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                open_xl.main()
            result_str = str(context.exception)
            self.assertIn("fail_json called", result_str)
            self.assertIn("Invalid cell_row or cell_col", result_str)

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_default_dest_naming(self, mock_load_workbook):
        # Create a dummy workbook with one sheet.
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.cell(row=1, column=1, value="Header")
        ws.cell(row=2, column=1, value="Value")
        wb.save = MagicMock()
        mock_load_workbook.return_value = wb

        with patch.object(open_xl, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            # Do not provide 'dest' to trigger default naming.
            fake_module.params = {
                'src': '/tmp/dummy.xlsx',
                'op': 'w',
                'sheet_name': 'Sheet1',
                'index_by_name': True,
                'read_range': {},
                'updates_matrix': [{'cell_row': 2, 'cell_col': 1, 'cell_value': 'Updated'}],
                'cell_style': {}
            }
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                open_xl.main()
            result_str = str(context.exception)
            self.assertIn("exit_json called", result_str)
            # Expect the default destination to be /tmp/dummy_updated.xlsx.
            wb.save.assert_called_with('/tmp/dummy_updated.xlsx')

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_workbook_load_error(self, mock_load_workbook):
        # Simulate an exception when loading the workbook.
        mock_load_workbook.side_effect = Exception("Load error")

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
            self.assertIn("fail_json called", result_str)
            self.assertIn("Error loading workbook: Load error", result_str)

    @patch("ansible_collections.ans2dev.general.plugins.modules.open_xl.openpyxl.load_workbook")
    def test_cell_style_application(self, mock_load_workbook):
        # Create a dummy workbook with one sheet.
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.cell(row=1, column=1, value="Header")
        ws.cell(row=2, column=1, value="Old")
        wb.save = MagicMock()
        mock_load_workbook.return_value = wb

        with patch.object(open_xl, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = {
                'src': '/tmp/dummy.xlsx',
                'dest': '/tmp/dummy_updated.xlsx',
                'op': 'w',
                'sheet_name': 'Sheet1',
                'index_by_name': True,
                'read_range': {},
                'updates_matrix': [{'cell_row': 2, 'cell_col': 1, 'cell_value': 'New'}],
                'cell_style': {
                    'fontColor': 'FF0000',
                    'bgColor': '00FF00',
                    'bold': True,
                    'italic': True,
                    'underline': True
                }
            }
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            mock_AnsibleModule.return_value = fake_module

            with self.assertRaises(Exception) as context:
                open_xl.main()
            result_str = str(context.exception)
            self.assertIn("exit_json called", result_str)
            wb.save.assert_called_with('/tmp/dummy_updated.xlsx')
            # Verify that the cell style was applied.
            cell = ws.cell(row=2, column=1)
            # Note: openpyxl prepends "00" to color values.
            self.assertEqual(cell.font.color.rgb, '00FF0000')
            self.assertTrue(cell.font.bold)
            self.assertTrue(cell.font.italic)
            self.assertEqual(cell.font.underline, 'single')
            # Check fill attribute.
            self.assertEqual(cell.fill.fgColor.rgb, '0000FF00')


if __name__ == '__main__':
    unittest.main()
