__version__ = "0.1.0"

from ._mesh import (
    compute_normals,
    shrink,
    join,
    subdivide,
    decimate,
    decimate_pro,
    decimate_binned,
    smooth,
    fill_holes,
    inside_points,
    extrude,
    split,
    extract_largest_region,
    binarize,
)

from ._points import (
    smooth_points,
    decimate_points,
    cluster_points,
    remove_outliers,
    compute_normals as compute_normals_points,
    extract_largest_cluster,
)

__all__ = [
    "compute_normals",
    "shrink",
    "join",
    "subdivide",
    "decimate",
    "decimate_pro",
    "decimate_binned",
    "smooth",
    "fill_holes",
    "inside_points",
    "extrude",
    "split",
    "extract_largest_region",
    "binarize",
    "smooth_points",
    "decimate_points",
    "cluster_points",
    "remove_outliers",
    "compute_normals_points",
    "extract_largest_cluster",
]
