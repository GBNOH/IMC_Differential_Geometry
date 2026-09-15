"""
연습문제 1.3 2번

두 벡터 a = (2, -6, -3)과 b = (4, 3, -1)에 직교하는 단위벡터를 구하여라.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([2, -6, -3])
b = np.array([4, 3, -1])

O = np.array([0, 0, 0])

unit_axb = np.cross(a,b)/np.linalg.norm(np.cross(a,b))

fig = pv.Plotter()

p3d.add_vector(fig, O, a, name = "a", show_endpoint = True)
p3d.add_vector(fig, O, b, name = "b", show_endpoint = True)
p3d.add_vector(fig, O, unit_axb, name = r"$\frac{a x b}{\|a x b\|}$", color = "red")

p3d.add_angle(fig, O, a, unit_axb, radius = 0.2)
p3d.add_angle(fig, O, b, unit_axb, radius = 0.2)

p3d.add_coordinate_axes(fig, axis_length = 6)

fig.show()