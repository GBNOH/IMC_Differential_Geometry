"""
연습문제 1.4 1번

세 벡터 a = (2, 1, -3), b = (1, 0, 1), c = (0, 1, -3)에 대하여, 다음 방정식을 구하여라

(a) 점 a를 지나면서 b에 평행한 직선
(b) 점 b와 c를 지나는 직선
(c) 점 b를 지나고 a에 직교하는 평면
(d) 점 c를 지나며 a와 b에 평행한 평면
(e) 점 a를 중심으로 하고 반지름의 길이가 2인 원
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([2, 1, -3])
b = np.array([1, 0, 1])
c = np.array([0, 1, -3])

O = np.array([0, 0, 0])

direction_ab_line = b
direction_bc_line = c - b

normal_plane_c = a
normal_plane_d = np.cross(a, b)

fig = pv.Plotter(shape=(1, 3), window_size=(1800, 600))

# (a), (b)
fig.subplot(0, 0)

fig.add_mesh(pv.Line(a - 3 * b, a + 3 * b),color="red", line_width=3)
fig.add_mesh(pv.Line(b - 1.5 * (c - b), b + 1.5 * (c - b)), color="blue", line_width=3)

p3d.add_vector(fig, a, b, name="b", color="red")
p3d.add_vector(fig, b, c - b, name="c - b", color="blue")

fig.add_point_labels(
    [a, b, c],
    ["a", "b", "c"],
    shape=None,
    text_color="black",
    font_size=16,
    always_visible=True,
)

fig.add_text(
    "(a) x = a + tb\n(b) x = b + t(c - b)",
    position="upper_left",
    font_size=11,
    color="black",
)

p3d.add_coordinate_axes(fig, axis_length=6, opacity=0.45)

fig.view_isometric()


# (c), (d)
fig.subplot(0, 1)

plane_c = pv.Plane(center=b, direction=a, i_size=8, j_size=8, i_resolution=8, j_resolution=8)
fig.add_mesh(plane_c, color="turquoise", opacity=0.30, show_edges=True, edge_color="gray", line_width=1)

plane_d = pv.Plane(center=c, direction=np.cross(a, b), i_size=8, j_size=8, i_resolution=8, j_resolution=8)
fig.add_mesh(plane_d, color="lightgreen", opacity=0.30, show_edges=True, edge_color="gray", line_width=1)

fig.add_point_labels(
    [b, c],
    ["b", "c"],
    shape=None,
    text_color="black",
    font_size=16,
    always_visible=True,
)

p3d.add_vector(fig, b, a, name="a", color="red")
p3d.add_vector(fig, c, a, name="a", color="purple")
p3d.add_vector(fig, c, b, name="b", color="blue")

fig.add_text(
    "(c) 2x + y - 3z + 1 = 0\n(d) x - 5y - z + 2 = 0",
    position="upper_left",
    font_size=11,
    color="black",
)

p3d.add_coordinate_axes(fig, axis_length=6, opacity=0.45)

fig.view_isometric()


# (e)
fig.subplot(0, 2)

t = np.linspace(0, 2 * np.pi, 300)
circle_points = np.column_stack([
    a[0] + 2.0 * np.cos(t),
    a[1] + 2.0 * np.sin(t),
    np.full_like(t, -3.0),
])

circle = pv.lines_from_points(circle_points, close=True)

fig.add_mesh(circle, color="darkmagenta", line_width=3)

fig.add_points(np.array([a]), color="black", point_size=12, render_points_as_spheres=True)
fig.add_point_labels(
    [a + np.array([0.15, 0.10, 0.10])],
    ["a"],
    show_points=False,
    shape=None,
    text_color="black",
    font_size=16,
    always_visible=True,
)

# 반지름 하나 표시
radius_end = a + np.array([2.0, 0.0, 0.0])

fig.add_mesh(
    pv.Line(a, radius_end),
    color="black",
    line_width=2,
)

fig.add_point_labels(
    [a + np.array([1.0, 0.25, 0.0])],
    ["r = 2"],
    show_points=False,
    shape=None,
    text_color="black",
    font_size=15,
    always_visible=True,
)

fig.add_text(
    "(e) x(t) = (2 + 2cos t, 1 + 2sin t, -3)",
    position="upper_left",
    font_size=11,
    color="black",
)

p3d.add_coordinate_axes(fig, axis_length=6, opacity=0.45)

fig.view_isometric()

fig.show()