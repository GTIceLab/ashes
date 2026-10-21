"""Create active switch/shifter spans and library-defined intervening fillers.

No bridge insertion, shared peripheral extension or implicit body-net ties are
performed here. Fillers consume physical columns but no selection channels.
"""
from dataclasses import dataclass
from .peripheral_gaps import discover_gaps
from ..placement.companion_groups import register_companion_group


@dataclass
class PeripheralBand:
    role: str
    stage: str
    active: tuple
    fillers: tuple
    profiles: tuple


def build_band(chain, stage, staging_index):
    selected = chain.switch if stage == 'switch' else chain.level_shifter
    if selected is False:
        return None
    island, layout = chain.owner, chain.layouts[0]
    gaps = discover_gaps(island, chain.role, layout, chain.channels)
    choices = [(gap, gap.stage_profile(stage, chain.role)) for gap in gaps]
    for gap, profile in choices:
        if not callable(getattr(chain.cells, profile.get('cell', ''), None)):
            raise ValueError(f'Missing {chain.role}/{stage} filler cell {profile.get("cell")}')
    active, fillers, profiles = [], [], []

    def place(cell, coordinate, kind):
        cell.fg_peripheral = True
        cell.physical_companion = True
        cell.fg_geometry = ('peripheral_band', chain.role, stage, coordinate, kind)
        cell.place((coordinate, staging_index) if layout.axis == 'rows'
                   else (staging_index, coordinate))
        cell.markAbut()

    for span in layout.spans:
        dim = ((span.stop - span.start, 1) if layout.axis == 'rows'
               else (1, span.stop - span.start))
        cell = selected(island.circuit, island, dim=dim)
        place(cell, span.start, 'active')
        active.append(cell)
    for gap, profile in choices:
        cell = getattr(chain.cells, profile['cell'])(island.circuit, island)
        place(cell, gap.coordinate, 'gap')
        fillers.append(cell)
        profiles.append(profile)
    return PeripheralBand(chain.role, stage, tuple(active), tuple(fillers), tuple(profiles))


def register_band(band, generated):
    """Declare the whole band for physical terminations, without filler wiring.

    Active circuit wiring stays in the chain algorithm. Passive filler
    continuity is supplied by the designed abutment, not profile pin metadata.
    """
    register_companion_group(band.active[0].island, (*band.active, *band.fillers),
                             supplies=generated.supplies)
