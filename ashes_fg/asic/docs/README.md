# ASIC package guide

Python implementations are grouped by function:

| Folder | Contents |
| --- | --- |
| `model/` | Circuit, island, standard-cell model and systems |
| `peripherals/` | FG discovery, chain management and generation |
| `placement/` | Coordinate conventions and physical edge/TAP placement |
| `netlist/` | Python-to-Verilog compilation |
| `layout/` | Verilog-to-GDS flow and text-to-GDS conversion |
| `routing/` | Global routing and global connections |
| `pd/` | External PD tools, Tcl generation and DEF-to-stream conversion |
| `library/` | Generated Python cell definitions and pin-interface updates |
| `common/` | Shared exceptions and geometry utilities |
| `lib/` | Existing process resources, kept at the package root |
| `gdsii/` | Bundled GDS reader/writer, kept at the package root |
| `docs/` | ASIC documentation |

The root `__init__.py` remains the public compile entry point. Implementations
live only in the subfolders; old compatibility imports and launchers have been
removed. See the [import and script migration guide](import-migration.md) for
the new paths to use in designs and external cell/algorithm libraries.

Decoder algorithms stay in the shared technology library's
`5_Tools/lib/algorithms/Decoders.py`; this package only invokes their interface.
No test scripts or backups are stored in this package.

## Documentation

- [FG peripheral usage and supported scope](FG_PERIPHERALS_README.md)
- [FG peripheral architecture](FG_PERIPHERAL_DESIGN.md)
- [Physical edge and TAP placement](PHYSICAL_CELL_PLACEMENT_README.md)
- [Synthesis settings](synthesis-settings.md)
