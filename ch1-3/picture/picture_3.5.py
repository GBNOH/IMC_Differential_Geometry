import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d(
    shape=(2, 3),
    equal_scale=True,
    horizontal_spacing=0.06,
    vertical_spacing=0.12,
)


def rotate(points, angle):
    c = np.cos(angle)
    s = np.sin(angle)
    R = np.array([[c, -s], [s, c]])
    return points @ R.T


def wrap_angle(t):
    return (t + np.pi) % (2 * np.pi) - np.pi


def beta_1(t):
    return np.array([1.45 * np.sin(t), 0.70 * np.sin(2 * t)])


def beta_2(t):
    phi = wrap_angle(t - np.pi / 2)
    r = 1.05 - 0.12 * np.cos(t) + 0.95 * np.exp(-(phi / 0.24) ** 2)

    return np.array([
        1.05 * r * np.cos(t),
        0.88 * r * np.sin(t) - 0.12,
    ])


def beta_3(t):
    p = np.array([1.15 * np.cos(t), 1.55 * np.sin(t)])
    return rotate(p[None, :], np.pi / 6)[0]


def beta_4(t):
    return np.array([t, 0.10 * t**3 + 0.45 * t])


def beta_5(t):
    r = 1.08 + 0.98 * np.sin(t)

    return np.array([
        1.02 * r * np.cos(t),
        0.92 * r * np.sin(t) + 0.02,
    ])


def beta_6(t):
    return np.array([1.35 * np.cos(t), 1.35 * np.sin(t)])


def draw_label(row, col, text):
    ptd.add_labels_2d(
        fig,
        [np.array([0.0, -2.15])],
        [text],
        color="black",
        font_size=18,
        row=row,
        col=col,
    )


# (1)
ptd.add_parametric_curve_2d(fig, beta_1, 0, 2 * np.pi, row=1, col=1)
ptd.add_points_2d(fig, [np.array([0.0, 0.0])], color="red", size=8, row=1, col=1)
draw_label(1, 1, r"$(1)$")


# (2)
ptd.add_parametric_curve_2d(fig, beta_2, 0, 2 * np.pi, row=1, col=2)

P2 = beta_2(0.50 * np.pi)
Q2 = beta_2(0.15 * np.pi)

ptd.add_points_2d(fig, [P2, Q2], color="red", size=9, row=1, col=2)
ptd.add_segment_2d(fig, P2, Q2, color="red", width=5, row=1, col=2)

draw_label(1, 2, r"$(2)$")


# (3)
ptd.add_parametric_curve_2d(fig, beta_3, 0, 2 * np.pi, row=1, col=3)

P3 = beta_3(0.30 * np.pi)
Q3 = beta_3(1.15 * np.pi)

ptd.add_points_2d(fig, [P3, Q3], size=7, row=1, col=3)
ptd.add_segment_2d(fig, P3, Q3, width=3, row=1, col=3)
draw_label(1, 3, r"$(3)$")


# (4)
ptd.add_parametric_curve_2d(fig, beta_4, -1.9, 1.9, row=2, col=1)

A4 = beta_4(-1.9)
B4 = beta_4(1.9)

ptd.add_points_2d(fig, [A4, B4], color="red", size=8, row=2, col=1)
draw_label(2, 1, r"$(4)$")


# (5)
ptd.add_parametric_curve_2d(fig, beta_5, 0, 2 * np.pi, row=2, col=2)

P5 = beta_5(1.16 * np.pi)
Q5 = beta_5(1.84 * np.pi)

ptd.add_points_2d(fig, [P5, Q5], color="red", size=9, row=2, col=2)
ptd.add_segment_2d(fig, P5, Q5, color="red", width=5, row=2, col=2)

draw_label(2, 2, r"$(5)$")


# (6)
ptd.add_parametric_curve_2d(fig, beta_6, 0, 2 * np.pi, row=2, col=3)

P6 = beta_6(0.18 * np.pi)
Q6 = beta_6(1.05 * np.pi)

ptd.add_points_2d(fig, [P6, Q6], size=7, row=2, col=3)
ptd.add_segment_2d(fig, P6, Q6, width=3, row=2, col=3)
draw_label(2, 3, r"$(6)$")


for row in [1, 2]:
    for col in [1, 2, 3]:
        fig.update_xaxes(visible=False, range=[-2.4, 2.4], row=row, col=col)
        fig.update_yaxes(visible=False, range=[-2.3, 2.3], row=row, col=col)


fig.update_layout(
    width=950,
    height=650,
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
)

fig.show()