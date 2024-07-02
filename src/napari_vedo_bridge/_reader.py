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
    from napari_timelapse_processor import TimelapseConverter
    from napari.layers import Layer

    if os.path.isdir(path):
        path = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.vtp')]

    if isinstance(path, str):
        path = [path]

    layers = []
    if len(path) == 1:
        points = vedo.load(path[0])
        print(points.pointdata)
        layer = (
            points.vertices,
            {
                'features': pd.DataFrame(dict(points.pointdata)),
                'size': 0.5
                },
            'points'
        )
        print(layer)
        return [layer]

    else:
        print('Loading multiple files')
        Converter = TimelapseConverter()
        for i, p in enumerate(path):
            points = vedo.load(p)
            layer = Layer.create(
                points.vertices,
                pd.DataFrame(points.pointdata),
                'points')
            layers.append(layer)

        print('Stacking data')
        layer_4d = Converter.stack_data(layers)

        print('Returning data')
        return [layer_4d.data, {'features': layer_4d.features}, 'points']