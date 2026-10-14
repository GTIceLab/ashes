"""Create active switch/shifter spans and library-defined intervening fillers.

No bridge insertion, shared peripheral extension or implicit body-net ties are
performed here. Fillers consume physical columns but no selection channels.
"""
from dataclasses import dataclass
import inspect
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
        cell.place((staging_index, coordinate) if chain.role == 'gate'
                   else (coordinate, staging_index))
        cell.markAbut()

    for span in layout.spans:
        dim = (1, span.stop - span.start) if chain.role == 'gate' else (span.stop - span.start, 1)
        cell = selected(island.circuit, island, dim=dim)
        place(cell, span.start, 'active')
        active.append(cell)
    for gap, profile in choices:
        cell = getattr(chain.cells, profile['cell'])(island.circuit, island)
        place(cell, gap.coordinate, 'gap')
        fillers.append(cell)
        profiles.append(profile)
    return PeripheralBand(chain.role, stage, tuple(active), tuple(fillers), tuple(profiles))


def bind_band(band, generated):
    from .fg_generation import connect
    model = inspect.getmodule(type(band.active[0].circuit))
    supplies = generated.supplies
    for cell, profile in zip(band.fillers, band.profiles):
        buses = {}
        for port in cell.ports:
            family = port.native_name.rsplit('_', 1)[0]
            supply_name = profile.get('supply_aliases', {}).get(family, family)
            source = supplies.get(supply_name)
            if source is not None:
                for pin in port.pins:
                    connect(pin, source)
            elif family in profile.get('controls', ()):
                if family not in generated.controls:
                    generated.controls[family] = model.Wire(cell.circuit)
                for pin in port.pins:
                    connect(pin, generated.controls[family])
            elif family in profile.get('pass_through', ()):
                if family not in buses:
                    buses[family] = model.Bus(cell.circuit, size=len(port))
                if len(buses[family]) != len(port):
                    raise ValueError('Peripheral filler pass-through width mismatch')
                for pin, source in zip(port.pins, buses[family]):
                    connect(pin, source)
        coordinate = cell.fg_geometry[3]
        for family, bus in buses.items():
            generated.gap_connections[(band.role, band.stage, coordinate, family)] = bus
    register_companion_group(band.active[0].island, (*band.active, *band.fillers), supplies=supplies)
