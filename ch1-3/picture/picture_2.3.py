import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])

a = 2
b = 0.4
H = 4 * np.pi * b
L = max(2.4 * a, H + 0.6)

def alpha(t):
    return np.array([a * np.cos(t), a * np.sin(t), b * t])


t0 = 0.5 * np.pi
t1 = 2.5 * np.pi

P0 = alpha(t0)
P1 = alpha(t1)

mid_xy = np.array([P0[0], P0[1], 0.0])
mid_xy = 1.45 * mid_xy / np.linalg.norm(mid_xy)

M = np.array([mid_xy[0], mid_xy[1], (P0[2] + P1[2]) / 2])
w = np.array([0.0, 0.0, P1[2] - P0[2]])

ptd.add_coordinate_axes_3d(fig, axis_length=L, show_labels=False, positive_only=True)
ptd.add_labels_3d(fig, [O, [1.05 * L, 0, 0], [0, 1.05 * L, 0], [0, 0, 1.05 * L]], [r"$O$", r"$x$", r"$y$", r"$z$"])

ptd.add_cylinder_3d(fig, radius=a, height=H, center=[0, 0, H / 2], opacity=0.25)
ptd.add_parametric_curve_3d(fig, alpha, 0, 4 * np.pi)

ptd.add_plane_3d(fig, [0, 0, P0[2]], [1.2 * a, 0, 0], [0, 1.2 * a, 0], opacity=0.12)
ptd.add_plane_3d(fig, [0, 0, P1[2]], [1.2 * a, 0, 0], [0, 1.2 * a, 0], opacity=0.12)

ptd.add_points_3d(fig, [P0, P1], point_size=12)
ptd.add_labels_3d(fig, [P0, P1], [r"$\alpha(t)$", r"$\alpha(t+2\pi)$"])

ptd.add_segment_3d(fig, [0, 0, P0[2]], P0)
ptd.add_segment_3d(fig, [0, 0, P1[2]], P1)

ptd.add_vector_3d(fig, M, 0.5 * w, shaft_radius=0.01, tip_radius=0.04, tip_length=0.12)
ptd.add_vector_3d(fig, M, -0.5 * w, shaft_radius=0.01, tip_radius=0.04, tip_length=0.12)

ptd.add_labels_3d(fig, [M, [0, 0, -0.6]], [r"$2\pi b$", r"$b>0$"])

fig.show()