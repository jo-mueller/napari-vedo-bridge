import pytest

@pytest.fixture
def create_4d_mesh():
    import vedo
    import numpy as np
    from napari_timelapse_processor import TimelapseConverter

    spheres = [vedo.IcoSphere(pos=(i, i, i), r=10) for i in range(10)]
    spheres_tuples = [(s.vertices, np.asarray(s.cells, dtype=int)) for s in spheres]

    Converter = TimelapseConverter()
    return Converter.stack_data(spheres_tuples, layertype='napari.types.SurfaceData')

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
