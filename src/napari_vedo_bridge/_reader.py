from typing import Union, Sequence, Callable, List, Optional
PathLike = str
PathOrPaths = Union[PathLike, Sequence[PathLike]]
from napari.layers import Layer
#ReaderFunction = Callable[[PathOrPaths], List[LayerData]]

def get_reader(path: "PathOrPaths") -> Optional["ReaderFunction"]:
    import os
    import vedo

    # in case a single file is passed
    if isinstance(path, str) and path.endswith('.vtp'):
        thing = vedo.load(path)
        if type(thing) is vedo.Points:
            return points_reader
        elif type(thing) is vedo.Mesh:
            return surfaces_reader

    # in case a list of files is passed
    elif isinstance(path, list) and all([p.endswith('.vtp') for p in path]):
        thing = vedo.load(path[0])
        if type(thing) is vedo.Points:
            return points_reader
        elif type(thing) is vedo.Mesh:
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
        path = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.vtp')]
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
    from napari_timelapse_processor import TimelapseConverter

    # whether directory, list of files or single file is passed
    if os.path.isdir(path):
        path = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.vtp')]
    elif isinstance(path, list):
        pass
    elif isinstance(path, str):
        path = [path]

    layers = []
    if len(path) == 1:
        layer = _read_single_surface(path[0])
        data = layer.data
        properties = {
            'features': layer.features,
            'size': 0.5
        }

    else:
        # read all the files, create a layer from each
        for i, p in tqdm.tqdm(enumerate(path), total=len(path)):
            layer = _read_single_surface(p)
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
    
    return [(data, properties, 'surface')]


def _read_single_points(path) -> Layer:
    """
    Read a single points file and return a Layer object
    """
    import vedo
    import pandas as pd
    points = vedo.load(path)

    layer = (
            points.vertices,
            {'features': pd.DataFrame(dict(points.pointdata))},
            'points'
        )
    
    return layer

def _read_single_surface(path):
    """
    Read a single surface file and return a Layer object
    """
    import vedo
    import pandas as pd
    surface = vedo.load(path)

    layer = (
            surface.points(),
            {},
            'surface'
        )
    layer.features = pd.DataFrame(dict(surface.pointdata))
    
    return layer