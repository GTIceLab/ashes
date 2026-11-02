## Physical pin extraction diagnostics

External-PD builds write `pd/pin_extraction_diagnostics.json` before checking
connected conventional-Verilog ports against extracted physical pins.
Unmatched selected labels produce console warnings with cell, pin, coordinates
(native database units), layer, selected datatype, reason and same-layer
rectangle count. Reasons distinguish labels on rectangle edges, outside
rectangles, and layers without selected pin rectangles.

A missing connected port stops the build before placement/output conversion.
The error names the instance, master, port and report path. Empty connections
do not fail. Pinless cells remain supported when no ports connect.

No technology-specific names, pin aliases or geometry exceptions were added.
Matching behavior is unchanged: strict interior tests and the existing selected
pin datatype still apply. Labels rejected by the existing layer filter are not
listed, although connected missing ports still fail. This report cannot establish
whether a differently typed rectangle exists in the source layout.

Preflight checks scalar port or bus-base existence against the same pin set
consumed by LEF export. It supports ASHES-generated named-port Verilog, not
arbitrary Verilog. Bus-width validation and preserving unused bus positions
remain separate pending fixes.

Rerun synthesis and inspect the report before launching Innovus. Verification
used synthetic data and model checks only: all 70 unit tests passed, and the
16nm circuit graph remained identical. No GDS or technology LEF was inspected.


Physical synthesis writes detailed unmatched-pin warnings to design/pd/pin_extraction.log, with only the log path printed to the terminal. The JSON diagnostic report is retained, and fatal preflight errors still stop the build. This supersedes earlier references to unmatched-pin console warnings. Logging is per build, without modifying root/global logging handlers.
