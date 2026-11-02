"""Legacy bridged 2-to-4 topology, with explicit native electrical outputs.

The physical cell pattern follows verilog_to_gds's decoder tree. Auxiliary
native pins remain visible in `unassigned`; no complementary input driver or
passive helper connectivity is invented from pin spelling.
"""
import logging
from dataclasses import dataclass, field

from ashes_fg.asic.model.asic_compile import Bus, Wire
from ashes_fg.asic.peripherals.fg_peripherals import DecoderResult
from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid
from ashes_fg.algorithms.common import native_port, connect, pass_through
from ashes_fg.algorithms.decoders.common import address_width


@dataclass
class BridgedResult(DecoderResult):
    run_outputs: list = field(default_factory=list)
    unassigned: list = field(default_factory=list)
    run_inputs: list = field(default_factory=list)
    internal_auxiliary: list = field(default_factory=list)
    internal_pin_ids: set = field(default_factory=set)


def unresolved_pins(result):
    """Recheck candidates after the caller has finished connecting the decoder."""
    internal = getattr(result, 'internal_pin_ids', set())
    return [(cell, port, tuple(i for i, pin in enumerate(port.pins)
                              if len(pin.net.pins) == 1 and id(pin) not in internal))
            for cell, port in result.unassigned
            if any(len(pin.net.pins) == 1 and id(pin) not in internal for pin in port.pins)]



def validate_auxiliary_contract(contract, known):
    """Only explicitly optional internal annotations may be absent."""
    required = set(contract.get('internal_ports', ())) | set(contract.get('leaf_ports', {}))
    if required - known:
        raise ValueError(f'Decoder auxiliary contract references missing ports: {sorted(required - known)}')
    optional = set(contract.get('optional_internal_ports', ()))
    if optional - known:
        logging.getLogger(__name__).warning(
            'Optional decoder internal ports absent from cell definitions: %s; no pins or connections created',
            sorted(optional - known))
    return set(contract.get('internal_ports', ())) | (optional & known)


def pattern(output_count):
    """Return (row, column, master suffix, level, group) in vertical orientation."""
    if type(output_count) is not int or output_count < 1:
        raise ValueError('Decoder output count must be a positive integer')
    levels = max(1, (address_width(output_count) + 1) // 2)
    rows = (output_count + 3) // 4
    columns = 2 * levels - 1
    result = []
    for row in range(rows):
        for column in range(columns):
            level = (columns - column - 1) // 2
            stride = 4 ** level
            if column % 2 == 0:
                suffix = '' if row % stride == 0 else '_spacing'
                result.append((row, column, suffix, level if not suffix else None, row // stride))
            else:
                suffix = ('_' + 'ABCD'[(row // stride) % 4] + '_bridge'
                          if row % stride == 0 else '_bridge_spacing')
                result.append((row, column, suffix, None, row // stride))
    return tuple(result)


def build(circuit, island, count, *, cells, master, role, origin=(0, 0), auxiliary_contract=None,
          row_gaps=None, active_outputs=None, family=None, interface=None):
    if role not in ('gate', 'drain'):
        raise ValueError('Decoder role must be gate or drain')
    if not family or not interface:
        raise ValueError('Bridged decoder requires explicit cell-family and pin-interface contracts')
    if family.get('') != master:
        raise ValueError('Decoder family core does not match the selected master')
    grid = AlgorithmGrid.for_process(island, 'xy', origin=origin)
    bits, enable = Bus(circuit, size=address_width(count)), Wire(circuit)
    supplies = {name: Wire(circuit) for name in interface['supplies']}
    ground = supplies['GND']
    instances, nodes, unassigned = [], {}, []
    records = pattern(count)
    gaps = dict(row_gaps or {})
    if any(type(row) is not int or row < 0 or type(size) is not int or size < 0
           for row, size in gaps.items()):
        raise ValueError('Decoder row gaps must use nonnegative integer rows and sizes')
    shifted = [(row + sum(size for start, size in gaps.items() if start <= row),
                col, suffix, level, group) for row, col, suffix, level, group in records]
    for start, size in gaps.items():
        physical = start + sum(n for r, n in gaps.items() if r < start)
        for row in range(physical, physical + size):
            for col in range(max(r[1] for r in records) + 1):
                shifted.append((row, col, '_spacing' if col % 2 == 0 else '_bridge_spacing', None, 0))
    for row, col, suffix, level, group in shifted:
        cell = getattr(cells, family[suffix])(circuit, island)
        # Legacy horizontal placement transposes the vertical cell array.
        grid.place(cell, (row, col) if role == 'gate' else (col, row))
        cell.markAbut()
        instances.append(cell)
        analog = (auxiliary_contract or {}).get('analog_inputs')
        run_output = interface.get('run_outputs')
        if analog and run_output:
            names = {port.native_name for port in cell.ports}
            if analog in names and run_output in names:
                pass_through(circuit, cell, analog, run_output)
        if level is not None:
            nodes[level, group] = cell
        for port in cell.ports:
            for name, pins in interface['supplies'].items():
                if port.native_name in pins:
                    for pin in port.pins:
                        connect(pin, supplies[name])
    top = max(level for level, group in nodes)
    for (level, group), cell in nodes.items():
        address = native_port(cell, interface['address'])
        if len(address) != 2 or len(native_port(cell, interface['outputs'])) != 4:
            raise ValueError('Bridged radix-4 requires two address inputs and four outputs per core')
        for lane, pin in enumerate(address.pins):
            index = 2 * level + lane
            connect(pin, bits[index] if index < len(bits) else ground)
        source = enable if level == top else native_port(
            nodes[level + 1, group // 4], interface['outputs'])[group % 4]
        connect(native_port(cell, interface['enable'])[0], source)
        if level != top:
            # Inter-stage bridges carry these nets in the native layout.
            native_port(cell, interface['enable']).native_abutment = True
        if level > 0:
            native_port(cell, interface['outputs']).native_abutment = True
    # Surface every remaining auxiliary port for an explicit profile mapping.
    for cell in instances:
        for port in cell.ports:
            if any(len(pin.net.pins) == 1 for pin in port.pins):
                # Final selections are consumed by the caller, not unresolved inputs.
                if port.native_name != interface['outputs']:
                    unassigned.append((cell, port))
    leaves = [nodes[0, group] for group in sorted(g for level, g in nodes if level == 0)]
    outputs = [pin for cell in leaves for pin in native_port(
        cell, interface['outputs']).pins][:count]
    run = ([pin for cell in leaves for pin in native_port(cell, interface['run_outputs']).pins][:count]
           if interface.get('run_outputs') else [])
    run_inputs, internal_records, internal_ids = [], [], set()
    contract = auxiliary_contract or {}
    active = set(range(count) if active_outputs is None else active_outputs)
    if any(type(i) is not int or not 0 <= i < count for i in active):
        raise ValueError('Decoder active output addresses must lie within its address space')
    by_cell = {cell: (level, group) for (level, group), cell in nodes.items()}
    known = {p.native_name for c in instances for p in c.ports}
    internal_names = validate_auxiliary_contract(contract, known)
    for cell, port in unassigned:
        info = by_cell.get(cell)
        if port.native_name in internal_names:
            indices = tuple(range(len(port)))
        elif port.native_name in contract.get('leaf_ports', {}):
            # Higher-stage/helper copies and rounded-up leaf outputs are internal;
            # active leaf terminals remain externally required, lane by lane.
            indices = tuple(i for i in range(len(port)) if info is None or info[0] != 0
                            or info[1] * 4 + i not in active)
        else:
            continue
        internal_records.append((cell, port, indices))
        internal_ids.update(id(port[i]) for i in indices)
    analog_name = contract.get('analog_inputs')
    if analog_name:
        # decoder_bands places stage zero at the top. Each physical column
        # carries independent analog lanes through its native helper/stage cells.
        columns = {}
        for cell in instances:
            column, stage = cell.algorithm_xy
            if any(port.native_name == analog_name for port in cell.ports):
                columns.setdefault(column, []).append((stage, cell))
        offset = 0
        leaf_set = set(leaves)
        for column in sorted(columns):
            stack = sorted(columns[column], key=lambda item: item[0])
            top_port = native_port(stack[0][1], analog_name)
            for stage, cell in stack:
                analog_port = native_port(cell, analog_name)
                if len(analog_port) != len(top_port):
                    raise ValueError('Decoder analog pass-through widths differ within a column')
                for top_pin, pin in zip(top_port.pins, analog_port.pins):
                    connect(top_pin, pin)
                analog_port.native_abutment = cell is not stack[0][1]
                for port in cell.ports:
                    if port.native_name == interface.get('run_outputs'):
                        # Only the leaf/bottom contact crosses to the switch bank.
                        port.native_abutment = cell not in leaf_set
            run_inputs.extend(pin for lane, pin in enumerate(top_port.pins)
                              if offset + lane in active)
            offset += len(top_port)
    return BridgedResult(bits=bits, enable=enable, outputs=outputs, instances=instances,
                         supplies=supplies,
                         run_outputs=run, unassigned=unassigned, run_inputs=run_inputs,
                         internal_auxiliary=internal_records, internal_pin_ids=internal_ids)
