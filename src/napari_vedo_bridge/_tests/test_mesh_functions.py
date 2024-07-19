import pytest
import numpy as np
from napari_vedo_bridge._mesh import (
    compute_normals,
    shrink,
    join,
    subdivide,
    decimate,
    decimate_pro,
    decimate_binned,
    smooth,
    fill_holes,
    inside_points,
    extrude,
    split,
    extract_largest_region,
    binarize,
)
from napari_vedo_bridge._points import (
    smooth_points,
    decimate_points,
    cluster_points,
    remove_outliers,
    compute_normals as compute_normals_points,
    extract_largest_cluster,
)

@pytest.fixture
def sample_mesh():
    vertices = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1],
    ])
    faces = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [4, 5, 6],
        [4, 6, 7],
        [0, 1, 5],
        [0, 5, 4],
        [1, 2, 6],
        [1, 6, 5],
        [2, 3, 7],
        [2, 7, 6],
        [3, 0, 4],
        [3, 4, 7],
    ])
    return vertices, faces

@pytest.fixture
def sample_points():
    return np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1],
    ])

def test_compute_normals(sample_mesh):
    result = compute_normals(sample_mesh)
    assert result is not None

def test_shrink(sample_mesh):
    result = shrink(sample_mesh, fraction=0.8)
    assert result is not None

def test_join(sample_mesh):
    result = join([sample_mesh, sample_mesh])
    assert result is not None

def test_subdivide(sample_mesh):
    result = subdivide(sample_mesh, n=2)
    assert result is not None

def test_decimate(sample_mesh):
    result = decimate(sample_mesh, fraction=0.3)
    assert result is not None

def test_decimate_pro(sample_mesh):
    result = decimate_pro(sample_mesh, reduction=0.3)
    assert result is not None

def test_decimate_binned(sample_mesh):
    result = decimate_binned(sample_mesh, bins=50)
    assert result is not None

def test_smooth(sample_mesh):
    result = smooth(sample_mesh, n_iterations=10, pass_band=0.2, edge_angle=20, feature_angle=70, boundary=True)
    assert result is not None

def test_fill_holes(sample_mesh):
    result = fill_holes(sample_mesh, size=500)
    assert result is not None

def test_inside_points(sample_mesh, sample_points):
    result = inside_points(sample_mesh, sample_points)
    assert result is not None

def test_extrude(sample_mesh):
    result = extrude(sample_mesh, zshift=2.0)
    assert result is not None

def test_split(sample_mesh):
    result = split(sample_mesh)
    assert result is not None

def test_extract_largest_region(sample_mesh):
    result = extract_largest_region(sample_mesh)
    assert result is not None

def test_binarize(sample_mesh):
    result = binarize(sample_mesh, threshold=0.6)
    assert result is not None

def test_smooth_points(sample_points):
    result = smooth_points(sample_points, n_iterations=10, pass_band=0.2, edge_angle=20, feature_angle=70, boundary=True)
    assert result is not None

def test_decimate_points(sample_points):
    result = decimate_points(sample_points, fraction=0.3)
    assert result is not None

def test_cluster_points(sample_points):
    result = cluster_points(sample_points, radius=0.2)
    assert result is not None

def test_remove_outliers(sample_points):
    result = remove_outliers(sample_points, radius=0.2, neighbors=3)
    assert result is not None

def test_compute_normals_points(sample_points):
    result = compute_normals_points(sample_points, radius=0.2)
    assert result is not None

def test_extract_largest_cluster(sample_points):
    result = extract_largest_cluster(sample_points)
    assert result is not None
