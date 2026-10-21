# Generated cell libraries and separate profiles

Keep generated cell definitions separate from hand-maintained placement rules:

```text
VMM_Muxs_to_frame_old_node/
    cells_16nm.py            # Generated class definitions and pin interfaces
    cells_16nm_profiles.py   # Hand-maintained metadata and register_profiles()
    VMM_Muxs_to_frame.py     # Design using the selected cell module
```

The current NNopt files live under
5_Tools/run_syn/VMM_Muxs_to_frame_old_node/. There is one profile provider for
that selected library. Do not copy the metadata into algorithm packages or
append it to regenerated cells. If the library moves, move its companion profile
file alongside it, or explicitly import and register a centrally stored provider.

## What belongs where

| Owner | Contents |
| --- | --- |
| Generated cells module | Cell classes, physical names, dimensions, pins and constructors |
| Hand-maintained profiles module | physical_companions, decoder_fillers and peripheral_fillers |
| Placement algorithm | Actual instance placement/wiring and register_companion_group calls |
| Shared ASHES passes | Profile loading, band construction, companion placement and geometry checks |

physical_companions describes which edge/TAP masters belong to a cell family
for its physical boundaries. decoder_fillers describes topology-specific
core/connector fillers over intervening columns. peripheral_fillers describes
switch/shifter filler masters. No signal or supply annotations are required.

These are cell-type contracts. register_companion_group(island, instances, ...)
declares a particular placed band and therefore stays in the algorithm. A profile
file cannot know which instances a design will place together.

Local gap-filler metadata does not implement routing bridges, switch-array or
island extension, or body-signal ties. Those remain separate contracts; see
[fillers versus bridges/extensions](PERIPHERAL_GAP_FILLERS.md).

## Explicit registration

```python
import cells_16nm as cells
from cells_16nm_profiles import register_profiles

register_profiles(cells)
fg = island.generate_fg_peripherals(cells=cells, ...)
```

The provider receives the actual module. It looks up classes with
getattr(cells, class_name), not globals() from the provider's own namespace.
The current VMM design shows this explicit registration.

## Automatic loading

ashes_fg.asic.library.cell_profiles.load_cell_library accepts a module object
or importable module name. For a source file named cells_16nm.py, it checks for
cells_16nm_profiles.py in the same directory and calls register_profiles(cells).
The provider is optional; libraries without one keep their existing behavior.

The loader is used by:

- FG planning/generation, including cells= names and inferred cell modules;
- algorithms.common.resolve_cells, including standalone Sblock_gen;
- the edge/TAP catalog, including physical-only compilation.

No special JSON setting or modification of the generated module is needed.
The loader uses the selected module's file location, rather than searching for
an arbitrary similarly named provider on sys.path. A conflicting cached provider
path, invalid provider interface or registration error is reported, not silently
ignored. Profiles are ordinary Python imports, cached for the process; restart
or explicitly reload the provider after editing its rules.

## Registration behavior and regeneration

The 16nm provider validates all referenced target/filler classes before attaching
metadata. Missing edge/TAP masters retain the physical pass's existing missing
companion handling; a profile does not manufacture a physical view.

Repeated calls preserve attributes already defined on a target class, including
designer overrides. Defaults are deep-copied per class, so modifying one class's
profile cannot unexpectedly change another class's dictionary. To override a
default, register first and then edit that class's metadata; later loading keeps
the override. Registration constructs no circuit cells and writes no files.

Regenerating/reloading cells replaces its classes. Register profiles on those
fresh classes, or let an ASHES entry path do it automatically. There is no
once-per-module applied marker that would skip newly generated class objects.

To add another family or variant, edit the profile provider's class-name map.
Do not change the generated file. Constructor/interface changes still require
matching profiles and physically compatible cells.

Checks cover class-definition preservation, repeated registration, isolated
dictionaries, overrides, missing-class validation, reloaded classes, all three
automatic loading paths and unchanged generated-source contents during use.
Placement checks exercise regular and mixed bands using the separated profiles.

## Simple placement-only profiles

The supplied profile file now lists only cell selections: edge_left, edge_right,
tap, decoder core/connector fillers, and switch/shifter filler masters. It does
not list signals, supplies, aliases, shared buses or mode controls.

Passive filler continuity is a property of the physical library and its
abutment. The designer is responsible for selecting cells whose metal/pins abut
correctly. ASHES checks placement dimensions/contact/overlap, not the electrical
continuity of their internal metal. Gap fillers receive no synthesized signal
buses, address connections or supply ties. A custom circuit may wire them
explicitly when needed; this is outside the placement profile.

Functional decoder, switch and level-shifter wiring remains in the algorithms.
Their circuit supplies and programming controls are still required. This change
removes electrical annotations from placement profiles; it does not remove the
functional circuit wiring. Restart the process to discard previously attached
older profiles, since registration deliberately preserves existing attributes.

## Worked example in NNopt

The README beside the selected cells_16nm_profiles.py now includes real S-block
selections, a complete register_profiles(cells) starter for another source
family, termination-group requirements and design usage. It is located at
5_Tools/run_syn/VMM_Muxs_to_frame_old_node/README.md in the NNopt repository.
