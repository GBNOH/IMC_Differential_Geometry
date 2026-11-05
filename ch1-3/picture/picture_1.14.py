"""
그림 1.14

구면표구장

F_1 = cos(psi)cos(theta)U_1 + cos(psi)sin(theta)U_2 + sin(psi)U_3
F_2 = -sin(theta)U_1 + cos(theta)U_2
F_3 = -sin(psi)cos(theta)U_1 - sin(psi)sin(theta)U_2 + cos(psi)U_3
"""

import numpy as np
import plot_tools_diffgeo as ptd


def add_dashed_arc(fig, curve, t_min, t_max, n=12):
    t = np.linspace(t_min, t_max, 2 * n + 1)

    for i in range(0, 2 * n, 2):
        ptd.add_parametric_curve_3d(fig, curve, t[i], t[i + 1], color="gray")


O = np.array([0, 0, 0])

rho = 1.6
theta = np.pi / 3
psi = np.pi / 5

U1 = np.array([1, 0, 0])
U2 = np.array([0, 1, 0])
U3 = np.array([0, 0, 1])

F1 = np.cos(psi) * np.cos(theta) * U1 + np.cos(psi) * np.sin(theta) * U2 + np.sin(psi) * U3
F2 = -np.sin(theta) * U1 + np.cos(theta) * U2
F3 = -np.sin(psi) * np.cos(theta) * U1 - np.sin(psi) * np.sin(theta) * U2 + np.cos(psi) * U3

p = rho * F1
er = np.cos(theta) * U1 + np.sin(theta) * U2
q = rho * np.cos(psi) * er
r = rho * er


def meridian(phi):
    return rho * (np.cos(phi) * er + np.sin(phi) * U3)


def arc_xz(phi):
    return rho * (np.cos(phi) * U1 + np.sin(phi) * U3)


def arc_xy(phi):
    return rho * (np.cos(phi) * U1 + np.sin(phi) * U2)


fig = ptd.create_figure_3d()

ptd.add_frame_3d(fig, p, F1, F2, F3, names=(r"$F_1$", r"$F_2$", r"$F_3$"), colors = ("cyan", "cyan", "cyan"), opacity=0.5, text_colors=("black", "black", "black"))
ptd.add_points_3d(fig, [p])
ptd.add_segment_3d(fig, O, p)
ptd.add_segment_3d(fig, O, r)
ptd.add_segment_3d(fig, q, p)

add_dashed_arc(fig, meridian, 0, np.pi / 2)
add_dashed_arc(fig, arc_xz, 0, np.pi / 2)
add_dashed_arc(fig, arc_xy, 0, np.pi / 2)

ptd.add_angle_3d(fig, O, U1, er, radius=0.5, label=r"$\theta$")
ptd.add_angle_3d(fig, O, er, F1, radius=0.6)

ptd.add_labels_3d(fig, [p, 0.5 * p, 0.5 * q], [r"$p$", r"$\rho$", r"$r$"])
ptd.add_coordinate_axes_3d(fig, axis_length=3, positive_only=True)

fig.show()