"""A shared extension stays in its bank; remote hosts do not move its lanes."""
import unittest
from types import SimpleNamespace
from ashes_fg.algorithms.cab.band_layout import drain_offsets


class SharedDrainExtensionTests(unittest.TestCase):
    def test_out_lanes_extend_same_column_without_spacer_rows(self):
        context = SimpleNamespace(
            cells={'SWITCH': {'width': 40, 'height': 22}},
            island={'items': {
                0: dict(type='matrix', name='SWITCH', logical_row=0, logical_col=0,
                        mat_info={'mat_row': 4, 'mat_col': 1}),
                1: dict(type='matrix', name='SWITCH', logical_row=4, logical_col=0,
                        mat_info={'mat_row': 3, 'mat_col': 1}),
            }},
            entries={0: ('drain_switch', 'A'), 1: ('drain_switch', 'Out')})
        boxes = drain_offsets({})(context)
        self.assertEqual(boxes[0], [0, 66, 40, 154])
        self.assertEqual(boxes[1], [0, 0, 40, 66])
        self.assertEqual(boxes[1][3], boxes[0][1])
