import vedo
import inspect
from functools import wraps
import pandas as pd
import numpy as np
import ruamel.yaml
from pathlib import Path

__all__ = [
    'decimate',
    'subdivide',    
]


def make_napari_compatible(func):
    """
    Decorator to make vedo functions compatible with napari.
    """

    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    for i, param in enumerate(params):
        if param.name == 'self':
            params[i] = inspect.Parameter(
                f'Input_mesh_{i}',
                param.kind,
                annotation='napari.types.SurfaceData')

    new_sig = sig.replace(parameters=params, return_annotation='napari.types.SurfaceData')

    @wraps(func)
    def wrapper(surface_data, *args, **kwargs):

        mesh = vedo.Mesh(surface_data)
        result = func(mesh, *args, **kwargs)
        return (result.vertices, np.asarray(result.cells))

    wrapper.__signature__ = new_sig
    return wrapper


# Get all member functions from vedo.Mesh
functions_dict = [
    x for x in inspect.getmembers(vedo.Mesh) if x[0] == '__dict__'
    ][0][1]

functions_to_add_to_yaml = []
for name, func in functions_dict.items():
    if not callable(func) or name not in __all__:
        # print(f'{name} is not a callable')
        continue

    signature = inspect.signature(func)
    if signature.return_annotation == 'Mesh':
        globals()[name] = make_napari_compatible(func)

        description = func.__doc__.split('\n')
        description.remove('') if '' in description else None
        description = [x.strip() for x in description][0]

        functions_to_add_to_yaml.append(
            {'name': func.__name__,
             'command_name': 'napari-vedo-bridge.' + func.__name__,
             'python_name': 'napari_vedo_bridge.vedo_functions:' + func.__name__,
             'description': description})

# add the functions to the globals and create a dataframe for the yaml file
functions_to_add_to_yaml = pd.DataFrame(functions_to_add_to_yaml)

# Create a yaml file for the napari plugin
metadata = {
    'name': 'napari-vedo-bridge',
    'display_name': 'Vedo'
}

# Create a dictionary for contributions
contributions = {
    'commands': [],
    'widgets': []
}

for index, row in functions_to_add_to_yaml.iterrows():
    command_entry = {
        'id': row['command_name'],
        'python_name': row['python_name'],
        'title': row['name']
    }

    widget_entry = {
        'command': row['command_name'],
        'autogenerate': True,
        'display_name': row['name']
    }

    contributions['commands'].append(command_entry)
    contributions['widgets'].append(widget_entry)

# Get path of current file
path = Path(__file__).parent.absolute()

# Load the existing YAML content
yaml = ruamel.yaml.YAML()

with open(path / 'napari.yaml', 'r') as yaml_file:
    existing_data = yaml.load(yaml_file)

# Merge the new contributions with the existing data and remove duplicates
for key in contributions:
    for item in contributions[key]:
        if item not in existing_data['contributions'][key]:
            existing_data['contributions'][key].append(item)

# Write the updated data back to the existing YAML file
with open(path / 'napari.yaml', 'w') as yaml_file:
    yaml.dump(existing_data, yaml_file)