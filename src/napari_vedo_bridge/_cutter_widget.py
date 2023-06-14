import os
from pathlib import Path
from qtpy import uic
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QFileDialog
import numpy as np
# from magicgui import magicgui

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import __version__ as _vedo_version
from vedo import Plotter, Text2D, Mesh, Axes, dataurl
from vedo import BoxCutter, PlaneCutter#, SphereCutter
from vedo.utils import is_ragged


class VedoCutter(QWidget):

    def __init__(self, napari_viewer=None):
        super().__init__()

        self.mesh = None

        self.cutter_widget = None

        self.mesh_color = "yellow6"
        self.mesh_backcolor = "purple7"
        self.mesh_lighting = "shiny"

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
        self.pushButton_load_mesh.clicked.connect(self._load_mesh)

        self.plt = Plotter(qt_widget=self.vtkWidget, bg='bb', interactive=False)
        self.plt += self.vedo_message
        self.plt += Text2D(
            "vedo " + _vedo_version,
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
            self.mesh = Mesh(dataurl + "mouse_brain.stl")

        self.mesh.c(self.mesh_color)
        self.mesh.backcolor(self.mesh_backcolor)
        self.mesh.lighting(self.mesh_lighting)

        try:
            if self.currently_selected_layer.name:
                self.mesh.name = self.currently_selected_layer.name
                self.vedo_message.text(f"Mesh: {self.mesh.name}")
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
        points = self.mesh.points()
        faces = self.mesh.faces()
        if len(faces):
            if is_ragged(faces) or len(faces[0]):
                tri_mesh = self.mesh.clone().triangulate()
                faces = tri_mesh.faces()
                self.vedo_message.text("Mesh has been forced triangular!")
                self.plt.render()
        faces = np.asarray(faces, dtype=int)
        mesh_tuple = (points, faces)

        if len(mesh_tuple[0]) == 0:
            self.vedo_message.text("No mesh to send to napari!")
            self.plt.render()
            return
        
        name = "vedo_mesh"
        if self.mesh.name:
            name = self.mesh.name
        elif self.mesh.filename:
            name = os.path.basename(self.mesh.filename).split(".")[0]
        self.napari_viewer.add_surface(mesh_tuple, name=name)

    def box_cutter_tool(self):
        """
        Add a box cutter tool to the vedo plotter
        """
        if not self.mesh:
            self.vedo_message.text("Please load a mesh first")
            self.plt.render()
            return

        # add new cutter
        self._remove_cutter()  # remove old cutter
        if self.pushButton_box_cutter.isChecked():
            self.cutter_widget = BoxCutter(self.mesh)
            self.plt.add(self.cutter_widget)
            self.vedo_message.text(
                "Press r to reset the cutter\n"
                'Press i to toggle it on/off\n'
                'Press u to invert the selection\n',
            )

        self.plt.render()

    def plane_cutter_tool(self):
        """
        Add a plane cutter tool to the vedo plotter
        """
        print("plane cutter tool")

        if not self.mesh:
            self.vedo_message.text("Please load a mesh first")
            self.plt.render()
            return

        # add new cutter
        self._remove_cutter()  # remove old cutter
        if self.pushButton_box_cutter.isChecked():
            self.cutter_widget = PlaneCutter(self.mesh)
            self.plt.add(self.cutter_widget)
            self.vedo_message.text(
                "Press r to reset the cutter\n"
                'Press i to toggle it on/off\n'
                'Press u to invert the selection\n',
            )

        self.plt.render()

    def sphere_cutter_tool(self):
        """
        Add a sphere cutter tool to the vedo plotter
        """
        self._remove_cutter()  # remove old cutter
        self.vedo_message.text("Coming soon!")
        self.plt.render()
        pass

    def _remove_cutter(self):
        if self.cutter_widget:
            self.plt.remove(self.cutter_widget)
            self.cutter_widget = None
        self.plt.render()

    def _load_mesh(self):
        """
        Opens a file dialog to load a mesh file.
        """
        filename = QFileDialog.getOpenFileName(
            caption='Open mesh file',
            filter='Mesh files (*.obj *.ply *.stl *.vtk *.vtp *.xml *.off *.gz)'
        )
        if len(filename) == 0:
            return

        self.pushButton_box_cutter.setChecked(False)
        self.pushButton_sphere_cutter.setChecked(False)
        self.pushButton_plane_cutter.setChecked(False)

        self._remove_cutter()
        self.plt.remove(self.mesh, self.vedo_axes)

        self.mesh = Mesh(filename[0])

        self.mesh.c(self.mesh_color)
        self.mesh.backcolor(self.mesh_backcolor)
        self.mesh.lighting(self.mesh_lighting)

        self.vedo_axes = Axes(self.mesh, c='white')
        name = os.path.basename(filename[0])
        self.vedo_message.text(f"Loaded Mesh: {name}")

        self.plt += [self.mesh, self.vedo_axes]
        self.plt.reset_camera().render()
