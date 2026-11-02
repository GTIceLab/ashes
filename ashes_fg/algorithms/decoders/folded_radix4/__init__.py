"""Folded radix-4 decoder algorithm: cell selection and logical arrangement.

GateDecoder and DrainDecoder are roles of the same algorithm. Wiring and
physical coordinate handling are implemented in the support modules.
"""
from ashes_fg.asic.peripherals.fg_peripherals import DecoderResult
from .placement import DecoderGrid, place_decoder_bands
from .wiring import wire_radix4
from .gaps import gap_slots, add_gap_cells
from ashes_fg.asic.placement.companion_groups import register_companion_group


def GateDecoder(context):
    """Place and connect the gate decoder for the supplied FG context."""
    if context.role != 'gate':
        raise ValueError('GateDecoder requires a gate context')
    return _place_tree(context)


def DrainDecoder(context):
    """Place and connect the drain decoder for the supplied FG context."""
    if context.role != 'drain':
        raise ValueError('DrainDecoder requires a drain context')
    return _place_tree(context)


def _place_tree(context):
    count, role = context.output_count, context.role
    if count < 2:
        raise ValueError('The 2-to-4 tree needs at least two channels')
    counts, n = [], (count + 3) // 4
    while True:
        counts.append(n)
        if n == 1:
            break
        n = (n + 3) // 4
    prefix = 'GateDecode' if role == 'gate' else 'DrainDecode'
    # The CAB topology packs all higher-level cores into one band. Preserve
    # level/group identity separately from their physical slot coordinates.
    slots, total_slots, occupied = {}, counts[0], set()
    for level in range(1, len(counts)):
        covered = 4**level
        for group in range(counts[level]):
            slot = group * covered + covered // 2 - 1
            if slot >= total_slots:
                slot = total_slots
                total_slots += 1
            if slot in occupied:
                raise ValueError('Decoder core slot collision')
            occupied.add(slot)
            slots[slot] = (level, group)
    band_count = 2 if len(counts) == 1 else len(counts) + 2
    levels = [[] for _ in counts]
    helpers = []
    slot_map, gap_fillers = gap_slots(context, total_slots)
    grid = DecoderGrid(context, total_slots)
    def make(name, band, slot, signal_level=None, node_ref=None):
        return grid.place(name, band, slot_map[slot], signal_level, node_ref)

    def conn_name(index, first=False):
        suffix = '_ALT' if first and index % 4 == 1 else ''
        return f'{prefix}_CON{index % 4}{suffix}'

    # Core bands and complete support bands, including empty physical slots.
    for band in range(band_count):
        for slot in range(total_slots):
            if band == 0:
                if slot < counts[0]:
                    level, group = 0, slot
                    node = make(prefix + '_2x4', band, slot, level)
                    node.fg_decode_level, node.fg_decode_group = level, group
                    levels[0].append(node)
                else:
                    helpers.append(make(prefix + '_2x4_FILL', band, slot))
            elif band == 1:
                name = conn_name(slot, first=True) if slot < counts[0] else prefix + '_CON_FILL'
                helpers.append(make(name, band, slot, 0, (0, slot)))
            elif band == 2:
                if slot in slots:
                    level, group = slots[slot]
                    node = make(prefix + '_2x4', band, slot, level)
                    node.fg_decode_level, node.fg_decode_group = level, group
                    levels[level].append(node)
                else:
                    helpers.append(make(prefix + '_2x4_FILL', band, slot))
            else:
                signal_level = band - 2
                if slot not in slots:
                    name, ref = prefix + '_CON_FILL', None
                else:
                    level, group = slots[slot]
                    ref = (level, group)
                    if signal_level > level:
                        name = prefix + '_CON_FILL'
                    elif signal_level == level:
                        name = conn_name(group)
                    elif signal_level == level - 1:
                        name = prefix + '_CON_TREE'
                    else:
                        name = prefix + '_CON_TREE_FILL'
                helpers.append(make(name, band, slot, signal_level, ref))
    signals = wire_radix4(context.circuit, role, count, levels, helpers)
    gap_connections = add_gap_cells(grid, gap_fillers, band_count)
    for band in range(band_count):
        register_companion_group(context.island,
                                 [cell for cell in grid.instances if cell.fg_geometry[1] == band],
                                 supplies=signals['supplies'])
    return DecoderResult(instances=grid.instances, layout=place_decoder_bands, gap_connections=gap_connections, **signals)
