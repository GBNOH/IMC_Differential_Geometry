r"""2017학년도 1차 B 5번: 반구와 원기둥의 교선 및 측지곡률.

S1: x²+y²+z²=4,z>0; S2: (x-1)²+y²=1,z>0.
gamma(theta)=(1+cos theta,sin theta,2sin(theta/2)), 0<theta<2π.
theta는 투영원의 중심 (1,0)에서 양의 x 방향과 이루는 각이다.
theta=π에서 q=(0,0,2), gamma'=(0,-1,0), gamma''=(1,0,-1/2).
이 점에서 속력 1, 속력의 도함수 0이므로 dT/ds=gamma''.
바깥 법선 U=(0,0,1), 법곡률벡터=(0,0,-1/2),
측지곡률벡터=(1,0,0). 따라서 |kappa_g|=1.
열린 구간의 양 끝점은 z=0이므로 곡선에 포함하지 않는다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2017_b_q5_sphere_cylinder.py
저장: 위 명령에 --output output/exam_2017_b_q5.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def gamma(theta: np.ndarray | float) -> np.ndarray:
    """0<theta<2π에 해당하는 교선 좌표를 반환한다."""
    t=np.asarray(theta)
    return np.stack((1+np.cos(t),np.sin(t),2*np.sin(t/2)),axis=-1)


def geometry(theta: float) -> tuple:
    """곡선의 단위접선, 곡면법선과 곡률벡터 분해를 반환한다."""
    t=theta
    first=np.array([-np.sin(t),np.cos(t),np.cos(t/2)])
    second=np.array([-np.cos(t),-np.sin(t),-.5*np.sin(t/2)])
    speed=np.linalg.norm(first)
    tangent=first/speed
    curvature=second/speed**2-first*np.dot(first,second)/speed**4
    normal=gamma(t)/2
    normal_part=np.dot(curvature,normal)*normal
    return tangent,normal,curvature,normal_part,curvature-normal_part


# 이 문항의 시각화 구성
def moving_traces(t: float) -> list:
    """교선과 투영원의 대응점 및 반지름, 높이선."""
    p=gamma(t)
    kg=np.linalg.norm(geometry(t)[4])
    return [go.Scatter3d(x=[p[0]],y=[p[1]],z=[p[2]],mode="markers",marker=dict(size=7,color="#E45756"),
                        name="현재 점",showlegend=False,hovertemplate=f"θ={t/np.pi:.3f}π<br>|κ_g|={kg:.5f}<extra></extra>"),
            go.Scatter3d(x=[p[0],p[0]],y=[p[1],p[1]],z=[0,p[2]],mode="lines",
                         line=dict(color="#777777",width=3,dash="dash"),showlegend=False),
            go.Scatter(x=[1,p[0]],y=[0,p[1]],mode="lines+markers",line=dict(color="#E45756",width=3),
                       marker=dict(size=8,color="#E45756"),showlegend=False)]


def build_figure() -> go.Figure:
    """반구·원기둥·교선과 각 theta의 정의를 표시한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],horizontal_spacing=.1,
                      subplot_titles=("반구와 원기둥의 교선 · q에서 곡률 분해","xy 투영: 중심 (1,0), 반지름 1"))
    a,b=np.meshgrid(np.linspace(0,np.pi/2-.001,65),np.linspace(0,2*np.pi,101))
    fig.add_trace(go.Surface(x=2*np.sin(a)*np.cos(b),y=2*np.sin(a)*np.sin(b),z=2*np.cos(a),opacity=.2,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],showscale=False,name="S₁: 반구",showlegend=True),row=1,col=1)
    t,z=np.meshgrid(np.linspace(0,2*np.pi,101),np.linspace(.001,2.2,41))
    fig.add_trace(go.Surface(x=1+np.cos(t),y=np.sin(t),z=z,opacity=.15,
                            colorscale=[[0,"#F2A541"],[1,"#F2A541"]],showscale=False,name="S₂: 원기둥",showlegend=True),row=1,col=1)
    ts=np.linspace(.001,2*np.pi-.001,801)
    p=gamma(ts)
    fig.add_trace(go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",line=dict(color="#7040A0",width=7),name="교선 γ"),row=1,col=1)
    fig.add_trace(go.Scatter(x=p[:,0],y=p[:,1],mode="lines",line=dict(color="#7040A0",width=4),showlegend=False),row=1,col=2)
    q=np.array([0.,0.,2.])
    _,_,k,kn,kg=geometry(np.pi)
    for vector,label,color in ((k,"q의 곡률벡터","#7040A0"),(kn,"법선 성분: 길이 1/2","#4C78A8"),(kg,"접평면 성분: 길이 1","#239B56")):
        end=q+vector
        fig.add_trace(go.Scatter3d(x=[q[0],end[0]],y=[q[1],end[1]],z=[q[2],end[2]],mode="lines+markers",
                                  line=dict(color=color,width=6),marker=dict(size=[0,4]),name=label),row=1,col=1)
    fig.add_trace(go.Scatter(x=[0,2],y=[0,0],mode="markers+text",text=["q의 투영 (θ=π)","θ=0,2π 제외"],
                            textposition="top center",marker=dict(size=8,color="#222222",symbol=["circle","circle-open"]),showlegend=False),row=1,col=2)
    indices=list(range(len(fig.data),len(fig.data)+3))
    for i,trace in enumerate(moving_traces(np.pi)):
        fig.add_trace(trace,row=1,col=2 if i==2 else 1)
    parameters=np.linspace(.05,2*np.pi-.05,41)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(t)),traces=indices) for i,t in enumerate(parameters)]
    fig.update_xaxes(title_text="x",range=[-.5,2.5],autorange=False,row=1,col=2)
    fig.update_yaxes(title_text="y",range=[-1.5,1.5],autorange=False,scaleanchor="x",scaleratio=1,row=1,col=2)
    fig.update_layout(title=dict(text="2017학년도 1차 B 5번 · 반구와 원기둥의 교선"
                                 "<br><sup>γ(θ)=(1+cosθ, sinθ, 2sin(θ/2)) · q=(0,0,2)에서 |κ_g|=1</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=25,r=30,t=115,b=180),
                      scene=dict(xaxis=dict(title="x",range=[-2.3,2.3],autorange=False),
                                 yaxis=dict(title="y",range=[-2.3,2.3],autorange=False),
                                 zaxis=dict(title="z",range=[-.2,2.4],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=1,y=1,z=2.6/4.6),uirevision="camera",
                                 camera=dict(eye=dict(x=1.6,y=1.6,z=1.3))),legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=20,y=-.07,currentvalue=dict(prefix="θ = "),steps=[
                          dict(label=f"{t/np.pi:.3f}π",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,t in enumerate(parameters)])])
    fig.add_annotation(text="q에 고정된 곡률벡터: dT/ds=(1,0,−1/2)=(0,0,−1/2)+(1,0,0). 빨간 점은 슬라이더로 이동합니다.",
                       xref="paper",yref="paper",x=.5,y=-.35,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def main() -> None:
    """그림을 생성하고 저장 또는 화면 표시를 실행한다."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,help="HTML 저장 경로")
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
