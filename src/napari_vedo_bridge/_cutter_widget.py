import os
from pathlib import Path
from qtpy import uic
from qtpy.QtWidgets import QWidget
import numpy as np
# from magicgui import magicgui

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter, Text2D, Mesh, Axes, BoxCutter, dataurl


class VedoCutter(QWidget):

    def __init__(self, napari_viewer=None):
        super().__init__()

        self.napari_viewer = napari_viewer
        uic.loadUi(os.path.join(Path(__file__).parent, "./vedo_extension.ui"), self)

        self.vtkWidget = QVTKRenderWindowInteractor()
        self.layout().insertWidget(0, self.vtkWidget)

        self.plt = Plotter(qt_widget=self.vtkWidget, bg='blackboard', axes=0)
        self.plt.show(interactive=False)

        self.pushButton_send_back.clicked.connect(self.send_to_napari)
        self.pushButton_get_from_napari.clicked.connect(self.get_from_napari)

        self.pushButton_box_cutter.clicked.connect(self.box_cutter_tool)
        self.pushButton_sphere_cutter.clicked.connect(self.sphere_cutter_tool)
        self.pushButton_plane_cutter.clicked.connect(self.plane_cutter_tool)

        self.plane_cutter_widget = None
        self.box_cutter_widget = None
        self.sphere_cutter_widget = None

        self.vedo_message = Text2D(font='Calco', c='white')

    def get_from_napari(self):
        """
        Get the currently selected layer from napari and display it in vedo
        """
        self.currently_selected_layer = self.napari_viewer.layers.selection.active
        
        # points = self.currently_selected_layer.data[0].astype(float)
        # faces = self.currently_selected_layer.data[1].astype(int)
        # scalars = self.currently_selected_layer.data[2]
        # self.mesh = Mesh([points, faces])  # only vertices and faces       
        # if len(scalars) > 0:
        #     self.mesh.pointdata['scalars'] = scalars
        #     #self.currently_selected_layer.features  # scalars

        self.mesh = Mesh("997.ply")
        self.mesh.triangulate()
        self.mesh.c("yellow5").backcolor("purple6").lighting("glossy")

        #mesh.pointdata = self.currently_selected_layer.features  # scalars
        # Create renderer and add the vedo objects and callbacks

        self.pushButton_box_cutter.setChecked(False)
        self.pushButton_sphere_cutter.setChecked(False)
        self.pushButton_plane_cutter.setChecked(False)

        self.plt += Axes(self.mesh, c='white')
        self.plt += self.mesh
        self.plt += self.vedo_message
        self.plt.reset_camera().render()

    def send_to_napari(self):
        """
        Send the currently displayed mesh in vedo to napari
        """
        # retrieve from plotter
        mesh_tuple = (self.mesh.points(), np.asarray(self.mesh.faces()))

        if len(mesh_tuple[0]) == 0:
            print('No mesh to send to napari')
            return

        self.napari_viewer.add_surface(mesh_tuple)

    def box_cutter_tool(self):
        """
        Add a box cutter tool to the vedo plotter
        """
        self.vedo_message.text(
            "Press r to reset the cutting box\n"
            'Press spacebar to toggle the cutting box on/off\n'
            'Press i to invert the selection\n',
        )
        if self.pushButton_box_cutter.isChecked():
            self.box_cutter_widget = BoxCutter(
                self.mesh,
                invert=self.checkBox_invert.isChecked(),
            )
            self.plt.add(self.box_cutter_widget)
        else:
            self.box_cutter_widget.off()

    def plane_cutter_tool(self):
        """
        Add a plane cutter tool to the vedo plotter
        """
        print(self.plt.actors)
        if self.pushButton_plane_cutter.isChecked():
            self.plt.add_cutter_tool(mode='plane',
                                     invert=self.checkBox_invert.isChecked())
            if self.box_cutter_widget is not None:
                self.box_cutter_widget.Off()
            if self.sphere_cutter_widget is not None:
                self.sphere_cutter_widget.Off()

            self.plt.cutter_widget.On()
            self.plane_cutter_widget = self.plt.cutter_widget
        else:
            self.plane_cutter_widget.Off()

    def sphere_cutter_tool(self):
        if self.pushButton_sphere_cutter.isChecked():
            self.plt.add_cutter_tool(mode='sphere',
                                     invert=self.checkBox_invert.isChecked())
            if self.plane_cutter_widget is not None:
                self.plane_cutter_widget.Off()
            if self.box_cutter_widget is not None:
                self.box_cutter_widget.Off()
            self.plt.cutter_widget.On()
            self.sphere_cutter_widget = self.plt.cutter_widget
        else:
            self.sphere_cutter_widget.Off()
