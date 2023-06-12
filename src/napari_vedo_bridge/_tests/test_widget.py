import numpy as np


# make_napari_viewer is a pytest fixture that returns a napari viewer object
def test_cutter_widget(make_napari_viewer):
    from .._cutter_widget import VedoCutter
    
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()
    
    # create our widget, passing in the viewer
    my_widget = VedoCutter(viewer)
    viewer.window.add_dock_widget(my_widget, area='right')