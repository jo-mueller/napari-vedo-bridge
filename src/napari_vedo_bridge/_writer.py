from typing import Any, List
from napari_timelapse_processor import TimelapseConverter
from napari.layers import Points, Layer, Surface


def write_points(
        path: str,
        layer_data: Any,
        attributes: dict
) -> List[str]:
    import vedo
    import os
    from pathlib import Path
    import tqdm

    format = Path(path).suffix[1:]

    layer = Layer.create(layer_data, attributes, 'points')
    Converter = TimelapseConverter()

    # is it 4D?
    if layer.data.shape[1] == 4:
        list_of_layers = Converter.unstack_data(layer, layertype=Points)
    else:
        list_of_layers = [layer]

    # if there is only one timepoint, just write it
    if len(list_of_layers) == 1:
        points = vedo.Points(list_of_layers[0].data)

        for key in dict(list_of_layers[0].features).keys():
            points.pointdata[key] = list_of_layers[0].features[key]
        vedo.write(points, path)
        return [path]

    # if there are multiple timepoints, write each one separately
    else:
        os.makedirs(Path(path).parent / Path(path).stem, exist_ok=True)
        output_paths = []
        for i, layer in tqdm.tqdm(enumerate(list_of_layers), total=len(list_of_layers)):
            points = vedo.Points(layer.data[:, :3])
            for key in dict(list_of_layers[0].features).keys():
                points.pointdata[key] = list_of_layers[i].features[key]

            output_path = str(Path(path).parent / Path(path).stem / "{:03d}.{:s}".format(i, format))
            output_paths.append(output_path)

            vedo.write(points, output_path)

        return output_paths


def write_surfaces(
        path: str,
        layer_data: Any,
        attributes: dict
) -> List[str]:
    import vedo
    import os
    from pathlib import Path
    import tqdm
    import pandas as pd

    format = Path(path).suffix[1:]

    layer = Layer.create(layer_data, attributes, 'surface')
    if not hasattr(layer, 'features'):
        layer.features = pd.DataFrame()

    # is it 4D?
    if layer.data[0].shape[1] == 4:
        Converter = TimelapseConverter()
        list_of_layers = Converter.unstack_data(layer, layertype=Surface)
    else:
        list_of_layers = [layer]

    # if there is only one timepoint, just write it
    if len(list_of_layers) == 1:
        mesh = vedo.Mesh(list_of_layers[0].data)
        for key in dict(list_of_layers[0].features).keys():
            mesh.pointdata[key] = list_of_layers[0].features[key]
        vedo.write(mesh, path)
        return [path]

    # if there are multiple timepoints, write each one separately
    else:
        os.makedirs(Path(path).parent / Path(path).stem, exist_ok=True)
        output_paths = []
        for i, layer in tqdm.tqdm(enumerate(list_of_layers), total=len(list_of_layers)):
            mesh = vedo.Mesh((layer.data[0], layer.data[1].astype(int)))
            for key in dict(list_of_layers[0].features).keys():
                mesh.pointdata[key] = list_of_layers[i].features[key]

            output_path = str(Path(path).parent / Path(path).stem / "{:03d}.{:s}".format(i, format))
            output_paths.append(output_path)

            vedo.write(mesh, output_path)

        return output_paths
