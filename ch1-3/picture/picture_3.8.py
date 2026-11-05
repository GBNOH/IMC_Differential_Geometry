import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d(
    shape=(2, 2),
    equal_scale=True,
    horizontal_spacing=0.08,
    vertical_spacing=0.12,
)


def tangent_vector(curve, t, h=1e-4):
    return (curve(t + h) - curve(t - h)) / (2 * h)


def add_tangent_line(fig, curve, t0, length=1.8, *, row=1, col=1):
    p = curve(t0)
    v = tangent_vector(curve, t0)
    v = v / np.linalg.norm(v)

    a = p - length * v
    b = p + length * v

    ptd.add_segment_2d(fig, a, b, color="gray", row=row, col=col)
    ptd.add_points_2d(fig, [p], size=6, row=row, col=col)


def draw_panel_label(row, col, text):
    ptd.add_labels_2d(
        fig,
        [np.array([0.0, -2.05])],
        [text],
        font_size=18,
        row=row,
        col=col,
    )


# -------------------------
# (1) 볼록곡선: 기울어진 타원
# -------------------------
c1 = np.array([0.0, 0.0])
M1 = np.array([
    [1.15, 0.45],
    [0.00, 1.55],
])


def beta_1(t):
    return c1 + M1 @ np.array([np.cos(t), np.sin(t)])


ptd.add_parametric_curve_2d(fig, beta_1, 0, 2 * np.pi, row=1, col=1)
add_tangent_line(fig, beta_1, 2.35, row=1, col=1)
add_tangent_line(fig, beta_1, 4.65, row=1, col=1)
add_tangent_line(fig, beta_1, 0.35, row=1, col=1)
draw_panel_label(1, 1, r"$(1)$")


# -------------------------
# (2) 볼록곡선: 볼록 그래프
# -------------------------
def beta_2(t):
    x = t
    y = 0.18 * (t + 1.2) ** 2 + 0.035 * (t + 1.2) ** 4 - 0.35
    return np.array([x, y])


ptd.add_parametric_curve_2d(fig, beta_2, -2.0, 1.8, row=1, col=2)
add_tangent_line(fig, beta_2, -1.2, length=1.2, row=1, col=2)
add_tangent_line(fig, beta_2, -0.2, length=1.2, row=1, col=2)
add_tangent_line(fig, beta_2, 0.9, length=1.2, row=1, col=2)
draw_panel_label(1, 2, r"$(2)$")


# -------------------------
# (3) 볼록곡선이 아님:
# 다른 단축 쪽이 오목하게 들어간 기울어진 타원
# -------------------------

def wrap_angle(t):
    return (t + np.pi) % (2 * np.pi) - np.pi


def beta_3(t):
    a = 1.55
    b = 1.05

    phi = wrap_angle(t - 3 * np.pi / 2)
    dent = 0.75 * np.exp(-(phi / 0.38) ** 2)

    p = np.array([
        a * np.cos(t),
        b * np.sin(t) + dent,
    ])

    angle = np.pi / 6

    R = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)],
    ])

    return R @ p


ptd.add_parametric_curve_2d(
    fig,
    beta_3,
    0,
    2 * np.pi,
    row=2,
    col=1,
)

t0 = 3 * np.pi / 2

add_tangent_line(
    fig,
    beta_3,
    t0,
    length=2.0,
    row=2,
    col=1,
)

draw_panel_label(2, 1, r"$(3)$")


# -------------------------
# (4) 볼록곡선이 아님: 변곡점이 있는 곡선
# -------------------------
def beta_4(t):
    return np.array([t, 0.22 * t**3])


ptd.add_parametric_curve_2d(fig, beta_4, -1.8, 1.8, row=2, col=2)
add_tangent_line(fig, beta_4, 0.0, length=1.8, row=2, col=2)
draw_panel_label(2, 2, r"$(4)$")


for row in [1, 2]:
    for col in [1, 2]:
        fig.update_xaxes(visible=False, range=[-2.4, 2.4], row=row, col=col)
        fig.update_yaxes(visible=False, range=[-2.2, 2.2], row=row, col=col)


fig.update_layout(
    width=900,
    height=700,
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
)

fig.show()