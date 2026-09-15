"""
예제 1.2.12 / 그림 1.2

{e_1, e_2, e_3}은 R^3의 표준 정규직교기저이다.
"""

import numpy as np
import plot_tools_diffgeo as ptd


e1 = np.array([1, 0, 0])
e2 = np.array([0, 1, 0])
e3 = np.array([0, 0, 1])
O = np.array([0, 0, 0])

fig = ptd.create_figure_3d()

ptd.add_frame_3d(fig, O, e1, e2, e3, names=(r"$e_1$", r"$e_2$", r"$e_3$"), colors = ("cyan", "cyan", "cyan"))

ptd.add_angle_3d(fig, O, e1, e2)
ptd.add_angle_3d(fig, O, e2, e3)
ptd.add_angle_3d(fig, O, e1, e3)

ptd.add_coordinate_axes_3d(fig, axis_length=2, positive_only=True, show_labels=False)
ptd.add_labels_3d(fig, [[2.1, 0, 0], [0, 2.1, 0], [0, 0, 2.1]], [r"$x_1$", r"$x_2$", r"$x_3$"])

fig.show()