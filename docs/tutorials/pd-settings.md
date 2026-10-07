# Physical-design settings: pd_settings.json

Place `pd_settings.json` beside the design Python file. The CLI reads this
exact filename and passes its contents as `pd_args` to ASIC compilation.
Select `pd_tool` in `synthesis_settings.json`: `cadence` or `openroad`.
ASHES writes Tcl; it does not automatically launch either external tool.

This reference describes the current `pd_tcl_gen.py`, including backend
differences. It documents generated commands, not a guarantee that arbitrary
layer names, dimensions, or tool versions are valid for your process.

## Structure and units

Use five sections: `init`, `pins`, `power`, `route`, and `signoff`.
For compatibility with both backends, each section is a list of objects.
OpenROAD also accepts a single object for a section; Cadence generally expects
the list form. Repeated keys usually use the last value. Technology-LEF paths
are collected in initialization; OpenROAD also collects Liberty paths.

Dimensions in PD settings are in **microns**. Layer names are native process
names. Keep `process_coordinates` in synthesis settings, not this file.

## init — libraries, supply nets, and non-default routing rules

| Key | Default / requirement | Backend behavior |
| --- | --- | --- |
| `tlef_path` | Supply explicitly; string or list | Technology/additional LEFs. OpenROAD rejects an empty list. Both also read generated `../inputs/cells.lef`. |
| `liberty_path` | Empty; string or list | OpenROAD only: timing libraries. Cadence does not consume this key. |
| `pwr_nets` | Cadence empty; OpenROAD falls back to the first power-global net | Use a comma-separated string for portability, e.g. `"VDD,VINJ"`. |
| `gnd_nets` | Cadence empty; OpenROAD falls back to the last power-global net | Use a comma-separated string, e.g. `"GND"`. |
| `ndr` | Empty list | Rule definitions; properties below. |

Each `ndr` entry supports:

| Key | Meaning |
| --- | --- |
| `name` | Required rule identifier. Define every rule assigned to a circuit net. |
| `width` | Object mapping routing layer to width in microns. |
| `spacing` | Object mapping routing layer to spacing in microns. |
| `min_cut` | Object mapping cut layer to minimum cut count. OpenROAD requires positive integers and actual CUT layers. |
| `via` | OpenROAD only: string or list of allowed via names. |

ASHES net metadata assigns these rules during route generation. A net whose
rule is `default` is assigned `ANALOG` by both backends, so define `ANALOG`
when using that behavior. OpenROAD reports conflicting assignments to the
same resolved net. Its initialization currently links the conventional
netlist's top module `TOP`.

## pins — native frame edges

| Key | Default | Meaning |
| --- | --- | --- |
| `site` | Cadence `core`; OpenROAD auto-detects | LEF CORE placement-site name. OpenROAD auto-detection requires exactly one CORE site; otherwise specify one. |
| `place_type` | `side` | Cadence forwards it as spread type. OpenROAD only accepts `side`. |
| `N`, `S`, `E`, `W` | No edge block | Per-native-edge properties. A pin group without a matching edge block is skipped. |

Each edge object supports:

| Key | Default | Meaning |
| --- | --- | --- |
| `met_layer` | Cadence `3`; OpenROAD `M3` | Cadence extracts the number from the value. OpenROAD uses the exact layer name. `M3` works for the examples. |
| `pin_width` | `0.3` | Microns; Cadence pin width, OpenROAD X size. |
| `pin_height` | `0.3` | Microns; Cadence pin depth, OpenROAD Y size. |
| `offset_start` | `0.6` | Margin from the start of the native edge. |
| `offset_end` | `0.6` | Margin from the end of the native edge. |

OpenROAD requires nonnegative offsets whose sum is smaller than the edge
length. It spreads multiple pins evenly between margins and centers a single
pin. Cadence emits side-spread commands with backend-specific spread direction.

Python frame edges are logical. In `columns_y_rows_minus_x` mode, ASHES maps
N→W, E→N, S→E, W→S before choosing these native edge properties. For example,
Python `createPort("S", "SelN_0", ...)` uses the E block here. Pin names and
connections are unchanged. Spacing remains sequential, not proximity-based.

## power — globals and rings or stripes

Use one object inside the `power` list. **Cadence reads only the first object**;
OpenROAD merges the section. Do not split a Cadence power configuration across
several objects.

`power_globals` supports:

| Key | Default | Meaning |
| --- | --- | --- |
| `nets` | `["VDD", "GND"]` | Ordered net list; use an array for both backends. OpenROAD also accepts a comma/space-separated string. |
| `type` | `rings` | `rings` or `stripes`. |
| `top_via_stack` | Cadence `M7` | Cadence stacked-via top limit. OpenROAD does not translate it. |
| `bot_via_stack` | Cadence `M1` | Cadence stacked-via bottom limit. OpenROAD does not translate it. |

Each `rings` entry needs `horiz_layer`, `vert_layer`, `width`, `spacing`, and
`offset`. Optional `center` defaults to false. OpenROAD rejects `center=true`;
use explicit offsets instead.

Each `stripes` entry supports:

| Key | Default / requirement | Meaning |
| --- | --- | --- |
| `layer` | Required | Native routing layer. |
| `direction` | Set explicitly for Cadence; optional in OpenROAD | Horizontal/vertical. OpenROAD checks a supplied direction against the technology layer. |
| `width`, `spacing` | Required | Microns. |
| `no_of_sets` | `1` | Cadence number of sets; forwarded as OpenROAD number of straps. |
| `start_offset` | `0` | Microns. Cadence starts from bottom. |
| `pitch` | OpenROAD: `2 * (width + spacing)` | OpenROAD only. |

OpenROAD-only `connect` is a list of two-layer arrays, such as
`[["M1", "M6"], ["M6", "M7"]]`, used to connect PDN layers. Omission produces
a warning when shapes are generated. OpenROAD's generated PDN supports one
power/ground pair; align `init` supply nets and `power_globals.nets`. Multiple
supply nets may receive global connections when no PDN shapes are requested.

Legacy flat keys such as `nets_order`, `horiz_ly`, `vert_ly`, `met_width`,
`net_spacing`, and `offset` at the top of the power section are not consumed
by the current ring/stripe generators. Use the nested schema above.

## route — signal routing

| Key | Cadence | OpenROAD |
| --- | --- | --- |
| `top_layer` | Sets design top routing layer; CLOCK attributes default to M7 if absent. | Supply together with `bot_layer` to set the signal-layer range. |
| `bot_layer` | Sets design bottom routing layer; CLOCK attributes default to M4 if absent. | Supply together with `top_layer`, or omit both. |
| `ant_dio_cell` | Sets antenna cell name if supplied. | Not consumed. |
| `iterations` | Not consumed; detailed end iteration is currently hardcoded to 10. | Set explicitly: passed to `detailed_route -droute_end_iter`; the current generator has no fallback. |

Cadence adds GND shielding for rules containing `CLOCK`, enables SI-related
attributes, and calls `route_design -global_detail`. Several router flags are
hardcoded rather than JSON options. OpenROAD assigns NDRs, calls `global_route`
and `detailed_route`, and writes guide/DRC outputs. It does not reproduce
Cadence clock shielding or SI repair.

## signoff — output and GDS assembly

Cadence consumes `gds_map_file` and `unit` for `write_stream`; supply both.
It writes netlist, GDS, and abstract LEF. Neither field has a usable fallback.
Cadence does not consume `def2stream`.

OpenROAD writes ODB, DEF, Verilog, and abstract LEF. Configure `def2stream` to
merge routed DEF with native cell GDS/OAS using KLayout; otherwise GDS export
is skipped. This is layout assembly, not the obsolete library-rotation method.

| `def2stream` key | Default / requirement |
| --- | --- |
| `tech_file` | KLayout `.lyt`; supply exactly one of this or `tech_lef`. |
| `tech_lef` | Alternative technology LEF; requires `layer_map`. |
| `layer_map` | KLayout LEF/DEF layer map. An Innovus stream-out map is not interchangeable. |
| `in_files` | Required directory string. The current generator resolves/enumerates it during synthesis, relative to the Python invocation directory; use an absolute path to avoid ambiguity. Must contain GDS/OAS files without whitespace in their paths. |
| `macro_lefs` | `["../inputs/cells.lef"]`; list or semicolon-separated string. List paths must be nonempty and contain no semicolons. |
| `seal_file` | Optional seal-ring layout. |
| `script` | Package `def2stream.py`. |
| `klayout` | `klayout`; executable name or path. |
| `def_units` | Defaults to the OpenROAD database's units-per-micron at runtime. Override must be a positive integer; it does not replace the DEF header. |

`in_def`, `out_file`, and `design_name` are generated automatically, not JSON
options. Other relative stream paths are passed to KLayout and resolve from
the tool run directory. Initialization LEF/Liberty and Cadence map paths also
resolve from the Tcl working directory, not the JSON file location.

The current OpenROAD wrapper logs a KLayout failure but still prints its GDS
completion message. Verify the output and `run/klayout_conversion.log` rather
than interpreting that message alone as success.

## Portable starter configuration

Replace paths/layers/site with values for your process. Empty power shapes
avoid prescribing a process-specific PDN. Define ANALOG because default nets
are assigned that rule. Add backend-specific signoff settings as needed.

```json
{
  "init": [
    {"tlef_path": "ABSOLUTE_PATH_TO_TECHNOLOGY_LEF"},
    {"pwr_nets": "VDD", "gnd_nets": "GND"},
    {"ndr": [{"name": "ANALOG", "width": {"M3": 0.1}, "spacing": {"M3": 0.1}}]}
  ],
  "pins": [
    {"site": "core", "place_type": "side"},
    {
      "N": {"met_layer": "M3", "offset_start": 5, "offset_end": 5},
      "S": {"met_layer": "M3", "offset_start": 5, "offset_end": 5},
      "E": {"met_layer": "M4", "offset_start": 5, "offset_end": 5},
      "W": {"met_layer": "M4", "offset_start": 5, "offset_end": 5}
    }
  ],
  "power": [{"power_globals": {"nets": ["VDD", "GND"], "type": "rings"}, "rings": []}],
  "route": [{"bot_layer": "M2", "top_layer": "M5", "iterations": 10}],
  "signoff": []
}
```

For Cadence replace `signoff` with, for example:

```json
{"signoff": [{"gds_map_file": "ABSOLUTE_PATH_TO_STREAM_MAP", "unit": 2000}]}
```

For OpenROAD GDS assembly:

```json
{"signoff": [{"def2stream": {
  "tech_lef": "ABSOLUTE_PATH_TO_TECHNOLOGY_LEF",
  "layer_map": "ABSOLUTE_PATH_TO_KLAYOUT_LAYER_MAP",
  "in_files": "ABSOLUTE_PATH_TO_NATIVE_CELL_GDS_DIRECTORY"
}}]}
```

Unknown keys are generally ignored by these generators, so spelling matters.
Only the keys documented above are read from JSON by the current implementation.
