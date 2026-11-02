"""Compose library-selected boundary rows around an electrical matrix body.

Boundary rows replace nominal rows, retaining four placement slots per row.
Unavailable signal lanes are represented by None, never by fabricated Pins.
"""
from types import SimpleNamespace
from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid
from ashes_fg.algorithms.common import native_port
from ashes_fg.algorithms.system_build import join


def build(circuit, island, *, cells, master, rows, columns, unit, recipe, coordinates='xy'):
    row_unit, column_unit = unit
    if rows < 1 or columns < 1 or rows % row_unit or columns % column_unit:
        raise ValueError('Requested matrix lanes must be whole multiples of matrix_unit')
    grid = AlgorithmGrid.for_process(island, coordinates)
    before, after = [], []
    middle_rows = rows // row_unit - len(recipe.get('before', ())) - len(recipe.get('after', ()))
    if middle_rows < 0:
        raise ValueError('Matrix has fewer nominal row units than its boundary recipe')
    cursor = 0
    for name in recipe.get('before', ()):
        cell = grid.create(getattr(cells, name), circuit, dim=(1, columns // column_unit))
        grid.place(cell, (0, cursor))
        cursor += grid.shape(cell)[0]
        before.append(cell)
    core = None
    if middle_rows:
        core = grid.create(getattr(cells, master), circuit,
                           dim=(middle_rows, columns // column_unit))
        grid.place(core, (0, cursor))
        cursor += grid.shape(core)[0]
    for name in recipe.get('after', ()):
        cell = grid.create(getattr(cells, name), circuit, dim=(1, columns // column_unit))
        grid.place(cell, (0, cursor))
        cursor += grid.shape(cell)[0]
        after.append(cell)
    members = tuple(before) + ((core,) if core is not None else ()) + tuple(after)
    for cell in members:
        cell.markAbut()
        # This assembly is electrically continuous through native abutment.
        routed = set(recipe.get('routing_ports', ()))
        if routed:
            names = {p.native_name for p in cell.ports}
            if routed - names:
                raise ValueError(f'{cell.name}: routing_ports references missing native ports {sorted(routed - names)}')
            for port in cell.ports:
                port.native_abutment = port.native_name not in routed
        else:
            cell.routing_export = 'native_abutment'
    for mapping in recipe.get('continuity', ()):
        for cell in (*before, *after):
            reference = core if core is not None else members[0]
            join(native_port(cell, mapping['boundary']), native_port(reference, mapping['body']))
    read_slots, program = [], []
    read_port, program_port = recipe.get('read_port', 'Vd_R_e'), recipe.get('program_port', 'Vd_P_e')
    for cell in members:
        read = native_port(cell, read_port)
        physical_slots = recipe.get('read_slots', {}).get(cell.name, tuple(range(len(read))))
        width = row_unit * cell.dim[0]
        if len(physical_slots) != len(read) or len(set(physical_slots)) != len(read):
            raise ValueError(f'{cell.name}: read_slots must identify every physical read lane once')
        slots = [None] * width
        for index, pin in zip(physical_slots, read.pins):
            if not 0 <= index < width:
                raise ValueError(f'{cell.name}: invalid reserved read-lane map')
            slots[index] = pin
        read_slots.extend(slots)
        program.extend(native_port(cell, program_port).pins)
    return SimpleNamespace(core=core, body=members, before=tuple(before), after=tuple(after),
                           physical_rows=cursor, nominal_rows=rows, functional_columns=columns,
                           read_slots=tuple(read_slots), usable_read_drains=tuple(p for p in read_slots if p is not None),
                           reserved_read_lanes=tuple(i for i, p in enumerate(read_slots) if p is None),
                           programming_drains=tuple(program))
