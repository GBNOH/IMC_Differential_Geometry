import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d(equal_scale=True)

O = np.array([0.0, 0.0])


def beta(theta):
    r = 1 - 2 * np.sin(theta)
    return np.array([
        r * np.cos(theta),
        r * np.sin(theta),
    ])


theta_1 = np.pi / 2
theta_2 = 3 * np.pi / 2

V1 = beta(theta_1)
V2 = beta(theta_2)

ptd.add_coordinate_axes_2d(fig, (-2.4, 2.4), (-3.6, 1.6))
ptd.add_parametric_curve_2d(fig, beta, 0, 2 * np.pi)

ptd.add_points_2d(fig, [V1, V2], color="red", size=9)

ptd.add_labels_2d(
    fig,
    [
        O,
        V1,
        V2,
        np.array([1.2, 1.1]),
    ],
    [
        r"$O$",
        r"$\theta=\frac{\pi}{2}$",
        r"$\theta=\frac{3\pi}{2}$",
        r"$r=1-2\sin\theta$",
    ],
    font_size=20,
)

fig.update_xaxes(visible=False, range=[-2.4, 2.4])
fig.update_yaxes(visible=False, range=[-3.6, 1.6])

fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
)

fig.show()