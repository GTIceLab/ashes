"""Declare cell bands whose outer boundaries receive shared physical companions."""
from dataclasses import dataclass, field


@dataclass
class CompanionGroup:
    members: tuple
    supplies: dict = field(default_factory=dict)
    endpoints: dict = field(default_factory=dict)


def register_companion_group(island, members, *, supplies=None, endpoints=None):
    """Declare a band without instantiating its edge or TAP cells.

    Library classes can provide physical_companions with edge_left, edge_right,
    tap and supply_aliases. Endpoints maps native W/E to signal-family bindings
    for signals exposed only by companions, for example {'W': {'OUT': pins}}.
    """
    members = tuple(members)
    if not members or len(set(members)) != len(members):
        raise ValueError('A companion group needs distinct members')
    if any(cell not in island.instances for cell in members):
        raise ValueError('Companion group members must belong to the island')
    existing = getattr(island, '_companion_groups', [])
    if any(set(members) & set(group.members) for group in existing):
        raise ValueError('A cell cannot belong to two companion groups')
    endpoints = dict(endpoints or {})
    if set(endpoints) - {'W', 'E'}:
        raise ValueError('Companion endpoint sides must be native W/E')
    group = CompanionGroup(members, dict(supplies or {}), endpoints)
    island._companion_groups = existing + [group]
    return group


def companion_names(parent):
    defaults = dict(edge_left=parent.name + '_EdgeL',
                    edge_right=parent.name + '_EdgeR', tap=parent.name + '_TAP')
    return dict(defaults, **getattr(type(parent), 'physical_companions', {}))


def _bounds(island, members):
    locations = [island.getLocation(cell) for cell in members]
    if any(not len(loc[0]) for loc in locations):
        raise ValueError('Place every companion group member before compiling')
    r0 = min(int(loc[0][0]) for loc in locations)
    c0 = min(int(loc[1][0]) for loc in locations)
    r1 = max(int(loc[0][0]) + cell.dim[0] for cell, loc in zip(members, locations))
    c1 = max(int(loc[1][0]) + cell.dim[1] for cell, loc in zip(members, locations))
    # Other strips may insert staging rows between custom-layout members.
    # Physical alignment is checked against the group's final box union.
    return r0, c0, r1, c1


def _pins(value):
    return list(value.pins) if hasattr(value, 'pins') else list(value) if isinstance(value, (tuple, list)) else [value]


def _bind_companion(group, side, companion, boundary, profile, exposed, fulfilled):
    """Connect declared supplies and boundary buses without merging unrelated nets."""
    sources = {}
    for cell in boundary:
        for port in cell.ports:
            if port.native_name.rsplit('_', 1)[-1].upper() == side:
                sources.setdefault(port.native_name.rsplit('_', 1)[0], []).append(port)
    # Some library bands carry a shared bus to both terminations while exposing
    # that bus only on one side of their interior cells.
    for family in profile.get('shared_families', ()):
        if family not in sources:
            candidates = [port for cell in group.members for port in cell.ports
                          if port.native_name.rsplit('_', 1)[0] == family]
            if candidates:
                first = candidates[0]
                if any(len(port) != len(first) or
                       any(a.net is not b.net for a, b in zip(port.pins, first.pins))
                       for port in candidates[1:]):
                    raise ValueError(f'{family}: library-declared shared band bus has inconsistent member nets')
                sources[family] = [first]
    by_family = {}
    for port in companion.ports:
        by_family.setdefault(port.native_name.rsplit('_', 1)[0], []).append(port)
    for family, targets in by_family.items():
        supply_name = profile.get('supply_aliases', {}).get(family, family)
        supply = group.supplies.get(supply_name)
        endpoint = group.endpoints.get(side, {}).get(family)
        source_ports = sources.get(family, [])
        if supply is not None:
            pins = _pins(supply)
        elif endpoint is not None:
            pins = _pins(endpoint)
            fulfilled.add((side, family))
        else:
            pins = [pin for port in source_ports for pin in port.pins]
            if not pins or not any(pin.isConnected() for pin in pins):
                continue
        for port in targets:
            if len(pins) == len(port):
                bindings = pins
            elif len({id(pin.net) for pin in pins}) == 1:
                bindings = [pins[0]] * len(port)
            else:
                raise ValueError(f'{companion.name}: {family} companion width does not match its boundary bus')
            for dst, src in zip(port.pins, bindings):
                if dst.net is not src.net:
                    dst.connect(src)
        for port in exposed.get(family, source_ports):
            port.routing_hidden = True
        # Retain only the outer port if both inner and outer ports are present.
        outer = [port for port in targets if port.native_name.endswith('_' + side.lower())]
        visible = outer or targets
        for port in targets:
            port.routing_hidden = port not in visible
        exposed[family] = visible


def prepare_groups(work, island, catalog, edges, taps, swapped, report, insert):
    """Materialize band companions during the shared physical-cell pass."""
    relationships = []
    axis = 0 if swapped else 1
    for group in getattr(island, '_companion_groups', ()):
        _bounds(island, group.members)
        fulfilled = set()
        for selection, side in (('left', 'W'), ('right', 'E')):
            r0, c0, r1, c1 = _bounds(island, group.members)
            boundary_coordinate = (r0, c0)[axis] if side == 'W' else (r1, c1)[axis]
            boundary = [cell for cell in group.members
                        if int(island.getLocation(cell)[axis][0]) + (0 if side == 'W' else cell.dim[axis])
                        == boundary_coordinate]
            cross_axis = 1 - axis
            boundary.sort(key=lambda cell: int(island.getLocation(cell)[cross_axis][0]))
            profile = companion_names(boundary[0])
            if any(companion_names(cell) != profile for cell in group.members):
                raise ValueError('Companion group members must share one library companion profile')
            names = []
            if edges in (selection, 'both'):
                names.append(profile['edge_left' if side == 'W' else 'edge_right'])
            if taps in (selection, 'both'):
                names.append(profile['tap'])
            dim = (1, c1-c0) if swapped else (r1-r0, 1)
            previous = group.members
            exposed = {}
            for name in names:
                if name is None:
                    continue
                if name not in catalog:
                    report(f'WARNING: {boundary[0].name} band: companion {name} on native {side} '
                           'not found in the library; skipping this cell.')
                    continue
                companion = catalog[name](work, island=island, dim=dim)
                companion.physical_companion = True
                _bind_companion(group, side, companion, boundary, profile, exposed, fulfilled)
                insert(island, companion, previous, side, swapped, dim)
                relationships.append((companion, previous, side))
                previous = companion
        missing = {(side, family) for side, signals in group.endpoints.items() for family in signals} - fulfilled
        if missing:
            raise ValueError(f'Companion-only endpoints {sorted(missing)} require matching edge/TAP cells; '
                             'enable the required sides in physical_cells')
    return relationships


def union_boxes(boxes):
    return [min(box[0] for box in boxes), min(box[1] for box in boxes),
            max(box[2] for box in boxes), max(box[3] for box in boxes)]
