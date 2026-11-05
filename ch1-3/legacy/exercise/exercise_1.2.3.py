"""
연습문제 1.2 3번

세 벡터 a₁ = 1/√6(1, 2, 1), a₂ = 1/√8(-2, 0, 2), a₃ = 1/√3(1, -1, 1)은 
3차원 유클리드 공간 E³의 한 표구임을 보이고, a = (6, 1, -1)을 이들의 일차결합으로 나타내어라.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

def add_segment_label(
    fig,
    start,
    end,
    text,
    *,
    color="black",
    font_size=16,
    offset=(0, 0, 0),
):
    start = np.asarray(start, dtype=float)
    end = np.asarray(end, dtype=float)
    offset = np.asarray(offset, dtype=float)

    midpoint = (start + end) / 2 + offset

    fig.add_point_labels(
        [midpoint],
        [text],
        show_points=False,
        shape=None,
        text_color=color,
        font_size=font_size,
        always_visible=True,
        bold=False,
        font_family="times",
    )

a = np.array([6, 1, -1])

a1 = np.array([1, 2, 1]) * np.sqrt(1/6)
a2 = np.array([-2, 0, 2]) * np.sqrt(1/8)
a3 = np.array([1, -1, 1]) * np.sqrt(1/3)

O = np.array([0, 0, 0])

c1 = np.dot(a,a1)
c2 = np.dot(a,a2)
c3 = np.dot(a,a3)

fig = pv.Plotter()

p3d.add_vector(fig, O, a, color = "black", name = "a")
p3d.add_vector(fig, O, a1, color = "red")
p3d.add_vector(fig, O, a2, color = "green")
p3d.add_vector(fig, O, a3, color = "blue")

p3d.add_angle(fig, O, a1, a2)
p3d.add_angle(fig, O, a2, a3)
p3d.add_angle(fig, O, a1, a3)

fig.add_mesh(pv.Line(O, c1*a1), color = "red")
fig.add_mesh(pv.Line(c1*a1, c1*a1 + c2*a2), color = "green")
fig.add_mesh(pv.Line(c1*a1 + c2*a2, a), color = "blue")

add_segment_label(
    fig, O, c1*a1,
    r"$\frac{7\sqrt{6}}{6}a_1$",
    color="red",
    offset=(0.1, 0.1, 0.1),
)

add_segment_label(
    fig, c1*a1, c1*a1 + c2*a2,
    r"$-\frac{7\sqrt{2}}{2}a_2$",
    color="green",
    offset=(0.1, 0.1, 0.1),
)

add_segment_label(
    fig, c1*a1 + c2*a2, a,
    r"$\frac{4\sqrt{3}}{3}a_3$",
    color="blue",
    offset=(0.1, 0.1, 0.1),
)

sphere = pv.Sphere(radius=1.0, center=O)

fig.add_mesh(
    sphere,
    color="gray",
    opacity=0.15,
    smooth_shading=True,
)

unit_points = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])

fig.add_point_labels(
    1.08 * unit_points,
    ["1", "1", "1"],
    show_points=False,
    shape=None,
    font_size=16,
    bold=False,
    always_visible=True,
)

p3d.add_coordinate_axes(fig)

fig.show()