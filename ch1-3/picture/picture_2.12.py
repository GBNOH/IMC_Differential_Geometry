import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_2d()

O = np.array([0, 0, 0])

a = 1.5


def alpha(t):
    return np.array([a * np.cosh(t / a), t])


def N(t):
    return np.array([1 / np.cosh(t / a), -np.tanh(t / a)])


def kappa(t):
    return 1 / (a * np.cosh(t / a) ** 2)


t0 = -1.4
s0 = a * np.sinh(t0 / a)

P = alpha(t0)
rho = 1 / kappa(t0)
C = P + rho * N(t0)


def circle(theta):
    return C + rho * np.array([np.cos(theta), np.sin(theta)])


ptd.add_coordinate_axes_2d(fig, (-0.5, 6.5), (-3.0, 3.0))
ptd.add_parametric_curve_2d(fig, alpha, -2.2, 2.2)
ptd.add_parametric_curve_2d(fig, circle, 0, 2 * np.pi, color="gray", dash="dash")
ptd.add_segment_2d(fig, P, C)
ptd.add_points_2d(fig, [P, C])

ptd.add_labels_2d(
    fig,
    [O[:2], P, C, (P + C) / 2, [3.7, 2.3]],
    [
        r"$O$",
        r"$\alpha(t_0)$",
        r"$C$",
        r"$\frac{1}{\kappa(s_0)}=\frac{s_0^2+a^2}{a}$",
        r"$\alpha(t)=\left(a\cosh\left(\frac{t}{a}\right),\,t,\,0\right)$",
    ],
)

fig.show()

### 9/15 곡률을 표현하기 위해 내접원 사용