from typing import Any, List
from napari_timelapse_processor import TimelapseConverter
from napari.layers import Points, Layer

def write_points(
        path: str,
        layer_data: Any,
        attributes: dict
) -> List[str]:
    import vedo
    import os
    from pathlib import Path
    import tqdm

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

            output_path = str(Path(path).parent / Path(path).stem / "{:03d}.vtp".format(i))
            output_paths.append(output_path)
            
            vedo.write(points, output_path)

        return output_paths
    
