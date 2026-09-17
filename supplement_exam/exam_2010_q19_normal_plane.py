r"""2010학년도 19번: 두 곡면의 교선과 q에서의 법평면.

S1: x²-y²=1, x>0; S2: z=xy.
gamma(t)=(sqrt(1+t²), t, t sqrt(1+t²)), gamma'(0)=(0,1,1).
q=(1,0,0)을 지나고 접선에 수직인 평면은 y+z=0, 정답은 ⑤.
필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2010_q19_normal_plane.py
HTML 저장: 위 명령에 --output output/exam_2010_q19.html --no-show 추가.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import plotly.graph_objects as go


# 수학적 정의와 계산
def gamma(t: np.ndarray | float) -> np.ndarray:
    """교선의 좌표를 마지막 축에 반환한다."""
    t = np.asarray(t)
    x = np.sqrt(1 + t**2)
    return np.stack((x, t, t * x), axis=-1)


def gamma_derivative(t: np.ndarray | float) -> np.ndarray:
    """교선의 접벡터 gamma'(t)를 반환한다."""
    t = np.asarray(t)
    x = np.sqrt(1 + t**2)
    return np.stack((t / x, np.ones_like(t), (1 + 2 * t**2) / x), axis=-1)


def normal_plane_residual(points: np.ndarray, t: float = 0.0) -> np.ndarray:
    """(p-gamma(t))·gamma'(t)를 계산한다. 0이면 법평면 위의 점이다."""
    return (np.asarray(points) - gamma(t)) @ gamma_derivative(t)


# 이 문항의 시각화 구성
def build_figure() -> go.Figure:
    """회전·확대 및 곡면 표시 전환이 가능한 그림을 만든다."""
    fig = go.Figure()

    def surface(x: np.ndarray, y: np.ndarray, z: np.ndarray, name: str, color: str) -> None:
        """현재 그림에 반투명 곡면을 추가한다."""
        fig.add_trace(go.Surface(
            x=x, y=y, z=z, name=name, opacity=0.3,
            colorscale=[[0, color], [1, color]], showscale=False,
            showlegend=True,
            hovertemplate=name + "<br>(%{x:.2f}, %{y:.2f}, %{z:.2f})<extra></extra>",
        ))

    y, z = np.meshgrid(np.linspace(-1.4, 1.4, 55), np.linspace(-2.5, 2.5, 55))
    surface(np.sqrt(1 + y**2), y, z, "S₁: x²−y²=1, x>0", "#4C78A8")
    x, y = np.meshgrid(np.linspace(-1.5, 2, 55), np.linspace(-1.3, 1.3, 55))
    surface(x, y, x * y, "S₂: z=xy", "#F2A541")
    x, y = np.meshgrid(np.linspace(-1.5, 2, 30), np.linspace(-1.5, 1.5, 30))
    surface(x, y, -y, "법평면: y+z=0", "#54A24B")

    def line(points: np.ndarray, name: str, color: str, dash: str = "solid") -> None:
        """현재 그림에 공간곡선 또는 선분을 추가한다."""
        fig.add_trace(go.Scatter3d(
            x=points[:, 0], y=points[:, 1], z=points[:, 2],
            mode="lines", name=name, line=dict(color=color, width=7, dash=dash),
        ))

    line(gamma(np.linspace(-1.4, 1.4, 401)), "교선 γ", "#7040A0")
    q = gamma(0.0)
    tangent = gamma_derivative(0.0)
    line(q + np.array([-1.5, 1.5])[:, None] * tangent,
         "접선: q+s(0,1,1)", "#E45756", "dash")
    fig.add_trace(go.Scatter3d(
        x=[1], y=[0], z=[0], mode="markers+text", text=["q=(1,0,0)"],
        textposition="top center", marker=dict(size=6, color="#222222"), name="점 q",
    ))
    choices = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 1], [1, -1, -1], [-1, 1, -1]])
    residuals = normal_plane_residual(choices)
    fig.add_trace(go.Scatter3d(
        x=choices[:, 0], y=choices[:, 1], z=choices[:, 2],
        mode="markers+text", text=["①", "②", "③", "④", "⑤ 정답"],
        textposition="top center", name="보기 (초록: 평면 위)",
        marker=dict(size=6, color=["#54A24B" if np.isclose(r, 0) else "#777777" for r in residuals]),
        customdata=residuals,
        hovertemplate="(%{x}, %{y}, %{z})<br>y+z=%{customdata}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="2010학년도 19번 · 교선의 접선과 법평면"
                   "<br><sup>γ′(0)=(0,1,1) ⇒ 법평면 y+z=0 · 정답 ⑤</sup>", x=0.5),
        template="plotly_white", height=800,
        margin=dict(l=20, r=20, t=130, b=100),
        scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z",
                   aspectmode="data", dragmode="orbit",
                   camera=dict(eye=dict(x=1.7, y=1.5, z=1.0))),
        legend=dict(orientation="h", y=-0.08),
        updatemenus=[dict(type="buttons", direction="right", x=0, y=1.09,
                         buttons=[
                             dict(label="전체 보기", method="update", args=[dict(visible=[True]*len(fig.data))]),
                             dict(label="접선·법평면 보기", method="update",
                                  args=[dict(visible=[i >= 2 for i in range(len(fig.data))])]),
                         ])],
    )
    return fig


# 실행 옵션과 HTML 저장
def parse_args() -> argparse.Namespace:
    """HTML 저장과 화면 표시 옵션을 읽는다."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="대화형 HTML 저장 경로")
    parser.add_argument("--no-show", action="store_true", help="브라우저를 열지 않음")
    return parser.parse_args()


def main() -> None:
    """그림을 생성하고 요청한 경우 HTML 저장 또는 화면 표시를 실행한다."""
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
