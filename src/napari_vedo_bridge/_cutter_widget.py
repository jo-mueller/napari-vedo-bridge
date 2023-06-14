from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter, Mesh, dataurl, Axes
import vedo
import os
from pathlib import Path
from qtpy import uic
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QFileDialog
import numpy as np
from magicgui import magicgui


class VedoCutter(QWidget):

    def __init__(self, napari_viewer=None):
        super().__init__()

        self.napari_viewer = napari_viewer
        uic.loadUi(os.path.join(Path(__file__).parent, "./vedo_extension.ui"), self)

    #     Qt.QMainWindow.__init__(self, parent)
    #     self.frame = Qt.QFrame()
        # self.layout = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor()
        self.layout().insertWidget(0, self.vtkWidget)
        self.plt = Plotter(qt_widget=self.vtkWidget, bg='blackboard', axes=0)
        self.plt.show(interactive=False)

        self.pushButton_send_back.clicked.connect(self.send_to_napari)
        self.pushButton_get_from_napari.clicked.connect(self.get_from_napari)

        self.pushButton_box_cutter.clicked.connect(self.box_cutter_tool)
        self.pushButton_sphere_cutter.clicked.connect(self.sphere_cutter_tool)
        self.pushButton_plane_cutter.clicked.connect(self.plane_cutter_tool)
        self.pushButton_load_mesh.clicked.connect(self._load_mesh)

        self.plane_cutter_widget = None
        self.box_cutter_widget = None
        self.sphere_cutter_widget = None

    def get_from_napari(self):
        """
        Get the currently selected layer from napari and display it in vedo
        """

        self.currently_selected_layer = self.napari_viewer.layers.selection.active
        self.mesh = Mesh(self.currently_selected_layer.data[:2])  # only vertices and faces
        #mesh.pointdata = self.currently_selected_layer.features  # scalars
        # Create renderer and add the vedo objects and callbacks

        self.pushButton_box_cutter.setChecked(False)
        self.pushButton_sphere_cutter.setChecked(False)
        self.pushButton_plane_cutter.setChecked(False)

        if len(self.plt.actors) > 0:
            self.plt.clear(deep=True)
        #self.plt += Axes(self.mesh, c='white')
        self.plt += self.mesh
        self.plt.reset_camera()

    def send_to_napari(self):
        """
        Send the currently displayed mesh in vedo to napari
        """
        # retrieve from plotter
        self.mesh = self.plt.actors[0]
        mesh_tuple = (self.mesh.points(), np.asarray(self.mesh.faces()))

        if len(mesh_tuple[0]) == 0:
            print('No mesh to send to napari')
            return

        self.napari_viewer.add_surface(mesh_tuple)

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

    def box_cutter_tool(self):
        """
        Add a box cutter tool to the vedo plotter
        """
        print(self.plt.actors)
        if self.pushButton_box_cutter.isChecked():
            self.plt.add_cutter_tool(mode='box',
                                     invert=self.checkBox_invert.isChecked())
            if self.plane_cutter_widget is not None:
                self.plane_cutter_widget.Off()
            if self.sphere_cutter_widget is not None:
                self.sphere_cutter_widget.Off()
                
            self.plt.cutter_widget.On()
            self.box_cutter_widget = self.plt.cutter_widget
        else:
            self.box_cutter_widget.Off()

    def sphere_cutter_tool(self):
        print(self.plt.actors)
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

    def _load_mesh(self):
        """
        Opens a file dialog to load a mesh file.
        """
        filename = QFileDialog.getOpenFileName(
            caption='Open mesh file',
            filter='Mesh files (*.obj *.ply *.stl *.vtk *.vtp)'
        )

        self.mesh = vedo.load(filename[0])
        if len(self.plt.actors) > 0:
            self.plt.clear(deep=True)
    
        #self.plt += Axes(self.mesh, c='white')
        self.plt += self.mesh
        self.plt.reset_camera()

