"""
그림 1.10

p = (1, 1, 3), a = (2, 3, 2)일 때
접벡터 a_p를 나타낸다.
"""

import numpy as np
import plot_tools_diffgeo as ptd


O = np.array([0, 0, 0])

p = np.array([1, 1, 3])
a = np.array([2, 3, 2])

p_plus_a = p + a

fig = ptd.create_figure_3d()

ptd.add_vector_3d(fig, p, a, color = "cyan", opacity = 0.5)

ptd.add_points_3d(fig, [p, p_plus_a])
ptd.add_labels_3d(
    fig,
    [O, p, p_plus_a, p + 0.5 * a],
    [
        r"$O$",
        r"$p=(1,1,3)$",
        r"$p+a=(3,4,5)$",
        r"$a_p$",
    ],
)

ptd.add_coordinate_axes_3d(fig, axis_length=6, positive_only=True, show_labels=False)
ptd.add_labels_3d(fig, [[6.2, 0, 0], [0, 6.2, 0], [0, 0, 6.2]], [r"$x_1$", r"$x_2$", r"$x_3$"])

fig.show()