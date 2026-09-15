import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])

def alpha(t):
    return np.array([t, 0.35 * t**3 - 0.8 * t, 0.6 * np.sin(t) + 1.2])

def alpha_prime(t):
    return np.array([1, 1.05 * t**2 - 0.8, 0.6 * np.cos(t)])


t = 0.6
P = alpha(t)
v = alpha_prime(t)

t_values = np.linspace(-2.2, 2.4, 400)
curve_points = np.array([alpha(s) for s in t_values])

ptd.add_coordinate_axes_3d(fig, axis_length=3.2, show_labels=False, positive_only=True)
ptd.add_labels_3d(fig, [O, [3.35, 0, 0], [0, 3.35, 0], [0, 0, 3.35]], [r"$O$", r"$x$", r"$y$", r"$z$"])

ptd.add_curve_3d(fig, curve_points)
ptd.add_points_3d(fig, [P], point_size=12)
ptd.add_vector_3d(fig, P, v)
ptd.add_labels_3d(fig, [P, P + v], [r"$\alpha(t)$", r"$\alpha'(t)$"])

fig.show()

### 9/14 구간을 나타내도 크게 의미하는 바가 없다고 생각되어 생략 / 곡선 임의 변경