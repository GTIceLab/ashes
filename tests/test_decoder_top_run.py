import unittest
from types import SimpleNamespace
import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.gds_to_celldef.json2python import render_class
from ashes_fg.algorithms.common import native_port
from ashes_fg.algorithms.decoders.bridged_radix4 import build

class DecoderTopRunTests(unittest.TestCase):
    def test_external_analog_access_is_topmost_with_native_intermediate_rows(self):
        namespace=dict(StandardCell=ac.StandardCell,Port=ac.Port)
        core=[('addr_w','W',2),('enable_n','N',1),('out_s','S',4),
              ('analog_n','N',4),('through_s','S',4),('ground_w','W',1)]
        helper=[('analog_n','N',4),('ground_w','W',1)]
        family={}
        for index,suffix in enumerate(('', '_spacing','_bridge_spacing','_A_bridge','_B_bridge','_C_bridge','_D_bridge')):
            name=f'D{index}';family[suffix]=name;ports=core if not suffix else helper
            exec(render_class(name,[p[0] for p in ports],ports,[10,10]),namespace)
        circuit=ac.Circuit()
        result=build(circuit,ac.Island(circuit),30,cells=SimpleNamespace(**namespace),
            master=family[''],role='gate',family=family,
            interface=dict(address='addr_w',enable='enable_n',outputs='out_s',
                run_outputs='through_s',supplies={'GND':('ground_w',)}),
            auxiliary_contract=dict(analog_inputs='analog_n',
                leaf_ports={'analog_n':'analog_input','through_s':'run_output'}))
        self.assertEqual(len(result.run_inputs),30)
        self.assertEqual(len({id(pin.net) for pin in result.run_inputs}),30)
        self.assertTrue(all(a.net is b.net for a,b in zip(result.run_inputs,result.run_outputs)))
        top_ids={id(pin) for cell in result.instances if cell.algorithm_xy[1]==0
                 for pin in native_port(cell,'analog_n').pins}
        self.assertTrue(all(id(pin) in top_ids for pin in result.run_inputs))
        for cell in result.instances:
            port=native_port(cell,'analog_n')
            self.assertEqual(port.native_abutment,cell.algorithm_xy[1]!=0)
            for p in cell.ports:
                if p.native_name=='through_s':
                    self.assertEqual(p.native_abutment,cell.algorithm_xy[1]!=4)

if __name__=='__main__':unittest.main()
