import vedo
import numpy as np
from napari_vedo_bridge.utils import napari_to_vedo_mesh, vedo_mesh_to_napari

def compute_normals(mesh: 'napari.types.SurfaceData') -> 'napari.types.SurfaceData':
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
    return vedo_mesh_to_napari(vedo_mesh)

def shrink(mesh: 'napari.types.SurfaceData', fraction: float = 0.9) -> 'napari.types.SurfaceData':
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

def join(meshes: list['napari.types.SurfaceData']) -> 'napari.types.SurfaceData':
    """
    Join the given meshes.

    Parameters
    ----------
    meshes : list[napari.types.SurfaceData]
        The input meshes.

    Returns
    -------
    napari.types.SurfaceData
        The joined mesh.
    """
    vedo_meshes = [napari_to_vedo_mesh(mesh) for mesh in meshes]
    joined_mesh = vedo.Mesh.join(*vedo_meshes)
    return vedo_mesh_to_napari(joined_mesh)

def subdivide(mesh: 'napari.types.SurfaceData', n: int = 1) -> 'napari.types.SurfaceData':
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

def decimate(mesh: 'napari.types.SurfaceData', fraction: float = 0.5) -> 'napari.types.SurfaceData':
    """
    Decimate the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    fraction : float, optional
        The fraction to decimate the mesh, by default 0.5.

    Returns
    -------
    napari.types.SurfaceData
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.decimate(fraction=fraction)
    return vedo_mesh_to_napari(vedo_mesh)

def decimate_pro(mesh: 'napari.types.SurfaceData', reduction: float = 0.5) -> 'napari.types.SurfaceData':
    """
    Decimate the given mesh using the Pro algorithm.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    reduction : float, optional
        The reduction factor, by default 0.5.

    Returns
    -------
    napari.types.SurfaceData
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.decimate_pro(reduction=reduction)
    return vedo_mesh_to_napari(vedo_mesh)

def decimate_binned(mesh: 'napari.types.SurfaceData', bins: int = 100) -> 'napari.types.SurfaceData':
    """
    Decimate the given mesh using the Binned algorithm.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    bins : int, optional
        The number of bins, by default 100.

    Returns
    -------
    napari.types.SurfaceData
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.decimate_binned(bins=bins)
    return vedo_mesh_to_napari(vedo_mesh)

def smooth(mesh: 'napari.types.SurfaceData', n_iterations: int = 15, pass_band: float = 0.1, edge_angle: float = 15, feature_angle: float = 60, boundary: bool = False) -> 'napari.types.SurfaceData':
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
    vedo_mesh.smooth(niter=n_iterations, passBand=pass_band, edgeAngle=edge_angle, featureAngle=feature_angle, boundary=boundary)
    return vedo_mesh_to_napari(vedo_mesh)

def fill_holes(mesh: 'napari.types.SurfaceData', size: float = 1000) -> 'napari.types.SurfaceData':
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

def inside_points(mesh: 'napari.types.SurfaceData', points: 'napari.types.PointsData') -> 'napari.types.PointsData':
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

def extrude(mesh: 'napari.types.SurfaceData', zshift: float = 1.0) -> 'napari.types.SurfaceData':
    """
    Extrude the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    zshift : float, optional
        The shift along the z-axis, by default 1.0.

    Returns
    -------
    napari.types.SurfaceData
        The extruded mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.extrude(zshift=zshift)
    return vedo_mesh_to_napari(vedo_mesh)

def split(mesh: 'napari.types.SurfaceData') -> list['napari.types.SurfaceData']:
    """
    Split the given mesh into connected components.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.

    Returns
    -------
    list[napari.types.SurfaceData]
        The list of connected components.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    split_meshes = vedo_mesh.split()
    return [vedo_mesh_to_napari(split_mesh) for split_mesh in split_meshes]

def extract_largest_region(mesh: 'napari.types.SurfaceData') -> 'napari.types.SurfaceData':
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

def binarize(mesh: 'napari.types.SurfaceData', threshold: float = 0.5) -> 'napari.types.SurfaceData':
    """
    Binarize the given mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input mesh.
    threshold : float, optional
        The threshold for binarization, by default 0.5.

    Returns
    -------
    napari.types.SurfaceData
        The binarized mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.binarize(threshold=threshold)
    return vedo_mesh_to_napari(vedo_mesh)
