"""2024학년도 1차 A 4번: 지수함수 공간곡선의 접선과 곡률.

C: y=exp(ax), yz=b. α(t)=(t,exp(at),b exp(-at)).
P=(0,1,b), α'(0)=(1,a,-ab).
Q=(2√2,3,-1)=P+2√2 α'(0)에서 a=1/√2, b=1, a²+b²=3/2.
P에서 κ=|α'×α''|/|α'|³=√2/4, R=2√2.
주법선 N=(0,1,1)/√2, 접촉원 중심은 P+RN=(0,3,3).
필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2024_a_q4_exponential_curve.py
저장 옵션: --output output/exam_2024_a_q4.html --no-show
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

A = 1/np.sqrt(2)
B = 1.


def curve(t):
    t=np.asarray(t)
    return np.stack((t,np.exp(A*t),B*np.exp(-A*t)),axis=-1)


def geometry(t=0.):
    p=curve(t)
    d=np.array([1,A*np.exp(A*t),-A*B*np.exp(-A*t)])
    dd=np.array([0,A*A*np.exp(A*t),A*A*B*np.exp(-A*t)])
    tangent=d/np.linalg.norm(d)
    normal=dd-(dd@tangent)*tangent
    normal/=np.linalg.norm(normal)
    curvature=np.linalg.norm(np.cross(d,dd))/np.linalg.norm(d)**3
    return p,d,tangent,normal,curvature,p+normal/curvature


def line(points,name,color,width=5,dash=None):
    return go.Scatter3d(x=points[:,0],y=points[:,1],z=points[:,2],mode="lines",
        name=name,line=dict(color=color,width=width,dash=dash))


def build_figure():
    p,d,T,N,k,center=geometry()
    q=np.array([2*np.sqrt(2),3,-1])
    fig=go.Figure()
    fig.add_trace(line(curve(np.linspace(-1.65,1.65,501)),"곡선 C","#4c78a8",7))
    fig.add_trace(line(p+np.array([-.8,3.3])[:,None]*d,"P에서의 접선 (Q 통과)","#e45756",6))
    theta=np.linspace(0,2*np.pi,361)
    circle=center+(np.sin(theta)[:,None]*T-np.cos(theta)[:,None]*N)/k
    fig.add_trace(line(circle,"P에서의 접촉원","#f2a900",4))
    fig.add_trace(line(np.array([p,center]),"곡률반지름 R=2√2","#8056b3",4,"dash"))
    for point,name,color,label in ((p,"접촉점 P","#4c78a8","P=(0,1,1)"),
        (q,"주어진 점 Q","#e45756","Q=(2√2,3,−1)"),
        (center,"곡률중심","#8056b3","중심=(0,3,3)")):
        fig.add_trace(go.Scatter3d(x=[point[0]],y=[point[1]],z=[point[2]],
            mode="markers+text",text=[label],textposition="top center",name=name,
            marker=dict(size=6,color=color)))
    y,z=np.meshgrid(np.linspace(-.5,5.4,15),np.linspace(-1.5,5.4,15))
    fig.add_trace(go.Surface(x=np.zeros_like(y),y=y,z=z,opacity=.12,
        colorscale=[[0,"#54a24b"],[1,"#54a24b"]],showscale=False,showlegend=True,
        name="yz 평면 (x=0)",hoverinfo="skip"))
    fig.update_layout(template="plotly_white",height=850,margin=dict(l=20,r=20,t=105,b=115),
        title=dict(x=.5,text="2024학년도 1차 A 4번 · 공간곡선의 접선과 접촉원"
            "<br><sup>a=1/√2, b=1 → a²+b²=3/2 · P에서 κ=√2/4 ≈ 0.353553</sup>"),
        scene=dict(xaxis=dict(title="x",range=[-3.4,3.6],autorange=False),
            yaxis=dict(title="y",range=[-1.2,6.],autorange=False),
            zaxis=dict(title="z",range=[-1.6,6.],autorange=False),
            aspectmode="manual",aspectratio=dict(x=7/7.6,y=7.2/7.6,z=1),
            camera=dict(eye=dict(x=1.6,y=1.5,z=1.1)),uirevision="fixed-camera"),
        legend=dict(orientation="h",y=-.02),
        annotations=[dict(x=.5,y=-.15,xref="paper",yref="paper",showarrow=False,
            text="드래그: 회전 · 범례 클릭: 표시/숨김 · Q는 P에서의 접선 위의 점이며 곡선 위의 점은 아닙니다.")])
    return fig


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--no-show",action="store_true")
    args=parser.parse_args()
    fig=build_figure()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        fig.write_html(args.output,include_plotlyjs=True)
        print(args.output.resolve())
    if not args.no_show:
        fig.show()


if __name__=="__main__":
    main()
