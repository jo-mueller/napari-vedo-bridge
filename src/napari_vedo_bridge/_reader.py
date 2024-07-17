import numpy as np
from napari.layers import Layer
from typing import Union, Sequence, List, Optional

PathLike = str
PathOrPaths = Union[PathLike, Sequence[PathLike]]


_supported_extensions = ['vtp', 'ply', 'obj', 'vtk', 'stl']


def get_reader(path: "PathOrPaths") -> Optional["ReaderFunction"]:
    import os
    from pathlib import Path
    import vedo

    # in case a single file is passed
    if isinstance(path, str) and path.split('.')[-1] in _supported_extensions:
        thing = vedo.load(path)
        if type(thing) is vedo.Points:
            return points_reader
        elif type(thing) is vedo.Mesh:

            # if it's a mesh with no edges, it's probably a points layer
            if len(thing.cells) == 0:
                return points_reader
            else:
                return surfaces_reader

    # in case a list of files is passed
    elif isinstance(path, list) and all(
        p.split('.')[-1] in _supported_extensions for p in path
    ):

        # ensure correct order of files(files are xxx.format.0, etc)
        path = sorted(path, key=lambda x: int(Path(x).stem))

        thing = vedo.load(path[0])
        if type(thing) is vedo.Points:
            return points_reader
        elif type(thing) is vedo.Mesh:

            # if it's a mesh with no edges, it's probably a points layer
            if len(thing.cells) == 0:
                return points_reader
            else:
                return surfaces_reader

    # in case a directory is passed
    # find all files inside and pass again as list
    elif isinstance(path, str) and os.path.isdir(path):
        filenames = [os.path.join(path, f) for f in os.listdir(path)] 
        return get_reader(filenames)

    return None


def points_reader(path: PathOrPaths) -> List["LayerData"]:
    import os
    import tqdm
    from napari_timelapse_processor import TimelapseConverter

    # whether directory, list of files or single file is passed
    if os.path.isdir(path):
        path = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.split('.')[-1] in _supported_extensions]
    elif isinstance(path, list):
        pass
    elif isinstance(path, str):
        path = [path]

    layers = []
    if len(path) == 1:
        layer = _read_single_points(path[0])
        data = layer.data
        properties = {
            'features': layer.features,
            'size': 0.5
        }

    else:
        # read all the files, create a layer from each
        for i, p in tqdm.tqdm(enumerate(path), total=len(path)):
            layer = _read_single_points(p)
            layers.append(layer)

        # Stack output layer and return
        Converter = TimelapseConverter()
        layer_4d = Converter.stack_data(layers, layertype=Layer)
        data = layer_4d.data
        properties = {
            'features': layer_4d.features,
            'size': 0.5
        }

    # color the pointcloud by the first detected feature
    if not properties['features'].empty:
        properties['face_color'] = properties['features'].columns[0]

    return [(data, properties, 'points')]


def surfaces_reader(path: PathOrPaths) -> List["LayerData"]:
    import os
    import tqdm
    import pkg_resources
    from napari_timelapse_processor import TimelapseConverter
    import napari

    # whether directory, list of files or single file is passed
    if os.path.isdir(path):
        path = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.split('.')[-1] in _supported_extensions
            ]
    elif isinstance(path, list):
        pass
    elif isinstance(path, str):
        path = [path]

    layers = []
    if len(path) == 1:
        layer = _read_single_surface(path[0])
        data = layer.data

    else:
        # read all the files, create a layer from each
        for i, p in tqdm.tqdm(enumerate(path), total=len(path)):
            layer = _read_single_surface(p)
            layers.append(layer)

        # Stack output layer and return
        Converter = TimelapseConverter()
        layer = Converter.stack_data(layers, layertype=Layer)
        data = layer.data

    # check if napari version is 0.5.0 or higher
    # surface_layer.features only available in 0.5.0 or higher

    properties = {}
    if pkg_resources.parse_version(napari.__version__) >= \
            pkg_resources.parse_version('0.5.0'):
        properties['features'] = layer.features

    return [(data, properties, 'surface')]


def _read_single_points(path) -> Layer:
    """
    Read a single points file and return a Layer object
    """
    import vedo
    import pandas as pd
    from napari.layers import Layer
    points = vedo.load(path)

    # This is done, because vedo adds an RGB (Nx3) feature
    # to the pointdata for some formats
    features = {
        key: np.asarray(points.pointdata[key])
        for key in points.pointdata.keys()
        if len(points.pointdata[key].shape) == 1
        }

    layer = Layer.create(
            points.vertices,
            {'features': pd.DataFrame(features)},
            'points'
        )

    return layer


def _read_single_surface(path):
    """
    Read a single surface file and return a Layer object
    """
    import vedo
    import pandas as pd
    from napari.layers import Layer
    surface = vedo.load(path)

    layer = Layer.create(
            (surface.vertices, np.asarray(surface.cells, dtype=int)),
            {},
            'surface'
        )
    layer.features = pd.DataFrame(dict(surface.pointdata))

    return layer
