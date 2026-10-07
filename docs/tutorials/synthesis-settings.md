# ASIC synthesis settings

Run `ashes asic design.py` from the design directory. The CLI loads settings
beside the design file and forwards `synthesis_settings.json` to
`ashes_fg.asic.compile()`. This guide describes the current ASIC implementation.

## Files and design variables

| Source | Purpose |
| --- | --- |
| `design.py` | Defines `Top`, `design_limits`, and `location_islands`. All three are required by the current CLI. |
| `synthesis_settings.json` | Process, library, placement mode, and tool selection. |
| `pd_settings.json` | External tool initialization, native pin-edge settings, power, routing, and export. |
| `router_settings.json` | Internal ASHES detailed-router parameters; absent means use its defaults. |

The CLI adds the design directory to the import path while loading Python.
An `import cells_16nm` therefore uses the design's local library copy if present.
Regenerating a different `cells.py` does not automatically update that copy.
Relative library paths currently resolve from the invocation's working directory.

## Options accepted in synthesis_settings.json

| Option | Type / API default | Meaning |
| --- | --- | --- |
| `process` | string / `"Process"` | Select a supported process below. The API placeholder is not a usable process. |
| `pd_tool` | string / `null` | Required: `"ashes"`, `"cadence"`, or `"openroad"`. The default is not a valid tool selection. |
| `lib_path` | string or `null` / `null` | Library root containing `gds`, `layer_map`, and technology resources. If null, use the package library for the selected technology. |
| `process_coordinates` | string / `"xy"` | Logical placement convention. Choose `"xy"` or `"columns_y_rows_minus_x"`. |
| `place` | boolean / `true` | Generate placement GDS and physical input files. False still writes netlists and external Tcl. |
| `route` | boolean / `true` | With `pd_tool="ashes"`, attempt internal detailed routing after placement. External tool selection prepares inputs/Tcl rather than launching the external tool. |
| `drainSpaceIdx` | integer or `null` / `null` | Island index receiving extra logical drain-mux spacing. Null disables the extra spacing. |
| `drainSpace` | number / `10` | Extra drain-mux spacing, multiplied by the process DBU in placement. Conventionally specified in microns. |
| `gateSpaceIdx` | integer or `null` / `null` | Island index receiving extra logical gate-mux spacing. Null disables the extra spacing. |
| `gateSpace` | number / `10` | Extra gate-mux spacing, multiplied by the process DBU in placement. Conventionally specified in microns. |
| `prBoundary_layer` | integer or `null` / `null` | GDS layer number used by parsing to recognize cell placement boundaries. For the NNopt example, use `108`. |

JSON uses `true`, `false`, and `null`; Python uses `True`, `False`, and `None`.
Unknown keys cause a Python unexpected-keyword error; arbitrary settings are
not silently ignored.

### Supported process strings

| Process | Internal technology name |
| --- | --- |
| `tsmc_350nm` | `vis350` |
| `sky_130nm` | `sky130` |
| `tsmc_16nm` | `tsmcN16` |
| `gf_180nm` | `gf180mcuD` |
| `gf_22nm` | `gfN22` |

Use these exact documented strings. Additional processes require a code and
library integration; this is not a generic process-node parser.

## Python API parameters supplied by the CLI

Do not repeat the following keys in `synthesis_settings.json`: the CLI already
supplies them explicitly, and duplicate keywords produce an error.

| Parameter | Source under CLI | Direct compile API default |
| --- | --- | --- |
| `circuit` | `Top` | Required |
| `project_path` | Directory containing the design file | `"."` |
| `project_name` | Design filename stem | `"project"` |
| `design_limits` | Python variable in the design | `[1e6, 6.1e5]` |
| `location_islands` | Python variable in the design | `None` |
| `qparams` | `router_settings.json`, or `None` | `None` |
| `pd_args` | `pd_settings.json`, or an empty object | `None` |

`design_limits` is `[width, height]` in the flow's nanometer convention and
describes the native physical area. `location_islands` is a sequence of island
anchor pairs in logical placement coordinates; `None` selects automatic
placement. These anchors are different from a cell's `.place([row, col])`.
The current process-specific IO-margin logic is applied automatically.

## Coordinate conventions

`xy` retains the conventional logical layout. `columns_y_rows_minus_x` maps
the logical arrangement 90 degrees counterclockwise into native coordinates:

```text
native_x = native_area_right - logical_y
native_y = native_area_bottom + logical_x
```

Cell `.place([row, col])` retains its logical top-left grid convention.
Increasing columns moves along native +Y; increasing row indices moves along
native +X. Cell geometry is native, and ordinary exported instances remain N.
Logical cell extents are swapped for placement calculations only.

Frame directions are mapped consistently in GDS and pin-placement Tcl:

| Python logical edge | Native edge |
| --- | --- |
| N | W |
| E | N |
| S | E |
| W | S |

The edge properties in `pd_settings.json` remain native: a logical S pin uses
the native E edge's configured layer, dimensions, and offsets. Pin placement
remains sequential; this does not promise placement nearest each connected cell.

## Native physical names and logical Python interfaces

Generated classes can expose a logical port while retaining a native identifier:

```python
self.VG_RUN_n = Port(
    circuit, self, 'VG_RUN_n', 'N', 2 * self.dim[1],
    native_name='VG_RUN_w'
)
```

The logical side controls vector counts and matrix edge selection. Both
netlist formats emit `VG_RUN_w`; LEF/GDS must contain that same physical name.
Setting `process_coordinates` does not regenerate or rename Python definitions.

## Example: NNopt 16nm with external OpenROAD

```json
{
  "process": "tsmc_16nm",
  "pd_tool": "openroad",
  "lib_path": "../../lib/",
  "prBoundary_layer": 108,
  "process_coordinates": "columns_y_rows_minus_x",
  "place": true,
  "route": false,
  "drainSpaceIdx": 0,
  "drainSpace": 0,
  "gateSpaceIdx": 0,
  "gateSpace": 0
}
```

Use `"cadence"` for the Cadence backend, or `"ashes"` for internal routing.
Supply matching `pd_settings.json` for external flows. Technology files,
routing layers, and physical rules are not rotated by the coordinate option.

## Troubleshooting and current limitations

- Missing logical attribute: inspect the actual imported library file and
  regenerate/copy the logical interface definitions, then restart Python.
- Unchanged placement: check `process_coordinates` in the settings beside the
  design file, not just in library generation.
- Unexpected netlist pin suffix: compare `Port.name` with `Port.native_name`
  and the label in prepared native GDS.
- Decimal GDS coordinates: native mapping now converts positions to integer
  database units; converter errors stop synthesis.
- The known mapped IO-margin duplication and external MUX-group naming issues
  remain follow-ups. Full production routing/signoff is not established by the
  synthetic regression tests.

See [PD settings](pd-settings.md) for all pd_settings.json sections and backend-specific options.
