"""
연습문제 1.1 2번
유클리드평면 E^3에 속하는 두 벡터 a, b,c가 동일평면 위에 있지 않으면, E^3의 임의의 벡터는 a, b와 c로 나타낼 수 있음을 보여라.

동일평면 위에 있지 않는 경우, 동일직선 위에 있는 경우, 그 외의 경우로 가능한 경우의 대표적인 예시로서 시각화한다.
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d


# =========================================================
# 사용자 변경
# =========================================================

# 동일 평면에 있지 않은 경우의 벡터
a = np.array([2, 1, 1])
b = np.array([0, -1, 2])
c = np.array([-1, 0, 3])

x = np.array([1.5, 3, -1])

# 동일 직선 / 동일 평면의 경우에 사용할 스칼라
s = -2
t = 1.5


# =========================================================
# 기본 설정
# =========================================================

O = np.array([0, 0, 0])

fig = pv.Plotter(
    shape=(2, 2),

    # 왼쪽의 (0, 0), (1, 0)을 하나의 subplot으로 묶음
    groups=[
        (slice(None), 0)
    ],

    # 왼쪽 subplot을 오른쪽보다 크게
    col_weights=[1.7, 1.0],

    window_size=(1600, 900),
    border=True,
)

fig.set_background("white")


# =========================================================
# 1. 동일 평면에 있지 않은 경우
# =========================================================

fig.subplot(0, 0)

p3d.add_vector(fig, O, a, name="a", color="red")
p3d.add_vector(fig, O, b, name="b", color="blue")
p3d.add_vector(fig, O, c, name="c", color="green")


# ---------------------------------------------------------
# 격자
# ---------------------------------------------------------

grid_segments = []


# a 방향
for j in range(-2, 3):
    for k in range(-2, 3):

        start = -2*a + j*b + k*c
        end = 2*a + j*b + k*c

        grid_segments.extend([start, end])


# b 방향
for i in range(-2, 3):
    for k in range(-2, 3):

        start = i*a - 2*b + k*c
        end = i*a + 2*b + k*c

        grid_segments.extend([start, end])


# c 방향
for i in range(-2, 3):
    for j in range(-2, 3):

        start = i*a + j*b - 2*c
        end = i*a + j*b + 2*c

        grid_segments.extend([start, end])


grid_segments = np.array(grid_segments)

grid = pv.line_segments_from_points(grid_segments)

fig.add_mesh(
    grid,
    color="lightgray",
    line_width=1,
    opacity=0.5,
)


# ---------------------------------------------------------
# x = pa + qb + rc
# ---------------------------------------------------------

A = np.column_stack((a, b, c))

p, q, r = np.linalg.solve(A, x)

p3d.add_vector(
    fig,
    O,
    x,
    name="x",
    color="purple",
)


# x = pa + qb + rc의 구성 과정
P1 = p*a
P2 = p*a + q*b

path_points = [
    O, P1,
    P1, P2,
    P2, x,
]

path = pv.line_segments_from_points(
    np.array(path_points)
)

fig.add_mesh(
    path,
    color="gray",
    line_width=4,
    opacity=0.7,
)


p3d.add_coordinate_axes(
    fig,
    label_font_size=18,
)


# =========================================================
# 2. 동일 직선에 있는 경우
# =========================================================

fig.subplot(0, 1)

p3d.add_vector(fig, O, a, name="a", color="red")
p3d.add_vector(fig, O, s*a, name="sa", color="blue")
p3d.add_vector(fig, O, t*a, name="ta", color="green")


# a가 생성하는 직선
line_grid = pv.Line(
    -3*a,
    3*a,
)

fig.add_mesh(
    line_grid,
    color="lightgray",
    line_width=2,
)


# 정수배 위치
ticks = np.array([
    k*a
    for k in range(-3, 4)
])

fig.add_points(
    ticks,
    color="gray",
    point_size=7,
    render_points_as_spheres=True,
)


p3d.add_coordinate_axes(
    fig,
    label_font_size=14,
)


# =========================================================
# 3. 동일 평면에 있으나 동일 직선에는 있지 않은 경우
# =========================================================

fig.subplot(1, 1)

p3d.add_vector(fig, O, a, name="a", color="red")
p3d.add_vector(fig, O, b, name="b", color="blue")

p3d.add_vector(
    fig,
    O,
    s*a + t*b,
    name="sa+tb",
    color="green",
)


# ---------------------------------------------------------
# a, b가 생성하는 평면 격자
# ---------------------------------------------------------

plane_grid_segments = []


# a 방향
for j in range(-2, 3):

    start = -2*a + j*b
    end = 2*a + j*b

    plane_grid_segments.extend([
        start,
        end,
    ])


# b 방향
for i in range(-2, 3):

    start = i*a - 2*b
    end = i*a + 2*b

    plane_grid_segments.extend([
        start,
        end,
    ])


plane_grid_segments = np.array(
    plane_grid_segments
)

plane_grid = pv.line_segments_from_points(
    plane_grid_segments
)

fig.add_mesh(
    plane_grid,
    color="lightgray",
    line_width=1,
    opacity=0.5,
)


p3d.add_coordinate_axes(
    fig,
    label_font_size=14,
)


fig.show()