import vedo
import numpy as np
from napari_vedo_bridge.utils import napari_to_vedo_mesh, vedo_mesh_to_napari
from napari.layers import Surface, Vectors, Points, Image, Labels
from napari.types import LayerDataTuple
from typing import Tuple, List, Union

from magicgui import widgets, magic_factory
from qtpy.QtCore import Qt


def _on_init(widget):
    label_widget = widgets.Label(value='')
    func_name = widget.label.split(' ')[0]
    label_widget.value = f'<a href=\"https://vedo.embl.es/docs/vedo/mesh.html#Mesh.{func_name}\" style=\"color: white;\">vedo.Mesh.{func_name}</a>'
    label_widget.native.setTextFormat(Qt.RichText)
    label_widget.native.setTextInteractionFlags(Qt.TextBrowserInteraction)
    label_widget.native.setOpenExternalLinks(True)
    widget.extend([label_widget])


@magic_factory(
    surface={'label': 'Surface'},
    widget_init=_on_init
)
def compute_normals(
        surface: Surface) -> Vectors:
    """
    Compute normals for the given mesh.

    Parameters
    ----------
    surface : Surface
        The input mesh.

    Returns
    -------
    Vectors
        The mesh with computed normals.
    """
    vedo_mesh = napari_to_vedo_mesh(surface)
    vedo_mesh.compute_normals()

    vedo_mesh.compute_normals()
    points = vedo_mesh.vertices
    directions = vedo_mesh.vertex_normals

    napari_vectors = np.stack([points, directions], axis=1)
    return Vectors(napari_vectors)


@magic_factory(
    surface={'label': 'Surface'},
    fraction={'label': 'Fraction', 'widget_type': 'FloatSlider', 'min': 0.1, 'max': 1.0, 'step': 0.1},
    widget_init=_on_init
)
def shrink(
        surface: Surface,
        fraction: float = 0.9) -> Surface:
    """
    Shrink the given mesh.

    Parameters
    ----------
    surface : Surface
        The input mesh.
    fraction : float, optional
        The fraction to shrink the mesh, by default 0.9.

    Returns
    -------
    Surface
        The shrunk surface.
    """
    vedo_mesh = napari_to_vedo_mesh(surface)
    vedo_mesh.shrink(fraction=fraction)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    surface={'label': 'Surface'},
    widget_init=_on_init
)
def subdivide(
        surface: Surface,
        n_iterations: int = 1) -> Surface:
    """
    Subdivide the given surface.

    Parameters
    ----------
    surface : Surface
        The input mesh.
    n_iterations : int, optional
        The number of subdivisions, by default 1.

    Returns
    -------
    Surface
        The subdivided mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(surface)
    vedo_mesh.subdivide(n=n_iterations)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    surface={'label': 'Surface'},
    fraction={'label': 'Fraction', 'min': 0.1, 'max': 1.0, 'step': 0.01},
    n_vertices={'label': 'Number of Vertices', 'min': 0, 'max': 100000, 'step': 100, 'nullable': True},
    widget_init=_on_init
)
def decimate(
        surface: Surface,
        fraction: float = 0.5,
        n_vertices: int = 0) -> Surface:
    """
    Decimate the given surface.

    Parameters
    ----------
    surface : Surface
        The input surface.
    fraction : float, optional
        The fraction to decimate the mesh, by default 0.5.
    n : int, optional
        The target number of vertices. Ignored if 0, by default 0.

    Returns
    -------
    Surface
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(surface)
    vedo_mesh.decimate(fraction=fraction, n=n_vertices)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    surface={'label': 'Surface'},
    fraction={'label': 'Fraction', 'min': 0.1, 'max': 1.0, 'step': 0.01},
    n_vertices={'label': 'Number of Vertices', 'min': 0, 'max': 65535, 'step': 1, 'nullable': True},
    widget_init=_on_init
)
def decimate_pro(
        surface: Surface,
        fraction: float = 0.5,
        n_vertices: int = 0) -> Surface:
    """
    Decimate the given mesh using the Pro algorithm.

    Parameters
    ----------
    surface : Surface
        The input surface.
    fraction : float, optional
        The reduction factor, by default 0.5.
    n_vertices : int, optional
        The target number of vertices. Ignored if 0, by default 0.

    Returns
    -------
    Surface
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(surface)
    vedo_mesh.decimate_pro(fraction=fraction, n=n_vertices)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    surface={'label': 'Surface'},
    divisions={'label': 'Divisions'},
    widget_init=_on_init
)
def decimate_binned(
        surface: Surface,
        divisions: Tuple[int, int, int]) -> Surface:
    """
    Decimate the given mesh using the Binned algorithm.

    Parameters
    ----------
    surface : Surface
        The input surface.
    divisions : Tuple[int, int, int]
        The number of divisions along the x, y, and z axes.

    Returns
    -------
    Surface
        The decimated mesh.
    """
    vedo_mesh = napari_to_vedo_mesh(surface)
    vedo_mesh.decimate_binned(divisions=divisions)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    surface={'label': 'Surface'},
    widget_init=_on_init
)
def smooth(
        surface: Surface,
        n_iterations: int = 15,
        pass_band: float = 0.1,
        edge_angle: int = 15,
        feature_angle: int = 60,
        boundary: bool = False) -> Surface:
    """
    Smooth the given surface.

    Parameters
    ----------
    surface : Surface
        The input surface.
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
    vedo_mesh = napari_to_vedo_mesh(surface)
    vedo_mesh.smooth(
        niter=n_iterations,
        pass_band=pass_band,
        edge_angle=edge_angle,
        feature_angle=feature_angle,
        boundary=boundary)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    surface={'label': 'Surface'},
    size={'label': 'Size', 'min': 0.1, 'max': 65535, 'step': 0.1},
    widget_init=_on_init
)
def fill_holes(
        surface: Surface,
        size: float = 1000) -> Surface:
    """
    Fill holes in the given surface.

    Parameters
    ----------
    surface : Surface
        The input surface.
    size : float, optional
        The max size of the holes to fill, by default 1000.

    Returns
    -------
    Surface
        The mesh with filled holes.
    """
    vedo_mesh = napari_to_vedo_mesh(surface)
    vedo_mesh.fill_holes(size=size)
    return vedo_mesh_to_napari(vedo_mesh)


@magic_factory(
    surface={'label': 'Surface'},
    widget_init=_on_init
)    
def split(surface: Surface) -> List[LayerDataTuple]:
    """
    Split the given surface into connected components.

    Parameters
    ----------
    surface : Surface
        The input surface.

    Returns
    -------
    List[Surface]
        The connected components of the mesh
    """
    vedo_mesh = napari_to_vedo_mesh(surface)
    split_meshes_v = list(vedo_mesh.split())
    split_meshes = [
        (vedo_mesh_to_napari(m), {}, 'surface')
        for m in split_meshes_v
        ]
    return split_meshes


@magic_factory(
    surface={'label': 'Surface'},
    widget_init=_on_init
)
def extract_largest_region(
        surface: Surface
        ) -> Surface:
    """
    Extract the largest region from the given surface.

    Parameters
    ----------
    surface : Surface
        The input surface.

    Returns
    -------
    Surface
        The largest region of the surface.
    """
    vedo_mesh = napari_to_vedo_mesh(surface)
    largest_region = vedo_mesh.extract_largest_region()
    return vedo_mesh_to_napari(largest_region)


@magic_factory(
    surface={'label': 'Surface'},
    reference_image={'label': 'Reference Image'},
    widget_init=_on_init
)
def binarize(
        surface: Surface,
        reference_image: Union[Image, Labels, None] = None
        ) -> Labels:
    """
    Binarize the given surface.

    Parameters
    ----------
    surface : Surface
        The input surface.
    reference_image : Union[napari.types.ImageData, napari.types.LabelsData]
        The reference image or labels from which to get the dimensions of the 
        binarized mesh

    Returns
    -------
    Surface
        The binarized mesh.
    """
    if reference_image is None:
        target_dimensions = None
    else:
        target_dimensions = reference_image.data.shape

    vedo_mesh = napari_to_vedo_mesh(surface)
    binarized = vedo_mesh.binarize(dims=target_dimensions).tonumpy()
    return Labels(binarized)
