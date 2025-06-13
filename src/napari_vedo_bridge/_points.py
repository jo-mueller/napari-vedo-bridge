import vedo
import numpy as np
from napari_vedo_bridge.utils import napari_to_vedo_points, vedo_points_to_napari
from napari.layers import Points
from magicgui import widgets, magic_factory
from qtpy.QtCore import Qt


def _on_init(widget):
    label_widget = widgets.Label(value='')
    func_name = widget.label.split(' ')[0]
    label_widget.value = f'<a href=\"https://vedo.embl.es/docs/vedo/pointcloud.html#Points.{func_name}\">vedo.Points.{func_name}</a>'
    label_widget.native.setTextFormat(Qt.RichText)
    label_widget.native.setTextInteractionFlags(Qt.TextBrowserInteraction)
    label_widget.native.setOpenExternalLinks(True)
    widget.extend([label_widget])


@magic_factory(
    points={'label': 'Points'},
    widget_init=_on_init
)
def smooth_mls_1d(
        points: Points,
        factor: float = 0.2,
        radius: float = 0) -> Points:
    """
    Smooth the given points.

    Parameters
    ----------
    points : Points
        The input points.
    factor : float, optional
        The smoothing factor, by default 0.2.
    radius : float, optional
        The radius for smoothing, by default 0.

    Returns
    -------
    Points
        The smoothed points.
    """
    vedo_points = napari_to_vedo_points(points)
    vedo_points.smooth_mls_1d(
        f=factor,
        radius=radius)
    return vedo_points_to_napari(vedo_points)

@magic_factory(
    points={'label': 'Points'},
    widget_init=_on_init
)
def smooth_mls_2d(
        points: Points,
        factor: float = 0.2,
        radius: Optional[float] = 0) -> Points:
    """
    Smooth the given points in 2D.

    Parameters
    ----------
    points : Points
        The input points.
    factor : float, optional
        The smoothing factor, by default 0.2.
    radius : float, optional
        The radius for smoothing, by default 0.

    Returns
    -------
    Points
        The smoothed points.
    """
    vedo_points = napari_to_vedo_points(points)
    vedo_points.smooth_mls_2d(
        f=factor,
        radius=radius)
    new_points = vedo_points_to_napari(vedo_points)
    new_points.scale = points.scale
    new_points.size = points.size
    new_points.translate = points.translate
    return new_points

@magic_factory(
    points={'label': 'Points'},
    radius={'label': 'Radius'},
    n_neighbors={'label': 'Number of Neighbors'},
    widget_init=_on_init
)
def remove_outliers(
        points: Points,
        radius: float = 0.1,
        n_neighbors: int = 5) -> Points:
    """
    Remove outliers from the given points.

    Parameters
    ----------
    points : Points
        The input points.
    radius : float, optional
        The radius for outlier detection, by default 0.1.
    n_neighbors : int, optional
        The number of neighbors for outlier detection, by default 5.

    Returns
    -------
    Points
        The points with outliers removed.
    """
    vedo_points = napari_to_vedo_points(points)
    filtered_points = vedo_points.remove_outliers(
        radius=radius,
        neighbors=n_neighbors)
    return vedo_points_to_napari(filtered_points)
