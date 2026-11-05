"""
그림 1.1

내적의 기하학적 의미
b의 a 방향 정사영의 크기를 나타낸다.
"""

import numpy as np
import plot_tools_diffgeo as ptd


a = np.array([2, 0])
b = np.array([1, 1])
O = np.array([0, 0])

a_norm = np.linalg.norm(a)
b_norm = np.linalg.norm(b)

if np.isclose(a_norm, 0) or np.isclose(b_norm, 0):
    raise ValueError("a와 b는 영벡터일 수 없습니다.")


# a 방향을 새로운 x축으로 잡는다.
e1 = a / a_norm
e2 = np.array([-e1[1], e1[0]])

# b가 위쪽 반평면에 놓이도록 e2의 방향만 선택한다.
if np.dot(b, e2) < 0:
    e2 = -e2

b_parallel = np.dot(b, e1)
b_perpendicular = np.dot(b, e2)

if b_parallel <= 0:
    raise ValueError("그림 1.1은 b의 a 방향 사영이 양수인 경우를 나타냅니다.")

A = np.array([a_norm, 0])
P = np.array([b_parallel, 0])
B = np.array([b_parallel, b_perpendicular])

fig = ptd.create_figure_2d()

ptd.add_filled_region_2d(fig, [O, P, B])

ptd.add_vector_2d(fig, O, A)
ptd.add_vector_2d(fig, O, B)

ptd.add_segment_2d(fig, P, B, color="gray", dash="dot")

ptd.add_angle_2d(fig, O, A, B, label=r"$\theta$", radius = 0.2)
ptd.add_angle_2d(fig, P, O - P, B - P, radius = 0.2)

ptd.add_labels_2d(fig, [0.88 * A, 0.5 * B], [r"$a$", r"$b$"], font_size = 20)

ptd.add_dimension_line_2d(fig, 0, P[0], -0.7, text=r"$\|b\|\cos\theta$")

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

fig.show()