"""
연습문제 1.2 10번 (a)

a = (-1, 1, -2), b = (1, -1, 1)일 때, a를 b 위에 내린 정사영과 b를 a 위에 내린 정사영을 구하라.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([-1, 1, -2])
b = np.array([1, -1, 1])

O = np.array([0, 0, 0])

projection_of_a_onto_b = np.dot(a,b)/np.dot(b,b) * b
projection_of_b_onto_a = np.dot(a,b)/np.dot(a,a) * a

fig = pv.Plotter()

p3d.add_vector(fig, O, a, name = "a", color = "red")
p3d.add_vector(fig, O, b, name = "b", color = "blue")
p3d.add_vector(fig, O, projection_of_a_onto_b, name = "$P_b (a)$", color = "black")
p3d.add_vector(fig, O, projection_of_b_onto_a, name = "$P_a (b)$", color = "black")


a_line = pv.Line(-2 * a / np.linalg.norm(a), 3 * a / np.linalg.norm(a))
b_line = pv.Line(-3 * b / np.linalg.norm(b), 2 * b / np.linalg.norm(b))

fig.add_mesh(a_line, color="red", line_width=3, opacity=0.5)
fig.add_mesh(b_line, color="blue", line_width=3, opacity=0.5)

fig.add_mesh(pv.Line(a, projection_of_a_onto_b), color="black", line_width=3)
fig.add_mesh(pv.Line(b, projection_of_b_onto_a), color="black", line_width=3)

p3d.add_angle(
    fig,
    projection_of_a_onto_b,
    O - projection_of_a_onto_b,
    a - projection_of_a_onto_b,
    radius=0.2,
    color="black"
)

p3d.add_angle(
    fig,
    projection_of_b_onto_a,
    O - projection_of_b_onto_a,
    b - projection_of_b_onto_a,
    radius=0.2,
    color="black"
)

p3d.add_coordinate_axes(fig)

fig.show()