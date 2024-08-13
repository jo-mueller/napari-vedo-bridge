from typing import List
import vedo
import numpy as np
from napari.utils import notifications

def beethoven() -> List["LayerData"]:
    """
    Load a mesh of Beethoven's head.

    Returns
    -------
    List["LayerData"]
        The mesh of Beethoven's head.
    """

    # create notification about license information
    notifications.show_info(
        message="License information about the Beethoven mesh can be found under " +\
                "https://vedo.embl.es/examples/data/LICENSE.txt"
    )

    mesh = vedo.load(vedo.dataurl + "beethoven.ply")
    return [((mesh.vertices * 10, np.asarray(mesh.cells, dtype=int)),
             {'name': 'Beethoven'},
             "surface")]


def apple() -> List["LayerData"]:
    """
    Load a mesh of an apple.

    Returns
    -------
    List["LayerData"]
        The mesh of an apple.
    """

    # create notification about license information
    notifications.show_info(
        message="License information about the apple mesh can be found under " +\
                "https://vedo.embl.es/examples/data/LICENSE.txt"
    )

    mesh = vedo.load(vedo.dataurl + "apple.ply")
    return [((mesh.vertices * 10, np.asarray(mesh.cells, dtype=int)),
             {'name': 'Apple'},
             "surface")]


def bunny() -> List["LayerData"]:
    """
    Load a mesh of a bunny.

    Returns
    -------
    List["LayerData"]
        The mesh of a bunny.
    """
    # create notification about license information
    notifications.show_info(
        message="License information about the apple mesh can be found under " +\
                "https://vedo.embl.es/examples/data/LICENSE.txt"
    )

    mesh = vedo.load(vedo.dataurl + "bunny.obj")
    return [((mesh.vertices * 10, np.asarray(mesh.cells, dtype=int)),
             {'name': 'Bunny'},"surface")]


def cow() -> List["LayerData"]:
    """
    Load a mesh of a cow.

    Returns
    -------
    List["LayerData"]
        The mesh of a cow.
    """
    # create notification about license information
    notifications.show_info(
        message="License information about the apple mesh can be found under " +\
                "https://vedo.embl.es/examples/data/LICENSE.txt"
    )

    mesh = vedo.load(vedo.dataurl + "cow.vtk")
    return [((mesh.vertices * 10, np.asarray(mesh.cells, dtype=int)),
             {'name': 'Cow'},
             "surface")]


def panther() -> List["LayerData"]:
    """
    Load a mesh of a panther.

    Returns
    -------
    List["LayerData"]
        The mesh of a panther.
    """
    # create notification about license information
    notifications.show_info(
        message="License information about the apple mesh can be found under " +\
                "https://vedo.embl.es/examples/data/LICENSE.txt"
    )

    mesh = vedo.load(vedo.dataurl + "panther.stl")
    return [((mesh.vertices * 10, np.asarray(mesh.cells, dtype=int)),
             {'name': 'Panther'},
             "surface")]


def mouse_limb1() -> List["LayerData"]:
    """
    Load a mesh of a mouse limb.

    Returns
    -------
    List["LayerData"]
        The mesh of a mouse limb.
    """
    # create notification about license information
    notifications.show_info(
        message="License information about the apple mesh can be found under " +\
                "https://vedo.embl.es/examples/data/LICENSE.txt"
    )

    mesh = vedo.load(vedo.dataurl + "250.vtk")
    return [((mesh.vertices * 10, np.asarray(mesh.cells, dtype=int)),
             {'name': 'Mouse limb 250'},
             "surface")]


def mouse_limb2() -> List["LayerData"]:
    """
    Load a mesh of a mouse limb.

    Returns
    -------
    List["LayerData"]
        The mesh of a mouse limb.
    """
    # create notification about license information
    notifications.show_info(
        message="License information about the apple mesh can be found under " +\
                "https://vedo.embl.es/examples/data/LICENSE.txt"
    )

    mesh = vedo.load(vedo.dataurl + "270.vtk")
    return [((mesh.vertices * 10, np.asarray(mesh.cells, dtype=int)),
             {'name': 'Mouse limb 270'},
             "surface")]


def mouse_limb3() -> List["LayerData"]:
    """
    Load a mesh of a mouse limb.

    Returns
    -------
    List["LayerData"]
        The mesh of a mouse limb.
    """
    # create notification about license information
    notifications.show_info(
        message="License information about the apple mesh can be found under " +\
                "https://vedo.embl.es/examples/data/LICENSE.txt"
    )

    mesh = vedo.load(vedo.dataurl + "290.vtk")
    return [((mesh.vertices * 10, np.asarray(mesh.cells, dtype=int)),
             {'name': 'Mouse limb 3'},
             "surface")]