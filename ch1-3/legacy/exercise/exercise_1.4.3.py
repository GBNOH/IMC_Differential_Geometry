"""
연습문제 1.4 3번

원점을 지나고, 평면 2x - y + 3z = 1에 평행한 평면의 방정식을 구하여라
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

O = np.array([0, 0, 0])

P = np.array([0, -1, 0])

n = np.array([2, -1, 3])

fig = pv.Plotter()

plane1 = pv.Plane(center=P, direction=n, i_size=8, j_size=8)
plane2 = pv.Plane(center=O, direction=n, i_size=8, j_size=8)
fig.add_mesh(plane1, color="turquoise", opacity=0.3, show_edges=True, edge_color="gray", line_width=1)
fig.add_mesh(plane2, color="lightcoral", opacity=0.7, show_edges=True, edge_color="gray", line_width=1)

p3d.add_vector(fig, O, n, name="n", color="red")

p3d.add_coordinate_axes(fig, axis_length=4, opacity=0.5)

fig.show()