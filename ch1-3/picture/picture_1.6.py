"""
그림 1.6

평행하지 않은 두 벡터 u, v와 점 a가 주어졌을 때
a를 지나고 u, v에 평행한 평면

x = a + λu + μv
"""

import numpy as np
import plot_tools_diffgeo as ptd
import pyvista as pv

def add_dashed_segment(fig, point1, point2, dash_length=0.12, gap_length=0.08):
    point1 = np.asarray(point1, dtype=float)
    point2 = np.asarray(point2, dtype=float)

    vector = point2 - point1
    length = np.linalg.norm(vector)

    if np.isclose(length, 0):
        raise ValueError("두 점은 서로 달라야 합니다.")

    direction = vector / length
    s = 0.0

    while s < length:
        t = min(s + dash_length, length)
        ptd.add_segment_3d(fig, point1 + s * direction, point1 + t * direction)
        s += dash_length + gap_length

def add_cone_head(fig, tip, direction, height=0.12, radius=0.04):
    tip = np.asarray(tip, dtype=float)
    direction = np.asarray(direction, dtype=float)

    norm = np.linalg.norm(direction)

    if np.isclose(norm, 0):
        raise ValueError("direction은 영벡터일 수 없습니다.")

    direction = direction / norm
    center = tip - 0.5 * height * direction

    cone = pv.Cone(center=center, direction=direction, height=height, radius=radius)
    fig.add_mesh(cone, color="black", opacity = 0.5)

a = np.array([0, 0, 0])
u = np.array([1, 0.4, 0])
v = np.array([0.4, 1, 0])

lam = 2.0
mu = 1.8

if np.allclose(np.cross(u, v), 0):
    raise ValueError("u와 v는 평행하지 않아야 합니다.")

U = a + u
V = a + v
P = a + lam * u
Q = a + mu * v
x = a + lam * u + mu * v

fig = ptd.create_figure_3d()

ptd.add_plane_3d(fig, a, u, v, color = "cyan", opacity = 0.35,u_range=(-0.4, 2.5), v_range=(-0.4, 2.3), show_edges=True)

ptd.add_vector_3d(fig, a, u, name=r"$u$")
ptd.add_vector_3d(fig, a, v, name=r"$v$")
ptd.add_vector_3d(fig, a, x - a, name=r"$x-a=\lambda u+\mu v$")

add_dashed_segment(fig, U, P)
add_dashed_segment(fig, V, Q)
add_dashed_segment(fig, P, x)
add_dashed_segment(fig, Q, x)

add_cone_head(fig, P, u)
add_cone_head(fig, Q, v)

ptd.add_points_3d(fig, [a, x])
ptd.add_labels_3d(
    fig,
    [a, x, 0.5 * (U + P), 0.5 * (V + Q)],
    [r"$a$", r"$x$", r"$\lambda u$", r"$\mu v$"],
)

fig.show()