import unittest
from ashes_fg.algorithms.cab.cab_parameters import parse


class CapacityProfileTests(unittest.TestCase):
    def settings(self):
        return dict(mode='matrix', AB_row=16, B_col=12, Out_row=12, A_col=12,
                    A_col_biases=4, A_col_pwr=2, C_EW=[12, 12], C_NS=[12, 12],
                    C_EW_to_A=6, C_NS_to_A=6, CSC_rows=12)

    def test_shared_selection_coverage_uses_supplied_sblock_capacity(self):
        expected = parse(self.settings(), shared_gate_selection=True, sblock_gate_channels=6)
        legacy = parse(self.settings(), shared_gate_selection=True)
        self.assertEqual(expected, legacy)
        with self.assertRaisesRegex(ValueError, 'CSC gate selections must cover'):
            parse(self.settings(), shared_gate_selection=True, sblock_gate_channels=0)

    def test_sblock_capacity_rejects_invalid_metadata(self):
        for capacity in (-1, True, 1.5):
            with self.subTest(capacity=capacity):
                with self.assertRaisesRegex(ValueError, 'S-block gate channels'):
                    parse(self.settings(), sblock_gate_channels=capacity)
