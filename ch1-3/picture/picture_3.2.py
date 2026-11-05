import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d(shape=(1, 2), equal_scale=True)


def beta_1(t):
    return np.array([1.8 * np.sin(t), 0.9 * np.sin(2 * t)])


A = np.array([
    [0.9, -0.15],
    [0.35, 0.55],
])


def beta_2(t):
    q = np.array([t**2 - 1, t * (t**2 - 1)])
    return A @ q


ptd.add_parametric_curve_2d(fig, beta_1, 0, 2 * np.pi, row=1, col=1)
ptd.add_points_2d(fig, [np.array([0, 0])], color="red", size=9, row=1, col=1)

ptd.add_parametric_curve_2d(fig, beta_2, -1.8, 2.2, row=1, col=2)
ptd.add_points_2d(fig, [np.array([0, 0])], color="red", size=9, row=1, col=2)

fig.update_xaxes(visible=False, range=[-2.2, 2.2], row=1, col=1)
fig.update_yaxes(visible=False, range=[-1.4, 1.4], row=1, col=1)

fig.update_xaxes(visible=False, range=[-1.2, 3.1], row=1, col=2)
fig.update_yaxes(visible=False, range=[-1.6, 2.2], row=1, col=2)

fig.update_layout(showlegend=False)

fig.show()

### 9/15 단순 곡선이 아님을 보이기 위해 교차점 표시