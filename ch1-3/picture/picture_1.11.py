"""
그림 1.11

V(x₁, x₂) = x₂ e₁ - x₁ e₂
"""

import numpy as np
import plot_tools_diffgeo as ptd


O = np.array([0, 0])


def V(x):
    x1, x2 = x
    return np.array([x2, -x1])


x = np.array([1.1, 1.7])

sample_points = np.array([
    [-1.0, -0.8],
    [-0.8,  0.5],
    [ 0.6, -1.3],
])

fig = ptd.create_figure_2d()

ptd.add_coordinate_axes_2d(fig, (-3.2, 3.8), (-3.2, 3.2), x_label=r"$x_1$", y_label=r"$x_2$")
ptd.add_points_2d(fig, [O, x, *sample_points])

ptd.add_segment_2d(fig, O, x, color="gray", dash="dash")
ptd.add_vector_2d(fig, x, V(x))

for q in sample_points:
    ptd.add_segment_2d(fig, O, q, color="gray", dash="dash")
    ptd.add_vector_2d(fig, q, V(q))

ptd.add_labels_2d(
    fig,
    [O, x, x + V(x) / 2],
    [r"$O$", r"$(x_1,x_2)$", r"$(x_2,-x_1)$"],
)

fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)

fig.show()