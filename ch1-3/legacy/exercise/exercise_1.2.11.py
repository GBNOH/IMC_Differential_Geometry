"""
연습문제 1.2 11번

u = 3e₁ + 2e₂ - e₃, v = e₁ + e₂ + 2e₃ 일 때, v를 u 위에 내린 정사영 Pu(v)를 구하여라
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

e1 = np.array([1, 0, 0])
e2 = np.array([0, 1, 0])
e3 = np.array([0, 0, 1])
O = np.array([0, 0, 0])

u = np.array([3, 2, -1])
v = np.array([1, 1, 2])

projection_of_v_onto_u = np.dot(v,u)/np.dot(u,u) * u

fig = pv.Plotter()

p3d.add_vector(fig, O, e1, color = "black", name = "$e_1$")
p3d.add_vector(fig, O, e2, color = "black", name = "$e_2$")
p3d.add_vector(fig, O, e3, color = "black", name = "$e_3$")

p3d.add_vector(fig, O, u, color = "red", opacity = 0.5, name = "u")
p3d.add_vector(fig, O, v, color = "blue", opacity = 0.5, name = "v")

p3d.add_vector(fig, O, projection_of_v_onto_u, color = "black")

line = pv.Line(-1 * u / np.linalg.norm(u), 4 * u / np.linalg.norm(u))
fig.add_mesh(line, color="red", line_width=3, opacity=0.5)

fig.add_mesh(pv.Line(v, projection_of_v_onto_u), color="black", line_width=3)

p3d.add_angle(
    fig,
    projection_of_v_onto_u,
    O - projection_of_v_onto_u,
    v - projection_of_v_onto_u,
    radius=0.2,
    color="black"
)

p3d.add_coordinate_axes(fig, opacity = 0.5, show_arrow = False, show_labels = False)

fig.show()