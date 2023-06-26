import numpy as np
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
    import vedo
    viewer = make_napari_viewer()
    mesh = vedo.load("https://vedo.embl.es/examples/data/270.vtk")
    viewer.add_surface((mesh.points(), np.asarray(mesh.faces())), name="test_mesh")

    vedo_cutter = VedoCutter(viewer)
    vedo_cutter.get_from_napari()

    # Assert that the mesh is loaded and displayed correctly in vedo
    assert vedo_cutter.mesh is not None

    n_layers = len(viewer.layers)
    vedo_cutter.send_to_napari()
    assert len(viewer.layers) == n_layers + 1


def test_cutters(make_napari_viewer):
    import vedo
    viewer = make_napari_viewer()
    mesh = vedo.load("https://vedo.embl.es/examples/data/270.vtk")
    viewer.add_surface((mesh.points(), np.asarray(mesh.faces())), name="test_mesh")

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