"""2024학년도 1차 B 7번: 타원면의 가우스곡률과 가우스 사상.

X(u,v)=(2sin u,cos u cos v,cos u sin v).
0<u<asin(2/√5), 0<v<π/3. 경계는 시각화를 위해 포함한다.
D=sin²u+4cos²u, K=4/D², dA=cos u √D du dv.
단위법선 n=(sin u,2cos u cos v,2cos u sin v)/√D.
K(√2,1/2,1/2)=16/25.
∫∫K dA=(π/3)[sin u/√D]_0^asin(2/√5)=π/(3√2).
단위구 위 가우스 사상의 넓이도 (π/3)·(1/√2)이다.
필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2024_b_q7_gauss_map.py
저장 옵션: --output output/exam_2024_b_q7.html --no-show
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

UMAX=np.arcsin(2/np.sqrt(5))


def surface(u,v):
    u,v=np.broadcast_arrays(u,v)
    return np.stack((2*np.sin(u),np.cos(u)*np.cos(v),np.cos(u)*np.sin(v)),axis=-1)


def normal(u,v):
    p=surface(u,v)*np.array([.5,2,2])
    return p/np.linalg.norm(p,axis=-1,keepdims=True)


def curvature(u):
    return 4/(np.sin(u)**2+4*np.cos(u)**2)**2


def line(p,name,color):
    return go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",
        name=name,line=dict(color=color,width=6))


def moving(u):
    v=np.linspace(0,np.pi/3,101)
    p=surface(u,np.pi/4); n=normal(u,np.pi/4)
    return [line(surface(u,v),"선택한 단면","#222222"),
        line(normal(u,v),"대응하는 구면 단면","#222222"),
        line(np.array([p,p+.35*n]),"외향 단위법선 (0.35배)","#e45756"),
        line(np.array([[0,0,0],n]),"단위법선의 위치벡터","#e45756")]


def build_figure():
    fig=make_subplots(rows=1,cols=2,specs=[[{"type":"scene"},{"type":"scene"}]],
        subplot_titles=("타원면의 영역 M","단위구 위의 가우스 사상 n(M)"),horizontal_spacing=.06)
    u,v=np.meshgrid(np.linspace(0,UMAX,81),np.linspace(0,np.pi/3,71))
    for col,func in ((1,surface),(2,normal)):
        p=func(u,v)
        fig.add_trace(go.Surface(x=p[:,:,0],y=p[:,:,1],z=p[:,:,2],surfacecolor=curvature(u),
            colorscale="Viridis",cmin=.25,cmax=1.5625,showscale=col==2,
            colorbar=dict(title="원곡면 K",thickness=12),opacity=.9,
            customdata=curvature(u),hovertemplate="K=%{customdata:.4f}<extra></extra>"),row=1,col=col)
        for h in (0,UMAX):
            fig.add_trace(line(func(h,np.linspace(0,np.pi/3,101)),"영역 경계","#777777"),row=1,col=col)
        p=func(np.pi/4,np.pi/4)
        fig.add_trace(go.Scatter3d(x=[p[0]],y=[p[1]],z=[p[2]],mode="markers",name="주어진 점" if col==1 else "주어진 점의 상",
            marker=dict(size=6,color="#e45756")),row=1,col=col)
    ids=list(range(len(fig.data),len(fig.data)+4))
    for tr,col in zip(moving(np.pi/4),(1,2,1,2)):
        fig.add_trace(tr,row=1,col=col)
    values=np.sort(np.unique(np.r_[np.linspace(0,UMAX,31),np.pi/4]))
    fig.frames=[go.Frame(name=str(i),data=moving(u),traces=ids) for i,u in enumerate(values)]
    for col in (1,2):
        ranges=([-0.2,2.2],[-.2,1.2],[-.2,1.2]) if col==1 else ([-.2,1.2],)*3
        spans=np.array([b-a for a,b in ranges])
        scene=dict(aspectmode="manual",aspectratio=dict(zip("xyz",spans/spans.max())),
            camera=dict(eye=dict(x=1.6,y=1.6,z=1.2)),uirevision="fixed-camera")
        for axis,r in zip("xyz",ranges):
            scene[axis+"axis"]=dict(title=axis,range=r,autorange=False)
        fig.update_layout(**{("scene" if col==1 else "scene2"):scene})
    fig.update_layout(template="plotly_white",height=820,margin=dict(l=20,r=55,t=105,b=185),
        title=dict(x=.5,text="2024학년도 1차 B 7번 · 타원면과 가우스 사상"
            "<br><sup>K(√2,1/2,1/2)=16/25 · ∫∫M K dA = 넓이(n(M)) = π/(3√2)</sup>"),
        showlegend=False,sliders=[dict(active=int(np.where(values==np.pi/4)[0][0]),y=-.07,
            currentvalue=dict(prefix="u = "),steps=[dict(label=f"{u:.3f}",method="animate",
            args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i,u in enumerate(values)])],
        annotations=list(fig.layout.annotations)+[dict(x=.5,y=-.27,xref="paper",yref="paper",showarrow=False,
            text="검정: 대응하는 단면 · 빨강: 외향 법선(왼쪽 0.35배) / 단위법선 위치벡터(오른쪽)"
            "<br>구면 영역: 0 ≤ nₓ ≤ 1/√2, 0 ≤ v ≤ π/3 · 경계는 설명을 위해 포함하여 표시")])
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
