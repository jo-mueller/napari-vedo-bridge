import pytest
import numpy as np
from napari_vedo_bridge._points import smooth_mls_1d, remove_outliers
from napari.layers import Points

@pytest.fixture
def sample_points():
    return Points(np.random.randn(1000, 3))

def test_smooth_points(sample_points):
    smoothed_points = smooth_mls_1d()(sample_points, factor=0.2, radius=0)
    assert smoothed_points.data.shape == sample_points.data.shape

def test_remove_outliers(sample_points):
    filtered_points = remove_outliers()(sample_points, radius=0.1, n_neighbors=5)
    assert filtered_points.data.shape[1] == 3
