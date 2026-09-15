"""
연습문제 1.4 2번

점 (0, -1, 3)을 지나고 점 (2, 1, -3)에 수직인 평면의 방정식을 구하여라.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([0, -1, 3])
b = np.array([2, 1, -3])

O = np.array([0, 0, 0])

fig = pv.Plotter()
plane = pv.Plane(center = a, direction = b, i_size = 5, j_size = 5)
fig.add_mesh(plane, color = "turquoise", show_edges = True, opacity = 0.5)

fig.add_point_labels([a], ["a"], shape = None)
p3d.add_vector(fig, a, b, color = "red", name = "b")

p3d.add_coordinate_axes(fig, axis_length = 5)

fig.show()