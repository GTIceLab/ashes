"""Resolve library-owned component interfaces without guessing pin aliases."""
import logging
from types import SimpleNamespace
import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.algorithms.common import native_port, connect
from ashes_fg.algorithms.system_build import join


def bind_component(builder, cell, specification):
    """Connect declared pass-throughs and expose selected public interfaces."""
    pairs = []
    for names in specification.get('pass_through', ()):
        ports = [native_port(cell, name) for name in names]
        if len({len(port) for port in ports}) != 1:
            raise ValueError(f'{cell.name}: pass-through port widths differ: {names}')
        pairs.append(ports)
    public = {name: [pin for native in names for pin in native_port(cell, native).pins]
              for name, names in specification.get('expose', {}).items()}
    for name in (*specification.get('native_internal_ports', ()),
                 *specification.get('deferred_fg_ports', ())):
        native_port(cell, name)
    present = {port.native_name for port in cell.ports}
    for name in specification.get('optional_native_internal_ports', ()):
        if name not in present:
            logging.getLogger(__name__).warning(
                '%s: optional native internal port %s is absent from the cell definition; '
                'no connection created', cell.name, name)
    for ports in pairs:
        for port in ports[1:]:
            join(ports[0], port)
    for name, pins in public.items():
        builder.expose(name, pins, specification.get('side', 'N'))
    return public


def bind_activation(builder, members, device_profiles, specification):
    """Bind explicit rails/bias roles; native-abutment terminals stay undriven.

    A bias terminal is never promoted to a functional CAB signal output.
    Ambiguous labels are not merged by spelling or case normalization.
    """
    groups = {}
    for role, mappings in specification.get('rails', {}).items():
        groups[role] = [pin for cell in members for name in mappings.get(cell.name, ())
                        for pin in native_port(cell, name).pins]
    for role in specification.get('native_rails', ()):
        if role not in groups:
            raise ValueError(f'Unknown native activation rail {role}')
        for pin in groups[role]:
            pin.port.native_abutment = True
    bias = {}
    auxiliary = {}
    for cell in members:
        metadata = device_profiles.get(cell.name, {})
        for role, names in metadata.get('bias_ports', {}).items():
            bias.setdefault(role, []).extend(pin for name in names for pin in native_port(cell, name).pins)
        for role, names in metadata.get('expose', {}).items():
            auxiliary.setdefault(role, []).extend(pin for name in names for pin in native_port(cell, name).pins)
        # Validate these names without connecting their independent model nets.
        for name in metadata.get('native_abutment_ports', ()):
            native_port(cell, name).native_abutment = True
        present = {port.native_name for port in cell.ports}
        for name in metadata.get('optional_native_abutment_ports', ()):
            if name not in present:
                logging.getLogger(__name__).warning(
                    '%s: optional native abutment annotation %s absent; native continuity remains an owner assumption',
                    cell.name, name)
            else:
                native_port(cell, name).native_abutment = True
    rails = {}
    for role, pins in groups.items():
        if not pins:
            raise ValueError(f'Activation rail {role} has no declared terminals')
        rail = ac.Wire(builder.circuit)
        for pin in pins:
            connect(pin, rail)
        rails[role] = rail
    prefix = specification.get('prefix', 'Activation_0_')
    if set(bias) & set(auxiliary):
        raise ValueError('Activation bias and auxiliary roles must have distinct names')
    for role in specification.get('expose_rails', ()):
        builder.expose(prefix + role, rails[role], 'N')
    for role, pins in bias.items():
        if role in specification.get('expose_bias_roles', bias):
            builder.expose(prefix + role, pins, 'N')
    for role, pins in auxiliary.items():
        builder.expose(prefix + role, pins, 'N')
    return SimpleNamespace(members=tuple(members), rails=rails, bias_ports=bias,
                           auxiliary_ports=auxiliary)
