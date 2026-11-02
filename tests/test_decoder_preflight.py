import unittest
from types import SimpleNamespace

from ashes_fg.algorithms.decoders.bridged_radix4 import unresolved_pins, validate_auxiliary_contract
from ashes_fg.algorithms.cab.relative_layout import create


class DecoderPreflightTests(unittest.TestCase):
    def test_optional_internal_annotations_may_be_absent_but_required_ports_may_not(self):
        with self.assertLogs('ashes_fg.algorithms.decoders.bridged_radix4', level='WARNING'):
            names = validate_auxiliary_contract(
                dict(optional_internal_ports=('present', 'missing')), {'present'})
        self.assertEqual(names, {'present'})
        for contract in (dict(internal_ports=('missing',)),
                         dict(leaf_ports={'missing': 'analog_input'})):
            with self.assertRaisesRegex(ValueError, 'references missing ports'):
                validate_auxiliary_contract(contract, set())

    def test_rechecks_auxiliary_candidates_after_caller_wiring(self):
        pin = SimpleNamespace()
        pin.net = SimpleNamespace(pins=[pin])
        port = SimpleNamespace(pins=[pin])
        cell = SimpleNamespace(name='Decoder')
        result = SimpleNamespace(unassigned=[(cell, port)])
        self.assertEqual(unresolved_pins(result)[0][2], (0,))
        pin.net.pins.append(object())
        self.assertEqual(unresolved_pins(result), [])

    def test_reports_only_unconnected_lanes_of_partially_connected_port(self):
        a, b = SimpleNamespace(), SimpleNamespace()
        a.net, b.net = SimpleNamespace(pins=[a, object()]), SimpleNamespace(pins=[b])
        result = SimpleNamespace(unassigned=[(object(), SimpleNamespace(pins=[a, b]))])
        self.assertEqual(unresolved_pins(result)[0][2], (1,))

    def test_only_explicitly_classified_internal_pins_are_excluded(self):
        a, b = SimpleNamespace(), SimpleNamespace()
        a.net, b.net = SimpleNamespace(pins=[a]), SimpleNamespace(pins=[b])
        result = SimpleNamespace(unassigned=[(object(), SimpleNamespace(pins=[a, b]))],
                                 internal_pin_ids={id(a)})
        self.assertEqual(unresolved_pins(result)[0][2], (1,))
        self.assertEqual(len(a.net.pins), 1)


class RelativeLayoutTests(unittest.TestCase):
    def test_abutment_and_margin_use_measured_boxes(self):
        layout = create(['A', 'B'], {'A': {}, 'B': dict(reference='A', side='right', gap=0)}, margin=10)
        blocks = [dict(coords=[[0, 0, 100, 50]]), dict(coords=[[0, 0, 80, 40]])]
        self.assertEqual(layout(blocks, {}, (0, 0, 1000, 1000)), [(10, 10), (110, 10)])

    def test_backend_mapping_uses_numeric_ids_not_insertion_order(self):
        layout = create(['A', 'B'], {'A': {}, 'B': dict(reference='A', side='right', gap=0)}, margin=10)
        blocks = {1: dict(coords=[[0, 0, 80, 40]]), 0: dict(coords=[[0, 0, 100, 50]])}
        self.assertEqual(layout(blocks, {}, (0, 0, 1000, 1000, 50, 100)), [(10, 10), (110, 10)])

    def test_block_count_and_numbering_mismatches_report_clear_errors(self):
        layout = create(['A'], {'A': {}})
        with self.assertRaisesRegex(ValueError, 'expected 1 blocks, got 0'):
            layout([], {}, (0, 0, 1000, 1000))
        with self.assertRaisesRegex(ValueError, 'contiguous numeric island IDs'):
            layout({2: dict(coords=[[0, 0, 10, 10]])}, {}, (0, 0, 1000, 1000))

    def test_cycle_and_overlap_are_actual_errors(self):
        blocks = [dict(coords=[[0, 0, 100, 50]]), dict(coords=[[0, 0, 80, 40]])]
        layout = create(['A', 'B'], {'A': dict(reference='B', side='right'),
                                     'B': dict(reference='A', side='right')})
        with self.assertRaisesRegex(ValueError, 'dependency cycle'):
            layout(blocks, {}, (0, 0, 1000, 1000))
        overlap = create(['A', 'B'], {'A': {}, 'B': {}}, margin=0)
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            overlap(blocks, {}, (0, 0, 1000, 1000))

    def test_missing_island_rule_fails_during_construction(self):
        with self.assertRaisesRegex(ValueError, 'cover every'):
            create(['A', 'B'], {'A': {}})

    def test_sparse_bank_anchors_to_switch_without_rejecting_empty_space(self):
        layout = create(['A', 'Drain'], {'A': {}, 'Drain': dict(reference='A', side='left', gap=0,
            align_y='top', align_x='right', reference_x='left', own_anchor=dict(master='SWITCH'))}, margin=10)
        blocks = {0: dict(coords=[[0, 0, 100, 50]], items={0: dict(name='MATRIX')}),
                  1: dict(coords=[[0, 100, 20, 150], [100, 0, 120, 50]],
                          items={0: dict(name='SWITCH'), 1: dict(name='SWITCH')})}
        self.assertEqual(layout(blocks, {}, (0, 0, 1000, 1000)), [(30, 110), (10, 10)])
        blocks[1]['coords'][1] = [100, 100, 120, 150]
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            layout(blocks, {}, (0, 0, 1000, 1000))

    def test_host_anchor_survives_backend_array_reordering(self):
        layout = create(['A', 'Drain'], {'A': {}, 'Drain': dict(reference='A', side='left', gap=0,
            align_y='top', align_x='right', reference_x='left',
            own_anchor=dict(master='SWITCH', logical_row=0, logical_col=5))}, margin=10)
        first = dict(name='SWITCH', logical_row=0, logical_col=5)
        other = dict(name='SWITCH', logical_row=6, logical_col=5)
        block = dict(coords=[[0, 100, 20, 150], [100, 0, 120, 50]], items={0: first, 1: other})
        a = dict(coords=[[0, 0, 100, 50]], items={0: dict(name='MATRIX')})
        expected = layout({0: a, 1: block}, {}, (0, 0, 1000, 1000))
        reordered = dict(coords=list(reversed(block['coords'])), items={0: other, 1: first})
        self.assertEqual(layout({0: a, 1: reordered}, {}, (0, 0, 1000, 1000)), expected)

    def test_volatile_style_bank_can_abut_below_and_center_on_host(self):
        layout = create(['A', 'Volatile'], {'A': {}, 'Volatile': dict(reference='A', side='below',
            gap=0, align_x='center')}, margin=0)
        blocks = [dict(coords=[[0, 0, 100, 50]]), dict(coords=[[0, 0, 60, 20]])]
        self.assertEqual(layout(blocks, {}, (0, 0, 1000, 1000)), [(0, 20), (20, 0)])
