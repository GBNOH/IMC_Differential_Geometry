"""
예제 1.3.5

세 점 A(1,2,3), B(0,1,2), C(0,3,2)를 원점 O(0,0,0)와 이어서 얻은 세 선분 OA,OB,OC를 모서리로 하는 평행육면체의 부피를 구하여라
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

A = np.array([1, 2, 3])
B = np.array([0, 1, 2])
C = np.array([0, 3, 2])

O = np.array([0, 0, 0])

fig = pv.Plotter()

faces = [
    [O, A, A + B, B],
    [O, A, A + C, C],
    [O, B, B + C, C],
    [C, A + C, A + B + C, B + C],
    [B, A + B, A + B + C, B + C],
    [A, A + B, A + B + C, B + C]
]

for points in faces:

    points = np.array(points)

    face = pv.PolyData(points, [4, 0, 1, 2, 3])

    fig.add_mesh(face, color="turquoise", opacity=0.2)

edges = [
    (O, A), (O, B), (O, C),
    (A, A + B), (B, A + B),
    (A, A + C), (C, A + C),
    (B, B + C), (C, B + C),
    (A + B, A + B + C), (A + C, A + B + C), (B + C, A + B + C),
    ]

for start, end in edges:

    fig.add_mesh(pv.Line(start, end), color="gray", line_width=2)

volume = abs(np.dot(A, np.cross(B, C)))

fig.add_point_labels(
    [A + B + C],
    [f"V = {volume:g}"],
    show_points=False,
    shape=None,
    text_color="black",
    font_size=18,
    always_visible=True,
)

p3d.add_vector(fig, O, A, name = r"$\overrightarrow{OA}$")
p3d.add_vector(fig, O, B, name = r"$\overrightarrow{OB}$")
p3d.add_vector(fig, O, C, name = r"$\overrightarrow{OC}$")

p3d.add_vector(fig, O, np.cross(B,C),name = r"$\|\overrightarrow{OB} x \overrightarrow{OC}\| =$" , color = "red", show_magnitude = True)

projection = np.dot(np.cross(B,C),A)/np.dot(np.cross(B,C),np.cross(B,C)) * np.cross(B,C)
p3d.add_vector(fig, O, projection, color = "blue", name = r"$\|\overrightarrow{OA}\|\cos{\theta}$ =", show_magnitude = True) 

fig.add_mesh(pv.Line(projection, A), color = "blue", line_width=2)

p3d.add_coordinate_axes(fig)
fig.show()