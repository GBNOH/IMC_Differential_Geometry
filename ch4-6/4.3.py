"""Draw a smoothly deformed torus with a chart, neighborhood, and point p."""

import os

import numpy as np
import pyvista as pv


# 0.0 gives a standard torus; 1.0 is the intended visibly deformed version.
DEFORMATION = 1.0
MAJOR_RADIUS = 2.65
MINOR_RADIUS = 1.50


def torus_xyz(u, v):
    """A periodic torus with smooth, large-scale deformation only."""
    d = DEFORMATION

    # One broad variation around the ring; higher harmonics would create bumps.
    major = MAJOR_RADIUS + 0.28 * d * np.cos(u - 0.30)
    minor = MINOR_RADIUS * (
        1.0
        + d
        * (
            -0.20 * np.cos(u)
            + 0.035 * np.sin(u - 0.45)
        )
    )

    rho = major + minor * np.cos(v)
    x0 = rho * np.cos(u)
    y0 = rho * np.sin(u)

    # Global oval stretching, shear, flattening, and a gentle one-wave bend.
    x = (1.0 + 0.20 * d) * x0 + 0.10 * d * y0
    y = (1.0 - 0.10 * d) * y0
    z = (
        (1.0 - 0.30 * d) * minor * np.sin(v)
        + 0.24 * d * np.sin(u - 0.55)
    )
    return np.stack((x, y, z), axis=-1)


def surface_normal(u, v, eps=1.0e-4):
    """Numerical outward unit normal of the deformed parametrization."""
    du = torus_xyz(u + eps, v) - torus_xyz(u - eps, v)
    dv = torus_xyz(u, v + eps) - torus_xyz(u, v - eps)
    normal = np.cross(du, dv)
    return normal / np.linalg.norm(normal, axis=-1, keepdims=True)


def lifted_points(u, v, lift=0.025):
    """Points slightly above the surface to prevent z-fighting."""
    return torus_xyz(u, v) + lift * surface_normal(u, v)


def polyline(points):
    return pv.lines_from_points(np.asarray(points), close=False)


def dashed_polyline(points, dash_points=5, gap_points=4):
    """Return disconnected polyline pieces forming a dashed curve."""
    points = np.asarray(points)
    kept = []
    cells = []
    cursor = 0

    for start in range(0, len(points) - 1, dash_points + gap_points):
        piece = points[start : start + dash_points]
        if len(piece) < 2:
            continue
        kept.extend(piece)
        cells.extend([len(piece), *range(cursor, cursor + len(piece))])
        cursor += len(piece)

    result = pv.PolyData(np.asarray(kept))
    result.lines = np.asarray(cells, dtype=np.int64)
    return result


def add_label(plotter, point, text, size=24, bold=False):
    plotter.add_point_labels(
        np.asarray(point)[None, :],
        [text],
        italic=not bold,
        bold=bold,
        font_size=size,
        text_color="black",
        font_family="times",
        show_points=False,
        shape=None,
        always_visible=True,
        reset_camera=False,
    )


# Confirm that the variable-radius tube remains safely separated from its axis.
u_check = np.linspace(0.0, 2.0 * np.pi, 2000)
d = DEFORMATION
major_check = MAJOR_RADIUS + 0.28 * d * np.cos(u_check - 0.30)
minor_check = MINOR_RADIUS * (
    1.0
    + d
    * (
        -0.20 * np.cos(u_check)
        + 0.035 * np.sin(u_check - 0.45)
    )
)
assert np.min(major_check - minor_check) > 0.5, "Deformation closes the torus hole."


# Main torus mesh: both parameters are periodic.
u = np.linspace(0.0, 2.0 * np.pi, 260)
v = np.linspace(0.0, 2.0 * np.pi, 150)
uu, vv = np.meshgrid(u, v, indexing="ij")
torus_points = torus_xyz(uu, vv)
torus = pv.StructuredGrid(
    torus_points[..., 0],
    torus_points[..., 1],
    torus_points[..., 2],
)


SAVE_IMAGE = os.environ.get("PYVISTA_SCREENSHOT")
plotter = pv.Plotter(
    off_screen=SAVE_IMAGE is not None,
    window_size=(1200, 850),
)
plotter.set_background("white")
plotter.enable_anti_aliasing("ssaa")

plotter.add_mesh(
    torus,
    color="#8FEAE8",
    smooth_shading=True,
    show_edges=False,
    ambient=0.30,
    diffuse=0.78,
    specular=0.20,
    specular_power=25,
)


# Dashed boundary of the coordinate patch x(D).
u_lo, u_hi = 2.95, 4.05
v_lo, v_hi = 1.55, 2.90
curve_parameter = np.linspace(0.0, 1.0, 180)
patch_curves = [
    lifted_points(
        u_lo + (u_hi - u_lo) * curve_parameter,
        np.full_like(curve_parameter, v_lo),
    ),
    lifted_points(
        u_lo + (u_hi - u_lo) * curve_parameter,
        np.full_like(curve_parameter, v_hi),
    ),
    lifted_points(
        np.full_like(curve_parameter, u_lo),
        v_lo + (v_hi - v_lo) * curve_parameter,
    ),
    lifted_points(
        np.full_like(curve_parameter, u_hi),
        v_lo + (v_hi - v_lo) * curve_parameter,
    ),
]
for curve in patch_curves:
    plotter.add_mesh(
        dashed_polyline(curve),
        color="#202020",
        line_width=1.7,
    )


# A smaller elliptical neighborhood N(p) contained in the chart.
u_p, v_p = 3.48, 2.22
disk_radius = np.linspace(0.0, 1.0, 36)
disk_angle = np.linspace(0.0, 2.0 * np.pi, 120)
ss, aa = np.meshgrid(disk_radius, disk_angle)
u_disk = u_p + 0.30 * ss * np.cos(aa)
v_disk = v_p + 0.40 * ss * np.sin(aa)
disk_points = lifted_points(u_disk, v_disk, lift=0.035)
neighborhood = pv.StructuredGrid(
    disk_points[..., 0],
    disk_points[..., 1],
    disk_points[..., 2],
)
plotter.add_mesh(
    neighborhood,
    color="#00CAD0",
    smooth_shading=True,
    ambient=0.34,
    diffuse=0.72,
    specular=0.15,
)

oval_angle = np.linspace(0.0, 2.0 * np.pi, 180)
oval = lifted_points(
    u_p + 0.30 * np.cos(oval_angle),
    v_p + 0.40 * np.sin(oval_angle),
    lift=0.045,
)
plotter.add_mesh(
    dashed_polyline(oval, dash_points=6, gap_points=4),
    color="#202020",
    line_width=1.5,
)


# Point p and labels.
p_location = lifted_points(np.array(u_p), np.array(v_p), lift=0.10)
plotter.add_mesh(pv.Sphere(radius=0.075, center=p_location), color="black")

add_label(plotter, lifted_points(np.array(3.00), np.array(1.62), 0.16), "x(D)", 27, True)
add_label(plotter, lifted_points(np.array(3.82), np.array(2.45), 0.14), "N(p)", 25)
add_label(plotter, lifted_points(np.array(u_p), np.array(v_p + 0.20), 0.15), "p", 25, True)
add_label(plotter, lifted_points(np.array(1.12), np.array(0.35), 0.20), "M", 30)


# High oblique view: the torus remains unmistakable while resembling the source.
camera_position = (7.0, -9.0, 26.0)
camera_target = (0.0, 0.0, 0.10)
plotter.camera_position = [
    camera_position,
    camera_target,
    (0.0, 0.0, 1.0),
]
plotter.camera.parallel_projection = True
plotter.camera.parallel_scale = 3.80
plotter.add_silhouette(torus, color="#202020", line_width=1.3)

if SAVE_IMAGE:
    plotter.show(screenshot=SAVE_IMAGE)
else:
    plotter.show()
