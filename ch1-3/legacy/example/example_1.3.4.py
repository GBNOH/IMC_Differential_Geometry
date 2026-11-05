"""
예제 1.3.4
a = (3, 2, 1), b = (1, -3, 4)를 이웃하는 두 변으로 하는 평행사변형의 넓이 A를 구하여라
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([3, 2, 1])
b = np.array([1, -3, 4])

O = np.array([0, 0, 0])

axb = np.cross(a,b)

fig = pv.Plotter()

p3d.add_vector(fig, O, a, name = "a", show_endpoint = True)
p3d.add_vector(fig, O, b, name = "b", show_endpoint = True)
p3d.add_vector(fig, O, axb, name = r"$\|a x b\| = 11\sqrt{3}$", show_endpoint = True, color = "red")

p3d.add_angle(fig, O, a, axb, radius = 1)
p3d.add_angle(fig, O, b, axb, radius = 1)

p3d.add_coordinate_axes(fig, axis_length = 7)

fig.show()