import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d(equal_scale=True)

O = np.array([0, 0, 0])

a = 2.4
b = 1.5

u1 = 0.85
u2 = 2.35


def alpha(u):
    return np.array([a * np.cos(u), b * np.sin(u)])


def alpha_prime(u):
    return np.array([-a * np.sin(u), b * np.cos(u)])


def unit_tangent(u):
    v = alpha_prime(u)
    return v / np.linalg.norm(v)


def unit_normal(u):
    t = unit_tangent(u)
    return np.array([-t[1], t[0]])


p1 = alpha(u1)
p2 = alpha(u2)

t1 = unit_tangent(u1)
t2 = unit_tangent(u2)

n1 = unit_normal(u1)
n2 = unit_normal(u2)

Lt = 1.8
Ln = 1.4


ptd.add_parametric_curve_2d(fig, alpha, 0, 2 * np.pi)

ptd.add_segment_2d(fig, p1 - Lt * t1, p1 + Lt * t1, color="gray", dash="dash")
ptd.add_segment_2d(fig, p1 - Ln * n1, p1 + Ln * n1, color="gray", dash="dash")

ptd.add_segment_2d(fig, p2 - Lt * t2, p2 + Lt * t2, color="gray", dash="dash")
ptd.add_segment_2d(fig, p2 - Ln * n2, p2 + Ln * n2, color="gray", dash="dash")

ptd.add_points_2d(fig, [p1, p2], size=8)

ptd.add_vector_2d(fig, p1, t1)
ptd.add_vector_2d(fig, p1, n1)

ptd.add_vector_2d(fig, p2, t2)
ptd.add_vector_2d(fig, p2, n2)

ptd.add_labels_2d(
    fig,
    [alpha(0.2), p1, p1 + t1, p1 + n1, p2, p2 + t2, p2 + n2],
    [r"$\alpha$", r"$p_1$", r"$t$", r"$n$", r"$p_2$", r"$t$", r"$n$"],
    font_size=26,
)

fig.update_xaxes(visible=False, range=[-3.1, 3.1])
fig.update_yaxes(visible=False, range=[-2.3, 2.3])

fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
)

fig.show()

### 9/15 기존 그림이 난형선 상의 점임을 잘 표현하지 못한다고 생각하여 타원을 통해 변경하였습니다