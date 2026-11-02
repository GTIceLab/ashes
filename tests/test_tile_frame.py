import unittest
from types import SimpleNamespace
import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.class_lib_mux import frame
from ashes_fg.algorithms.system_build import CircuitBuilder
from ashes_fg.algorithms.cab.tile_frame import finish
from ashes_fg.asic.placement.placement_axes import PlacementAxes

class TileFrameTests(unittest.TestCase):
    def builder(self,mode='xy'):
        top=ac.Circuit();f=frame(top)
        b=CircuitBuilder(top,frame=f,cells=SimpleNamespace(),supply_names=('GND','VDD'),process_coordinates=mode)
        for name,side,width in [('N','N',2),('S','S',2),('E','E',2),('W','W',2),('CAB_IN_N','N',1),('CAB_OUT_S','S',1),('CAB_IN_E','E',1),('CAB_OUT_W','W',1),('Sblock_S','S',2),('Sblock_W','W',2),('AB_extra','E',1),('bias','N',1)]:
            b.expose(name,[ac.Wire(top) for _ in range(width)],side)
        return b
    def test_directional_buffer_paths_and_local_analog_preservation(self):
        for mode in ('xy','columns_y_rows_minus_x'):
            b=self.builder(mode);incoming=[ac.Wire(b.circuit) for _ in range(3)];outgoing=[ac.Wire(b.circuit) for _ in range(3)]
            b.expose('old_gate',incoming,'W')
            finish(b,digital=[('GateBits',incoming,outgoing,'N',('old_gate',))])
            ports={p.name:p for p in b.frame.ports}
            self.assertEqual(PlacementAxes(mode).native_side(ports['GateBits_IN'].location),'N')
            self.assertEqual(PlacementAxes(mode).native_side(ports['GateBits_OUT'].location),'S')
            for x,y in zip(ports['GateBits_IN'],ports['GateBits_OUT']):self.assertIsNot(x.net,y.net)
            for x,y in zip(ports['N'],ports['S']):self.assertIsNot(x.net,y.net)
            self.assertIs(ports['GND'][0].net,ports['GND_S'][0].net)
            self.assertEqual(ports['bias'].location,'N')
            self.assertNotIn('bias_S',ports)
            self.assertFalse({'Sblock_S','Sblock_W','AB_extra','old_gate'} & set(ports))
    def test_shared_frame_buses_alias_independent_bits_without_scalar_patch(self):
        b=self.builder();lanes=[ac.Wire(b.circuit) for _ in range(3)]
        finish(b,digital=[('GateBits',lanes,lanes,'N',())])
        source,_,_=b.circuit.print_conventional('test')
        for index in range(3):self.assertIn(f'assign GateBits_OUT[{index}] = GateBits_IN[{index}];',source)
        self.assertIn('assign GND_S = GND;',source)
        self.assertNotIn('patch_',source)
        ports={p.name:p for p in b.frame.ports}
        self.assertEqual(len({id(p.net) for p in ports['GateBits_IN']}),3)
        self.assertEqual(ports['GND'][0].net.print(),'GND')
    def test_mismatched_fabric_width_is_rejected(self):
        b=self.builder();next(p for p in b.frame.ports if p.name=='S').pins.pop()
        with self.assertRaisesRegex(ValueError,'unequal lane counts'):finish(b)
