"""
plot_tools_diffgeo.py

2D 시각화: Plotly
3D 시각화: PyVista

수학적 데이터의 위치와 벡터 크기는 임의로 확대하거나 축소하지 않는다.
시각적 조정은 선 굵기, 화살촉 크기, 라벨 위치 등의 표시 속성으로만 한다.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pyvista as pv


# =============================================================================
# 공통 보조 함수
# =============================================================================

def _as_point_2d(point, name="point"):
    point = np.asarray(point, dtype=float)

    if point.shape != (2,):
        raise ValueError(f"{name}는 길이가 2인 배열이어야 합니다.")

    return point


def _as_point_3d(point, name="point"):
    point = np.asarray(point, dtype=float)

    if point.shape != (3,):
        raise ValueError(f"{name}는 길이가 3인 배열이어야 합니다.")

    return point


def _as_points_2d(points):
    points = np.asarray(points, dtype=float)

    if points.shape == (2,):
        points = points.reshape(1, 2)

    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points는 [x, y] 또는 (n, 2) 형태여야 합니다.")

    return points


def _as_points_3d(points):
    points = np.asarray(points, dtype=float)

    if points.shape == (3,):
        points = points.reshape(1, 3)

    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points는 [x, y, z] 또는 (n, 3) 형태여야 합니다.")

    return points


def _unit_vector_3d(vector):
    vector = _as_point_3d(vector, "vector")
    norm = np.linalg.norm(vector)

    if np.isclose(norm, 0.0):
        raise ValueError("영벡터의 방향은 정의할 수 없습니다.")

    return vector / norm


def _orthonormal_basis_perpendicular_to(axis):
    axis = _unit_vector_3d(axis)

    coordinate_axes = np.eye(3)
    reference = coordinate_axes[np.argmin(np.abs(axis))]

    e1 = np.cross(axis, reference)
    e1 = e1 / np.linalg.norm(e1)

    e2 = np.cross(axis, e1)
    e2 = e2 / np.linalg.norm(e2)

    return e1, e2



def _validate_subplot_args(row=None, col=None):
    if (row is None) != (col is None):
        raise ValueError("row와 col은 둘 다 지정하거나 둘 다 생략해야 합니다.")


def _get_subplot_refs_2d(fig, row=None, col=None):
    _validate_subplot_args(row, col)

    if row is None:
        return "x", "y"

    subplot = fig.get_subplot(row, col)

    if subplot is None:
        raise ValueError(f"({row}, {col}) 위치에 subplot이 없습니다.")

    xref = subplot.xaxis.plotly_name.replace("axis", "")
    yref = subplot.yaxis.plotly_name.replace("axis", "")

    return xref, yref


def _add_trace_2d(fig, trace, row=None, col=None):
    _validate_subplot_args(row, col)

    if row is None:
        fig.add_trace(trace)
    else:
        fig.add_trace(trace, row=row, col=col)


def _select_subplot_3d(fig, row=None, col=None):
    _validate_subplot_args(row, col)

    if row is not None:
        fig.subplot(row, col)


# =============================================================================
# 2D : Plotly
# =============================================================================

def create_figure_2d(
    title=None,
    *,
    x_title="x",
    y_title="y",
    equal_scale=True,
    show_grid=False,
    shape=None,
    subplot_titles=None,
    horizontal_spacing=None,
    vertical_spacing=None,
):
    if shape is None:
        fig = go.Figure()
        subplot_positions = [(None, None)]
    else:
        if len(shape) != 2:
            raise ValueError("shape은 (rows, cols) 형태여야 합니다.")

        rows, cols = map(int, shape)

        if rows <= 0 or cols <= 0:
            raise ValueError("shape의 rows와 cols는 양수여야 합니다.")

        subplot_kwargs = dict(
            rows=rows,
            cols=cols,
            subplot_titles=subplot_titles,
        )

        if horizontal_spacing is not None:
            subplot_kwargs["horizontal_spacing"] = horizontal_spacing

        if vertical_spacing is not None:
            subplot_kwargs["vertical_spacing"] = vertical_spacing

        fig = make_subplots(**subplot_kwargs)
        subplot_positions = [
            (row, col)
            for row in range(1, rows + 1)
            for col in range(1, cols + 1)
        ]

    fig.update_layout(
        title=title,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    for row, col in subplot_positions:
        if row is None:
            fig.update_xaxes(
                title=x_title,
                showgrid=show_grid,
                zeroline=False,
            )
            fig.update_yaxes(
                title=y_title,
                showgrid=show_grid,
                zeroline=False,
            )

            if equal_scale:
                fig.update_yaxes(scaleanchor="x", scaleratio=1)
        else:
            fig.update_xaxes(
                title=x_title,
                showgrid=show_grid,
                zeroline=False,
                row=row,
                col=col,
            )
            fig.update_yaxes(
                title=y_title,
                showgrid=show_grid,
                zeroline=False,
                row=row,
                col=col,
            )

            if equal_scale:
                xref, _ = _get_subplot_refs_2d(fig, row, col)
                fig.update_yaxes(
                    scaleanchor=xref,
                    scaleratio=1,
                    row=row,
                    col=col,
                )

    return fig



def add_coordinate_axes_2d(
    fig,
    x_range,
    y_range,
    *,
    axis_color="black",
    width=2,
    show_labels=True,
    x_label="x",
    y_label="y",
    row=None,
    col=None,
):
    xmin, xmax = map(float, x_range)
    ymin, ymax = map(float, y_range)

    if not xmin < xmax:
        raise ValueError("x_range는 (최솟값, 최댓값) 순서여야 합니다.")

    if not ymin < ymax:
        raise ValueError("y_range는 (최솟값, 최댓값) 순서여야 합니다.")

    xref, yref = _get_subplot_refs_2d(fig, row, col)

    fig.add_shape(
        type="line",
        x0=xmin,
        y0=0,
        x1=xmax,
        y1=0,
        xref=xref,
        yref=yref,
        line=dict(color=axis_color, width=width),
    )

    fig.add_shape(
        type="line",
        x0=0,
        y0=ymin,
        x1=0,
        y1=ymax,
        xref=xref,
        yref=yref,
        line=dict(color=axis_color, width=width),
    )

    fig.add_annotation(
        x=xmax,
        y=0,
        ax=xmax - 0.04 * (xmax - xmin),
        ay=0,
        xref=xref,
        yref=yref,
        axref=xref,
        ayref=yref,
        text="",
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=width,
        arrowcolor=axis_color,
    )

    fig.add_annotation(
        x=0,
        y=ymax,
        ax=0,
        ay=ymax - 0.04 * (ymax - ymin),
        xref=xref,
        yref=yref,
        axref=xref,
        ayref=yref,
        text="",
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=width,
        arrowcolor=axis_color,
    )

    if show_labels:
        fig.add_annotation(
            x=xmax,
            y=0,
            xref=xref,
            yref=yref,
            text=x_label,
            showarrow=False,
            xshift=12,
            yshift=-10,
            font=dict(color=axis_color),
        )

        fig.add_annotation(
            x=0,
            y=ymax,
            xref=xref,
            yref=yref,
            text=y_label,
            showarrow=False,
            xshift=10,
            yshift=12,
            font=dict(color=axis_color),
        )

    if row is None:
        fig.update_xaxes(range=[xmin, xmax])
        fig.update_yaxes(range=[ymin, ymax])
    else:
        fig.update_xaxes(range=[xmin, xmax], row=row, col=col)
        fig.update_yaxes(range=[ymin, ymax], row=row, col=col)

    return fig



def add_points_2d(
    fig,
    points,
    *,
    name=None,
    color="black",
    size=6,
    symbol="circle",
    opacity=0.6,
    row=None,
    col=None,
):
    points = _as_points_2d(points)

    if size <= 0:
        raise ValueError("size는 0보다 커야 합니다.")

    if not 0 <= opacity <= 1:
        raise ValueError("opacity는 0 이상 1 이하여야 합니다.")

    trace = go.Scatter(
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
        showlegend=(name is not None),
    )

    _add_trace_2d(fig, trace, row, col)

    return fig



def add_labels_2d(
    fig,
    points,
    labels,
    *,
    color="black",
    font_size=14,
    xshift=0,
    yshift=0,
    row=None,
    col=None,
):
    points = _as_points_2d(points)
    labels = list(labels)

    if len(labels) != len(points):
        raise ValueError("labels의 개수는 points의 개수와 같아야 합니다.")

    xref, yref = _get_subplot_refs_2d(fig, row, col)

    for point, label in zip(points, labels):
        fig.add_annotation(
            x=point[0],
            y=point[1],
            xref=xref,
            yref=yref,
            text=str(label),
            showarrow=False,
            xshift=xshift,
            yshift=yshift,
            font=dict(
                color=color,
                size=font_size,
            ),
        )

    return fig



def add_curve_2d(
    fig,
    points,
    *,
    name=None,
    color="deepskyblue",
    width=4,
    dash="solid",
    opacity=0.8,
    closed=False,
    row=None,
    col=None,
):
    points = _as_points_2d(points)

    if closed and not np.allclose(points[0], points[-1]):
        points = np.vstack([points, points[0]])

    trace = go.Scatter(
        x=points[:, 0],
        y=points[:, 1],
        mode="lines",
        name=name,
        opacity=opacity,
        line=dict(
            color=color,
            width=width,
            dash=dash,
        ),
        showlegend=(name is not None),
    )

    _add_trace_2d(fig, trace, row, col)

    return fig



def add_segment_2d(
    fig,
    point1,
    point2,
    *,
    color="black",
    width=2,
    dash="solid",
    row=None,
    col=None,
):
    point1 = _as_point_2d(point1, "point1")
    point2 = _as_point_2d(point2, "point2")

    return add_curve_2d(
        fig,
        np.array([point1, point2]),
        color=color,
        width=width,
        dash=dash,
        row=row,
        col=col,
    )


def add_arc_2d(
    fig,
    point1,
    point2,
    *,
    height=None,
    height_ratio=0.15,
    label=None,
    label_position=0.5,
    color="black",
    width=2,
    dash="solid",
    opacity=0.8,
    resolution=100,
    font_size=14,
    row=None,
    col=None,
):
    """
    두 점을 현으로 하는 원호를 그린다.

    height는 현의 중점에서 원호의 중점까지의 부호 있는 거리이다.
    양수이면 point1 -> point2 방향의 왼쪽, 음수이면 오른쪽으로 휜다.
    """
    point1 = _as_point_2d(point1, "point1")
    point2 = _as_point_2d(point2, "point2")

    chord = point2 - point1
    chord_length = np.linalg.norm(chord)

    if np.isclose(chord_length, 0.0):
        raise ValueError("point1과 point2는 서로 달라야 합니다.")

    if resolution < 2:
        raise ValueError("resolution은 2 이상이어야 합니다.")

    if not 0 <= label_position <= 1:
        raise ValueError("label_position은 0 이상 1 이하여야 합니다.")

    tangent = chord / chord_length
    normal = np.array([-tangent[1], tangent[0]])

    if height is None:
        h = height_ratio * chord_length
    else:
        h = float(height)

    if np.isclose(h, 0.0):
        raise ValueError("height는 0이 아니어야 합니다.")

    midpoint = (point1 + point2) / 2

    center_offset = h / 2 - chord_length**2 / (8 * h)
    center = midpoint + center_offset * normal
    radius = np.linalg.norm(point1 - center)

    bulge_point = midpoint + h * normal

    def angle_of(point):
        relative = point - center
        return np.arctan2(
            np.dot(relative, normal),
            np.dot(relative, tangent),
        )

    theta1 = angle_of(point1)
    theta2 = angle_of(point2)
    theta_mid = angle_of(bulge_point)

    ccw_delta = (theta2 - theta1) % (2 * np.pi)
    ccw_mid = (theta_mid - theta1) % (2 * np.pi)

    if ccw_mid <= ccw_delta:
        delta = ccw_delta
    else:
        delta = ccw_delta - 2 * np.pi

    theta = np.linspace(theta1, theta1 + delta, resolution)

    arc_points = (
        center
        + radius * np.cos(theta)[:, None] * tangent
        + radius * np.sin(theta)[:, None] * normal
    )

    add_curve_2d(
        fig,
        arc_points,
        color=color,
        width=width,
        dash=dash,
        opacity=opacity,
        row=row,
        col=col,
    )

    if label is not None:
        label_theta = theta1 + label_position * delta
        label_point = (
            center
            + radius * np.cos(label_theta) * tangent
            + radius * np.sin(label_theta) * normal
        )

        add_labels_2d(
            fig,
            [label_point],
            [label],
            color=color,
            font_size=font_size,
            row=row,
            col=col,
        )

    return fig


def add_vector_2d(
    fig,
    origin,
    vector,
    *,
    name=None,
    color="black",
    width=3,
    show_magnitude=False,
    font_size=14,
    label_position=0.5,
    row=None,
    col=None,
):
    origin = _as_point_2d(origin, "origin")
    vector = _as_point_2d(vector, "vector")

    vector_length = np.linalg.norm(vector)

    if np.isclose(vector_length, 0.0):
        raise ValueError("영벡터는 화살표로 나타낼 수 없습니다.")

    if not 0 <= label_position <= 1:
        raise ValueError("label_position은 0 이상 1 이하여야 합니다.")

    xref, yref = _get_subplot_refs_2d(fig, row, col)
    end = origin + vector

    fig.add_annotation(
        x=end[0],
        y=end[1],
        ax=origin[0],
        ay=origin[1],
        xref=xref,
        yref=yref,
        axref=xref,
        ayref=yref,
        text="",
        showarrow=True,
        arrowhead=3,
        arrowwidth=width,
        arrowcolor=color,
    )

    label_parts = []

    if name is not None:
        label_parts.append(str(name))

    if show_magnitude:
        label_parts.append(f"{vector_length:g}")

    if label_parts:
        label_point = origin + label_position * vector

        fig.add_annotation(
            x=label_point[0],
            y=label_point[1],
            xref=xref,
            yref=yref,
            text="   ".join(label_parts),
            showarrow=False,
            font=dict(
                color=color,
                size=font_size,
            ),
            yshift=10,
        )

    trace = go.Scatter(
        x=[origin[0], end[0]],
        y=[origin[1], end[1]],
        mode="markers",
        marker=dict(size=1, opacity=0),
        showlegend=False,
        hoverinfo="skip",
    )
    _add_trace_2d(fig, trace, row, col)

    return fig



def add_angle_2d(
    fig,
    origin,
    vector1,
    vector2,
    *,
    radius=None,
    radius_ratio=0.20,
    label=None,
    show_degree=False,
    decimals=1,
    color="black",
    width=2,
    font_size=14,
    label_scale=1.3,
    show_right_angle=True,
    right_angle_tol=1e-8,
    resolution=100,
    row=None,
    col=None,
):
    origin = _as_point_2d(origin, "origin")
    vector1 = _as_point_2d(vector1, "vector1")
    vector2 = _as_point_2d(vector2, "vector2")

    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    if np.isclose(norm1, 0.0) or np.isclose(norm2, 0.0):
        raise ValueError("각을 이루는 벡터는 영벡터일 수 없습니다.")

    e1 = vector1 / norm1
    e2 = vector2 / norm2

    dot = np.clip(np.dot(e1, e2), -1.0, 1.0)
    cross = e1[0] * e2[1] - e1[1] * e2[0]

    signed_angle = np.arctan2(cross, dot)
    theta = abs(signed_angle)

    if np.isclose(theta, 0.0):
        raise ValueError("두 벡터의 방향이 같아 각 표시를 만들 수 없습니다.")

    if np.isclose(theta, np.pi):
        raise ValueError("180도 각 표시는 현재 지원하지 않습니다.")

    if radius is None:
        r = radius_ratio * min(norm1, norm2)
    else:
        r = float(radius)

    if r <= 0:
        raise ValueError("radius는 양수여야 합니다.")

    if show_right_angle and np.isclose(dot, 0.0, atol=right_angle_tol):
        p1 = origin + r * e1
        p2 = origin + r * (e1 + e2)
        p3 = origin + r * e2

        add_curve_2d(
            fig,
            np.array([p1, p2, p3]),
            color=color,
            width=width,
            row=row,
            col=col,
        )

        label_direction = e1 + e2
        label_direction /= np.linalg.norm(label_direction)

    else:
        normal = np.array([-e1[1], e1[0]])
        t = np.linspace(0.0, signed_angle, resolution)

        arc = (
            origin
            + r * np.cos(t)[:, None] * e1
            + r * np.sin(t)[:, None] * normal
        )

        add_curve_2d(
            fig,
            arc,
            color=color,
            width=width,
            row=row,
            col=col,
        )

        middle_angle = signed_angle / 2

        label_direction = (
            np.cos(middle_angle) * e1
            + np.sin(middle_angle) * normal
        )

    text = None
    degree = np.degrees(theta)

    if label is not None and show_degree:
        text = f"{label} = {degree:.{decimals}f}°"
    elif label is not None:
        text = str(label)
    elif show_degree:
        text = f"{degree:.{decimals}f}°"

    if text is not None:
        label_point = origin + label_scale * r * label_direction
        xref, yref = _get_subplot_refs_2d(fig, row, col)

        fig.add_annotation(
            x=label_point[0],
            y=label_point[1],
            xref=xref,
            yref=yref,
            text=text,
            showarrow=False,
            font=dict(
                color=color,
                size=font_size,
            ),
        )

    return theta



def add_parametric_curve_2d(
    fig,
    curve,
    t_min,
    t_max,
    *,
    resolution=400,
    name=None,
    color="deepskyblue",
    width=4,
    dash="solid",
    closed=False,
    row=None,
    col=None,
):
    if resolution < 2:
        raise ValueError("resolution은 2 이상이어야 합니다.")

    t_values = np.linspace(float(t_min), float(t_max), resolution)
    points = np.array([curve(t) for t in t_values], dtype=float)

    return add_curve_2d(
        fig,
        points,
        name=name,
        color=color,
        width=width,
        dash=dash,
        closed=closed,
        row=row,
        col=col,
    )



def add_polar_curve_2d(
    fig,
    radius_function,
    theta_min,
    theta_max,
    *,
    resolution=600,
    name=None,
    color="deepskyblue",
    width=4,
    dash="solid",
    closed=False,
    row=None,
    col=None,
):
    if resolution < 2:
        raise ValueError("resolution은 2 이상이어야 합니다.")

    theta = np.linspace(float(theta_min), float(theta_max), resolution)
    radius = np.array([radius_function(value) for value in theta], dtype=float)

    points = np.column_stack(
        (
            radius * np.cos(theta),
            radius * np.sin(theta),
        )
    )

    return add_curve_2d(
        fig,
        points,
        name=name,
        color=color,
        width=width,
        dash=dash,
        closed=closed,
        row=row,
        col=col,
    )



def add_filled_region_2d(
    fig,
    boundary_points,
    *,
    fill_color="lightcyan",
    line_color="black",
    line_width=2,
    opacity=0.6,
    name=None,
    row=None,
    col=None,
):
    boundary_points = _as_points_2d(boundary_points)

    if not np.allclose(boundary_points[0], boundary_points[-1]):
        boundary_points = np.vstack(
            [boundary_points, boundary_points[0]]
        )

    trace = go.Scatter(
        x=boundary_points[:, 0],
        y=boundary_points[:, 1],
        mode="lines",
        fill="toself",
        fillcolor=fill_color,
        opacity=opacity,
        line=dict(
            color=line_color,
            width=line_width,
        ),
        name=name,
        showlegend=(name is not None),
    )

    _add_trace_2d(fig, trace, row, col)

    return fig



# =============================================================================
# 3D : PyVista
# =============================================================================

def create_figure_3d(
    *,
    window_size=(900, 700),
    background="white",
    shape=None,
):
    if shape is None:
        fig = pv.Plotter(window_size=window_size)
    else:
        fig = pv.Plotter(shape=shape, window_size=window_size)

    fig.set_background(background)

    return fig



def add_points_3d(
    fig,
    points,
    *,
    color="black",
    point_size=10,
    opacity=0.6,
    render_points_as_spheres=True,
    row=None,
    col=None,
):
    _select_subplot_3d(fig, row, col)
    points = _as_points_3d(points)

    if point_size <= 0:
        raise ValueError("point_size는 0보다 커야 합니다.")

    if not 0 <= opacity <= 1:
        raise ValueError("opacity는 0 이상 1 이하여야 합니다.")

    fig.add_points(
        points,
        color=color,
        point_size=point_size,
        opacity=opacity,
        render_points_as_spheres=render_points_as_spheres,
    )

    return fig



def add_labels_3d(
    fig,
    points,
    labels,
    *,
    color="black",
    font_size=16,
    always_visible=True,
    row=None,
    col=None,
):
    _select_subplot_3d(fig, row, col)
    points = _as_points_3d(points)
    labels = list(labels)

    if len(labels) != len(points):
        raise ValueError("labels의 개수는 points의 개수와 같아야 합니다.")

    fig.add_point_labels(
        points,
        [str(label) for label in labels],
        show_points=False,
        shape=None,
        text_color=color,
        font_size=font_size,
        always_visible=always_visible,
    )

    return fig



def add_curve_3d(
    fig,
    points,
    *,
    color="deepskyblue",
    line_width=4,
    opacity=0.8,
    closed=False,
    row=None,
    col=None,
):
    _select_subplot_3d(fig, row, col)
    points = _as_points_3d(points)

    if len(points) < 2:
        raise ValueError("곡선을 그리려면 최소 두 점이 필요합니다.")

    curve = pv.lines_from_points(
        points,
        close=closed,
    )

    fig.add_mesh(
        curve,
        color=color,
        line_width=line_width,
        opacity=opacity,
    )

    return fig



def add_segment_3d(
    fig,
    point1,
    point2,
    *,
    color="black",
    line_width=3,
    opacity=0.8,
    row=None,
    col=None,
):
    point1 = _as_point_3d(point1, "point1")
    point2 = _as_point_3d(point2, "point2")

    return add_curve_3d(
        fig,
        np.array([point1, point2]),
        color=color,
        line_width=line_width,
        opacity=opacity,
        row=row,
        col=col,
    )



def add_vector_3d(
    fig,
    origin,
    vector,
    *,
    name=None,
    color="black",
    text_color=None,
    show_magnitude=False,
    show_endpoint=False,
    opacity=0.8,
    shaft_radius=0.02,
    tip_radius=0.06,
    tip_length=0.20,
    font_size=18,
    label_position=0.5,
    row=None,
    col=None,
):
    _select_subplot_3d(fig, row, col)
    origin = _as_point_3d(origin, "origin")
    vector = _as_point_3d(vector, "vector")

    vector_length = np.linalg.norm(vector)

    if np.isclose(vector_length, 0.0):
        raise ValueError("영벡터는 화살표로 나타낼 수 없습니다.")

    if shaft_radius <= 0:
        raise ValueError("shaft_radius는 0보다 커야 합니다.")

    if tip_radius <= 0:
        raise ValueError("tip_radius는 0보다 커야 합니다.")

    if not 0 < tip_length < 1:
        raise ValueError("tip_length는 0과 1 사이여야 합니다.")

    if not 0 <= label_position <= 1:
        raise ValueError("label_position은 0 이상 1 이하여야 합니다.")

    arrow = pv.Arrow(
        start=origin,
        direction=vector,
        shaft_radius=shaft_radius / vector_length,
        tip_radius=tip_radius / vector_length,
        tip_length=tip_length / vector_length,
        scale="auto",
    )

    fig.add_mesh(
        arrow,
        color=color,
        smooth_shading=True,
        opacity=opacity,
    )

    if text_color is None:
        text_color = color

    label_parts = []

    if name is not None:
        label_parts.append(str(name))

    if show_magnitude:
        label_parts.append(f"{vector_length:g}")

    if label_parts:
        label_point = origin + label_position * vector

        fig.add_point_labels(
            [label_point],
            ["   ".join(label_parts)],
            show_points=False,
            shape=None,
            text_color=text_color,
            font_size=font_size,
            always_visible=True,
        )

    if show_endpoint:
        end = origin + vector
        endpoint_text = f"({end[0]:g}, {end[1]:g}, {end[2]:g})"

        fig.add_point_labels(
            [end],
            [endpoint_text],
            show_points=False,
            shape=None,
            text_color=text_color,
            font_size=font_size,
            always_visible=True,
        )

    return fig



def add_coordinate_axes_3d(
    fig,
    *,
    axis_length=1.0,
    axis_color="black",
    line_width=3,
    show_labels=True,
    font_size=16,
    positive_only=False,
    opacity=0.8,
    row=None,
    col=None,
):
    _select_subplot_3d(fig, row, col)
    L = float(axis_length)

    if L <= 0:
        raise ValueError("axis_length는 양수여야 합니다.")

    origin = np.zeros(3)

    if not positive_only:
        add_segment_3d(
            fig,
            np.array([-L, 0.0, 0.0]),
            origin,
            color=axis_color,
            line_width=line_width,
            opacity=opacity,
        )
        add_segment_3d(
            fig,
            np.array([0.0, -L, 0.0]),
            origin,
            color=axis_color,
            line_width=line_width,
            opacity=opacity,
        )
        add_segment_3d(
            fig,
            np.array([0.0, 0.0, -L]),
            origin,
            color=axis_color,
            line_width=line_width,
            opacity=opacity,
        )

    add_vector_3d(
        fig,
        origin,
        np.array([L, 0.0, 0.0]),
        color=axis_color,
        opacity=opacity,
        shaft_radius=0.01,
        tip_radius=0.04,
        tip_length=0.12,
    )
    add_vector_3d(
        fig,
        origin,
        np.array([0.0, L, 0.0]),
        color=axis_color,
        opacity=opacity,
        shaft_radius=0.01,
        tip_radius=0.04,
        tip_length=0.12,
    )
    add_vector_3d(
        fig,
        origin,
        np.array([0.0, 0.0, L]),
        color=axis_color,
        opacity=opacity,
        shaft_radius=0.01,
        tip_radius=0.04,
        tip_length=0.12,
    )

    if show_labels:
        add_labels_3d(
            fig,
            np.array([
                [1.08 * L, 0.0, 0.0],
                [0.0, 1.08 * L, 0.0],
                [0.0, 0.0, 1.08 * L],
            ]),
            [r"$x$", r"$y$", r"$z$"],
            color=axis_color,
            font_size=font_size,
        )

    return fig



def add_angle_3d(
    fig,
    origin,
    vector1,
    vector2,
    *,
    color="black",
    line_width=3,
    radius=None,
    radius_ratio=0.20,
    resolution=60,
    label=None,
    show_degree=False,
    decimals=1,
    font_size=18,
    label_scale=1.25,
    show_right_angle=True,
    right_angle_tol=1e-8,
    row=None,
    col=None,
):
    _select_subplot_3d(fig, row, col)
    origin = _as_point_3d(origin, "origin")
    vector1 = _as_point_3d(vector1, "vector1")
    vector2 = _as_point_3d(vector2, "vector2")

    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    if np.isclose(norm1, 0.0) or np.isclose(norm2, 0.0):
        raise ValueError("각을 이루는 벡터는 영벡터일 수 없습니다.")

    e1 = vector1 / norm1
    e2 = vector2 / norm2

    cos_theta = np.clip(np.dot(e1, e2), -1.0, 1.0)
    theta = np.arccos(cos_theta)

    if np.isclose(theta, 0.0):
        raise ValueError("두 벡터의 방향이 같아 각 표시를 만들 수 없습니다.")

    if np.isclose(theta, np.pi):
        raise ValueError("180도 각 표시는 현재 지원하지 않습니다.")

    if radius is None:
        r = radius_ratio * min(norm1, norm2)
    else:
        r = float(radius)

    if r <= 0:
        raise ValueError("radius는 양수여야 합니다.")

    if show_right_angle and np.isclose(
        cos_theta,
        0.0,
        atol=right_angle_tol,
    ):
        p1 = origin + r * e1
        p2 = origin + r * (e1 + e2)
        p3 = origin + r * e2

        add_curve_3d(
            fig,
            np.array([p1, p2, p3]),
            color=color,
            line_width=line_width,
        )

        label_direction = e1 + e2
        label_direction /= np.linalg.norm(label_direction)

    else:
        arc_start = origin + r * e1
        arc_end = origin + r * e2

        arc = pv.CircularArc(
            pointa=arc_start,
            pointb=arc_end,
            center=origin,
            resolution=resolution,
        )

        fig.add_mesh(
            arc,
            color=color,
            line_width=line_width,
        )

        label_direction = e1 + e2

        if np.isclose(np.linalg.norm(label_direction), 0.0):
            raise ValueError("각의 이등분선 방향을 계산할 수 없습니다.")

        label_direction /= np.linalg.norm(label_direction)

    degree = np.degrees(theta)
    text = None

    if label is not None and show_degree:
        text = f"{label} = {degree:.{decimals}f}°"
    elif label is not None:
        text = str(label)
    elif show_degree:
        text = f"{degree:.{decimals}f}°"

    if text is not None:
        label_point = origin + label_scale * r * label_direction

        add_labels_3d(
            fig,
            [label_point],
            [text],
            color=color,
            font_size=font_size,
        )

    return theta



def add_frame_3d(
    fig,
    point,
    vector1,
    vector2,
    vector3,
    *,
    names=(None, None, None),
    colors=("red", "green", "blue"),
    text_colors=None,
    opacity=1.0,
    shaft_radius=0.02,
    tip_radius=0.06,
    tip_length=0.20,
    show_point=False,
    point_color="black",
    point_size=10,
    row=None,
    col=None,
):
    _select_subplot_3d(fig, row, col)
    point = _as_point_3d(point, "point")
    vectors = [
        _as_point_3d(vector1, "vector1"),
        _as_point_3d(vector2, "vector2"),
        _as_point_3d(vector3, "vector3"),
    ]

    if len(names) != 3:
        raise ValueError("names는 길이가 3이어야 합니다.")

    if len(colors) != 3:
        raise ValueError("colors는 길이가 3이어야 합니다.")

    if text_colors is None:
        text_colors = colors

    if len(text_colors) != 3:
        raise ValueError("text_colors는 길이가 3이어야 합니다.")

    if show_point:
        add_points_3d(
            fig,
            [point],
            color=point_color,
            point_size=point_size,
        )

    for vector, name, color, text_color in zip(
        vectors,
        names,
        colors,
        text_colors,
    ):
        add_vector_3d(
            fig,
            point,
            vector,
            name=name,
            color=color,
            text_color=text_color,
            opacity=opacity,
            shaft_radius=shaft_radius,
            tip_radius=tip_radius,
            tip_length=tip_length,
        )

    return fig



def add_parametric_curve_3d(
    fig,
    curve,
    t_min,
    t_max,
    *,
    resolution=400,
    color="deepskyblue",
    line_width=4,
    opacity=1.0,
    closed=False,
    row=None,
    col=None,
):
    if resolution < 2:
        raise ValueError("resolution은 2 이상이어야 합니다.")

    t_values = np.linspace(float(t_min), float(t_max), resolution)
    points = np.array([curve(t) for t in t_values], dtype=float)

    return add_curve_3d(
        fig,
        points,
        color=color,
        line_width=line_width,
        opacity=opacity,
        closed=closed,
        row=row,
        col=col,
    )



def add_surface_3d(
    fig,
    x,
    y,
    z,
    *,
    color="lightcyan",
    opacity=0.6,
    show_edges=False,
    edge_color="black",
    row=None,
    col=None,
):
    _select_subplot_3d(fig, row, col)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    z = np.asarray(z, dtype=float)

    if x.shape != y.shape or x.shape != z.shape:
        raise ValueError("x, y, z는 같은 shape이어야 합니다.")

    if x.ndim != 2:
        raise ValueError("x, y, z는 2차원 배열이어야 합니다.")

    grid = pv.StructuredGrid(x, y, z)

    fig.add_mesh(
        grid,
        color=color,
        opacity=opacity,
        show_edges=show_edges,
        edge_color=edge_color,
        smooth_shading=True,
    )

    return fig



def add_parametric_surface_3d(
    fig,
    surface,
    u_range,
    v_range,
    *,
    u_resolution=80,
    v_resolution=80,
    color="lightcyan",
    opacity=0.6,
    show_edges=False,
    edge_color="black",
    row=None,
    col=None,
):
    _select_subplot_3d(fig, row, col)

    if u_resolution < 2 or v_resolution < 2:
        raise ValueError("u_resolution과 v_resolution은 2 이상이어야 합니다.")

    u_values = np.linspace(
        float(u_range[0]),
        float(u_range[1]),
        u_resolution,
    )

    v_values = np.linspace(
        float(v_range[0]),
        float(v_range[1]),
        v_resolution,
    )

    points = np.empty(
        (u_resolution, v_resolution, 3),
        dtype=float,
    )

    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            points[i, j] = surface(u, v)

    grid = pv.StructuredGrid(
        points[:, :, 0],
        points[:, :, 1],
        points[:, :, 2],
    )

    fig.add_mesh(
        grid,
        color=color,
        opacity=opacity,
        show_edges=show_edges,
        edge_color=edge_color,
        smooth_shading=True,
    )

    return fig



def add_plane_3d(
    fig,
    origin,
    vector1,
    vector2,
    *,
    u_range=(-1.0, 1.0),
    v_range=(-1.0, 1.0),
    color="lightcyan",
    opacity=0.5,
    show_edges=False,
    row=None,
    col=None,
):
    origin = _as_point_3d(origin, "origin")
    vector1 = _as_point_3d(vector1, "vector1")
    vector2 = _as_point_3d(vector2, "vector2")

    if np.isclose(np.linalg.norm(vector1), 0.0):
        raise ValueError("vector1은 영벡터일 수 없습니다.")

    if np.isclose(np.linalg.norm(vector2), 0.0):
        raise ValueError("vector2는 영벡터일 수 없습니다.")

    if np.isclose(np.linalg.norm(np.cross(vector1, vector2)), 0.0):
        raise ValueError("vector1과 vector2는 평행할 수 없습니다.")

    def surface(u, v):
        return origin + u * vector1 + v * vector2

    return add_parametric_surface_3d(
        fig,
        surface,
        u_range,
        v_range,
        u_resolution=2,
        v_resolution=2,
        color=color,
        opacity=opacity,
        show_edges=show_edges,
        row=row,
        col=col,
    )



def add_cylinder_3d(
    fig,
    *,
    radius=1.0,
    height=2.0,
    center=(0.0, 0.0, 0.0),
    axis=(0.0, 0.0, 1.0),
    theta_resolution=100,
    height_resolution=40,
    color="lightcyan",
    opacity=0.5,
    show_edges=False,
    row=None,
    col=None,
):
    radius = float(radius)
    height = float(height)
    center = _as_point_3d(center, "center")
    axis = _unit_vector_3d(axis)

    if radius <= 0:
        raise ValueError("radius는 양수여야 합니다.")

    if height <= 0:
        raise ValueError("height는 양수여야 합니다.")

    e1, e2 = _orthonormal_basis_perpendicular_to(axis)

    def surface(theta, z):
        radial = np.cos(theta) * e1 + np.sin(theta) * e2
        return center + z * axis + radius * radial

    return add_parametric_surface_3d(
        fig,
        surface,
        (0.0, 2.0 * np.pi),
        (-height / 2.0, height / 2.0),
        u_resolution=theta_resolution,
        v_resolution=height_resolution,
        color=color,
        opacity=opacity,
        show_edges=show_edges,
        row=row,
        col=col,
    )



def add_sphere_3d(
    fig,
    *,
    radius=1.0,
    center=(0.0, 0.0, 0.0),
    theta_resolution=100,
    phi_resolution=60,
    color="lightcyan",
    opacity=0.5,
    show_edges=False,
    row=None,
    col=None,
):
    radius = float(radius)
    center = _as_point_3d(center, "center")

    if radius <= 0:
        raise ValueError("radius는 양수여야 합니다.")

    def surface(theta, phi):
        return center + radius * np.array(
            [
                np.sin(phi) * np.cos(theta),
                np.sin(phi) * np.sin(theta),
                np.cos(phi),
            ]
        )

    return add_parametric_surface_3d(
        fig,
        surface,
        (0.0, 2.0 * np.pi),
        (0.0, np.pi),
        u_resolution=theta_resolution,
        v_resolution=phi_resolution,
        color=color,
        opacity=opacity,
        show_edges=show_edges,
        row=row,
        col=col,
    )



def add_torus_3d(
    fig,
    *,
    major_radius=2.0,
    minor_radius=0.5,
    center=(0.0, 0.0, 0.0),
    axis=(0.0, 0.0, 1.0),
    major_resolution=120,
    minor_resolution=60,
    color="lightcyan",
    opacity=0.5,
    show_edges=False,
    row=None,
    col=None,
):
    major_radius = float(major_radius)
    minor_radius = float(minor_radius)
    center = _as_point_3d(center, "center")
    axis = _unit_vector_3d(axis)

    if major_radius <= 0:
        raise ValueError("major_radius는 양수여야 합니다.")

    if minor_radius <= 0:
        raise ValueError("minor_radius는 양수여야 합니다.")

    e1, e2 = _orthonormal_basis_perpendicular_to(axis)

    def surface(theta, phi):
        radial = np.cos(theta) * e1 + np.sin(theta) * e2

        return (
            center
            + (major_radius + minor_radius * np.cos(phi)) * radial
            + minor_radius * np.sin(phi) * axis
        )

    return add_parametric_surface_3d(
        fig,
        surface,
        (0.0, 2.0 * np.pi),
        (0.0, 2.0 * np.pi),
        u_resolution=major_resolution,
        v_resolution=minor_resolution,
        color=color,
        opacity=opacity,
        show_edges=show_edges,
        row=row,
        col=col,
    )

def add_dimension_line_2d(
    fig,
    x0,
    x1,
    y,
    *,
    text,
    guide_y=0.0,
    color="black",
    width=1,
    tick_height=0.10,
    arrow_length=0.15,
    font_size=16,
    text_yshift=-15,
    row=None,
    col=None,
):
    x0 = float(x0)
    x1 = float(x1)
    y = float(y)

    if np.isclose(x0, x1):
        raise ValueError("치수선의 두 끝점은 서로 달라야 합니다.")

    left = min(x0, x1)
    right = max(x0, x1)

    add_segment_2d(
        fig,
        [left, y],
        [right, y],
        color=color,
        width=width,
        row=row,
        col=col,
    )

    for x in [x0, x1]:
        add_segment_2d(
            fig,
            [x, guide_y],
            [x, y],
            color="gray",
            width=1,
            dash="dot",
            row=row,
            col=col,
        )

        add_segment_2d(
            fig,
            [x, y - tick_height / 2],
            [x, y + tick_height / 2],
            color=color,
            width=width,
            row=row,
            col=col,
        )

    add_vector_2d(
        fig,
        [left + arrow_length, y],
        [-arrow_length, 0],
        color=color,
        width=width,
        row=row,
        col=col,
    )

    add_vector_2d(
        fig,
        [right - arrow_length, y],
        [arrow_length, 0],
        color=color,
        width=width,
        row=row,
        col=col,
    )

    add_labels_2d(
        fig,
        [[(left + right) / 2, y]],
        [text],
        color=color,
        font_size=font_size,
        yshift=text_yshift,
        row=row,
        col=col,
    )

    return fig