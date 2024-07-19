import vedo
import numpy as np
from napari_vedo_bridge.utils import napari_to_vedo_points, vedo_points_to_napari

def smooth_points(points: 'napari.types.PointsData', n_iterations: int = 15, pass_band: float = 0.1, edge_angle: float = 15, feature_angle: float = 60, boundary: bool = False) -> 'napari.types.PointsData':
    """
    Smooth the given points.

    Parameters
    ----------
    points : napari.types.PointsData
        The input points.
    n_iterations : int, optional
        The number of iterations, by default 15.
    pass_band : float, optional
        The pass band, by default 0.1.
    edge_angle : float, optional
        The edge angle, by default 15.
    feature_angle : float, optional
        The feature angle, by default 60.
    boundary : bool, optional
        Whether to smooth the boundary, by default False.

    Returns
    -------
    napari.types.PointsData
        The smoothed points.
    """
    vedo_points = napari_to_vedo_points(points)
    vedo_points.smooth(niter=n_iterations, passBand=pass_band, edgeAngle=edge_angle, featureAngle=feature_angle, boundary=boundary)
    return vedo_points_to_napari(vedo_points)

def decimate_points(points: 'napari.types.PointsData', fraction: float = 0.5) -> 'napari.types.PointsData':
    """
    Decimate the given points.

    Parameters
    ----------
    points : napari.types.PointsData
        The input points.
    fraction : float, optional
        The fraction to decimate the points, by default 0.5.

    Returns
    -------
    napari.types.PointsData
        The decimated points.
    """
    vedo_points = napari_to_vedo_points(points)
    vedo_points.decimate(fraction=fraction)
    return vedo_points_to_napari(vedo_points)

def cluster_points(points: 'napari.types.PointsData', radius: float = 0.1) -> 'napari.types.PointsData':
    """
    Cluster the given points.

    Parameters
    ----------
    points : napari.types.PointsData
        The input points.
    radius : float, optional
        The radius for clustering, by default 0.1.

    Returns
    -------
    napari.types.PointsData
        The clustered points.
    """
    vedo_points = napari_to_vedo_points(points)
    clustered_points = vedo_points.cluster(radius=radius)
    return vedo_points_to_napari(clustered_points)

def remove_outliers(points: 'napari.types.PointsData', radius: float = 0.1, neighbors: int = 5) -> 'napari.types.PointsData':
    """
    Remove outliers from the given points.

    Parameters
    ----------
    points : napari.types.PointsData
        The input points.
    radius : float, optional
        The radius for outlier detection, by default 0.1.
    neighbors : int, optional
        The number of neighbors for outlier detection, by default 5.

    Returns
    -------
    napari.types.PointsData
        The points with outliers removed.
    """
    vedo_points = napari_to_vedo_points(points)
    filtered_points = vedo_points.remove_outliers(radius=radius, neighbors=neighbors)
    return vedo_points_to_napari(filtered_points)

def compute_normals(points: 'napari.types.PointsData', radius: float = 0.1) -> 'napari.types.PointsData':
    """
    Compute normals for the given points.

    Parameters
    ----------
    points : napari.types.PointsData
        The input points.
    radius : float, optional
        The radius for normal computation, by default 0.1.

    Returns
    -------
    napari.types.PointsData
        The points with computed normals.
    """
    vedo_points = napari_to_vedo_points(points)
    vedo_points.compute_normals(radius=radius)
    return vedo_points_to_napari(vedo_points)

def extract_largest_cluster(points: 'napari.types.PointsData') -> 'napari.types.PointsData':
    """
    Extract the largest cluster from the given points.

    Parameters
    ----------
    points : napari.types.PointsData
        The input points.

    Returns
    -------
    napari.types.PointsData
        The largest cluster of points.
    """
    vedo_points = napari_to_vedo_points(points)
    largest_cluster = vedo_points.extract_largest_cluster()
    return vedo_points_to_napari(largest_cluster)
