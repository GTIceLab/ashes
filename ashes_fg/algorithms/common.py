"""Small electrical/library utilities independent of algorithm topology."""
from ashes_fg.asic.library.cell_profiles import load_cell_library


def resolve_cells(cells=None):
    """Load a module/name and its optional adjacent profiles; default cells_16nm."""
    return load_cell_library('cells_16nm' if cells is None else cells)


def native_port(cell, name):
    """Find a port by its physical library identifier."""
    ports = [port for port in cell.ports if port.native_name == name]
    if len(ports) != 1:
        raise ValueError(f'{cell.name}: expected native port {name}')
    return ports[0]


def connect(a, b):
    """Merge two connections only when they currently belong to different nets."""
    if a.net is not b.net:
        a.connect(b)


def pass_through(circuit, cell, entry, exit):
    """Declare lane-preserving native continuity and retain both physical accesses."""
    first, second = native_port(cell, entry), native_port(cell, exit)
    if len(first) != len(second):
        raise ValueError(f'{cell.name}: pass-through port widths differ: {entry}, {exit}')
    for a, b in zip(first.pins, second.pins):
        connect(a, b)
    policy = getattr(circuit, 'routing_access_contract', None)
    if policy is None:
        policy = circuit.routing_access_contract = {}
    groups = policy.setdefault('groups_by_master', {}).setdefault(cell.name, [])
    declaration = dict(ports=(entry, exit))
    if declaration not in groups:
        groups.append(declaration)
