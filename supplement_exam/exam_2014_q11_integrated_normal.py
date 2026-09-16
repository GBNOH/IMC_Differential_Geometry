r"""2014학년도 11번: 주법선벡터를 적분하여 얻는 곡선.

단위속력곡선 alpha의 곡률은 1, 비틀림은 상수 tau이다.
omega=sqrt(1+tau²)라 두고 대표 원나선을
alpha(s)=(cos(omega s)/omega²,sin(omega s)/omega²,tau s/omega)로 택한다.
N(s)=(-cos(omega s),-sin(omega s),0)이므로
beta(s)=∫₀ˢN(t)dt=(-sin(omega s),cos(omega s)-1,0)/omega.
beta는 반지름 1/omega인 원으로, beta'=N, kappa_beta=omega, tau_beta=0이다.
따라서 kappa_beta+tau_beta=sqrt(1+tau²).
Frenet 공식으로도 beta''=-T+tau B, beta'''=-(1+tau²)N이므로 같은 결과를 얻는다.
화살표는 실제 길이 1이며 두 그림의 좌표는 평행이동 없이 표시한다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2014_q11_integrated_normal.py
    python .\supplement_exam\exam_2014_q11_integrated_normal.py --tau 1 --output output/exam_2014_q11.html --no-show
"""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def alpha(s: np.ndarray | float, tau: float) -> np.ndarray:
    """곡률 1, 비틀림 tau인 단위속력 원나선."""
    s=np.asarray(s)
    w=np.sqrt(1+tau*tau)
    return np.stack((np.cos(w*s)/w**2,np.sin(w*s)/w**2,tau*s/w),axis=-1)


def principal_normal(s: np.ndarray | float, tau: float) -> np.ndarray:
    """원곡선의 단위 주법선 N(s)."""
    s=np.asarray(s)
    w=np.sqrt(1+tau*tau)
    return np.stack((-np.cos(w*s),-np.sin(w*s),np.zeros_like(s)),axis=-1)


def beta(s: np.ndarray | float, tau: float) -> np.ndarray:
    """N의 0부터 s까지 적분. beta(0)=0이다."""
    s=np.asarray(s)
    w=np.sqrt(1+tau*tau)
    return np.stack((-np.sin(w*s)/w,(np.cos(w*s)-1)/w,np.zeros_like(s)),axis=-1)


# 이 문항의 시각화 구성
def moving_traces(s: float, tau: float) -> list:
    """두 대응점에서 같은 방향의 단위벡터를 표시한다."""
    result=[]
    vector=principal_normal(s,tau)
    for point,label in ((alpha(s,tau),"Nα(s)"),(beta(s,tau),"β′(s)=Nα(s)")):
        endpoint=point+vector
        result.append(go.Scatter3d(x=[point[0]],y=[point[1]],z=[point[2]],mode="markers",
                                  marker=dict(size=6,color="#222222"),showlegend=False))
        result.append(go.Scatter3d(x=[point[0],endpoint[0]],y=[point[1],endpoint[1]],z=[point[2],endpoint[2]],
                                  mode="lines",line=dict(color="#E45756",width=7),name=label))
        result.append(go.Cone(x=[endpoint[0]],y=[endpoint[1]],z=[endpoint[2]],u=[vector[0]],v=[vector[1]],w=[vector[2]],
                              anchor="tip",sizemode="absolute",sizeref=.15,showscale=False,
                              colorscale=[[0,"#E45756"],[1,"#E45756"]],hoverinfo="skip"))
    return result


def build_figure(tau: float = 1.0) -> go.Figure:
    """한 회전 동안 원곡선과 적분곡선의 대응을 보여 준다."""
    if not np.isfinite(tau):
        raise ValueError("tau는 유한한 실수여야 합니다.")
    w=np.sqrt(1+tau*tau)
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="scene")]],horizontal_spacing=.05,
                      subplot_titles=(f"α: κ=1, τ={tau:g}",f"β: 반지름 {1/w:.4f}, κ={w:.4f}, τ=0"))
    s=np.linspace(0,2*np.pi/w,501)
    for col,points,name in ((1,alpha(s,tau),"원곡선 α"),(2,beta(s,tau),"적분곡선 β")):
        fig.add_trace(go.Scatter3d(x=points[:,0],y=points[:,1],z=points[:,2],mode="lines",
                                  line=dict(color="#7040A0",width=6),name=name),row=1,col=col)
    fig.add_trace(go.Scatter3d(x=[0],y=[0],z=[0],mode="markers+text",text=["β(0)=0"],
                              textposition="top center",marker=dict(size=4,color="#239B56"),showlegend=False),row=1,col=2)
    indices=list(range(len(fig.data),len(fig.data)+6))
    for i,trace in enumerate(moving_traces(0,tau)):
        fig.add_trace(trace,row=1,col=1 if i<3 else 2)
    parameters=np.linspace(0,2*np.pi/w,41)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(s),tau),traces=indices) for i,s in enumerate(parameters)]
    # 현재 점의 벡터가 이동해도 축 범위와 좌표 단위가 바뀌지 않도록 고정한다.
    all_points=np.vstack((alpha(parameters,tau),beta(parameters,tau),
                          alpha(parameters,tau)+principal_normal(parameters,tau),
                          beta(parameters,tau)+principal_normal(parameters,tau)))
    lower=all_points.min(axis=0)-.3
    upper=all_points.max(axis=0)+.3
    # data 모드는 이동하는 화살표의 경계에 따라 장면 비율을 재계산할 수 있다.
    # 고정 범위의 길이 비율을 사용해 프레임마다 동일한 좌표 축척을 유지한다.
    spans=upper-lower
    ratios=spans/np.max(spans)
    scene=dict(xaxis=dict(title="x",range=[lower[0],upper[0]],autorange=False),
               yaxis=dict(title="y",range=[lower[1],upper[1]],autorange=False),
               zaxis=dict(title="z",range=[lower[2],upper[2]],autorange=False),
               aspectmode="manual",aspectratio=dict(x=ratios[0],y=ratios[1],z=ratios[2]),
               uirevision="camera",camera=dict(eye=dict(x=1.5,y=1.5,z=1.2)))
    fig.update_layout(title=dict(text="2014학년도 11번 · 주법선벡터의 적분"
                                 f"<br><sup>β′=Nα · κβ+τβ=√(1+τ²)={w:.4f}</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=20,r=20,t=110,b=180),
                      scene=scene,scene2=scene,legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=0,y=-.07,currentvalue=dict(prefix="호길이 매개변수 s = "),steps=[
                          dict(label=f"{s:.2f}",method="animate",args=[[str(i)],
                               dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,s in enumerate(parameters)])])
    fig.add_annotation(text="β″=−T+τB → ||β″||=√(1+τ²). β는 z=0 평면의 원이므로 τβ=0.",
                       xref="paper",yref="paper",x=.5,y=-.34,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def parse_args() -> argparse.Namespace:
    """비틀림과 출력 옵션을 읽는다."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tau",type=float,default=1.0,help="원곡선의 상수 비틀림 (기본값 1)")
    parser.add_argument("--output",type=Path,help="HTML 저장 경로")
    parser.add_argument("--no-show",action="store_true",help="브라우저 창을 열지 않음")
    return parser.parse_args()


def main() -> None:
    """그림을 생성하고 HTML 저장 또는 화면 표시를 실행한다."""
    args=parse_args()
    figure=build_figure(args.tau)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        figure.write_html(args.output,include_plotlyjs=True)
        print(f"저장 완료: {args.output.resolve()}")
    if not args.no_show:
        figure.show()


if __name__ == "__main__":
    main()
