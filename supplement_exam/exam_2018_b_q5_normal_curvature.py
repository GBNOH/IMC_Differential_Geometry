r"""2018학년도 1차 B 5번: 회전면의 주곡률과 지정 방향의 법곡률.

X(u,v)=(u cos v,u sin v,1/u), u>0,-π<v<π. p=X(1,0).
X_u×X_v 방향의 법선 U=(1,0,1)/sqrt(2)를 택한다.
p에서 E=2,F=0,G=1,L=sqrt(2),M=0,N=-1/sqrt(2).
k1=1/sqrt(2), k2=-1/sqrt(2).
e1=(1,0,-1)/sqrt(2), e2=(0,1,0),
w=(1,1,-1)/sqrt(3)=sqrt(2/3)e1+sqrt(1/3)e2.
따라서 kn(w)=(2/3)k1+(1/3)k2=sqrt(2)/6.
법선 방향을 반대로 택하면 부호도 반대로 바뀐다.
그림에는 0.4≤u≤2.2의 일부만 표시한다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2018_b_q5_normal_curvature.py
저장: 위 명령에 --output output/exam_2018_b_q5.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

P=np.array([1.,0.,1.])
E1=np.array([1.,0.,-1.])/np.sqrt(2)
E2=np.array([0.,1.,0.])
THETA_W=np.arctan(1/np.sqrt(2))


# 수학적 정의와 계산
def surface(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """양의 u에서 회전면 좌표를 반환한다."""
    u,v=np.broadcast_arrays(u,v)
    if np.any(u<=0):
        raise ValueError("u는 양수여야 합니다.")
    return np.stack((u*np.cos(v),u*np.sin(v),1/u),axis=-1)


def normal_curvature(theta: np.ndarray | float) -> np.ndarray:
    """e1과 각 theta를 이루는 단위방향에 Euler 공식을 적용한다."""
    return (np.cos(theta)**2-np.sin(theta)**2)/np.sqrt(2)


# 이 문항의 시각화 구성
def line(points: np.ndarray, name: str, color: str) -> go.Scatter3d:
    """공간 선분 또는 곡선을 만든다."""
    return go.Scatter3d(x=points[:,0],y=points[:,1],z=points[:,2],mode="lines",
                        line=dict(color=color,width=6),name=name)


def moving_traces(theta: float) -> list:
    """선택한 단위 접벡터와 법곡률 그래프의 대응점."""
    w=np.cos(theta)*E1+np.sin(theta)*E2
    return [line(np.array([P,P+w]),"선택한 방향","#E45756"),
            go.Cone(x=[(P+w)[0]],y=[(P+w)[1]],z=[(P+w)[2]],u=[w[0]],v=[w[1]],w=[w[2]],
                    anchor="tip",sizemode="absolute",sizeref=.13,showscale=False,
                    colorscale=[[0,"#E45756"],[1,"#E45756"]],hoverinfo="skip"),
            go.Scatter(x=[np.degrees(theta)],y=[normal_curvature(theta)],mode="markers",
                       marker=dict(size=12,color="#E45756"),showlegend=False)]


def build_figure() -> go.Figure:
    """곡면과 접평면의 주방향, 법곡률 그래프를 표시한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],horizontal_spacing=.1,
                      subplot_titles=("p=(1,0,1)의 접평면과 주방향","Euler 공식: κₙ(θ)=cos(2θ)/√2"))
    u,v=np.meshgrid(np.linspace(.4,2.2,81),np.linspace(-np.pi+.001,np.pi-.001,101))
    xyz=surface(u,v)
    fig.add_trace(go.Surface(x=xyz[...,0],y=xyz[...,1],z=xyz[...,2],opacity=.35,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],showscale=False,hoverinfo="skip"),row=1,col=1)
    a,b=np.meshgrid([-.7,.7],[-.7,.7])
    plane=P+a[...,None]*E1+b[...,None]*E2
    fig.add_trace(go.Surface(x=plane[...,0],y=plane[...,1],z=plane[...,2],opacity=.3,
                            colorscale=[[0,"#F2A541"],[1,"#F2A541"]],showscale=False,name="접평면 x+z=2",showlegend=True),row=1,col=1)
    for vector,name,color in ((E1,"e₁: κ₁=1/√2","#7040A0"),(E2,"e₂: κ₂=−1/√2","#239B56")):
        fig.add_trace(line(np.array([P,P+vector]),name,color),row=1,col=1)
    fig.add_trace(go.Scatter3d(x=[1],y=[0],z=[1],mode="markers+text",text=["p"],
                              marker=dict(size=5,color="#222222"),showlegend=False),row=1,col=1)
    angles=np.linspace(0,np.pi,361)
    fig.add_trace(go.Scatter(x=np.degrees(angles),y=normal_curvature(angles),mode="lines",
                            line=dict(color="#4C78A8",width=4),name="법곡률"),row=1,col=2)
    fig.add_trace(go.Scatter(x=[np.degrees(THETA_W)],y=[normal_curvature(THETA_W)],mode="markers+text",
                            text=["w: √2/6"],textposition="top right",marker=dict(size=10,color="#222222"),showlegend=False),row=1,col=2)
    indices=list(range(len(fig.data),len(fig.data)+3))
    for i,trace in enumerate(moving_traces(THETA_W)):
        fig.add_trace(trace,row=1,col=2 if i==2 else 1)
    parameters=np.sort(np.r_[np.linspace(0,np.pi,25),THETA_W])
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(t)),traces=indices) for i,t in enumerate(parameters)]
    fig.update_xaxes(title_text="e₁와 이루는 각 θ (도)",range=[0,180],autorange=False,row=1,col=2)
    fig.update_yaxes(title_text="법곡률",range=[-.85,.85],autorange=False,row=1,col=2)
    fig.update_layout(title=dict(text="2018학년도 1차 B 5번 · 주곡률과 법곡률"
                                 "<br><sup>κ₁=1/√2, κ₂=−1/√2 · κ(w)=(2/3)κ₁+(1/3)κ₂=√2/6</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=25,r=30,t=115,b=180),
                      scene=dict(xaxis=dict(title="x",range=[-2.4,2.4],autorange=False),
                                 yaxis=dict(title="y",range=[-2.4,2.4],autorange=False),
                                 zaxis=dict(title="z",range=[-.2,2.8],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=1,y=1,z=3/4.8),uirevision="camera",
                                 camera=dict(eye=dict(x=1.6,y=1.6,z=1.2))),legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=int(np.argmin(abs(parameters-THETA_W))),y=-.07,currentvalue=dict(prefix="θ = "),steps=[
                          dict(label="w" if np.isclose(t,THETA_W) else f"{np.degrees(t):.1f}°",method="animate",args=[[str(i)],
                               dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i,t in enumerate(parameters)])])
    fig.add_annotation(text="법선 U=(1,0,1)/√2 기준. w의 주방향 성분 제곱은 2/3, 1/3이며 합은 1입니다.",
                       xref="paper",yref="paper",x=.5,y=-.35,showarrow=False)
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
