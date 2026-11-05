import numpy as np
import plotly.graph_objects as go

def create_figure(title=None):

    fig = go.Figure()

    fig.update_layout(
        title=title,
        xaxis=dict(
            title="x",
        ),
        yaxis=dict(
            title="y",
            scaleanchor="x",         # x축과 y축의 단위 길이를 동일하게 설정
            scaleratio=1,
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig

def add_points(
    fig,
    points,                         # 하나 이상의 점으로 이루어진 (n, 2) 형태의 배열
    *,
    name=None,
    color="black",
    size=6,
    symbol="circle",
    opacity=0.7,
):

    points = np.asarray(points, dtype=float)

    if points.shape == (2,):
        points = points.reshape(1, 2)

    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError(
            "points는 [x, y] 또는 (n, 2) 형태여야 합니다."
        )

    if size <= 0:
        raise ValueError("size는 0보다 커야 합니다.")

    if not 0 <= opacity <= 1:
        raise ValueError("opacity는 0 이상 1 이하여야 합니다.")

    fig.add_trace(
        go.Scatter(
            x=points[:, 0],
            y=points[:, 1],
            mode="markers",
            name=name,
            marker=dict(
                color=color,
                size=size,
                symbol=symbol,
                opacity=opacity,
            ),
            showlegend=(name is not None)
        )
    )

    return fig

def add_curve(
    fig,
    points,                         # 공간 좌표들의 모임 (n, 2)
    *,
    name=None,
    color="blue",
    width=5,
    dash="solid"
):

    points = np.asarray(points, dtype=float)

    # 오입력 방지
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError(
            "points는 (n, 2) 형태(즉, nx2)여야 합니다."
        )

    fig.add_trace(
        go.Scatter(
            x=points[:, 0],         # x좌표 추출
            y=points[:, 1],         # y좌표 추출
            mode="lines",
            name=name,
            line=dict(
                color=color,
                width=width,
                dash=dash
            ),
            showlegend=(name is not None)
        )
    )

    return fig

def add_vector(
    fig,
    origin,
    vector,
    *,
    color="red",
    width=3,
    show_magnitude = False,
    name = "",
    row = None,
    col = None,
):

    if (row is None) != (col is None):
        raise ValueError("row와 col은 둘 다 지정하거나 둘 다 생략해야 합니다.")
    
    origin = np.asarray(origin, dtype=float)
    vector = np.asarray(vector, dtype=float)

    end = origin + vector
    vector_length = np.linalg.norm(vector)

    if row is None:

        xref = "x"
        yref = "y"

    else:

        subplot = fig.get_subplot(row,col)

        if subplot is None:

            raise ValueError(f"({row},{col})위치에 subplot이 없습니다.")

        xref = subplot.xaxis.plotly_name.replace("axis", "")
        yref = subplot.yaxis.plotly_name.replace("axis", "")

    fig.add_annotation(
        x = end[0],
        y = end[1],
        ax = origin[0],
        ay = origin[1],

        xref = xref,
        yref = yref,
        axref = xref,
        ayref = yref,

        text = name,

        showarrow = True,
        arrowhead = 3,
        arrowwidth = width,
        arrowcolor = color,
    )

    if show_magnitude:

        midpoint = origin + vector / 2

        if np.isclose(vector_length, round(vector_length)):

            magnitude_text = str(int(round(vector_length)))

        else:
            magnitude_text = f"{vector_length:.2f}"

        fig.add_annotation(
            x=midpoint[0],
            y=midpoint[1],

            xref=xref,
            yref=yref,

            text=magnitude_text,

            showarrow=False,

            font=dict(
                color=color
            ),

            yshift=10
        )

    fig.add_trace(go.Scatter(
        x=[end[0]], y=[end[1]],
        mode="markers",
        marker=dict(size=1, opacity=0),
        showlegend=False,
        hoverinfo="skip"
    )
)  

def display_angle(
    fig,
    vertex,                         # 교점
    point1,                         # 첫 번째 벡터의 종점
    point2,                         # 두 번째 벡터의 종점
    *,
    radius=0.5,                     # 각 표시의 크기
    label=None,                     # 표시할 기호 ("θ", "α" 등)
    show_degree=True,               # 각도 숫자 표시 여부
    decimals=1,                     # 각도 소수점 자릿수
    color="black",                  # 선과 글자의 색
    width=2,                        # 선 굵기
    font_size=14,                   # 글자 크기
    text_distance=1.3,              # 글자의 위치
    show_right_angle=True,          # 직각일 때 ㄱ자 표시 여부
):

    # NumPy 배열로 변환
    vertex = np.asarray(vertex, dtype=float)
    point1 = np.asarray(point1, dtype=float)
    point2 = np.asarray(point2, dtype=float)

    # 입력값 검사
    if (
        vertex.shape != (2,)
        or point1.shape != (2,)
        or point2.shape != (2,)
    ):
        raise ValueError(
            "vertex, point1, point2는 길이가 2인 배열이어야 합니다."
        )

    # 교점에서 각 종점으로 향하는 벡터
    v1 = point1 - vertex
    v2 = point2 - vertex

    # 각 벡터의 크기
    length1 = np.linalg.norm(v1)
    length2 = np.linalg.norm(v2)

    # 영벡터 검사
    if np.isclose(length1, 0) or np.isclose(length2, 0):
        raise ValueError(
            "종점은 교점과 달라야 합니다."
        )

    # 단위벡터
    e1 = v1 / length1
    e2 = v2 / length2

    # 두 단위벡터의 내적
    dot = np.dot(e1, e2)

    # 2차원 외적에 해당하는 값
    cross = (
        e1[0] * e2[1]
        - e1[1] * e2[0]
    )

    # v1에서 v2로 향하는 부호 있는 각
    signed_angle = np.arctan2(cross, dot)

    # 두 벡터 사이의 작은 각
    angle = abs(signed_angle)

    # degree로 변환
    degree = np.degrees(angle)

    # e1에 수직인 단위벡터
    normal = np.array([
        -e1[1],
        e1[0]
    ])

    # ------ 표시 ------

    is_right_angle = np.isclose(
        dot,
        0.0,
        atol=1e-6
    )

    if show_right_angle and is_right_angle:

        corner1 = vertex + radius * e1
        corner2 = (vertex + radius * e1 + radius * e2)
        corner3 = vertex + radius * e2

        add_curve(fig, np.array([corner1, corner2, corner3]), color=color, width=width)

    else:

        t = np.linspace(0, signed_angle, 100)

        add_curve(fig, vertex + radius*(np.cos(t)[:, None]*e1 + np.sin(t)[:, None]*normal), color=color, width=width)

    # ------ 표시할 문자 결정 ------

    if label is not None and show_degree:

        text = (f"{label} = " f"{degree:.{decimals}f}°")

    elif label is not None:

        text = label

    elif show_degree:

        text = f"{degree:.{decimals}f}°"

    else:

        text = None

    # ------ 글자 위치 ------

    if text is not None:

        middle_angle = signed_angle / 2

        text_direction = (
            np.cos(middle_angle) * e1
            + np.sin(middle_angle) * normal
        )

        text_position = (
            vertex
            + text_distance
            * radius
            * text_direction
        )

        fig.add_annotation(
            x=text_position[0],
            y=text_position[1],
            text=text,
            showarrow=False,
            font=dict(
                size=font_size,
                color=color
            )
        )