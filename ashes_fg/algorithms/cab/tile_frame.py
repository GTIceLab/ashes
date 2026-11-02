"""CAB tile frame roles; pin coordinates remain the PD tool's side spreading."""
from ashes_fg.asic.placement.placement_axes import PlacementAxes
from ashes_fg.algorithms.system_build import pins


def finish(builder, *, digital=()):
    """Replace temporary exports with paired tile roles and retained local ports.

    digital entries are (name, input pins, output pins, native input side).
    A buffered control has distinct input/output nets. Without a buffer the
    caller explicitly supplies the same lanes for a native pass-through.
    """
    frame = builder.frame
    previous = {p.name: (list(p.pins), p.location) for p in frame.ports}
    for port in frame.ports:
        for pin in port.pins:
            if pin in pin.net.pins:
                pin.net.pins.remove(pin)
    frame.ports = []
    frame.pins = []
    builder.exposed = {}
    axes = PlacementAxes(builder.process_coordinates)
    opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    logical = {axes.native_side(s): s for s in opposite}
    consumed = set()
    pairs = []

    def pair(first, second, left, right, side, *, native=False):
        if len(left) != len(right):
            raise ValueError(f'Tile frame pair {first}/{second} has unequal lane counts')
        if not left:
            return
        first_side = logical[side] if native else side
        builder.expose(first, left, first_side)
        builder.expose(second, right, opposite[first_side])
        pairs.append((first, second))
        consumed.update((first, second))

    for a, b, side in (('N', 'S', 'N'), ('E', 'W', 'E'),
                        ('CAB_IN_N', 'CAB_OUT_S', 'N'), ('CAB_IN_E', 'CAB_OUT_W', 'E')):
        pair(a, b, previous[a][0], previous[b][0], side)
    # Extra native S-block contacts and spare/diagnostic lanes are not tile IO.
    consumed.update(('Sblock_S', 'Sblock_W', 'AB_extra', 'CEW_spare_inputs', 'CNS_spare_inputs'))
    for name, inputs, outputs, side, old_names in digital:
        pair(name + '_IN', name + '_OUT', pins(inputs), pins(outputs), side, native=True)
        consumed.update(old_names)
    for name, values in {**builder.supplies, **builder.controls}.items():
        if name in consumed:
            continue
        power = name.removesuffix('_b') in builder.supplies
        if power or name in ('VGPROG', 'VGRUN'):
            pair(name, name + '_S', pins(values), pins(values), 'N', native=True)
        elif name in ('Drainline_Indirect', 'Drainline_Direct'):
            pair(name, name + '_E', pins(values), pins(values), 'W', native=True)
    # Keep intentional local analog/bias/device interfaces in their previous roles.
    for name, (values, side) in previous.items():
        if name not in consumed:
            builder.expose(name, values, side)
    builder.circuit.tile_frame_pairs = tuple(pairs)
    builder.circuit.tile_frame_local_ports = tuple(name for name in previous if name not in consumed)
