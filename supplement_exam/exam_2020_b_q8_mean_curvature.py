r"""2020학년도 1차 B 8번: 접평면과 평균곡률.

X(u,v)=(u²+v,u-v²,uv), P=X(1,2)=(3,-3,2).
Xu=(2,1,2), Xv=(1,-4,1), N=(1,0,-1)/sqrt(2).
접평면은 x-z-1=0. I=diag(9,18), II=[[sqrt(2),-1/sqrt(2)],[-1/sqrt(2),0]].
H=(EN+GL-2FM)/(2(EG-F²))=sqrt(2)/18.
제시된 해설의 L=0은 Xuu=(2,0,0)과 모순이며 실제 L=sqrt(2)이다.
직교 단위기저 e1=Xu/3,e2=Xv/sqrt(18)에서 모양연산자 행렬은
[[sqrt(2)/9,-1/18],[-1/18,0]]. 고유값이 주곡률이며 그 평균은 H이다.
법선 방향을 반대로 택하면 H의 부호가 바뀐다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2020_b_q8_mean_curvature.py
저장: 위 명령에 --output output/exam_2020_b_q8.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def surface(u: np.ndarray | float, v: np.ndarray | float) -> np.ndarray:
    """곡면 좌표를 반환한다."""
    u,v=np.broadcast_arrays(u,v)
    return np.stack((u*u+v,u-v*v,u*v),axis=-1)


def geometry() -> tuple:
    """단위 접기저와 법선, 직교기저에서의 모양연산자를 계산한다."""
    xu=np.array([2.,1.,2.]); xv=np.array([1.,-4.,1.])
    normal=np.cross(xu,xv); normal/=np.linalg.norm(normal)
    E=xu@xu; G=xv@xv
    L=np.array([2.,0,0])@normal
    M=np.array([0.,0,1])@normal
    N=np.array([0.,-2,0])@normal
    shape=np.array([[L/E,M/np.sqrt(E*G)],[M/np.sqrt(E*G),N/G]])
    return xu/np.sqrt(E),xv/np.sqrt(G),normal,shape


def normal_curvature(theta: np.ndarray | float) -> np.ndarray:
    """단위 접방향의 법곡률."""
    *_,shape=geometry()
    d=np.stack((np.cos(theta),np.sin(theta)),axis=-1)
    return np.einsum('...i,ij,...j->...',d,shape,d)


# 이 문항의 시각화 구성
def moving_traces(theta: float) -> list:
    """P의 접방향과 그래프 대응점."""
    e1,e2,_,_=geometry(); p=surface(1,2)
    d=np.cos(theta)*e1+np.sin(theta)*e2
    end=p+d
    return [go.Scatter3d(x=[p[0],end[0]],y=[p[1],end[1]],z=[p[2],end[2]],mode="lines",
                        line=dict(color="#E45756",width=7),name="단위 접방향"),
            go.Cone(x=[end[0]],y=[end[1]],z=[end[2]],u=[d[0]],v=[d[1]],w=[d[2]],
                    anchor="tip",sizemode="absolute",sizeref=.15,showscale=False,
                    colorscale=[[0,"#E45756"],[1,"#E45756"]],hoverinfo="skip"),
            go.Scatter(x=[np.degrees(theta)],y=[normal_curvature(theta)],mode="markers",
                       marker=dict(size=12,color="#E45756"),showlegend=False)]


def build_figure() -> go.Figure:
    """접평면과 방향별 법곡률, 평균곡률을 표시한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],horizontal_spacing=.1,
                      subplot_titles=("P의 접평면 x−z−1=0","법곡률의 최댓값·최솟값의 평균이 H"))
    u,v=np.meshgrid(np.linspace(.5,1.5,71),np.linspace(1.5,2.5,71))
    p=surface(u,v)
    fig.add_trace(go.Surface(x=p[...,0],y=p[...,1],z=p[...,2],opacity=.6,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],showscale=False,name="곡면",showlegend=True),row=1,col=1)
    e1,e2,n,S=geometry(); point=surface(1,2)
    a,b=np.meshgrid([-1.3,1.3],[-1.3,1.3]); plane=point+a[...,None]*e1+b[...,None]*e2
    fig.add_trace(go.Surface(x=plane[...,0],y=plane[...,1],z=plane[...,2],opacity=.3,
                            colorscale=[[0,"#F2A541"],[1,"#F2A541"]],showscale=False,name="접평면",showlegend=True),row=1,col=1)
    for d,label,color in ((e1,"e₁=Xu/3","#7040A0"),(e2,"e₂=Xv/√18","#239B56"),(n,"단위법선 N","#4C78A8")):
        end=point+d
        fig.add_trace(go.Scatter3d(x=[point[0],end[0]],y=[point[1],end[1]],z=[point[2],end[2]],mode="lines",
                                  line=dict(color=color,width=4),name=label),row=1,col=1)
    fig.add_trace(go.Scatter3d(x=[3],y=[-3],z=[2],mode="markers+text",text=["P"],marker=dict(size=5,color="#222222"),showlegend=False),row=1,col=1)
    angles=np.linspace(0,np.pi,361)
    fig.add_trace(go.Scatter(x=np.degrees(angles),y=normal_curvature(angles),mode="lines",line=dict(color="#7040A0",width=4),name="κₙ(θ)"),row=1,col=2)
    H=np.trace(S)/2
    for k,label in [(H,"H=√2/18"),*[(k,f"주곡률 {k:.5f}") for k in np.linalg.eigvalsh(S)]]:
        fig.add_trace(go.Scatter(x=[0,180],y=[k,k],mode="lines",line=dict(width=2,dash="dash"),name=label),row=1,col=2)
    indices=list(range(len(fig.data),len(fig.data)+3))
    for i,trace in enumerate(moving_traces(0)):
        fig.add_trace(trace,row=1,col=2 if i==2 else 1)
    parameters=np.linspace(0,np.pi,37)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(t)),traces=indices) for i,t in enumerate(parameters)]
    fig.update_xaxes(title_text="e₁와 이루는 각 θ (도)",range=[0,180],autorange=False,row=1,col=2)
    fig.update_yaxes(title_text="곡률",range=[-.05,.21],autorange=False,row=1,col=2)
    fig.update_layout(title=dict(text="2020학년도 1차 B 8번 · 접평면과 평균곡률"
                                 "<br><sup>P=(3,−3,2) · x−z−1=0 · H=√2/18 ≈ 0.07857</sup>",x=.5),
                      template="plotly_white",height=840,margin=dict(l=25,r=30,t=115,b=190),
                      scene=dict(xaxis=dict(title="x",range=[1,5],autorange=False),
                                 yaxis=dict(title="y",range=[-6,0],autorange=False),
                                 zaxis=dict(title="z",range=[0,4],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=2/3,y=1,z=2/3),uirevision="camera",
                                 camera=dict(eye=dict(x=1.6,y=1.6,z=1.2))),legend=dict(orientation="h",y=-.24),
                      sliders=[dict(active=0,y=-.07,currentvalue=dict(prefix="θ = "),steps=[
                          dict(label=f"{np.degrees(t):.0f}°",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i,t in enumerate(parameters)])])
    fig.add_annotation(text="해설의 L=0과 달리 Xuu·N=√2입니다. 법선은 Xu×Xv 방향이며, e₁,e₂는 주방향이 아닙니다.",
                       xref="paper",yref="paper",x=.5,y=-.37,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def main() -> None:
    """그림을 생성하고 저장 또는 표시한다."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--no-show",action="store_true")
    args=parser.parse_args()
    fig=build_figure()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        fig.write_html(args.output,include_plotlyjs=True)
        print(f"저장 완료: {args.output.resolve()}")
    if not args.no_show:
        fig.show()


if __name__ == "__main__":
    main()
