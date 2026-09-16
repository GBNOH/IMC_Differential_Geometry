"""2025학년도 1차 A 9번: 카테노이드의 접평면과 곡률.

X(u,v)=(1+2u,2cosh(u)cos(v),2cosh(u)sin(v)).
P=X(0,π/4)=(1,√2,√2). 접평면: y+z=2√2.
법선은 Xu×Xv 방향: n=(0,-1/√2,-1/√2) at P.
E=G=4, F=0, L=-2, M=0, N=2.
주곡률 k1=-1/2, k2=1/2, K=-1/4, H=0.
법곡률 kn(θ)=k1 cos²θ+k2 sin²θ=-cos(2θ)/2.
전체 곡면에서도 주곡률은 ±1/(2cosh²u)이므로 H=0이다.
필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2025_a_q9_catenoid.py
저장 옵션: --output output/exam_2025_a_q9.html --no-show
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

P=np.array([1.,np.sqrt(2),np.sqrt(2)])
E1=np.array([1.,0,0])
E2=np.array([0.,-1/np.sqrt(2),1/np.sqrt(2)])
NORMAL=np.cross(E1,E2)


def surface(u,v):
    u,v=np.broadcast_arrays(u,v)
    return np.stack((1+2*u,2*np.cosh(u)*np.cos(v),2*np.cosh(u)*np.sin(v)),axis=-1)


def normal_curvature(theta):
    return -.5*np.cos(2*np.asarray(theta))


def line(p,name,color,width=5):
    return go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",name=name,
        line=dict(color=color,width=width))


def moving(theta):
    tangent=np.cos(theta)*E1+np.sin(theta)*E2
    return [line(np.array([P-1.1*tangent,P+1.1*tangent]),"선택한 접선 방향","#222222",7),
        go.Scatter(x=[theta*180/np.pi],y=[normal_curvature(theta)],mode="markers",
            marker=dict(size=12,color="#222222"),showlegend=False)]


def build_figure():
    fig=make_subplots(rows=1,cols=2,specs=[[{"type":"scene"},{"type":"xy"}]],
        column_widths=[.62,.38],horizontal_spacing=.09,
        subplot_titles=("카테노이드와 P에서의 접평면","P에서 방향에 따른 법곡률"))
    u,v=np.meshgrid(np.linspace(-1,1,81),np.linspace(0,2*np.pi,121))
    p=surface(u,v)
    fig.add_trace(go.Surface(x=p[:,:,0],y=p[:,:,1],z=p[:,:,2],opacity=.45,
        colorscale=[[0,"#9bc4df"],[1,"#9bc4df"]],showscale=False,hoverinfo="skip",name="카테노이드"),row=1,col=1)
    a,b=np.meshgrid(np.linspace(-1.4,1.4,15),np.linspace(-1.4,1.4,15))
    patch=P+a[:,:,None]*E1+b[:,:,None]*E2
    fig.add_trace(go.Surface(x=patch[:,:,0],y=patch[:,:,1],z=patch[:,:,2],opacity=.35,
        colorscale=[[0,"#f2cc72"],[1,"#f2cc72"]],showscale=False,hoverinfo="skip"),row=1,col=1)
    fig.add_trace(line(surface(np.linspace(-1,1,201),np.pi/4),"자오선: k₁=−1/2","#e45756"),row=1,col=1)
    fig.add_trace(line(surface(0,np.linspace(0,2*np.pi,241)),"평행원: k₂=1/2","#54a24b"),row=1,col=1)
    fig.add_trace(line(np.array([P,P+NORMAL]),"단위법선 n","#8056b3"),row=1,col=1)
    fig.add_trace(go.Scatter3d(x=[P[0]],y=[P[1]],z=[P[2]],mode="markers+text",text=["P"],
        marker=dict(size=6,color="#222222"),showlegend=False),row=1,col=1)
    angles=np.linspace(0,np.pi,361)
    fig.add_trace(go.Scatter(x=angles*180/np.pi,y=normal_curvature(angles),mode="lines",
        name="κn(θ)=−cos(2θ)/2",line=dict(color="#8056b3",width=4)),row=1,col=2)
    fig.add_trace(go.Scatter(x=[0,45,90,135,180],y=[-.5,0,.5,0,-.5],mode="markers",
        marker=dict(size=8,color="#8056b3"),showlegend=False),row=1,col=2)
    ids=[len(fig.data),len(fig.data)+1]
    tr,pt=moving(0)
    fig.add_trace(tr,row=1,col=1); fig.add_trace(pt,row=1,col=2)
    values=np.linspace(0,np.pi,37)
    fig.frames=[go.Frame(name=str(i),data=moving(t),traces=ids) for i,t in enumerate(values)]
    fig.update_xaxes(title="접선 방향 θ (도)",range=[-5,185],autorange=False,row=1,col=2)
    fig.update_yaxes(title="법곡률 κn",range=[-.65,.65],autorange=False,row=1,col=2)
    fig.update_layout(template="plotly_white",height=840,margin=dict(l=20,r=35,t=110,b=190),
        title=dict(x=.5,text="2025학년도 1차 A 9번 · 카테노이드의 접평면과 곡률"
            "<br><sup>P=(1,√2,√2) · 접평면 y+z=2√2 · K=−1/4 · H=0</sup>"),
        scene=dict(xaxis=dict(title="x",range=[-1.5,3.5],autorange=False),
            yaxis=dict(title="y",range=[-3.5,3.5],autorange=False),
            zaxis=dict(title="z",range=[-3.5,3.5],autorange=False),
            aspectmode="manual",aspectratio=dict(x=5/7,y=1,z=1),
            camera=dict(eye=dict(x=1.7,y=1.7,z=1.1)),uirevision="fixed-camera"),
        legend=dict(orientation="h",y=-.26),
        sliders=[dict(active=0,y=-.07,currentvalue=dict(prefix="θ (도) = "),steps=[
            dict(label=f"{t*180/np.pi:.0f}",method="animate",args=[[str(i)],dict(mode="immediate",
                frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i,t in enumerate(values)])])
    fig.add_annotation(x=.5,y=-.37,xref="paper",yref="paper",showarrow=False,
        text="θ=0°: 자오선 방향 · θ=90°: 평행원 방향 · θ=45°,135°: 법곡률 0"
        "<br>H=(k₁+k₂)/2=0: 두 주곡률이 상쇄되는 극소곡면")
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
