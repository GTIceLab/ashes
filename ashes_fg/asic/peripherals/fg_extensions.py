"""Explicit routed programming extensions using the existing FG chain builders.

The ordered scopes supply real parent pins. No dummy VMM or independent
decoder is created per scope; one switch/shifter/decoder chain owns them all.
"""
from copy import deepcopy
from .fg_peripherals import Chain, Channel, Layout, Span, Peripherals, _signature
from .fg_generation import Generated, wire_chain, _place
from ..placement.algorithm_grid import AlgorithmGrid
from ..library.cell_profiles import load_cell_library


def generate_drain_extension(island, scopes, *, cells, process_coordinates='xy', decoder=None):
    """Generate one drain programming chain for ordered (P, R) pin scopes."""
    from algorithms.decoders.folded_radix4 import DrainDecoder
    cells = load_cell_library(cells)
    parents, channels = [], []
    for program_p, program_r in scopes:
        pp, rr = list(program_p), list(program_r)
        if len(pp) != len(rr) or not pp:
            raise ValueError('Drain extension scopes need equal, nonempty P/R widths')
        for p, r in zip(pp, rr):
            for pin in (p, r):
                if pin.cell.circuit is not island.circuit:
                    raise ValueError('Drain extension targets must belong to the same circuit')
                if pin.cell not in parents:
                    parents.append(pin.cell)
            index = len(channels)
            channels.append(Channel(index, index // 4, index % 4, [p, r]))
    if not channels or len(channels) % 4:
        raise ValueError('Drain extension channels must fit the selected four-lane interface')
    if island.instances or hasattr(island, 'fg_generated'):
        raise ValueError('Build the extension on an empty programming island')
    units = len(channels) // 4
    chain = Chain('drain', island, [island], cells.SWC_Drain, cells.LevelShift_4x_Drain,
                  decoder or DrainDecoder, False, channels,
                  [Layout('columns' if process_coordinates == 'xy' else 'rows',
                          (Span(0, units),), (), (0, units), units)],
                  process_coordinates, cells)
    island.fg = Peripherals(island, drain=chain, signature=_signature(island))
    dim = (1, units) if process_coordinates == 'xy' else (units, 1)
    chain.switches = cells.SWC_Drain(island.circuit, island, dim=dim)
    chain.level_shifters = cells.LevelShift_4x_Drain(island.circuit, island, dim=dim)
    grid = AlgorithmGrid.for_process(island, process_coordinates)
    for slot, (name, cell) in enumerate((('switch', chain.switches), ('shifter', chain.level_shifters))):
        _place(cell, grid.staging_point((0, slot)), ('extension_' + name, units, process_coordinates))
    chain.decoder_placement = AlgorithmGrid.for_process(island, process_coordinates, origin=(0, 4))
    result = chain.build_decoder()
    for cell in result.instances:
        cell.fg_geometry = ('extension_decoder', units, process_coordinates, result.layout, cell.fg_geometry)
    generated = Generated(None, chain, layout=layout_drain_extension)
    wire_chain(chain, generated, tuple(parents), result)
    generated.instances = tuple(island.instances)
    island.fg_generated = generated
    return generated


def layout_drain_extension(context):
    """Place a program-only strip in native XY, then adapt its block pose."""
    from .fg_peripherals import DecoderPlacementContext
    desc = next(iter(context.entries.values()))
    units, coordinates = desc[1:3]
    swapped = coordinates != 'xy'
    cells = ({name: dict(info, width=info['height'], height=info['width'])
              for name, info in context.cells.items()} if swapped else context.cells)
    items = deepcopy(context.island['items'])
    if swapped:
        for item in items.values():
            if 'mat_info' in item:
                mat = item['mat_info']
                mat['mat_row'], mat['mat_col'] = mat['mat_col'], mat['mat_row']
    def size(idx):
        item = items[idx]
        info = cells[item['name']]
        mat = item.get('mat_info', {'mat_row': 1, 'mat_col': 1})
        return info['width'] * mat['mat_col'], info['height'] * mat['mat_row']
    switch = next(idx for idx, d in context.entries.items() if d[0] == 'extension_switch')
    shifter = next(idx for idx, d in context.entries.items() if d[0] == 'extension_shifter')
    sw, sh = size(switch)
    lw, lh = size(shifter)
    if sw != lw:
        raise ValueError('Extended switch/shifter channel pitches differ')
    boxes = {switch: [0, -sh, sw, 0], shifter: [0, -sh-lh, lw, -sh]}
    decoder = {idx: d[4] for idx, d in context.entries.items() if d[0] == 'extension_decoder'}
    callback = next(d[3] for d in context.entries.values() if d[0] == 'extension_decoder')
    scope = dict(context.island, items=items)
    local = callback(DecoderPlacementContext('drain', scope, cells, decoder, 0,
                     (sw / units, sh), (units, 1), sw / units))
    cursor = -sh-lh
    for idx, box in local.items():
        boxes[idx] = [box[0], cursor-box[3], box[2], cursor-box[1]]
    if swapped:
        right = max(box[2] for box in boxes.values())
        return {idx: [box[1], right-box[2], box[3], right-box[0]] for idx, box in boxes.items()}
    return boxes
