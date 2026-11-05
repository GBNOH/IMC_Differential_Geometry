import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d(
    shape=(3, 3),
    equal_scale=True,
    horizontal_spacing=0.04,
    vertical_spacing=0.07,
)


def point(z):
    return np.array([z.real, z.imag])


def add_direction_triangle(fig, curve, t, *, size=0.13, row=1, col=1):
    h = 1e-4

    P = curve(t)
    v = curve(t + h) - curve(t - h)
    v = v / np.linalg.norm(v)

    n = np.array([-v[1], v[0]])

    tip = P + size * v
    base = P - 0.65 * size * v
    left = base + 0.55 * size * n
    right = base - 0.55 * size * n

    triangle = np.array([tip, left, right])

    ptd.add_filled_region_2d(
        fig,
        triangle,
        fill_color="black",
        line_color="black",
        line_width=1,
        opacity=1.0,
        row=row,
        col=col,
    )


def draw_curve(fig, curve, t_values, label, *, row, col):
    ptd.add_parametric_curve_2d(fig, curve, 0, 2 * np.pi, row=row, col=col)

    for t in t_values:
        add_direction_triangle(fig, curve, t, row=row, col=col)

    ptd.add_labels_2d(
        fig,
        [np.array([0.0, -2.05])],
        [label],
        color="deepskyblue",
        font_size=20,
        row=row,
        col=col,
    )


def curve_m1(t):
    z = 1.45 * np.exp(1j * t)
    return point(z)


def curve_m_minus1(t):
    z = 1.45 * np.exp(-1j * t)
    return point(z)


def curve_m0(t):
    z = 1.45 * np.sin(t) + 1.00j * np.sin(2 * t)
    return point(z)


def curve_m2(t):
    z = 0.72 * np.exp(1j * t) + 0.68 * np.exp(2j * t)
    return point(z)


def curve_m3(t):
    r = 1.15 + 0.65 * np.cos(t)

    return np.array([
        r * np.cos(3 * t),
        r * np.sin(3 * t),
    ])


draw_curve(fig, curve_m1, [0.6, 3.4], r"$m=1$", row=1, col=1)
draw_curve(fig, curve_m_minus1, [0.8, 3.6], r"$m=-1$", row=1, col=3)
draw_curve(fig, curve_m0, [0.45, 2.15, 4.65], r"$m=0$", row=2, col=2)
draw_curve(fig, curve_m2, [0.5, 2.0, 3.7, 5.2], r"$m=2$", row=3, col=1)
draw_curve(fig, curve_m3, [0.25, 1.25, 2.25, 3.25, 4.25, 5.25], r"$m=3$", row=3, col=3)


for row in range(1, 4):
    for col in range(1, 4):
        fig.update_xaxes(visible=False, range=[-2.35, 2.35], row=row, col=col)
        fig.update_yaxes(visible=False, range=[-2.35, 2.35], row=row, col=col)


fig.update_layout(
    width=900,
    height=900,
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
)

fig.show()

### 9/15 해당 그림이 유의미한지 검토 필요합니다