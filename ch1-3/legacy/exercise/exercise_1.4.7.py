"""
연습문제 1.4 7번

두 평면 10x + 2y - 2z = 5와 5x + y - z = 1 사이의 거리를 구하여라
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

n = np.array([5, 1, -1])

P1 = (2.5 / np.dot(n,n)) * n
P2 = (1 / np.dot(n,n)) * n

distance = np.linalg.norm(P1 - P2)

fig = pv.Plotter()

plane1 = pv.Plane(center=P1, direction=n, i_size=5, j_size=5)
plane2 = pv.Plane(center=P2, direction=n, i_size=5, j_size=5)
fig.add_mesh(plane1, color="turquoise", opacity=0.35, show_edges=True, edge_color="gray")
fig.add_mesh(plane2, color="lightcoral", opacity=0.5, show_edges=True, edge_color="gray")

fig.add_mesh(pv.Line(P1, P2), color="red", line_width=4)
fig.add_point_labels(
    [(P1 + P2) / 2],
    [r"$d = \frac{\sqrt{3}}{6}$"],
    show_points=False,
    shape=None,
    text_color="red",
    font_size=16,
    always_visible=True,
)

fig.add_point_labels([P1 + np.array([-0.5,1,-1])], ["10x + 2y - 2z = 5"], show_points=False, shape=None, text_color="turquoise")
fig.add_point_labels([P2 + np.array([-0.5,1,-1])], ["5x + y - z = 1"], show_points=False, shape=None, text_color="lightcoral")

p3d.add_coordinate_axes(fig, axis_length=3, opacity=0.5)

fig.show()