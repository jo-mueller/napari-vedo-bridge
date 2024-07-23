import pytest
import numpy as np
from napari_vedo_bridge._points import smooth_points, remove_outliers
from napari.layers import Points

@pytest.fixture
def sample_points():
    return np.random.randn(1000, 3)

def test_smooth_points(sample_points):
    points = Points(sample_points)
    smoothed_points = smooth_points(points, n_iterations=15, pass_band=0.1, edge_angle=15, feature_angle=60, boundary=False)
    assert smoothed_points.data.shape == points.data.shape

def test_remove_outliers(sample_points):
    points = Points(sample_points)
    filtered_points = remove_outliers(points, radius=0.1, n_neighbors=5)
    assert filtered_points.data.shape[1] == 3
