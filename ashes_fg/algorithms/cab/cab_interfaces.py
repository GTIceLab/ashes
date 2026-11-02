"""Read golden-coordinate signal ports without constructing design instances.

Libraries supply cab_interfaces for devices whose analog interface is not W/E.
Pin overrides in cab_settings.json use exact native port names.
"""
import ast
from pathlib import Path


class Interfaces:
    def __init__(self, library_path, profiles=None):
        self.profiles = profiles or {}
        self.cells = {}
        for cell in ast.parse(Path(library_path).read_text(encoding='utf-8')).body:
            if not isinstance(cell, ast.ClassDef):
                continue
            ports = {}
            for node in ast.walk(cell):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != 'Port':
                    continue
                name, side = ast.literal_eval(node.args[2]), ast.literal_eval(node.args[3])
                kwargs = {item.arg: item.value for item in node.keywords}
                if 'native_name' in kwargs:
                    name = ast.literal_eval(kwargs['native_name'])
                    # Generated logical interfaces retain the physical side in
                    # native_name, not in the transformed Port.location.
                    suffix = name.rsplit('_', 1)[-1].upper()
                    if suffix in ('N', 'S', 'E', 'W'):
                        side = suffix
                width = node.args[4]
                if not isinstance(width, ast.BinOp) or not isinstance(width.op, ast.Mult):
                    raise ValueError(f'{cell.name}.{name}: unsupported generated port width')
                count = ast.literal_eval(width.left)
                if type(count) is not int or count < 1:
                    raise ValueError(f'{cell.name}.{name}: invalid lane count')
                if name in ports:
                    raise ValueError(f'{cell.name}: duplicate native port {name}')
                ports[name] = (side, count)
            if ports:
                self.cells[cell.name] = ports

    def __call__(self, master, inputs=None, outputs=None):
        if master not in self.cells:
            raise ValueError(f'Unknown CAB standard cell {master!r}; select a master in the chosen library')
        ports = self.cells[master]
        profile = self.profiles.get(master, {})

        def expand(names, role, side):
            use_profile_order = names is None
            if names is None:
                names = profile.get(role)
            if names is None:
                # Explicitly exclude static rails. Bias/control names are
                # technology-owned: profiles must list those under static_ports.
                static = set(profile.get('static_ports', ()))
                names = [name for name, (location, _) in ports.items()
                         if location == side and name not in static and
                         name.rsplit('_', 1)[0].upper() not in
                         {'GND', 'VDD', 'VDD_CORE', 'VSS', 'VINJ', 'VTUN', 'VGPROG', 'VGRUN', 'PROG', 'RUN'}]
            result = []
            for name in names:
                if name not in ports:
                    raise ValueError(f'{master}: unknown native {role} port {name!r}')
                result.extend(f'{name}[{lane}]' for lane in range(ports[name][1]))
            lane_order = profile.get(role[:-1] + '_lanes') if use_profile_order else None
            if lane_order is not None:
                if (not isinstance(lane_order, list)
                        or len(lane_order) != len(set(lane_order))
                        or set(lane_order) != set(result)):
                    raise ValueError(f'{master}: {role} lane order must list every selected lane once')
                result = lane_order
            return tuple(result)
        return (expand(inputs, 'inputs', profile.get('input_side', 'W')),
                expand(outputs, 'outputs', profile.get('output_side', 'E')))


def validate_dimensions(parameters, *, row_unit, column_unit, sblock_unit=4):
    """Reject, never round, dimensions that cannot be tiled in this library."""
    from .cab_parameters import integer
    for name, value in (('row_unit', row_unit), ('column_unit', column_unit), ('sblock_unit', sblock_unit)):
        integer(value, name, 1)
    for name, rows, cols in (
        ('A', parameters.AMatrix_Rows, parameters.AMatrix_Cols),
        ('B', parameters.BMatrix_Rows, parameters.BMatrix_Cols),
        ('Out', parameters.OutMatrix_Rows, parameters.OutMatrix_Cols),
        ('CEW', parameters.CEW_Rows, parameters.CEW_Cols),
        ('CNS', parameters.CNS_Rows, parameters.CNS_Cols),
    ):
        if rows % row_unit or cols % column_unit:
            raise ValueError(f'{name} matrix [{rows}, {cols}] does not fit {row_unit}x{column_unit} cells; adjust the configuration')
    if parameters.CSC_rows % sblock_unit:
        raise ValueError(f'CSC_rows must be divisible by {sblock_unit}')
