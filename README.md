# napari-vedo-bridge

[![License BSD-3](https://img.shields.io/pypi/l/napari-vedo-bridge.svg?color=green)](https://github.com/jo-mueller/napari-vedo-bridge/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-vedo-bridge.svg?color=green)](https://pypi.org/project/napari-vedo-bridge)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-vedo-bridge.svg?color=green)](https://python.org)
[![tests](https://github.com/jo-mueller/napari-vedo-bridge/workflows/tests/badge.svg)](https://github.com/jo-mueller/napari-vedo-bridge/actions)
[![codecov](https://codecov.io/gh/jo-mueller/napari-vedo-bridge/branch/main/graph/badge.svg)](https://codecov.io/gh/jo-mueller/napari-vedo-bridge)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-vedo-bridge)](https://napari-hub.org/plugins/napari-vedo-bridge)

To be able to use interactive processing of meshes in napari, this plugin provides a bridge to the vedo library. It allows to transfer meshes between napari and vedo and to use the interactive processing capabilities of vedo in napari. 

## I/O

The plugin allows to export and import meshes and point layers. The following are supported:

| napari layer type | File Format | Import | Export | Features |
|:------------------:|:-----------:|:------:|:------:|:--------:|
| Surface | .vtp | ✓ | ✓ |  ✓ |
| Surface | .vtk | ✓ | ✓ |  ✗ |
| Surface | .obj | ✓ | ✓ |  ✗ |
| Surface | .stl | ✓ | ✓ |  ✗ |
| Surface | .ply | ✓ | ✓ |  ✗ |
| Points | .vtp | ✓ | ✓ |  ✓ |
| Points | .vtk | ✓ | ✓ |  ✗ |
| Points | .ply | ✓ | ✓ |  ✗ |
| Points | .obj | ✓ | ✓ |  ✗ |

## Interactive mesh cutting
To interactively cut meshes in the napari-vedo MeshCutter, install the plugin (see below) and open the plugin it from the napari plugins menu (`Plugins > Mesh Cutter (napari-vedo-bridge)`). 

To cut meshes you can use the following cutters:
- `PlaneCutter`: cuts a mesh with a plane
- `SphereCutter`: cuts a mesh with a sphere
- `BoxCutter`: cuts a mesh with a box

![](https://github.com/jo-mueller/napari-vedo-bridge/raw/main/docs/imgs/screenshot_box_cutter.png)

To send and get data into and from the plugin, you can:

- Retrieve the current mesh from napari (click `Retrieve mesh from napari`) - this imports the **currently selected mesh layer** from napari
- Load a mesh from file (click `Load mesh`)
- Send a mesh to napari (click `Send back to napari`) - this creates a new mesh layer in napari

## Mesh Processing Functions

The plugin also provides a set of mesh processing functions that can be used in napari. These functions are wrapped from the vedo library and provide various mesh processing capabilities. The following functions are available:

- `compute_normals`: Compute normals for the given mesh.
- `shrink`: Shrink the given mesh.
- `join`: Join the given meshes.
- `subdivide`: Subdivide the given mesh.
- `decimate`: Decimate the given mesh.
- `decimate_pro`: Decimate the given mesh using the Pro algorithm.
- `decimate_binned`: Decimate the given mesh using the Binned algorithm.
- `smooth`: Smooth the given mesh.
- `fill_holes`: Fill holes in the given mesh.
- `inside_points`: Get the points inside the given mesh.
- `extrude`: Extrude the given mesh.
- `split`: Split the given mesh into connected components.
- `extract_largest_region`: Extract the largest region from the given mesh.
- `binarize`: Binarize the given mesh.

## Pointcloud Processing Functions

The plugin also provides a set of pointcloud processing functions that can be used in napari. These functions are wrapped from the vedo library and provide various pointcloud processing capabilities. The following functions are available:

- `smooth_points`: Smooth the given points.
- `decimate_points`: Decimate the given points.
- `cluster_points`: Cluster the given points.
- `remove_outliers`: Remove outliers from the given points.
- `compute_normals_points`: Compute normals for the given points.
- `extract_largest_cluster`: Extract the largest cluster from the given points.

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/stable/plugins/index.html
-->

## Installation

You can install `napari-vedo-bridge` via [pip]:

    pip install napari-vedo-bridge

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-vedo-bridge" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
