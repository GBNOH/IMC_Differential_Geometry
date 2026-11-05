"""
그림 1.12

자연표구장
U_1(p) = (1,0,0)_p, U_2(p) = (0,1,0)_p, U_3(p) = (0,0,1)_p
"""

import numpy as np
import plot_tools_diffgeo as ptd


O = np.array([0, 0, 0])

p = np.array([0.9, 1.0, 1.2])

e1 = np.array([1, 0, 0])
e2 = np.array([0, 1, 0])
e3 = np.array([0, 0, 1])

fig = ptd.create_figure_3d()

ptd.add_frame_3d(fig, p, e1, e2, e3, names=(r"$U_1(p)$", r"$U_2(p)$", r"$U_3(p)$"), colors = ("cyan", "cyan", "cyan"), opacity = 0.5, text_colors = ("black", "black", "black"))
ptd.add_points_3d(fig, [p])
ptd.add_labels_3d(fig, [O, p], [r"$O$", r"$p$"], font_size = 20)

ptd.add_coordinate_axes_3d(fig, axis_length=3, positive_only=True, show_labels=False)
ptd.add_labels_3d(fig, [[3.2, 0, 0], [0, 3.2, 0], [0, 0, 3.2]], [r"$x_1$", r"$x_2$", r"$x_3$"])

fig.show()