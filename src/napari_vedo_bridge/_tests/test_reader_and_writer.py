import pytest

@pytest.fixture
def create_4d_mesh():
    import vedo
    import numpy as np
    from napari_timelapse_processor import TimelapseConverter

    spheres = [vedo.IcoSphere(pos=(i, i, i), r=10).clean() for i in range(10)]
    spheres_tuples = [(np.round(s.vertices, 3), np.asarray(s.cells, dtype=int)) for s in spheres]

    Converter = TimelapseConverter()
    return Converter.stack_data(spheres_tuples, layertype='napari.types.SurfaceData')

@pytest.fixture
def create_4d_points():
    import vedo
    import numpy as np
    from napari_timelapse_processor import TimelapseConverter
    from napari.layers import Points
    import pandas as pd

    spheres = [np.round(vedo.Sphere(pos=(i, i, i), r=10).clean().vertices, 3) for i in range(10)]

    Converter = TimelapseConverter()
    points_4d = Converter.stack_data(spheres, layertype='napari.types.PointsData')
    features = pd.DataFrame({'feature1': np.random.rand(len(points_4d))})

    return Points(data=points_4d, features=features)

@pytest.mark.parametrize("formats", ['vtp', 'vtk', 'obj', 'stl', 'ply'])
def test_writer_reader_mesh_4d(create_4d_mesh, formats):
    from napari.layers import Layer, Surface
    from pathlib import Path
    import numpy as np

    from napari_vedo_bridge._writer import write_surfaces
    from napari_vedo_bridge._reader import get_reader

    layer_input = Surface(create_4d_mesh)
    layer_input.features = None
    ldtuple = Layer.as_layer_data_tuple(layer_input)

    output_paths = write_surfaces('test.vtp', ldtuple[0], ldtuple[1])
    assert len(output_paths) == 10

    reader = get_reader(output_paths[0])
    assert reader is not None

    layers = reader(Path(output_paths[0]).parent)

    print(layers[0][0][0])
    print(layer_input.data[0])
    assert len(layers) == 1
    assert np.array_equal(layers[0][0][0], layer_input.data[0])
    assert np.array_equal(layers[0][0][1], layer_input.data[1])

    # clean up
    for p in output_paths:
        Path(p).unlink()

    # remove directory if it exists
    if Path('test').exists():
        Path('test').rmdir()


@pytest.mark.parametrize("formats", ['vtp', 'vtk', 'obj', 'stl', 'ply'])
def test_writer_reader_points_4d(create_4d_points, formats):
    from napari.layers import Layer, Points
    from pathlib import Path
    import numpy as np

    from napari_vedo_bridge._writer import write_points
    from napari_vedo_bridge._reader import get_reader

    ldtuple = Layer.as_layer_data_tuple(create_4d_points)

    output_paths = write_points('test.vtp', ldtuple[0], ldtuple[1])
    assert len(output_paths) == 10

    reader = get_reader(output_paths[0])
    assert reader is not None

    layers = reader(Path(output_paths[0]).parent)
    
    # check that only one (4d) layer is returned
    assert len(layers) == 1

    # check that point coordinates are the same
    assert np.array_equal(layers[0][0], create_4d_points.data)

    # check that features are the same
    assert np.array_equal(layers[0][1]['features']['feature1'], create_4d_points.features['feature1'])

    # clean up
    for p in output_paths:
        Path(p).unlink()

    # remove directory if it exists
    if Path('test').exists():
        Path('test').rmdir()