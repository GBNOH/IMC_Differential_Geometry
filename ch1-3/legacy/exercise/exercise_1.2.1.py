"""
연습문제 1.2 1번

두 벡터 a = (1, 2, -1)과 b = (-1, 0, 3)에 대하여 다음을 구하여라.
(a) <a, b>
(b) a / ||a||, b / ||b||
(c) a와 b가 이루는 각의 크기의 코사인
""" 

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

def add_math_point_label(
    fig,
    point,
    text,
    *,
    offset=(0, 0, 0),
    color="black",
    font_size=16,
):
    point = np.asarray(point, dtype=float)
    offset = np.asarray(offset, dtype=float)

    fig.add_point_labels(
        [point + offset],
        [text],
        show_points=False,
        shape=None,
        text_color=color,
        font_size=font_size,
        always_visible=True,
        bold=False,
        font_family="times",
    )


a = np.array([1, 2, -1])
b = np.array([-1, 0, 3])
O = np.array([0, 0, 0])

a_norm = np.linalg.norm(a)
b_norm = np.linalg.norm(b)

a_unit = a / a_norm
b_unit = b / b_norm

inner_product = np.dot(a, b)
cos_theta = inner_product / (a_norm * b_norm)
theta_deg = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

fig = pv.Plotter(shape=(1, 2))

# 왼쪽: (a) 내적
fig.subplot(0, 0)

p3d.add_vector(fig, O, a, name=r"$a,\quad \|a\|=\sqrt{6}$", color="red")
p3d.add_vector(fig, O, b, name=r"$b,\quad \|b\|=\sqrt{10}$", color="blue")

projection = (np.dot(b, a) / np.dot(a, a)) * a

fig.add_mesh(pv.Line(O, projection), color="black", line_width=3)
fig.add_mesh( pv.Line(projection, b), color="gray", line_width=2)

points = np.array([O, projection, b])
triangle = pv.PolyData( points, faces=np.array([3, 0, 1, 2]))
fig.add_mesh(triangle, color="lightblue", opacity=0.18)

p3d.add_angle(fig, projection, O - projection, b - projection, radius=0.25,)
p3d.add_angle(fig, O, a, b, radius=0.7, angle_name=r"\theta")

fig.add_point_labels(
    [projection / 2],
    [r"$\|b\|\cos\theta=-\frac{4}{\sqrt{6}}$"],
    show_points=False,
    shape=None,
    font_size=16,
    font_family="times",
    bold=False,
    always_visible=True,
)

p3d.add_coordinate_axes(fig)

# 오른쪽: (b), (c) 단위벡터와 코사인
fig.subplot(0, 1)

sphere = pv.Sphere(radius=1.0, center=O, theta_resolution=60, phi_resolution=60,)
fig.add_mesh(sphere, color="gray", opacity=0.15, smooth_shading=True)

p3d.add_vector(fig, O, a, color = "red", opacity = 0.5, name = "a")
p3d.add_vector(fig, O, b, color = "blue", opacity = 0.5, name = "b")
p3d.add_vector(fig, O, a_unit, color="black")
p3d.add_vector(fig, O, b_unit, color="black")

fig.add_points(np.array([a_unit, b_unit]), color="black", point_size=10, render_points_as_spheres=True)

add_math_point_label(
    fig,
    a_unit,
    r"$\frac{a}{\|a\|}=\left(\frac{1}{\sqrt{6}},\frac{2}{\sqrt{6}},-\frac{1}{\sqrt{6}}\right)$",
    offset=(0.08, 0.10, 0.08),
    color="red",
    font_size=15,
)

add_math_point_label(
    fig,
    b_unit,
    r"$\frac{b}{\|b\|}=\left(-\frac{1}{\sqrt{10}},0,\frac{3}{\sqrt{10}}\right)$",
    offset=(0.08, 0.10, 0.08),
    color="blue",
    font_size=15,
)

p3d.add_angle(fig, O, a_unit, b_unit, radius=0.45, angle_name=r"\theta", show_angle_value=True)

p3d.add_coordinate_axes(fig, axis_length=1.7)

fig.show()