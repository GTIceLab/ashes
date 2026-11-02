"""Adapt declared cell interfaces between placement conventions without rotating masters."""
import inspect
from functools import wraps
import sys
from types import ModuleType
from .cell_profiles import load_cell_library
from ..model.asic_compile import StandardCell

def for_coordinates(cells, process_coordinates='xy'):
    library = load_cell_library(cells)
    if process_coordinates not in ('xy', 'columns_y_rows_minus_x'):
        raise ValueError('Invalid process_coordinates')
    declared = getattr(library, 'cell_coordinates', 'xy')
    if declared == process_coordinates:
        return library
    if declared not in ('xy', 'columns_y_rows_minus_x'):
        raise ValueError('Invalid library cell_coordinates')
    name = library.__name__ + '__' + process_coordinates
    if name in sys.modules:
        return sys.modules[name]
    result = ModuleType(name)
    result.__dict__.update(vars(library))
    result.__name__ = name
    result.__file__ = None  # Profiles are inherited from the already loaded native library.
    result.native_library_file = library.__file__
    result.cell_coordinates = process_coordinates
    logical_side = dict(N='E', E='S', S='W', W='N')
    def adapted(base):
        signature = inspect.signature(base.__init__)
        @wraps(base.__init__)
        def init(self, *args, **kwargs):
            bound = signature.bind(self, *args, **kwargs)
            bound.apply_defaults()
            dim = bound.arguments.get('dim')
            if dim is not None:
                bound.arguments['dim'] = tuple(reversed(dim))
            base.__init__(*bound.args, **bound.kwargs)
            if dim is not None:
                self.dim = tuple(dim)
            for port in self.ports:
                native_name = getattr(port, 'native_name', port.name)
                suffix = native_name.rsplit('_', 1)[-1].upper()
                source_side = ({v: k for k, v in logical_side.items()}[port.location]
                               if declared != 'xy' else port.location)
                native = getattr(port, 'native_location',
                                 suffix if suffix in logical_side else source_side)
                port.native_location = native
                port.location = logical_side[native] if process_coordinates != 'xy' else native
        return type(base.__name__, (base,), dict(__init__=init, __module__=name,
                    library_master_name=base.__name__))
    for key, value in vars(library).items():
        if inspect.isclass(value) and value is not StandardCell and issubclass(value, StandardCell):
            setattr(result, key, adapted(value))
    sys.modules[name] = result
    return result
