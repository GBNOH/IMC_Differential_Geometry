"""
그림 1.8, 1.9

접벡터 a_q 와 p_O
"""

import numpy as np
import plot_tools_diffgeo as ptd


O = np.array([0, 0, 0])

q = np.array([1, 2, 0])
a = np.array([-1, -1, 1])

p = np.array([2, 1, 1])

if np.allclose(a, 0):
    raise ValueError("a는 영벡터일 수 없습니다.")

if np.allclose(p, 0):
    raise ValueError("p는 영벡터일 수 없습니다.")

qa = q + a

fig = ptd.create_figure_3d()

ptd.add_vector_3d(fig, q, a, opacity = 0.5, color = "cyan")
ptd.add_vector_3d(fig, O, p, opacity = 0.5, color = "cyan")

ptd.add_points_3d(fig, [q, qa, O, p])
ptd.add_labels_3d(
    fig,
    [q, qa, 0.5 * (q + qa), O, p, 0.5 * p],
    [r"$q$", r"$q+a$", r"$a_q$", r"$O$", r"$p$", r"$p_O$"],
)

ptd.add_coordinate_axes_3d(fig, axis_length=2.6, positive_only=True, show_labels=False)
ptd.add_labels_3d(fig, [[2.8, 0, 0], [0, 2.8, 0], [0, 0, 2.8]], [r"$x_1$", r"$x_2$", r"$x_3$"])

fig.show()