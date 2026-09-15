"""
예제 1.4.5

a = (0, 1, 0)를 지나고 u = (1, 0, 0)와 v = (-1, 0, 1)에 평행한 평면의 방정식은 x = λu + μv + a = (λ - μ, 1 , μ)이다.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([0, 1, 0])

u = np.array([1, 0, 0])
v = np.array([-1, 0, 1])

O = np.array([0, 0, 0])

n = np.cross(u, v)

fig = pv.Plotter()

plane = pv.Plane(center=a, direction=n, i_size=4, j_size=4)
fig.add_mesh(plane, color="turquoise", opacity=0.3, show_edges=True, edge_color="gray")

fig.add_point_labels(
    [a],
    ["a"],
    show_points=False,
    shape=None,
    text_color="black",
    font_size=16,
    always_visible=True,
)

p3d.add_vector(fig, a, u, name="u")
p3d.add_vector(fig, a, v, name="v")
p3d.add_vector(fig, a, n, name="n", color="red")

p3d.add_angle(fig, a, n, u)
p3d.add_angle(fig, a, n, v)

fig.show()