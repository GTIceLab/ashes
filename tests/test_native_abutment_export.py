from types import SimpleNamespace
from pathlib import Path
import json
import tempfile
import unittest
from ashes_fg.asic.pd.routing_export import native_abutment_instances, omit_native_abutment_connections
from ashes_fg.asic.pd.supply_access import apply_supply_access


class NativeAbutmentExportTests(unittest.TestCase):
    def test_physical_export_without_supply_filter_preserves_full_original(self):
        source='module TOP();\nBoundary cap (.fgmem_n(fg));\nBody body (.Vg_n(fg));\nendmodule\n'
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); net=root/'design.v'; defs=root/'design.def'
            net.write_text(source)
            defs.write_text('- cap Boundary + PLACED ( 0 0 ) N ;\n- body Body + PLACED ( 0 10 ) N ;\n')
            apply_supply_access(net,defs,{},None,[],1000,root/'report.json',native_abutment={'cap':'Boundary'})
            self.assertEqual(net.with_suffix('.full.v').read_text(),source)
            self.assertIn('Boundary cap ();',net.read_text())
            self.assertIn('Body body (.Vg_n(fg));',net.read_text())
            report=json.loads((root/'report.json').read_text())
            self.assertEqual(report['native_abutment_export']['removed_terminals'],1)

    def test_only_explicitly_selected_instance_becomes_connectionless(self):
        source=('module TOP();\nBoundary cap (.fgmem_n({fg1, fg0}), .GND_n(GND));\n'
                'Body body (.Vg_n(gate), .GND_n(GND));\nendmodule\n')
        text, report=omit_native_abutment_connections(source, {'cap':'Boundary'})
        self.assertIn('Boundary cap ();', text)
        self.assertIn('Body body (.Vg_n(gate), .GND_n(GND));', text)
        self.assertEqual(report['removed_terminals'], 3)
        self.assertIn('.fgmem_n({fg1, fg0})', source)

    def test_missing_or_wrong_master_fails_without_silently_selecting_other_cells(self):
        source='module TOP();\nBody placed (.p(n));\nendmodule\n'
        for declared in ({'missing':'Body'}, {'placed':'Other'}):
            with self.assertRaises(ValueError):
                omit_native_abutment_connections(source, declared)

    def test_partial_port_export_validates_placement_and_preserves_full_source(self):
        source = 'module TOP();\nSwitch sw (.Vs_s(vs), .VMM_IN_n(input_net));\nendmodule\n'
        selection = {'sw': dict(master='Switch', ports=['Vs_s'])}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            net, defs = root/'design.v', root/'design.def'
            net.write_text(source)
            defs.write_text('- sw Switch + PLACED ( 0 0 ) N ;\n')
            apply_supply_access(net, defs, {}, None, [], 1000, root/'report.json',
                                native_abutment=selection)
            self.assertIn('Switch sw (.VMM_IN_n(input_net));', net.read_text())
            self.assertEqual(net.with_suffix('.full.v').read_text(), source)
            for placement in ('', '- sw WrongMaster + PLACED ( 0 0 ) N ;\n'):
                net.write_text(source)
                defs.write_text(placement)
                with self.assertRaisesRegex(ValueError, 'no matching physical placement'):
                    apply_supply_access(net, defs, {}, None, [], 1000, root/'report.json',
                                        native_abutment=selection)
                self.assertEqual(net.read_text(), source)

    def test_partial_native_ports_preserve_external_connections(self):
        source = 'module TOP();\nDecode d (.OUT_e({n1, n0}), .ENABLE_w(en), .IN_n(addr));\nendmodule\n'
        text, report = omit_native_abutment_connections(source,
            {'d': dict(master='Decode', ports=['OUT_e', 'ENABLE_w'])})
        self.assertIn('Decode d (.IN_n(addr));', text)
        self.assertEqual(report['removed_terminals'], 3)
        self.assertEqual(report['instances'][0]['removed_ports'], ['OUT_e', 'ENABLE_w'])

    def test_per_lane_native_marks_select_only_matching_array_units(self):
        pins=[SimpleNamespace(native_abutment=i<16) for i in range(28)]
        port=SimpleNamespace(native_name='read_e',pins=pins,location='E',numPins=lambda:4)
        cell=SimpleNamespace(name='Bank',ports=[port],dim=(7,1),isDecoder=lambda:False)
        island=SimpleNamespace(instances=[cell],getLocation=lambda cell:([2],[3]))
        selected=native_abutment_instances(SimpleNamespace(Islands=[island]))
        self.assertEqual(len(selected),4)
        self.assertIn('I_0_5_3_3_0',selected)
        self.assertNotIn('I_0_6_3_4_0',selected)
        self.assertTrue(all(v['ports']==['read_e'] for v in selected.values()))

    def test_model_flag_expands_only_selected_array_instances(self):
        cell=SimpleNamespace(routing_export='native_abutment',name='Boundary',
                             dim=(1,2),isDecoder=lambda:False)
        untouched=SimpleNamespace(name='Body')
        island=SimpleNamespace(instances=[cell,untouched],getLocation=lambda cell:([2],[3]))
        circuit=SimpleNamespace(Islands=[island])
        self.assertEqual(native_abutment_instances(circuit),
                         {'I_0_2_3_0_0':'Boundary','I_0_2_4_0_1':'Boundary'})


if __name__=='__main__':
    unittest.main()
