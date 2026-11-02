import unittest
from ashes_fg.asic.common.pin_preflight import match_pin_labels, validate_connected_abstract_ports


class PinPreflightTests(unittest.TestCase):
    def test_reports_edge_outside_and_missing_layer_without_inventing_pins(self):
        diagnostics = []
        labels = [(1, 'ok', 5, 5), (1, 'edge', 0, 5),
                  (1, 'outside', 20, 5), (2, 'missing', 5, 5)]
        with self.assertLogs('ashes_fg.asic.common.pin_preflight', level='WARNING'):
            result = match_pin_labels(labels, [(1, 0, 0, 10, 10)],
                                      {'1,7': {'pdk_name': 'METAL1'}}, '7',
                                      'synthetic', diagnostics)
        self.assertEqual(set(result), {'ok'})
        self.assertEqual([d['reason'] for d in diagnostics], [
            'label_on_rectangle_edge', 'label_outside_selected_pin_rectangles',
            'no_selected_pin_rectangles_on_layer'])
        self.assertEqual(diagnostics[0]['cell'], 'synthetic')
        self.assertEqual(diagnostics[0]['coordinates'], [0, 5])

    def test_missing_connected_port_fails_with_context(self):
        with self.assertRaisesRegex(ValueError, r'u0 \(CELL\).*supply'):
            validate_connected_abstract_ports(
                'module TOP(); CELL u0 (.supply(VDD)); endmodule',
                {'CELL': {'cell_pins': {'other': {}}}})

    def test_bus_base_and_unconnected_ports(self):
        validate_connected_abstract_ports(
            'module TOP(); CELL u0 (.OUT({a,b}), .unused()); endmodule',
            {'CELL': {'cell_pins': {'OUT<0>': {}, 'OUT<1>': {}}}})

    def test_missing_master_is_not_silently_skipped(self):
        with self.assertRaisesRegex(ValueError, 'no physical abstract metadata'):
            validate_connected_abstract_ports('CELL u0 (.p(n));', {})

    def test_comments_are_ignored(self):
        validate_connected_abstract_ports('// CELL u0 (.bad(x));\n/* CELL u1 (.bad(y)); */', {})


if __name__ == '__main__':
    unittest.main()
