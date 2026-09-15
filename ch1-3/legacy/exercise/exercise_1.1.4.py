"""
연습문제 1.1 4번 (일부)

일차독립, 일차종속에 대해 다음을 증명하라
(a) a = (1, -1, 0), b = (0, 2, -1), c = (2, 0, -1)은 일차종속이다.
(c) a = (1, 0, 0), b = (0, 1, 0), c= (0, 0, 1)은 일차독립이다.

(a), (c)에 대해서만 주어진 벡터가 생성하는 공간을 그리드 형태로 나타내어 보인다.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d

O = np.array([0, 0, 0])

fig = pv.Plotter(shape=(1, 2))

# (a)
fig.subplot(0, 0)

a = np.array([1, -1, 0])
b = np.array([0, 2, -1])
c = np.array([2, 0, -1])

p3d.add_vector(fig, O, a, name="a", color="red")
p3d.add_vector(fig, O, b, name="b", color="blue")
p3d.add_vector(fig, O, c, name="c", color="green")

### 그리드 생성 ###
plane_grid_segments = []

for j in range(-3, 4):
    start = -3 * a + j * b
    end   =  3 * a + j * b
    plane_grid_segments.extend([start, end])

for i in range(-3, 4):
    start = i * a - 3 * b
    end   = i * a + 3 * b
    plane_grid_segments.extend([start, end])

plane_grid_segments = np.array(plane_grid_segments)
plane_grid = pv.line_segments_from_points(plane_grid_segments)
fig.add_mesh(plane_grid, color="lightgray", line_width=1, opacity=0.6)
######

fig.add_mesh(pv.Line(O, 2*a), color="red", line_width=4, opacity=0.3)
fig.add_point_labels([(O + 2*a) / 2], ["2a"], show_points=False, shape=None, font_size=18)

fig.add_mesh( pv.Line(2*a, c), color="blue", line_width=4, opacity=0.3)
fig.add_point_labels([(2*a + c) / 2], ["b"], show_points=False, shape=None, font_size=18)
p3d.add_coordinate_axes(fig, label_font_size=16)

# (c)
fig.subplot(0, 1)

a = np.array([1, 0, 0])
b = np.array([0, 1, 0])
c = np.array([0, 0, 1])

p3d.add_vector(fig, O, a, name="a", color="red")
p3d.add_vector(fig, O, b, name="b", color="blue")
p3d.add_vector(fig, O, c, name="c", color="green")

# a, b, c가 생성하는 3차원 격자
grid_segments = []

# a 방향
for j in range(-2, 3):
    for k in range(-2, 3):
        start = -2 * a + j * b + k * c
        end   =  2 * a + j * b + k * c
        grid_segments.extend([start, end])

# b 방향
for i in range(-2, 3):
    for k in range(-2, 3):
        start = i * a - 2 * b + k * c
        end   = i * a + 2 * b + k * c
        grid_segments.extend([start, end])

# c 방향
for i in range(-2, 3):
    for j in range(-2, 3):
        start = i * a + j * b - 2 * c
        end   = i * a + j * b + 2 * c
        grid_segments.extend([start, end])

grid_segments = np.array(grid_segments)
grid = pv.line_segments_from_points(grid_segments)
fig.add_mesh(grid, color="lightgray", line_width=1, opacity=0.5)

p3d.add_coordinate_axes(fig, label_font_size=16)


fig.show()