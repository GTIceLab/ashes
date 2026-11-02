"""Expand physical slots using library profiles for intervening body cells."""


def gap_slots(context, total_slots):
    by_slot = {}
    for gap in context.gaps:
        # A 2-to-4 leaf spans four outputs. Splitting a leaf requires a
        # different topology/cell family, not an implicit lane permutation.
        if gap.before_output % 4:
            raise ValueError('folded_radix4 gap must fall between complete four-output leaf groups')
        slot = gap.before_output // 4
        if not 0 < slot < total_slots:
            raise ValueError('Decoder gap is outside the leaf slot range')
        profile = gap.profile('folded_radix4', context.role)
        if not all(key in profile for key in ('core', 'connector')):
            raise ValueError('Decoder filler profile requires core and connector cells')
        for name in (profile['core'], profile['connector']):
            if not callable(getattr(context.cells, name, None)):
                raise ValueError(f'Missing decoder gap filler cell {name}')
        by_slot.setdefault(slot, []).append((gap, profile))
    mapping, fillers, position = {}, [], 0
    for slot in range(total_slots):
        for gap, profile in by_slot.get(slot, ()):
            fillers.append((position, gap, profile))
            position += 1
        mapping[slot] = position
        position += 1
    return mapping, fillers


def add_gap_cells(grid, fillers, band_count):
    """Place selected passive masters; electrical continuity relies on abutment.

    No signal buses, address connections or supply aliases are synthesized
    for gap fillers. Functional decoder nodes retain their explicit wiring.
    """
    from ashes_fg.algorithms.common import native_port
    connections = {}
    for slot, gap, profile in fillers:
        access = profile.get("frame_access")
        access_band = (band_count - 1 if access and access["band"] == "outer"
                       else access["band"] if access else None)
        if access and not 0 <= access_band < band_count:
            raise ValueError("Decoder frame-access band is outside the placed decoder")
        for band in range(band_count):
            kind = 'core' if band in (0, 2) else 'connector'
            cell = grid.place(profile[kind], band, slot)
            cell.fg_gap = True
            cell.fg_geometry = (*cell.fg_geometry, 'gap')
            if access and band == access_band:
                connections.setdefault((access['name'],), []).extend(
                    native_port(cell, access['port']).pins)
    return connections
