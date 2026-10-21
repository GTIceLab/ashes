# Decoder fillers over intervening body cells

ASHES discovers internal gaps between the selected FG spans when creating a
DecoderContext. `context.gaps` contains PeripheralGap records: logical coordinate,
before_output (the number of real selection outputs preceding the gap), source
instances and their library profiles. Leading/trailing margins are not gaps.
Detection uses placement and metadata, not S-block name matching.

The selected decoder algorithm owns how its bands traverse these regions.
`folded_radix4` inserts a filler column into every core/connector band for each
gap coordinate. Electrical level/group numbers and output ordering remain
unchanged. Gaps must fall between complete four-output leaf groups; a gap
splitting a leaf is rejected. Missing or conflicting profiles are errors, with
generation rolled back. Empty grid gaps also need an explicit physical cell;
the algorithm does not guess a suitable pitch or library master.

## Register another intervening cell

Define this metadata in a separate profiles provider, inside
register_profiles(cells), resolving OtherRouting = getattr(cells, 'OtherRouting'):

```python
OtherRouting.decoder_fillers = {
    'gate': {
        'folded_radix4': {
            'core': 'Other_FILL_GateDecode',
            'connector': 'Other_FILL_GateDecodeCONN',
        }
    }
}
```

`core` and `connector` are class names in the selected cell module. The classes
must have the library constructor interface and compatible heights for their
bands. Core and connector variants must have the same gap width. Width comes
from their actual physical footprints, rather than the ordinary decoder slot
pitch. These profiles name only core/connector filler masters. The physical
library and designer provide signal/supply continuity through abutment; ASHES
does not annotate or synthesize nets for passive gap filler pins. Functional
decoder address, enable and selection wiring remains in the decoder algorithm.

The separate 16nm profile provider registers regular profiles on Sblock_Routing and
Sblock_Filler, and narrow variants on Sblock_Filler_Start/End. Gate filler
classes share the decoder core/connector companion profiles, so outer edge/TAP
placement stays with the common physical-cell pass. Different topologies or
drain filler families can register their own role/topology entries.

## Using the selected decoder in a mixed peripheral algorithm

```python
# Inside the existing PeripheralContext callback:
gate = context.plan.gate
# Optionally set gate.decoder_placement to an AlgorithmGrid region.
result = gate.build_decoder()
# result.instances includes the discovered gap fillers.
```

Without an explicit region, ASHES reserves staging space beyond the placed
body for a single-island chain. The decoder layout callback returns local XY
boxes including variable-width fillers. A custom whole-peripheral layout must
incorporate these boxes, orient/anchor them, and place the surrounding stages.
The default path now composes supported local mixed-body switch/shifter
bands and selected decoder boxes automatically. Bridge/extension geometry and
body-signal bindings remain separate design responsibilities. See
[local bands versus bridges/extensions](PERIPHERAL_GAP_FILLERS.md).

The unused shared `decoders/cell_helpers.py` has been removed. Historical
standalone Decoders.py copies under run_syn were not changed. Active decoder
filler handling lives in decoders/folded_radix4/gaps.py; reusable gap discovery
lives in ASHES peripherals/peripheral_gaps.py.

Automatic placement-only gap filling creates no gap_connections entries.
Custom algorithms may still return explicit connections when their circuit needs
them; that is separate from the profile's cell-selection responsibility.

Profile rules belong in cells_16nm_profiles.py, not the generated cells_16nm.py.
See [registration and loader behavior](CELL_LIBRARY_PROFILES.md).
