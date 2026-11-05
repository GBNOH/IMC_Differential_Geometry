"""
그림 1.3

a × b ≠ 0이면 {a, b, a × b}는 우수계를 이룬다.
공간에서 a벡터와 b벡터가 이루는 평면에서 왼쪽의 그림을 구현하는 방식으로 작성되었다.
"""

import numpy as np
import pyvista as pv
import plot_tools_diffgeo as ptd


a = np.array([3, 0, 0])
b = np.array([1, 2, 0])
O = np.array([0, 0, 0])

axb = np.cross(a, b)

if np.allclose(axb, 0):
    raise ValueError("a × b ≠ 0이어야 합니다.")

P = np.dot(a, b) / np.dot(a, a) * a
h = b - P

A = a
B = b
C = a + b
Q = a + P

u = a / np.linalg.norm(a)
v = h / np.linalg.norm(h)

fig = ptd.create_figure_3d()

ptd.add_plane_3d(fig, O, a, b, u_range=(0, 1), v_range=(0, 1), color="cyan", opacity=0.35, show_edges=True)

ptd.add_vector_3d(fig, O, a, name=r"$a$")
ptd.add_vector_3d(fig, O, b, name=r"$b$")
ptd.add_vector_3d(fig, O, axb, name=r"$a\times b$")

ptd.add_angle_3d(fig, O, a, b, label=r"$\theta$", radius = 0.5)
ptd.add_angle_3d(fig, O, a, axb, radius = 0.5)
ptd.add_angle_3d(fig, O, b, axb, radius = 0.5)

fig.add_mesh(pv.Line(A, Q), color="gray", opacity=0.35, line_width=2)

ptd.add_segment_3d(fig, Q, C)
ptd.add_labels_3d(fig, [Q + (C - Q) / 2], [r"$\|b\|\sin\theta$"])

ptd.add_angle_3d(fig, Q, A - Q, C - Q)

fig.show()