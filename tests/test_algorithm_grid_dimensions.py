"""Golden XY array construction preserves native lanes across conventions."""
import sys
import unittest
from types import ModuleType
from ashes_fg.asic.model import asic_compile as ac
from ashes_fg.asic.library.coordinate_library import for_coordinates
from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid


class NativeCell(ac.StandardCell):
    def __init__(self, circuit, island=None, dim=(1, 1)):
        self.circuit, self.island, self.dim = circuit, island, dim
        self.name, self.size = 'Test', [2, 4]
        self.pins, self.ports = [], []
        self.gate = ac.Port(circuit, self, 'Vg_w', 'W', 2 * dim[0], native_name='Vg_w')
        self.drain = ac.Port(circuit, self, 'Vd_n', 'N', 4 * dim[1], native_name='Vd_n')
        circuit.addInstance(self, island)


class GoldenDimensionsTests(unittest.TestCase):
    def library(self, name, convention='xy', cell=NativeCell):
        lib = ModuleType(name)
        lib.__file__ = None
        lib.cell_coordinates = convention
        lib.Cell = cell
        self.addCleanup(sys.modules.pop, name + '__xy', None)
        self.addCleanup(sys.modules.pop, name + '__columns_y_rows_minus_x', None)
        return lib

    def test_unequal_array_preserves_native_pin_counts(self):
        for convention, dim, position in (
            ('xy', (3, 5), (7, 2)),
            ('columns_y_rows_minus_x', (5, 3), (2, 7)),
        ):
            with self.subTest(convention=convention):
                lib = for_coordinates(self.library('test_' + convention), convention)
                circuit = ac.Circuit()
                island = ac.Island(circuit)
                grid = AlgorithmGrid.for_process(island, convention)
                cell = grid.create(lib.Cell, circuit, dim=(3, 5))
                self.assertEqual(cell.dim, dim)
                self.assertEqual(len(cell.gate.pins), 6)
                self.assertEqual(len(cell.drain.pins), 20)
                self.assertEqual(grid.staging_point((2, 7)), position)
                grid.place(cell, (2, 7))
                self.assertEqual(cell.algorithm_xy, (2, 7))

    def test_mapped_library_can_be_adapted_back_to_xy(self):
        lib = for_coordinates(self.library('test_roundtrip'), 'columns_y_rows_minus_x')
        lib = for_coordinates(lib, 'xy')
        circuit = ac.Circuit()
        island = ac.Island(circuit)
        cell = AlgorithmGrid.for_process(island).create(lib.Cell, circuit, dim=(3, 5))
        self.assertEqual(cell.dim, (3, 5))
        self.assertEqual(cell.gate.location, 'W')
        self.assertEqual(cell.drain.location, 'N')
        self.assertEqual((len(cell.gate.pins), len(cell.drain.pins)), (6, 20))

    def test_invalid_size_rejected(self):
        circuit = ac.Circuit()
        grid = AlgorithmGrid.for_process(ac.Island(circuit))
        with self.assertRaises(ValueError):
            grid.create(NativeCell, circuit, dim=(0, 5))


class ProfiledMatrixTests(GoldenDimensionsTests):
    def test_library_axes_preserve_matrix_lanes(self):
        class ProfiledCell(NativeCell):
            matrix_axes = ('columns', 'rows')

        for convention, staging_dim in (
            ('xy', (8, 11)), ('columns_y_rows_minus_x', (11, 8)),
        ):
            with self.subTest(convention=convention):
                lib = self.library('profiled_' + convention, cell=ProfiledCell)
                lib = for_coordinates(lib, convention)
                circuit = ac.Circuit()
                island = ac.Island(circuit)
                grid = AlgorithmGrid.for_process(island, convention)
                cell = grid.create(lib.Cell, circuit, dim=(44 // 4, 16 // 2))
                self.assertEqual(cell.algorithm_dim, (11, 8))
                self.assertEqual(cell.dim, staging_dim)
                self.assertEqual(grid.shape(cell), (8, 11))
                self.assertEqual(len(cell.gate.pins), 16)
                self.assertEqual(len(cell.drain.pins), 44)
