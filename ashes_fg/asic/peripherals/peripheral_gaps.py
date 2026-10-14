"""Discover intervening body columns/rows independently of peripheral topology."""
from dataclasses import dataclass


@dataclass(frozen=True)
class PeripheralGap:
    coordinate: int
    before_output: int
    sources: tuple
    profiles: tuple

    def profile(self, topology, role):
        choices = [profile.get(role, {}).get(topology) for profile in self.profiles]
        if not choices or any(choice is None for choice in choices):
            names = ', '.join(sorted({cell.name for cell in self.sources})) or 'empty grid'
            raise ValueError(f'No {role}/{topology} decoder filler profile at '
                             f'{self.coordinate}: {names}')
        if any(choice != choices[0] for choice in choices[1:]):
            raise ValueError(f'Conflicting decoder filler profiles at {self.coordinate}')
        return choices[0]


    def stage_profile(self, stage, role):
        choices = [getattr(type(cell), 'peripheral_fillers', {}).get(role, {}).get(stage)
                   for cell in self.sources]
        if not choices or any(choice is None for choice in choices):
            names = ', '.join(sorted({cell.name for cell in self.sources})) or 'empty grid'
            raise ValueError(f'No {role}/{stage} peripheral filler profile at '
                             f'{self.coordinate}: {names}')
        if any(choice != choices[0] for choice in choices[1:]):
            raise ValueError(f'Conflicting {role}/{stage} filler profiles at {self.coordinate}')
        return choices[0]


def discover_gaps(island, role, layout, channels):
    """Describe only internal gaps; margins do not require decoder fillers.

    Coordinates use the same logical axis as Layout/Channel. The algorithm
    receives before_output so adding geometry cannot renumber electrical nets.
    All projected source cells must agree on their library filler profile.
    """
    if len(layout.spans) < 2:
        return ()
    axis = 1 if role == 'gate' else 0
    occupied = {n for span in layout.spans for n in range(span.start, span.stop)}
    gaps = []
    for coordinate in range(layout.spans[0].start, layout.spans[-1].stop):
        if coordinate in occupied:
            continue
        sources = []
        for cell in island.instances:
            if getattr(cell, 'fg_peripheral', False):
                continue
            loc = island.getLocation(cell)
            if len(loc[axis]) and int(loc[axis][0]) <= coordinate < int(loc[axis][0]) + cell.dim[axis]:
                sources.append(cell)
        gaps.append(PeripheralGap(coordinate,
                    sum(channel.coordinate < coordinate for channel in channels),
                    tuple(sources), tuple(getattr(type(cell), 'decoder_fillers', {})
                                          for cell in sources)))
    return tuple(gaps)
