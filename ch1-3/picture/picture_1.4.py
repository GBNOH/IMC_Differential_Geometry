"""
그림 1.4

점 a를 지나고 u를 방향벡터로 하는 직선
x = a + tu
"""

import numpy as np
import plot_tools_diffgeo as ptd


O = np.array([0, 0, 0])

a = np.array([0.8, 1.0, 1.4])
u = np.array([0.3, 0.8, 0.2])

if np.allclose(u, 0):
    raise ValueError("u는 영벡터일 수 없습니다.")

t = 1.5
x = a + t * u


def alpha(s):
    return a + s * u


fig = ptd.create_figure_3d()

ptd.add_parametric_curve_3d(fig, alpha, -2.5, 3.0)

ptd.add_vector_3d(fig, O, u, name=r"$u$")
ptd.add_vector_3d(fig, a, t * u, name=r"$tu=x-a$")

ptd.add_points_3d(fig, [O, a, x])
ptd.add_labels_3d(fig, [O, a, x], [r"$O$", r"$a$", r"$x$"])

ptd.add_coordinate_axes_3d(fig, axis_length=3, positive_only=True, show_labels=False)
ptd.add_labels_3d(fig, [[3.2, 0, 0], [0, 3.2, 0], [0, 0, 3.2]], [r"$x_1$", r"$x_2$", r"$x_3$"])

fig.show()