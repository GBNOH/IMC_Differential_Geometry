"""
예제 1.2.11
다음 벡터와 같은 방향의 단위벡터를 구하여라
(1) a = (1, 1, 1)
(2) b = (3, 0, 4)
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([1, 1, 1])
b = np.array([3, 0, 4])
O = np.array([0, 0, 0])

a_unit = a / np.linalg.norm(a)
b_unit = b / np.linalg.norm(b)

fig = pv.Plotter()
p3d.add_vector(fig, O, a, color = "red", opacity = 0.5)
p3d.add_vector(fig, O, b, color = "blue", opacity = 0.5)
p3d.add_vector(fig, O, a_unit, color = "black")
p3d.add_vector(fig, O, b_unit, color = "black")

fig.add_point_labels(
    [a, b, a_unit, b_unit], 
    [
        f"({a[0]}, {a[1]}, {a[2]})",
        f"({b[0]}, {b[1]}, {b[2]})",
        fr"$\frac{{a}}{{\|a\|}}$",
        fr"$\frac{{b}}{{\|b\|}}$"
    ],
    shape = None,
    font_size = 16
)

sphere = pv.Sphere(radius=1.0, center=O, theta_resolution=30,phi_resolution=30)
fig.add_mesh(sphere, color="gray", line_width=1, opacity=0.5)

p3d.add_coordinate_axes(fig)
fig.show()