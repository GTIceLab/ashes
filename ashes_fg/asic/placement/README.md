# Placement support

| File | Purpose |
| --- | --- |
| `algorithm_grid.py` | Convert canonical algorithm XY indices to staging row/column indices, including origins and band orientation |
| `placement_axes.py` | Map logical coordinates and matrix members to native process coordinates |
| `physical_cell_placement.py` | Discover edge/TAP cells, augment an isolated circuit, reserve strips and validate contact/overlap |
| `peripheral_layout.py` | Compose automatic mixed-body peripheral bands with real pitches and shared termination strips |
| `companion_groups.py` | Declare algorithm body bands, resolve library companion profiles and connect their boundary endpoints |

Algorithms place functional cells, connectors and fillers. They declare bands
without choosing termination cells:

```python
from ashes_fg.asic.placement.companion_groups import register_companion_group
register_companion_group(island, body_cells, supplies=supplies)
```

The compile-time `physical_cells` settings select edge/TAP sides. Technology
cell classes supply `physical_companions` metadata when their names differ
from the default suffix convention. See
[automatic physical placement](../docs/PHYSICAL_CELL_PLACEMENT_README.md) for
settings, metadata, deferred endpoints and geometry checks.

## Canonical algorithm coordinates

Algorithm grids use `(x, y)`: X is the slot/column index, Y is the row/band
index. Y is an integer row index, distinct from the upward Cartesian Y used
in physical boxes. Algorithms do not swap axes according to a process node.

```python
# A standalone block chooses its backend once; its placement loop stays XY.
from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid
grid = AlgorithmGrid.for_process(island, process_coordinates, origin=(start_x, start_y))
grid.place(cell, (x, y))

# Decoder builders receive a region already adapted by the FG manager.
context.placement.place(cell, (slot, band))
```

For standalone XY staging, the adapter maps `(x, y)` to `(row=y, col=x)`.
For columns_y_rows_minus_x staging, it maps to `(row=x, col=y)`. The existing
PlacementAxes physical stage subsequently resolves native coordinates; library
devices are not rotated. The FG manager supplies chain-specific decoder regions
so gate and drain bodies can use the same local slot/band grid.

Decoder physical callbacks also return canonical **local Cartesian XY boxes**.
The context supplies normalized footprints, slot_pitch and a local anchor of
zero. The algorithm stacks horizontal slot bands. The FG manager applies the
gate/drain orientation and chain anchor, resolves shared companions, translates
the island and performs the final process conversion.

`algorithm_grid.grid_layout()` supports custom variable-pitch layouts while
reserving the shared edge/TAP strips. It creates no filler or bridge cells.
