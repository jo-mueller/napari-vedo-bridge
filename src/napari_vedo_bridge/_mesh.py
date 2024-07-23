import vedo
import numpy as np
from napari_vedo_bridge.utils import napari_to_vedo_mesh, vedo_mesh_to_napari

from typing import Tuple, List, Union


def compute_normals(
        mesh: 'napari.types.SurfaceData') -> 'napari.types.VectorsData':
    """
    Compute normals for the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.

    Returns
    -------
    napari.types.SurfaceData
        The mesh with computed normals.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.compute_normals()

    normals = vedo_mesh.normals()
    points = vedo_mesh.vertices

    napari_vectors = np.stack([points, normals], axis=1)
    return napari_vectors


def shrink(
        mesh: 'napari.types.SurfaceData',
        fraction: float = 0.9) -> 'napari.types.SurfaceData':
    """
    Shrink the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    fraction : float, optional
        The fraction to shrink the mesh, by default 0.9.

    Returns
    -------
    napari.types.SurfaceData
        The shrunk mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.shrink(fraction=fraction)
    return vedo_mesh_to_napari(vedo_mesh)


def subdivide(
        mesh: 'napari.types.SurfaceData',
        n: int = 1) -> 'napari.types.SurfaceData':
    """
    Subdivide the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    n : int, optional
        The number of subdivisions, by default 1.

    Returns
    -------
    napari.types.SurfaceData
        The subdivided mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.subdivide(n=n)
    return vedo_mesh_to_napari(vedo_mesh)


def decimate(
        mesh: 'napari.types.SurfaceData',
        fraction: float = 0.5,
        n_vertices: int = 0) -> 'napari.types.SurfaceData':
    """
    Decimate the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    fraction : float, optional
        The fraction to decimate the mesh, by default 0.5.
    n : int, optional
        The target number of vertices. Ignored if 0, by default 0.

    Returns
    -------
    napari.types.SurfaceData
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.decimate(fraction=fraction, n=n_vertices)
    return vedo_mesh_to_napari(vedo_mesh)


def decimate_pro(
        mesh: 'napari.types.SurfaceData',
        fraction: float = 0.5,
        n_vertices: int = 0) -> 'napari.types.SurfaceData':
    """
    Decimate the given mesh using the Pro algorithm.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    fraction : float, optional
        The reduction factor, by default 0.5.
    n_vertices : int, optional
        The target number of vertices. Ignored if 0, by default 0.

    Returns
    -------
    napari.types.SurfaceData
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.decimate_pro(fraction=fraction, n=n_vertices)
    return vedo_mesh_to_napari(vedo_mesh)


def decimate_binned(
        mesh: 'napari.types.SurfaceData',
        divisions: Tuple[int, int, int]) -> 'napari.types.SurfaceData':
    """
    Decimate the given mesh using the Binned algorithm.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    divisions : Tuple[int, int, int]
        The number of divisions along the x, y, and z axes.

    Returns
    -------
    napari.types.SurfaceData
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.decimate_binned(divisions=divisions)
    return vedo_mesh_to_napari(vedo_mesh)


def smooth(
        mesh: 'napari.types.SurfaceData',
        n_iterations: int = 15,
        pass_band: float = 0.1,
        edge_angle: float = 15,
        feature_angle: float = 60,
        boundary: bool = False) -> 'napari.types.SurfaceData':
    """
    Smooth the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
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
    napari.types.SurfaceData
        The smoothed mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.smooth(
        niter=n_iterations,
        passBand=pass_band,
        edgeAngle=edge_angle,
        featureAngle=feature_angle,
        boundary=boundary)
    return vedo_mesh_to_napari(vedo_mesh)


def fill_holes(
        mesh: 'napari.types.SurfaceData',
        size: float = 1000) -> 'napari.types.SurfaceData':
    """
    Fill holes in the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    size : float, optional
        The maximum size of the holes to fill, by default 1000.

    Returns
    -------
    napari.types.SurfaceData
        The mesh with filled holes.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.fill_holes(size=size)
    return vedo_mesh_to_napari(vedo_mesh)


def inside_points(
        mesh: 'napari.types.SurfaceData',
        points: 'napari.types.PointsData'
        ) -> 'napari.types.PointsData':
    """
    Get the points inside the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    points : napari.types.PointsData
        The input points.

    Returns
    -------
    napari.types.PointsData
        The points inside the mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_points = vedo.Points(points)
    inside_points = vedo_mesh.inside_points(vedo_points)
    return inside_points.points()


def split(mesh: 'napari.types.SurfaceData') -> List['napari.types.LayerDataTuple']:
    """
    Split the given mesh into connected components.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.

    Returns
    -------
    List[napari.types.LayerDataTuple]
        The connected components of the mesh
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    split_meshes = vedo_mesh.split()
    split_meshes = [
        (vedo_mesh_to_napari(split_mesh), {}, 'surface')
        for split_mesh in split_meshes
        ]
    return split_meshes


def extract_largest_region(
        mesh: 'napari.types.SurfaceData'
        ) -> 'napari.types.SurfaceData':
    """
    Extract the largest region from the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.

    Returns
    -------
    napari.types.SurfaceData
        The largest region of the mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    largest_region = vedo_mesh.extract_largest_region()
    return vedo_mesh_to_napari(largest_region)


def binarize(
        mesh: 'napari.types.SurfaceData',
        reference_image: Union['napari.types.ImageData', 'napari.types.LabelsData']
        ) -> 'napari.types.SurfaceData':
    """
    Binarize the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    reference_image : Union[napari.types.ImageData, napari.types.LabelsData]
        The reference image or labels from which to get the dimensions of the 
        binarized mesh

    Returns
    -------
    napari.types.SurfaceData
        The binarized mesh.
    """

    target_dimensions = reference_image.shape
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.binarize(dims=target_dimensions)
    return vedo_mesh_to_napari(vedo_mesh)
