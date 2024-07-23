import vedo
import numpy as np
from napari_vedo_bridge.utils import napari_to_vedo_points, vedo_points_to_napari
from napari.layers import Points
from magicgui import widgets, magic_factory
from qtpy.QtCore import Qt


def _on_init(widget):
    label_widget = widgets.Label(value='')
    func_name = widget.label.split(' ')[0]
    label_widget.value = f'<a href=\"https://vedo.embl.es/docs/vedo/pointcloud.html#Points.{func_name}\">skimage.filters.{func_name}</a>'
    label_widget.native.setTextFormat(Qt.RichText)
    label_widget.native.setTextInteractionFlags(Qt.TextBrowserInteraction)
    label_widget.native.setOpenExternalLinks(True)
    widget.extend([label_widget])


@magic_factory(
    points={'label': 'Points'},
    boundary={'label': 'Boundary', 'widget_type': 'CheckBox'},
    widget_init=_on_init
)
def smooth_points(
        points: Points,
        n_iterations: int = 15,
        pass_band: float = 0.1,
        edge_angle: float = 15,
        feature_angle: float = 60,
        boundary: bool = False) -> Points:
    """
    Smooth the given points.

    Parameters
    ----------
    points : Points
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
    Points
        The smoothed points.
    """
    vedo_points = napari_to_vedo_points(points)
    vedo_points.smooth(
        niter=n_iterations,
        passBand=pass_band,
        edgeAngle=edge_angle,
        featureAngle=feature_angle,
        boundary=boundary)
    return vedo_points_to_napari(vedo_points)


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
