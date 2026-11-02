import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

import gdstk
from ashes_fg.gds_to_celldef import cli, library


class CellPinGeometryTests(unittest.TestCase):
    def fixture(self, label=True, origin=(0, 5), datatype=7):
        lib = gdstk.Library()
        cell = lib.new_cell('Example')
        cell.add(gdstk.rectangle((0, 0), (10, 10), layer=12, datatype=datatype))
        if label:
            cell.add(gdstk.Label('SUPPLY_n', origin, layer=12, texttype=9))
        return lib

    def test_edge_diagnostic_and_strict_failure(self):
        with self.assertLogs(library.__name__, level='WARNING'):
            issues = library.validate_pin_geometry(self.fixture(), 'Example', pin_layers=[(12, 7)])
        self.assertEqual(issues[0]['reason'], 'label_on_rectangle_edge')
        self.assertEqual(issues[0]['texttype'], 9)
        with self.assertLogs(library.__name__, level='WARNING'), self.assertRaisesRegex(ValueError, 'no usable physical'):
            library.validate_pin_geometry(self.fixture(), 'Example', pin_layers=[(12, 7)], strict=True)

    def test_valid_interior_and_different_label_texttype(self):
        self.assertEqual(library.validate_pin_geometry(self.fixture(origin=(5, 5)), 'Example',
                                                     pin_layers=[(12, 7)], strict=True), [])

    def test_wrong_polygon_datatype_does_not_pass(self):
        with self.assertLogs(library.__name__, level='WARNING'):
            issues = library.validate_pin_geometry(self.fixture(origin=(5, 5), datatype=2),
                                                   'Example', pin_layers=[(12, 7)])
        self.assertEqual(issues[0]['reason'], 'no_selected_pin_rectangles_on_layer')

    def test_unselected_label_layer_is_reported(self):
        with self.assertLogs(library.__name__, level='WARNING'):
            issues = library.validate_pin_geometry(self.fixture(), 'Example', pin_layers=[(13, 7)])
        self.assertEqual(issues[0]['reason'], 'label_layer_not_selected_by_physical_parser')

    def test_pinless_strict_is_allowed(self):
        with self.assertLogs(library.__name__, level='WARNING'):
            self.assertEqual(library.validate_pin_geometry(self.fixture(label=False), 'Example', strict=True), [])

    def test_strict_requires_selection(self):
        with self.assertRaisesRegex(ValueError, 'requires --pin-layer'):
            library.validate_pin_geometry(self.fixture(), 'Example', strict=True)

    def test_cli_warn_omits_pin_and_strict_preserves_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'gds').mkdir()
            (root / 'layer_map').mkdir()
            (root / 'layer_map/test_350nm.json').write_text(json.dumps({
                '12,7': {'purpose': 'pin', 'pdk_name': 'M1'}}))
            self.fixture().write_gds(root / 'gds/Example.gds')
            previous = Path.cwd()
            try:
                os.chdir(root)
                parser = argparse.ArgumentParser()
                cli.add_parser(parser.add_subparsers(dest='command', required=True))
                command = ['cells', 'generate', '--process-node', '350', '--foundry', 'test',
                           '--process-coordinates', 'xy']
                with contextlib.redirect_stdout(io.StringIO()):
                    cli.run(parser.parse_args(command))
                spec = json.loads((root / 'cell_def/cells.json').read_text())
                self.assertNotIn('SUPPLY_n', spec['Example']['N'])
                self.assertNotIn('SUPPLY_n', (root / 'cell_def/cells.py').read_text())
                self.assertIn('label_on_rectangle_edge', (root / 'cell_def/cell_generation.log').read_text())
                before = (root / 'cell_def/cells.json').read_bytes()
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(ValueError, 'Check log'):
                    cli.run(parser.parse_args(command + ['--strict-pin-geometry']))
                self.assertEqual(before, (root / 'cell_def/cells.json').read_bytes())
            finally:
                os.chdir(previous)


if __name__ == '__main__':
    unittest.main()
