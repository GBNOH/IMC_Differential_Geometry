"""Reproduce a coordinate-chart diagram on a smoothly deformed torus."""

import os

import numpy as np
import pyvista as pv


# Geometry controls.  Increase VERTICAL_SCALE to make the surface taller.
DEFORMATION = 1.0
VERTICAL_SCALE = 1.0
MAJOR_RADIUS = 2.35
MINOR_RADIUS = 1.48


def surface_xyz(u, v):
    """Smooth periodic parametrization of the deformed torus M."""
    d = DEFORMATION

    # The lower-left part is smaller and lower; the upper-right part is fuller.
    phase = u + np.pi / 4.0
    major = MAJOR_RADIUS * (1.0 - 0.10 * d * np.cos(phase))
    minor = MINOR_RADIUS * (1.0 - 0.24 * d * np.cos(phase))

    rho = major + minor * np.cos(v)
    x0 = rho * np.cos(u)
    y0 = rho * np.sin(u)

    # Broad affine deformation preserves the visual character of a ring.
    x = 0.92 * x0 + 0.10 * d * y0
    y = 1.08 * y0
    center_height = 1.72 - 0.90 * d * np.cos(phase)
    z = VERTICAL_SCALE * (
        center_height + 0.72 * minor * np.sin(v)
    )
    return np.stack((x, y, z), axis=-1)


def surface_normal(u, v, eps=1.0e-4):
    """Numerical unit normal of the parametrized surface."""
    du = surface_xyz(u + eps, v) - surface_xyz(u - eps, v)
    dv = surface_xyz(u, v + eps) - surface_xyz(u, v - eps)
    normal = np.cross(du, dv)
    return normal / np.linalg.norm(normal, axis=-1, keepdims=True)


def lifted_surface_points(u, v, lift=0.025):
    """Lift curves slightly to prevent z-fighting."""
    return surface_xyz(u, v) + lift * surface_normal(u, v)


def dashed_polyline(points, dash_points=7, gap_points=5):
    """Create a single PolyData object containing disconnected dash segments."""
    points = np.asarray(points)
    kept_points = []
    line_cells = []
    cursor = 0

    for start in range(0, len(points) - 1, dash_points + gap_points):
        piece = points[start : start + dash_points]
        if len(piece) < 2:
            continue
        kept_points.extend(piece)
        line_cells.extend([len(piece), *range(cursor, cursor + len(piece))])
        cursor += len(piece)

    result = pv.PolyData(np.asarray(kept_points))
    result.lines = np.asarray(line_cells, dtype=np.int64)
    return result


def dashed_segment(start, end, dash_count=10, occupied_fraction=0.56):
    """Dashed straight segment, used for vertical projection lines."""
    start = np.asarray(start, dtype=float)
    end = np.asarray(end, dtype=float)
    pieces = []

    for index in range(dash_count):
        a = index / dash_count
        b = a + occupied_fraction / dash_count
        pieces.extend(
            [
                start + a * (end - start),
                start + b * (end - start),
            ]
        )

    result = pv.PolyData(np.asarray(pieces))
    cells = []
    for index in range(dash_count):
        cells.extend([2, 2 * index, 2 * index + 1])
    result.lines = np.asarray(cells, dtype=np.int64)
    return result


def disk_mesh(u0, v0, du, dv, project_to_plane=False, lift=0.0):
    """Triangulated parameter disk, either on M or vertically projected to z=0."""
    radial_count = 24
    angular_count = 120
    angles = np.linspace(0.0, 2.0 * np.pi, angular_count, endpoint=False)

    parameter_pairs = [(u0, v0)]
    for radial_index in range(1, radial_count + 1):
        radius = radial_index / radial_count
        parameter_pairs.extend(
            zip(
                u0 + du * radius * np.cos(angles),
                v0 + dv * radius * np.sin(angles),
            )
        )

    parameter_pairs = np.asarray(parameter_pairs)
    disk_points = surface_xyz(parameter_pairs[:, 0], parameter_pairs[:, 1])

    if project_to_plane:
        disk_points[:, 2] = 0.035
    elif lift:
        disk_points += lift * surface_normal(
            parameter_pairs[:, 0], parameter_pairs[:, 1]
        )

    faces = []
    # Triangle fan between the center and the first ring.
    first_ring = 1
    for j in range(angular_count):
        j_next = (j + 1) % angular_count
        faces.extend([3, 0, first_ring + j, first_ring + j_next])

    # Quad strips between all subsequent rings.
    for radial_index in range(1, radial_count):
        inner = 1 + (radial_index - 1) * angular_count
        outer = 1 + radial_index * angular_count
        for j in range(angular_count):
            j_next = (j + 1) % angular_count
            faces.extend(
                [
                    4,
                    inner + j,
                    outer + j,
                    outer + j_next,
                    inner + j_next,
                ]
            )

    return pv.PolyData(disk_points, np.asarray(faces, dtype=np.int64))


def add_label(plotter, point, text, size=24, bold=False, italic=False):
    """Add a clean, unboxed Times label at a fixed 3-D location."""
    plotter.add_point_labels(
        np.asarray(point, dtype=float)[None, :],
        [text],
        show_points=False,
        always_visible=True,
        shape=None,
        font_family="times",
        font_size=size,
        text_color="black",
        bold=bold,
        italic=italic,
        reset_camera=False,
    )


def add_axis(plotter, direction, length, label):
    """Add one manual black coordinate arrow and its correct label."""
    direction = np.asarray(direction, dtype=float)
    arrow = pv.Arrow(
        start=(0.0, 0.0, 0.0),
        direction=direction,
        scale=length,
        shaft_radius=0.006,
        tip_radius=0.035,
        tip_length=0.10,
    )
    plotter.add_mesh(arrow, color="black", smooth_shading=True)
    label_point = 1.09 * length * direction
    add_label(plotter, label_point, label, size=23, italic=True)


# Confirm that the variable tube remains separated from the torus axis.
u_check = np.linspace(0.0, 2.0 * np.pi, 2000)
minor_check = MINOR_RADIUS * (
    1.0 - 0.24 * DEFORMATION * np.cos(u_check + np.pi / 4.0)
)
major_check = MAJOR_RADIUS * (
    1.0 - 0.10 * DEFORMATION * np.cos(u_check + np.pi / 4.0)
)
assert np.min(major_check - minor_check) > 0.70, "The torus hole has closed."


# Main periodic surface.
u = np.linspace(0.0, 2.0 * np.pi, 280)
v = np.linspace(0.0, 2.0 * np.pi, 170)
uu, vv = np.meshgrid(u, v, indexing="ij")
surface_points = surface_xyz(uu, vv)
surface = pv.StructuredGrid(
    surface_points[..., 0],
    surface_points[..., 1],
    surface_points[..., 2],
)


# The local coordinate disk is placed on the fuller upper-right lobe.
u_p = 3.0 * np.pi / 4.0
v_p = np.pi / 2.0
du = 0.34
dv = 0.40

chart_patch = disk_mesh(u_p, v_p, du, dv, lift=0.035)
domain_disk = disk_mesh(u_p, v_p, du, dv, project_to_plane=True)

boundary_angle = np.linspace(0.0, 2.0 * np.pi, 260)
boundary_u = u_p + du * np.cos(boundary_angle)
boundary_v = v_p + dv * np.sin(boundary_angle)
surface_boundary = lifted_surface_points(boundary_u, boundary_v, lift=0.055)
domain_boundary = surface_xyz(boundary_u, boundary_v)
domain_boundary[:, 2] = 0.055


SAVE_IMAGE = os.environ.get("PYVISTA_SCREENSHOT")
plotter = pv.Plotter(
    off_screen=SAVE_IMAGE is not None,
    window_size=(1200, 900),
)
plotter.set_background("white")
plotter.enable_anti_aliasing("ssaa")


# Matte cyan surface, avoiding a plastic appearance.
plotter.add_mesh(
    surface,
    color="#9BEDEC",
    smooth_shading=True,
    show_edges=False,
    ambient=0.38,
    diffuse=0.70,
    specular=0.08,
    specular_power=18,
)
plotter.add_silhouette(surface, color="#202020", line_width=1.25)


# Highlight x(D) and its planar domain D.
plotter.add_mesh(
    chart_patch,
    color="#16D4D7",
    smooth_shading=True,
    ambient=0.44,
    diffuse=0.62,
    specular=0.06,
)
plotter.add_mesh(
    domain_disk,
    color="#19CED3",
    smooth_shading=True,
    ambient=0.55,
    diffuse=0.55,
    specular=0.04,
)
plotter.add_mesh(
    dashed_polyline(surface_boundary),
    color="#202020",
    line_width=1.8,
)
plotter.add_mesh(
    dashed_polyline(domain_boundary),
    color="#202020",
    line_width=1.8,
)


# Point p, its parameter point (u,v), and vertical projection fibers.
p_raw = surface_xyz(np.array(u_p), np.array(v_p))
p_surface = p_raw + np.array([0.0, 0.0, 0.10])
p_domain = np.array([p_raw[0], p_raw[1], 0.095])
plotter.add_mesh(pv.Sphere(radius=0.075, center=p_surface), color="black")
plotter.add_mesh(pv.Sphere(radius=0.050, center=p_domain), color="black")

projection_parameters = [
    (u_p - du, v_p),
    (u_p, v_p),
    (u_p + du, v_p),
]
for line_u, line_v in projection_parameters:
    upper = surface_xyz(np.array(line_u), np.array(line_v))
    upper = upper + np.array([0.0, 0.0, 0.07])
    lower = np.array([upper[0], upper[1], 0.065])
    plotter.add_mesh(
        dashed_segment(lower, upper, dash_count=11),
        color="#303030",
        line_width=1.45,
    )


# Coordinate axes are manual so the three labels cannot become x, x, x.
add_axis(plotter, (1.0, 0.0, 0.0), 4.50, "x")
add_axis(plotter, (0.0, 1.0, 0.0), 4.65, "y")
add_axis(plotter, (0.0, 0.0, 1.0), 4.75, "z")


# Labels, placed to follow the layout of the source figure.
add_label(
    plotter,
    p_surface + np.array([0.05, 0.00, 0.55]),
    "x(D)",
    size=28,
    bold=True,
)
add_label(
    plotter,
    p_surface + np.array([-0.58, 0.42, 0.02]),
    "p = (u, v, h(u, v))",
    size=24,
    bold=True,
)
add_label(
    plotter,
    p_domain + np.array([0.44, -0.28, -0.03]),
    "(u, v)",
    size=23,
    italic=True,
)
add_label(
    plotter,
    p_domain + np.array([-0.48, 0.34, -0.02]),
    "D",
    size=26,
    italic=True,
)

label_m = lifted_surface_points(
    np.array(7.0 * np.pi / 4.0),
    np.array(1.10 * np.pi),
    lift=0.14,
)
add_label(plotter, label_m, "M", size=29, italic=True)


# Isometric-like view: +x points lower-left, +y right, and +z upward.
plotter.camera_position = [
    (8.5, 12.5, 9.5),
    (0.0, 0.0, 1.72),
    (0.0, 0.0, 1.0),
]
plotter.camera.parallel_projection = True
plotter.camera.parallel_scale = 4.65

if SAVE_IMAGE:
    plotter.show(screenshot=SAVE_IMAGE)
else:
    plotter.show()
