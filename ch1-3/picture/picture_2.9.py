import numpy as np
import plot_tools_diffgeo as ptd


fig = ptd.create_figure_3d()

O = np.array([0, 0, 0])
x = O

T = np.array([1, 0, 0])
N = np.array([0, 1, 0])
B = np.array([0, 0, 1])

L = 2.0

ptd.add_plane_3d(fig, x, T, N, u_range=(-L, L), v_range=(-L, L), color="lightcyan", opacity=0.18)
ptd.add_plane_3d(fig, x, N, B, u_range=(-L, L), v_range=(-L, L), color="mistyrose", opacity=0.18)
ptd.add_plane_3d(fig, x, T, B, u_range=(-L, L), v_range=(-L, L), color="lavender", opacity=0.18)

ptd.add_segment_3d(fig, x - L * T, x + L * T)
ptd.add_segment_3d(fig, x - L * N, x + L * N)
ptd.add_segment_3d(fig, x - L * B, x + L * B)

ptd.add_vector_3d(fig, x, T)
ptd.add_vector_3d(fig, x, N)
ptd.add_vector_3d(fig, x, B)

ptd.add_points_3d(fig, [x], point_size=12)

ptd.add_labels_3d(
    fig,
    [
        x,
        x + 1.15 * T,
        x + 1.15 * N,
        x + 1.15 * B,
        np.array([1.1, -0.25, -0.15]),
        np.array([0.25, 1.1, -0.15]),
        np.array([0.15, 0.2, 1.1]),
        np.array([0.0, -1.25, 1.0]),
        np.array([1.0, 0.0, -1.25]),
        np.array([-1.15, 1.0, 0.0]),
    ],
    [
        r"$x$",
        r"$T$",
        r"$N$",
        r"$B$",
        r"$y=x+tT$",
        r"$y=x+tN$",
        r"$y=x+tB$",
        r"$\langle y-x,\;T\rangle=0$",
        r"$\langle y-x,\;N\rangle=0$",
        r"$\langle y-x,\;B\rangle=0$",
    ],
)

fig.show()

### 9/14 한글이 컴파일되지 않아 수식으로 표현