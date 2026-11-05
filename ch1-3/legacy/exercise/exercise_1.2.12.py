"""
예제 1.2.12

두 벡터 2e₁ - e₂ + 3e₃, e₁ + 2e₂ + 9e₃와 직교하는 단위벡터를 구하여라.
""" 

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

e1 = np.array([1, 0, 0])
e2 = np.array([0, 1, 0])
e3 = np.array([0, 0, 1])
O = np.array([0, 0, 0])

a = np.array([2, -1, 3])
b = np.array([1, 2, 9])

c = np.cross(a,b)/np.linalg.norm(np.cross(a,b))

fig = pv.Plotter()

p3d.add_vector(fig, O, e1, color = "black", name = "$e_1$")
p3d.add_vector(fig, O, e2, color = "black", name = "$e_2$")
p3d.add_vector(fig, O, e3, color = "black", name = "$e_3$")

p3d.add_vector(fig, O, a, color = "red", opacity = 0.5)
p3d.add_vector(fig, O, b, color = "red", opacity = 0.5)
p3d.add_vector(fig, O, c, color = "blue")

fig.add_point_labels(
    [a, b, c],
    [
        "$(2,-1,3)$",
        "$(1,2,9)$",
        r"$(-\frac{3}{\sqrt{19}}, -\frac{3}{\sqrt{19}}, \frac{1}{\sqrt{19}})$"
    ],
    show_points=False,
    shape=None,
    font_size=16,
    always_visible=True,
)

p3d.add_angle(fig, O, a, c)
p3d.add_angle(fig, O, b, c)

p3d.add_coordinate_axes(fig, opacity = 0.5, show_arrow = False, show_labels = False, axis_length = 5)

fig.show()