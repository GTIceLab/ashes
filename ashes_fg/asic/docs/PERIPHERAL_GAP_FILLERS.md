# Peripheral gap fillers, bridges and extensions

These mechanisms solve different problems and must be configured separately.

| Mechanism | Purpose | Does not imply |
| --- | --- | --- |
| Local peripheral gap filling | Continue switch, level-shifter and decoder bands across intervening non-FG columns/rows | New selection outputs, bridge insertion, extension or body-signal sharing |
| Routing bridge | Adapt or carry specified programming lines where direct abutment is unsuitable | More switches, address sharing or run/program isolation |
| Peripheral extension and connection ties | Serve another region/island and explicitly map its additional switches/lines/signals | A physical bridge or safe abutment supplied by gap fillers |

One design may need all three. A filler may contain real pass-through wiring,
but its registration is not a bridge contract or authorization to short body
signals. `share_fg_bits` shares digital address inputs with separate enables;
it does not extend a switch array or establish an FG programming bridge.

## Automatic local bands

For a placed body containing VMM spans and registered intervening columns:

```text
decoder cells  | decoder fillers       | decoder cells
level shifters | level-shifter fillers | level shifters
gate switches | switch fillers        | gate switches
VMM columns   | non-FG columns        | VMM columns
```

ASHES discovers spans, channels and internal gaps. It places selected active
switch/shifter matrices over FG spans, and library-defined filler cells over
the gaps. The selected decoder algorithm handles fillers across its own bands.
Fillers consume physical width, not programming channels or address bits.

```python
# left_vmm and right_vmm are already placed; routing columns lie between them.
fg = island.generate_fg_peripherals(
    cells=cells_16nm,
    parents=(left_vmm, right_vmm),
    roles=('gate',),
    gate_switch='SWC_Gate',
    gate_level_shifter='LevelShift_2x_Gate',
)
```

No my_sblock_peripherals callback is needed for this supported local-band case.
`parents=` selects the FG targets, not the filler sources: ASHES still inspects
intervening body instances. It is useful when the body also contains S-block
FG cores or routing drain pins that require separate interface/bridge treatment.

`roles` defaults to ('gate', 'drain'). It limits automatic generation to the
listed roles; omitted roles remain planned, with their body connections left
designer-owned. Disabling a stage skips both its new active devices and its
fillers. Existing body-created devices are retained. `Sblock_gen` remains a
body builder, not a peripheral algorithm, and its FG core interfaces are not
automatically treated as IndirectVMM_4x2 interfaces.

The current automatic geometry supports the swapped 16nm convention and VMM
programming interfaces. It handles a natural abutting body grid with consistent
projected row/column pitch. Missing profiles, conflicting projections, incompatible
widths/heights or unsupported interfaces raise errors. Generation failures restore
the circuit. Physical footprint conflicts discovered during compilation fail
placement rather than stretch matrices or silently move pins.

A role requiring a bridge is explicitly rejected by this local generator,
even when a class name for a bridge is provided: bridge placement and lane mapping
must be implemented separately. For example, gate bands may cross a registered
gap while drain lines crossing between the VMM regions still require a bridge.
Generate roles=('gate',) and handle the drain topology explicitly in that case.
The assumed bridge masters remain FG_RoutingBridge_Gate/Drain; this change does
not create physical bridge cells or implement extension placement.

## Registering another intervening cell family

Keep these rules in the hand-maintained profiles provider and attach them
to the selected generated classes inside register_profiles(cells). For example,
resolve OtherRouting = getattr(cells, 'OtherRouting') before these assignments:

```python
OtherRouting.peripheral_fillers = {
    'gate': {
        'switch': {
            'cell': 'Other_FILL_GateSwc',
        },
        'level_shifter': {
            'cell': 'Other_FILL_GateLVLShift',
        },
    },
}
```

Stage keys are `switch` and `level_shifter`; role keys are `gate` and `drain`.
`cell` is a class name in the selected module. Profiles refer to actual physical
cells; ASHES does not synthesize missing masters. Register the appropriate profile
on every projected source class, including boundary variants. Sources aligned
at the same coordinate must agree on the profile. Unknown or empty internal
gaps cannot silently inherit an ordinary VMM filler.

The separate 16nm profile provider registers Sblock_Routing/Sblock_Filler with regular
fillers and Sblock_Filler_Start/End with narrow variants. Its existing gate-stage
body fillers receive matching source metadata too. Actual GDS dimensions must
match the body's gap width and the selected active stage's thickness. A different
switch/shifter master may require different profiles and native pin compatibility.

Decoder metadata is separate because the selected topology has multiple kinds
of bands:

```python
OtherRouting.decoder_fillers = {
    'gate': {'folded_radix4': {
        'core': 'Other_FILL_GateDecode',
        'connector': 'Other_FILL_GateDecodeCONN',
    }}
}
```

See [decoder gap details](DECODER_GAPS.md). Folded radix-4 requires gaps between
complete four-output leaf groups. Switch/shifter bands themselves do not impose
that grouping; disabling the decoder removes that topology-specific constraint.

## Electrical ownership

Profiles select cells only. The designer/library is responsible for passive
signal and supply continuity through correctly designed abutment. ASHES does
not synthesize nets, mode-control bindings or address connections for gap fillers.
Geometric checks do not verify metal-layer/pin continuity inside the masters.

Functional decoder and active switch/shifter wiring remains in the algorithms.
VG_RUN/VS lanes stay distinct across active spans. Their supplies and circuit
controls remain normal design connections, outside the placement profiles.

fg.bands[(role, stage)] exposes the active matrices and placed fillers. Mixed
chain.switches/level_shifters are tuples of active matrices, or None when disabled;
regular single-VMM generation retains its existing single-matrix attributes.
gap_connections remains available to custom algorithms, but these placement-only
profiles create no entries and require no filler bus binding in the design.

No bridge, extension, cross-island connection or body-signal tie is inferred.

## Placement and advanced layouts

Stage construction is in peripherals/peripheral_bands.py. Generic discovery is
in peripherals/peripheral_gaps.py. mixed_generation.py coordinates local bands
and shared chain wiring. placement/peripheral_layout.py composes the body, bands
and selected decoder boxes using actual footprints, then reserves shared edge/TAP
strips. The shared physical pass remains responsible for termination selection,
net transfer and contact validation; no algorithm constructs edge/TAP cells.

A custom algorithm= callback is still available for arbitrary body interfaces,
bridge routing, extensions or layouts outside the abutting-grid contract. It
receives normalized options, including roles, and must implement its requested
topology explicitly. This hook does not provide an extension/bridge implementation.

Verification includes all eight stage combinations for mixed gate bands,
regular/narrow S-block variants, an independently named source family, analog
lane isolation, passive fillers without synthesized nets, rollback, missing-profile/bridge rejection,
and placement-only GDS/DEF builds. Existing regular VMM checks remain applicable.
Routing, DRC, LVS and electrical signoff have not been performed.

Profile rules belong in cells_16nm_profiles.py, not the generated cells_16nm.py.
See [registration and loader behavior](CELL_LIBRARY_PROFILES.md).
