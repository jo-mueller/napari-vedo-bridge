import pytest
import numpy as np
from napari_vedo_bridge._points import smooth_mls_1d, smooth_mls_2d, remove_outliers
from napari.layers import Points


@pytest.fixture
def sample_points():
    return Points(np.random.randn(1000, 3))


def test_smooth_points(sample_points):
    smoothed_points = smooth_mls_1d()(sample_points, factor=0.2, radius=0)
    assert smoothed_points.data.shape == sample_points.data.shape

def smooth_points_2d(sample_points):
    smoothed_points = smooth_mls_2d()(sample_points, factor=0.2, radius=0)
    assert smoothed_points.data.shape == sample_points.data.shape

def test_remove_outliers(sample_points):
    # add a far-out point
    sample_points.data[0] = [100, 100, 100]

    filtered_points = remove_outliers()(sample_points, radius=2.5, n_neighbors=1)
    assert filtered_points.data.shape[0] == sample_points.data.shape[0] - 1
