"""
그림 1.5

점 a를 지나고 n에 수직인 평면
<x - a, n> = 0
"""

import numpy as np
import plot_tools_diffgeo as ptd


O = np.array([0, 0, 0])

a = np.array([1.2, 1.5, 1.2])
n = np.array([0.2, -0.4, 1.0])

if np.allclose(n, 0):
    raise ValueError("n은 영벡터일 수 없습니다.")

n_hat = n / np.linalg.norm(n)

reference = np.eye(3)[np.argmin(np.abs(n_hat))]

u = np.cross(n_hat, reference)
u = u / np.linalg.norm(u)

v = np.cross(n_hat, u)

x = a + u + 0.4 * v

fig = ptd.create_figure_3d()

ptd.add_plane_3d(fig, a, u, v, color = "cyan", opacity = 0.35, u_range = (-1, 1.5), v_range = (-1, 1.5), show_edges = True)

ptd.add_vector_3d(fig, O, n, name=r"$n$", color = "cyan")
ptd.add_vector_3d(fig, a, n, name=r"$n$")
ptd.add_vector_3d(fig, a, x - a, name=r"$x-a$")

ptd.add_angle_3d(fig, a, x - a, n)

ptd.add_points_3d(fig, [a])
ptd.add_labels_3d(fig, [a, x], [r"$a$", r"$x$"])

ptd.add_coordinate_axes_3d(fig, axis_length=3.2, positive_only=True, show_labels=False)
ptd.add_labels_3d(fig, [[3.4, 0, 0], [0, 3.4, 0], [0, 0, 3.4]], [r"$x_1$", r"$x_2$", r"$x_3$"])

fig.show()