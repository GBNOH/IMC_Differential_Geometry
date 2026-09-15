"""
연습문제 1.4 4번

세 점 A(1, 4, 6), B(-2, 5, -1), C(1, -1, 1)을 지나는 평면에 수직인 한 벡터를 구하여라.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

A = np.array([1, 4, 6])
B = np.array([-2, 5, -1])
C = np.array([1, -1, 1])

O = np.array([0, 0, 0])

AB = B - A
AC = C - A
n = np.cross(AB, AC)

fig = pv.Plotter()

plane = pv.Plane(center = (A + B + C)/3, direction = n, i_size = 10, j_size = 10)
fig.add_mesh(plane, "turquoise", show_edges = True, opacity = 0.5)

fig.add_points(np.array([A, B, C]), render_points_as_spheres = True)
fig.add_point_labels([A, B, C], ["A", "B", "C"], show_points = False, shape = True, always_visible = True)
p3d.add_vector(fig, (A + B + C)/3, n / np.linalg.norm(n), color = "red", name = r"$\frac{AB x AC}{\|AB x AC\|}$")
p3d.add_vector(fig, A, AB)
p3d.add_vector(fig, A, AC)

p3d.add_coordinate_axes(fig)

fig.show()