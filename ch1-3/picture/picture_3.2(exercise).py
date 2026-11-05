import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d(equal_scale=True)


A = np.array([-1.0, 0.0])
B = np.array([1.0, 0.0])
C = np.array([0.0, np.sqrt(3)])

L = np.array([-0.5, np.sqrt(3) / 2])
R = np.array([0.5, np.sqrt(3) / 2])
D = np.array([0.0, 0.0])

r = 1.0


def circle(center, theta):
    return center + r * np.array([
        np.cos(theta),
        np.sin(theta),
    ])


def arc(center, theta_start, theta_end, resolution=300):
    theta = np.linspace(theta_start, theta_end, resolution)

    return center + r * np.column_stack([
        np.cos(theta),
        np.sin(theta),
    ])


def left_circle(theta):
    return circle(L, theta)


def right_circle(theta):
    return circle(R, theta)


def bottom_circle(theta):
    return circle(D, theta)


# --------------------------------------------------
# 색칠 영역의 경계
#
# A -> C : 왼쪽 위 원의 바깥쪽 원호
# C -> B : 오른쪽 위 원의 바깥쪽 원호
# B -> A : 아래 원의 위쪽 원호
# --------------------------------------------------

left_outer_arc = arc(
    L,
    4 * np.pi / 3,
    np.pi / 3,
)

right_outer_arc = arc(
    R,
    2 * np.pi / 3,
    -np.pi / 3,
)

bottom_upper_arc = arc(
    D,
    0,
    np.pi,
)

region = np.vstack([
    left_outer_arc,
    right_outer_arc[1:],
    bottom_upper_arc[1:],
])


# --------------------------------------------------
# 색칠된 영역
# --------------------------------------------------

ptd.add_filled_region_2d(
    fig,
    region,
    fill_color="lightcyan",
    line_color="deepskyblue",
    line_width=3,
    opacity=0.8,
)


# --------------------------------------------------
# 반지름 1인 세 원 전체
# --------------------------------------------------

ptd.add_parametric_curve_2d(
    fig,
    left_circle,
    0,
    2 * np.pi,
    color="gray",
    width=2,
    dash="dash",
)

ptd.add_parametric_curve_2d(
    fig,
    right_circle,
    0,
    2 * np.pi,
    color="gray",
    width=2,
    dash="dash",
)

ptd.add_parametric_curve_2d(
    fig,
    bottom_circle,
    0,
    2 * np.pi,
    color="gray",
    width=2,
    dash="dash",
)


# 색칠 영역의 경계를 다시 선명하게 표시
ptd.add_curve_2d(
    fig,
    region,
    color="black",
    width=4,
    closed=True,
)


# --------------------------------------------------
# 세 점을 잇는 정삼각형
# --------------------------------------------------

ptd.add_segment_2d(fig, A, C, color="gray", dash="dash")
ptd.add_segment_2d(fig, B, C, color="gray", dash="dash")


# --------------------------------------------------
# 교점
# --------------------------------------------------

ptd.add_points_2d(
    fig,
    [A, B, C],
    size=7,
)


ptd.add_labels_2d(
    fig,
    [
        A + np.array([-0.15, -0.12]),
        B + np.array([0.15, -0.12]),
        C + np.array([0.0, 0.12]),
    ],
    [
        r"$(-1,0)$",
        r"$(1,0)$",
        r"$(0,\sqrt{3})$",
    ],
    font_size=20,
)


fig.update_xaxes(
    visible=False,
    range=[-1.8, 1.8],
)

fig.update_yaxes(
    visible=False,
    range=[-1.2, 2.1],
)

fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
)

fig.show()