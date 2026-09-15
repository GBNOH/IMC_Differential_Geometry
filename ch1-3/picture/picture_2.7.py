import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])


def gamma(u):
    return np.array([u, 2 * np.sin(u), 0])


def gamma_prime(u):
    return np.array([1, 2 * np.cos(u), 0])


def gamma_second(u):
    return np.array([0, -2 * np.sin(u), 0])


u_grid = np.linspace(-2.2, 2.2, 4000)
speed_grid = np.array([np.linalg.norm(gamma_prime(u)) for u in u_grid])

s_grid = np.zeros_like(u_grid)
s_grid[1:] = np.cumsum(0.5 * (speed_grid[1:] + speed_grid[:-1]) * np.diff(u_grid))


def u_of_s(s):
    return np.interp(s, s_grid, u_grid)


def beta(s):
    return gamma(u_of_s(s))


def T(s):
    u = u_of_s(s)
    v = gamma_prime(u)
    return v / np.linalg.norm(v)


def curvature(u):
    v = gamma_prime(u)
    a = gamma_second(u)
    numerator = np.linalg.norm(np.cross(v, a))
    denominator = np.linalg.norm(v) ** 3
    return numerator / denominator


u0 = np.pi / 2
s0 = np.interp(u0, u_grid, s_grid)

P = beta(s0)
T_s = T(s0)

N_s = np.array([0, -1, 0])
minus_N_s = -N_s
T_prime_s = 2 * N_s

s_values = np.linspace(s_grid[0], s_grid[-1], 500)
curve_points = np.array([beta(s) for s in s_values])

ptd.add_curve_3d(fig, curve_points)
ptd.add_points_3d(fig, [P], point_size=12)

ptd.add_vector_3d(fig, P, T_s, shaft_radius=0.008, tip_radius=0.025)
ptd.add_vector_3d(fig, P, N_s, shaft_radius=0.008, tip_radius=0.025)
ptd.add_vector_3d(fig, P, minus_N_s, shaft_radius=0.008, tip_radius=0.025)
ptd.add_vector_3d(fig, P, T_prime_s, shaft_radius=0.008, tip_radius=0.025)

ptd.add_angle_3d(fig, P, T_s, N_s)

ptd.add_labels_3d(
    fig,
    [P, P + T_s, P + N_s, P + minus_N_s, P + T_prime_s],
    [r"$\beta(s)$", r"$T(s)$", r"$N(s)$", r"$-N(s)$", r"$T'(s)$"],
)

fig.show()