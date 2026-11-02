"""Decoder wiring must follow profiles, not native cell/pin spelling."""
from types import SimpleNamespace
import unittest

import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.gds_to_celldef.json2python import render_class
from ashes_fg.algorithms.decoders.bridged_radix4 import build
from ashes_fg.algorithms.common import native_port


class DecoderProfileContractTests(unittest.TestCase):
    def test_non_native_master_and_pin_names_are_resolved_from_contract(self):
        namespace = dict(StandardCell=ac.StandardCell, Port=ac.Port)
        metadata = [('ADDR', 'W', 2), ('GO', 'N', 1), ('RESULT', 'S', 4), ('ZERO', 'W', 1)]
        exec(render_class('Logic', [p[0] for p in metadata], metadata, [10, 10]), namespace)
        exec(render_class('Pad', [], [], [10, 10]), namespace)
        cells = SimpleNamespace(Logic=namespace['Logic'], Pad=namespace['Pad'])
        circuit = ac.Circuit()
        island = ac.Island(circuit)
        family = {suffix: 'Pad' for suffix in ('_spacing', '_bridge_spacing', '_A_bridge',
                                              '_B_bridge', '_C_bridge', '_D_bridge')}
        family[''] = 'Logic'
        result = build(circuit, island, 8, cells=cells, master='Logic', role='gate', family=family,
                       interface=dict(address='ADDR', enable='GO', outputs='RESULT',
                                      supplies={'GND': ('ZERO',)}))
        self.assertEqual(len(result.outputs), 8)
        self.assertEqual(len(result.bits), 3)
        self.assertEqual({cell.name for cell in result.instances}, {'Logic', 'Pad'})
        for cell in result.instances:
            if cell.name == 'Logic':
                self.assertIs(native_port(cell, 'ZERO')[0].net, result.supplies['GND'].net)
        self.assertEqual(len({id(pin) for pin in result.outputs}), 8)

    def test_missing_contract_fails_before_creating_decoder_instances(self):
        circuit = ac.Circuit()
        island = ac.Island(circuit)
        before = len(circuit.Instances)
        with self.assertRaisesRegex(ValueError, 'explicit cell-family and pin-interface'):
            build(circuit, island, 8, cells=SimpleNamespace(), master='Unused', role='gate')
        self.assertEqual(len(circuit.Instances), before)
