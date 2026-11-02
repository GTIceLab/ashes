# Installed placement and circuit algorithms

Import through `ashes_fg.algorithms`; project folders do not need an `algorithms`
copy or a path entry pointing to the 16nm project.

| Module | Responsibility |
| --- | --- |
| `common` | Native pin lookup and electrical connection helpers |
| `system_build` | Circuit registries, matrix/support creation and external ports |
| `decoders.folded_radix4` | Existing 16nm gate/drain decoder builders |
| `decoders.bridged_radix4` | Legacy bridge/spacing decoder topology and native interfaces |
| `sblock.switch_matrix` | Existing 16nm switch-matrix S-block |
| `sblock.sectioned` | Four-lane sectioned staircase from `FPAA_Synthesis/cab1.py` |
| `cab` | Parameter parsing and native device interface discovery |
| `cab.matrix_rows` | Profile-selected boundary rows, nominal/read/program capacities |
| `cab.abut_native` | Native abutting CAB draft selected by library profile |

Project-independent construction is exposed by `ashes_fg.generators.cab_nn`.
The generated cell library and its adjacent `<stem>_profiles.py` remain local to
the project. Profiles select algorithms, native role bindings and boundary-cell
recipes; the top-level generator has no process-specific branches.

```python
from ashes_fg.algorithms.decoders.folded_radix4 import GateDecoder, DrainDecoder
from ashes_fg.generators.cab_nn import build

# Explicit callbacks remain supported by the shared peripheral API.
# The default callback now resolves inside this installed package.
tile = build('/path/to/Tools/run_syn/CAB_NN_global')
```

For 350nm use `build(..., strict=False)` only for model inspection. Strict mode
rejects unresolved electrical contracts before a design reaches synthesis.
The bridged algorithm surfaces auxiliary pins rather than inferring their
direction/meaning from label spelling. See `docs/cab-generators.md` in ASHES
and the project runner README for validation status and commands.
