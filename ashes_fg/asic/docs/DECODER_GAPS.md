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

Define metadata on its cell class in the selected cell library:

```python
OtherRouting.decoder_fillers = {
    'gate': {
        'folded_radix4': {
            'core': 'Other_FILL_GateDecode',
            'connector': 'Other_FILL_GateDecodeCONN',
            'pass_through': ('E',),
            'address_family': 'B',
            'supply_aliases': {'VDD': 'VDD_CORE'},
        }
    }
}
```

`core` and `connector` are class names in the selected cell module. The classes
must have the library constructor interface and compatible heights for their
bands. Core and connector variants must have the same gap width. Width comes
from their actual physical footprints, rather than the ordinary decoder slot
pitch. Supply aliases bind the declared supply families. `address_family`
identifies connector address pins; unused high bits connect to GND.

`pass_through` names native pin families. Opposite sides of each family join
the same bus within a filler. Different bands receive independent buses,
exposed by `DecoderResult.gap_connections[(coordinate, band, family)]`.
The mixed-body peripheral algorithm/designer must connect these to the intended
body signals. ASHES does not assume that S-block east/west signals or separate
bands should be shorted. This replaces the old helper's Sblock_E return value
with explicitly identified connection points.

The selected 16nm library registers regular profiles on Sblock_Routing and
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
# Bind result.gap_connections to intended body signals here.
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

Automatic generation aggregates decoder pass-through buses into fg.gap_connections
under (role, 'decoder', coordinate, band, family). This does not tie them to
switch/shifter filler buses or body signals.
