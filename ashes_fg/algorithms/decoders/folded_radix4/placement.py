"""Canonical XY placement for the folded decoder body.

X indexes slots and Y indexes bands. ASHES adapts the staging grid and the
physical block orientation; this algorithm contains no process-axis mapping.
"""


class DecoderGrid:
    """Collect cells placed at canonical local (slot, band) grid points."""
    def __init__(self, context, total_slots):
        self.context = context
        self.instances = []
        if context.placement is None:
            raise ValueError('The decoder context requires an ASHES placement grid')

    def place(self, name, band, slot, signal_level=None, node_ref=None):
        context = self.context
        cell_cls = getattr(context.cells, name, None)
        if cell_cls is None:
            raise ValueError(f'Missing decoder support cell {name}')
        cell = cell_cls(context.circuit, context.island)
        cell.fg_peripheral = True
        cell.physical_companion = True
        cell.fg_geometry = (context.role + '_decoder_band', band, slot)
        context.placement.place(cell, (slot, band))
        cell.fg_signal_level, cell.fg_node_ref = signal_level, node_ref
        self.instances.append(cell)
        return cell


def place_decoder_bands(context):
    """Return local Cartesian XY boxes using canonical cell footprints."""
    boxes = {}
    cursor = context.anchor
    widths = {}
    gap_slots = set()
    for idx, descriptor in context.entries.items():
        slot = descriptor[2]
        info = context.cells[context.island['items'][idx]['name']]
        if slot in widths and widths[slot] != info['width']:
            raise ValueError('Decoder slot has inconsistent widths across bands')
        widths[slot] = info['width']
        if len(descriptor) > 3 and descriptor[3] == 'gap':
            gap_slots.add(slot)
    origins, x = {}, 0
    for slot in sorted(widths):
        origins[slot] = x
        x += widths[slot]
    for band in sorted({descriptor[1] for descriptor in context.entries.values()}):
        heights = set()
        for idx, descriptor in context.entries.items():
            if descriptor[1] != band:
                continue
            info = context.cells[context.island['items'][idx]['name']]
            width, height = info['width'], info['height']
            if descriptor[2] not in gap_slots and width != context.slot_pitch:
                raise ValueError('Decoder helper does not match its canonical XY slot pitch')
            x = origins[descriptor[2]]
            boxes[idx] = [x, cursor, x + width, cursor + height]
            heights.add(height)
        if len(heights) != 1:
            raise ValueError('Decoder band has inconsistent canonical height')
        cursor += heights.pop()
    return boxes
