"""Process validation must precede output generation and layout access."""
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import ashes_fg.asic as asic


class ProcessConfigurationTests(unittest.TestCase):
    def test_missing_or_invalid_process_fails_before_outputs(self):
        with tempfile.TemporaryDirectory() as folder:
            for process in ('Process', '', 'tsmc', 'TSMC350nm', 'unknown_350nm', None):
                with self.subTest(process=process):
                    with patch.object(asic, 'gds_synthesis', side_effect=AssertionError('Layout must not run')):
                        with self.assertRaisesRegex(ValueError, "Set 'process' in synthesis_settings.json"):
                            asic.compile(None, process=process, project_path=folder)
                    self.assertEqual(list(Path(folder).iterdir()), [])

    def test_supported_processes_reach_netlist_without_placement(self):
        for process in ('tsmc_350nm', 'TSMC_350nm', 'sky_130nm', 'tsmc_16nm', 'gf_180nm', 'gf_22nm'):
            with self.subTest(process=process), tempfile.TemporaryDirectory() as folder:
                circuit = SimpleNamespace(Islands=[], print=lambda _: 'module test; endmodule\n')
                with patch.object(asic, 'gds_synthesis', side_effect=AssertionError('Layout must not run')):
                    asic.compile(circuit, process=process, project_path=folder,
                                 place=False, route=False, pd_tool='ashes')
                self.assertTrue((Path(folder) / 'syn/project.v').exists())
