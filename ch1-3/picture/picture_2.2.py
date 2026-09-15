import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d()

O = np.array([0, 0, 0])

a = 2.0

def alpha(t):
    return np.array([a * np.cos(t), a * np.sin(t)])


ptd.add_coordinate_axes_2d(fig, (-3, 3), (-3, 3), show_labels=False)
ptd.add_parametric_curve_2d(fig, alpha, 0, 2 * np.pi)
ptd.add_segment_2d(fig, O[:2], [a, 0])
ptd.add_arc_2d(fig, O[:2], [a, 0], label=r"$a$")

ptd.add_labels_2d(
    fig,
    [O[:2], [3, 0], [0, 3]],
    [r"$O$", r"$x$", r"$y$"],
)

fig.show()

### 9/14 해당 곡선을 3D에서 그릴지 고민중입니다.