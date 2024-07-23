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
    inside_points,
    split,
    extract_largest_region,
    binarize,
)
from napari.layers import Surface, Points


@pytest.fixture
def sample_surface():
    return vedo.load(vedo.dataurl + 'bunny.obj')


@pytest.fixture
def sample_points():
    return np.random.randn(1000, 3)


def test_compute_normals(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    normals = compute_normals(surface)
    assert normals.shape == (surface.data[0].shape[0], 2, 3)


def test_shrink(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    shrunk_surface = shrink(surface, fraction=0.5)
    assert shrunk_surface.data[0].shape == surface.data[0].shape
    assert shrunk_surface.data[1].shape == surface.data[1].shape


def test_subdivide(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    subdivided_surface = subdivide(surface, n_iterations=1)
    assert subdivided_surface.data[0].shape[0] > surface.data[0].shape[0]
    assert subdivided_surface.data[1].shape[0] > surface.data[1].shape[0]


def test_decimate(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    decimated_surface = decimate(surface, fraction=0.5)
    assert decimated_surface.data[0].shape[0] < surface.data[0].shape[0]
    assert decimated_surface.data[1].shape[0] < surface.data[1].shape[0]


def test_decimate_pro(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    decimated_surface = decimate_pro(surface, fraction=0.5)
    assert decimated_surface.data[0].shape[0] < surface.data[0].shape[0]
    assert decimated_surface.data[1].shape[0] < surface.data[1].shape[0]


def test_decimate_binned(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    decimated_surface = decimate_binned(surface, divisions=(10, 10, 10))
    assert decimated_surface.data[0].shape[0] < surface.data[0].shape[0]
    assert decimated_surface.data[1].shape[0] < surface.data[1].shape[0]


def test_smooth(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    smoothed_surface = smooth(surface, n_iterations=15, pass_band=0.1, edge_angle=15, feature_angle=60, boundary=False)
    assert smoothed_surface.data[0].shape == surface.data[0].shape
    assert smoothed_surface.data[1].shape == surface.data[1].shape


def test_fill_holes(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    filled_surface = fill_holes(surface, size=1000)
    assert filled_surface.data[0].shape == surface.data[0].shape
    assert filled_surface.data[1].shape == surface.data[1].shape


def test_inside_points(sample_surface, sample_points):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    points = Points(sample_points)
    inside_pts = inside_points(surface, points)
    assert inside_pts.shape[1] == 3


def test_split(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    split_surfaces = split(surface)
    assert len(split_surfaces) > 1


def test_extract_largest_region(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    largest_region = extract_largest_region(surface)
    assert largest_region.data[0].shape[0] <= surface.data[0].shape[0]
    assert largest_region.data[1].shape[0] <= surface.data[1].shape[0]


def test_binarize(sample_surface):
    surface = Surface((sample_surface.vertices, np.asarray(sample_surface.cells)))
    reference_image = np.zeros((100, 100, 100))
    binarized_surface = binarize(surface, reference_image)
    assert binarized_surface.data[0].shape[0] > 0
    assert binarized_surface.data[1].shape[0] > 0
