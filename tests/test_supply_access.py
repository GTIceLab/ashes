from pathlib import Path
import tempfile
import unittest

from ashes_fg.asic.pd.supply_access import filter_supplies, placed_components, apply_supply_access
from ashes_fg.asic.pd import pd_tcl_gen


def policy():
    return dict(mode='exposed_abutment', same_net_terminals_connected_within_cell=True,
                nets=['GND', 'GND_b'], port_families=['GND', 'GND_b'], tolerance_dbu=0)


def macro(width=10, height=10, pins=None, metal='M1'):
    return dict(width=width, height=height, origin=(0, 0), top_metal=metal,
                cell_pins={name: dict(Layer=layer, RECT=rect)
                           for name, (layer, rect) in (pins or {}).items()})


class SupplyAccessTests(unittest.TestCase):
    def setUp(self):
        self.cells = {'C': macro(pins={'GND_w': ('M1', (0, 4, 1, 6)),
                                      'GND_e': ('M1', (9, 4, 10, 6))})}
        self.placed = dict(A=dict(master='C', x=0, y=0, orientation='N'),
                           B=dict(master='C', x=10, y=0, orientation='N'))
        self.netlist = ('module TOP(GND);\ninout GND;\n'
                        'C A (.GND_w(GND), .GND_e(GND), .IN_n(signal));\n'
                        'C B (.GND_w(GND), .GND_e(GND));\nendmodule\n')

    def test_shared_boundary_removes_buried_supply_taps_only(self):
        text, report = filter_supplies(self.netlist, self.placed, self.cells, policy(), ['M1'])
        self.assertEqual(report['removed_terminals'], 2)
        self.assertIn('C A (.GND_w(GND), .IN_n(signal));', text)
        self.assertIn('C B (.GND_e(GND));', text)
        self.assertEqual(report['removed_by_net'], {'GND': 2})

    def test_open_gap_and_lower_metal_neighbor_do_not_hide_access(self):
        self.placed['B']['x'] = 11
        text, report = filter_supplies(self.netlist, self.placed, self.cells, policy(), ['M1'])
        self.assertEqual(text, self.netlist)
        self.assertEqual(report['removed_terminals'], 0)
        self.placed['B']['x'] = 10
        self.cells['C']['cell_pins']['GND_e']['Layer'] = 'M2'
        _, report = filter_supplies(self.netlist, self.placed, self.cells, policy(), ['M1', 'M2'])
        right_a = next(r for r in report['terminals'] if r['instance']=='A' and r['pin']=='GND_e')
        self.assertFalse(right_a['removed'])

    def test_enclosed_group_without_proven_access_is_preserved(self):
        cells = {'A': macro(pins={'GND_e': ('M1', (9, 4, 10, 6))}), 'Block': macro()}
        placed = dict(A=dict(master='A', x=0, y=0, orientation='N'),
                      B=dict(master='Block', x=10, y=0, orientation='N'))
        source = 'module TOP();\nA A (.GND_e(GND));\nBlock B ();\nendmodule\n'
        text, report = filter_supplies(source, placed, cells, policy(), ['M1'])
        self.assertEqual(source, text)
        self.assertEqual(report['terminals'][0]['reason'], 'buried_but_no_proven_exposed_path_preserved')

    def test_partial_bus_preserves_bit_positions_with_isolated_unused_lane(self):
        cells = {'C': macro(pins={'GND_n[0]': ('M1', (7, 9, 8, 10)),
                                 'GND_n[1]': ('M1', (1, 9, 2, 10))}),
                 'B': macro(width=5, pins={'GND_s': ('M1', (1, 0, 2, 1)),
                                          'GND_n': ('M1', (1, 9, 2, 10))})}
        placed = dict(A=dict(master='C', x=0, y=0, orientation='N'),
                      B=dict(master='B', x=0, y=10, orientation='N'))
        source = 'module TOP();\nC A (.GND_n({GND, GND}));\nB B (.GND_s(GND), .GND_n(GND));\nendmodule\n'
        text, report = filter_supplies(source, placed, cells, policy(), ['M1'])
        self.assertIn('.GND_n({__ashes_supply_open_0, GND})', text)
        self.assertIn('wire __ashes_supply_open_0;', text)
        self.assertEqual(report['isolated_bus_lanes'], 1)
        self.assertEqual(report['removed_terminals'], 2)

    def test_unsupported_orientation_is_preserved(self):
        self.placed['A']['orientation'] = 'FN'
        text, report = filter_supplies(self.netlist, self.placed, self.cells, policy(), ['M1'])
        self.assertIn('C A (.GND_w(GND), .GND_e(GND), .IN_n(signal));', text)
        self.assertTrue(report['preserved_issues'])

    def test_policy_requires_explicit_continuity_declaration(self):
        p = policy(); p.pop('same_net_terminals_connected_within_cell')
        with self.assertRaisesRegex(ValueError, 'continuity declaration'):
            filter_supplies(self.netlist, self.placed, self.cells, p, ['M1'])

    def test_supply_names_are_not_aliases_and_signal_pins_are_not_filtered(self):
        source = self.netlist.replace('C B (.GND_w(GND), .GND_e(GND))',
                                      'C B (.GND_w(GND_b), .GND_e(GND_b))')
        text, report = filter_supplies(source, self.placed, self.cells, policy(), ['M1'])
        self.assertIn('.IN_n(signal)', text)
        self.assertIn('C B (.GND_e(GND_b));', text)
        self.assertNotIn('.GND_w(GND), .GND_e(GND)', text)
        self.assertEqual(set(r['net'] for r in report['terminals']), {'GND', 'GND_b'})

    def test_buried_cell_requires_actual_same_layer_abutment_path(self):
        cells = {'A': macro(pins={'GND_e': ('M1', (9, 4, 10, 6))}),
                 'B': macro(pins={'GND_w': ('M1', (0, 4, 1, 6)),
                                  'GND_e': ('M1', (9, 4, 10, 6))})}
        placed = dict(A=dict(master='A', x=0, y=0, orientation='N'),
                      B=dict(master='B', x=10, y=0, orientation='N'))
        source='module TOP();\nA A (.GND_e(GND));\nB B (.GND_w(GND), .GND_e(GND));\nendmodule\n'
        text, report=filter_supplies(source, placed, cells, policy(), ['M1'])
        self.assertIn('A A ();', text)
        self.assertEqual(report['removed_terminals'], 2)
        cells['B']['cell_pins']['GND_w']['RECT']=(0, 7, 1, 9)
        text, report=filter_supplies(source, placed, cells, policy(), ['M1'])
        self.assertIn('A A (.GND_e(GND));', text)

    def test_file_export_keeps_full_netlist_and_design_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); net=root/'design.v'; defs=root/'design.def'; report=root/'supply_access.json'
            net.write_text(self.netlist)
            defs.write_text('COMPONENTS 2 ;\n- A C + PLACED ( 0 0 ) N ;\n- B C + PLACED ( 10 0 ) N ;\nEND COMPONENTS\n')
            apply_supply_access(net, defs, self.cells, policy(), ['M1'], 1000, report)
            self.assertEqual(net.with_suffix('.full.v').read_text(), self.netlist)
            self.assertTrue(report.is_file())
            self.assertTrue(report.with_suffix('.log').is_file())
            self.assertNotEqual(net.read_text(), self.netlist)


class PDPolicyTests(unittest.TestCase):
    def test_configurable_floorplan_power_and_antenna_behavior(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)
            config=dict(pins=[dict(core_margins=dict(left=10, right=10, bottom=10, top=10))],
                        route=[dict(top_layer='M4', bot_layer='M1', default_ndr='ANALOG',
                                    antenna_diode_insertion=None, iterations=10)], power_enabled=False)
            pd_tcl_gen.generate_pins_tcl(config, (0,0,920000,610000,0,0), {}, p/'pins.tcl')
            pd_tcl_gen.generate_power_tcl(config, p/'power.tcl')
            pd_tcl_gen.generate_route_tcl(config, {'net0':'default'}, p/'route.tcl')
            self.assertIn('-core_size 920.0 610.0 10 10 10 10', (p/'pins.tcl').read_text())
            self.assertNotIn('add_stripes', (p/'power.tcl').read_text())
            route=(p/'route.tcl').read_text()
            self.assertNotIn('route_antenna_diode_insertion', route)
            self.assertIn('-route_rule ANALOG', route)
            self.assertIn('route_detail_end_iteration 10', route)


if __name__ == '__main__':
    unittest.main()
