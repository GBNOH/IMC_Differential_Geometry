r"""2011학년도 35번: 원나선의 길이를 원기둥의 전개도로 설명한다.

gamma(t)=(a cos t, a sin t, bt), P=(2,0,4π), Q=(2,0,8π).
a>0이므로 a=2. Δz=4π, L=4√10 π에서
L²=(a Δt)²+(Δz)², Δt=Δz/b이므로 b=2/3, a+b=8/3 (정답 ①).
t_P=6π, t_Q=12π이므로 P에서 Q까지 세 바퀴 돈다.
전개 좌표는 u=a(t-t_P), v=b(t-t_P)이다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2011_q35_helix_length.py
    python .\supplement_exam\exam_2011_q35_helix_length.py --output output/exam_2011_q35.html --no-show
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def solve_parameters() -> tuple[float, float]:
    """두 점과 호길이 조건으로부터 양수 a, b를 계산한다."""
    a = 2.0
    height = 4 * np.pi
    length = 4 * np.sqrt(10) * np.pi
    b = a * height / np.sqrt(length**2 - height**2)
    return a, b


def gamma(t: np.ndarray | float, a: float, b: float) -> np.ndarray:
    """원나선의 좌표를 마지막 축에 반환한다."""
    t = np.asarray(t)
    return np.stack((a*np.cos(t), a*np.sin(t), b*t), axis=-1)


def developed_curve(t: np.ndarray | float, a: float, b: float) -> np.ndarray:
    """P를 원점으로 하는 원기둥 전개 좌표 (u,v)를 반환한다."""
    delta = np.asarray(t) - 4*np.pi/b
    return np.stack((a*delta, b*delta), axis=-1)


# 이 문항의 시각화 구성
def build_figure() -> go.Figure:
    """원나선과 전개도를 같은 진행률로 탐색하는 그림을 만든다."""
    a, b = solve_parameters()
    start, end = 4*np.pi/b, 8*np.pi/b
    t = np.linspace(start, end, 901)
    points = gamma(t, a, b)
    flat = developed_curve(t, a, b)
    figure = make_subplots(
        rows=1, cols=2, specs=[[dict(type="scene"), dict(type="xy")]],
        column_widths=[.48, .52], horizontal_spacing=.08,
        subplot_titles=("P → Q: 반지름 2인 원기둥 위의 세 바퀴", "전개도: 가로 12π, 높이 4π"),
    )
    angle, height = np.meshgrid(np.linspace(0, 2*np.pi, 65), np.linspace(4*np.pi, 8*np.pi, 35))
    figure.add_trace(go.Surface(
        x=a*np.cos(angle), y=a*np.sin(angle), z=height,
        opacity=.15, colorscale=[[0, "#82A6C8"], [1, "#82A6C8"]],
        showscale=False, name="원기둥 x²+y²=4", showlegend=True, hoverinfo="skip",
    ), row=1, col=1)
    figure.add_trace(go.Scatter3d(
        x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="lines",
        line=dict(color="#7040A0", width=7), name="원나선 P → Q",
    ), row=1, col=1)
    ends = points[[0, -1]]
    figure.add_trace(go.Scatter3d(
        x=ends[:, 0], y=ends[:, 1], z=ends[:, 2], mode="markers+text",
        marker=dict(color="#222222", size=5), text=["P (2,0,4π)", "Q (2,0,8π)"],
        textposition="top center", showlegend=False,
    ), row=1, col=1)
    figure.add_trace(go.Scatter(
        x=flat[:, 0], y=flat[:, 1], mode="lines",
        line=dict(color="#7040A0", width=5), name="펼친 곡선 · 길이 4√10π",
    ), row=1, col=2)
    figure.add_trace(go.Scatter(
        x=[0, 12*np.pi, 12*np.pi], y=[0, 0, 4*np.pi], mode="lines",
        line=dict(color="#777777", width=2, dash="dash"),
        name="수평 이동과 높이 변화",
    ), row=1, col=2)
    figure.add_trace(go.Scatter(
        x=[0, 12*np.pi], y=[0, 4*np.pi], mode="markers+text",
        text=["P′", "Q′"], textposition="top left",
        marker=dict(color="#222222", size=8), showlegend=False,
    ), row=1, col=2)
    for turn in (1, 2):
        figure.add_shape(type="line", x0=turn*4*np.pi, x1=turn*4*np.pi,
                         y0=0, y1=4*np.pi, line=dict(color="#BBBBBB", dash="dot"), row=1, col=2)

    def markers(parameter: float) -> list:
        """같은 매개변수에 대응하는 두 화면의 관찰점을 반환한다."""
        point = gamma(parameter, a, b)
        uv = developed_curve(parameter, a, b)
        return [
            go.Scatter3d(x=[point[0]], y=[point[1]], z=[point[2]], mode="markers",
                         marker=dict(color="#E45756", size=7), name="현재 위치", showlegend=False),
            go.Scatter(x=[uv[0]], y=[uv[1]], mode="markers",
                       marker=dict(color="#E45756", size=12), name="현재 위치", showlegend=False),
        ]

    first, second = markers(start)
    figure.add_trace(first, row=1, col=1)
    figure.add_trace(second, row=1, col=2)
    indices = [len(figure.data)-2, len(figure.data)-1]
    parameters = np.linspace(start, end, 49)
    figure.frames = [go.Frame(name=str(i), data=markers(float(value)), traces=indices)
                     for i, value in enumerate(parameters)]
    figure.update_xaxes(title_text="u = a(t−t_P) · 원주 방향 거리",
                        tickvals=np.arange(4)*4*np.pi, ticktext=["0", "4π", "8π", "12π"],
                        range=[-2, 12*np.pi+3], row=1, col=2)
    figure.update_yaxes(title_text="v = z−4π · 높이 변화", scaleanchor="x", scaleratio=1,
                        tickvals=[0, 2*np.pi, 4*np.pi], ticktext=["0", "2π", "4π"],
                        range=[-2, 4*np.pi+3], row=1, col=2)
    figure.update_layout(
        title=dict(text="2011학년도 35번 · 원나선의 길이"
                   "<br><sup>L²=(12π)²+(4π)² ⇒ a=2, b=2/3, a+b=8/3 · 정답 ①</sup>", x=.5),
        template="plotly_white", height=800, margin=dict(l=35, r=30, t=120, b=160),
        scene=dict(aspectmode="data", xaxis_title="x", yaxis_title="y", zaxis_title="z",
                   zaxis=dict(tickvals=[4*np.pi, 6*np.pi, 8*np.pi], ticktext=["4π", "6π", "8π"]),
                   uirevision="camera", camera=dict(eye=dict(x=1.7, y=1.7, z=.7))),
        legend=dict(orientation="h", y=-.23),
        sliders=[dict(y=-.08, currentvalue=dict(prefix="P에서 진행한 회전 수: "), steps=[
            dict(label=f"{i/16:.2f}", method="animate", args=[[str(i)],
                 dict(mode="immediate", frame=dict(duration=0, redraw=True),
                      transition=dict(duration=0))]) for i in range(49)])],
    )
    return figure


# 실행 옵션과 HTML 저장
def parse_args() -> argparse.Namespace:
    """HTML 저장과 화면 표시 옵션을 읽는다."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="대화형 HTML을 저장할 경로")
    parser.add_argument("--no-show", action="store_true", help="브라우저 창을 열지 않음")
    return parser.parse_args()


def main() -> None:
    """그림을 생성하고 HTML 저장 또는 화면 표시를 실행한다."""
    args = parse_args()
    figure = build_figure()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        figure.write_html(args.output, include_plotlyjs=True)
        print(f"저장 완료: {args.output.resolve()}")
    if not args.no_show:
        figure.show()


if __name__ == "__main__":
    main()
