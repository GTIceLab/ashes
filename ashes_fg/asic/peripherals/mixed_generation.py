"""Local abutting peripheral bands across registered non-FG body columns.

This generator creates no routing bridges, cross-island extensions or sharing.
Advanced body interfaces and bridge-dependent roles remain explicit callbacks.
"""
from .fg_generation import Generated, wire_chain
from .fg_peripherals import _signature
from .peripheral_bands import build_band, bind_band
from ..placement.algorithm_grid import AlgorithmGrid
from ..placement.peripheral_layout import layout_mixed


def generate_mixed(island, plan, roles):
    parents = {pin.cell for role in roles for channel in
               (getattr(plan, role).channels if getattr(plan, role) else ())
               for pin in channel.targets}
    if not parents or any(parent.name != 'IndirectVMM_4x2' for parent in parents):
        raise ValueError('Automatic abutting bands require VMM programming interfaces; '
                         'select VMM parents explicitly with parents= or use a custom algorithm')
    for role in roles:
        chain = getattr(plan, role)
        if chain is None:
            continue
        if chain.members != [island]:
            raise ValueError('Peripheral extension is separate from local gap filling; use an extension algorithm')
        if any(channel.bridge_required for channel in chain.channels):
            raise ValueError(f'{role}: a routing bridge is required; local gap fillers do not '
                             'implement bridges or connection ties. Use roles= to generate '
                             'only local roles, and handle this role explicitly.')
    body = tuple(island.instances)
    bounds = []
    for cell in body:
        loc = island.getLocation(cell)
        if not len(loc[0]) or not len(loc[1]):
            raise ValueError('Place the complete island body before generating peripheral bands')
        row, col = int(loc[0][0]), int(loc[1][0])
        if getattr(cell, 'fg_peripheral', False):
            raise ValueError('Generate bands from the original ungenerated body')
        bounds.append((row, col, row + cell.dim[0], col + cell.dim[1]))
        cell.fg_geometry = ('mixed_body', row, col, *cell.dim)
    end_row = max(b[2] for b in bounds)
    end_col = max(b[3] for b in bounds)
    start_row = min(b[0] for b in bounds)
    start_col = min(b[1] for b in bounds)
    generated = Generated(plan.gate, plan.drain, layout=layout_mixed)
    for role in roles:
        chain = getattr(plan, role)
        if chain is None:
            continue
        bands = []
        # Staging is only a unique indexing space. Physical abutment is resolved
        # below from real footprints; these reserved gaps add no physical space.
        origin = end_row + 4 if role == 'gate' else end_col + sum(
            getattr(plan, r).output_count for r in roles if getattr(plan, r)) + 8
        for stage in ('switch', 'level_shifter'):
            band = build_band(chain, stage, origin + len(bands))
            if band is not None:
                bands.append(band)
                generated.bands[(role, stage)] = band
        chain.switches = next((b.active for b in bands if b.stage == 'switch'), None)
        chain.level_shifters = next((b.active for b in bands if b.stage == 'level_shifter'), None)
        chain.decoder_placement = (AlgorithmGrid(island, (origin + len(bands) + 2, start_col))
                                   if role == 'gate' else AlgorithmGrid(
                                       island, (start_row, origin + len(bands) + 2), (1, 0), (0, 1)))
        plan.signature = _signature(island)
        result = None if chain.decoder is False else chain.build_decoder()
        wire_chain(chain, generated, tuple(parents), result)
        for band in bands:
            bind_band(band, generated)
        if result is not None:
            if not callable(result.layout):
                raise ValueError('Selected decoder must return a physical layout callback')
            for cell in result.instances:
                cell.fg_geometry = ('mixed_decoder', role, result.layout, cell.fg_geometry,
                                    chain.layouts[0].spans[0].start)
            for key, bus in result.gap_connections.items():
                generated.gap_connections[(role, 'decoder', *key)] = bus
    return generated

