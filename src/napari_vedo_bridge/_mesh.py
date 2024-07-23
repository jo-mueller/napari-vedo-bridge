import vedo
import numpy as np
from napari_vedo_bridge.utils import napari_to_vedo_mesh, vedo_mesh_to_napari
from napari.layers import Surface, Vectors, Points
from typing import Tuple, List, Union

from magicgui import widgets, magic_factory
from qtpy.QtCore import Qt


def _on_init(widget):
    label_widget = widgets.Label(value='')
    func_name = widget.label.split(' ')[0]
    label_widget.value = f'<a href=\"https://vedo.embl.es/docs/vedo/mesh.html#Mesh.{func_name}\">skimage.filters.{func_name}</a>'
    label_widget.native.setTextFormat(Qt.RichText)
    label_widget.native.setTextInteractionFlags(Qt.TextBrowserInteraction)
    label_widget.native.setOpenExternalLinks(True)
    widget.extend([label_widget])


@magic_factory(
    mesh={'label': 'Surface'},
    widget_init=_on_init
)
def compute_normals(
        mesh: Surface) -> Vectors:
    """
    Compute normals for the given mesh.

    Parameters
    ----------
    mesh : Surface
        The input mesh.

    Returns
    -------
    Vectors
        The mesh with computed normals.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.compute_normals()

    normals = vedo_mesh.normals()
    points = vedo_mesh.vertices

    napari_vectors = np.stack([points, normals], axis=1)
    return napari_vectors


@magic_factory(
    mesh={'label': 'Surface'},
    fraction={'label': 'Fraction', 'widget_type': 'FloatSlider', 'min': 0.1, 'max': 1.0, 'step': 0.1},
    widget_init=_on_init
)
def shrink(
        mesh: Surface,
        fraction: float = 0.9) -> Surface:
    """
    Shrink the given mesh.

    Parameters
    ----------
    mesh : Surface
        The input mesh.
    fraction : float, optional
        The fraction to shrink the mesh, by default 0.9.

    Returns
    -------
    Surface
        The shrunk mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.shrink(fraction=fraction)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    mesh={'label': 'Surface'},
    widget_init=_on_init
)
def subdivide(
        mesh: Surface,
        n_iterations: int = 1) -> Surface:
    """
    Subdivide the given mesh.

    Parameters
    ----------
    mesh : Surface
        The input mesh.
    n_iterations : int, optional
        The number of subdivisions, by default 1.

    Returns
    -------
    Surface
        The subdivided mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.subdivide(n=n_iterations)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    mesh={'label': 'Surface'},
    fraction={'label': 'Fraction', 'widget_type': 'FloatSlider', 'min': 0.1, 'max': 1.0, 'step': 0.01},
    n_vertices={'label': 'Number of Vertices', 'widget_type': 'IntSlider', 'min': 0, 'max': 100000, 'step': 100},
    widget_init=_on_init
)
def decimate(
        mesh: Surface,
        fraction: float = 0.5,
        n_vertices: int = 0) -> Surface:
    """
    Decimate the given mesh.

    Parameters
    ----------
    mesh : Surface
        The input mesh.
    fraction : float, optional
        The fraction to decimate the mesh, by default 0.5.
    n : int, optional
        The target number of vertices. Ignored if 0, by default 0.

    Returns
    -------
    Surface
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.decimate(fraction=fraction, n=n_vertices)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    mesh={'label': 'Surface'},
    divisions={'label': 'Divisions', 'widget_type': 'TupleSlider', 'min': 1, 'max': 100, 'step': 1},
    widget_init=_on_init
)
def decimate_pro(
        mesh: Surface,
        fraction: float = 0.5,
        n_vertices: int = 0) -> Surface:
    """
    Decimate the given mesh using the Pro algorithm.

    Parameters
    ----------
    mesh : Surface
        The input mesh.
    fraction : float, optional
        The reduction factor, by default 0.5.
    n_vertices : int, optional
        The target number of vertices. Ignored if 0, by default 0.

    Returns
    -------
    Surface
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.decimate_pro(fraction=fraction, n=n_vertices)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    mesh={'label': 'Surface'},
    divisions={'label': 'Divisions', 'widget_type': 'TupleSlider', 'min': 1, 'max': 100, 'step': 1},
    widget_init=_on_init
)
def decimate_binned(
        mesh: Surface,
        divisions: Tuple[int, int, int]) -> Surface:
    """
    Decimate the given mesh using the Binned algorithm.

    Parameters
    ----------
    mesh : Surface
        The input mesh.
    divisions : Tuple[int, int, int]
        The number of divisions along the x, y, and z axes.

    Returns
    -------
    Surface
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.decimate_binned(divisions=divisions)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    mesh={'label': 'Surface'},
    widget_init=_on_init
)
def smooth(
        mesh: Surface,
        n_iterations: int = 15,
        pass_band: float = 0.1,
        edge_angle: float = 15,
        feature_angle: float = 60,
        boundary: bool = False) -> Surface:
    """
    Smooth the given mesh.

    Parameters
    ----------
    mesh : Surface
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
    Surface
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


@magic_factory(
    mesh={'label': 'Surface'},
    widget_init=_on_init
)
def fill_holes(
        mesh: Surface,
        size: float = 1000) -> Surface:
    """
    Fill holes in the given mesh.

    Parameters
    ----------
    mesh : Surface
        The input mesh.
    size : float, optional
        The max size of the holes to fill, by default 1000.

    Returns
    -------
    Surface
        The mesh with filled holes.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.fill_holes(size=size)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    mesh={'label': 'Surface'},
    points={'label': 'Points'},
    widget_init=_on_init
)
def inside_points(
        mesh: Surface,
        points: Points
        ) -> Points:
    """
    Get the points inside the given mesh.

    Parameters
    ----------
    mesh : Surface
        The input mesh.
    points : Points
        The input points.

    Returns
    -------
    Points
        The points inside the mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_points = vedo.Points(points)
    inside_points = vedo_mesh.inside_points(vedo_points)
    return inside_points.vertices


@magic_factory(
    mesh={'label': 'Surface'},
    widget_init=_on_init
)    
def split(mesh: Surface) -> List[Surface]:
    """
    Split the given mesh into connected components.

    Parameters
    ----------
    mesh : Surface
        The input mesh.

    Returns
    -------
    List[Surface]
        The connected components of the mesh
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    split_meshes = vedo_mesh.split()
    split_meshes = [
        (vedo_mesh_to_napari(split_mesh), {}, 'surface')
        for split_mesh in split_meshes
        ]
    return split_meshes


@magic_factory(
    mesh={'label': 'Surface'},
    widget_init=_on_init
)
def extract_largest_region(
        mesh: Surface
        ) -> Surface:
    """
    Extract the largest region from the given mesh.

    Parameters
    ----------
    mesh : Surface
        The input mesh.

    Returns
    -------
    Surface
        The largest region of the mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(mesh)
    largest_region = vedo_mesh.extract_largest_region()
    return vedo_mesh_to_napari(largest_region)


@magic_factory(
    mesh={'label': 'Surface'},
    reference_image={'label': 'Reference Image'},
    widget_init=_on_init
)
def binarize(
        mesh: Surface,
        reference_image: Union['napari.types.ImageData', 'napari.types.LabelsData']
        ) -> Surface:
    """
    Binarize the given mesh.

    Parameters
    ----------
    mesh : Surface
        The input mesh.
    reference_image : Union[napari.types.ImageData, napari.types.LabelsData]
        The reference image or labels from which to get the dimensions of the 
        binarized mesh

    Returns
    -------
    Surface
        The binarized mesh.
    """

    target_dimensions = reference_image.shape
    vedo_mesh = napari_to_vedo_mesh(mesh)
    vedo_mesh.binarize(dims=target_dimensions)
    return vedo_mesh_to_napari(vedo_mesh)
