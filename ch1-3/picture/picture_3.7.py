import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d(equal_scale=True)

O = np.array([0.0, 0.0])

c = np.array([2.0, 0.0])
M = np.array([
    [1.4, 0.55],
    [0.0, 1.05],
])


def beta(t):
    return c + M @ np.array([np.cos(t), np.sin(t)])


def beta_prime(t):
    return M @ np.array([-np.sin(t), np.cos(t)])


def unit_tangent(t):
    v = beta_prime(t)
    return v / np.linalg.norm(v)


def add_direction_arrow(t, length=0.20):
    p = beta(t)
    v = length * unit_tangent(t)
    ptd.add_vector_2d(fig, p, v, color="deepskyblue", width=2)


A = beta(0.0)
B = beta(np.pi)
P = beta(0.85)

ptd.add_coordinate_axes_2d(fig, (-0.4, 4.0), (-1.8, 1.8))
ptd.add_parametric_curve_2d(fig, beta, 0, 2 * np.pi)
ptd.add_points_2d(fig, [A, B, P], size=7)

add_direction_arrow(0.70)
add_direction_arrow(2.45)

ptd.add_labels_2d(
    fig,
    [
        O,
        A,
        B,
        P,
        P + np.array([0.10, 0.22]),
        beta(0.45),
    ],
    [
        r"$O$",
        r"$A$",
        r"$B$",
        r"$\beta(s)$",
        r"$(x(s),y(s))$",
        r"$\beta$",
    ],
    font_size=20,
)

ptd.add_labels_2d(
    fig,
    [
        A + np.array([0.00, 0.18]),
        B + np.array([0.10, 0.12]),
    ],
    [
        r"$s=0$",
        r"$s=a$",
    ],
    font_size=18,
)

fig.update_xaxes(visible=False, range=[-0.4, 4.0])
fig.update_yaxes(visible=False, range=[-1.8, 1.8])

fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
)

fig.show()

### 9/15 그림 자체는 교재 그림과 동일하게 가져왔지만 실제로 증명에 도움되는 그림은 아님