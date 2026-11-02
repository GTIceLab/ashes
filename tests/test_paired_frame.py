import unittest
import tempfile
from pathlib import Path
from ashes_fg.asic.pd.pd_tcl_gen import generate_pins_tcl
class SideSpreadTests(unittest.TestCase):
    def test_cadence_uses_side_spreading_without_coordinate_assignments(self):
        config={'pins':[{side: {'met_layer':'M3'} for side in 'NSEW'}]}
        groups={side:[side+'[0]',side+'[1]'] for side in 'NSEW'}
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'pins.tcl'
            for mode in ('xy','columns_y_rows_minus_x'):
                generate_pins_tcl(config,(1000,1000,100000,200000),groups,path,process_coordinates=mode)
                text=path.read_text()
                self.assertNotIn('-assign ',text)
                self.assertEqual(text.count('-spread_type side'),4)
                self.assertEqual(text.count('-spread_direction  clockwise'),2)
                self.assertEqual(text.count('-spread_direction  counterclockwise'),2)
