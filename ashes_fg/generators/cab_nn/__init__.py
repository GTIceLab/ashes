"""Profile-selected CAB construction without process-specific branches."""
from importlib import import_module
import json
from pathlib import Path

from ashes_fg.asic.library.cell_profiles import load_cell_library


def build(project='.', settings_path=None, *, cells=None, process_coordinates=None, design_limits=None, **options):
    project = Path(project).resolve()
    synthesis = json.loads((project / 'synthesis_settings.json').read_text())
    library = load_cell_library(cells or synthesis.get('cell_module', 'cell_def.cells'))
    profile = getattr(library, 'cab_profile', {})
    entry = profile.get('builder', 'ashes_fg.generators.cab_nn.legacy.build')
    module, _, function = entry.rpartition('.')
    if not module:
        raise ValueError('CAB profile builder must be a dotted function path')
    recipe = getattr(import_module(module), function)
    area = design_limits if design_limits is not None else synthesis.get('design_limits')
    if area is not None:
        import math
        if (not isinstance(area, (list, tuple)) or len(area) != 2
                or any(isinstance(value, bool) or not isinstance(value, (int, float))
                       or not math.isfinite(value) or value <= 0 for value in area)):
            raise ValueError('design_limits must contain positive finite width and height in database units')
        options['design_limits'] = list(area)
    return recipe(project, settings_path, cells=library,
                  process_coordinates=process_coordinates or synthesis.get('process_coordinates', 'xy'),
                  **options)


def publish(namespace, project):
    """Populate the existing design-file driver contract from one shared build."""
    tile = build(project)
    namespace.update(vars(tile))
    return tile
