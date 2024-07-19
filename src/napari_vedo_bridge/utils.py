import vedo
import numpy as np

def napari_to_vedo_mesh(mesh: 'napari.types.SurfaceData') -> vedo.Mesh:
    """
    Convert a napari mesh to a vedo mesh.

    Parameters
    ----------
    mesh : napari.types.SurfaceData
        The input napari mesh.

    Returns
    -------
    vedo.Mesh
        The converted vedo mesh.
    """
    vertices, faces = mesh
    return vedo.Mesh([vertices, faces])

def vedo_mesh_to_napari(mesh: vedo.Mesh) -> 'napari.types.SurfaceData':
    """
    Convert a vedo mesh to a napari mesh.

    Parameters
    ----------
    mesh : vedo.Mesh
        The input vedo mesh.

    Returns
    -------
    napari.types.SurfaceData
        The converted napari mesh.
    """
    return mesh.vertices, np.asarray(mesh.cells, dtype=int)

def napari_to_vedo_points(points: 'napari.types.PointsData') -> vedo.Points:
    """
    Convert napari points to vedo points.

    Parameters
    ----------
    points : napari.types.PointsData
        The input napari points.

    Returns
    -------
    vedo.Points
        The converted vedo points.
    """
    return vedo.Points(points)

def vedo_points_to_napari(points: vedo.Points) -> 'napari.types.PointsData':
    """
    Convert vedo points to napari points.

    Parameters
    ----------
    points : vedo.Points
        The input vedo points.

    Returns
    -------
    napari.types.PointsData
        The converted napari points.
    """
    return points.points()

def napari_to_vedo_vectors(vectors: 'napari.types.VectorsData') -> vedo.Line:
    """
    Convert napari vectors to vedo vectors.

    Parameters
    ----------
    vectors : napari.types.VectorsData
        The input napari vectors.

    Returns
    -------
    vedo.Lines
        The converted vedo vectors.
    """
    return vedo.Line(vectors[:, 0], vectors[:, 1])

def vedo_vectors_to_napari(vectors: vedo.Lines) -> 'napari.types.VectorsData':
    """
    Convert vedo vectors to napari vectors.

    Parameters
    ----------
    vectors : vedo.Lines
        The input vedo vectors.

    Returns
    -------
    napari.types.VectorsData
        The converted napari vectors.
    """
    return np.stack([vectors.points(0), vectors.points(1)], axis=1)
