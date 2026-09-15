"""
그림 2.6

재매개화

h : J -> I
alpha : I -> R^2
beta = alpha o h : J -> R^2

재매개화를 시각적으로 나타내기 위해 점을 배치하여 나타냄
"""

import numpy as np
import plot_tools_diffgeo as ptd


def h(t):
    return np.exp(t)


def alpha(s):
    return np.array([np.cos(s), np.sin(s)])


def beta(t):
    return alpha(h(t))


offset = np.array([10.8, 1.4])


def alpha_display(s):
    return alpha(s) + offset


def beta_display(t):
    return beta(t) + offset


def J_embed(t):
    x = 0.8 + (t / np.log(4)) * 2.8
    return np.array([x, 0])


def I_embed(s):
    x = 4.8 + ((s - 1) / 3) * 2.8
    return np.array([x, 0])


fig = ptd.create_figure_2d(equal_scale=False)


# J, I
ptd.add_segment_2d(fig, [0.8, 0], [3.6, 0])
ptd.add_segment_2d(fig, [4.8, 0], [7.6, 0])

ptd.add_labels_2d(
    fig,
    [[0.8, 0], [3.6, 0], [4.8, 0], [7.6, 0], [2.2, 0.45], [6.2, 0.45]],
    [r"$($", r"$)$", r"$($", r"$)$", r"$J=(0,\ln 4)$", r"$I=(1,4)$"],
)


# alpha(I) = beta(J)
s_values = np.linspace(1, 4, 400)
curve_points = np.array([alpha_display(s) for s in s_values])

ptd.add_curve_2d(fig, curve_points)


# 대응점
t_values = np.linspace(0.08, np.log(4) - 0.08, 7)
s_values = np.array([h(t) for t in t_values])

J_points = np.array([J_embed(t) for t in t_values])
I_points = np.array([I_embed(s) for s in s_values])
curve_points = np.array([beta_display(t) for t in t_values])

colors = ["red", "orange", "gold", "green", "deepskyblue", "blue", "purple"]

for J_point, I_point, curve_point, color in zip(J_points, I_points, curve_points, colors):
    ptd.add_points_2d(fig, J_point, color=color, size=9)
    ptd.add_points_2d(fig, I_point, color=color, size=9)
    ptd.add_points_2d(fig, curve_point, color=color, size=9)


# 사상
ptd.add_vector_2d(fig, [3.9, 0.55], [0.7, 0], name=r"$h(t)=e^t$")
ptd.add_vector_2d(fig, [7.9, 0.75], [1.1, 0.55], name=r"$\alpha(s)=(\cos s,\sin s)$")
ptd.add_vector_2d(fig, [2.2, 1.2], [6.6, 0.9], name=r"$\beta(t)=(\cos(e^t),\sin(e^t))$")

ptd.add_labels_2d(fig, [[10.8, 2.9]], [r"$\beta=\alpha\circ h$"])

fig.update_xaxes(visible=False, range=[-0.2, 12.5])
fig.update_yaxes(visible=False, range=[-0.8, 3.4])
fig.update_layout(showlegend=False)

fig.show()