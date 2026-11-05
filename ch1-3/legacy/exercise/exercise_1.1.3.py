"""
연습문제 1.1 3번
평행사변형의 두 대각선은 서로 이등분함을 증명하라

서로 평행하지 않은 두 벡터로 생성되는 평행사변형을 통해 직접 나타낸다
"""
import numpy as np
import plotly.graph_objects as go
import plot2d_tools_diffgeo as p2d

a = np.array([1,2])
b = np.array([3,1])

o = np.array([0,0])
m = (a+b)/2

fig = go.Figure()

p2d.add_vector(fig, o, a, color = "red")
p2d.add_vector(fig, o, b, color = "blue")

p2d.add_curve(fig, [o, a, a+b, b, o], color = "black")
p2d.add_curve(fig, [o, m], color = "gray")
p2d.add_curve(fig, [a, m], color = "gray")
p2d.add_curve(fig, [b, m], color = "gray")
p2d.add_curve(fig, [a+b, m], color = "gray")

p2d.add_points(fig, [o,a,b,a+b,m])

fig.add_annotation(x = m[0], y = m[1], text = "교점", showarrow = False, xshift = 15, yshift = 15, font = dict(size = 20))

om = abs(np.linalg.norm(m))
am = abs(np.linalg.norm(m-a))
bm = abs(np.linalg.norm(m-b))
cm = abs(np.linalg.norm(m-(a+b)))

# 각 선분 중점
mid_om = (o + m) / 2
mid_cm = (m + a + b) / 2
mid_am = (m + a) / 2
mid_bm = (m + b) / 2

# 각 선분 위에 길이 표시
fig.add_annotation(x = mid_om[0], y = mid_om[1], text = f"{om:.2f}", showarrow = False, yshift = 12)
fig.add_annotation(x = mid_cm[0], y = mid_cm[1], text = f"{cm:.2f}", showarrow = False, yshift = 12)
fig.add_annotation(x = mid_am[0], y = mid_am[1], text = f"{am:.2f}", showarrow = False, yshift = -12)
fig.add_annotation(x = mid_bm[0], y = mid_bm[1], text = f"{bm:.2f}", showarrow = False, yshift = -12)

fig.show()