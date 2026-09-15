"""
예제 1.2.7

(1,1,1), (2,1,3), (4,-5,1)은 서로 직교하는 벡터들이다.

직각을 잘 나타내기 위해 인위적으로 각을 표기하였다.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([1, 1, 1])
b = np.array([2, 1, -3])
c = np.array([4, -5, 1])
O = np.array([0, 0, 0])

fig = pv.Plotter()
p3d.add_vector(fig, O, a, color = "red")
p3d.add_vector(fig, O, b, color = "green")
p3d.add_vector(fig, O, c, color = "blue")

fig.add_point_labels(
    [a, b, c],
    [
        f"a = ({a[0]}, {a[1]}, {a[2]})",
        f"b = ({b[0]}, {b[1]}, {b[2]})",
        f"c = ({c[0]}, {c[1]}, {c[2]})"
    ],
    show_points = False,
    shape = None,
    font_size = 16
)

# Pyvista의 경우 각 표시가 원형으로만 가능하기에 인위적으로 설정
a_unit = a / np.linalg.norm(a)
b_unit = b / np.linalg.norm(b)
c_unit = c / np.linalg.norm(c)

Pa = 0.5 * a_unit
Pb = 0.5 * b_unit
Pc = 0.5 * c_unit
Pab = 0.5 * (a_unit + b_unit)
Pbc = 0.5 * (b_unit + c_unit)
Pac = 0.5 * (a_unit + c_unit)

arc_ab = pv.lines_from_points(np.array([Pa,Pab,Pb]))
fig.add_mesh(arc_ab, color="black", line_width=3) 

arc_bc = pv.lines_from_points(np.array([Pb,Pbc,Pc]))
fig.add_mesh(arc_bc, color="black", line_width=3) 

arc_ac = pv.lines_from_points(np.array([Pa,Pac,Pc]))
fig.add_mesh(arc_ac, color="black", line_width=3) 

p3d.add_coordinate_axes(fig)

fig.show()