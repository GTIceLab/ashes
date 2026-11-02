import json
from pathlib import Path
import tempfile
import unittest
from ashes_fg.asic.pd.supply_access import filter_supplies, apply_supply_access
from ashes_fg.asic.pd.multi_access import pin_plan, canonical_netlist


def policy():
    return dict(mode='exposed_boundary',same_net_terminals_connected_within_cell=True,
                nets=['GND'],port_families=['GND'],tolerance_dbu=0,
                same_net_supplies_connected_across_abutments=True)

def macro():
    return dict(width=10,height=10,origin=(0,0),cell_pins={
        'GND_n':dict(Layer='M1',RECT=(4,9,6,10)),
        'GND_s':dict(Layer='M1',RECT=(4,0,6,1)),
        'SIG_n':dict(Layer='M1',RECT=(1,9,2,10)),
        'SIG_s':dict(Layer='M1',RECT=(1,0,2,1))})

class BoundarySupplyTests(unittest.TestCase):
    def test_three_rows_retain_only_outer_faces_across_islands(self):
        cells={'C':macro()}
        placed={n:dict(master='C',x=0,y=y,orientation='N',island=n)
                for n,y in [('bottom',0),('middle',10),('top',20)]}
        source='module TOP();\n'+''.join(
            f'C {n} (.GND_n(GND), .GND_s(GND));\n' for n in placed)+'endmodule\n'
        text,report=filter_supplies(source,placed,cells,policy(),['M1'])
        self.assertIn('C middle ();',text)
        self.assertIn('C top (.GND_n(GND));',text)
        self.assertIn('C bottom (.GND_s(GND));',text)
        self.assertEqual(report['removed_terminals'],4)
        self.assertFalse(report['no_exposed_access'])
        self.assertTrue(all(r['blocking_neighbors'] for r in report['terminals'] if r['removed']))

    def test_pinless_helper_does_not_break_declared_native_continuity(self):
        cells={'C':macro(),'Helper':dict(width=10,height=10,origin=(0,0),cell_pins={})}
        placed={'bottom':dict(master='C',x=0,y=0,orientation='N'),
                'helper':dict(master='Helper',x=0,y=10,orientation='N'),
                'top':dict(master='C',x=0,y=20,orientation='N')}
        source='module TOP();\nC bottom (.GND_n(GND), .GND_s(GND));\nHelper helper ();\nC top (.GND_n(GND), .GND_s(GND));\nendmodule\n'
        text,report=filter_supplies(source,placed,cells,policy(),['M1'])
        self.assertIn('C bottom (.GND_s(GND));',text)
        self.assertIn('C top (.GND_n(GND));',text)
        self.assertFalse(report['no_exposed_access'])
        placed['top']['y']=21
        _,report=filter_supplies(source,placed,cells,policy(),['M1'])
        self.assertFalse(any(r['removed'] for r in report['terminals'] if r['instance']=='top'))

    def test_isolated_cell_and_real_gap_keep_both_faces(self):
        cells={'C':macro()}
        placed={n:dict(master='C',x=0,y=y,orientation='N') for n,y in [('a',0),('b',11)]}
        source='module TOP();\nC a (.GND_n(GND), .GND_s(GND));\nC b (.GND_n(GND), .GND_s(GND));\nendmodule\n'
        text,report=filter_supplies(source,placed,cells,policy(),['M1'])
        self.assertEqual(text,source)
        self.assertEqual(report['removed_terminals'],0)

    def test_supply_faces_are_not_reintroduced_as_multiaccess_shapes(self):
        info={'C':macro()}
        plan=pin_plan(info,dict(same_family_faces_connected=True),supply_policy=policy())
        self.assertEqual(plan['C']['mapping']['GND_n'],'GND_n')
        self.assertEqual(plan['C']['mapping']['GND_s'],'GND_s')
        self.assertEqual(len(plan['C']['shapes']['GND_n']),1)
        self.assertEqual(plan['C']['mapping']['SIG_s'],'SIG_n')

    def test_no_exposed_supply_anchor_writes_report_without_committing_netlist(self):
        source='module TOP();\nC a (.GND_n(GND));\nC b (.GND_s(GND));\nendmodule\n'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);net=root/'top.v';defs=root/'top.def';report=root/'routing_access.json'
            net.write_text(source)
            defs.write_text('- a C + PLACED ( 0 0 ) N ;\n- b C + PLACED ( 0 10 ) N ;\n')
            with self.assertRaisesRegex(ValueError,'lack exposed access'):
                apply_supply_access(net,defs,{'C':macro()},policy(),['M1'],1000,report)
            self.assertEqual(net.read_text(),source)
            self.assertTrue(json.loads(report.read_text())['no_exposed_access'])

    def test_native_only_contact_cannot_count_as_external_anchor(self):
        source='module TOP();\nC a (.GND_n(GND), .GND_s(GND));\nC b (.GND_s(GND));\nendmodule\n'
        placed={'a':dict(master='C',x=0,y=0,orientation='N'),
                'b':dict(master='C',x=0,y=10,orientation='N')}
        _,report=filter_supplies(source,placed,{'C':macro()},policy(),['M1'],native_abutment={'a':'C'})
        self.assertTrue(report['no_exposed_access'])

    def test_partial_coverage_is_reported_without_removing_whole_pin(self):
        info={'C':macro(),'Half':dict(width=5,height=10,origin=(0,0),cell_pins={})}
        source='module TOP();\nC a (.GND_n(GND), .GND_s(GND));\nHalf b ();\nendmodule\n'
        placed={'a':dict(master='C',x=0,y=0,orientation='N'),
                'b':dict(master='Half',x=0,y=10,orientation='N')}
        _,report=filter_supplies(source,placed,info,policy(),['M1'])
        north=next(r for r in report['terminals'] if r['pin']=='GND_n')
        self.assertFalse(north['removed'])
        self.assertEqual(north['reason'],'partial_coverage_preserved')

class AllSignalAccessTests(unittest.TestCase):
    def test_signal_contacts_follow_same_boundary_rule_without_lane_shorting(self):
        p=policy();p.update(scope='all_signals',same_net_signals_connected_across_abutments=True)
        source='module TOP();\nC a (.SIG_n(bus0), .SIG_s(bus0));\nC b (.SIG_n(bus0), .SIG_s(bus0));\nendmodule\n'
        placed={'a':dict(master='C',x=0,y=0,orientation='N'),
                'b':dict(master='C',x=0,y=10,orientation='N')}
        text,report=filter_supplies(source,placed,{'C':macro()},p,['M1'])
        self.assertIn('C a (.SIG_s(bus0));',text)
        self.assertIn('C b (.SIG_n(bus0));',text)
        self.assertFalse(report['no_exposed_access'])
        self.assertEqual(pin_plan({'C':macro()},dict(same_family_faces_connected=True),p),{})

    def test_explicit_buried_contact_override_is_logged_and_not_silently_applied(self):
        p=policy();p.update(scope='all_signals',same_net_signals_connected_across_abutments=True,
            keep_access_overrides=[dict(instance='a',port='SIG_n',net='run',reason='Owner-selected access')])
        source='module TOP();\nC a (.SIG_n(run), .SIG_s(run));\nC b (.SIG_n(run), .SIG_s(run));\nendmodule\n'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);net=root/'top.v';defs=root/'top.def';report=root/'access.json'
            net.write_text(source);defs.write_text('- a C + PLACED ( 0 0 ) N ;\n- b C + PLACED ( 0 10 ) N ;\n')
            apply_supply_access(net,defs,{'C':macro()},p,['M1'],1000,report)
            self.assertIn('C a (.SIG_n(run));',net.read_text())
            self.assertIn('OVERRIDE: a.SIG_n net=run: Owner-selected access',report.with_suffix('.log').read_text())
            self.assertTrue(json.loads(report.read_text())['access_overrides'])

    def test_exact_bus_override_does_not_match_other_buses(self):
        p=policy();p.update(scope='all_signals',same_net_signals_connected_across_abutments=True,
            keep_access_overrides=[dict(master='C',port='SIG_n',net_bus='W',reason='Final-column access')])
        cells={'C':macro()}
        placed={'a':dict(master='C',x=0,y=0,orientation='N')}
        for net,expected in [('W[0]',True),('W[12]',True),('WIDE[0]',False),('S[0]',False)]:
            _,report=filter_supplies(f'module TOP();\nC a (.SIG_n({net}));\nendmodule\n',placed,cells,p,['M1'])
            self.assertEqual(bool(report['access_overrides']),expected)

    def test_preserve_setting_logs_each_access_error_override(self):
        p=policy();p['on_no_exposed_access']='preserve'
        source='module TOP();\nC a (.GND_n(GND));\nC b (.GND_s(GND));\nendmodule\n'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);net=root/'top.v';defs=root/'top.def';report=root/'access.json'
            net.write_text(source);defs.write_text('- a C + PLACED ( 0 0 ) N ;\n- b C + PLACED ( 0 10 ) N ;\n')
            apply_supply_access(net,defs,{'C':macro()},p,['M1'],1000,report)
            self.assertEqual(net.read_text(),source)
            self.assertIn('OVERRIDE: on_no_exposed_access=preserve',report.with_suffix('.log').read_text())

class NativeAssemblyRoutingTests(unittest.TestCase):
    def test_internal_signal_is_contracted_only_with_native_declaration(self):
        p=policy();p.update(scope='all_signals',same_net_signals_connected_across_abutments=True,
                            native_assembly_routing='boundary_only')
        source='module TOP();\nC a (.SIG_n(signal), .SIG_s(signal));\nC b (.SIG_n(signal), .SIG_s(signal));\nendmodule\n'
        placed={'a':dict(master='C',x=0,y=0,orientation='N'),
                'b':dict(master='C',x=0,y=10,orientation='N')}
        text,report=filter_supplies(source,placed,{'C':macro()},p,['M1'])
        self.assertIn('.SIG_s(signal)',text)
        self.assertFalse(report['native_internal_nets'])
        text,report=filter_supplies(source,placed,{'C':macro()},p,['M1'],
            native_abutment={'a':dict(master='C',ports=['SIG_n'])})
        self.assertEqual(report['native_internal_nets'],['signal'])
        self.assertNotIn('.SIG_s(signal)',text)
        self.assertNotIn('C b (.SIG_n(signal))',text)

    def test_missing_power_access_preserve_override_keeps_one_not_all(self):
        p=policy();p.update(scope='all_signals',same_net_signals_connected_across_abutments=True,
                            native_assembly_routing='boundary_only',on_no_exposed_access='preserve')
        source='module TOP(GND);\ninout GND;\nC a (.GND_n(GND));\nC b (.GND_s(GND));\nendmodule\n'
        placed={'a':dict(master='C',x=0,y=0,orientation='N'),
                'b':dict(master='C',x=0,y=10,orientation='N')}
        text,report=filter_supplies(source,placed,{'C':macro()},p,['M1'])
        self.assertEqual(text.count('(GND)'),2)  # module header plus one cell contact
        self.assertEqual(len(report['access_overrides']),1)
        self.assertIn('selected one unexposed',report['access_overrides'][0]['reason'])
        self.assertTrue(report['no_exposed_access'])

if __name__=='__main__':unittest.main()
