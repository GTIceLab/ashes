"""Python FG peripheral planning and decoder-builder interfaces.

No library definitions are copied here. Plans retain live island/cell references.
Physical bridge geometry is supplied by the technology library, not fabricated.
"""
from dataclasses import dataclass, field
from copy import copy, deepcopy
import importlib
import inspect
from types import SimpleNamespace
from ..placement.algorithm_grid import AlgorithmGrid
from .peripheral_gaps import discover_gaps
from ..library.cell_profiles import load_cell_library


DEFAULTS = {
    'gate': ('SWC_Gate', 'LevelShift_2x_Gate', 'GateDecoder', 'FG_RoutingBridge_Gate'),
    'drain': ('SWC_Drain', 'LevelShift_4x_Drain', 'DrainDecoder', 'FG_RoutingBridge_Drain'),
}
COORDINATES = ('xy', 'columns_y_rows_minus_x')


@dataclass(frozen=True)
class Span:
    start: int
    stop: int


@dataclass
class Layout:
    """Logical grid coordinates, independent of decoder output numbering."""
    axis: str
    spans: tuple
    filler_coordinates: tuple
    edge_coordinates: tuple
    extent: int


@dataclass
class Channel:
    index: int
    coordinate: int
    lane: int
    targets: list = field(default_factory=list)
    bridge_required: bool = False


@dataclass
class DecoderResult:
    """A Python algorithm must expose electrical outputs as well as controls.

    outputs is an ordered list of Pins (or one-pin Ports); output_complements is
    required for gate shifters needing true/complementary selections.
    """
    bits: object
    enable: object
    outputs: list
    instances: list
    output_complements: list = field(default_factory=list)
    supplies: dict = field(default_factory=dict)
    abutments: list = field(default_factory=list)
    layout: object = None
    gap_connections: dict = field(default_factory=dict)


@dataclass(frozen=True)
class DecoderPlacementContext:
    """Canonical local XY footprints supplied to the chosen algorithm.

    entries maps indices to opaque algorithm-owned descriptors. Return local
    XY boxes for exactly those entries. ASHES orients and anchors the block.
    anchor is a local Y origin; slot_pitch is the canonical X slot width.
    """
    role: str
    island: object
    cells: dict
    entries: dict
    anchor: float
    core_size: tuple
    core_shape: tuple
    slot_pitch: float = None


@dataclass
class DecoderContext:
    circuit: object
    island: object
    cells: object
    role: str
    output_count: int
    layout: Layout
    process_coordinates: str
    channels: tuple
    layouts: tuple
    placement: object = None
    gaps: tuple = ()


@dataclass
class Chain:
    role: str
    owner: object
    members: list
    switch: object
    level_shifter: object
    decoder: object
    bridge: object
    channels: list
    layouts: list
    process_coordinates: str
    cells: object
    decoder_result: object = None
    external_inputs: dict = field(default_factory=dict)
    decoder_placement: object = None

    def __deepcopy__(self, memo):
        # A library module is shared immutable configuration, not circuit state.
        result = type(self).__new__(type(self))
        memo[id(self)] = result
        for name, value in self.__dict__.items():
            setattr(result, name, value if name == 'cells' else deepcopy(value, memo))
        return result

    @property
    def inputs(self):
        if self.decoder is False:
            raise ValueError('Decoder placement is disabled; use external_inputs selection signals')
        if self.decoder_result is None:
            raise ValueError('Build the decoder before accessing its input ports')
        return SimpleNamespace(address=self.decoder_result.bits,
                               bits=self.decoder_result.bits,
                               enable=self.decoder_result.enable)

    @property
    def output_count(self):
        return len(self.channels)

    @property
    def address_width(self):
        return (self.output_count - 1).bit_length() if self.output_count > 1 else 0

    @property
    def missing_cells(self):
        if any(c.bridge_required for c in self.channels) and not callable(self.bridge):
            return [self.bridge]
        return []

    def decoder_context(self):
        placement = self.decoder_placement
        core = getattr(self.owner, '_fg_core', None)
        if placement is None and core is not None:
            loc = self.owner.getLocation(core)
            row, col = int(loc[0][0]), int(loc[1][0])
            # Reserve a staging region for each chain. Algorithms always use
            # local X=slot, Y=band; only this manager knows its island axes.
            if self.role == 'gate':
                placement = AlgorithmGrid(self.owner, (row + core.dim[0] + 2, col))
            else:
                placement = AlgorithmGrid(self.owner, (row, col + core.dim[1] + 2),
                                          (1, 0), (0, 1))
        if placement is None and self.members == [self.owner]:
            # Mixed bodies do not have one _fg_core. Reserve a region beyond
            # the complete placed body; custom generators may override it.
            placed = [(cell, self.owner.getLocation(cell)) for cell in self.owner.instances
                      if not getattr(cell, 'fg_peripheral', False)]
            placed = [(cell, loc) for cell, loc in placed if len(loc[0]) and len(loc[1])]
            if placed:
                row = min(int(loc[0][0]) for cell, loc in placed)
                col = min(int(loc[1][0]) for cell, loc in placed)
                end_row = max(int(loc[0][0]) + cell.dim[0] for cell, loc in placed)
                end_col = max(int(loc[1][0]) + cell.dim[1] for cell, loc in placed)
                placement = (AlgorithmGrid(self.owner, (end_row + 2, col))
                             if self.role == 'gate' else
                             AlgorithmGrid(self.owner, (row, end_col + 2), (1, 0), (0, 1)))
        return DecoderContext(self.owner.circuit, self.owner, self.cells, self.role,
                              self.output_count, self.layouts[0],
                              self.process_coordinates, tuple(self.channels),
                              tuple(self.layouts), placement,
                              discover_gaps(self.owner, self.role,
                                                    self.layouts[0], self.channels))

    def build_decoder(self):
        """Run a normalized Python builder; never call the GDS decoder generator.

        Builders receive the real placement owner and all member layouts through
        the chain channels; physical mutation is their responsibility. They must
        validate placement before adding cells. This method is intentionally
        separate from planning so missing bridge cells can be reported first.
        """
        if self.decoder_result is not None:
            return self.decoder_result
        for member in self.members:
            if member.fg.signature != _signature(member):
                raise ValueError('Island layout changed after FG planning; rebuild the plan')
        if not callable(self.decoder):
            raise ValueError(f'Provide the shared Python {self.decoder} builder; '
                             'legacy CAB builders need adapt_decoder(...).')
        snapshot = _snapshot(self.owner.circuit)
        try:
            return self._build_decoder()
        except Exception:
            for obj, state in snapshot:
                obj.__dict__.clear()
                obj.__dict__.update(state)
            raise

    def _build_decoder(self):
        result = self.decoder(self.decoder_context())
        if not isinstance(result, DecoderResult):
            raise TypeError('Decoder builder must return DecoderResult')
        if result.bits is None or result.enable is None:
            raise ValueError('Decoder builder must expose bits and enable')
        if len(result.outputs) != self.output_count:
            raise ValueError('Decoder output count does not match requested channels')
        if self.role == 'gate' and len(result.output_complements) != self.output_count:
            raise ValueError('Gate decoder must expose complementary outputs')
        if len(result.bits) != self.address_width:
            raise ValueError('Decoder address width does not match requested outputs')
        if any(cell not in self.owner.instances for cell in result.instances):
            raise ValueError('Decoder instances must belong to the placement owner')
        for cell in result.instances:
            cell.fg_peripheral = True
        for member in self.members:
            member.fg.signature = _signature(member)
        self.decoder_result = result
        return result


@dataclass
class Peripherals:
    island: object
    gate: object = None
    drain: object = None
    configuration: object = None
    signature: object = None

    @property
    def missing_cells(self):
        return sorted({name for chain in (self.gate, self.drain) if chain
                       for name in chain.missing_cells})

    @property
    def missing_algorithms(self):
        return sorted({chain.decoder for chain in (self.gate, self.drain)
                       if chain is not None and chain.decoder is not False and not callable(chain.decoder)})


def _library(island, cells):
    if isinstance(cells, str):
        return load_cell_library(cells)
    if cells is not None:
        return load_cell_library(cells)
    candidates = []
    for parent in island.instances:
        module = inspect.getmodule(type(parent))
        if module is not None and hasattr(module, 'SWC_Gate') and module not in candidates:
            candidates.append(module)
    if len(candidates) != 1:
        raise ValueError('Pass cells=<shared cell module> when it cannot be inferred uniquely')
    return load_cell_library(candidates[0])


def _snapshot(circuit):
    """Preserve existing model objects and nets if a decoder builder fails.

    This restores the circuit model, not arbitrary external files or objects a
    custom algorithm mutates. Algorithm callbacks should only build model cells.
    """
    objects = [circuit, *circuit.Islands, *circuit.Instances, *circuit.Nets]
    for island in circuit.Islands:
        plan = getattr(island, 'fg', None)
        if plan is not None:
            objects.append(plan)
            for chain in (plan.gate, plan.drain):
                if chain is not None:
                    objects.extend((chain, *chain.channels, *chain.layouts))
        generated = getattr(island, 'fg_generated', None)
        if generated is not None:
            objects.append(generated)
    for cell in circuit.Instances:
        objects.extend(cell.ports)
        objects.extend(cell.pins)
    for net in circuit.Nets:
        for pin in net.pins:
            objects.extend((pin, pin.port))
    snapshot, seen = [], set()
    for obj in objects:
        if obj is None or id(obj) in seen:
            continue
        seen.add(id(obj))
        state = {key: copy(value) if isinstance(value, (list, dict, set))
                 or hasattr(value, 'shape') else value
                 for key, value in obj.__dict__.items()}
        snapshot.append((obj, state))
    return snapshot


def _resolve(cells, selected, default):
    value = default if selected is None or selected is True else selected
    return getattr(cells, value, value) if isinstance(value, str) else value


def _signature(island):
    records = []
    for cell in island.instances:
        if getattr(cell, 'fg_peripheral', False):
            continue
        loc = island.getLocation(cell)
        placed = tuple((int(a[0]) if len(a) else None) for a in loc)
        records.append((id(cell), cell.name, tuple(cell.dim), placed,
                        tuple((p.native_name, len(p)) for p in cell.ports)))
    return tuple(records)


def _parents(island, selected):
    if selected is not None:
        parents = list(selected)
        if any(p not in island.instances for p in parents):
            raise ValueError('Every FG parent must belong to the selected island')
        return parents
    return [c for c in island.instances
            if not c.isDecoder() and not getattr(c, 'fg_peripheral', False)
            and not c.name.startswith(('SWC', 'LevelShift', 'GateDecode', 'DrainDecode',
                                       'FG_RoutingBridge'))
            and not c.name.endswith(('_EdgeL', '_EdgeR', '_TAP'))
            and 'FILL' not in c.name.upper()
            and any(p.native_name in ('Vg_w', 'Vg_e', 'Vg_n', 'Vg_s')
                    or p.native_name.startswith(('Vd_P_', 'Vd_R_', 'VD_P_', 'VD_R_'))
                    for p in c.ports)]


def _ports(parent, role):
    prefixes = ('Vg_',) if role == 'gate' else ('Vd_P_', 'Vd_R_', 'VD_P_', 'VD_R_')
    return [p for p in parent.ports if p.native_name.startswith(prefixes)]


def _channel_axis(parents, role):
    axes = {0 if port.location in ('W', 'E') else 1
            for parent in parents for port in _ports(parent, role)}
    if len(axes) != 1:
        raise ValueError(f'{role}: programming ports need one consistent native/logical axis')
    return axes.pop()


def _layout(island, parents, role):
    axis = _channel_axis(parents, role)
    extent = island.getNumCols() if axis else island.getNumRows()
    occupied = set()
    for parent in parents:
        if not _ports(parent, role):
            continue
        loc = island.getLocation(parent)
        if not len(loc[axis]):
            raise ValueError(f'FG parent {parent.name} is not placed')
        start = int(loc[axis][0])
        occupied.update(range(start, start + parent.dim[axis]))
    spans = []
    for coordinate in sorted(occupied):
        if spans and spans[-1].stop == coordinate:
            spans[-1] = Span(spans[-1].start, coordinate + 1)
        else:
            spans.append(Span(coordinate, coordinate + 1))
    edges = tuple(sorted({edge for span in spans for edge in (span.start, span.stop)}))
    return Layout('columns' if axis else 'rows', tuple(spans),
                  tuple(i for i in range(extent) if i not in occupied), edges, extent)


def _channels(island, parents, role):
    """Aligned VMM columns/rows are continuous lines; other cells remain distinct.

    Alias opposite-edge copies within a parent only. Different non-VMM parents
    are never shorted just because their names or coordinates match.
    """
    axis = _channel_axis(parents, role)
    channels = {}
    intervals = {}
    for parent in parents:
        ports = _ports(parent, role)
        if not ports:
            continue
        # Bias-only cells require explicit selection through parents=, but still
        # retain their native pin names and receive bridge treatment.
        loc = island.getLocation(parent)
        if not len(loc[axis]):
            raise ValueError(f'FG parent {parent.name} is not placed')
        start = int(loc[axis][0])
        length = parent.dim[axis]
        widths = {len(p) for p in ports}
        if len(widths) != 1 or next(iter(widths)) % length:
            raise ValueError(f'{parent.name}: inconsistent {role} line widths; '
                             'use cell definitions generated for the logical axes')
        lanes = next(iter(widths)) // length
        direct = (parent.name == 'IndirectVMM_4x2' or
                  getattr(type(parent), 'fg_regular_interface', None) == 'vmm')
        for offset in range(length):
            coordinate = start + offset
            for lane in range(lanes):
                key = (coordinate, lane, None if direct else id(parent))
                channel = channels.setdefault(key, Channel(-1, coordinate, lane,
                                                          bridge_required=not direct))
                cross_start = int(loc[1 - axis][0])
                intervals.setdefault(key, []).append((cross_start,
                                                       cross_start + parent.dim[1 - axis]))
                for port in ports:
                    channel.targets.append(port.pins[offset * lanes + lane])
    for key, sections in intervals.items():
        end = None
        for start, stop in sorted(sections):
            if end is not None and start > end:
                channels[key].bridge_required = True
            end = max(end or stop, stop)
    result = sorted(channels.values(), key=lambda c: (c.coordinate, c.lane))
    for index, channel in enumerate(result):
        channel.index = index
    return result


def prepare(island, *, cells=None, gate_switch=None, drain_switch=None,
            gate_level_shifter=None, drain_level_shifter=None,
            gate_decoder=None, drain_decoder=None, gate_bridge=None, drain_bridge=None,
            parents=None, process_coordinates='xy', extend_from=None,
            extend_roles=('drain',)):
    """Discover and attach an FG plan without mutating cells, nets, or placement.

    Decoder generation is explicit via chain.build_decoder(). Standard-cell
    placement requires algorithms implementing the full DecoderResult interface.
    """
    if process_coordinates not in COORDINATES:
        raise ValueError(f'process_coordinates must be one of {COORDINATES}')
    cells = _library(island, cells)
    parents = _parents(island, parents)
    # Only canonical Vg_<side> counts as automatic programming discovery. Other
    # Vg_ names are accepted when the designer explicitly selects the parent.
    extend_roles = tuple(extend_roles)
    if len(set(extend_roles)) != len(extend_roles) or any(r not in DEFAULTS for r in extend_roles):
        raise ValueError('extend_roles must contain distinct gate/drain roles')
    options = ((gate_switch, gate_level_shifter, gate_decoder, gate_bridge),
               (drain_switch, drain_level_shifter, drain_decoder, drain_bridge))
    configuration = (id(cells), options, tuple(id(p) for p in parents),
                     process_coordinates, id(extend_from), extend_roles)
    signature = _signature(island)
    previous = getattr(island, 'fg', None)
    if previous is not None:
        if previous.configuration != configuration or previous.signature != signature:
            raise ValueError('FG configuration/layout changed; rebuild from an unprepared circuit')
        return previous
    if extend_from is not None:
        if extend_from is island or extend_from.circuit is not island.circuit:
            raise ValueError('extend_from must be another island in the same circuit')
        if getattr(extend_from, 'fg', None) is None:
            raise ValueError('Prepare the source island before extending it')
        if extend_from.fg.signature != _signature(extend_from):
            raise ValueError('Source island layout changed after FG planning')
    work = Peripherals(island, configuration=configuration, signature=signature)
    for role, chosen in zip(('gate', 'drain'), options):
        channels = _channels(island, parents, role)
        if not channels:
            continue
        resolved = tuple(_resolve(cells, value, default)
                         for value, default in zip(chosen, DEFAULTS[role]))
        for cls in resolved[:2]:
            if cls is not False and not callable(cls):
                raise ValueError(f'Missing standard cell {cls}')
        chain = Chain(role, island, [island], *resolved, channels,
                      [_layout(island, parents, role)], process_coordinates, cells)
        if extend_from is not None and role in extend_roles:
            source = getattr(extend_from.fg, role)
            if source is None:
                raise ValueError(f'Source island has no {role} chain to extend')
            if source.decoder_result is not None:
                raise ValueError('Extend the peripheral group before building its decoder')
            if source.process_coordinates != process_coordinates:
                raise ValueError('Extended islands must use the same coordinate convention')
            if source.cells is not cells or any(value is not None and actual != expected
                                                for value, actual, expected in
                                                zip(chosen, resolved, (source.switch,
                                                    source.level_shifter, source.decoder,
                                                    source.bridge))):
                raise ValueError('Extended chain component choices must match its source')
            # Appended drains are additional outputs, not corresponding-lane ties.
            # The gate topology is deferred to its algorithm; retain local gate
            # switching requirements without duplicating the shared decoder.
            if any(c.bridge_required for c in channels) or role == 'drain':
                for c in channels:
                    c.bridge_required = True
            chain.owner = source.owner
        setattr(work, role, chain)
    # Commit only after every role validates. Append to shared groups atomically.
    if extend_from is not None:
        for role in ('gate', 'drain'):
            if role not in extend_roles:
                continue
            local = getattr(work, role)
            if local is None:
                continue
            source = getattr(extend_from.fg, role)
            offset = source.output_count
            for index, channel in enumerate(local.channels, offset):
                channel.index = index
            source.channels.extend(local.channels)
            source.layouts.extend(local.layouts)
            source.members.append(island)
            setattr(work, role, source)
    island.fg = work
    return work


def share_bits(first, second, role='both'):
    """Tie address inputs, preserving each decoder's independent enable net."""
    roles = ('gate', 'drain') if role == 'both' else (role,)
    if any(r not in DEFAULTS for r in roles):
        raise ValueError('role must be gate, drain, or both')
    pairs = []
    for r in roles:
        a, b = getattr(first.fg, r), getattr(second.fg, r)
        if a is None or b is None or a.decoder_result is None or b.decoder_result is None:
            raise ValueError(f'Build both {r} decoders before sharing bits')
        if a.owner.circuit is not b.owner.circuit:
            raise ValueError('Shared bits must belong to the same circuit')
        if a is b:
            raise ValueError('These islands already share a decoder; independent enables '
                             'require separate decoding/selection branches')
        if len(a.decoder_result.bits) != len(b.decoder_result.bits):
            raise ValueError('Different address widths require an explicit bit slice mapping')
        pairs.append((a.decoder_result.bits, b.decoder_result.bits))
    for a, b in pairs:
        if a is not b:
            a.connectPort(b)


def adapt_decoder(builder, *, role, output_selector, placement=None):
    """Adapt a legacy CAB builder without guessing its output/contact topology.

    placement(context) returns keyword arguments including filler/edge positions
    supported by that algorithm. output_selector(context, instances, controls)
    returns (true_outputs, complementary_outputs). All internal connections must
    be established by the builder/selector; adjacency alone is not a net.
    """
    if role not in DEFAULTS:
        raise ValueError('role must be gate or drain')
    def algorithm(context):
        if context.role != role:
            raise ValueError('Decoder adapter role mismatch')
        before = set(map(id, context.island.instances))
        count_arg = 'numCols' if role == 'gate' else 'numRows'
        kwargs = dict(placement(context) if placement else {})
        kwargs[count_arg] = context.output_count
        controls = builder(context.circuit, context.island, **kwargs)
        instances = [c for c in context.island.instances if id(c) not in before]
        outputs, complements = output_selector(context, instances, controls)
        return DecoderResult(controls['Bits'], controls['Enable'], list(outputs),
                             instances, list(complements),
                             {k: controls[k] for k in ('VDD', 'GND') if k in controls})
    return algorithm
