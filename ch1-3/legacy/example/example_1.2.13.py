"""
예제 1.2.13

E³상의 세 벡터 a = (1/√2 ,1/√2, 0), b = (1/√2, -1/√2, 0), c = (0, 0, -1)일 때,
<a,a> = <b,b> = <c,c> = 1이고
<a,b> = <b,c> = <a,c> = 0이다.
따라서 {a,b,c}는 E^3의 한 표구이다
""" 

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = (1/np.sqrt(2), 1/np.sqrt(2), 0)
b = (1/np.sqrt(2), -1/np.sqrt(2), 0)
c = (0, 0, -1)
O = (0, 0, 0)

fig = pv.Plotter()

p3d.add_vector(fig, O, a, color = "red", name = "a", text_color = "black")
p3d.add_vector(fig, O, b, color = "green", name = "b", text_color = "black")
p3d.add_vector(fig, O, c, color = "blue", name = "c", text_color = "black")

fig.add_point_labels(
    [a, b, c],
    [
        r"$(\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, 0)$",
        r"$(\frac{1}{\sqrt{2}}, -\frac{1}{\sqrt{2}}, 0)$",
        r"$(0, 0, -1)$",
    ],
    show_points = False, shape = None, 
    font_size = 16, font_family="arial", bold=False,
    always_visible = True
)

p3d.add_angle(fig, O, a, b)
p3d.add_angle(fig, O, b, c)
p3d.add_angle(fig, O, a, c)

p3d.add_coordinate_axes(fig, axis_length = 2)
fig.show()