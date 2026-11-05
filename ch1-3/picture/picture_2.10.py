import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])


def beta(s):
    return np.array([s, 0.2 * s**2, 0])


def T(s):
    v = np.array([1, 0.4 * s, 0])
    return v / np.linalg.norm(v)


def B(s):
    return np.array([0, 0, 1])


def N(s):
    return np.cross(B(s), T(s))


s = 1.6

beta_0 = beta(0)
beta_s = beta(s)

T_s = T(s)
N_s = N(s)
B_s = B(s)

d = beta_0 - beta_s

u = np.linspace(-0.4, 3.0, 400)
curve_points = np.array([beta(value) for value in u])

ptd.add_plane_3d(fig, O, [1, 0, 0], [0, 1, 0], u_range=(-0.5, 3.4), v_range=(-0.8, 2.0), opacity=0.18)
ptd.add_curve_3d(fig, curve_points)
ptd.add_points_3d(fig, [beta_0, beta_s], point_size=12)

ptd.add_vector_3d(fig, beta_s, d, color="red")
ptd.add_vector_3d(fig, beta_s, T_s)
ptd.add_vector_3d(fig, beta_s, N_s)
ptd.add_vector_3d(fig, beta_s, B_s)

ptd.add_angle_3d(fig, beta_s, d, B_s, color="red")

ptd.add_labels_3d(
    fig,
    [
        beta_0,
        beta_s,
        beta_s + d,
        beta_s + T_s,
        beta_s + N_s,
        beta_s + B_s,
        np.array([1.7, 1.2, 0]),
    ],
    [
        r"$\beta(0)$",
        r"$\beta(s)$",
        r"$\beta(s)-\beta(0)$",
        r"$T(s)$",
        r"$N(s)$",
        r"$B(s)$",
        r"$\langle \beta(0)-\beta(s),\,B(s)\rangle=0$",
    ],
)

fig.show()