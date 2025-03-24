import napari.utils
from qtpy import uic, QtWidgets
from qtpy.QtCore import QObject, Signal, Qt

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import napari
import numpy as np
import sys
import os
from pathlib import Path

from vedo import Plotter, Mesh, settings, Text2D
from vedo import __version__ as _vedo_version

settings.default_backend = 'vtk'


class EmittingStream(QObject):
    textWritten = Signal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


class VedoWidget(QtWidgets.QWidget):
    def __init__(self, napari_viewer: napari.Viewer):
        super().__init__()
        self.napari_viewer = napari_viewer

        self._setup_ui()
        self._connect_signals()

        self.plt = Plotter(qt_widget=self.vtk_widget, interactive=True, axes=2, bg='bb')
        self._show_relevant_text()
        self.plt.show()
        self.mesh = None

    def _setup_ui(self):

        uic.loadUi(
            os.path.join(Path(__file__).parent, "./base_widget.ui"),
            self
            )

        # insert vtk widget at the top
        self.vtk_widget = QVTKRenderWindowInteractor()
        self.layout().insertWidget(0, self.vtk_widget)

    def _connect_signals(self):
        self.pushButton_get_from_napari.clicked.connect(self._from_napari)
        self.pushButton_send_back.clicked.connect(self._to_napari)
        self.pushButton_clear.clicked.connect(self._clear)
        self.pushButton_show_hotkeys.clicked.connect(self._show_hotkey_reference)

        # connect stdout to text edit
        sys.stdout = EmittingStream(textWritten=self._collect_stdout)

    def _from_napari(self):
        selected_layers = self.napari_viewer.layers.selection.active

        if not isinstance(selected_layers, napari.layers.Surface):
            # throw napari warning
            napari.utils.notifications.Notification(
                title="Invalid Layer",
                message="Please select a surface layer",
                duration=2
            ).send()
            return

        self.mesh = Mesh(selected_layers.data[:2])  # only vertices and faces
        text = Text2D(
            "Layer: " + selected_layers.name,
            pos='top-left',
            font='Calco',
            c='k5',
            s=0.5,
        )
        self.plt += [text, self.mesh]
        self.plt.render()

        self.status_text_edit.appendPlainText(f"Mesh: {selected_layers.name}")

    def _to_napari(self):
        """
        Get mesh data from the plotter and send back
        """
        if self.mesh is None:
            return

        # get vertices and faces
        vertices, faces = self.mesh.vertices, self.mesh.cells
        layer = napari.layers.Surface((vertices, np.asarray(faces)))
        self.napari_viewer.add_layer(layer)

        self.status_text_edit.appendPlainText(f"Sent to Napari: {layer.name}")

    def _show_relevant_text(self):
        self.plt += Text2D(
            "vedo " + _vedo_version,
            pos='bottom-right',
            font='Calco',
            c='k5',
            s=0.5,
        )

    def _show_hotkey_reference(self):
        hotkey_reference = VedoHotkeyreference(self.napari_viewer)
        self.napari_viewer.window.add_dock_widget(hotkey_reference, area='right')

    def _clear(self):
        self.plt.clear()
        [self.plt.remove(actor) for actor in self.plt.actors]
        self._show_relevant_text()
        self.plt.render()
        self.mesh = None

        self.status_text_edit.clear()

    def _collect_stdout(self, text):
        self.status_text_edit.appendPlainText(text)


class VedoHotkeyreference(QtWidgets.QWidget):
    def __init__(self, napari_viewer: napari.Viewer):
        super().__init__()

        self._setup_ui()

    def _setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout()

        # Create a QTableWidget
        self.hotkey_table = QtWidgets.QTableWidget()
        self.hotkey_table.setRowCount(28)  # Number of hotkeys
        self.hotkey_table.setColumnCount(2)  # Hotkey and description
        self.hotkey_table.setHorizontalHeaderLabels(["Hotkey", "Description"])
        self.hotkey_table.verticalHeader().setVisible(False)
        self.hotkey_table.horizontalHeader().setStretchLastSection(True)

        # Hotkey descriptions
        hotkeys = [
            ("i", "print info about the last clicked object"),
            ("I", "print color of the pixel under the mouse"),
            ("Y", "show the pipeline for this object as a graph"),
            ("<- ->", "use arrows to reduce/increase opacity"),
            ("x", "toggle mesh visibility"),
            ("w", "toggle wireframe/surface style"),
            ("l", "toggle surface edges visibility"),
            ("p/P", "hide surface faces and show only points"),
            ("1-3", "cycle surface color (2=light, 3=dark)"),
            ("4", "cycle color map (press shift-4 to go back)"),
            ("5-6", "cycle point-cell arrays (shift to go back)"),
            ("7-8", "cycle background and gradient color"),
            ("09+-", "cycle axes styles (on keypad, or press +/-)"),
            ("k", "cycle available lighting styles"),
            ("K", "toggle shading as flat or phong"),
            ("A", "toggle anti-aliasing"),
            ("D", "toggle depth-peeling (for transparencies)"),
            ("U", "toggle perspective/parallel projection"),
            ("o/O", "toggle extra light to scene and rotate it"),
            ("a", "toggle interaction to Actor Mode"),
            ("n", "toggle surface normals"),
            ("r", "reset camera position"),
            ("R", "reset camera to the closest orthogonal view"),
            (".", "fly camera to the last clicked point"),
            ("C", "print the current camera parameters state"),
            ("X", "invoke a cutter widget tool"),
            ("S", "save a screenshot of the current scene"),
            ("E/F", "export 3D scene to numpy file or X3D"),
            ("q", "return control to python script"),
            ("Esc", "abort execution and exit python kernel"),
        ]

        # Populate the table
        for row, (hotkey, description) in enumerate(hotkeys):
            hotkey_item = QtWidgets.QTableWidgetItem(hotkey)
            description_item = QtWidgets.QTableWidgetItem(description)
            hotkey_item.setFlags(hotkey_item.flags() & ~Qt.ItemIsEditable)
            description_item.setFlags(description_item.flags() & ~Qt.ItemIsEditable)
            self.hotkey_table.setItem(row, 0, hotkey_item)
            self.hotkey_table.setItem(row, 1, description_item)

        self.layout.addWidget(self.hotkey_table)
        self.setLayout(self.layout)
