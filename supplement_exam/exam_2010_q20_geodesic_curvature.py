r"""2010학년도 20번: 교선의 곡률벡터를 분해하여 측지곡률을 시각화한다.

S: z²-x²-y²=2, P: z=2의 교선은 alpha(t)=(√2 cos t, √2 sin t, 2).
곡선의 곡률은 kappa=1/√2이다. 위쪽 단위법선을 택하면
N=(-cos t/√3, -sin t/√3, √(2/3)), kappa_n=1/√6.
dT/ds=kappa_n N + K_g이므로 |kappa_g|=||K_g||=1/√3 (정답 ④).
그림에는 교선을 포함하는 S의 위쪽 연결성분만 표시한다.
화살표는 실제 벡터 길이를 사용하며, 슬라이더로 관찰점을 이동한다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2010_q20_geodesic_curvature.py
    python .\supplement_exam\exam_2010_q20_geodesic_curvature.py --output output/q20.html --no-show
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import plotly.graph_objects as go


# 수학적 정의와 계산
def alpha(t: np.ndarray | float) -> np.ndarray:
    """교선의 좌표를 마지막 축의 길이가 3인 배열로 반환한다."""
    t = np.asarray(t)
    return np.stack((np.sqrt(2) * np.cos(t), np.sqrt(2) * np.sin(t),
                     np.full_like(t, 2, dtype=float)), axis=-1)


def curvature_components(t: float) -> tuple[np.ndarray, ...]:
    """단위접선, 단위법선, 곡률벡터, 법곡률벡터, 측지곡률벡터를 반환한다."""
    tangent = np.array([-np.sin(t), np.cos(t), 0.])
    normal = np.array([-np.cos(t), -np.sin(t), np.sqrt(2)]) / np.sqrt(3)
    curvature = np.array([-np.cos(t), -np.sin(t), 0.]) / np.sqrt(2)
    normal_component = np.dot(curvature, normal) * normal
    geodesic_component = curvature - normal_component
    return tangent, normal, curvature, normal_component, geodesic_component


# 이 문항의 시각화 구성
def add_vector(figure: go.Figure, point: np.ndarray, vector: np.ndarray,
               name: str, color: str) -> None:
    """실제 길이의 선분과 끝점의 화살촉으로 벡터를 추가한다."""
    endpoint = point + vector
    figure.add_trace(go.Scatter3d(
        x=[point[0], endpoint[0]], y=[point[1], endpoint[1]], z=[point[2], endpoint[2]],
        mode="lines", line=dict(color=color, width=7), name=name,
        hovertemplate=name + f"<br>길이={np.linalg.norm(vector):.6f}<extra></extra>",
    ))
    figure.add_trace(go.Cone(
        x=[endpoint[0]], y=[endpoint[1]], z=[endpoint[2]],
        u=[vector[0]], v=[vector[1]], w=[vector[2]],
        anchor="tip", sizemode="absolute", sizeref=0.12,
        colorscale=[[0, color], [1, color]], showscale=False, showlegend=False,
        hoverinfo="skip",
    ))


def moving_traces(t: float) -> tuple:
    """관찰점에 종속되는 접평면과 곡률 분해 그림을 만든다."""
    figure = go.Figure()
    point = alpha(t)
    tangent, normal, curvature, normal_part, geodesic_part = curvature_components(t)
    other = np.cross(normal, tangent)
    u, v = np.meshgrid(np.linspace(-.85, .85, 2), np.linspace(-.85, .85, 2))
    plane = point + u[..., None] * tangent + v[..., None] * other
    figure.add_trace(go.Surface(
        x=plane[..., 0], y=plane[..., 1], z=plane[..., 2], opacity=.25,
        colorscale=[[0, "#54A24B"], [1, "#54A24B"]], showscale=False,
        name="관찰점의 접평면", showlegend=True, hoverinfo="skip",
    ))
    figure.add_trace(go.Scatter3d(
        x=[point[0]], y=[point[1]], z=[point[2]], mode="markers+text",
        text=["α(t)"], textposition="top center", name="관찰점",
        marker=dict(size=6, color="#222222"),
    ))
    for vector, name, color in (
        (curvature, "곡률벡터 dT/ds · 길이 1/√2", "#E45756"),
        (normal_part, "법선 성분 κₙN · 길이 1/√6", "#4C78A8"),
        (geodesic_part, "접평면 성분 K_g · 길이 1/√3", "#239B56"),
    ):
        add_vector(figure, point, vector, name, color)
    corners = np.array([point + normal_part, point + curvature, point + geodesic_part])
    figure.add_trace(go.Scatter3d(
        x=corners[:, 0], y=corners[:, 1], z=corners[:, 2], mode="lines",
        line=dict(color="#777777", width=3, dash="dash"),
        name="벡터의 합", showlegend=False, hoverinfo="skip",
    ))
    return figure.data


def build_figure() -> go.Figure:
    """곡면·교선과 관찰점을 이동할 수 있는 곡률 분해 그림을 만든다."""
    figure = go.Figure()
    r, theta = np.meshgrid(np.linspace(0, 2.2, 45), np.linspace(0, 2*np.pi, 100))
    figure.add_trace(go.Surface(
        x=r*np.cos(theta), y=r*np.sin(theta), z=np.sqrt(2+r*r),
        opacity=.22, colorscale=[[0, "#82A6C8"], [1, "#82A6C8"]],
        showscale=False, showlegend=True, name="S의 위쪽 성분",
        hovertemplate="S: z²−x²−y²=2<extra></extra>",
    ))
    x, y = np.meshgrid([-2.2, 2.2], [-2.2, 2.2])
    figure.add_trace(go.Surface(
        x=x, y=y, z=np.full_like(x, 2), opacity=.12,
        colorscale=[[0, "#F2A541"], [1, "#F2A541"]], showscale=False,
        showlegend=True, name="P: z=2", hoverinfo="skip",
    ))
    curve = alpha(np.linspace(0, 2*np.pi, 361))
    figure.add_trace(go.Scatter3d(
        x=curve[:, 0], y=curve[:, 1], z=curve[:, 2], mode="lines",
        line=dict(color="#7040A0", width=7), name="교선 α · 반지름 √2",
    ))
    figure.add_traces(moving_traces(0))
    moving_indices = list(range(3, len(figure.data)))
    parameters = np.linspace(0, 2*np.pi, 25)
    figure.frames = [go.Frame(name=str(i), data=moving_traces(float(t)), traces=moving_indices)
                     for i, t in enumerate(parameters)]
    figure.update_layout(
        title=dict(text="2010학년도 20번 · 측지곡률"
                   "<br><sup>κ² = κₙ² + κ_g² : 1/2 = 1/6 + 1/3 · 정답 ④</sup>", x=.5),
        template="plotly_white", height=850, margin=dict(l=20, r=20, t=105, b=160),
        scene=dict(aspectmode="data", xaxis_title="x", yaxis_title="y", zaxis_title="z",
                   xaxis=dict(range=[-2.4, 2.4]), yaxis=dict(range=[-2.4, 2.4]),
                   zaxis=dict(range=[.9, 3.2]), uirevision="camera",
                   camera=dict(eye=dict(x=1.6, y=1.5, z=1.1))),
        legend=dict(orientation="h", y=-.23),
        sliders=[dict(active=0, y=-.02, currentvalue=dict(prefix="관찰점 t = "), steps=[
            dict(label=f"{t/np.pi:.2f}π", method="animate", args=[[str(i)],
                 dict(mode="immediate", frame=dict(duration=0, redraw=True),
                      transition=dict(duration=0))]) for i, t in enumerate(parameters)])],
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
