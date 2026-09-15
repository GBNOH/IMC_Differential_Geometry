"""
연습문제 1.5 1번

자연표구장 {U₁, U₂, U₃}에 대하여 다음과 같이 정의된 벡터장 V₁, V₂, V₃의 모양을 그려보아라.
(a) V₁ = xU₁ + yU₂
(b) V₂ = -xU₁ -yU₂
(c) V₃ = -xU₁ + yU₂ + zU₃
"""

"""
연습문제 1.5 1번

자연표구장 {U_1, U_2, U_3}에 대하여 다음과 같이 정의된
벡터장 V_1, V_2, V_3의 모양을 그려보아라.

(a) V_1 = xU_1 + yU_2

(b) V_2 = -xU_1 - yU_2

(c) V_3 = -xU_1 + yU_2 + zU_3
"""

import numpy as np
import pyvista as pv
import plot3d_tools_diffgeo as p3d


# =================================================
# 벡터장
# =================================================

def V1(point):

    x, y, z = point

    return np.array([
        x,
        y,
        0.0
    ])


def V2(point):

    x, y, z = point

    return np.array([
        -x,
        -y,
        0.0
    ])


def V3(point):

    x, y, z = point

    return np.array([
        -x,
        y,
        z
    ])


# =================================================
# 벡터장 표시
# =================================================

def add_vector_field(
    fig,
    points,
    field,
    *,
    scale=0.4,
    color="turquoise",
):

    for point in points:

        vector = field(point)

        # 원점 등에서 영벡터가 나오는 경우
        # p3d.add_vector는 영벡터를 그릴 수 없으므로 제외
        if np.isclose(np.linalg.norm(vector), 0):
            continue

        p3d.add_vector(
            fig,
            point,
            scale * vector,
            color=color,
        )


# =================================================
# 벡터를 그릴 점들
# =================================================

values = np.array([
    -1.0,
     0.0,
     1.0
])

points = np.array([
    [x, y, z]
    for x in values
    for y in values
    for z in values
])


# =================================================
# figure
# =================================================

fig = pv.Plotter(
    shape=(1, 3),
    window_size=(1800, 600),
)

fig.set_background("white")


# 공통 좌표축 길이
axis_length = 1.8


# 공통 카메라
camera_position = [
    (4.0, -5.0, 3.5),
    (0.0, 0.0, 0.0),
    (0.0, 0.0, 1.0),
]


# =================================================
# (a) V_1 = xU_1 + yU_2
# =================================================

fig.subplot(0, 0)


# 벡터가 부착되는 점들
fig.add_points(
    points,
    color="black",
    point_size=5,
    render_points_as_spheres=True,
)


# 벡터장
add_vector_field(
    fig,
    points,
    V1,
    scale=0.40,
    color="turquoise",
)


# 좌표축
p3d.add_coordinate_axes(
    fig,
    axis_length=axis_length,
    show_labels=False,
    opacity=0.4,
)


# 좌표축 라벨
fig.add_point_labels(
    [
        [axis_length + 0.12, 0.0, 0.0],
        [0.0, axis_length + 0.12, 0.0],
        [0.0, 0.0, axis_length + 0.12],
    ],
    [
        r"$x_1$",
        r"$x_2$",
        r"$x_3$",
    ],
    show_points=False,
    shape=None,
    text_color="black",
    font_size=15,
    always_visible=True,
)


fig.add_text(
    r"(a)  V_1 = xU_1 + yU_2",
    position="upper_left",
    font_size=12,
    color="black",
)

fig.camera_position = camera_position
fig.camera.zoom(1.1)


# =================================================
# (b) V_2 = -xU_1 - yU_2
# =================================================

fig.subplot(0, 1)


fig.add_points(
    points,
    color="black",
    point_size=5,
    render_points_as_spheres=True,
)


add_vector_field(
    fig,
    points,
    V2,
    scale=0.40,
    color="turquoise",
)


p3d.add_coordinate_axes(
    fig,
    axis_length=axis_length,
    show_labels=False,
    opacity=0.4,
)


fig.add_point_labels(
    [
        [axis_length + 0.12, 0.0, 0.0],
        [0.0, axis_length + 0.12, 0.0],
        [0.0, 0.0, axis_length + 0.12],
    ],
    [
        r"$x_1$",
        r"$x_2$",
        r"$x_3$",
    ],
    show_points=False,
    shape=None,
    text_color="black",
    font_size=15,
    always_visible=True,
)


fig.add_text(
    r"(b)  V_2 = -xU_1 - yU_2",
    position="upper_left",
    font_size=12,
    color="black",
)

fig.camera_position = camera_position
fig.camera.zoom(1.1)


# =================================================
# (c) V_3 = -xU_1 + yU_2 + zU_3
# =================================================

fig.subplot(0, 2)


fig.add_points(
    points,
    color="black",
    point_size=5,
    render_points_as_spheres=True,
)


add_vector_field(
    fig,
    points,
    V3,
    scale=0.35,
    color="turquoise",
)


p3d.add_coordinate_axes(
    fig,
    axis_length=axis_length,
    show_labels=False,
    opacity=0.4,
)


fig.add_point_labels(
    [
        [axis_length + 0.12, 0.0, 0.0],
        [0.0, axis_length + 0.12, 0.0],
        [0.0, 0.0, axis_length + 0.12],
    ],
    [
        r"$x_1$",
        r"$x_2$",
        r"$x_3$",
    ],
    show_points=False,
    shape=None,
    text_color="black",
    font_size=15,
    always_visible=True,
)


fig.add_text(
    r"(c)  V_3 = -xU_1 + yU_2 + zU_3",
    position="upper_left",
    font_size=12,
    color="black",
)

fig.camera_position = camera_position
fig.camera.zoom(1.1)


# =================================================
# 출력
# =================================================

fig.show()