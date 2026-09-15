"""
예제 1.2.6

E^3에서 (1, 2, 3)과 (4, -5, 2)는 직교한다. 왜냐하면
    <(1, 2, 3), (4, -5, 2)> = 1*4 + 2*(-5) + 3*2 = 0
이기 때문이다.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([1, 2, 3])
b = np.array([4, -5, 2])
O = np.array([0, 0, 0])

fig = pv.Plotter()
p3d.add_vector(fig, O, a, color = "red")
p3d.add_vector(fig, O, b, color = "blue")

fig.add_point_labels(
    [a, b],
    [
        f"a = ({a[0]}, {a[1]}, {a[2]})",
        f"b = ({b[0]}, {b[1]}, {b[2]})",
    ],
    show_points = False,
    shape = None,
    font_size = 16
)

p3d.add_angle(fig, O, a, b)

p3d.add_coordinate_axes(fig)

fig.show()