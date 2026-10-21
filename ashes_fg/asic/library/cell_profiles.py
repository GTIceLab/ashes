"""Load optional hand-maintained profiles beside a generated cell module."""
from importlib import import_module, util
from pathlib import Path
import sys


def load_cell_library(cells):
    """Resolve a module/name and register its adjacent <stem>_profiles.py.

    Libraries without a companion file retain their existing behavior. Profile
    import/validation errors propagate; a broken profile is never silently
    ignored. Registration is repeatable and the provider must preserve overrides.
    """
    library = import_module(cells) if isinstance(cells, str) else cells
    source = getattr(library, '__file__', None)
    if source is None:
        return library
    source = Path(source)
    path = source.with_name(source.stem + '_profiles.py')
    if not path.is_file():
        return library
    name = library.__name__ + '_profiles'
    provider = sys.modules.get(name)
    if provider is not None:
        if Path(provider.__file__).resolve() != path.resolve():
            raise ValueError(f'Profile module {name} is already loaded from another library path')
    else:
        spec = util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f'Cannot load cell profiles: {path}')
        provider = util.module_from_spec(spec)
        sys.modules[name] = provider
        try:
            spec.loader.exec_module(provider)
        except Exception:
            sys.modules.pop(name, None)
            raise
    register = getattr(provider, 'register_profiles', None)
    if not callable(register):
        raise TypeError(f'{path}: expected register_profiles(cells)')
    register(library)
    return library
