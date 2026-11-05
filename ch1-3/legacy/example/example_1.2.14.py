"""
예제 1.2.14

벡터 v = (2, 3, -2)의 표구 {e₁, e₂, e₃}에 대한 성분은 (2, 3, -2)이다.
그러나 세 벡터
    f₁ = (1, 0, 0), f₂ = (0, 1/√2, 1/√2), f₃ = (0, 1/√2, -1/√2)
로 이루어진 표구에 대한 벡터 v의 성분은
    (<v,f₁>, <v,f₂>, <v,f₃>) = (2, √2/2, 5√2/2)
이다. 따라서 벡터 v는
    v = 2e₁ + 3e₂ - 2e₃ 또는 v = 2f₁ + √2/2f₂ + 5√2/2f₃
이다.
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

v = np.array([2, 3, -2])

e1 = np.array([1, 0, 0])
e2 = np.array([0, 1, 0])
e3 = np.array([0, 0, 1])

f1 = np.array([1, 0, 0])
f2 = np.array([0, 1/np.sqrt(2), 1/np.sqrt(2)])
f3 = np.array([0, 1/np.sqrt(2), -1/np.sqrt(2)])

O = np.array([0, 0, 0])

c1 = np.dot(v,e1)
c2 = np.dot(v,e2)
c3 = np.dot(v,e3)

d1 = np.dot(v,f1)
d2 = np.dot(v,f2)
d3 = np.dot(v,f3)

O = (0, 0, 0)

fig = pv.Plotter(shape = (1,2))

# (1) {e1, e2, e3}
fig.subplot(0,0)

p3d.add_vector(fig, O, v, color = "black", name = "v")
p3d.add_vector(fig, O, e1, color = "red", name = "$e_1$")
p3d.add_vector(fig, O, e2, color = "green", name = "$e_2$")
p3d.add_vector(fig, O, e3, color = "blue", name = "$e_3$")

fig.add_mesh(pv.Line(O, c1*e1), color = "red")
fig.add_mesh(pv.Line(c1*e1, c1*e1 + c2*e2), color = "green")
fig.add_mesh(pv.Line(c1*e1 + c2*e2, v), color = "blue")

add_segment_label(
    fig, O, c1*e1,
    r"$2e_1$",
    color="red",
    offset=(0.1, 0.1, 0.1),
)

add_segment_label(
    fig, c1*e1, c1*e1 + c2*e2,
    r"$3e_2$",
    color="green",
    offset=(0.1, 0.1, 0.1),
)

add_segment_label(
    fig, c1*e1 + c2*e2, v,
    r"$-2e_3$",
    color="blue",
    offset=(0.1, 0.1, 0.1),
)

p3d.add_coordinate_axes(fig)

# (2) {f1, f2, f3}
fig.subplot(0,1)

p3d.add_vector(fig, O, v, color = "black", name = "v")
p3d.add_vector(fig, O, f1, color = "red", name = "$f_1$")
p3d.add_vector(fig, O, f2, color = "green", name = "$f_2$")
p3d.add_vector(fig, O, f3, color = "blue", name = "$f_3$")

fig.add_mesh(pv.Line(O, d1*f1), color = "red")
fig.add_mesh(pv.Line(d1*f1, d1*f1 + d2*f2), color = "green")
fig.add_mesh(pv.Line(d1*f1 + d2*f2, v), color = "blue")

add_segment_label(
    fig, O, d1*f1,
    r"$2f_1$",
    color="red",
    offset=(0.1, 0.1, 0.1),
)

add_segment_label(
    fig, d1*f1, d1*f1 + d2*f2,
     r"$\frac{\sqrt{2}}{2}f_2$",
    color="green",
    offset=(0.1, 0.1, 0.1),
)

add_segment_label(
    fig, d1*f1 + d2*f2, v,
    r"$\frac{5\sqrt{2}}{2}f_3$",
    color="blue",
    offset=(0.1, 0.1, 0.1),
)

p3d.add_coordinate_axes(fig)

fig.show()