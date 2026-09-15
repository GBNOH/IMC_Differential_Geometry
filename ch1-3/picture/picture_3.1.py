import numpy as np
import plot_tools_diffgeo as ptd


R = 1.4
s0 = 0.7


def beta_positive(s):
    return np.array([R * np.sin(s / R), R * (1 - np.cos(s / R))])


def T_positive(s):
    return np.array([np.cos(s / R), np.sin(s / R)])


def N_positive(s):
    return np.array([-np.sin(s / R), np.cos(s / R)])


def T_prime_positive(s):
    return (1 / R) * N_positive(s)


def beta_negative(s):
    return np.array([R * np.sin(s / R), -R * (1 - np.cos(s / R))])


def T_negative(s):
    return np.array([np.cos(s / R), -np.sin(s / R)])


def N_negative(s):
    return np.array([np.sin(s / R), np.cos(s / R)])


def T_prime_negative(s):
    return -(1 / R) * N_negative(s)


fig = ptd.create_figure_2d(
    shape=(1, 2),
    subplot_titles=[r"$\kappa>0$", r"$\kappa<0$"],
    equal_scale=True,
)


P = beta_positive(s0)
T = T_positive(s0)
N = N_positive(s0)
T_prime = T_prime_positive(s0)

ptd.add_parametric_curve_2d(fig, beta_positive, -1.5, 1.8, row=1, col=1)
ptd.add_points_2d(fig, [P], row=1, col=1)
ptd.add_vector_2d(fig, P, T, row=1, col=1)
ptd.add_vector_2d(fig, P, N, row=1, col=1)
ptd.add_vector_2d(fig, P, T_prime, row=1, col=1)
ptd.add_labels_2d(
    fig,
    [P, P + T, P + N, P + T_prime, beta_positive(1.7)],
    [r"$\beta(s)$", r"$t$", r"$n$", r"$t'$", r"$\beta$"],
    font_size=24,
    row=1,
    col=1,
)


P = beta_negative(s0)
T = T_negative(s0)
N = N_negative(s0)
T_prime = T_prime_negative(s0)

ptd.add_parametric_curve_2d(fig, beta_negative, -1.5, 1.8, row=1, col=2)
ptd.add_points_2d(fig, [P], row=1, col=2)
ptd.add_vector_2d(fig, P, T, row=1, col=2)
ptd.add_vector_2d(fig, P, N, row=1, col=2)
ptd.add_vector_2d(fig, P, T_prime, row=1, col=2)
ptd.add_labels_2d(
    fig,
    [P, P + T, P + N, P + T_prime, beta_negative(1.7)],
    [r"$\beta(s)$", r"$t$", r"$n$", r"$t'$", r"$\beta$"],
    font_size=24,
    row=1,
    col=2,
)


fig.update_xaxes(visible=False, range=[-1.6, 2.3], row=1, col=1)
fig.update_yaxes(visible=False, range=[-0.3, 2.1], row=1, col=1)

fig.update_xaxes(visible=False, range=[-1.6, 2.3], row=1, col=2)
fig.update_yaxes(visible=False, range=[-2.1, 0.3], row=1, col=2)

fig.update_annotations(font_size=24)
fig.update_layout(showlegend=False)

fig.show()