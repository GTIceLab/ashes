import unittest
from unittest.mock import patch
from types import SimpleNamespace
import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.gds_to_celldef.json2python import render_class
from ashes_fg.algorithms.common import native_port
from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid
from ashes_fg.asic.placement.physical_cell_placement import prepare_physical_cells
from ashes_fg.asic.placement.companion_groups import _bind_companion

class NativeCompanionTests(unittest.TestCase):
    def classes(self):
        ns=dict(StandardCell=ac.StandardCell,Port=ac.Port)
        ports=[('signal_w','W',2),('signal_e','E',2),('other_e','E',1)]
        for name in ('Body','Tap'):
            exec(render_class(name,[p[0] for p in ports],ports,[10,10]),ns)
        ns['Body'].physical_companions=dict(edge_left=None,edge_right=None,tap='Tap')
        return ns

    def test_whole_native_body_passes_status_to_both_terminations(self):
        ns=self.classes();c=ac.Circuit();i=ac.Island(c)
        body=ns['Body'](c,i,dim=(1,2));AlgorithmGrid.for_process(i,'xy').place(body,(0,0))
        body.routing_export='native_abutment'
        with patch('ashes_fg.asic.placement.physical_cell_placement._catalog',return_value={'Tap':ns['Tap']}):
            augmented,_=prepare_physical_cells(c,dict(edges='off',taps='both',scope='all'),'xy')
        taps=[cell for cell in augmented.Instances if cell.name=='Tap']
        self.assertEqual(len(taps),2)
        self.assertTrue(all(cell.routing_export=='native_abutment' for cell in taps))

    def test_selected_native_interface_passes_status_without_hiding_other_ports(self):
        ns=self.classes();c=ac.Circuit();i=ac.Island(c)
        body,tap=ns['Body'](c,i),ns['Tap'](c,i)
        for pin in native_port(body,'signal_w').pins:
            pin.connect(ac.Wire(c))
        native_port(body,'signal_w').native_abutment=True
        group=SimpleNamespace(members=(body,),supplies={},endpoints={})
        _bind_companion(group,'W',tap,[body],{}, {}, set())
        self.assertTrue(native_port(tap,'signal_w').native_abutment)
        self.assertFalse(getattr(native_port(tap,'other_e'),'native_abutment',False))

if __name__=='__main__':unittest.main()
