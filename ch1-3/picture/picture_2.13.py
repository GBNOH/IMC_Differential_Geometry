import numpy as np
import pyvista as pv
import plot_tools_diffgeo as ptd


O = np.array([0, 0, 0])

c = 0.4
k = np.sqrt(1 - c**2)


def phi(s):
    return c * s


def theta(s):
    p = phi(s)
    return k / c * np.log(1 / np.cos(p) + np.tan(p))


def gamma(s):
    p = phi(s)
    t = theta(s)

    return np.array([
        np.cos(p) * np.cos(t),
        np.cos(p) * np.sin(t),
        np.sin(p),
    ])


def gamma_prime(s):
    p = phi(s)
    t = theta(s)

    return np.array([
        -c * np.sin(p) * np.cos(t) - k * np.sin(t),
        -c * np.sin(p) * np.sin(t) + k * np.cos(t),
        c * np.cos(p),
    ])


s_max = 0.9 * np.pi / (2 * c)
s0 = 0.8

p = gamma(s0)
T = gamma_prime(s0)

fig = ptd.create_figure_3d()

sphere = pv.Sphere(radius=1.0, theta_resolution=60, phi_resolution=60)
fig.add_mesh(sphere, color="lightcyan", opacity=0.18)

ptd.add_parametric_curve_3d(fig, gamma, -s_max, s_max)
ptd.add_segment_3d(fig, O, p, color="gray", opacity=0.6)
ptd.add_vector_3d(fig, p, T)

ptd.add_points_3d(fig, [O, p])
ptd.add_labels_3d(fig, [O, p, p + T, gamma(1.6)], [r"$O$", r"$p$", r"$\gamma'(s)$", r"$\gamma(s)$"])

fig.show()