r"""2021학년도 1차 A 4번: 구면 법선과 종법선의 일정한 각.

바깥 단위법선 n=gamma를 택한다. gamma·T=0, gamma·N=-1/kappa,
gamma·B=1/2이므로 1=1/kappa²+1/4 → kappa=2/sqrt(3).
(gamma·B)'=-tau gamma·N=tau/kappa=0 → tau=0.
대표 곡선 gamma(s)=(r cos(s/r),r sin(s/r),1/2), r=sqrt(3)/2.
이는 단위속력이며 0≤s≤1 구간을 강조한다. 전체 원은 참고용 점선이다.
T=(-sin,cos,0), N=(-cos,-sin,0), B=(0,0,1), n=-rN+B/2.
따라서 B와 n의 각은 60도. 곡선은 강체회전 등으로 달라질 수 있다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2021_a_q4_spherical_circle.py
저장: 위 명령에 --output output/exam_2021_a_q4.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

RADIUS=np.sqrt(3)/2


# 수학적 정의와 계산
def gamma(s: np.ndarray | float) -> np.ndarray:
    """단위 구면 위 단위속력 원의 좌표."""
    s=np.asarray(s); t=s/RADIUS
    return np.stack((RADIUS*np.cos(t),RADIUS*np.sin(t),np.full_like(t,.5)),axis=-1)


def frame(s: float) -> tuple[np.ndarray, ...]:
    """T,N,B와 구면의 바깥 단위법선 n."""
    t=s/RADIUS
    return (np.array([-np.sin(t),np.cos(t),0]),np.array([-np.cos(t),-np.sin(t),0]),
            np.array([0.,0.,1.]),gamma(s))


# 이 문항의 시각화 구성
def moving_traces(s: float) -> list:
    """관찰점과 실제 길이 1인 벡터, 60도 각을 표시한다."""
    p=gamma(s); T,N,B,n=frame(s)
    traces=[go.Scatter3d(x=[p[0]],y=[p[1]],z=[p[2]],mode="markers",marker=dict(size=6,color="#222222"),showlegend=False)]
    for vector,label,color in ((N,"주법선 N","#239B56"),(B,"종법선 B","#4C78A8"),(n,"구면 법선 n","#E45756")):
        end=p+vector
        traces.append(go.Scatter3d(x=[p[0],end[0]],y=[p[1],end[1]],z=[p[2],end[2]],mode="lines",
                                  line=dict(color=color,width=6),name=label))
        traces.append(go.Cone(x=[end[0]],y=[end[1]],z=[end[2]],u=[vector[0]],v=[vector[1]],w=[vector[2]],
                              anchor="tip",sizemode="absolute",sizeref=.12,showscale=False,
                              colorscale=[[0,color],[1,color]],hoverinfo="skip"))
    angle=np.linspace(0,np.pi/3,41)
    arc=p+.3*(np.cos(angle)[:,None]*B-np.sin(angle)[:,None]*N)
    traces.append(go.Scatter3d(x=arc[:,0],y=arc[:,1],z=arc[:,2],mode="lines",line=dict(color="#222222",width=3),showlegend=False))
    return traces


def build_figure() -> go.Figure:
    """구면 위 관찰점과 직교 성분의 관계를 표시한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],horizontal_spacing=.1,
                      subplot_titles=("구면 위 작은 원 · 실선은 0≤s≤1","이동하는 (N,B) 기저에서 n의 성분은 일정"))
    u,v=np.meshgrid(np.linspace(0,np.pi,61),np.linspace(0,2*np.pi,81))
    fig.add_trace(go.Surface(x=np.sin(u)*np.cos(v),y=np.sin(u)*np.sin(v),z=np.cos(u),opacity=.18,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],showscale=False,hoverinfo="skip"),row=1,col=1)
    for ss,name,dash,width in ((np.linspace(0,2*np.pi*RADIUS,401),"참고: 전체 원","dash",3),
                               (np.linspace(0,1,201),"γ: 문제의 구간","solid",7)):
        p=gamma(ss)
        fig.add_trace(go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",line=dict(color="#7040A0",width=width,dash=dash),name=name),row=1,col=1)
    fig.add_trace(go.Scatter(x=[0,-RADIUS,-RADIUS,0],y=[0,0,.5,0],mode="lines+markers",
                            line=dict(color="#E45756",width=4),marker=dict(size=6),showlegend=False),row=1,col=2)
    fig.add_trace(go.Scatter(x=[-RADIUS/2,-RADIUS-.12,-RADIUS/2],y=[-.12,.25,.38],mode="text",
                            text=["−1/κ=−√3/2","1/2","||n||=1"],showlegend=False),row=1,col=2)
    indices=list(range(len(fig.data),len(fig.data)+8))
    for trace in moving_traces(0):
        fig.add_trace(trace,row=1,col=1)
    parameters=np.linspace(0,1,41)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(s)),traces=indices) for i,s in enumerate(parameters)]
    fig.update_xaxes(title_text="N 성분",range=[-1.3,.4],autorange=False,row=1,col=2)
    fig.update_yaxes(title_text="B 성분",range=[-.4,1.2],autorange=False,scaleanchor="x",scaleratio=1,row=1,col=2)
    fig.update_layout(title=dict(text="2021학년도 1차 A 4번 · B·n=1/2인 구면곡선"
                                 "<br><sup>비틀림 a(s)=0 · 곡률 b(s)=2/√3 · B와 n의 각=60°</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=25,r=30,t=115,b=180),
                      scene=dict(xaxis=dict(title="x",range=[-1.2,2],autorange=False),
                                 yaxis=dict(title="y",range=[-1.2,2],autorange=False),
                                 zaxis=dict(title="z",range=[-1.2,1.8],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=1,y=1,z=3/3.2),uirevision="camera",
                                 camera=dict(eye=dict(x=1.6,y=1.6,z=1.2))),legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=0,y=-.07,currentvalue=dict(prefix="호길이 s = "),steps=[
                          dict(label=f"{s:.3f}",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i,s in enumerate(parameters)])])
    fig.add_annotation(text="n=−N/κ+B/2 → 1=1/κ²+1/4. (B·n)′=τ/κ=0 → τ=0. 법선은 바깥 방향을 사용합니다.",
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
