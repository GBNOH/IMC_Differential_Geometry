r"""2013학년도 2차 3-2 (II): 구의 단면을 사영한 타원체의 가우스곡률.

S³: x²+y²+z²+w²=1, H: y+z+w=0에서 w=-y-z를 제거하면
M: x²+2y²+2z²+2yz=1이다.
a=(y+z)/√2, b=(y-z)/√2로 두면 x²+3a²+b²=1.
q=(1,0,0)의 주방향은 e_a=(0,1,1)/√2, e_b=(0,1,-1)/√2이다.
바깥 법선 (1,0,0), 모양연산자 -dN 기준 주곡률은 -3,-1이고 K=3.
3차원 화면은 사영 결과 M이며 4차원 구 자체를 직접 그린 것이 아니다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2013_second_q3_2_projected_sphere.py
    python .\supplement_exam\exam_2013_second_q3_2_projected_sphere.py --output output/exam_2013_second_q3_2.html --no-show
"""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def coordinates(x: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """회전된 직교좌표 (x,a,b)를 (x,y,z)로 변환한다."""
    x,a,b=np.broadcast_arrays(x,a,b)
    return np.stack((x,(a+b)/np.sqrt(2),(a-b)/np.sqrt(2)),axis=-1)


def ellipsoid(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """사영된 타원체의 매개변수표현을 반환한다."""
    return coordinates(np.cos(u),np.sin(u)*np.cos(v)/np.sqrt(3),np.sin(u)*np.sin(v))


def lift(points: np.ndarray) -> np.ndarray:
    """사영점에 w=-y-z를 복원하여 H∩S³의 점을 반환한다."""
    p=np.asarray(points)
    return np.concatenate((p,(-p[...,1]-p[...,2])[...,None]),axis=-1)


def normal_curvature(theta: np.ndarray | float) -> np.ndarray:
    """e_a와 각 theta를 이루는 방향의 법곡률(바깥 법선 기준)."""
    return -3*np.cos(theta)**2-np.sin(theta)**2


# 이 문항의 시각화 구성
def selected_traces(theta: float) -> list:
    """선택한 법단면과 q에서의 단위 접선, 곡률 대응점을 만든다."""
    t=np.linspace(0,2*np.pi,241)
    coefficient=3*np.cos(theta)**2+np.sin(theta)**2
    r=np.sin(t)/np.sqrt(coefficient)
    p=coordinates(np.cos(t),r*np.cos(theta),r*np.sin(theta))
    direction=coordinates(0,np.cos(theta),np.sin(theta))
    line=np.array([np.array([1,0,0])-.65*direction,np.array([1,0,0])+.65*direction])
    return [go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",
                        line=dict(color="#E45756",width=7),name="선택한 법단면"),
            go.Scatter3d(x=line[:,0],y=line[:,1],z=line[:,2],mode="lines",
                         line=dict(color="#222222",width=5),name="q의 접선 방향"),
            go.Scatter(x=[np.degrees(theta)],y=[normal_curvature(theta)],mode="markers",
                       marker=dict(color="#E45756",size=12),showlegend=False)]


def build_figure() -> go.Figure:
    """타원체의 법단면과 방향별 법곡률을 함께 표시한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],
                      horizontal_spacing=.1,subplot_titles=("사영 결과 M: x²+3a²+b²=1","q에서 주곡률 −3, −1 → K=3"))
    u,v=np.meshgrid(np.linspace(0,np.pi,81),np.linspace(0,2*np.pi,101))
    p=ellipsoid(u,v)
    fig.add_trace(go.Surface(x=p[...,0],y=p[...,1],z=p[...,2],opacity=.3,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],showscale=False,
                            name="타원체 M",showlegend=True),row=1,col=1)
    t=np.linspace(0,2*np.pi,241)
    for theta,color,name in ((0,"#7040A0","주단면 b=0: |κ₁|=3"),(np.pi/2,"#239B56","주단면 a=0: |κ₂|=1")):
        r=np.sin(t)/np.sqrt(3*np.cos(theta)**2+np.sin(theta)**2)
        p=coordinates(np.cos(t),r*np.cos(theta),r*np.sin(theta))
        fig.add_trace(go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",
                                  line=dict(color=color,width=5),name=name),row=1,col=1)
    fig.add_trace(go.Scatter3d(x=[1],y=[0],z=[0],mode="markers+text",text=["q=(1,0,0)"],
                              textposition="top center",marker=dict(size=6,color="#222222"),showlegend=False),row=1,col=1)
    angles=np.linspace(0,np.pi,361)
    fig.add_trace(go.Scatter(x=np.degrees(angles),y=normal_curvature(angles),mode="lines",
                            line=dict(color="#7040A0",width=4),name="κₙ(θ)=−3cos²θ−sin²θ"),row=1,col=2)
    moving=selected_traces(0)
    indices=[len(fig.data)+i for i in range(3)]
    for i,trace in enumerate(moving):
        fig.add_trace(trace,row=1,col=2 if i==2 else 1)
    parameters=np.linspace(0,np.pi,25)
    fig.frames=[go.Frame(name=str(i),data=selected_traces(float(t)),traces=indices) for i,t in enumerate(parameters)]
    fig.update_xaxes(title_text="e_a와 이루는 각 θ (도)",range=[0,180],tickvals=[0,45,90,135,180],row=1,col=2)
    fig.update_yaxes(title_text="법곡률 κₙ · 바깥 법선 기준",range=[-3.3,-.7],row=1,col=2)
    fig.update_layout(title=dict(text="2013학년도 2차 3-2 (II) · 사영된 타원체의 곡률"
                                 "<br><sup>w=−y−z → x²+2y²+2z²+2yz=1 · K(1,0,0)=3</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=30,r=30,t=115,b=180),
                      scene=dict(aspectmode="data",xaxis_title="x",yaxis_title="y",zaxis_title="z",
                                 uirevision="camera",camera=dict(eye=dict(x=1.6,y=1.5,z=1.2))),
                      legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=0,y=-.07,currentvalue=dict(prefix="법단면 방향 θ = "),steps=[
                          dict(label=f"{np.degrees(t):.1f}°",method="animate",args=[[str(i)],
                               dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,t in enumerate(parameters)])])
    fig.add_annotation(text="a=(y+z)/√2, b=(y−z)/√2 · 법선 방향을 바꾸어도 K=κ₁κ₂=3은 같다.",
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
