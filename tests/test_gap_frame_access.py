import unittest
from types import SimpleNamespace
from ashes_fg.algorithms.decoders.folded_radix4.gaps import add_gap_cells

class GapFrameAccessTests(unittest.TestCase):
    def grid(self):
        class Grid:
            def __init__(self): self.cells=[]
            def place(self,name,band,slot):
                port=SimpleNamespace(native_name='E_w',pins=[object() for _ in range(4)])
                cell=SimpleNamespace(name=name,ports=[port],fg_geometry=('gate_decoder_band',band,slot))
                self.cells.append(cell)
                return cell
        return Grid()
    def test_only_outer_connector_exports_each_lane_once(self):
        grid=self.grid();profile=dict(core='core',connector='connector',
            frame_access=dict(name='north',band='outer',port='E_w'))
        result=add_gap_cells(grid,[(2,None,profile),(3,None,profile)],5)
        self.assertEqual(len(result[('north',)]),8)
        outer=[c for c in grid.cells if c.fg_geometry[1]==4]
        self.assertEqual(result[('north',)],[p for c in outer for p in c.ports[0].pins])
    def test_without_export_contract_fillers_remain_passive(self):
        grid=self.grid()
        self.assertEqual(add_gap_cells(grid,[(2,None,dict(core='core',connector='connector'))],5),{})
    def test_invalid_export_band_fails(self):
        with self.assertRaisesRegex(ValueError,'outside'):
            add_gap_cells(self.grid(),[(2,None,dict(core='core',connector='connector',
                frame_access=dict(name='north',band=5,port='E_w')))],5)
