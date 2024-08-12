__version__ = "0.1.0"

from ._mesh import (
    compute_normals,
    shrink,
    subdivide,
    decimate,
    decimate_pro,
    decimate_binned,
    smooth,
    fill_holes,
    split,
    extract_largest_region,
    binarize,
)

from ._points import (
    smooth_mls_1d,
    remove_outliers,
)

__all__ = [
    "compute_normals",
    "shrink",
    "subdivide",
    "decimate",
    "decimate_pro",
    "decimate_binned",
    "smooth",
    "fill_holes",
    "split",
    "extract_largest_region",
    "binarize",
    "smooth_points",
    "remove_outliers"
]
