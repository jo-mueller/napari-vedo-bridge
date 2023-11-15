import os
from pathlib import Path
from qtpy import uic
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QFileDialog
import numpy as np
# from magicgui import magicgui  # pyqt5-tools designer

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import __version__ as _vedo_version
from vedo import Plotter, Text2D, Mesh, Axes, dataurl, settings
from vedo import BoxCutter, PlaneCutter, SphereCutter
from vedo.utils import is_ragged
from vedo.pyplot import histogram


class VedoCutter(QWidget):

    def __init__(self, napari_viewer=None):
        super().__init__()

        self.mesh = None

        self.cutter_widget = None

        settings.default_font = "Calco"
        self.mesh_color = "yellow7"
        self.mesh_backcolor = "purple8"
        self.mesh_lighting = "shiny"
        self.cmap_name = "RdYlBu"

        self.vedo_message = Text2D(pos='bottom-left', c='white', s=0.9)
        self.vedo_axes = None

        self.napari_viewer = napari_viewer
        uic.loadUi(os.path.join(Path(__file__).parent, "./vedo_extension.ui"), self)

        self.vtk_widget = QVTKRenderWindowInteractor()
        self.layout().insertWidget(0, self.vtk_widget)
        self.plot_frame = None
        self.currently_selected_layer = None

        self.pushButton_send_back.clicked.connect(self.send_to_napari)
        self.pushButton_get_from_napari.clicked.connect(self.get_from_napari)

        self.pushButton_box_cutter.clicked.connect(self.box_cutter_tool)
        self.pushButton_sphere_cutter.clicked.connect(self.sphere_cutter_tool)
        self.pushButton_plane_cutter.clicked.connect(self.plane_cutter_tool)
        self.pushButton_load_mesh.clicked.connect(self._load_mesh)
        self.pushButton_save_mesh.clicked.connect(self._save_mesh)
        self.pushButton_extract_largest.clicked.connect(self._extract_largest)
        self.pushButton_compute_curvature.clicked.connect(self._compute_curvature)
        self.pushButton_compute_face_quality.clicked.connect(self._compute_face_quality)
        self.pushButton_compute_area.clicked.connect(self._compute_area)
        self.pushButton_compute_volume.clicked.connect(self._compute_volume)

        self.plt = Plotter(qt_widget=self.vtk_widget, bg='bb', interactive=False)
        self.plt += self.vedo_message
        self.plt += Text2D(
            "vedo " + _vedo_version,
            pos='bottom-right',
            c='k5',
            s=0.5,
        )
        self.plt.interactor.RemoveAllObservers()
        # self.plt.interactor.AddObserver('KeyPressEvent', self.plt._keypress)
        # self.plt.interactor.AddObserver("LeftButtonPressEvent", self.plt._mouseleftclick)
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
            # flip y axis
            points[:,1] = -points[:,1]
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
            self.mesh.name = "mouse brain"

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
        points = self.mesh.vertices.copy()
        points[:,1] = -points[:,1] # flip y axis
        faces = self.mesh.cells
        if len(faces):
            if is_ragged(faces) or len(faces[0]):
                tri_mesh = self.mesh.clone().triangulate()
                faces = tri_mesh.cells
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
                "Press\n"
                " r to reset the cutter\n"
                ' i to toggle it on/off\n'
                ' u to invert the selection',
            )
        self.plt.render()

    def plane_cutter_tool(self):
        """
        Add a plane cutter tool to the vedo plotter
        """
        if not self.mesh:
            self.vedo_message.text("Please load a mesh first")
            self.plt.render()
            return

        # add new cutter
        self._remove_cutter()  # remove old cutter
        if self.pushButton_plane_cutter.isChecked():
            self.cutter_widget = PlaneCutter(self.mesh)
            self.plt.add(self.cutter_widget)
            self.vedo_message.text(
                "Press\n"
                " r to reset the cutter\n"
                ' i to toggle it on/off\n'
                ' u to invert the selection\n'
                ' xyz to reset the axis',
            )
        self.plt.render()

    def sphere_cutter_tool(self):
        """
        Add a sphere cutter tool to the vedo plotter
        """
        if not self.mesh:
            self.vedo_message.text("Please load a mesh first")
            self.plt.render()
            return

        # add new cutter
        self._remove_cutter()  # remove old cutter
        if self.pushButton_sphere_cutter.isChecked():
            self.cutter_widget = SphereCutter(self.mesh)
            self.plt.add(self.cutter_widget)
            self.vedo_message.text(
                "Press\n"
                " r to reset the cutter\n"
                ' i to toggle it on/off\n'
                ' u to invert the selection',
            )
        self.plt.render()

    def _remove_cutter(self):
        if self.cutter_widget:
            self.plt.remove(self.cutter_widget)
            self.cutter_widget = None
        self.vedo_message.text(
            f"Mesh: {self.mesh.name}\n"
            f"Number of points: {self.mesh.npoints}\n"
            f"Number of faces: {self.mesh.ncells}"
        )
        self.plt.render()

    def _load_mesh(self):
        """
        Opens a file dialog to load a mesh file.
        """
        filename = QFileDialog.getOpenFileName(
            caption='Open mesh file',
            filter='Mesh files (*.obj *.ply *.stl *.vtk *.vtp *.xml *.off *.gz)'
        )
        if not filename[0]:
            return

        self.pushButton_box_cutter.setChecked(False)
        self.pushButton_sphere_cutter.setChecked(False)
        self.pushButton_plane_cutter.setChecked(False)

        self.plt.remove(self.mesh, self.vedo_axes, self.plot_frame)

        self.mesh = Mesh(filename[0])

        self.mesh.c(self.mesh_color)
        self.mesh.backcolor(self.mesh_backcolor)
        self.mesh.lighting(self.mesh_lighting)

        self.vedo_axes = Axes(self.mesh, c='white')
        name = os.path.basename(filename[0])
        self.mesh.name = name
        self._remove_cutter()

        self.plt += [self.mesh, self.vedo_axes]
        self.plt.reset_camera().render()

    def _extract_largest(self):
        if self.mesh:
            self._remove_cutter()
            self.plt.remove(self.mesh, self.vedo_axes, self.plot_frame)
            name = self.mesh.name
            self.mesh = self.mesh.extract_largest_region()
            self.mesh.name = name # keep the same name
            self.vedo_axes = Axes(self.mesh, c='white')
            self.plt.add(self.mesh, self.vedo_axes)
            self.plt.render()

    def _compute_curvature(self):
        if self.mesh:
            self.mesh.compute_curvature(method=1)
            arr = self.mesh.pointdata["Mean_Curvature"]
            mean = np.mean(arr)
            std = np.std(arr)
            n = 1
            self.mesh.cmap(self.cmap_name, vmin=mean-n*std, vmax=mean+n*std)
            histo = histogram(
                arr,
                c=self.cmap_name,
                ac="w", gap=0, aspect=2,
                xlim=[mean-n*std, mean+n*std],
                axes={
                    "xtitle": " ",
                    "htitle": "Mean Curvature",
                    "htitle_offset":(0, 0.02, 0),
                    "text_scale": 1.75, 
                    "number_of_divisions": 3,
                    "show_ticks": False,
                },
            )
            self._remove_cutter()
            self.plt.remove(self.plot_frame)
            self.plot_frame = histo.clone2d(pos="top-right", scale=0.5)
            self.plt.add(self.plot_frame)
            self.plt.render()

    def _compute_face_quality(self):
        if self.mesh:
            self.mesh.compute_quality()
            self.mesh.cmap(self.cmap_name, on="cells")#.print()
            histo = histogram(
                self.mesh.celldata["Quality"], 
                c=self.cmap_name,
                ac="w", gap=0, aspect=2, 
                axes={
                    "xtitle": " ",
                    "htitle": "Quality of Polygonal Faces",
                    "htitle_offset":(0, 0.02, 0),
                    "text_scale": 1.75, 
                    "number_of_divisions": 3,
                    "show_ticks": False,
                },
            )
            self._remove_cutter()
            self.plt.remove(self.plot_frame)
            self.plot_frame = histo.clone2d(pos="top-right", scale=0.5)
            self.plt.add(self.plot_frame)
            self.plt.render()

    def _compute_area(self):
        if self.mesh:
            area = self.mesh.clone().triangulate().area()
            self.vedo_message.text(f"Surface area: {area:.4f}")
            self.plt.render()

    def _compute_volume(self):
        if self.mesh:
            volume = self.mesh.clone().triangulate().volume()
            closed = self.mesh.is_closed()
            manifold = self.mesh.is_manifold()
            self.vedo_message.text(
                f"Mesh volume: {volume:.3f}"
                f"\nis closed: {closed}"
                f"\nis manifold: {manifold}"
            )
            self.plt.render()

    def _save_mesh(self):
        filename = QFileDialog.getSaveFileName(
            caption='Save mesh file',
            initialFilter='Mesh files (*.obj *.ply *.stl *.vtk *.vtp *.xml *.off *.gz)'
        )
        if not filename[0]:
            return
        self.mesh.write(filename[0])
        self.vedo_message.text(f"Saved Mesh as: {filename[0]}")
        self.plt.render()
