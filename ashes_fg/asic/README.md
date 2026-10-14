# ASHES ASIC package

This package turns Python circuit designs into netlists and physical layouts.
Its implementations are grouped by function; the table below shows where to
look for each part of the flow.

| Folder | What is inside | Main files |
| --- | --- | --- |
| [model/](model/) | Circuit, island, pin, port, net and standard-cell objects, plus system helpers | `asic_compile.py`, `asic_systems.py` |
| [peripherals/](peripherals/) | FG pin discovery, peripheral plans, switch/shifter generation, shared bits, and the interface to decoder algorithms | `fg_peripherals.py`, `fg_generation.py` |
| [placement/](placement/) | Logical/native coordinate mapping and automatic edge/TAP cell placement | `algorithm_grid.py`, `placement_axes.py`, `physical_cell_placement.py`, `companion_groups.py` |
| [netlist/](netlist/) | Python-to-Verilog compilation | `py_to_verilog.py` |
| [layout/](layout/) | Verilog-to-GDS compilation, layout assembly and text-to-GDS conversion | `verilog_to_gds.py`, `txt2gds.py` |
| [routing/](routing/) | Global routing and global signal connections | `global_router.py`, `add_global.py` |
| [pd/](pd/) | External physical-design tool selection, Tcl generation and KLayout DEF/GDS merging | `pd_tools.py`, `pd_tcl_gen.py`, `def2stream.py` |
| [library/](library/) | Python cell-definition generation from JSON and pin-interface update utilities | `json2python.py`, `update_generated_pin_interfaces.py` |
| [common/](common/) | Shared exceptions and geometry utilities | `exceptions.py`, `utils.py` |
| [lib/](lib/) | Process-specific resources used by the layout flow | Existing technology data |
| [gdsii/](gdsii/) | Bundled GDSII reader/writer | GDS record, tag and type definitions |
| [docs/](docs/) | Usage instructions, settings and architecture notes | [Documentation index](docs/README.md) |

## Files at the package root

`__init__.py` is the public `ashes_fg.asic.compile()` entry point and must remain.
`qrouter_default.json` supplies default routing settings. Python implementations
live only in the subfolders; the old root compatibility modules have been removed.
`__pycache__/` folders are generated automatically by Python.

Use the new imports and script paths listed in the
[migration guide](docs/import-migration.md). External designs, cell-definition
modules and decoder libraries must update their references too.

## Decoder algorithms and cell libraries

Technology-specific decoder algorithms own core/CON/FILL selection, wiring
and multirow/multicolumn placement. They declare companion bands; the shared
physical-cell pass selects and places edge/TAP cells from library metadata.
Decoder algorithms live in the shared project
library at `5_Tools/lib/algorithms/decoders/folded_radix4/__init__.py`. The FG manager calls the selected
algorithm and consumes its results. Designs can select algorithms through
`gate_decoder=` and `drain_decoder=`.

Designs supply their cell-definition module through `cells=`. This package does
not contain a duplicate of the project's `cells_16nm.py` library.

See [FG peripheral usage](docs/FG_PERIPHERALS_README.md) for supported generation
cases and [physical cell placement](docs/PHYSICAL_CELL_PLACEMENT_README.md) for
edge/TAP configuration.

Algorithm placement uses canonical XY indices through AlgorithmGrid. Decoder
callbacks return local XY boxes; ASHES supplies their orientation and anchor.
See [placement support](placement/README.md) for the coordinate contract.

See [FG generation options](docs/FG_GENERATION_OPTIONS.md) for stage switches and custom peripheral algorithms.

See [decoder gap fillers](docs/DECODER_GAPS.md) for traversing registered non-FG columns.

See [local peripheral fillers, routing bridges and extensions](docs/PERIPHERAL_GAP_FILLERS.md)
for automatic mixed bands, general library profiles and separate connection ownership.
