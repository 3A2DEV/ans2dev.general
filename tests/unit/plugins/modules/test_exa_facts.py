# Copyright (c) 2025, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from unittest.mock import patch, MagicMock
import xml.etree.ElementTree as ET

# Import the exa_facts module from the collection.
from ansible_collections.a2dev.general.plugins.modules import exa_facts


def exit_json(*args, **kwargs):
    raise Exception("exit_json called: " + str(kwargs))


def fail_json(*args, **kwargs):
    raise Exception("fail_json called: " + str(kwargs))


class TestExaFactsModule(unittest.TestCase):
    def test_exa_facts(self):
        # Simulated outputs for external commands.
        fake_imageinfo_stdout = (
            "Image image type: production\n"
            "Kernel version: 4.14.35-2047.518.4.2.el7uek.x86_64\n"
            "Image created: 2023-03-02 03:40:44 -0800\n"
            "Image status: success\n"
            "Uptrack kernel version: 4.14.35-2047.522.3.el7uek.x86_64\n"
            "Node type: GUEST\n"
            "Image version: 22.1.9.0.0.230302\n"
            "System partition on device: /dev/mapper/VGExaDb-LVDbSys2\n"
            "Image label: OSS_22.1.9.0.0_LINUX.X64_230302\n"
            "Image kernel version: 4.14.35-2047.518.4.2.el7uek\n"
            "Install type: XEN Guest with InfiniBand\n"
            "Image activated: 2023-09-02 04:02:42 +0200"
        )
        fake_hw_stdout = "HVM domU"
        fake_dmidecode_stdout = (
            "System Information\n"
            "SKU Number: B88854\n"
            "UUID: 089271ba-b91f-4230-acce-be01a22fab09\n"
            "Family: Not Specified\n"
            "Serial Number: 089271ba-b91f-4230-acce-be01a22fab09\n"
            "Version: 4.4.4OVM\n"
            "Product Name: HVM domU\n"
            "Wake-up Type: Power Switch\n"
            "Manufacturer: Xen\n"
        )

        # Create a dummy XML tree to simulate the databasemachine.xml file.
        root = ET.Element("databasemachine")
        cluster = ET.SubElement(root, "ORACLE_CLUSTER")
        node = ET.SubElement(cluster, "NODE")
        node.text = "TestNode"
        dummy_tree = ET.ElementTree(root)

        # Patch AnsibleModule in exa_facts.
        with patch.object(exa_facts, 'AnsibleModule') as mock_AnsibleModule:
            fake_module = MagicMock()
            fake_module.params = {}
            fake_module.exit_json.side_effect = exit_json
            fake_module.fail_json.side_effect = fail_json
            # Simulate three run_command calls for imageinfo, exadata.img.hw, and dmidecode.
            fake_module.run_command.side_effect = [
                (0, fake_imageinfo_stdout, ""),
                (0, fake_hw_stdout, ""),
                (0, fake_dmidecode_stdout, "")
            ]
            mock_AnsibleModule.return_value = fake_module

            # Patch file-related functions.
            with patch.object(exa_facts, 'os') as mock_os, \
                 patch.object(exa_facts, 'platform') as mock_platform, \
                 patch.object(exa_facts, 'ET') as mock_ET:

                mock_os.path.isfile.return_value = True
                mock_os.access.return_value = True
                mock_platform.system.return_value = "Linux"
                # Simulate that the XML file exists.
                mock_os.path.exists.return_value = True
                # Patch ET.parse to return our dummy XML tree.
                mock_ET.parse.return_value = dummy_tree

                with self.assertRaises(Exception) as context:
                    exa_facts.main()

                result_str = str(context.exception)
                # Verify that the output contains expected facts.
                self.assertIn("exit_json called", result_str)
                self.assertIn("production", result_str)
                self.assertIn("HVM domU", result_str)
                self.assertIn("B88854", result_str)
                self.assertIn("TestNode", result_str)


if __name__ == '__main__':
    unittest.main()
