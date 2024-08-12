import numpy as np
import vedo
from .._cutter_widget import VedoCutter


# make_napari_viewer is a pytest fixture that returns a napari viewer object
def test_cutter_widget(make_napari_viewer):

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    my_widget = VedoCutter(viewer)
    viewer.window.add_dock_widget(my_widget, area='right')


def test_get_from_napari(make_napari_viewer):
    # Load the test mesh into the napari viewer
    viewer = make_napari_viewer()
    mesh = vedo.load("https://vedo.embl.es/examples/data/270.vtk")
    viewer.add_surface((mesh.vertices, np.asarray(mesh.cells)), name="test_mesh")

    vedo_cutter = VedoCutter(viewer)
    vedo_cutter.get_from_napari()

    # Assert that the mesh is loaded and displayed correctly in vedo
    assert vedo_cutter.mesh is not None

    n_layers = len(viewer.layers)
    vedo_cutter.send_to_napari()
    assert len(viewer.layers) == n_layers + 1


def test_cutters(make_napari_viewer):
    viewer = make_napari_viewer()
    mesh = vedo.load("https://vedo.embl.es/examples/data/270.vtk")
    viewer.add_surface((mesh.vertices, np.asarray(mesh.cells)), name="test_mesh")

    vedo_cutter = VedoCutter(viewer)
    vedo_cutter.get_from_napari()

    vedo_cutter.buttonGroup.buttons()[0].click()
    n_checked_buttons = len([b for b in vedo_cutter.buttonGroup.buttons() if b.isChecked()])
    assert n_checked_buttons == 1

    vedo_cutter.buttonGroup.buttons()[1].click()
    n_checked_buttons = len([b for b in vedo_cutter.buttonGroup.buttons() if b.isChecked()])
    assert n_checked_buttons == 1

    vedo_cutter.buttonGroup.buttons()[2].click()
    n_checked_buttons = len([b for b in vedo_cutter.buttonGroup.buttons() if b.isChecked()])
    assert n_checked_buttons == 1


def base_widget(make_napari_viewer):
    from napari_vedo_bridge._widgets.base_widget import BaseWidget
    viewer = make_napari_viewer()

    n_widgets = len(viewer.window._dock_widgets)

    mesh = vedo.load("https://vedo.embl.es/examples/data/270.vtk")
    viewer.add_surface((mesh.vertices, np.asarray(mesh.cells)), name="test_mesh")
    n_layers = len(viewer.layers)

    base_widget = BaseWidget(viewer)
    viewer.window.add_dock_widget(base_widget, area='right')

    assert len(viewer.window._dock_widgets) == n_widgets + 1

    base_widget.pushButton_get_from_napari.click()
    assert base_widget.mesh is not None

    base_widget.pushButton_send_back.click()
    assert len(viewer.layers) == n_layers + 1

    base_widget.pushButton_clear.click()
    assert base_widget.mesh is None

    base_widget.pushButton_show_hotkeys.click()
    assert len(viewer.window._dock_widgets) == n_widgets + 2



