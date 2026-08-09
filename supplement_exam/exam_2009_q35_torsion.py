r"""2009학년도 중등교사 임용시험 35번: 비틀림의 변환을 시각화한다.

문제의 변환 ``beta(t) = 2 alpha(-2t)``에는 두 효과가 함께 들어 있다.

* ``-2t``는 같은 곡선을 반대 방향과 다른 속도로 매개화한다.
* 공간에서 곡선을 2배 확대하면 비틀림의 크기는 1/2배가 된다.

아래에서는 비틀림이 양수인 원나선
``alpha(theta) = (cos(theta), sin(theta), pitch * theta)``를 예로 들어
두 곡선과 t=0에서의 Frenet 표준틀을 나란히 그린다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2009_q35_torsion.py
    python .\supplement_exam\exam_2009_q35_torsion.py --output q35.html --no-show
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


FRAME_COLORS = {"T": "#E45756", "N": "#54A24B", "B": "#4C78A8"}


def alpha(theta: np.ndarray | float, pitch: float) -> np.ndarray:
    """원나선 alpha(theta)를 마지막 축의 길이가 3이 되도록 반환한다."""
    theta_array = np.asarray(theta)
    return np.stack(
        (np.cos(theta_array), np.sin(theta_array), pitch * theta_array), axis=-1
    )


def alpha_derivatives(theta: float, pitch: float) -> tuple[np.ndarray, ...]:
    """alpha의 1, 2, 3계 도함수를 반환한다."""
    first = np.array([-np.sin(theta), np.cos(theta), pitch])
    second = np.array([-np.cos(theta), -np.sin(theta), 0.0])
    third = np.array([np.sin(theta), -np.cos(theta), 0.0])
    return first, second, third


def beta_derivatives(t: float, pitch: float) -> tuple[np.ndarray, ...]:
    """beta(t)=2 alpha(-2t)의 1, 2, 3계 도함수를 반환한다."""
    first, second, third = alpha_derivatives(-2.0 * t, pitch)
    return -4.0 * first, 8.0 * second, -16.0 * third


def torsion(derivatives: tuple[np.ndarray, ...]) -> float:
    """tau=((r' x r'') . r''') / ||r' x r''||^2를 계산한다."""
    first, second, third = derivatives
    cross = np.cross(first, second)
    return float(np.dot(cross, third) / np.dot(cross, cross))


def frenet_frame(derivatives: tuple[np.ndarray, ...]) -> np.ndarray:
    """행이 각각 단위 접선 T, 주법선 N, 종법선 B인 배열을 반환한다."""
    first, second, _ = derivatives
    tangent = first / np.linalg.norm(first)
    binormal = np.cross(first, second)
    binormal /= np.linalg.norm(binormal)
    normal = np.cross(binormal, tangent)
    return np.stack((tangent, normal, binormal))


def add_frenet_frame(
    figure: go.Figure,
    point: np.ndarray,
    frame: np.ndarray,
    row: int,
    col: int,
    scale: float,
    show_legend: bool,
) -> None:
    """3차원 부분 그림에 Frenet 표준틀을 선과 끝점으로 추가한다."""
    for label, vector in zip(("T", "N", "B"), frame, strict=True):
        endpoint = point + scale * vector
        figure.add_trace(
            go.Scatter3d(
                x=[point[0], endpoint[0]],
                y=[point[1], endpoint[1]],
                z=[point[2], endpoint[2]],
                mode="lines+markers",
                line={"color": FRAME_COLORS[label], "width": 7},
                marker={"color": FRAME_COLORS[label], "size": [2, 5]},
                name=label,
                legendgroup=f"frame-{label}",
                showlegend=show_legend,
                hovertemplate=f"{label} 벡터<extra></extra>",
            ),
            row=row,
            col=col,
        )


def build_figure(pitch: float = 0.35) -> go.Figure:
    """35번의 비틀림 변환을 설명하는 대화형 Plotly 그림을 만든다."""
    if pitch <= 0:
        raise ValueError("문제의 조건 tau > 0을 나타내려면 pitch가 양수여야 합니다.")

    theta = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 500)
    t = np.linspace(-np.pi, np.pi, 500)
    alpha_points = alpha(theta, pitch)
    beta_points = 2.0 * alpha(-2.0 * t, pitch)

    tau_alpha = torsion(alpha_derivatives(0.0, pitch))
    tau_beta = torsion(beta_derivatives(0.0, pitch))

    figure = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "scene"}, {"type": "scene"}]],
        subplot_titles=(
            f"원곡선 α(θ) - τ(0) = {tau_alpha:.4f}",
            f"β(t) = 2α(-2t) - τβ(0) = {tau_beta:.4f}",
        ),
        horizontal_spacing=0.04,
    )

    for col, points, name, color in (
        (1, alpha_points, "α(θ)", "#7A5195"),
        (2, beta_points, "β(t)", "#EF5675"),
    ):
        figure.add_trace(
            go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                mode="lines",
                line={"color": color, "width": 8},
                name=name,
                hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<extra>"
                + name
                + "</extra>",
            ),
            row=1,
            col=col,
        )

    alpha_zero = alpha(0.0, pitch)
    beta_zero = 2.0 * alpha_zero
    add_frenet_frame(
        figure,
        alpha_zero,
        frenet_frame(alpha_derivatives(0.0, pitch)),
        row=1,
        col=1,
        scale=0.8,
        show_legend=True,
    )
    add_frenet_frame(
        figure,
        beta_zero,
        frenet_frame(beta_derivatives(0.0, pitch)),
        row=1,
        col=2,
        scale=1.6,
        show_legend=False,
    )

    common_scene = {
        "xaxis_title": "x",
        "yaxis_title": "y",
        "zaxis_title": "z",
        "aspectmode": "data",
        "camera": {"eye": {"x": 1.45, "y": 1.45, "z": 0.9}},
    }
    figure.update_layout(
        title={
            "text": (
                "2009학년도 중등교사 임용시험 35번 - 확대와 재매개화에 따른 비틀림"
                "<br><sup>τβ(0) / τα(0) = 1/2 (정답 ①)</sup>"
            ),
            "x": 0.5,
        },
        template="plotly_white",
        height=720,
        margin={"l": 20, "r": 20, "t": 105, "b": 125},
        legend={"orientation": "h", "x": 0.5, "xanchor": "center", "y": -0.02},
        scene=common_scene,
        scene2=common_scene,
        annotations=[
            {
                "text": (
                    "β'=-4α', β''=8α'', β'''=-16α'''이므로 "
                    "분자는 512배, 분모는 1024배가 되어 τβ=τα/2"
                ),
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": -0.16,
                "showarrow": False,
                "font": {"size": 14},
            }
        ],
    )
    return figure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pitch", type=float, default=0.35, help="예시 원나선의 양의 pitch (기본값: 0.35)"
    )
    parser.add_argument("--output", type=Path, help="대화형 HTML을 저장할 경로")
    parser.add_argument("--no-show", action="store_true", help="브라우저 창을 열지 않음")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figure = build_figure(args.pitch)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        figure.write_html(args.output, include_plotlyjs=True)
        print(f"저장 완료: {args.output.resolve()}")
    if not args.no_show:
        figure.show()


if __name__ == "__main__":
    main()
