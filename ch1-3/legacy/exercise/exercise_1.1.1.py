"""
연습문제 1.1 1번
유클리드평면 E^2에 속하는 두 벡터 a, b가 동일직선 위에 있지 않으면, E^2의 임의의 벡터는 a와 b로 나타낼 수 있음을 보여라.

subplot을 이용하여 동일직선 위에 있는 경우와 그렇지 않은 경우에 대해 생성하는 공간을 grid형식으로 나타낸다.
"""
import numpy as np
import plotly.graph_objects as go
import plot2d_tools_diffgeo as p2d
from plotly.subplots import make_subplots

# 사용자 변경 - 벡터

a = np.array([2, 1])
b = np.array([1, 1])
k = -0.5
v = np.array([1, 2])

# 사용자 변경 - 서식

grid_style = dict(
    color = "lightgray",
    width = 1
)

#--------------------------------------------#

O = np.array([0, 0])
A = np.column_stack((a, b))
s, t = np.linalg.solve(A, v)

sa = s*a

a_parallel = a
b_parallel = k*a

# subplot 설정
fig = make_subplots(
    rows = 1, cols = 2,
    subplot_titles = (
        "a, b가 평행하지 않은 경우",
        "a, b가 평행한 경우"
    ),
    horizontal_spacing = 0.08
)

fig.update_xaxes(
    range=[-6, 6],
    zeroline=True,
    zerolinecolor="black",
    showgrid=False,
    row = 1, col = 1
)

fig.update_yaxes(
    range=[-6, 6],
    zeroline=True,
    zerolinecolor="black",
    showgrid=False,

    scaleanchor="x",
    scaleratio=1,

    row = 1, col = 1
)

fig.update_xaxes(
    range=[-6, 6],
    zeroline=True,
    zerolinecolor="black",
    showgrid=False,
    row = 1, col = 2
)

fig.update_yaxes(
    range=[-6, 6],
    zeroline=True,
    zerolinecolor="black",
    showgrid=False,

    scaleanchor="x2",
    scaleratio=1,

    row = 1,col = 2
)

fig.update_layout(
    title="두 벡터가 생성하는 부분공간",

    width=1200,
    height=600,

    template="plotly_white",

    showlegend=False
)

# 1. 평행하지 않은 경우

# grid 생성
straight_line = np.array([-20, 20])

for k in range(-17, 18):

    for grid_line in [
        k * b + straight_line[:, None] * a,
        k * a + straight_line[:, None] * b
    ]:
        
        fig.add_trace(
            go.Scatter(
                x=grid_line[:, 0],
                y=grid_line[:, 1],

                mode="lines",

                line=grid_style,

                hoverinfo="skip",
                showlegend=False
            ),
            row = 1, col = 1
        )

# 각 벡터 표현
p2d.add_vector(fig, O, a, color="red", row=1, col=1)
p2d.add_vector(fig, O, b, color="blue", row=1, col=1)
p2d.add_vector(fig, O, v, color="green", width=3, row=1, col=1)

# 생성 가능 보이기
fig.add_trace(
    go.Scatter(
        x=[O[0], sa[0], v[0]],
        y=[O[1], sa[1], v[1]],

        mode="lines",

        line=dict(
            color="gray",
            width=2,
            dash="dash"
        ),
        hoverinfo="skip",
        showlegend=False
    ),
    row = 1, col = 1
)

mid_sa = (O + sa) / 2
mid_tb = (sa + v) / 2

fig.add_annotation(
    x=mid_sa[0],
    y=mid_sa[1],
    text=f"{s}",
    showarrow=False,
    yshift=10,
    row=1,
    col=1
)

fig.add_annotation(
    x=mid_tb[0],
    y=mid_tb[1],
    text=f"{t}",
    showarrow=False,
    yshift=10,
    row=1,
    col=1
)

# 2. 평행한 경우

# 그리드 (직선) 생성
span_line = straight_line[:, None] * a_parallel

fig.add_trace(
    go.Scatter(
        x=span_line[:, 0],
        y=span_line[:, 1],

        mode="lines",

        line=dict(
            color="lightgray",
            width=2,
            dash="dash"
        ),

        hoverinfo="skip",
        showlegend=False
    ),
    row = 1, col = 2
)

p2d.add_vector(fig, O, a_parallel, color="red", row=1, col=2)
p2d.add_vector(fig, O, b_parallel, color="blue", row=1, col=2)
p2d.add_vector(fig, O, v, color="green", width=3, row=1, col=2)

fig.show()