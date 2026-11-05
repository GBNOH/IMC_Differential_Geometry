import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])

a = 6.0
b = 2.0
c = np.sqrt(a**2 + b**2)

u = np.array([0, 0, 1])


def alpha(t):
    return np.array([a * np.cos(t), a * np.sin(t), b * t])


def T(t):
    return np.array([-a * np.sin(t), a * np.cos(t), b]) / c


def cylinder_patch(theta, z):
    return np.array([a * np.cos(theta), a * np.sin(theta), z])


t_values = np.array([0.2, 0.9, 1.6, 2.3])

theta_min = -0.3
theta_max = 2.8
z_min = -0.5
z_max = b * 2.8 + 0.8


ptd.add_parametric_surface_3d(
    fig,
    cylinder_patch,
    (theta_min, theta_max),
    (z_min, z_max),
    color="lightcyan",
    opacity=0.25,
)

ptd.add_parametric_curve_3d(fig, alpha, 0, 2.6)

for t in t_values:
    P = alpha(t)
    T_t = T(t)

    bottom = np.array([P[0], P[1], z_min])
    top = np.array([P[0], P[1], z_max])

    ptd.add_points_3d(fig, [P], point_size=12)
    ptd.add_segment_3d(fig, bottom, top, color="gray")
    ptd.add_vector_3d(fig, P, T_t)

    ptd.add_angle_3d(fig, P, T_t, u, label=r"$\theta$")


# 한 점에서만 u 방향벡터 표시
t_u = t_values[1]
P_u = alpha(t_u)

ptd.add_vector_3d(fig, P_u, u, color = "red")
ptd.add_labels_3d(fig, [P_u + u], [r"$u$"])


fig.show()