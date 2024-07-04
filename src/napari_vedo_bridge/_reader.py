from typing import Union, Sequence, Callable, List, Optional
PathLike = str
PathOrPaths = Union[PathLike, Sequence[PathLike]]
#ReaderFunction = Callable[[PathOrPaths], List[LayerData]]

def get_reader(path: "PathOrPaths") -> Optional["ReaderFunction"]:
    import os
    if isinstance(path, str) and path.endswith('.vtp'):
        return points_reader
    elif isinstance(path, list) and all([p.endswith('.vtp') for p in path]):
        return points_reader
    elif isinstance(path, str) and os.path.isdir(path):
        return points_reader

    return None

def points_reader(path: PathOrPaths) -> List["LayerData"]:
    import vedo
    import pandas as pd
    import os
    import tqdm
    from napari_timelapse_processor import TimelapseConverter
    from napari.layers import Layer

    # whether directory, list of files or single file is passed
    if os.path.isdir(path):
        path = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.vtp')]
    elif isinstance(path, list):
        pass
    elif isinstance(path, str):
        path = [path]

    layers = []
    if len(path) == 1:
        points = vedo.load(path[0])
        layer = (
            points.vertices,
            {'features': pd.DataFrame(dict(points.pointdata))},
            'points'
        )

        data = layer.data
        properties = {
            'features': layer.features,
            'size': 0.5
        }

    else:
        # read all the files, create a layer from each
        for i, p in tqdm.tqdm(enumerate(path), total=len(path)):
            points = vedo.load(p)
            layer = Layer.create(
                points.vertices,
                {
                    'features': pd.DataFrame(dict(points.pointdata)),
                    'size': 0.5,
                    },
                'points')
            layers.append(layer)

        # Stack output layer and return
        Converter = TimelapseConverter()
        layer_4d = Converter.stack_data(layers, layertype=Layer)
        data = layer_4d.data
        properties = {
            'features': layer_4d.features,
            'size': 0.5
        }

    # color the pointclloud by the first detected feature
    if not properties['features'].empty:
        properties['face_color'] = properties['features'].columns[0]
    
    return [(data, properties, 'points')]