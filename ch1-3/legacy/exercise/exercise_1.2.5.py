"""
연습문제 1.2 5번

세 벡터 a = (3, -2, 1), b = (1, -3, 5), c = (2, 1, -4)는 직각삼각형을 이룸을 보여라
"""
import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([3, -2, 1])
b = np.array([1, -3, 5])
c = np.array([2, 1, -4])

O = np.array([0, 0, 0])

fig = pv.Plotter()

p3d.add_vector(fig, O, a, name = "a", color = "red")
p3d.add_vector(fig, O, b, name = "b", color = "green", opacity = 0.2)
p3d.add_vector(fig, O, c, name = "c", color = "blue")

p3d.add_angle(fig, O, a, c, radius = 0.4)

p3d.add_vector(fig, c, b, name = "b", color = "green")

p3d.add_coordinate_axes(fig)

fig.show()