import os

import numpy as np
import pyvista as pv


R_MAX = np.sqrt(2.0)
# Change only this value to exaggerate or flatten the vertical direction:
# 1.0 = reference proportions, 1.2 = 20% taller, 0.8 = 20% flatter.
HEIGHT_SCALE = 1.0
r = np.linspace(0.0, R_MAX, 90)
theta = np.linspace(0.0, 2.0 * np.pi, 240)
r_grid, theta_grid = np.meshgrid(r, theta)

u = r_grid * np.cos(theta_grid)
v = r_grid * np.sin(theta_grid)
x1 = u + v
x2 = u - v
x3 = HEIGHT_SCALE * (u**2 + v**2)
surface = pv.StructuredGrid(x1, x2, x3)


def polyline(points):
    return pv.lines_from_points(np.asarray(points), close=False)


def dashed_polyline(points, dash_points=5, gap_points=4):
    """Create one PolyData containing disconnected pieces of a dashed curve."""
    points = np.asarray(points)
    kept_points = []
    cells = []
    cursor = 0
    start = 0
    while start < len(points) - 1:
        stop = min(start + dash_points, len(points))
        piece = points[start:stop]
        if len(piece) >= 2:
            kept_points.extend(piece)
            cells.extend([len(piece), *range(cursor, cursor + len(piece))])
            cursor += len(piece)
        start += dash_points + gap_points

    dashed = pv.PolyData(np.asarray(kept_points))
    dashed.lines = np.asarray(cells)
    return dashed


def add_axis(plotter, direction, length, tip_length=0.14, tip_radius=0.05):
    """Add a thin, constant-width axis and a small solid arrowhead."""
    direction = np.asarray(direction, dtype=float)
    direction /= np.linalg.norm(direction)
    end = length * direction
    shaft_end = end - tip_length * direction

    plotter.add_mesh(
        pv.Line((0.0, 0.0, 0.0), shaft_end),
        color="black",
        line_width=2.0,
    )
    plotter.add_mesh(
        pv.Cone(
            center=end - 0.5 * tip_length * direction,
            direction=direction,
            height=tip_length,
            radius=tip_radius,
            resolution=24,
        ),
        color="black",
    )


SAVE_IMAGE = os.environ.get("PYVISTA_SCREENSHOT")
plotter = pv.Plotter(
    off_screen=SAVE_IMAGE is not None,
    window_size=(1200, 800),
)
plotter.set_background("white")
plotter.enable_anti_aliasing("ssaa")

# Retain PyVista's default light kit.  It produces the broad cyan-to-white
# gradation of the source illustration without a plastic-looking PBR material.
plotter.add_mesh(
    surface.extract_surface().clean(tolerance=1e-9),
    color="#91ECEB",
    smooth_shading=True,
    show_edges=False,
    ambient=0.85,
    diffuse=0.90,
    specular=0.08,
    specular_power=18,
    reset_camera=False,
)

# Low camera elevation gives the top rim the same shallow ellipse as the source.
camera_target = (0.0, 0.0, HEIGHT_SCALE)
camera_position = (5.0, 1.65, HEIGHT_SCALE + 1.14)

# Boundary: solid camera-facing half and dashed hidden half.
phi_camera = np.arctan2(camera_position[1], camera_position[0])
rim_radius = np.sqrt(2.0) * R_MAX
rim_height = HEIGHT_SCALE * R_MAX**2

phi_front = np.linspace(phi_camera - np.pi / 2, phi_camera + np.pi / 2, 240)
front_rim = np.column_stack(
    (
        rim_radius * np.cos(phi_front),
        rim_radius * np.sin(phi_front),
        np.full_like(phi_front, rim_height),
    )
)

phi_back = np.linspace(phi_camera + np.pi / 2, phi_camera + 3 * np.pi / 2, 180)
back_rim = np.column_stack(
    (
        rim_radius * np.cos(phi_back),
        rim_radius * np.sin(phi_back),
        np.full_like(phi_back, rim_height),
    )
)

plotter.add_mesh(polyline(front_rim), color="#202020", line_width=1.7)
plotter.add_mesh(dashed_polyline(back_rim), color="#303030", line_width=1.5)

# The textbook axes are stylized to compensate for foreshortening.
add_axis(plotter, (1, 0, 0), 6.4)
add_axis(plotter, (0, 1, 0), 4.2)
add_axis(plotter, (0, 0, 1), 3.5 * HEIGHT_SCALE)

label_points = np.array(
    [
        [6.68, 0.00, -0.06],
        [0.00, 4.45, -0.05],
        [0.00, 0.00, 3.72 * HEIGHT_SCALE],
        [0.10, 0.05, -0.14],
    ]
)
plotter.add_point_labels(
    label_points,
    ["x", "y", "z", "O"],
    italic=True,
    bold=False,
    font_size=24,
    text_color="black",
    font_family="times",
    show_points=False,
    shape=None,
    always_visible=True,
    reset_camera=False,
)

plotter.camera_position = [
    camera_position,
    camera_target,
    (0.0, 0.0, 1.0),
]
plotter.camera.parallel_projection = True
plotter.camera.parallel_scale = max(3.05, 2.70 * HEIGHT_SCALE)

# Add the thin visible outline only after the final camera has been selected.
plotter.add_silhouette(surface, color="#202020", line_width=1.4)

if SAVE_IMAGE:
    plotter.show(screenshot=SAVE_IMAGE)
else:
    plotter.show()
