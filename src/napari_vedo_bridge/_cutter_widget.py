import os
from pathlib import Path
from qtpy import uic
from qtpy.QtWidgets import QWidget
import numpy as np
# from magicgui import magicgui

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter, Text2D, Mesh, Axes, BoxCutter, dataurl
from vedo import __version__ as _vedo_version


class VedoCutter(QWidget):

    def __init__(self, napari_viewer=None):
        super().__init__()

        self.mesh = None

        self.cutter_widget = None
    
        self.vedo_message = Text2D(font='Calco', c='white')
        self.vedo_axes = None

        self.napari_viewer = napari_viewer
        uic.loadUi(os.path.join(Path(__file__).parent, "./vedo_extension.ui"), self)

        self.vtkWidget = QVTKRenderWindowInteractor()
        self.layout().insertWidget(0, self.vtkWidget)

        self.pushButton_send_back.clicked.connect(self.send_to_napari)
        self.pushButton_get_from_napari.clicked.connect(self.get_from_napari)

        self.pushButton_box_cutter.clicked.connect(self.box_cutter_tool)
        self.pushButton_sphere_cutter.clicked.connect(self.sphere_cutter_tool)
        self.pushButton_plane_cutter.clicked.connect(self.plane_cutter_tool)

        self.plt = Plotter(qt_widget=self.vtkWidget, bg='bb', interactive=False)
        self.plt += self.vedo_message
        self.plt += Text2D(
            "vedo "+_vedo_version,
            pos='top-right',
            font='Calco',
            c='k5',
            s=0.5,
        )
        self.plt.show()


    def get_from_napari(self):
        """
        Get the currently selected layer from napari and display it in vedo
        """        
        if self.cutter_widget:
            self.plt.remove(self.cutter_widget)
        self.plt.remove(self.mesh, self.vedo_axes)

        self.currently_selected_layer = self.napari_viewer.layers.selection.active
        if self.currently_selected_layer:
            points = self.currently_selected_layer.data[0].astype(float)
            faces = self.currently_selected_layer.data[1].astype(int)
            scalars = self.currently_selected_layer.data[2]
            self.mesh = Mesh([points, faces])  # only vertices and faces       
            if len(scalars) > 0:
                self.mesh.pointdata['scalars'] = scalars
        else:
            # TEST mesh
            self.mesh = Mesh(dataurl+"mouse_brain.stl")

        # self.mesh.triangulate()
        self.mesh.c("yellow6").backcolor("purple6").lighting("shiny")

        try:
            if self.currently_selected_layer.name:
                self.vedo_message.text(f"Mesh: {self.currently_selected_layer.name}")
        except AttributeError:
            self.vedo_message.text("Test Mesh (mouse brain)")

        self.pushButton_box_cutter.setChecked(False)
        self.pushButton_sphere_cutter.setChecked(False)
        self.pushButton_plane_cutter.setChecked(False)

        self.vedo_axes = Axes(self.mesh, c='white')
        self.plt.add(self.vedo_axes, self.mesh)
        self.plt.reset_camera().render()

    def send_to_napari(self):
        """
        Send the currently displayed mesh in vedo to napari
        """
        # retrieve from plotter
        mesh_tuple = (self.mesh.points(), np.asarray(self.mesh.faces()))

        if len(mesh_tuple[0]) == 0:
            self.vedo_message.text("No mesh to send to napari!")
            self.plt.render()
            return

        self.napari_viewer.add_surface(mesh_tuple)

    def box_cutter_tool(self):
        """
        Add a box cutter tool to the vedo plotter
        """
        if not self.mesh:
            self.vedo_message.text("Please load a mesh first")
            self.plt.render()
            return

        # remove old cutter
        if self.cutter_widget is not None:
            self.plt.remove(self.cutter_widget)
            self.cutter_widget = None
            self.vedo_message.text("cutter removed")

        # add new cutter
        if self.pushButton_box_cutter.isChecked():
            self.cutter_widget = BoxCutter(
                self.mesh,
                invert=self.checkBox_invert.isChecked(),
            )
            self.plt.add(self.cutter_widget)
            self.vedo_message.text(
                "Press r to reset the cutter\n"
                'Press spacebar to toggle the cutter on/off\n'
                'Press i to invert the selection\n',
            )
        
        self.plt.render()

    def plane_cutter_tool(self):
        """
        Add a plane cutter tool to the vedo plotter
        """
        pass

    def sphere_cutter_tool(self):
        """
        Add a sphere cutter tool to the vedo plotter
        """
        pass