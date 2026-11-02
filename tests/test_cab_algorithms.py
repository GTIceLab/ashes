"""Model-only algorithm tests: no process geometry, GDS, or technology files."""
import unittest
from types import SimpleNamespace

import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.gds_to_celldef.json2python import render_class
from ashes_fg.algorithms.cab.matrix_rows import build as matrix_rows
from ashes_fg.algorithms.decoders.bridged_radix4 import pattern
from ashes_fg.algorithms.common import native_port


def library():
    namespace = dict(StandardCell=ac.StandardCell, Port=ac.Port)
    for name, read_width, memory in (('Body', 4, None), ('Top', 3, 'n'), ('Bottom', 3, 's')):
        meta = [('Vd_R_e', 'E', read_width), ('Vd_P_e', 'E', 4),
                ('Vg_n', 'N', 2), ('Vs_n', 'N', 2), ('Vsel_n', 'N', 2)]
        if memory:
            meta.append(('fgmem_' + memory, memory.upper(), 2))
        exec(render_class(name, [p[0] for p in meta], meta, [10, 10]), namespace)
    return SimpleNamespace(**namespace)


class MatrixRowsTests(unittest.TestCase):
    def make(self, rows=16, bottom=True):
        circuit = ac.Circuit()
        island = ac.Island(circuit)
        recipe = dict(before=('Top',), after=('Bottom',) if bottom else (),
            continuity=[dict(boundary='Vg_n', body='Vg_n')],
            read_slots={'Top': (1, 2, 3), 'Bottom': (0, 1, 2)})
        return matrix_rows(circuit, island, cells=library(), master='Body', rows=rows,
                           columns=12, unit=(4, 2), recipe=recipe)

    def test_boundary_rows_replace_instead_of_increasing_requested_rows(self):
        a, b = self.make(bottom=False), self.make()
        self.assertEqual((a.physical_rows, b.physical_rows), (4, 4))
        self.assertEqual((a.nominal_rows, b.nominal_rows), (16, 16))
        self.assertEqual((len(a.usable_read_drains), len(b.usable_read_drains)), (15, 14))
        self.assertEqual((a.reserved_read_lanes, b.reserved_read_lanes), ((0,), (0, 15)))
        self.assertEqual(len(b.programming_drains), 16)

    def test_boundary_net_continuity_preserves_independent_memory_lanes(self):
        assembly = self.make()
        top = assembly.before[0]
        for a, b in zip(native_port(top, 'Vg_n').pins, native_port(assembly.core, 'Vg_n').pins):
            self.assertIs(a.net, b.net)
        memory = native_port(top, 'fgmem_n')
        self.assertIsNot(memory[0].net, memory[1].net)

    def test_every_native_matrix_member_omits_all_routing_contacts(self):
        self.assertTrue(all(cell.routing_export == 'native_abutment' for cell in self.make().body))

    def test_explicit_remote_drain_access_keeps_other_ports_native(self):
        circuit = ac.Circuit()
        assembly = matrix_rows(circuit, ac.Island(circuit), cells=library(),
            master='Body', rows=12, columns=4, unit=(4, 2),
            recipe={'routing_ports': ('Vd_R_e', 'Vd_P_e')})
        body = assembly.core
        self.assertFalse(hasattr(body, 'routing_export'))
        self.assertFalse(native_port(body, 'Vd_R_e').native_abutment)
        self.assertFalse(native_port(body, 'Vd_P_e').native_abutment)
        self.assertTrue(native_port(body, 'Vs_n').native_abutment)
        self.assertEqual(len(assembly.read_slots), 12)

    def test_missing_remote_access_port_is_rejected(self):
        circuit = ac.Circuit()
        with self.assertRaisesRegex(ValueError, 'routing_ports references missing'):
            matrix_rows(circuit, ac.Island(circuit), cells=library(),
                master='Body', rows=4, columns=2, unit=(4, 2),
                recipe={'routing_ports': ('missing_e',)})

    def test_reserved_slot_is_not_replaced_with_another_pin(self):
        assembly = self.make()
        self.assertIsNone(assembly.read_slots[0])
        self.assertIsNone(assembly.read_slots[-1])
        self.assertIs(assembly.read_slots[1], native_port(assembly.before[0], 'Vd_R_e')[0])
        self.assertEqual(len({id(p) for p in assembly.usable_read_drains}), 14)

    def test_small_matrix_can_consist_of_boundary_rows_only(self):
        assembly = self.make(rows=8)
        self.assertIsNone(assembly.core)
        self.assertEqual(len(assembly.usable_read_drains), 6)
        self.assertEqual(assembly.physical_rows, 2)

    def test_insufficient_nominal_rows_fail_before_creating_invalid_core(self):
        with self.assertRaisesRegex(ValueError, 'fewer nominal row units'):
            self.make(rows=4)


class DecoderTopologyTests(unittest.TestCase):
    def test_leaf_coverage_and_unique_root_for_odd_and_even_address_widths(self):
        for count in (1, 4, 8, 16, 30, 64, 128):
            with self.subTest(count=count):
                records = pattern(count)
                cores = [record for record in records if record[3] is not None]
                leaves = [record for record in cores if record[3] == 0]
                self.assertGreaterEqual(len(leaves) * 4, count)
                level = max(record[3] for record in cores)
                self.assertEqual(sum(record[3] == level for record in cores), 1)
                self.assertEqual(len({(r[0], r[1]) for r in records}), len(records))

    def test_legacy_six_bit_tree_cell_pattern(self):
        records = pattern(64)
        self.assertEqual(len(records), 16 * 5)
        self.assertEqual(sum(record[3] == 0 for record in records), 16)
        self.assertEqual(sum(record[3] == 1 for record in records), 4)
        self.assertEqual(sum(record[3] == 2 for record in records), 1)


if __name__ == '__main__':
    unittest.main()
