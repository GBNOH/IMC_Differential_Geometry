r"""2013학년도 1차 33번: 거울상 원나선의 곡률과 비틀림.

alpha(t)=(3 cos(t/5),3 sin(t/5),4t/5),
beta(t)=(3 cos(t/5),3 sin(t/5),-4t/5)는 단위속력곡선이다.
두 곡선의 곡률은 3/25, 비틀림은 각각 4/25와 -4/25이다.
beta=diag(1,1,-1) alpha이며 이 반사의 행렬식은 -1이다.
행렬식 1인 직교변환은 비틀림을 보존하므로 주어진 대응을 만들 수 없다.
따라서 ㄱ, ㄴ만 참: 정답 ③. 화면은 -5π≤t≤5π 구간을 표시한다.
T,N,B 화살표는 모두 실제 길이 1인 단위벡터이다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2013_q33_reflected_helices.py
    python .\supplement_exam\exam_2013_q33_reflected_helices.py --output output/exam_2013_q33.html --no-show
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def curve(t: np.ndarray | float, sign: int = 1) -> np.ndarray:
    """sign=1이면 alpha, -1이면 beta의 좌표를 반환한다."""
    if sign not in (-1, 1):
        raise ValueError("sign은 1 또는 -1이어야 합니다.")
    t = np.asarray(t)
    return np.stack((3*np.cos(t/5), 3*np.sin(t/5), sign*4*t/5), axis=-1)


def derivatives(t: float, sign: int = 1) -> tuple[np.ndarray, ...]:
    """곡선의 1, 2, 3계 도함수를 반환한다."""
    return (
        np.array([-3*np.sin(t/5)/5, 3*np.cos(t/5)/5, sign*4/5]),
        np.array([-3*np.cos(t/5)/25, -3*np.sin(t/5)/25, 0.]),
        np.array([3*np.sin(t/5)/125, -3*np.cos(t/5)/125, 0.]),
    )


def geometry(t: float, sign: int = 1) -> tuple[float, float, np.ndarray]:
    """도함수로 곡률, 비틀림, 행이 T,N,B인 Frenet 표구를 계산한다."""
    first, second, third = derivatives(t, sign)
    cross = np.cross(first, second)
    curvature = np.linalg.norm(cross) / np.linalg.norm(first)**3
    torsion = np.dot(cross, third) / np.dot(cross, cross)
    tangent = first / np.linalg.norm(first)
    binormal = cross / np.linalg.norm(cross)
    normal = np.cross(binormal, tangent)
    return float(curvature), float(torsion), np.stack((tangent, normal, binormal))


# 이 문항의 시각화 구성
def moving_traces(t: float, sign: int) -> list:
    """관찰점과 단위 Frenet 표구를 만든다."""
    point = curve(t, sign)
    k, tau, frame = geometry(t, sign)
    traces = [go.Scatter3d(
        x=[point[0]], y=[point[1]], z=[point[2]], mode="markers",
        marker=dict(size=6, color="#222222"), showlegend=False,
        hovertemplate=f"t={t:.3f}<br>κ={k:.2f}<br>τ={tau:.2f}<extra></extra>",
    )]
    for label, color, vector in zip(("T", "N", "B"), ("#E45756", "#239B56", "#4C78A8"), frame):
        end = point + vector
        traces.append(go.Scatter3d(
            x=[point[0], end[0]], y=[point[1], end[1]], z=[point[2], end[2]],
            mode="lines", line=dict(color=color, width=7), name=label,
            legendgroup=label, showlegend=sign == 1,
        ))
        traces.append(go.Cone(
            x=[end[0]], y=[end[1]], z=[end[2]], u=[vector[0]], v=[vector[1]], w=[vector[2]],
            anchor="tip", sizemode="absolute", sizeref=.22,
            colorscale=[[0, color], [1, color]], showscale=False, hoverinfo="skip",
        ))
    return traces


def build_figure() -> go.Figure:
    """두 원나선과 대응 표구를 같은 축척으로 나란히 표시한다."""
    figure = make_subplots(
        rows=1, cols=2, specs=[[dict(type="scene"), dict(type="scene")]],
        subplot_titles=("α: κ=3/25, τ=4/25", "β: κ=3/25, τ=−4/25"), horizontal_spacing=.05,
    )
    indices = []
    t = np.linspace(-5*np.pi, 5*np.pi, 701)
    for col, sign, label in ((1, 1, "α"), (2, -1, "β")):
        points = curve(t, sign)
        figure.add_trace(go.Scatter3d(
            x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="lines",
            line=dict(color="#7040A0", width=6), name=label,
        ), row=1, col=col)
        x, y = np.meshgrid([-4, 4], [-4, 4])
        figure.add_trace(go.Surface(
            x=x, y=y, z=np.zeros_like(x), opacity=.15,
            colorscale=[[0, "#999999"], [1, "#999999"]], showscale=False,
            name="반사 평면 z=0", showlegend=col == 1, hoverinfo="skip",
        ), row=1, col=col)
        for trace in moving_traces(0, sign):
            indices.append(len(figure.data))
            figure.add_trace(trace, row=1, col=col)
    parameters = np.linspace(-5*np.pi, 5*np.pi, 41)
    figure.frames = [go.Frame(name=str(i), data=moving_traces(float(t), 1)+moving_traces(float(t), -1),
                             traces=indices) for i, t in enumerate(parameters)]
    scene = dict(xaxis=dict(title="x", range=[-4.5, 4.5]),
                 yaxis=dict(title="y", range=[-4.5, 4.5]),
                 zaxis=dict(title="z", range=[-14, 14]), aspectmode="data",
                 uirevision="camera", camera=dict(eye=dict(x=1.6, y=1.6, z=.6)))
    figure.update_layout(
        title=dict(text="2013학년도 1차 33번 · 거울상 원나선"
                   "<br><sup>같은 곡률, 반대 부호의 비틀림 · 정답 ③ (ㄱ, ㄴ)</sup>", x=.5),
        template="plotly_white", height=820, margin=dict(l=20, r=20, t=110, b=180),
        scene=scene, scene2=scene, legend=dict(orientation="h", y=-.23),
        sliders=[dict(active=20, y=-.07, currentvalue=dict(prefix="대응점 t = "), steps=[
            dict(label=f"{t/np.pi:.2f}π", method="animate", args=[[str(i)],
                 dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))])
            for i, t in enumerate(parameters)])],
    )
    figure.add_annotation(
        text="반사 L=diag(1,1,−1): det L=−1. det L=1인 직교변환은 비틀림을 보존하므로 ㄷ은 거짓.",
        xref="paper", yref="paper", x=.5, y=-.34, showarrow=False,
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
