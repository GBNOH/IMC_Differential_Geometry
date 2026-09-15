"""
연습문제 1.2 4번

표구 {f₁ = (1, 0, 0), f₂ = (0, 1/√2, 1/√2), f₃ = (0, 1/√2, -1/√2)}에 대한 벡터 v = (-2, 1, -1)의 성분을 구하여라.
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

v = np.array([-2, 1, -1])

f1 = np.array([1, 0, 0])
f2 = np.array([0, 1/np.sqrt(2), 1/np.sqrt(2)])
f3 = np.array([0, 1/np.sqrt(2), -1/np.sqrt(2)])

O = np.array([0, 0, 0])

c1 = np.dot(v,f1)
c2 = np.dot(v,f2)
c3 = np.dot(v,f3)

fig = pv.Plotter()

p3d.add_vector(fig, O, v, color = "black", name = "v")
p3d.add_vector(fig, O, f1, color = "red")
p3d.add_vector(fig, O, f2, color = "green")
p3d.add_vector(fig, O, f3, color = "blue")

fig.add_mesh(pv.Line(O, c3*f3), color = "blue")
fig.add_mesh(pv.Line(c3*f3, v), color = "red")

add_segment_label(
    fig, c3*f3, c1*f1+c3*f3,
    "$-2f_1$",
    color="red",
    offset=(0.1, 0.1, 0.1),
)

add_segment_label(
    fig, O, c3*f3,
    r"$\sqrt{2}f_3$",
    color="blue",
    offset=(0.1, 0.1, 0.1),
)

p3d.add_coordinate_axes(fig)

fig.show()