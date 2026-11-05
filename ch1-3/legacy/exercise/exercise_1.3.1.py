"""
연습문제 1.3 1번

두 벡터 a = (1, 2, -1)과 b = (-1, 0, 3)에서 a x b와 ||a x b||를 구하여라.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([1, 2, -1])
b = np.array([-1, 0, 3])

O = np.array([0, 0, 0])

axb = np.cross(a,b)

fig = pv.Plotter()

p3d.add_vector(fig, O, a, name = "a", show_endpoint = True)
p3d.add_vector(fig, O, b, name = "b", show_endpoint = True)

p3d.add_vector(fig, O, axb, name = "a x b", show_endpoint = True, color = "red")
p3d.add_angle(fig, O, a, axb, radius = 0.5)
p3d.add_angle(fig, O, b, axb, radius = 0.5)

p3d.add_coordinate_axes(fig, axis_length = 4)

fig.show()