"""
그림 1.13

주면표구장
G_1 = cos(theta) U_1 + sin(theta) U_2
G_2 = -sin(theta) U_1 + cos(theta) U_2
G_3 = U_3
"""

import numpy as np
import plot_tools_diffgeo as ptd


def add_dashed_segment(fig, point1, point2, dash_length=0.08, gap_length=0.06):
    point1 = np.asarray(point1, dtype=float)
    point2 = np.asarray(point2, dtype=float)

    vector = point2 - point1
    length = np.linalg.norm(vector)

    if np.isclose(length, 0):
        raise ValueError("두 점은 서로 달라야 합니다.")

    direction = vector / length
    s = 0.0

    while s < length:
        t = min(s + dash_length, length)
        ptd.add_segment_3d(fig, point1 + s * direction, point1 + t * direction)
        s += dash_length + gap_length


O = np.array([0, 0, 0])

r = 1.4
theta = np.pi / 6
z = 1.2

p = np.array([r * np.cos(theta), r * np.sin(theta), z])
q = np.array([r * np.cos(theta), r * np.sin(theta), 0])
p0 = np.array([0, 0, z])

U1 = np.array([1, 0, 0])
U2 = np.array([0, 1, 0])
U3 = np.array([0, 0, 1])

G1 = np.cos(theta) * U1 + np.sin(theta) * U2
G2 = -np.sin(theta) * U1 + np.cos(theta) * U2
G3 = U3

fig = ptd.create_figure_3d()

ptd.add_points_3d(fig, [O, p])
ptd.add_vector_3d(fig, p, G1, name=r"$G_1$", color = "cyan", opacity = 0.5, text_color = "black")
ptd.add_vector_3d(fig, p, G2, name=r"$G_2$", color = "cyan", opacity = 0.5, text_color = "black")
ptd.add_vector_3d(fig, p, G3, name=r"$G_3$", color = "cyan", opacity = 0.5, text_color = "black")

ptd.add_segment_3d(fig, O, q)
ptd.add_segment_3d(fig, q, p, color="gray", opacity=0.6)
add_dashed_segment(fig, p0, p)

ptd.add_labels_3d(fig, [p, 0.5 * q, 0.5 * (q + p)], [r"$p$", r"$r$", r"$z$"])

ptd.add_angle_3d(fig, O, np.array([1, 0, 0]), q, label=r"$\theta$", radius = 0.5)

ptd.add_coordinate_axes_3d(fig, axis_length=3, positive_only=True, show_labels=False)
ptd.add_labels_3d(fig, [[3.2, 0, 0], [0, 3.2, 0], [0, 0, 3.2]], [r"$x$", r"$y$", r"$z$"])

fig.show()