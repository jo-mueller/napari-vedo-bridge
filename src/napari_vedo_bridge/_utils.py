import vedo
import numpy as np

def napari_to_vedo_mesh(mesh: 'napari.types.SurfaceData') -> vedo.Mesh:
    vertices, faces = mesh
    return vedo.Mesh([vertices, faces])

def vedo_mesh_to_napari(mesh: vedo.Mesh) -> 'napari.types.SurfaceData':
    return mesh.vertices, np.asarray(mesh.cells, dtype=int)

def napari_to_vedo_points(points: 'napari.types.PointsData') -> vedo.Points:
    return vedo.Points(points)

def vedo_points_to_napari(points: vedo.Points) -> 'napari.types.PointsData':
    return points.vertices
