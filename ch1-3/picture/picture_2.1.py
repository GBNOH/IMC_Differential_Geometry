import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])

p = np.array([0.0, 1.4, 0.8])
q = np.array([0.0, 1.3, 0.7])

t = 1.0
alpha_t = p + t * q

line_points = np.array([p - 0.4 * q, p + 1.2 * q])

ptd.add_coordinate_axes_3d(fig, axis_length=3.0, show_labels=False, positive_only=True)
ptd.add_labels_3d(fig, [O, [3.1, 0, 0], [0, 3.1, 0], [0, 0, 3.1]], [r"$O$", r"$x$", r"$y$", r"$z$"])
ptd.add_curve_3d(fig, line_points)
ptd.add_vector_3d(fig, p, q, color="deepskyblue")
ptd.add_points_3d(fig, [p, alpha_t], point_size=12)
ptd.add_labels_3d(fig, [p, p + 0.55 * q, alpha_t], [r"$p$", r"$q$", r"$\alpha(t)$"])

fig.show()