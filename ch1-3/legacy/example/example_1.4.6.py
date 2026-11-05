"""
예제 1.4.6

세 점 A (-3, 0, -1), B (-2, 3, 2), C (1, 1, 3)을 지나는 평면의 방정식을 구하여라.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

A = np.array([-3, 0, -1])
B = np.array([-2, 3, 2])
C = np.array([1, 1, 3])

AB = B - A
AC = C - A

n = np.cross(AB, AC)

fig = pv.Plotter()

plane = pv.Plane(center = (A + B + C)/3, direction = n, i_size = 8, j_size = 8)
fig.add_mesh(plane, color = "turquoise", opacity = 0.5)

p3d.add_vector(fig, A, AB, name = r"$\overrightarrow{AB}$")
p3d.add_vector(fig, A, AC, name = r"$\overrightarrow{AC}$")
p3d.add_vector(fig, A, n, color = "red", name = "n")

p3d.add_angle(fig, A, AB, n, radius = 0.5)
p3d.add_angle(fig, A, AC, n, radius = 0.5)

fig.add_point_labels([A, B, C], ["A", "B", "C"], show_points = False, always_visible = True, shape = None)

fig.show()