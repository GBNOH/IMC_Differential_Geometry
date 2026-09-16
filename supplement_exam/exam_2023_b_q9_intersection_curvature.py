"""2023학년도 1차 B 9번: 교선의 법곡률과 측지곡률.

M: z=x²-y², N: x+y+z=1.
p를 지나는 교선 가지 γ(t)=(cosh t-1/2,sinh t+1/2,1-exp t).
위쪽 단위법선 n=(-2x,2y,1)/√(4x²+4y²+1)을 사용한다.
곡률벡터 A=dT/ds=γ''/v²-γ'(γ'·γ'')/v⁴.
법곡률 kn=A·n, 측지곡률 크기 kg=|A-kn n|.
p=γ(0): kn=-1/√3, kg=1/(2√6), κ=√6/4.
법선 방향을 반대로 정하면 kn의 부호가 반대가 된다.
필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2023_b_q9_intersection_curvature.py
저장 옵션: --output output/exam_2023_b_q9.html --no-show
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go


def curve(t):
    t=np.asarray(t)
    return np.stack((np.cosh(t)-.5,np.sinh(t)+.5,1-np.exp(t)),axis=-1)


def geometry(t):
    p=curve(t)
    d=np.array([np.sinh(t),np.cosh(t),-np.exp(t)])
    dd=np.array([np.cosh(t),np.sinh(t),-np.exp(t)])
    v2=d@d
    tangent=d/np.sqrt(v2)
    normal=np.array([-2*p[0],2*p[1],1.])
    normal/=np.linalg.norm(normal)
    a=dd/v2-d*(d@dd)/v2**2
    kn=a@normal
    return p,tangent,normal,a,kn,a-kn*normal


def line(points,name,color,width=5):
    return go.Scatter3d(x=points[:,0],y=points[:,1],z=points[:,2],
        mode="lines",name=name,line=dict(color=color,width=width))


def moving(t):
    p,T,n,a,kn,g=geometry(t)
    traces=[]
    for vec,name,color in ((a,"곡률벡터 dT/ds","#222222"),
        (kn*n,"법선 성분 κn n","#e45756"),(g,"접평면 성분","#f2a900")):
        trace=line(np.array([p,p+2*vec]),name,color,8)
        trace.mode="lines+markers"
        trace.marker=dict(size=[0,4],color=color)
        traces.append(trace)
    traces.append(line(np.array([p,p+.7*n]),"위쪽 단위법선 n","#54a24b"))
    traces.append(go.Scatter3d(x=[p[0]],y=[p[1]],z=[p[2]],mode="markers",
        marker=dict(size=6,color="#8056b3"),name="선택한 점"))
    q=np.linspace(-.55,.55,9)
    u,v=np.meshgrid(q,q)
    patch=p+u[:,:,None]*T+v[:,:,None]*np.cross(n,T)
    traces.append(go.Surface(x=patch[:,:,0],y=patch[:,:,1],z=patch[:,:,2],
        opacity=.25,colorscale=[[0,"#f2a900"],[1,"#f2a900"]],showscale=False,
        name="접평면",hoverinfo="skip"))
    return traces


def annotation(t):
    _,_,_,a,kn,g=geometry(t)
    return dict(x=.5,y=-.24,xref="paper",yref="paper",showarrow=False,
        text=f"t={t:.2f} · κ={np.linalg.norm(a):.5f} · κn={kn:.5f} · |κg|={np.linalg.norm(g):.5f}"
        "<br>t=0: p=(1/2,1/2,0), κn=−1/√3, |κg|=1/(2√6) · κ²=κn²+κg²")


def build_figure():
    fig=go.Figure()
    x,y=np.meshgrid(np.linspace(-.7,1.6,65),np.linspace(-.7,1.7,65))
    for z,name,color,opacity in ((x*x-y*y,"M: z=x²−y²","#4c78a8",.45),
                                (1-x-y,"N: x+y+z=1","#aaaaaa",.23)):
        fig.add_trace(go.Surface(x=x,y=y,z=z,name=name,showlegend=True,
            opacity=opacity,colorscale=[[0,color],[1,color]],showscale=False,hoverinfo="skip"))
    fig.add_trace(line(curve(np.linspace(-.8,.8,301)),"교선 γ (p를 지나는 가지)","#8056b3",7))
    fig.add_traces(moving(0))
    values=np.linspace(-.7,.7,41)
    fig.frames=[go.Frame(name=str(i),data=moving(t),traces=list(range(3,9)),
        layout=dict(annotations=[annotation(t)])) for i,t in enumerate(values)]
    fig.update_layout(template="plotly_white",height=850,margin=dict(l=20,r=20,t=105,b=185),
        title=dict(x=.5,text="2023학년도 1차 B 9번 · 교선의 곡률벡터 분해"
            "<br><sup>곡률벡터와 두 성분은 모두 2배로 표시 · 노란 면은 선택한 점의 접평면</sup>"),
        scene=dict(xaxis=dict(title="x",range=[-1,2],autorange=False),
            yaxis=dict(title="y",range=[-1,2],autorange=False),
            zaxis=dict(title="z",range=[-3,3],autorange=False),
            aspectmode="manual",aspectratio=dict(x=.5,y=.5,z=1),
            camera=dict(eye=dict(x=1.7,y=1.7,z=1.1)),uirevision="fixed-camera"),
        legend=dict(orientation="h",y=1.02),annotations=[annotation(0)],
        sliders=[dict(active=20,y=-.07,currentvalue=dict(prefix="t = "),steps=[
            dict(label=f"{t:.2f}",method="animate",args=[[str(i)],dict(mode="immediate",
                frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i,t in enumerate(values)])])
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
