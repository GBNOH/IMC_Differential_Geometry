r"""2013학년도 1차 34번: 토러스 안쪽 점에서 교선의 법곡률.

X(u,v)=((2+cos u)cos v,(2+cos u)sin v,sin u), q=X(π,0).
q에서 U=(1,0,0)을 택하면 E=G=1,F=0,L=1,M=0,N=-1이다.
P:y+z=0의 교선 접선은 (0,1,-1)/√2이므로 법곡률은 (1-1)/2=0.
따라서 계산에 따른 정답은 ①이다. 제시된 해설의 N=1, 정답 ④와 불일치한다.
국소 교선 c(z)=(sqrt((2-sqrt(1-z²))²-z²),-z,z)의 c''(0)=0으로도 확인된다.
교선 표시용 매개변수 u는 호길이가 아니며, 법곡률 계산에는 단위접선을 사용한다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2013_q34_torus_normal_curvature.py
    python .\supplement_exam\exam_2013_q34_torus_normal_curvature.py --output output/exam_2013_q34.html --no-show
"""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def surface(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """토러스의 공간 좌표를 반환한다."""
    u, v = np.broadcast_arrays(u, v)
    return np.stack(((2+np.cos(u))*np.cos(v), (2+np.cos(u))*np.sin(v), np.sin(u)), axis=-1)


def intersection(u: np.ndarray, side: int = 1) -> np.ndarray:
    """y+z=0인 교선의 x 양수 또는 음수 연결성분을 반환한다."""
    z = np.sin(u)
    x = side*np.sqrt((2+np.cos(u))**2-z*z)
    return np.stack((x, -z, z), axis=-1)


def normal_curvature(theta: np.ndarray | float) -> np.ndarray:
    """q에서 방향 cos(theta)X_u+sin(theta)X_v의 법곡률."""
    return np.cos(np.asarray(theta))**2 - np.sin(np.asarray(theta))**2


# 이 문항의 시각화 구성
def moving_traces(theta: float) -> list:
    """q의 접평면 위 단위방향과 Euler 공식의 대응점."""
    q = np.array([1., 0., 0.])
    direction = np.array([0., np.sin(theta), -np.cos(theta)])
    points = np.array([q-direction, q+direction])
    return [go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="lines",
                        line=dict(color="#E45756", width=7), name="선택한 접선 방향"),
            go.Scatter(x=[np.degrees(theta)], y=[normal_curvature(theta)], mode="markers",
                       marker=dict(size=12, color="#E45756"), showlegend=False)]


def build_figure() -> go.Figure:
    """토러스 교선과 방향에 따른 법곡률을 나란히 표시한다."""
    fig = make_subplots(rows=1, cols=2, specs=[[dict(type="scene"), dict(type="xy")]],
                        horizontal_spacing=.10,
                        subplot_titles=("토러스와 평면 y+z=0의 교선", "q에서 κₙ(θ)=cos²θ−sin²θ"))
    u, v = np.meshgrid(np.linspace(0, 2*np.pi, 101), np.linspace(0, 2*np.pi, 101))
    p = surface(u, v)
    fig.add_trace(go.Surface(x=p[..., 0], y=p[..., 1], z=p[..., 2], opacity=.3,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]], showscale=False,
                            name="토러스", showlegend=True), row=1, col=1)
    x, y = np.meshgrid([-3.2, 3.2], [-1.3, 1.3])
    fig.add_trace(go.Surface(x=x,y=y,z=-y,opacity=.18,showscale=False,
                            colorscale=[[0,"#F2A541"],[1,"#F2A541"]], name="P: y+z=0",
                            showlegend=True),row=1,col=1)
    for side in (1,-1):
        p=intersection(np.linspace(0,2*np.pi,501),side)
        fig.add_trace(go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",
                                  line=dict(color="#7040A0",width=6), name="교선",showlegend=side==1),row=1,col=1)
    fig.add_trace(go.Scatter3d(x=[1],y=[0],z=[0],mode="markers+text",text=["q=(1,0,0)"],
                              textposition="top center",marker=dict(size=6,color="#222222"),showlegend=False),row=1,col=1)
    angles=np.linspace(0,np.pi,361)
    fig.add_trace(go.Scatter(x=np.degrees(angles),y=normal_curvature(angles),mode="lines",
                            name="Euler 공식",line=dict(color="#7040A0",width=4)),row=1,col=2)
    fig.add_trace(go.Scatter(x=[45],y=[0],mode="markers+text",text=["문제의 방향: 45°, κₙ=0"],
                            textposition="top right",marker=dict(size=10,color="#239B56"),showlegend=False),row=1,col=2)
    indices=[len(fig.data),len(fig.data)+1]
    a,b=moving_traces(np.pi/4)
    fig.add_trace(a,row=1,col=1)
    fig.add_trace(b,row=1,col=2)
    parameters=np.linspace(0,np.pi,25)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(t)),traces=indices) for i,t in enumerate(parameters)]
    fig.update_xaxes(title_text="주방향 X_u와 이루는 각 θ (도)",range=[0,180],tickvals=[0,45,90,135,180],row=1,col=2)
    fig.update_yaxes(title_text="법곡률 κₙ",range=[-1.2,1.2],row=1,col=2)
    fig.update_layout(title=dict(text="2013학년도 1차 34번 · 토러스의 법곡률"
                                 "<br><sup>q의 주곡률은 +1, −1 · 문제의 교선 방향에서 |κₙ|=0 (①)</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=30,r=30,t=115,b=180),
                      scene=dict(aspectmode="data",xaxis_title="x",yaxis_title="y",zaxis_title="z",
                                 uirevision="camera",camera=dict(eye=dict(x=1.5,y=1.5,z=1.5))),
                      legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=6,y=-.07,currentvalue=dict(prefix="접선 방향 θ = "),steps=[
                          dict(label=f"{np.degrees(t):.1f}°",method="animate",args=[[str(i)],
                               dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,t in enumerate(parameters)])])
    fig.add_annotation(text="해설의 N=+1은 부호 오류로 판단됨: U=(1,0,0)일 때 X_vv=(-1,0,0), 따라서 N=−1.",
                       xref="paper",yref="paper",x=.5,y=-.34,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def parse_args() -> argparse.Namespace:
    """출력 옵션을 읽는다."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,help="HTML 저장 경로")
    parser.add_argument("--no-show",action="store_true",help="브라우저 창을 열지 않음")
    return parser.parse_args()


def main() -> None:
    """그림을 생성하고 HTML 저장 또는 화면 표시를 실행한다."""
    args=parse_args()
    figure=build_figure()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        figure.write_html(args.output,include_plotlyjs=True)
        print(f"저장 완료: {args.output.resolve()}")
    if not args.no_show:
        figure.show()


if __name__ == "__main__":
    main()
