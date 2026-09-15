import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])

a = 2.5
b = 0.8
c = np.sqrt(a**2 + b**2)

u = np.array([0, 0, 1])

cos_theta = b / c
sin_theta = a / c


def alpha(t):
    return np.array([a * np.cos(t), a * np.sin(t), b * t])


def T(t):
    return np.array([-a * np.sin(t), a * np.cos(t), b]) / c


def N(t):
    return np.array([-np.cos(t), -np.sin(t), 0])


def B(t):
    return np.cross(T(t), N(t))


def cylinder_patch(theta, z):
    return np.array([a * np.cos(theta), a * np.sin(theta), z])


t0 = 0.9

P = alpha(t0)
T_0 = T(t0)
N_0 = N(t0)
B_0 = B(t0)

u_T = cos_theta * T_0
u_B = sin_theta * B_0

theta_min = -0.1
theta_max = 2.0
z_min = -0.2
z_max = b * 2.0 + 0.4

ptd.add_parametric_surface_3d(fig, cylinder_patch, (theta_min, theta_max), (z_min, z_max), color="lightcyan", opacity=0.2)
ptd.add_parametric_curve_3d(fig, alpha, 0, 1.9)
ptd.add_plane_3d(fig, P, T_0, B_0, u_range=(-0.9, 0.9), v_range=(-0.9, 0.9), color="lightgray", opacity=0.18)

ptd.add_points_3d(fig, [P], point_size=12)
ptd.add_segment_3d(fig, P - u, P + 1.2 * u, color="gray")

ptd.add_vector_3d(fig, P, T_0)
ptd.add_vector_3d(fig, P, N_0)
ptd.add_vector_3d(fig, P, B_0)
ptd.add_vector_3d(fig, P, u, color="cyan")

ptd.add_vector_3d(fig, P, u_T, color="gray")
ptd.add_vector_3d(fig, P + u_T, u_B, color="gray")
ptd.add_segment_3d(fig, P + u_B, P + u, color="gray")
ptd.add_segment_3d(fig, P + u_T, P + u, color="gray")

ptd.add_angle_3d(fig, P, T_0, u, label=r"$\theta$")
ptd.add_angle_3d(fig, P, u, N_0, color="cyan")

ptd.add_labels_3d(
    fig,
    [
        alpha(1.75),
        P,
        P + T_0,
        P + N_0,
        P + B_0,
        P + u,
        P + u_T,
        P + u_T + u_B,
        P + np.array([0.45, -0.15, 0.85]),
    ],
    [
        r"$\alpha$",
        r"$\alpha(t_0)$",
        r"$T$",
        r"$N$",
        r"$B$",
        r"$u$",
        r"$\cos\theta\,T$",
        r"$\sin\theta\,B$",
        r"$u=\cos\theta\,T+\sin\theta\,B$",
    ],
)

fig.show()