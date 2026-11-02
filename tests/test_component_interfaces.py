"""Component contracts resolve native terminals without signal-role guesses."""
from types import SimpleNamespace
import unittest

import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.class_lib_mux import frame
from ashes_fg.gds_to_celldef.json2python import render_class
from ashes_fg.algorithms.system_build import CircuitBuilder
from ashes_fg.algorithms.common import native_port
from ashes_fg.algorithms.cab.component_interfaces import bind_component, bind_activation
from ashes_fg.algorithms.sblock.sectioned import gate_fillers


def cell_class(name, metadata, width=10):
    namespace = {'StandardCell': ac.StandardCell, 'Port': ac.Port}
    exec(render_class(name, [p[0] for p in metadata], metadata, [width, 22]), namespace)
    return namespace[name]


class ComponentInterfaceTests(unittest.TestCase):
    def setUp(self):
        self.circuit = ac.Circuit()
        self.builder = CircuitBuilder(self.circuit, frame=frame(self.circuit), cells=SimpleNamespace())
        self.island = self.builder.island('Component')

    def test_clock_reset_and_data_pass_through_do_not_short_serial_output(self):
        meta = [(name, name[-1].upper(), 1) for name in
                ('CLK_w', 'CLK_e', 'RSTN_w', 'RSTN_e', 'D_In_w', 'D_In_e', 'D_Out_e')]
        cell = cell_class('Volatile', meta)(self.circuit, self.island)
        public = bind_component(self.builder, cell, dict(
            pass_through=(('CLK_w', 'CLK_e'), ('RSTN_w', 'RSTN_e'), ('D_In_w', 'D_In_e')),
            expose={'CLK': ('CLK_w',), 'RESET': ('RSTN_w',), 'DOUT': ('D_Out_e',)}))
        for first, second in (('CLK_w', 'CLK_e'), ('RSTN_w', 'RSTN_e'), ('D_In_w', 'D_In_e')):
            self.assertIs(native_port(cell, first)[0].net, native_port(cell, second)[0].net)
        self.assertIsNot(native_port(cell, 'D_In_w')[0].net, native_port(cell, 'D_Out_e')[0].net)
        self.assertIsNot(public['CLK'][0].net, public['RESET'][0].net)

    def test_optional_internal_port_absence_warns_without_inventing_port(self):
        cell = cell_class('Synthetic', [('CLK_w', 'W', 1)])(self.circuit, self.island)
        with self.assertLogs('ashes_fg.algorithms.cab.component_interfaces', level='WARNING'):
            bind_component(self.builder, cell, dict(optional_native_internal_ports=('internal_w',)))
        self.assertEqual([port.native_name for port in cell.ports], ['CLK_w'])
        with self.assertRaisesRegex(ValueError, 'expected native port internal_w'):
            bind_component(self.builder, cell, dict(native_internal_ports=('internal_w',)))

    def test_optional_abutment_annotation_absence_does_not_create_connection(self):
        cell = cell_class('Synthetic', [('CLK_w', 'W', 1)])(self.circuit, self.island)
        with self.assertLogs('ashes_fg.algorithms.cab.component_interfaces', level='WARNING'):
            bind_activation(self.builder, [cell], {'Synthetic': dict(optional_native_abutment_ports=('rail_n',))}, {})
        self.assertEqual([p.native_name for p in cell.ports], ['CLK_w'])

    def test_native_activation_bias_is_internal_without_hiding_control_access(self):
        cell = cell_class('Active', [('BIAS_n', 'N', 1), ('BIAS_s', 'S', 1),
                                     ('WTA_n', 'N', 1)])(self.circuit, self.island)
        group = bind_activation(self.builder, [cell], {}, dict(
            rails={'bias': {'Active': ('BIAS_n', 'BIAS_s')}, 'WTA': {'Active': ('WTA_n',)}},
            native_rails=('bias',), expose_rails=('WTA',)))
        self.assertTrue(native_port(cell, 'BIAS_n').native_abutment)
        self.assertTrue(native_port(cell, 'BIAS_s').native_abutment)
        self.assertFalse(getattr(native_port(cell, 'WTA_n'), 'native_abutment', False))
        self.assertIs(native_port(cell, 'BIAS_n')[0].net, native_port(cell, 'BIAS_s')[0].net)
        self.assertIsNot(group.rails['bias'].net, group.rails['WTA'].net)
        self.assertEqual([p.name for p in self.builder.frame.ports], ['Activation_0_WTA'])

    def test_native_bottom_bias_metadata_does_not_create_a_frame_driver(self):
        cell = cell_class('Bot', [('WTA_s', 'S', 1), ('IOUT_e', 'E', 1),
                                  ('GATE_w', 'W', 1)])(self.circuit, self.island)
        group = bind_activation(self.builder, [cell], {'Bot': {
            'bias_ports': {'bias': ('IOUT_e',)},
            'native_abutment_ports': ('IOUT_e', 'GATE_w'),
            'optional_native_abutment_ports': ('WTA_s',)}}, dict(
            rails={'WTA': {'Bot': ('WTA_s',)}}, native_rails=('WTA',),
            expose_bias_roles=(), expose_rails=()))
        self.assertEqual(self.builder.frame.ports, [])
        self.assertTrue(all(p.native_abutment for p in cell.ports))
        self.assertIsNot(group.bias_ports['bias'][0].net, group.rails['WTA'].net)
        self.assertIsNot(native_port(cell,'GATE_w')[0].net, group.rails['WTA'].net)

    def test_bad_public_pin_fails_before_pass_through_mutation(self):
        cell = cell_class('Volatile', [('CLK_w', 'W', 1), ('CLK_e', 'E', 1)])(self.circuit, self.island)
        first, second = native_port(cell, 'CLK_w')[0], native_port(cell, 'CLK_e')[0]
        with self.assertRaisesRegex(ValueError, 'expected native port missing'):
            bind_component(self.builder, cell, dict(pass_through=(('CLK_w', 'CLK_e'),),
                                                    expose={'BAD': ('missing',)}))
        self.assertIsNot(first.net, second.net)

    def test_bias_role_and_explicit_rails_leave_ambiguous_abutment_pins_separate(self):
        active = cell_class('Active', [('VC_n', 'N', 1), ('VC_b_s', 'S', 1),
                                     ('WTA__n', 'N', 1), ('VG_N_n', 'N', 1)])(self.circuit, self.island)
        bot = cell_class('Bot', [('Vc_s', 'S', 1), ('IOUT_e', 'E', 1),
                                ('WTA_s', 'S', 1), ('WTA_B_s', 'S', 1)])(self.circuit, self.island)
        profiles = {'Active': {'native_abutment_ports': ('WTA__n', 'VG_N_n')},
                    'Bot': {'bias_ports': {'WTA_bot_bias': ('IOUT_e',)},
                            'native_abutment_ports': ('WTA_s', 'WTA_B_s')}}
        group = bind_activation(self.builder, [active, bot], profiles,
            dict(rails={'Vc': {'Active': ('VC_n', 'VC_b_s'), 'Bot': ('Vc_s',)}}))
        self.assertIs(native_port(active, 'VC_n')[0].net, native_port(bot, 'Vc_s')[0].net)
        self.assertIs(group.bias_ports['WTA_bot_bias'][0], native_port(bot, 'IOUT_e')[0])
        self.assertIsNot(group.bias_ports['WTA_bot_bias'][0].net, group.rails['Vc'].net)
        self.assertIsNot(native_port(bot, 'WTA_s')[0].net, native_port(bot, 'WTA_B_s')[0].net)
        self.assertEqual(len(native_port(active, 'WTA__n')[0].net.pins), 1)
        self.assertEqual(len(native_port(active, 'VG_N_n')[0].net.pins), 1)

    def test_passive_fillers_carry_independent_tracks_without_extra_gate_channels(self):
        cells = SimpleNamespace(Buffer=cell_class('Buffer', []),
            Route=cell_class('Route', [('n_n', 'N', 4)]), Conn=cell_class('Conn', []))
        inner = cells.Route(self.circuit, self.island)
        tracks = native_port(inner, 'n_n')
        body = SimpleNamespace(body=(inner,), passive_bands=(
            dict(kind='buffer', column=1, signals={}),
            dict(kind='routing', column=2, signals={'north': tuple(tracks.pins)}),
            dict(kind='connector_23', column=4, signals={})))
        fillers = gate_fillers(self.circuit, self.island, cells=cells, sblock=body,
            specifications={'buffer': dict(cell='Buffer'), 'routing': dict(cell='Route', signals={'n_n': 'north'}),
                            'connector_23': dict(cell='Conn')})
        self.assertEqual([cell.algorithm_xy for cell in fillers], [(1, 0), (2, 0), (4, 0)])
        route = native_port(fillers[1], 'n_n')
        self.assertTrue(all(a.net is b.net for a, b in zip(route.pins, tracks.pins)))
        self.assertEqual(len({id(pin.net) for pin in route.pins}), 4)
        self.assertTrue(tracks.native_abutment)
        self.assertFalse(getattr(route, 'native_abutment', False))
        self.assertFalse(any(p.native_name.startswith(('Vg_', 'Vsel_')) for c in fillers for p in c.ports))
