"""
예제 1.2.9

두 벡터 (2,2,-1)과 (6,-3,2)에 대하여 내적의 기하학적 성질에 의해 이루는 각의 크기를 구할 수 있다.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([2, 2, -1])
b = np.array([6, -3, 2])

O = np.array([0, 0, 0])

fig = pv.Plotter()
p3d.add_vector(fig, O, a, color = "red")
p3d.add_vector(fig, O, b, color = "green")

fig.add_point_labels(
    [a, b],
    [
        f"({a[0]}, {a[1]}, {a[2]})",
        f"({b[0]}, {b[1]}, {b[2]})",
    ],
    show_points = False,
    shape = None,
    font_size = 16
)

p3d.add_angle(fig, O, a, b, show_angle_value = True)

p3d.add_coordinate_axes(fig)

fig.show()