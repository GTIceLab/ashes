"""S-block body, routing tiles and fillers; companions belong to ASHES."""
import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.asic.placement.companion_groups import register_companion_group
from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid
from ...common import connect, native_port, resolve_cells
from ..common import validate_input_count


def Sblock_gen(circuit, Sblock_Island, sblock_input=8, start_loc_x=0, start_loc_y=0,
               *, cells=None, process_coordinates='columns_y_rows_minus_x', peripherals=True,
               below=None):
    """Place the body and declare its termination bands for physical_cells.

    start_loc_x/start_loc_y retain their positional interface and specify the
    canonical XY origin. Pin access uses native library identifiers.
    below places this complete body after a reference cell/group. With
    peripherals=False, body columns start at zero; no peripheral slots are
    reserved. The result exposes body cells and drain-programming lane groups.
    """
    lib = resolve_cells(cells)
    validate_input_count(sblock_input)
    if below is not None:
        if (start_loc_x, start_loc_y) != (0, 0):
            raise ValueError('Use either below or an explicit S-block origin')
        start_loc_x, start_loc_y = AlgorithmGrid.for_process(
            Sblock_Island, process_coordinates).below(below)
    grid = AlgorithmGrid.for_process(Sblock_Island, process_coordinates,
                                     origin=(start_loc_x, start_loc_y))
    units = sblock_input // 4
    supplies = {name: ac.Wire(circuit) for name in ('GND', 'VINJ')}
    signals = {name: [ac.Wire(circuit) for _ in range(sblock_input)]
               for name in ('Sblock_N', 'Sblock_S', 'Sblock_E', 'Sblock_W')}
    selects = [[ac.Wire(circuit) for _ in range(2)] for _ in range(3)]
    vgrun = ac.Wire(circuit)
    body = []
    drain_programming = []
    body_column = 2 if peripherals else 0

    def place(name, band, slot):
        cell = getattr(lib, name)(circuit, Sblock_Island)
        cell.physical_companion = True  # Compact 1x1 placement metadata.
        grid.place(cell, (slot, band))
        cell.markAbut()
        body.append(cell)
        for port in cell.ports:
            supply = supplies.get(port.native_name.rsplit('_', 1)[0])
            if supply is not None:
                for pin in port.pins:
                    connect(pin, supply)
        return cell

    # Only the standalone peripheral mode reserves its shifter/switch columns.
    core_bands = ((0, 'Sblock_N'), (units + 3, 'Sblock_S_0'), (units + 4, 'Sblock_S_1'))
    for index, (band, name) in enumerate(core_bands):
        members = [place(name, band, body_column + unit) for unit in range(units)]
        for unit, cell in enumerate(members):
            drain_programming.append((cell, slice(4 * unit, 4 * unit + 4)))
            for pin, wire in zip(native_port(cell, 'Vsel_w').pins, selects[index]):
                connect(pin, wire)
            output_name = 'N_n' if index == 0 else 'S_s' if index == 2 else None
            if output_name is not None:
                target = signals['Sblock_N' if index == 0 else 'Sblock_S']
                for lane, pin in enumerate(native_port(cell, output_name).pins):
                    connect(pin, target[4 * unit + lane])
        register_companion_group(Sblock_Island, members, supplies=supplies)
        if peripherals:
            place('LevelShift_2x_Gate', band, 0)
            switch = place('SWC_Gate', band, 1)
            for pin in native_port(switch, 'VG_RUN_w').pins:
                connect(pin, vgrun)

    # Routing bands retain their diagonal active tiles and passive fill slots.
    for offset in range(units + 2):
        band = offset + 1
        members = []
        for unit in range(units):
            name = ('Sblock_Filler_Start' if offset == 0 else
                    'Sblock_Filler_End' if offset == units + 1 else
                    'Sblock_Routing' if unit == offset - 1 else 'Sblock_Filler')
            member = place(name, band, body_column + unit)
            members.append(member)
            drain_programming.append((member, slice(4 * unit, 4 * unit + 4)))
        endpoints = {}
        if 1 <= offset <= units:
            start = 4 * (offset - 1)
            endpoints = {'W': {'OUT': signals['Sblock_E'][start:start + 4]},
                         'E': {'OUT': signals['Sblock_W'][start:start + 4]}}
        register_companion_group(Sblock_Island, members, supplies=supplies, endpoints=endpoints)
        small = offset in (0, units + 1)
        suffix = '_Small' if small else ''
        if peripherals:
            # Select traversal masters from the body cell's registered profile.
            rules = type(members[0]).peripheral_fillers['gate']
            place(rules['level_shifter']['cell'], band, 0)
            place(rules['switch']['cell'], band, 1)

    # Preserve the historical connection ordering, while using core pin names
    # rather than referencing TAP instances that do not exist until compilation.
    signals['VSEL'] = selects[2] + selects[1] + selects[0]
    signals['VGRUN'] = vgrun
    signals['supplies'] = supplies
    signals['body'] = tuple(body)
    signals['drain_programming'] = tuple(drain_programming)
    return signals
