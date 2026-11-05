"""
예제 1.1.1
a = (3, -1, -4), b = (-2, 4, -3), c = (1, 2, -1)에 대해 다음을 구하여라

(1) 2a-b+3c
(2) ||a+b+c||

직접 표현하여 나타낸다
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

a = np.array([3,-1,-4])
b = np.array([-2, 4, -3])
c = np.array([1, 2, -1])
o = np.array([0,0,0])

fig = pv.Plotter(shape = (1,2))

# (1)
fig.subplot(0,0)

p3d.add_vector(fig, o, a, name = "a", color = "red")
p3d.add_vector(fig, o, b, name = "b", color = "green")
p3d.add_vector(fig, o, c, name = "c", color = "blue")

p3d.add_vector(fig, o, 2*a-b+3*c, name = "2a-b+3c", color = "black")

p3d.add_vector(fig, o, 2*a, name = "2a", color = "gray")
p3d.add_vector(fig, 2*a, -b, name = "-b", color = "gray")
p3d.add_vector(fig, 2*a-b, 3*c, name = "3c", color = "gray")

p3d.add_coordinate_axes(fig, axis_length = 6)

# (2)
fig.subplot(0,1)

p3d.add_vector(fig, o, a, name = "a", color = "red")
p3d.add_vector(fig, o, b, name = "b", color = "green")
p3d.add_vector(fig, o, c, name = "c", color = "blue")

p3d.add_vector(fig, o, a+b+c, name = "a+b+c", color = "black", show_magnitude=True)

p3d.add_coordinate_axes(fig, axis_length = 6)

fig.show()