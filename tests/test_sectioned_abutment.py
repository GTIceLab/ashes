"""Native S-block returns retain logical nets without routing contacts."""
import unittest
from types import SimpleNamespace
import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.gds_to_celldef.json2python import render_class
from ashes_fg.algorithms.common import native_port
from ashes_fg.algorithms.sblock.sectioned import build
from ashes_fg.asic.pd.routing_export import native_abutment_instances, omit_native_abutment_connections
from ashes_fg.asic.pd.supply_access import INSTANCE, CONNECTION

class SectionedAbutmentTests(unittest.TestCase):
    def test_bottom_returns_are_native_and_top_gate_access_remains(self):
        namespace = dict(StandardCell=ac.StandardCell, Port=ac.Port)
        section = [('g_n','N',2),('gback_s','S',2),('sel_n','N',2),
                   ('selback_s','S',2),('left_w','W',4),('right_e','E',4),('drain_w','W',4)]
        routing = [('track_n','N',4),('track_s','S',4),('return_s','S',4)]
        for name, ports in [('One',section),('Two',section),('Three',section),
                            ('Buffer',[]),('Bridge',routing),('Up',routing),
                            ('Down',routing),('Join',[])]:
            exec(render_class(name,[p[0] for p in ports],ports,[10,10]),namespace)
        profile = dict(lane_unit=4,sections=('One','Two','Three'),buffer='Buffer',
            connector_12='Bridge',connector_23='Join',space_up='Up',space_down='Down',
            section_gate_lane_order=(1,0),
            section_ports=dict(gate='g_n',gate_return='gback_s',selection='sel_n',
                selection_return='selback_s',west='left_w',east='right_e',drain='drain_w'),
            routing_ports=dict(north='track_n',south='track_s',north_return='return_s'))
        circuit=ac.Circuit();island=ac.Island(circuit)
        result=build(circuit,island,12,cells=SimpleNamespace(**namespace),profile=profile)
        for cell in result.sections:
            for front,back in [('g_n','gback_s'),('sel_n','selback_s')]:
                outer,inner=native_port(cell,front),native_port(cell,back)
                self.assertTrue(inner.native_abutment)
                self.assertFalse(getattr(outer,'native_abutment',False))
                self.assertTrue(all(a.net is b.net for a,b in zip(outer.pins,inner.pins)))
                self.assertEqual(len({id(pin.net) for pin in outer.pins}),2)
        source,_,_=circuit.print_conventional('test')
        routing,_=omit_native_abutment_connections(source,native_abutment_instances(circuit))
        for match in INSTANCE.finditer(routing):
            if match.group(2) not in ('One','Two','Three'):continue
            ports=dict(CONNECTION.findall(match.group(4)))
            self.assertNotIn('gback_s',ports)
            self.assertNotIn('selback_s',ports)

if __name__=='__main__':unittest.main()
