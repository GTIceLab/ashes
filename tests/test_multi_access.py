from pathlib import Path
import re
import tempfile
import unittest

import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.gds_to_celldef.json2python import render_class
from ashes_fg.asic.pd.multi_access import pin_plan, canonical_netlist, merged_pins
from ashes_fg.asic.layout.verilog_to_gds import generate_lef


def shape(layer,rect):return dict(Layer=layer,RECT=rect)


class MultiAccessTests(unittest.TestCase):
    def setUp(self):
        self.info={'Cell':dict(width=10000,height=10000,origin=(0,0),cell_pins={
            'SIG_n[0]':shape('M1',(0,9000,1000,10000)),
            'SIG_n[1]':shape('M1',(2000,9000,3000,10000)),
            'SIG_s[0]':shape('M2',(0,0,1000,1000)),
            'SIG_s[1]':shape('M2',(2000,0,3000,1000)),
            'OTHER_w':shape('M1',(0,4000,1000,5000))})}
        self.plan=pin_plan(self.info,dict(same_family_faces_connected=True))

    def test_algorithm_pass_through_preserves_lanes_and_registers_both_accesses(self):
        from ashes_fg.algorithms.common import pass_through, native_port
        namespace = dict(StandardCell=ac.StandardCell, Port=ac.Port)
        ports = [('SIG_n','N',2),('SIG_s','S',2)]
        exec(render_class('Cell',[p[0] for p in ports],ports,[10,10]),namespace)
        circuit = ac.Circuit()
        cell = namespace['Cell'](circuit,ac.Island(circuit))
        pass_through(circuit,cell,'SIG_n','SIG_s')
        pass_through(circuit,cell,'SIG_n','SIG_s')
        entry,exit = native_port(cell,'SIG_n'),native_port(cell,'SIG_s')
        self.assertTrue(all(a.net is b.net for a,b in zip(entry.pins,exit.pins)))
        self.assertIsNot(entry[0].net,entry[1].net)
        groups = circuit.routing_access_contract['groups_by_master']['Cell']
        self.assertEqual(len(groups),1)
        plan = pin_plan(self.info,circuit.routing_access_contract)
        self.assertEqual(plan['Cell']['mapping']['SIG_s[0]'],'SIG_n[0]')
        self.assertEqual(len(plan['Cell']['shapes']['SIG_n[0]']),2)

    def test_duplicate_faces_become_one_pin_with_both_access_shapes(self):
        source='module TOP();\nCell x (.SIG_n({b,a}), .SIG_s({b,a}), .OTHER_w(c));\nendmodule\n'
        text,report=canonical_netlist(source,self.info,self.plan)
        self.assertEqual(text.count('.SIG_n('),1)
        self.assertNotIn('.SIG_s(',text)
        self.assertIn('.OTHER_w(c)',text)
        self.assertEqual(report['duplicate_terminal_references_removed'],2)
        pins=merged_pins('Cell',self.info['Cell']['cell_pins'],self.plan)
        self.assertEqual(len(pins['SIG_n[0]']['access_shapes']),2)
        self.assertEqual({s['Layer'] for s in pins['SIG_n[0]']['access_shapes']},{'M1','M2'})

    def test_alternate_face_alone_still_maps_to_same_canonical_pin(self):
        text,_=canonical_netlist('module TOP();\nCell x (.SIG_s({b,a}));\nendmodule\n',self.info,self.plan)
        self.assertIn('.SIG_n({b, a})',text)
        self.assertNotIn('.SIG_s(',text)

    def test_conflicting_alias_nets_fail_without_shorting(self):
        with self.assertRaisesRegex(ValueError,'different nets'):
            canonical_netlist('module TOP();\nCell x (.SIG_n({b,a}), .SIG_s({b,c}));\nendmodule\n',self.info,self.plan)

    def test_distinct_lanes_and_distinct_families_remain_separate(self):
        mapping=self.plan['Cell']['mapping']
        self.assertNotEqual(mapping['SIG_n[0]'],mapping['SIG_n[1]'])
        self.assertNotEqual(mapping['SIG_n[0]'],mapping['OTHER_w'])
        self.assertEqual(pin_plan(self.info,{}),{})

    def test_shortened_buses_fail_instead_of_shifting_lanes(self):
        with self.assertRaisesRegex(ValueError,'expected 2 bus positions'):
            canonical_netlist('module TOP();\nCell x (.SIG_s(a));\nendmodule\n',self.info,self.plan)

    def test_isolated_lane_can_use_connected_alias_without_shifting(self):
        source='module TOP();\nCell x (.SIG_n({b,__ashes_open_0}), .SIG_s({__ashes_open_1,a}));\nendmodule\n'
        text,_=canonical_netlist(source,self.info,self.plan)
        self.assertIn('.SIG_n({b, a})',text)

    def test_lef_uses_one_port_with_all_shapes_and_no_alias_pin(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'cells.lef'
            generate_lef(['Cell'],self.info,'synthetic',str(path),1000,{},directory,'cadence',routing_pin_plan=self.plan)
            text=path.read_text()
            self.assertNotIn('PIN SIG_s',text)
            section=re.search(r'  PIN SIG_n\[0\]\n(.*?)  END SIG_n\[0\]',text,re.S)[1]
            self.assertEqual(section.count('    PORT\n'),1)
            self.assertEqual(section.count('RECT '),2)
            self.assertIn('LAYER M1',section)
            self.assertIn('LAYER M2',section)

    def test_broadcast_requires_explicit_declaration(self):
        info={'Cell':dict(cell_pins={'P_n':shape('M1',(0,0,1,1)),
                                     'P_s[0]':shape('M1',(1,0,2,1)),
                                     'P_s[1]':shape('M1',(2,0,3,1))})}
        self.assertEqual(pin_plan(info,dict(same_family_faces_connected=True)),{})
        plan=pin_plan(info,dict(groups_by_master={'Cell':[dict(ports=['P_n','P_s'],broadcast=True)]}))
        text,_=canonical_netlist('module TOP();\nCell x (.P_n(p), .P_s({p,p}));\nendmodule\n',info,plan)
        self.assertIn('Cell x (.P_n(p));',text)


class ConventionalBusTests(unittest.TestCase):
    def test_partial_port_preserves_physical_positions(self):
        namespace=dict(StandardCell=ac.StandardCell,Port=ac.Port)
        exec(render_class('Cell',['SIG_n'],[('SIG_n','N',3)],[10,10]),namespace)
        circuit=ac.Circuit();island=ac.Island(circuit);cell=namespace['Cell'](circuit,island)
        wire=ac.Wire(circuit);wire+=cell.SIG_n[2]
        circuit.nameNetsFlat()
        expression=cell.SIG_n.print_conventional(0,0)
        values=expression.split('{')[1].split('}')[0].split(',')
        self.assertEqual(len(values),3)
        self.assertEqual(values[0].strip(),cell.SIG_n[2].net.print())
        self.assertTrue(all('__ashes_open_' in v for v in values[1:]))
        full,_,_=circuit.print_conventional('synthetic')
        for name in circuit._conventional_open_wires:self.assertIn(f'wire {name};',full)


if __name__=='__main__':unittest.main()
