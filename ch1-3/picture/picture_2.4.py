import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d()

O = np.array([0, 0, 0])

def alpha(t):
    return np.array([t + 3, t**2 + 3, 0])

def alpha_xy(t):
    return alpha(t)[:2]


P = alpha(0)

ptd.add_coordinate_axes_2d(fig, (-2, 8), (-1, 20), x_label=r"$x$", y_label=r"$y$")
ptd.add_parametric_curve_2d(fig, alpha_xy, -4, 4)

ptd.add_segment_2d(fig, [P[0], 0], P[:2], dash="dot")
ptd.add_segment_2d(fig, [0, P[1]], P[:2], dash="dot")

ptd.add_points_2d(fig, P[:2])

ptd.add_labels_2d(
    fig,
    [O[:2], [3, 0], [0, 3], [0, 12], P[:2]],
    [r"$O$", r"$3$", r"$3$", r"$12$", r"$(3,3)$"],
)

fig.show()