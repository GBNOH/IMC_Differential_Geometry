r"""2009학년도 중등교사 임용시험 36번: K=0인 선직면을 시각화한다.

곡면
    x(u, v) = (u, v, u^3 + 2v)
            = (u, 0, u^3) + v(0, 1, 2)
은 일정한 방향 delta=(0, 1, 2)로 평행이동해 얻는 선직면이다.
제2기본형에서 M=N=0이므로 Gaussian 곡률 K=(LN-M^2)/(EG-F^2)는
모든 점에서 0이다.

오른쪽 패널은 곡면을 평면으로 전개한 좌표 (s, w)를 보여 준다. 이 좌표에서
직선 삼각형을 만든 뒤 왼쪽 곡면으로 되돌리면 세 변은 측지선이며, 내각의 합은
평면과 똑같이 pi이다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2009_q36_developable_surface.py
    python .\supplement_exam\exam_2009_q36_developable_surface.py --output q36.html --no-show
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


SQRT_FIVE = np.sqrt(5.0)


def surface(u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, ...]:
    """x(u,v)=(u,v,u^3+2v)의 x, y, z 성분을 반환한다."""
    return u, v, u**3 + 2.0 * v


def developed_coordinates(u: np.ndarray, v: np.ndarray, s: np.ndarray) -> tuple[np.ndarray, ...]:
    """곡면의 등거리 전개 좌표 (s,w)를 반환한다."""
    w = SQRT_FIVE * v + 2.0 * u**3 / SQRT_FIVE
    return s, w


def arc_coordinate_grid(u_min: float, u_max: float, count: int = 4001) -> tuple[np.ndarray, ...]:
    """ds/du=sqrt(1+9u^4/5)를 수치 적분한 단조 좌표표를 만든다."""
    u = np.linspace(u_min, u_max, count)
    speed = np.sqrt(1.0 + 9.0 * u**4 / 5.0)
    increments = 0.5 * (speed[:-1] + speed[1:]) * np.diff(u)
    s = np.concatenate(([0.0], np.cumsum(increments)))
    s -= np.interp(0.0, u, s)
    return u, s


def map_developed_to_surface(
    s_values: np.ndarray,
    w_values: np.ndarray,
    u_lookup: np.ndarray,
    s_lookup: np.ndarray,
) -> tuple[np.ndarray, ...]:
    """전개평면의 점 (s,w)를 원래 곡면의 점 (x,y,z)로 옮긴다."""
    u = np.interp(s_values, s_lookup, u_lookup)
    v = w_values / SQRT_FIVE - 2.0 * u**3 / 5.0
    return surface(u, v)


def triangle_angles(vertices: np.ndarray) -> np.ndarray:
    """2차원 삼각형의 세 내각을 라디안으로 반환한다."""
    angles = []
    for index in range(3):
        vertex = vertices[index]
        first = vertices[(index - 1) % 3] - vertex
        second = vertices[(index + 1) % 3] - vertex
        cosine = np.dot(first, second) / (np.linalg.norm(first) * np.linalg.norm(second))
        angles.append(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return np.asarray(angles)


def sampled_triangle_edges(vertices: np.ndarray, points_per_edge: int = 100) -> np.ndarray:
    """닫힌 삼각형의 각 변을 일정하게 표본화한다."""
    pieces = []
    for index in range(3):
        start = vertices[index]
        end = vertices[(index + 1) % 3]
        parameter = np.linspace(0.0, 1.0, points_per_edge, endpoint=False)[:, None]
        pieces.append((1.0 - parameter) * start + parameter * end)
    return np.vstack((*pieces, vertices[0][None, :]))


def build_figure() -> go.Figure:
    """36번의 선직면, rulings, 등거리 전개, 측지삼각형을 함께 그린다."""
    u_values = np.linspace(-2.0, 2.0, 151)
    v_values = np.linspace(-2.0, 2.0, 121)
    u_mesh, v_mesh = np.meshgrid(u_values, v_values, indexing="ij")
    x_mesh, y_mesh, z_mesh = surface(u_mesh, v_mesh)

    u_lookup, s_lookup = arc_coordinate_grid(-2.1, 2.1)
    triangle = np.array([[-1.45, -1.0], [1.35, -0.7], [0.15, 1.45]])
    closed_triangle = np.vstack((triangle, triangle[0]))
    edge_points = sampled_triangle_edges(triangle)
    geo_x, geo_y, geo_z = map_developed_to_surface(
        edge_points[:, 0], edge_points[:, 1], u_lookup, s_lookup
    )
    angles = triangle_angles(triangle)
    angle_sum = float(np.sum(angles))

    figure = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "scene"}, {"type": "xy"}]],
        column_widths=[0.66, 0.34],
        subplot_titles=(
            "선직면 x(u,v), 평행한 모선과 측지삼각형",
            "등거리 전개평면 (s,w)",
        ),
        horizontal_spacing=0.06,
    )

    figure.add_trace(
        go.Surface(
            x=x_mesh,
            y=y_mesh,
            z=z_mesh,
            surfacecolor=np.zeros_like(z_mesh),
            colorscale=[[0.0, "#B8DEDE"], [1.0, "#B8DEDE"]],
            cmin=-1.0,
            cmax=1.0,
            opacity=0.82,
            showscale=False,
            name="K=0인 곡면",
            hovertemplate="u=%{x:.2f}<br>v=%{y:.2f}<br>z=%{z:.2f}<br>K=0<extra></extra>",
        ),
        row=1,
        col=1,
    )

    for index, fixed_u in enumerate(np.linspace(-1.8, 1.8, 9)):
        ruling_v = np.linspace(-2.0, 2.0, 80)
        ruling_u = np.full_like(ruling_v, fixed_u)
        ruling_x, ruling_y, ruling_z = surface(ruling_u, ruling_v)
        figure.add_trace(
            go.Scatter3d(
                x=ruling_x,
                y=ruling_y,
                z=ruling_z,
                mode="lines",
                line={"color": "rgba(37,94,145,0.7)", "width": 3},
                name="모선: δ=(0,1,2)",
                legendgroup="rulings",
                showlegend=index == 0,
                hovertemplate=f"u={fixed_u:.2f}인 직선 모선<extra></extra>",
            ),
            row=1,
            col=1,
        )

    base_u = np.linspace(-2.0, 2.0, 300)
    base_v = np.zeros_like(base_u)
    base_x, base_y, base_z = surface(base_u, base_v)
    figure.add_trace(
        go.Scatter3d(
            x=base_x,
            y=base_y,
            z=base_z,
            mode="lines",
            line={"color": "#7A5195", "width": 8},
            name="C: y=0, z=x³",
            hovertemplate="기저곡선 C<br>x=%{x:.2f}<br>z=%{z:.2f}<extra></extra>",
        ),
        row=1,
        col=1,
    )

    directrix_v = np.linspace(-2.0, 2.0, 100)
    directrix_u = np.zeros_like(directrix_v)
    line_x, line_y, line_z = surface(directrix_u, directrix_v)
    figure.add_trace(
        go.Scatter3d(
            x=line_x,
            y=line_y,
            z=line_z,
            mode="lines",
            line={"color": "#F58518", "width": 8},
            name="l₀: x=0, z=2y",
            hovertemplate="직선 l₀<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
        ),
        row=1,
        col=1,
    )

    figure.add_trace(
        go.Scatter3d(
            x=geo_x,
            y=geo_y,
            z=geo_z,
            mode="lines",
            line={"color": "#E45756", "width": 10},
            name="측지삼각형",
            hovertemplate="측지삼각형의 변<extra></extra>",
        ),
        row=1,
        col=1,
    )

    angle_labels = [f"{np.degrees(value):.1f}°" for value in angles]
    figure.add_trace(
        go.Scatter(
            x=closed_triangle[:, 0],
            y=closed_triangle[:, 1],
            mode="lines+markers",
            fill="toself",
            fillcolor="rgba(228,87,86,0.18)",
            line={"color": "#E45756", "width": 4},
            marker={"size": 9, "color": "#E45756"},
            name="전개된 측지삼각형",
            showlegend=False,
            customdata=angle_labels + [angle_labels[0]],
            hovertemplate="s=%{x:.2f}<br>w=%{y:.2f}<br>내각=%{customdata}<extra></extra>",
        ),
        row=1,
        col=2,
    )

    figure.update_xaxes(title_text="s (곡선에 수직인 호길이 좌표)", row=1, col=2)
    figure.update_yaxes(
        title_text="w (모선 방향 거리)",
        scaleanchor="x",
        scaleratio=1,
        row=1,
        col=2,
    )
    figure.update_layout(
        title={
            "text": (
                "2009학년도 중등교사 임용시험 36번 - K=0인 전개가능 선직면"
                f"<br><sup>측지삼각형의 내각합 = {angle_sum:.6f} rad = "
                f"{np.degrees(angle_sum):.1f}° = π (정답 ⑤)</sup>"
            ),
            "x": 0.5,
        },
        template="plotly_white",
        height=760,
        margin={"l": 30, "r": 30, "t": 110, "b": 125},
        legend={"orientation": "h", "x": 0.5, "xanchor": "center", "y": -0.03},
        scene={
            "xaxis_title": "x=u",
            "yaxis_title": "y=v",
            "zaxis_title": "z=u³+2v",
            "aspectmode": "data",
            "camera": {"eye": {"x": 1.4, "y": 1.65, "z": 0.85}},
        },
        annotations=[
            {
                "text": "M=N=0 ⇒ K=(LN-M²)/(EG-F²)=0",
                "xref": "paper",
                "yref": "paper",
                "x": 0.27,
                "y": -0.16,
                "showarrow": False,
                "font": {"size": 14},
            },
            {
                "text": " + ".join(angle_labels) + " = 180.0°",
                "xref": "x",
                "yref": "y",
                "x": 0.0,
                "y": -1.55,
                "showarrow": False,
                "font": {"size": 14, "color": "#B03A48"},
            },
        ],
    )
    return figure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="대화형 HTML을 저장할 경로")
    parser.add_argument("--no-show", action="store_true", help="브라우저 창을 열지 않음")
    return parser.parse_args()


def main() -> None:
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
