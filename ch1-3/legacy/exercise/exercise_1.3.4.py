"""
연습문제 1.3 4번

세 벡터 a = (3, -1, 2), b = (2, 1, -1), c = (1, -2, 2)에서
(a x b) x c와 a x (b x c)를 구하여, 일반적으로 서로 같지 않음을 보여라
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([3, -1, 2])
b = np.array([2, 1, -1])
c = np.array([1, -2, 2])

O = np.array([0, 0, 0])

left_case = np.cross(np.cross(a, b), c)
right_case = np.cross(a, np.cross(b, c))

fig = pv.Plotter()

p3d.add_vector(fig, O, a, name = "a")
p3d.add_vector(fig, O, b, name = "b")
p3d.add_vector(fig, O, c, name = "c")

p3d.add_vector(fig, O, left_case, color = "red", show_endpoint = True, name = "(a x b) x c")
p3d.add_vector(fig, O, right_case, color = "blue", show_endpoint = True, name = "a x (b x c)")

p3d.add_coordinate_axes(fig, opacity = 0.5, axis_length = 5)

fig.show()