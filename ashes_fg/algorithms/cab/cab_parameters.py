"""Technology-independent CAB sizing; physical rounding belongs to the adapter."""
from dataclasses import dataclass, asdict
import json
from pathlib import Path


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{name} must be an integer >= {minimum}')
    return value


@dataclass(frozen=True)
class Device:
    key: str
    std_cell: str
    count: int
    inputs: tuple
    outputs: tuple
    role: str = 'signal'
    assembly: str = ''


@dataclass(frozen=True)
class Parameters:
    mode: str
    devices: tuple
    cab_device_cfg: str
    AMatrix_Rows: int
    AMatrix_Cols: int
    BMatrix_Rows: int
    BMatrix_Cols: int
    OutMatrix_Rows: int
    OutMatrix_Cols: int
    CEW_Rows: int
    CEW_Cols: int
    CNS_Rows: int
    CNS_Cols: int
    C_EW_to_A: int
    C_NS_to_A: int
    CSC_rows: int
    A_col: int
    A_col_biases: int
    A_col_pwr: int
    A_bias_connections: tuple = ()

    def as_dict(self):
        return asdict(self)


def parse(settings, discover=None, *, csc_gate_alignment=None, shared_gate_selection=False,
          sblock_gate_channels=6):
    """discover(master, input_names, output_names) returns ordered pin identifiers.

    Names may be omitted: a technology adapter then discovers analog interface
    pins from its golden-coordinate metadata. Bus members count individually.
    Device keys and instance repetitions retain JSON insertion order.
    """
    mode = settings.get('mode')
    integer(sblock_gate_channels, 'S-block gate channels')
    if mode not in ('cab_devices', 'matrix'):
        raise ValueError('mode must be "cab_devices" or "matrix"')

    def get(name, minimum=0):
        if name not in settings:
            raise ValueError(f'{mode}: missing required parameter {name}')
        return integer(settings[name], name, minimum)

    a = get('A_col', 1)
    biases, power = get('A_col_biases'), get('A_col_pwr')
    out, csc = get('Out_row', 1), get('CSC_rows', 1)
    if __package__:
        from .a_bias import validate_connections
    else:
        from a_bias import validate_connections
    bias_connections = validate_connections(settings.get('A_bias_connections', []), biases)
    cfg = settings.get('cab_device_cfg', 'abut')
    if cfg not in ('abut', 'spaced'):
        raise ValueError('cab_device_cfg must be "abut" or "spaced"')
    devices = []
    if mode == 'cab_devices':
        entries = settings.get('cab_device_list')
        if not isinstance(entries, dict) or not entries:
            raise ValueError('cab_device_list must be a nonempty ordered object')
        if discover is None:
            raise ValueError('cab_devices requires a technology pin-discovery adapter')
        for key, entry in entries.items():
            if not isinstance(entry, dict) or not isinstance(entry.get('std_cell'), str):
                raise ValueError(f'{key}: expected std_cell and count')
            count = integer(entry.get('count'), f'{key}.count', 1)
            for field in ('inp_pins', 'out_pins'):
                names = entry.get(field)
                if names is not None and (not isinstance(names, list) or
                        any(not isinstance(name, str) for name in names) or
                        len(set(names)) != len(names)):
                    raise ValueError(f'{key}.{field}: expected a list of unique port names')
            metadata = getattr(discover, 'profiles', {}).get(entry['std_cell'], {})
            role, assembly = metadata.get('role', 'signal'), metadata.get('assembly', '')
            if role not in ('signal', 'support'):
                raise ValueError(f'{key}: unsupported device role {role!r}')
            if role == 'support' and (assembly != 'activation' or not devices
                    or devices[-1].assembly != assembly or devices[-1].role != 'signal'
                    or count != 1):
                raise ValueError(f'{key}: one activation support cell must follow its signal devices')
            inputs, outputs = discover(entry['std_cell'], entry.get('inp_pins'), entry.get('out_pins'))
            inputs, outputs = tuple(inputs), tuple(outputs)
            if role == 'signal' and (not inputs or not outputs):
                raise ValueError(f'{key}: device needs input and output signal pins')
            if role == 'support' and (inputs or outputs):
                raise ValueError(f'{key}: support cells must not add functional matrix lanes')
            if len(set(inputs)) != len(inputs) or len(set(outputs)) != len(outputs) or set(inputs) & set(outputs):
                raise ValueError(f'{key}: duplicate or overlapping device pins')
            devices.append(Device(key, entry['std_cell'], count, inputs, outputs, role, assembly))
        rows = sum(d.count * len(d.inputs) for d in devices) + get('AB_row_extras')
        columns = sum(d.count * len(d.outputs) for d in devices)
        # Odd A_col gives the extra lane to CNS; odd output count goes to CNS.
        ew_a, ns_a = a // 2, a - a // 2
        ew_rows = ns_rows = csc
        ew_columns = ew_a + out // 2
        ns_columns = ns_a + out - out // 2
    else:
        rows, columns = get('AB_row', 1), get('B_col', 1)
        ew_a, ns_a = get('C_EW_to_A'), get('C_NS_to_A')
        if ew_a + ns_a != a:
            raise ValueError('C_EW_to_A + C_NS_to_A must equal A_col')
        dimensions = []
        for name in ('C_EW', 'C_NS'):
            dim = settings.get(name)
            if not isinstance(dim, list) or len(dim) != 2:
                raise ValueError(f'{name} must be [rows, columns]')
            dimensions.append(tuple(integer(n, f'{name}[{i}]', 1) for i, n in enumerate(dim)))
        (ew_rows, ew_columns), (ns_rows, ns_columns) = dimensions
        if ew_rows != csc or ns_rows != csc:
            raise ValueError('C_EW and C_NS row counts must match CSC_rows for the S-block interface')
        if ew_columns < ew_a + out // 2 or ns_columns < ns_a + out - out // 2:
            raise ValueError('C matrix columns must accommodate A connections and external input lanes')
    if shared_gate_selection:
        # A and B consume one combined prefix of the CSC gate selections.
        # Legacy callers retain six channels; profile-selected callers supply
        # the capacity of their chosen S-block algorithm/interface.
        required = a + biases + power + columns
        missing = max(0, required - (ew_columns + ns_columns + sblock_gate_channels))
        if missing and mode == 'matrix':
            raise ValueError('CSC gate selections must cover A columns plus B columns')
        ew_columns += missing // 2
        ns_columns += missing - missing // 2
    if csc_gate_alignment is not None:
        leaf, ns_residue = csc_gate_alignment
        integer(leaf, 'CSC decoder leaf size', 1)
        integer(ns_residue, 'CNS decoder residue')
        if ns_residue >= leaf:
            raise ValueError('CNS decoder residue must be smaller than its leaf size')
        if mode == 'cab_devices':
            ew_columns += (-ew_columns) % leaf
            ns_columns += (ns_residue - ns_columns) % leaf
        elif ew_columns % leaf or ns_columns % leaf != ns_residue:
            raise ValueError(f'CSC gate profile requires C_EW columns divisible by {leaf} '
                             f'and C_NS columns congruent to {ns_residue} modulo {leaf}')
    return Parameters(mode, tuple(devices), cfg, rows, a + biases + power,
                      rows, columns, out, columns, ew_rows, ew_columns,
                      ns_rows, ns_columns, ew_a, ns_a, csc, a, biases, power, bias_connections)


def load(path, discover=None, *, csc_gate_alignment=None, shared_gate_selection=False,
         sblock_gate_channels=6):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    with Path(path).open(encoding='utf-8') as source:
        return parse(json.load(source, object_pairs_hook=unique_object), discover,
                     csc_gate_alignment=csc_gate_alignment, shared_gate_selection=shared_gate_selection,
                     sblock_gate_channels=sblock_gate_channels)
