r"""2011학년도 36번: 현수면의 가우스곡률을 시각화한다.

현수선 y=2 cosh(x/2)를 x축 둘레로 회전한 현수면은
X(u,v)=(u, 2 cosh(u/2) cos v, 2 cosh(u/2) sin v)이다.
회전면의 곡률 공식 K=-r''/[r(1+r'²)²]에
r=2 cosh(u/2)를 대입하면 K=-1/[4 cosh⁴(u/2)]이다.
따라서 모든 점에서 K<0, u=0에서 최솟값 -1/4이다.
평면의 K=0과 다르므로 가우스곡률을 보존하는 국소 등거리변환도 불가능하다.
보기 ㄴ만 참이므로 정답은 ②이다. 화면에는 -4≤u≤4의 일부를 표시한다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2011_q36_catenoid_curvature.py
    python .\supplement_exam\exam_2011_q36_catenoid_curvature.py --output output/exam_2011_q36.html --no-show
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def radius(u: np.ndarray | float) -> np.ndarray:
    """현수면의 회전 반지름 r(u)를 반환한다."""
    return 2 * np.cosh(np.asarray(u) / 2)


def surface(u: np.ndarray | float, v: np.ndarray | float) -> np.ndarray:
    """브로드캐스트 가능한 매개변수로부터 마지막 축에 공간 좌표를 반환한다."""
    u, v = np.broadcast_arrays(np.asarray(u), np.asarray(v))
    r = radius(u)
    return np.stack((u, r * np.cos(v), r * np.sin(v)), axis=-1)


def gaussian_curvature(u: np.ndarray | float) -> np.ndarray:
    """K(u)=-1/[4 cosh⁴(u/2)]를 반환한다. 회전각 v에는 무관하다."""
    return -1 / (4 * np.cosh(np.asarray(u) / 2)**4)


# 이 문항의 시각화 구성
def selected_traces(u: float) -> list:
    """선택한 평행원과 곡률 그래프의 대응점을 반환한다."""
    circle = surface(u, np.linspace(0, 2*np.pi, 121))
    k = float(gaussian_curvature(u))
    return [
        go.Scatter3d(
            x=circle[:, 0], y=circle[:, 1], z=circle[:, 2], mode="lines",
            line=dict(color="#E45756", width=8), name="선택한 단면 x=u",
            hovertemplate=f"u={u:.2f}<br>반지름={float(radius(u)):.3f}<br>K={k:.6f}<extra></extra>",
        ),
        go.Scatter(
            x=[u], y=[k], mode="markers", marker=dict(color="#E45756", size=13),
            showlegend=False, hovertemplate="u=%{x:.2f}<br>K=%{y:.6f}<extra></extra>",
        ),
    ]


def build_figure() -> go.Figure:
    """현수면과 K 그래프를 슬라이더로 연결한 그림을 만든다."""
    figure = make_subplots(
        rows=1, cols=2, specs=[[dict(type="scene"), dict(type="xy")]],
        column_widths=[.55, .45], horizontal_spacing=.12,
        subplot_titles=("현수면 · 색상은 가우스곡률 K", "K(u): 허리에서 −1/4, 양끝 방향으로 0에 접근"),
    )
    u, v = np.meshgrid(np.linspace(-4, 4, 101), np.linspace(0, 2*np.pi, 101))
    points = surface(u, v)
    figure.add_trace(go.Surface(
        x=points[..., 0], y=points[..., 1], z=points[..., 2],
        surfacecolor=gaussian_curvature(u), cmin=-.25, cmax=0,
        colorscale=[[0, "#54278F"], [.5, "#756BB1"], [1, "#DADAEB"]],
        colorbar=dict(title="K", x=.51, len=.65, thickness=12,
                      tickvals=[-.25, -.125, 0]),
        opacity=.8, name="현수면",
        customdata=gaussian_curvature(u),
        hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<br>K=%{customdata:.6f}<extra></extra>",
    ), row=1, col=1)
    values = np.linspace(-4, 4, 401)
    profile = surface(values, 0)
    figure.add_trace(go.Scatter3d(
        x=profile[:, 0], y=profile[:, 1], z=profile[:, 2], mode="lines",
        line=dict(color="#F2A541", width=6), name="측면곡선 y=2 cosh(x/2)",
    ), row=1, col=1)
    figure.add_trace(go.Scatter3d(
        x=[-4.5, 4.5], y=[0, 0], z=[0, 0], mode="lines",
        line=dict(color="#444444", width=3, dash="dash"), name="회전축 x",
    ), row=1, col=1)
    figure.add_trace(go.Scatter(
        x=values, y=gaussian_curvature(values), mode="lines",
        line=dict(color="#54278F", width=4), name="K(u)",
    ), row=1, col=2)
    figure.add_trace(go.Scatter(
        x=[-4, 4], y=[0, 0], mode="lines",
        line=dict(color="#888888", width=2, dash="dash"), name="평면의 K=0",
    ), row=1, col=2)
    circle, marker = selected_traces(0)
    figure.add_trace(circle, row=1, col=1)
    figure.add_trace(marker, row=1, col=2)
    parameters = np.linspace(-4, 4, 33)
    figure.frames = [go.Frame(name=str(i), data=selected_traces(float(value)), traces=[5, 6])
                     for i, value in enumerate(parameters)]
    figure.update_xaxes(title_text="u = x", range=[-4.3, 4.3], row=1, col=2)
    figure.update_yaxes(title_text="가우스곡률 K", range=[-.28, .025],
                        tickvals=[-.25, -.2, -.15, -.1, -.05, 0], row=1, col=2)
    figure.update_layout(
        title=dict(text="2011학년도 36번 · 현수면의 가우스곡률"
                   "<br><sup>K=−1/[4 cosh⁴(u/2)] · ㄱ 거짓 / ㄴ 참 / ㄷ 거짓 · 정답 ②</sup>", x=.5),
        template="plotly_white", height=820, margin=dict(l=35, r=30, t=120, b=185),
        scene=dict(aspectmode="data", xaxis_title="x", yaxis_title="y", zaxis_title="z",
                   uirevision="camera", camera=dict(eye=dict(x=1.5, y=1.6, z=1.1))),
        legend=dict(orientation="h", y=-.25),
        sliders=[dict(active=16, y=-.08, currentvalue=dict(prefix="선택한 위치 u = "), steps=[
            dict(label=f"{value:.2f}", method="animate", args=[[str(i)],
                 dict(mode="immediate", frame=dict(duration=0, redraw=True),
                      transition=dict(duration=0))]) for i, value in enumerate(parameters)])],
    )
    figure.add_annotation(
        text="등거리변환은 K를 보존한다. 현수면은 K<0, 평면은 K=0이므로 서로 등거리동형이 아니다.",
        xref="paper", yref="paper", x=.5, y=-.36, showarrow=False, font=dict(size=13),
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
