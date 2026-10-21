# Cell library tools

| File | Purpose |
| --- | --- |
| json2python.py | Generate Python cell classes from library descriptions |
| update_generated_pin_interfaces.py | Update generated pin-interface definitions |
| cell_profiles.py | Load an optional adjacent hand-maintained profile provider |

Generated definitions and placement metadata have separate owners. The profile
loader registers attributes at runtime without rewriting generated files.
See [cell-library profile guide](../docs/CELL_LIBRARY_PROFILES.md).
