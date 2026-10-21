"""Adapt native generated cells to a placement convention, without rotating masters."""
import inspect
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
    if declared != 'xy' or process_coordinates != 'columns_y_rows_minus_x':
        raise ValueError('Coordinate adaptation requires a native XY cell library')
    name = library.__name__ + '__columns_y_rows_minus_x'
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
                native = getattr(port, 'native_location', port.location)
                port.native_location = native
                port.location = logical_side[native]
        return type(base.__name__, (base,), dict(__init__=init, __module__=name,
                    library_master_name=base.__name__))
    for key, value in vars(library).items():
        if inspect.isclass(value) and value is not StandardCell and issubclass(value, StandardCell):
            setattr(result, key, adapted(value))
    sys.modules[name] = result
    return result
