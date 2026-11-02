"""Electrical connection helpers for enabled radix-4 decoder trees.

These helpers connect already-created cells; they do not choose their positions.
Native pin conventions here are those used by the current decoder cell family.
"""
import inspect
from ...common import connect, native_port
from ..common import address_width


def wire_radix4(circuit, role, count, levels, helpers):
    """Return address, enable, selection and supply connections for a tree."""
    model = inspect.getmodule(type(circuit))
    width = address_width(count)
    bits = model.Bus(circuit, size=width)
    enable = model.Wire(circuit)
    ground, vdd = model.Wire(circuit), model.Wire(circuit)
    for nodes in levels:
        nodes.sort(key=lambda node: node.fg_decode_group)
    for level, nodes in enumerate(levels):
        for node in nodes:
            address = native_port(node, 'B_w' if role == 'gate' else 'B_s')
            # Address bus is accessed through the outer connector/termination.
            address.native_abutment = True
            if len(address) != 2:
                raise ValueError('A 2x4 decoder must have two bit inputs')
            for lane, pin in enumerate(address.pins):
                bit = 2 * level + lane
                connect(pin, bits[bit] if bit < width else ground)
            for port in node.ports:
                shared = ground if port.native_name.startswith('GND_') else (
                    vdd if port.native_name.startswith('VDD_') else None)
                if shared is not None:
                    for pin in port.pins:
                        connect(pin, shared)
            # Library SEL ports on opposite boundaries are output pass-throughs.
            names = ('SEL_e', 'SEL_w') if role == 'gate' else ('SEL_n', 'SEL_s')
            for port in node.ports:
                if port.native_name.rsplit('_', 1)[0] in ('SEL', 'SELN'):
                    port.native_abutment = True
            for a, b in zip(native_port(node, names[0]).pins, native_port(node, names[1]).pins):
                connect(a, b)
    for level, nodes in enumerate(levels):
        for group, node in enumerate(nodes):
            pin = native_port(node, 'ENABLE_w' if role == 'gate' else 'ENABLE_s')[0]
            source = enable if level == len(levels) - 1 else native_port(
                levels[level + 1][group // 4], 'SEL_e' if role == 'gate' else 'SEL_n')[group % 4]
            connect(pin, source)
            if level != len(levels) - 1:
                native_port(node, 'ENABLE_w' if role == 'gate' else 'ENABLE_s').native_abutment = True
    def bit_source(level, lane):
        index = 2 * level + lane
        return bits[index] if index < width else ground

    def parent_selection(level, group, lane):
        if level + 1 == len(levels):
            return enable
        parent = levels[level + 1][group // 4]
        return native_port(parent, 'SEL_e' if role == 'gate' else 'SEL_n')[lane]

    injection = model.Wire(circuit) if role == 'drain' else None
    # Assign every passive helper endpoint to the actual bus/branch it carries.
    # Cross-direction bit ports in TREE cells belong to a different level than
    # the straight bus; they must never be implicitly shorted together.
    for helper in helpers:
        signal_level, ref = helper.fg_signal_level, helper.fg_node_ref
        tree = '_CON_TREE' in helper.name
        for p in helper.ports:
            name = p.native_name
            family, _, side = name.rpartition('_')
            for lane, pin in enumerate(p.pins):
                target = None
                if family == 'GND':
                    target = ground
                elif family == 'VDD':
                    target = vdd
                elif family == 'VINJ':
                    target = injection
                elif family == 'B' and signal_level is not None:
                    primary = side in (('n', 's') if role == 'gate' else ('w', 'e'))
                    carried_level = signal_level if primary or not tree else ref[0]
                    target = bit_source(carried_level, lane)
                elif family.startswith('Enable_') and signal_level is not None:
                    code = family.removeprefix('Enable_')
                    if code in ('00', '01', '10', '11'):
                        selection = int(code, 2)
                        if tree:
                            node = levels[ref[0]][ref[1]]
                            target = native_port(node, 'SEL_e' if role == 'gate' else 'SEL_n')[selection]
                        else:
                            group = ref[1]
                            target = parent_selection(signal_level, group, selection)
                elif family == 'Enable' and tree:
                    target = native_port(levels[ref[0]][ref[1]],
                                         'ENABLE_w' if role == 'gate' else 'ENABLE_s')[0]
                elif family.lower() == 'sel' and tree:
                    target = native_port(levels[ref[0]][ref[1]],
                                         'SEL_e' if role == 'gate' else 'SEL_n')[lane]
                if target is not None:
                    connect(pin, target)
                    if family.startswith('Enable_') or family.lower() == 'sel':
                        p.native_abutment = True
    outputs = [pin for node in levels[0] for pin in native_port(
        node, 'SEL_e' if role == 'gate' else 'SEL_n').pins][:count]
    complements = ([pin for node in levels[0] for pin in native_port(node, 'SELN_e').pins][:count]
                   if role == 'gate' else [])
    supplies = {'GND': ground, 'VDD_CORE': vdd}
    if injection is not None:
        supplies['VINJ'] = injection
    return dict(bits=bits, enable=enable, outputs=outputs,
                output_complements=complements, supplies=supplies)
