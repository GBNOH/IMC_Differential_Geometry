"""
그림 1.7

동일 직선상에 있지 않은 세 점 a, b, c를 지나는 평면

<x - a, (b - a) × (c - a)> = 0
"""

import numpy as np
import plot_tools_diffgeo as ptd


a = np.array([0, 0, 0])
b = np.array([2, -1, 0])
c = np.array([1, 1, 0])

ab = b - a
ac = c - a

n = np.cross(ab, ac)

if np.allclose(n, 0):
    raise ValueError("a, b, c는 동일 직선상에 있지 않아야 합니다.")

fig = ptd.create_figure_3d()

ptd.add_plane_3d(fig, a, ab, ac, color = "cyan", opacity = 0.35, u_range=(-0.35, 1.55), v_range=(-0.35, 1.45), show_edges=True)

ptd.add_vector_3d(fig, a, ab)
ptd.add_vector_3d(fig, a, ac)
ptd.add_vector_3d(fig, a, n, name=r"$(b-a)\times(c-a)$")

ptd.add_angle_3d(fig, a, n, ab, radius = 0.3)
ptd.add_angle_3d(fig, a, n, ac, radius = 0.3)

ptd.add_points_3d(fig, [a, b, c])
ptd.add_labels_3d(fig, [a, b, c], [r"$a$", r"$b$", r"$c$"])

fig.show()