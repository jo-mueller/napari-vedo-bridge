import pytest
import vedo
import numpy as np
from napari_vedo_bridge._mesh import (
    compute_normals,
    shrink,
    subdivide,
    decimate,
    decimate_pro,
    decimate_binned,
    smooth,
    fill_holes,
    split,
    extract_largest_region,
    binarize,
)
from napari.layers import Surface


@pytest.fixture
def sample_surface():
    mesh = vedo.load(vedo.dataurl + 'bunny.obj')
    surface = Surface((mesh.vertices, np.asarray(mesh.cells, dtype=int)))
    return surface


@pytest.fixture
def sample_points():
    return np.random.randn(1000, 3)


def test_compute_normals(sample_surface):
    normals = compute_normals()(surface=sample_surface)
    assert normals.data.shape == (sample_surface.data[0].shape[0], 2, 3)


def test_shrink(sample_surface):
    shrunk_surface = shrink()(surface=sample_surface, fraction=0.5)
    assert shrunk_surface is not None


def test_subdivide(sample_surface):
    subdivided_surface = subdivide()(surface=sample_surface, n_iterations=1)
    assert subdivided_surface.data[0].shape[0] > sample_surface.data[0].shape[0]
    assert subdivided_surface.data[1].shape[0] > sample_surface.data[1].shape[0]


def test_decimate(sample_surface):
    decimated_surface = decimate()(surface=sample_surface, fraction=0.5)
    assert decimated_surface.data[0].shape[0] < sample_surface.data[0].shape[0]
    assert decimated_surface.data[1].shape[0] < sample_surface.data[1].shape[0]


def test_decimate_pro(sample_surface):
    decimated_surface = decimate_pro()(surface=sample_surface, fraction=0.5)
    assert decimated_surface.data[0].shape[0] < sample_surface.data[0].shape[0]
    assert decimated_surface.data[1].shape[0] < sample_surface.data[1].shape[0]


def test_decimate_binned(sample_surface):
    decimated_surface = decimate_binned()(surface=sample_surface, divisions=(10, 10, 10))
    assert decimated_surface.data[0].shape[0] < sample_surface.data[0].shape[0]
    assert decimated_surface.data[1].shape[0] < sample_surface.data[1].shape[0]


def test_smooth(sample_surface):
    smoothed_surface = smooth()(surface=sample_surface, n_iterations=15, pass_band=0.1, edge_angle=15, feature_angle=60, boundary=False)
    assert smoothed_surface.data[0].shape == sample_surface.data[0].shape
    assert smoothed_surface.data[1].shape == sample_surface.data[1].shape


def test_fill_holes(sample_surface):

    mesh_data = list(sample_surface.data)
    # remove some faces to create holes
    mesh_data[1] = mesh_data[1][:-2]
    sample_surface = Surface(mesh_data)

    filled_surface = fill_holes()(surface=sample_surface, size=1000)

    assert filled_surface.data[0].shape[0] == sample_surface.data[0].shape[0]


def test_split(sample_surface):
    split_surfaces = split()(surface=sample_surface)
    assert len(split_surfaces) == 1


def test_extract_largest_region(sample_surface):
    largest_region = extract_largest_region()(surface=sample_surface)
    assert largest_region.data[0].shape[0] <= sample_surface.data[0].shape[0]
    assert largest_region.data[1].shape[0] <= sample_surface.data[1].shape[0]


def test_binarize(sample_surface):
    binarized_surface = binarize()(surface=sample_surface)
    assert binarized_surface.data[0].shape[0] > 0
    assert binarized_surface.data[1].shape[0] > 0
