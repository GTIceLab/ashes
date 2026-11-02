import unittest
from types import SimpleNamespace
from ashes_fg.algorithms.cab.band_layout import section_gates, decoder_columns, decoder_bands
from ashes_fg.algorithms.decoders.bridged_radix4 import pattern


class SparseBandTests(unittest.TestCase):
    def test_gate_switches_follow_sections_instead_of_passive_routing_bands(self):
        sources = [('SEC',), ('ROUTE',), ('ROUTE',), ('ROUTE',), ('ROUTE',),
                   ('SEC',), ('ROUTE',), ('SEC',)]
        cells = {'SEC': dict(width=20, height=10), 'ROUTE': dict(width=4, height=10),
                 'SWITCH': dict(width=20, height=5)}
        entries = {0: ('section_gate', 0), 1: ('section_gate', 5), 2: ('section_gate', 7)}
        context = SimpleNamespace(entries=entries, cells=cells,
                                  island={'items': {i: {'name': 'SWITCH'} for i in entries}})
        boxes = section_gates(sources)(context)
        self.assertEqual([box[0] for box in boxes.values()], [0, 36, 60])
        self.assertEqual(len(boxes), 3)

    def test_partial_tree_does_not_materialize_unused_tail_leaf_groups(self):
        nodes = [r for r in pattern(40) if r[3] == 0]
        self.assertEqual(len(nodes), 10)
        self.assertEqual([r[4] for r in nodes], list(range(10)))

    def test_compact_decoder_uses_active_sections_without_allocating_passive_outputs(self):
        sources = [('SEC',), ('ROUTE',), ('ROUTE',), ('ROUTE',), ('ROUTE',),
                   ('SEC',), ('ROUTE',), ('SEC',)]
        cells = {'SEC': dict(width=20, height=10), 'ROUTE': dict(width=4, height=10),
                 'DECODE': dict(width=20, height=5)}
        entries = {0: ('gate_decoder', 0, 0), 1: ('gate_decoder', 1, 0)}
        context = SimpleNamespace(entries=entries, cells=cells,
                                  island={'items': {i: {'name': 'DECODE'} for i in entries}})
        boxes = decoder_columns(sources, active_columns=(0, 5, 7))(context)
        self.assertEqual(len(boxes), 2)  # Six active outputs need two 2-to-4 leaves, not eight column leaves.
        self.assertEqual([box[0] for box in boxes.values()], [0, 20])

    def test_duplicate_active_column_mapping_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'distinct host columns'):
            decoder_columns([('SEC',)], active_columns=(0, 0))

    def test_all_decoder_stages_remain_contiguous_across_host_routing_gaps(self):
        cells = {'CORE': dict(width=54.92, height=22), 'BRIDGE': dict(width=54.92, height=10)}
        entries, items = {}, {}
        for group in range(8):
            for stage in range(3):
                index = len(entries)
                entries[index] = ('gate_decoder', group, stage)
                items[index] = {'name': 'BRIDGE' if stage == 1 else 'CORE'}
        boxes = decoder_bands()(SimpleNamespace(entries=entries, cells=cells, island={'items': items}))
        for stage in range(3):
            bands = sorted((boxes[i] for i, d in entries.items() if d[2] == stage), key=lambda b: b[0])
            for first, second in zip(bands, bands[1:]):
                self.assertAlmostEqual(first[2], second[0])
        self.assertAlmostEqual(max(box[2] for box in boxes.values()), 8 * 54.92)

    def test_mismatched_native_stage_widths_fail_instead_of_leaving_silent_gaps(self):
        context = SimpleNamespace(entries={0: ('gate_decoder', 0, 0), 1: ('gate_decoder', 0, 1)},
            cells={'CORE': dict(width=55, height=22), 'BRIDGE': dict(width=50, height=10)},
            island={'items': {0: {'name': 'CORE'}, 1: {'name': 'BRIDGE'}}})
        with self.assertRaisesRegex(ValueError, 'stage widths differ'):
            decoder_bands()(context)
