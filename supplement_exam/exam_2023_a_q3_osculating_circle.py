"""2023학년도 1차 A 3번: 평면곡선의 접촉원.

α(t)=(2 sin t-sin 2t, 2 cos t-cos 2t), 0≤t≤π.
정칙인 t>0에서 C=α+|α'|²/det(α',α'')*(-y',x'), R=|α'|³/|det|.
t=π/2: α=(2,1), C=(2/3,-1/3), R=4√2/3, κ=3√2/8.
t=0은 α'=0인 특이점이므로 접촉원 슬라이더에서 제외한다.
필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2023_a_q3_osculating_circle.py
저장 옵션: --output output/exam_2023_a_q3.html --no-show
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go


def curve(t):
    t = np.asarray(t)
    return np.stack((2*np.sin(t)-np.sin(2*t),2*np.cos(t)-np.cos(2*t)),axis=-1)


def geometry(t):
    p = curve(t)
    d = np.array([2*np.cos(t)-2*np.cos(2*t),-2*np.sin(t)+2*np.sin(2*t)])
    dd = np.array([-2*np.sin(t)+4*np.sin(2*t),-2*np.cos(t)+4*np.cos(2*t)])
    speed = np.linalg.norm(d)
    determinant = d[0]*dd[1]-d[1]*dd[0]
    if speed < 1e-12:
        raise ValueError("t=0에서는 정칙 접촉원을 정의하지 않습니다.")
    center = p+speed**2/determinant*np.array([-d[1],d[0]])
    radius = speed**3/abs(determinant)
    return p,center,radius,d/speed


def line(points, name, color, dash=None):
    return go.Scatter(x=points[:,0],y=points[:,1],mode="lines",name=name,
        line=dict(color=color,width=3,dash=dash))


def moving(t):
    p,c,r,tangent = geometry(t)
    angles = np.linspace(0,2*np.pi,241)
    circle = c+r*np.column_stack((np.cos(angles),np.sin(angles)))
    return [line(circle,"접촉원", "#e45756"),
        line(np.array([p-1.2*tangent,p+1.2*tangent]),"접선", "#54a24b","dash"),
        line(np.array([p,c]),"곡률반지름", "#8056b3"),
        go.Scatter(x=[p[0],c[0]],y=[p[1],c[1]],mode="markers+text",
            text=["접촉점 P","중심 C"],textposition=["top right","bottom left"],
            marker=dict(size=10,color=["#4c78a8","#8056b3"]),name="P, C",
            hovertemplate="(%{x:.4f}, %{y:.4f})<extra></extra>")]


def status(t):
    p,c,r,_ = geometry(t)
    return dict(x=.5,y=-.24,xref="paper",yref="paper",showarrow=False,
        text=f"선택한 t={t/np.pi:.3f}π · C=({c[0]:.4f}, {c[1]:.4f}) · R={r:.4f} · κ={1/r:.4f}")


def build_figure():
    fig = go.Figure()
    fig.add_trace(line(curve(np.linspace(0,np.pi,601)),"곡선 α", "#4c78a8"))
    fig.add_trace(go.Scatter(x=[0],y=[1],mode="markers",name="t=0: 특이점",
        marker=dict(size=9,symbol="x",color="#555555")))
    fig.add_traces(moving(np.pi/2))
    values = np.linspace(np.pi/40,np.pi,40)
    fig.frames = [go.Frame(name=str(i),data=moving(t),traces=[2,3,4,5],
        layout=dict(annotations=[status(t)])) for i,t in enumerate(values)]
    fig.update_layout(template="plotly_white",height=850,
        title=dict(x=.5,text="2023학년도 1차 A 3번 · 곡선과 접촉원"
            "<br><sup>t=π/2에서 P=(2,1), C=(2/3,−1/3), R=4√2/3</sup>"),
        margin=dict(l=65,r=35,t=100,b=200),
        xaxis=dict(title="x",range=[-3.5,4.5],autorange=False,constrain="domain"),
        yaxis=dict(title="y",range=[-3.8,4.2],autorange=False,scaleanchor="x",scaleratio=1),
        uirevision="fixed-view",legend=dict(orientation="h",y=1.06),
        annotations=[status(np.pi/2)],
        sliders=[dict(active=19,y=-.09,currentvalue=dict(prefix="t / π = "),steps=[
            dict(label=f"{t/np.pi:.3f}",method="animate",args=[[str(i)],dict(mode="immediate",
                frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i,t in enumerate(values)])])
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--no-show",action="store_true")
    args = parser.parse_args()
    fig = build_figure()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        fig.write_html(args.output,include_plotlyjs=True)
        print(args.output.resolve())
    if not args.no_show:
        fig.show()


if __name__ == "__main__":
    main()
