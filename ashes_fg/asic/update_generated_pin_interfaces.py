"""Update generated classes from their saved native Port declarations."""
import ast
from pathlib import Path
from json2python import logical_pin_interface, render_class

root = Path('/home/praveen/Projects/NNopt_FPAA_16nm/5_Tools/lib')
paths = [root / 'stdcell_defs/cells.py', root / 'algorithms/cells.py']
staged = []
sizes = {}

for path in paths:
    source = path.read_text()
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    replacements = []
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef) or not any(isinstance(base, ast.Name) and base.id == 'StandardCell' for base in cls.bases):
            continue
        meta = []
        dimension = sizes.get(cls.name, [None, None])
        for node in ast.walk(cls):
            if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call):
                if isinstance(node, ast.Assign) and any(isinstance(target, ast.Attribute) and target.attr == 'size' for target in node.targets):
                    dimension = ast.literal_eval(node.value)
                continue
            call = node.value
            if not isinstance(call.func, ast.Name) or call.func.id != 'Port':
                continue
            # Only the generator's ordinary vector ports are supported here.
            if call.keywords or len(call.args) != 5:
                raise ValueError(f'{path}: {cls.name} has a custom Port declaration; use the generator instead')
            name, direction = ast.literal_eval(call.args[2]), ast.literal_eval(call.args[3])
            count = call.args[4]
            if not isinstance(count, ast.BinOp) or not isinstance(count.op, ast.Mult):
                raise ValueError(f'{cls.name}.{name}: unsupported vector count')
            meta.append((name, direction, ast.literal_eval(count.left)))
        if not meta:
            continue
        sizes[cls.name] = dimension
        try:
            order, logical_meta, native_names = logical_pin_interface([item[0] for item in meta], meta,
                                                  'columns_y_rows_minus_x')
        except ValueError as error:
            print(f'Explicit pin map needed for {cls.name}: {error}; keeping this class unchanged')
            continue
        replacement = render_class(cls.name, order, logical_meta, dimension, native_names,
                                   {name: side for name, side, width in meta})
        replacements.append((cls.lineno - 1, cls.end_lineno, replacement))
    for start, end, replacement in reversed(replacements):
        lines[start:end] = [replacement]
    result = ''.join(lines)
    ast.parse(result)
    staged.append((path, result, len(replacements)))

# Validate both complete files before replacing either; no GDS is changed.
for path, result, count in staged:
    path.write_text(result)
    print(f'Updated {count} generated logical interfaces in {path}')
