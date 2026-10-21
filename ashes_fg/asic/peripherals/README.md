# FG peripheral model and generation

| File | Responsibility |
| --- | --- |
| fg_peripherals.py | Discover FG channels, retain island plans, select decoders and manage sharing/planned extensions |
| fg_generation.py | Public generation options, shared stage wiring and compile handoff |
| peripheral_gaps.py | Discover intervening body columns/rows and resolve registered profiles |
| peripheral_bands.py | Build active switch/shifter spans and their local filler cells |
| mixed_generation.py | Coordinate automatic local bands around a placed abutting VMM body |

Technology-specific decoder algorithms stay in the shared algorithm library.
Physical composition stays in placement/peripheral_layout.py. Local fillers do
not implement routing bridges, island extension or body-signal sharing.

See [gap fillers and separate bridge/extension concepts](../docs/PERIPHERAL_GAP_FILLERS.md),
[generation options](../docs/FG_GENERATION_OPTIONS.md) and
[decoder gap profiles](../docs/DECODER_GAPS.md).

See [separate generated cells and hand-maintained profiles](../docs/CELL_LIBRARY_PROFILES.md)
for cells_16nm_profiles.py, explicit registration and automatic library loading.

Supplied placement profiles now name cell masters only. They require no signal
or supply annotations. Passive gap fillers rely on designer-verified abutment;
functional active-cell wiring remains in the algorithms. See
[simple profiles](../docs/CELL_LIBRARY_PROFILES.md#simple-placement-only-profiles).
