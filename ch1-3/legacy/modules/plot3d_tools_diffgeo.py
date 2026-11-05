import numpy as np
import pyvista as pv

def add_vector(
    fig,
    origin,
    vector,
    *,
    name=None,
    color="black",
    text_color=None,
    show_magnitude=False,
    show_endpoint=False,
    opacity=1.0,
):

    origin = np.asarray(origin, dtype=float)
    vector = np.asarray(vector, dtype=float)

    if origin.shape != (3,) or vector.shape != (3,):
        raise ValueError(
            "origin과 vector는 길이가 3인 배열이어야 합니다."
        )

    vector_length = np.linalg.norm(vector)

    if np.isclose(vector_length, 0):
        raise ValueError(
            "영벡터는 화살표로 나타낼 수 없습니다."
        )

    end = origin + vector

    # 화살표 형태는 고정
    shaft_radius = 0.02
    tip_radius = 0.06
    tip_length = 0.20

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

    # text_color를 지정하지 않으면 벡터 색을 따름
    if text_color is None:
        text_color = color

    # 벡터 이름 또는 크기
    if name is not None or show_magnitude:

        midpoint = origin + vector / 2

        label_parts = []

        if name is not None:
            label_parts.append(str(name))

        if show_magnitude:
            label_parts.append(f"{vector_length:g}")

        label_text = "   ".join(label_parts)

        fig.add_point_labels(
            [midpoint],
            [label_text],
            show_points=False,
            shape=None,
            text_color=text_color,
            font_size=18,
            always_visible=True,
        )

    # 끝점 좌표
    if show_endpoint:

        # 화살촉과 겹치지 않도록 벡터 방향으로 조금 이동
        label_point = end + 0.08 * vector / vector_length

        endpoint_text = (
            f"({end[0]:g}, {end[1]:g}, {end[2]:g})"
        )

        fig.add_point_labels(
            [label_point],
            [endpoint_text],
            show_points=False,
            shape=None,
            text_color=text_color,
            font_size=16,
            always_visible=True,
        )

def _compute_axis_length_from_bounds(bounds):

    # 고정값
    margin_ratio = 0.10
    default_axis_length = 1.0

    bounds = np.asarray(bounds, dtype=float)

    if bounds.shape != (6,):
        return default_axis_length

    if not np.all(np.isfinite(bounds)):
        return default_axis_length

    max_abs = np.max(np.abs(bounds))

    if np.isclose(max_abs, 0.0):
        return default_axis_length

    return (1.0 + margin_ratio) * max_abs


def add_coordinate_axes(
    fig,
    *,
    axis_length=None,
    axis_color="black",
    show_arrow=True,
    show_labels=True,
    positive_only=False,
    opacity=1.0,
):
    # -------------------------------------------------
    # 고정 설정값
    # -------------------------------------------------

    label_font_size = 16
    label_offset_ratio = 0.08

    arrow_head_length = 0.20
    arrow_head_radius = 0.05

    axis_shaft_radius = 0.01

    # -------------------------------------------------
    # 축 길이
    # -------------------------------------------------

    if axis_length is None:

        L = _compute_axis_length_from_bounds(
            fig.bounds
        )

    else:

        L = float(axis_length)

        if L <= 0:
            raise ValueError(
                "axis_length는 양수여야 합니다."
            )

    # -------------------------------------------------
    # 축 몸통의 중심과 길이
    # -------------------------------------------------

    if positive_only:

        if show_arrow:
            shaft_center = (L - arrow_head_length) / 2
            shaft_height = L - arrow_head_length

        else:
            shaft_center = L / 2
            shaft_height = L

    else:

        if show_arrow:
            shaft_center = -arrow_head_length / 2
            shaft_height = 2 * L - arrow_head_length

        else:
            shaft_center = 0.0
            shaft_height = 2 * L

    # -------------------------------------------------
    # 축 몸통
    # -------------------------------------------------

    x_axis = pv.Cylinder(
        center=(shaft_center, 0, 0),
        direction=(1, 0, 0),
        radius=axis_shaft_radius,
        height=shaft_height,
    )

    y_axis = pv.Cylinder(
        center=(0, shaft_center, 0),
        direction=(0, 1, 0),
        radius=axis_shaft_radius,
        height=shaft_height,
    )

    z_axis = pv.Cylinder(
        center=(0, 0, shaft_center),
        direction=(0, 0, 1),
        radius=axis_shaft_radius,
        height=shaft_height,
    )

    fig.add_mesh(
        x_axis,
        color=axis_color,
        smooth_shading=True,
        opacity=opacity,
    )

    fig.add_mesh(
        y_axis,
        color=axis_color,
        smooth_shading=True,
        opacity=opacity,
    )

    fig.add_mesh(
        z_axis,
        color=axis_color,
        smooth_shading=True,
        opacity=opacity,
    )

    # -------------------------------------------------
    # 양의 방향 화살머리
    # -------------------------------------------------

    if show_arrow:

        x_head = pv.Cone(
            center=(L - arrow_head_length / 2, 0, 0),
            direction=(1, 0, 0),
            height=arrow_head_length,
            radius=arrow_head_radius,
        )

        y_head = pv.Cone(
            center=(0, L - arrow_head_length / 2, 0),
            direction=(0, 1, 0),
            height=arrow_head_length,
            radius=arrow_head_radius,
        )

        z_head = pv.Cone(
            center=(0, 0, L - arrow_head_length / 2),
            direction=(0, 0, 1),
            height=arrow_head_length,
            radius=arrow_head_radius,
        )

        fig.add_mesh(
            x_head,
            color=axis_color,
            smooth_shading=True,
            opacity=opacity,
        )

        fig.add_mesh(
            y_head,
            color=axis_color,
            smooth_shading=True,
            opacity=opacity,
        )

        fig.add_mesh(
            z_head,
            color=axis_color,
            smooth_shading=True,
            opacity=opacity,
        )

    # -------------------------------------------------
    # 축 라벨
    # -------------------------------------------------

    if show_labels:

        offset = label_offset_ratio * L

        label_points = np.array([
            [L + offset, 0.0, 0.0],
            [0.0, L + offset, 0.0],
            [0.0, 0.0, L + offset],
        ])

        fig.add_point_labels(
            label_points,
            ["x", "y", "z"],
            font_size=label_font_size,
            text_color=axis_color,
            show_points=False,
            shape=None,
            always_visible=True,
        )

def add_angle(
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
    angle_name=None,
    show_angle_value=False,
    font_size=18,
    label_scale=1.25,
    right_angle_tol=1e-6,
):
    """
    3차원에서 두 벡터 사이의 각을 표시한다.

    직각인 경우에는 원호 대신 일반적인 직각 표기(꺾인 선)를 사용한다.

    Parameters
    ----------
    fig
        pyvista.Plotter 객체

    origin
        각의 꼭짓점

    vector1, vector2
        각을 이루는 두 벡터

    color
        각 표시의 색

    line_width
        원호 또는 직각표시 선의 두께

    radius
        각 표시 반지름.
        None이면 radius_ratio * min(||vector1||, ||vector2||) 로 자동 설정

    radius_ratio
        radius=None일 때 사용할 비율

    resolution
        일반 각도에서 원호를 그릴 때 분할 수

    angle_name
        각 라벨 이름.
        예: r"\\theta", r"\\alpha"
        show_angle_value=False이면 기호만,
        True이면 "\\theta = 79.0^\\circ" 형태로 표시

    show_angle_value
        각도값 표시 여부

    font_size
        라벨 글자 크기

    label_scale
        라벨 위치를 반지름의 몇 배로 둘 것인지 결정

    right_angle_tol
        직각 판정 허용오차

    Returns
    -------
    theta
        두 벡터 사이의 각(라디안)
    """

    origin = np.asarray(origin, dtype=float)
    vector1 = np.asarray(vector1, dtype=float)
    vector2 = np.asarray(vector2, dtype=float)

    if origin.shape != (3,) or vector1.shape != (3,) or vector2.shape != (3,):
        raise ValueError("origin, vector1, vector2는 길이가 3인 배열이어야 합니다.")

    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    if np.isclose(norm1, 0):
        raise ValueError("vector1은 영벡터일 수 없습니다.")

    if np.isclose(norm2, 0):
        raise ValueError("vector2는 영벡터일 수 없습니다.")

    u1 = vector1 / norm1
    u2 = vector2 / norm2

    cos_theta = np.dot(u1, u2)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    theta = np.arccos(cos_theta)
    theta_deg = np.degrees(theta)

    if radius is None:
        r = radius_ratio * min(norm1, norm2)
    else:
        r = float(radius)
        if r <= 0:
            raise ValueError("radius는 양수여야 합니다.")

    if np.isclose(r, 0):
        raise ValueError("반지름이 너무 작습니다.")

    # -------------------------------------------------
    # 라벨 텍스트
    # -------------------------------------------------
    label_text = None

    if angle_name is not None and show_angle_value:
        label_text = fr"${angle_name} = {theta_deg:.1f}^\circ$"
    elif angle_name is not None:
        label_text = fr"${angle_name}$"
    elif show_angle_value:
        label_text = fr"${theta_deg:.1f}^\circ$"

    # -------------------------------------------------
    # 직각인 경우: 꺾인 선으로 표시
    # -------------------------------------------------
    if np.isclose(cos_theta, 0.0, atol=right_angle_tol):

        P1 = origin + r * u1
        P2 = origin + r * (u1 + u2)
        P3 = origin + r * u2

        right_angle = pv.lines_from_points(
            np.array([P1, P2, P3])
        )

        fig.add_mesh(
            right_angle,
            color=color,
            line_width=line_width,
        )

        if label_text is not None:
            label_dir = u1 + u2
            label_dir = label_dir / np.linalg.norm(label_dir)

            label_pos = origin + (label_scale * r) * label_dir

            fig.add_point_labels(
                [label_pos],
                [label_text],
                show_points=False,
                shape=None,
                text_color=color,
                font_size=font_size,
                always_visible=True,
            )

        return theta

    # -------------------------------------------------
    # 180도는 예외 처리
    # -------------------------------------------------
    if np.isclose(theta, np.pi, atol=1e-6):
        raise ValueError("서로 반대 방향인 두 벡터(180°)에 대한 각 표시는 현재 지원하지 않습니다.")

    # -------------------------------------------------
    # 일반적인 경우: 원호로 표시
    # -------------------------------------------------
    arc_start = origin + r * u1
    arc_end = origin + r * u2

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

    if label_text is not None:
        label_dir = u1 + u2
        label_dir = label_dir / np.linalg.norm(label_dir)

        label_pos = origin + (label_scale * r) * label_dir

        fig.add_point_labels(
            [label_pos],
            [label_text],
            show_points=False,
            shape=None,
            text_color=color,
            font_size=font_size,
            always_visible=True,
        )

    return theta

def add_frame(
    fig,
    point,
    v1,
    v2,
    v3,
    *,
    names=None,
    colors=("red", "green", "blue"),
    text_colors=None,
    scale=1.0,
    normalize=False,
    opacity=1.0,
    show_point=False,
    point_color="black",
    point_size=10,
):
    point = np.asarray(point, dtype=float)
    v1 = np.asarray(v1, dtype=float)
    v2 = np.asarray(v2, dtype=float)
    v3 = np.asarray(v3, dtype=float)

    if point.shape != (3,):
        raise ValueError("point는 길이가 3인 배열이어야 합니다.")

    for v in (v1, v2, v3):
        if v.shape != (3,):
            raise ValueError("v1, v2, v3는 길이가 3인 배열이어야 합니다.")

    if names is None:
        names = (None, None, None)

    if len(names) != 3:
        raise ValueError("names는 길이가 3이어야 합니다.")

    if len(colors) != 3:
        raise ValueError("colors는 길이가 3이어야 합니다.")

    if text_colors is None:
        text_colors = colors

    if len(text_colors) != 3:
        raise ValueError("text_colors는 길이가 3이어야 합니다.")

    vectors = [v1.copy(), v2.copy(), v3.copy()]

    if normalize:
        for i, v in enumerate(vectors):
            norm = np.linalg.norm(v)
            if np.isclose(norm, 0):
                raise ValueError("영벡터는 표구 벡터로 사용할 수 없습니다.")
            vectors[i] = v / norm

    vectors = [scale * v for v in vectors]

    if show_point:
        fig.add_points(
            np.array([point]),
            color=point_color,
            point_size=point_size,
            render_points_as_spheres=True,
        )

    for v, name, color, text_color in zip(vectors, names, colors, text_colors):
        add_vector(
            fig,
            point,
            v,
            name=name,
            color=color,
            text_color=text_color,
            opacity=opacity,
        )