"""Sectioned four-lane staircase S-block, derived from FPAA_Synthesis/cab1.py."""
from types import SimpleNamespace

from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid
from ashes_fg.algorithms.common import native_port, connect
from ashes_fg.algorithms.system_build import join


def build(circuit, island, count, *, cells, profile, origin=(0, 0)):
    unit = profile['lane_unit']
    if type(unit) is not int or unit < 1 or type(count) is not int or count < unit or count % unit:
        raise ValueError('Sectioned S-block count must be a positive whole number of lane units')
    section_ports, routing_ports = profile['section_ports'], profile['routing_ports']
    if len(profile['sections']) != 3:
        raise ValueError('The sectioned S-block algorithm requires exactly three functional sections')
    units = count // unit
    grid = AlgorithmGrid.for_process(island, 'xy', origin=origin)
    body, sections, north, south, passive_bands = [], [], [], [], []

    def place(master, band, row=0, rows=1):
        cell = grid.create(getattr(cells, master), circuit, dim=(rows, 1))
        grid.place(cell, (band, row))
        cell.markAbut()
        body.append(cell)
        return cell

    sections.append(place(profile['sections'][0], 0, rows=units))
    place(profile['buffer'], 1, rows=units)
    passive_bands.append(dict(kind='buffer', column=1, signals={}))
    for step in range(units):
        band = step + 2
        above = units - step - 1
        up = place(profile['space_up'], band, rows=above) if above else None
        connector = place(profile['connector_12'], band, above)
        down = place(profile['space_down'], band, above + 1, step) if step else None
        upper = native_port(up or connector, routing_ports['north'])
        lower = native_port(down or connector, routing_ports['south'])
        north.extend(upper.pins)
        south.extend(lower.pins)
        passive_bands.append(dict(kind='routing', column=band, signals={'north': tuple(upper.pins)}))
        # Native opposite-edge copies describe the same four vertical tracks.
        if up is not None:
            join(native_port(up, routing_ports['north_return']), native_port(connector, routing_ports['north']))
            native_port(up, routing_ports['north_return']).native_abutment = True
            native_port(connector, routing_ports['north']).native_abutment = True
    sections.append(place(profile['sections'][1], units + 2, rows=units))
    place(profile['connector_23'], units + 3, rows=units)
    passive_bands.append(dict(kind='connector_23', column=units + 3, signals={}))
    sections.append(place(profile['sections'][2], units + 4, rows=units))

    # Gate/control rails pass through every repeated instance of each section.
    # Return each section separately: no blanket short across SEC1/SEC2/SEC3.
    gates, selections = [], []
    order = profile['section_gate_lane_order']
    for section in sections:
        g = native_port(section, section_ports['gate'])
        s = native_port(section, section_ports['selection'])
        for signal, role in ((g, 'gate_return'), (s, 'selection_return')):
            returning = native_port(section, section_ports[role])
            join(signal, returning)
            # Native continuation, not an additional routing endpoint.
            returning.native_abutment = True
        gates.extend(g[i] for i in order)
        selections.extend(s[i] for i in order)
    programming_port = native_port(sections[0], section_ports['drain'])
    # The adjoining C-block supplies the programming drain by native abutment.
    programming_port.native_abutment = True
    return SimpleNamespace(
        body=tuple(body), sections=tuple(sections), gates=tuple(gates), selections=tuple(selections),
        north=tuple(north), south=tuple(south),
        west=tuple(native_port(sections[0], section_ports['west']).pins),
        east=tuple(native_port(sections[2], section_ports['east']).pins),
        programming_drains=tuple(programming_port.pins),
        width_bands=units + 5, height_units=units, passive_bands=tuple(passive_bands))


def gate_fillers(circuit, island, *, cells, sblock, specifications):
    """Fill only passive bands, binding any carried signal tracks explicitly."""
    grid = AlgorithmGrid.for_process(island, 'xy')
    fillers = []
    for band in sblock.passive_bands:
        if band['kind'] not in specifications:
            raise ValueError(f"Missing gate-side filler profile for {band['kind']}")
        spec = specifications[band['kind']]
        cell = grid.create(getattr(cells, spec['cell']), circuit)
        grid.place(cell, (band['column'], 0))
        cell.markAbut()
        cell.fg_geometry = ('section_gate', band['column'])
        for native, signal in spec.get('signals', {}).items():
            if signal not in band['signals']:
                raise ValueError(f"Unknown S-block filler signal {signal!r}")
            join(native_port(cell, native), band['signals'][signal])
            # The filler carries this bus to its outer access; do not route
            # a second contact on the abutting body side.
            inner = {id(pin) for pin in band['signals'][signal]}
            for member in sblock.body:
                for port in member.ports:
                    if port.pins and all(id(pin) in inner for pin in port.pins):
                        port.native_abutment = True
        fillers.append(cell)
    return tuple(fillers)
