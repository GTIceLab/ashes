"""Behavior tests for project-local, process-independent cell generation."""
import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import gdstk
from ashes_fg.gds_to_celldef import cli, library


class CellLibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.previous = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, self.previous)

    def gds(self, folder='gds_source', name='Example', labels=None, unrelated=False, boundary=False):
        directory = self.root / folder
        directory.mkdir(exist_ok=True)
        lib = gdstk.Library()
        cell = lib.new_cell(name)
        cell.add(gdstk.rectangle((0, 0), (10, 10), layer=34))
        for text, point in labels or [('IN', (.1, 5)), ('OUT', (9.9, 5)),
                                    ('VINJ', (4, 9.9)), ('VINJ', (6, 9.9)),
                                    ('D<0>', (4, .1)), ('D<1>', (6, .1))]:
            cell.add(gdstk.Label(text, point, layer=34, texttype=5))
        if unrelated:
            lib.new_cell('Unrelated').add(gdstk.rectangle((0, 0), (999, 999)))
        if boundary:
            cell.add(gdstk.rectangle((-1, -1), (11, 11), layer=123, datatype=4))
        path = directory / (name + '.gds')
        lib.write_gds(path)
        return path

    def run_command(self, action, *extra):
        parser = argparse.ArgumentParser()
        actions = parser.add_subparsers(dest='flow', required=True)
        cli.add_parser(actions)
        arguments = ['cells', action]
        if action != 'prepare':
            arguments += ['--process-node', '180', '--foundry', 'test_foundry', '--process-coordinates', 'xy']
        args = parser.parse_args(arguments + list(extra))
        with contextlib.redirect_stdout(io.StringIO()):
            cli.run(args)

    def outputs(self):
        return json.loads((self.root / 'cell_def/cells.json').read_text())

    def test_build_preserves_original_and_deduplicates_scalar_labels(self):
        source = self.gds(unrelated=True)
        original = source.read_bytes()
        self.run_command('build')
        self.assertEqual(source.read_bytes(), original)
        spec = self.outputs()['Example']
        self.assertEqual((spec['width'], spec['height']), (10, 10))
        self.assertEqual(spec['N'], ['VINJ_n'])
        self.assertEqual(spec['S'], ['D_s[0:1]'])
        self.assertEqual(spec['process_node'], '180nm')
        self.assertEqual(spec['foundry'], 'test_foundry')
        self.assertIn('IN_w', (self.root / 'cell_def/cells.py').read_text())

    def test_non_micron_gds_units_are_normalized(self):
        directory = self.root / 'gds_source'
        directory.mkdir()
        lib = gdstk.Library(unit=1e-9, precision=1e-12)
        cell = lib.new_cell('NanometerExport')
        cell.add(gdstk.rectangle((0, 0), (10000, 10000)))
        cell.add(gdstk.Label('IN', (100, 5000)))
        lib.write_gds(directory / 'NanometerExport.gds')
        self.run_command('build')
        self.assertEqual(self.outputs()['NanometerExport']['width'], 10)
        self.assertEqual(gdstk.read_gds(self.root / 'gds/NanometerExport.gds').unit, 1e-6)

    def test_missing_directories_do_not_create_outputs(self):
        for action in ('prepare', 'generate', 'build'):
            with self.assertRaisesRegex(ValueError, 'Missing'):
                self.run_command(action)
            self.assertFalse((self.root / 'cell_def').exists())
            self.assertFalse((self.root / 'gds').exists())

    def test_legacy_source_alias_and_existing_suffixes(self):
        self.gds('gds_cadence', labels=[('IN_w', (.1, 5)), ('OUT_e', (9.9, 5))])
        self.run_command('prepare')
        self.run_command('generate')
        self.assertIn('IN_w', self.outputs()['Example']['W'])
        self.assertNotIn('IN_w_w', (self.root / 'cell_def/cells.py').read_text())

    def test_two_source_directories_require_explicit_choice(self):
        self.gds('gds_source')
        self.gds('gds_cadence')
        with self.assertRaisesRegex(ValueError, 'Both'):
            self.run_command('prepare')
        self.run_command('build', '--source-dir', 'gds_source')

    def test_explicit_boundary_layer(self):
        self.gds(boundary=True)
        self.run_command('build', '--boundary-layer', '123:4')
        self.assertEqual(self.outputs()['Example']['width'], 12)

    def test_invalid_batch_does_not_modify_any_existing_outputs(self):
        self.gds()
        self.run_command('build')
        snapshot = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file() and 'gds_source' not in p.parts}
        self.gds(name='Broken', labels=[('internal.node', (5, 9.9))])
        with self.assertRaisesRegex(ValueError, 'not a supported Verilog'):
            self.run_command('build')
        self.assertEqual({p: p.read_bytes() for p in snapshot}, snapshot)
        self.assertFalse((self.root / 'gds/Broken.gds').exists())

    def test_logical_mapping_keeps_native_export_name(self):
        self.gds(labels=[('VG_w', (.1, 5)), ('OUT_e', (9.9, 5))])
        self.run_command('build', '--process-coordinates', 'columns_y_rows_minus_x')
        spec = importlib.util.spec_from_file_location('generated_test_cells', self.root / 'cell_def/cells.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        import ashes_fg.asic.asic_compile as ac
        circuit = ac.Circuit()
        cell = module.Example(circuit, ac.Island(circuit))
        self.assertEqual(cell.VG_n.native_name, 'VG_w')
        self.assertEqual(cell.VG_n.location, 'N')
        wire = ac.Wire(circuit)
        wire += cell.VG_n[0]
        circuit.nameNetsFlat()
        self.assertIn('.VG_w(', cell.VG_n.print_conventional(0, 0))
        self.assertNotIn('.VG_n(', cell.VG_n.print_conventional(0, 0))

    def test_ambiguous_corner_requires_direction_map(self):
        self.gds(labels=[('IN', (0, 0))])
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            self.run_command('prepare')
        path = self.root / 'directions.json'
        path.write_text(json.dumps({'Example': {'IN': 'W'}}))
        self.run_command('build', '--direction-map', str(path))
        self.assertEqual(self.outputs()['Example']['W'], ['IN_w'])

    def test_explicit_pin_map_and_invalid_target(self):
        self.gds(labels=[('VG_w', (.1, 5))])
        path = self.root / 'pins.json'
        path.write_text(json.dumps({'Example': {'gate_n': 'missing'}}))
        with self.assertRaisesRegex(ValueError, 'missing native'):
            self.run_command('build', '--pin-map', str(path))
        path.write_text(json.dumps({'Example': {'gate_n': 'VG_w'}}))
        self.run_command('build', '--pin-map', str(path))
        self.assertEqual(self.outputs()['Example']['logical_to_native']['gate_n'], 'VG_w')

    def test_sparse_bus_is_rejected_without_inventing_pins(self):
        self.gds(labels=[('D_w[1]', (.1, 5))])
        with self.assertRaisesRegex(ValueError, 'zero-based'):
            self.run_command('build')

    def test_replacements_preserve_other_classes_and_record_history(self):
        self.gds()
        self.gds(name='Other')
        self.run_command('build')
        self.gds(labels=[('IN', (.1, 5)), ('OUT', (9.9, 5))])
        self.run_command('build', '--cells', 'Example')
        self.assertEqual(set(self.outputs()), {'Example', 'Other'})
        self.assertEqual(len(list((self.root / 'cell_def/cell_histories').glob('Example.*.py.txt'))), 1)

    def test_source_output_overlap_is_rejected(self):
        self.gds()
        with self.assertRaisesRegex(ValueError, 'must differ'):
            self.run_command('prepare', '--gds-dir', 'gds_source')

    def test_label_layer_filter_is_explicit(self):
        path = self.gds()
        lib = gdstk.read_gds(path)
        lib.cells[0].add(gdstk.Label('internal.node', (5, 5), layer=77))
        lib.write_gds(path)
        self.run_command('build', '--label-layer', '34:5')

    def test_atomic_replacement_failure_restores_originals(self):
        from unittest.mock import patch
        a, b = self.root / 'cells.py', self.root / 'cells.json'
        a.write_bytes(b'original python')
        b.write_bytes(b'original json')
        replace = library.os.replace
        calls = []
        def fail_second(source, target):
            calls.append(target)
            if len(calls) == 2:
                raise OSError('simulated replacement failure')
            return replace(source, target)
        with patch.object(library.os, 'replace', side_effect=fail_second):
            with self.assertRaisesRegex(OSError, 'simulated'):
                library.write_outputs({a: b'new python', b: b'new json'})
        self.assertEqual(a.read_bytes(), b'original python')
        self.assertEqual(b.read_bytes(), b'original json')

    def test_legacy_import_header_is_migrated(self):
        self.gds()
        self.run_command('build')
        path = self.root / 'cell_def/cells.py'
        path.write_text(path.read_text().replace('ashes_fg.asic.asic_compile', 'ashes_fg.asic.model.asic_compile'))
        self.run_command('generate')
        self.assertIn('from ashes_fg.asic.asic_compile import', path.read_text())
        self.assertNotIn('from ashes_fg.asic.model.', path.read_text())

    def test_legacy_single_file_entry_point_defaults_to_project_output(self):
        path = self.gds('gds', labels=[('VG_w', (.1, 5))])
        result = subprocess.run([sys.executable, '-m', 'ashes_fg.gds_to_celldef.gen_stdcell_defs', str(path),
            '-pn', '130', '-foundry', 'sky'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'cell_def/cells.py').is_file())

    def test_cli_error_is_readable_and_help_is_available(self):
        command = [sys.executable, '-m', 'ashes_fg.cli', 'cells']
        result = subprocess.run(command + ['--help'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('prepare', result.stdout)
        result = subprocess.run(command + ['generate', '--process-node', '130', '--foundry', 'sky', '--process-coordinates', 'xy'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Tools/lib', result.stderr)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
