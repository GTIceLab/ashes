import unittest
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
if __package__:
    from .cab_parameters import parse
    from .cab_interfaces import Interfaces, validate_dimensions
else:
    from cab_parameters import parse


class SizingTests(unittest.TestCase):
    def setUp(self):
        self.settings = dict(mode='cab_devices', cab_device_list={
            'second': dict(std_cell='dual', count=10),
            'first': dict(std_cell='single', count=2)},
            cab_device_cfg='abut', AB_row_extras=2, Out_row=12,
            A_col=12, A_col_biases=2, A_col_pwr=2, CSC_rows=12)

    @staticmethod
    def discover(master, inputs, outputs):
        return (('i0', 'i1') if master == 'dual' else ('i0',)), ('o0',)

    def test_order_and_pin_counts(self):
        p = parse(self.settings, self.discover)
        self.assertEqual([d.key for d in p.devices], ['second', 'first'])
        self.assertEqual((p.AMatrix_Rows, p.BMatrix_Rows, p.BMatrix_Cols), (24, 24, 12))
        self.assertEqual((p.AMatrix_Cols, p.CEW_Cols, p.CNS_Cols), (16, 12, 12))
        self.assertEqual((p.OutMatrix_Rows, p.OutMatrix_Cols), (12, 12))

    def test_device_mode_ignores_matrix_only_values(self):
        p = parse(dict(self.settings, C_EW='ignored', C_NS=None,
                       C_EW_to_A=-5, C_NS_to_A=-5), self.discover)
        self.assertEqual((p.C_EW_to_A, p.C_NS_to_A), (6, 6))

    def test_spaced_uses_identical_sizing(self):
        a = parse(self.settings, self.discover)
        b = parse(dict(self.settings, cab_device_cfg='spaced'), self.discover)
        self.assertEqual(replace(a, cab_device_cfg='spaced'), b)

    def test_matrix_requires_and_consumes_all_dimensions(self):
        settings = dict(self.settings, mode='matrix', AB_row=24, B_col=12,
                        C_EW=[12, 14], C_NS=[12, 10], C_EW_to_A=8, C_NS_to_A=4)
        p = parse(settings)
        self.assertEqual((p.CEW_Cols, p.CNS_Cols, p.C_EW_to_A, p.C_NS_to_A), (14, 10, 8, 4))
        for name in ('AB_row', 'B_col', 'C_EW', 'C_NS', 'C_EW_to_A', 'C_NS_to_A'):
            missing = dict(settings)
            del missing[name]
            with self.subTest(name=name), self.assertRaises(ValueError):
                parse(missing)

    def test_invalid_modes_counts_and_configuration(self):
        for change in (dict(mode='anything'), dict(mode=None), dict(A_col=True),
                       dict(cab_device_cfg='typo'), dict(cab_device_list={}),
                       dict(cab_device_list={'d': dict(std_cell='dual', count=0)})):
            with self.subTest(change=change), self.assertRaises(ValueError):
                parse(dict(self.settings, **change), self.discover)

    def test_missing_a_column_is_actionable(self):
        del self.settings['A_col']
        with self.assertRaisesRegex(ValueError, 'A_col'):
            parse(self.settings, self.discover)

    def test_csc_leaf_alignment_is_profile_driven(self):
        p = parse(self.settings, self.discover, csc_gate_alignment=(4, 2))
        self.assertEqual((p.CEW_Cols, p.CNS_Cols), (12, 14))
        self.assertEqual((p.C_EW_to_A, p.C_NS_to_A), (6, 6))

    def test_explicit_matrix_profile_mismatch_is_rejected(self):
        settings = dict(self.settings, mode='matrix', AB_row=24, B_col=12,
                        C_EW=[12, 12], C_NS=[12, 12], C_EW_to_A=6, C_NS_to_A=6)
        with self.assertRaisesRegex(ValueError, 'CSC gate profile'):
            parse(settings, csc_gate_alignment=(4, 2))
        settings['C_NS'] = [12, 14]
        self.assertEqual(parse(settings, csc_gate_alignment=(4, 2)).CNS_Cols, 14)

    @unittest.skipUnless(__package__, 'Run as an installed package for technology checks')
    def test_physical_dimension_rejection(self):
        p = parse(self.settings, self.discover)
        validate_dimensions(p, row_unit=4, column_unit=2)
        with self.assertRaisesRegex(ValueError, 'does not fit'):
            validate_dimensions(replace(p, AMatrix_Rows=22), row_unit=4, column_unit=2)
        # A library with unit granularity can retain these exact logical rows.
        validate_dimensions(replace(p, AMatrix_Rows=22), row_unit=1, column_unit=1)

    @unittest.skipUnless(__package__, 'Run as an installed package for technology checks')
    def test_native_pin_names_vector_counts_and_static_exclusions(self):
        source = '''class Device:
    def __init__(self):
        self.a = Port(circuit, self, "in_n", "N", 2*self.dim[1], native_name="in_w")
        self.b = Port(circuit, self, "out_s", "S", 3*self.dim[1], native_name="out_e")
        self.v = Port(circuit, self, "VDD_n", "N", 1*self.dim[1], native_name="VDD_w")
'''
        with TemporaryDirectory() as folder:
            library = Path(folder) / 'cells.py'
            library.write_text(source)
            discovery = Interfaces(library)
            inputs, outputs = discovery('Device')
            self.assertEqual(inputs, ('in_w[0]', 'in_w[1]'))
            self.assertEqual(len(outputs), 3)
            with self.assertRaisesRegex(ValueError, 'Unknown CAB standard cell'):
                discovery('Missing')
            with self.assertRaisesRegex(ValueError, 'unknown native'):
                discovery('Device', ['missing_w'])


if __name__ == '__main__':
    unittest.main()
