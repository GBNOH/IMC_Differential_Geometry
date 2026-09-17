"""2025학년도 1차 B 2번: 카디오이드의 길이와 전곡률.

r=1-cos(θ-π/3), α=(r cosθ,r sinθ), 0≤θ≤2π.
속력=2|sin((θ-π/3)/2)|, 길이=8.
θ=π/3에서 α'=0. 이 첨점에서 단위접선과 곡률은 정의되지 않는다.
정칙 부분에서 κ=3/[4|sin((θ-π/3)/2)|], κ ds/dθ=3/2.
첨점을 제외한 이상적분 ∫κ ds=3π. 첨점의 회전각은 더하지 않는다.
필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2025_b_q2_cardioid.py
저장 옵션: --output output/exam_2025_b_q2.html --no-show
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CUSP=np.pi/3


def curve(theta):
    theta=np.asarray(theta)
    r=1-np.cos(theta-CUSP)
    return np.stack((r*np.cos(theta),r*np.sin(theta)),axis=-1)


def velocity(theta):
    r=1-np.cos(theta-CUSP); dr=np.sin(theta-CUSP)
    return np.array([dr*np.cos(theta)-r*np.sin(theta),dr*np.sin(theta)+r*np.cos(theta)])


def length(theta):
    theta=np.asarray(theta)
    c=np.cos(CUSP/2)
    return np.where(theta<=CUSP,4*(np.cos((theta-CUSP)/2)-c),
                    4*(1-c)+4*(1-np.cos((theta-CUSP)/2)))


def moving(theta):
    path=curve(np.linspace(0,theta,301)); p=curve(theta)
    if abs(theta-CUSP)<1e-10:
        tangent=np.full((2,2),np.nan)
    else:
        d=velocity(theta); d/=np.linalg.norm(d)
        tangent=np.array([p,p+.55*d])
    return [go.Scatter(x=path[:,0],y=path[:,1],mode="lines",name="지나온 구간",
                line=dict(color="#4c78a8",width=6)),
            go.Scatter(x=[p[0]],y=[p[1]],mode="markers",name="현재 점",marker=dict(size=10,color="#222222")),
            go.Scatter(x=tangent[:,0],y=tangent[:,1],mode="lines+markers",name="진행 방향 T (0.55배)",
                line=dict(color="#e45756",width=5),marker=dict(size=[0,9],symbol="arrow",angleref="previous")),
            go.Scatter(x=[theta],y=[length(theta)],mode="markers",marker=dict(size=10,color="#4c78a8"),showlegend=False),
            go.Scatter(x=[theta],y=[1.5*theta],mode="markers",marker=dict(size=10,color="#8056b3"),showlegend=False)]


def status(theta):
    cusp=abs(theta-CUSP)<1e-10
    detail="첨점: 속력=0, 단위접선·곡률 정의되지 않음" if cusp else f"속력={np.linalg.norm(velocity(theta)):.3f} · κ={3/(4*abs(np.sin((theta-CUSP)/2))):.3f}"
    return dict(x=.5,y=-.32,xref="paper",yref="paper",showarrow=False,
        text=f"θ={theta/np.pi:.3f}π · {detail}<br>누적 길이={float(length(theta)):.4f} · 누적 곡률 적분={1.5*theta/np.pi:.3f}π")


def build_figure():
    fig=make_subplots(rows=1,cols=2,horizontal_spacing=.13,
        subplot_titles=("카디오이드와 진행 방향","θ=0부터의 누적 길이와 곡률 적분"))
    theta=np.linspace(0,2*np.pi,1201); p=curve(theta)
    fig.add_trace(go.Scatter(x=p[:,0],y=p[:,1],mode="lines",name="전체 곡선",line=dict(color="#bbbbbb",width=3)),row=1,col=1)
    fig.add_trace(go.Scatter(x=[0],y=[0],mode="markers+text",text=["첨점 θ=π/3"],textposition="top right",
        marker=dict(size=10,symbol="x",color="#e45756"),showlegend=False),row=1,col=1)
    fig.add_trace(go.Scatter(x=theta,y=length(theta),name="누적 길이 (전체 8)",line=dict(color="#4c78a8",width=3)),row=1,col=2)
    fig.add_trace(go.Scatter(x=theta,y=1.5*theta,name="누적 ∫κ ds (전체 3π)",line=dict(color="#8056b3",width=3)),row=1,col=2)
    ids=list(range(4,9))
    for tr,col in zip(moving(0),(1,1,1,2,2)):
        fig.add_trace(tr,row=1,col=col)
    values=np.linspace(0,2*np.pi,73)
    fig.frames=[go.Frame(name=str(i),data=moving(t),traces=ids,layout=dict(annotations=list(fig.layout.annotations)+[status(t)])) for i,t in enumerate(values)]
    fig.add_vline(x=CUSP,line_dash="dot",line_color="#e45756",row=1,col=2)
    fig.update_xaxes(title="x",range=[-2.7,1.7],autorange=False,constrain="domain",row=1,col=1)
    fig.update_yaxes(title="y",range=[-2.7,1.7],autorange=False,scaleanchor="x",scaleratio=1,row=1,col=1)
    fig.update_xaxes(title="θ",range=[-.15,2*np.pi+.15],autorange=False,tickvals=[0,CUSP,np.pi,2*np.pi],ticktext=["0","π/3","π","2π"],row=1,col=2)
    fig.update_yaxes(title="누적 값",range=[-.3,10],autorange=False,row=1,col=2)
    fig.update_layout(template="plotly_white",height=820,margin=dict(l=45,r=30,t=115,b=185),
        title=dict(x=.5,text="2025학년도 1차 B 2번 · 카디오이드의 길이와 전곡률"
            "<br><sup>r=1−cos(θ−π/3) · L=8 · ∫κ ds=3π (첨점의 회전각을 더하지 않은 적분)</sup>"),
        legend=dict(orientation="h",y=-.23),uirevision="fixed-view",
        sliders=[dict(active=0,y=-.07,currentvalue=dict(prefix="θ / π = "),steps=[
            dict(label=f"{t/np.pi:.3f}",method="animate",args=[[str(i)],dict(mode="immediate",
                frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i,t in enumerate(values)])])
    fig.add_annotation(status(0))
    return fig


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--no-show",action="store_true")
    args=parser.parse_args(); fig=build_figure()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        fig.write_html(args.output,include_plotlyjs=True)
        print(args.output.resolve())
    if not args.no_show:
        fig.show()


if __name__=="__main__":
    main()
