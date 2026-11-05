import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])

R = 9 / 2


def theta(t):
    return (2 / 3) * t + (2 / 9) * t**2


def theta_prime(t):
    return 2 / 3 + (4 / 9) * t


def theta_second(t):
    return 4 / 9


def alpha(t):
    return R * np.array([
        np.cos(theta(t)),
        np.sin(theta(t)),
        0,
    ])


def speed(t):
    return R * theta_prime(t)


def T(t):
    return np.array([
        -np.sin(theta(t)),
        np.cos(theta(t)),
        0,
    ])


def N(t):
    return np.array([
        -np.cos(theta(t)),
        -np.sin(theta(t)),
        0,
    ])


def B(t):
    return np.cross(T(t), N(t))


def kappa(t):
    return 1 / R


def dv_dt(t):
    return R * theta_second(t)


t = 0

P = alpha(t)

v = speed(t)
T_t = T(t)
N_t = N(t)
B_t = B(t)

alpha_t = v * T_t
tangent_part = dv_dt(t) * T_t
normal_part = kappa(t) * v**2 * N_t

alpha_tt = tangent_part + normal_part

t_values = np.linspace(-1.2, 1.4, 500)
curve_points = np.array([alpha(value) for value in t_values])

ptd.add_curve_3d(fig, curve_points)
ptd.add_points_3d(fig, [P])

# T 방향
ptd.add_vector_3d(fig, P, T_t, color="red")
ptd.add_vector_3d(fig, P, tangent_part)
ptd.add_vector_3d(fig, P, alpha_t)

# N 방향
ptd.add_vector_3d(fig, P, N_t, color="red")
ptd.add_vector_3d(fig, P, normal_part)

# B
ptd.add_vector_3d(fig, P, B_t, color="red")

# alpha'' = (dv/dt)T + kappa v^2 N
ptd.add_vector_3d(fig, P, alpha_tt, color="gray")

ptd.add_segment_3d(fig, P + tangent_part, P + alpha_tt, color="gray")
ptd.add_segment_3d(fig, P + normal_part, P + alpha_tt, color="gray")

ptd.add_labels_3d(
    fig,
    [
        P,
        P + T_t,
        P + tangent_part,
        P + alpha_t,
        P + N_t,
        P + normal_part,
        P + B_t,
        P + alpha_tt,
    ],
    [
        r"$\alpha(t)$",
        r"$T$",
        r"$\frac{dv}{dt}T$",
        r"$\alpha'=vT$",
        r"$N$",
        r"$\kappa v^2N$",
        r"$B$",
        r"$\alpha''$",
    ],
)

fig.show()