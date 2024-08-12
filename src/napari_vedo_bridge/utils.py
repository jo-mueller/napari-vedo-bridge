import vedo
import numpy as np
from napari.layers import Surface, Points, Vectors
import vedo.pointcloud

def napari_to_vedo_mesh(surface: Surface) -> vedo.Mesh:
    """
    Convert a napari mesh to a vedo mesh.

    Parameters
    ----------
    surface : Surface
        The input napari mesh.

    Returns
    -------
    vedo.Mesh
        The converted vedo mesh.
    """
    vertices, faces = surface.data[0], surface.data[1]
    return vedo.Mesh([vertices, faces])

def vedo_mesh_to_napari(mesh: vedo.Mesh) -> Surface:
    """
    Convert a vedo mesh to a napari mesh.

    Parameters
    ----------
    mesh : vedo.Mesh
        The input vedo mesh.

    Returns
    -------
    Surface
        The converted napari mesh.
    """
    return Surface((mesh.vertices, np.asarray(mesh.cells, dtype=int)))

def napari_to_vedo_points(points: Points) -> vedo.Points:
    """
    Convert napari points to vedo points.

    Parameters
    ----------
    points : Points
        The input napari points.

    Returns
    -------
    vedo.Points
        The converted vedo points.
    """
    return vedo.pointcloud.Points(points.data)

def vedo_points_to_napari(points: vedo.Points) -> Points:
    """
    Convert vedo points to napari points.

    Parameters
    ----------
    points : vedo.Points
        The input vedo points.

    Returns
    -------
    Points
        The converted napari points.
    """
    return Points(points.vertices)

def napari_to_vedo_vectors(vectors: Vectors) -> vedo.Line:
    """
    Convert napari vectors to vedo vectors.

    Parameters
    ----------
    vectors : Vectors
        The input napari vectors.

    Returns
    -------
    vedo.Lines
        The converted vedo vectors.
    """
    return vedo.Line(vectors.data[:, 0], vectors.data[:, 1])

def vedo_vectors_to_napari(vectors: vedo.Lines) -> Vectors:
    """
    Convert vedo vectors to napari vectors.

    Parameters
    ----------
    vectors : vedo.Lines
        The input vedo vectors.

    Returns
    -------
    Vectors
        The converted napari vectors.
    """
    return Vectors(np.stack([vectors.points(0), vectors.points(1)], axis=1))
