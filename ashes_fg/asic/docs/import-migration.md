# ASIC imports and script paths

Compatibility modules at the ASIC package root have been removed. Each module
now has one implementation in its functional subfolder. Update external run
files, generated cell-definition imports, decoder algorithms and script settings.
All references inside this ASHES repository have been migrated.

```python
from ashes_fg.asic import compile
import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.asic.model.asic_compile import StandardCell, Port
from ashes_fg.asic.peripherals.fg_peripherals import DecoderResult
```

`from ashes_fg.asic import compile` is unchanged. The table maps former module
names under `ashes_fg.asic` to their new imports and file paths relative to
`ashes_fg/asic/`.

| Former module | New import | New script/file path |
| --- | --- | --- |
| `asic_compile` | `ashes_fg.asic.model.asic_compile` | `model/asic_compile.py` |
| `asic_systems` | `ashes_fg.asic.model.asic_systems` | `model/asic_systems.py` |
| `fg_generation` | `ashes_fg.asic.peripherals.fg_generation` | `peripherals/fg_generation.py` |
| `fg_peripherals` | `ashes_fg.asic.peripherals.fg_peripherals` | `peripherals/fg_peripherals.py` |
| `physical_cell_placement` | `ashes_fg.asic.placement.physical_cell_placement` | `placement/physical_cell_placement.py` |
| `placement_axes` | `ashes_fg.asic.placement.placement_axes` | `placement/placement_axes.py` |
| `global_router` | `ashes_fg.asic.routing.global_router` | `routing/global_router.py` |
| `add_global` | `ashes_fg.asic.routing.add_global` | `routing/add_global.py` |
| `py_to_verilog` | `ashes_fg.asic.netlist.py_to_verilog` | `netlist/py_to_verilog.py` |
| `verilog_to_gds` | `ashes_fg.asic.layout.verilog_to_gds` | `layout/verilog_to_gds.py` |
| `txt2gds` | `ashes_fg.asic.layout.txt2gds` | `layout/txt2gds.py` |
| `pd_tools` | `ashes_fg.asic.pd.pd_tools` | `pd/pd_tools.py` |
| `pd_tcl_gen` | `ashes_fg.asic.pd.pd_tcl_gen` | `pd/pd_tcl_gen.py` |
| `def2stream` | `ashes_fg.asic.pd.def2stream` | `pd/def2stream.py` |
| `json2python` | `ashes_fg.asic.library.json2python` | `library/json2python.py` |
| `update_generated_pin_interfaces` | `ashes_fg.asic.library.update_generated_pin_interfaces` | `library/update_generated_pin_interfaces.py` |
| `exceptions` | `ashes_fg.asic.common.exceptions` | `common/exceptions.py` |
| `utils` | `ashes_fg.asic.common.utils` | `common/utils.py` |

For example, KLayout's DEF conversion script is now
`ashes_fg/asic/pd/def2stream.py`, and the text-to-GDS converter is
`ashes_fg/asic/layout/txt2gds.py`. Update hard-coded script paths accordingly.
The built-in flow already uses these paths.

Keep root `__init__.py` and `qrouter_default.json`. `lib/` and `gdsii/` stay at
their existing locations. Restart long-running Python sessions after migrating
so they do not retain previously imported compatibility modules.
