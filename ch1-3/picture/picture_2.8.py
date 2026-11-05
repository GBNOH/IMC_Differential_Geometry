import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])

a = 2
b = 1
c = np.sqrt(a**2 + b**2)


def beta(s):
    return np.array([
        a * np.cos(s / c),
        a * np.sin(s / c) + 1.5,
        b * s / c + 1,
    ])


def T(s):
    return np.array([
        -(a / c) * np.sin(s / c),
        (a / c) * np.cos(s / c),
        b / c,
    ])


def N(s):
    return np.array([
        -np.cos(s / c),
        -np.sin(s / c),
        0,
    ])


def B(s):
    return np.cross(T(s), N(s))


s = 0

P = beta(s)
T_s = T(s)
N_s = N(s)
B_s = B(s)


ptd.add_coordinate_axes_3d(fig, axis_length=4, positive_only=True)

ptd.add_parametric_curve_3d(fig, beta, -2.5, 3.0)
ptd.add_points_3d(fig, [P])

ptd.add_vector_3d(fig, P, T_s)
ptd.add_vector_3d(fig, P, N_s)
ptd.add_vector_3d(fig, P, B_s)

ptd.add_angle_3d(fig, P, T_s, N_s)
ptd.add_angle_3d(fig, P, N_s, B_s)
ptd.add_angle_3d(fig, P, T_s, B_s)

ptd.add_labels_3d(
    fig,
    [P + T_s, P + N_s, P + B_s],
    [r"$T$", r"$N$", r"$B$"],
)

ptd.add_labels_3d(
    fig,
    [beta(2.5)],
    [r"$\beta$"],
)

fig.show()