"""2022학년도 1차 A 9번: Frenet 표준틀로 정의한 곡선 β.

β'=τT+κB=κ(fT+B), 따라서 |β'|=κ√(1+f²)>0.
Frenet 식에서 T'=κN, B'=-τN이므로 β''=τ'T+κ'B.
κβ=|τκ'-κτ'|/(τ²+κ²)^(3/2)=|f'|/[κ(1+f²)^(3/2)].
τ(1)κβ(1)=f(1)|f'(1)|/(1+f(1)²)^(3/2)=√3/4.
대표 예시: κ=1, f(t)=√3-2(t-1). 실제 문제는 곡선을 유일하게 정하지 않는다.
표준틀과 두 곡선은 RK4로 적분한다. NumPy, Plotly 필요.
실행: python supplement_exam/exam_2022_a_q9_frenet_curve.py
저장 옵션: --output output/exam_2022_a_q9.html --no-show
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def ratio(t):
    return np.sqrt(3)-2*(np.asarray(t)-1)


def rhs(t, state):
    """상태 행: α, T, N, B, β. κ=1, τ=f."""
    a, tangent, normal, binormal, b = state
    f = float(ratio(t))
    return np.array([tangent, normal, -tangent+f*binormal,
                     -f*normal, f*tangent+binormal])


def integrate(samples=2001):
    t = np.linspace(0, 2, samples)
    states = np.zeros((samples, 5, 3))
    states[0, 1:4] = np.eye(3)
    for i, h in enumerate(np.diff(t)):
        y = states[i]
        k1 = rhs(t[i], y)
        k2 = rhs(t[i]+h/2, y+h*k1/2)
        k3 = rhs(t[i]+h/2, y+h*k2/2)
        k4 = rhs(t[i]+h, y+h*k3)
        states[i+1] = y+h*(k1+2*k2+2*k3+k4)/6
    return t, states


def line(points, name, color, width=5, **kwargs):
    return go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2],
                        mode="lines", name=name, line=dict(color=color, width=width), **kwargs)


def moving(t, state):
    a, tangent, normal, binormal, b = state
    # 모든 벡터에 동일한 표시 배율을 적용한다.
    velocity = float(ratio(t))*tangent+binormal
    traces = []
    for origin, vector, name, color in (
        (a,tangent,"T", "#e45756"), (a,binormal,"B", "#54a24b"),
        (b,float(ratio(t))*tangent,"τT", "#e45756"),
        (b,binormal,"κB", "#54a24b"), (b,velocity,"β′=τT+κB", "#f2a900")):
        points = np.array([origin, origin+vector*.4])
        trace = line(points, name, color, 7)
        trace.mode = "lines+markers"
        trace.marker = dict(size=[0,4], color=color)
        traces.append(trace)
    for point, color in ((a,"#4c78a8"),(b,"#8056b3")):
        traces.append(go.Scatter3d(x=[point[0]],y=[point[1]],z=[point[2]],
            mode="markers",marker=dict(size=6,color=color),showlegend=False))
    return traces


def build_figure():
    t, states = integrate()
    fig = make_subplots(rows=1, cols=2, specs=[[{"type":"scene"},{"type":"scene"}]],
        subplot_titles=("원곡선 α와 T, B", "β와 속도벡터의 분해"), horizontal_spacing=.06)
    for col, index, name, color in ((1,0,"α", "#4c78a8"),(2,4,"β", "#8056b3")):
        fig.add_trace(line(states[:,index],name,color),row=1,col=col)
    indices = list(range(2,9))
    for trace, col in zip(moving(1,states[1000]),[1,1,2,2,2,1,2]):
        fig.add_trace(trace,row=1,col=col)
    chosen = np.arange(0,len(t),40)
    fig.frames = [go.Frame(name=str(i),data=moving(t[i],states[i]),traces=indices) for i in chosen]
    # 모든 시점의 벡터 끝점까지 포함한 고정 범위. 각 패널의 단위 비율도 유지한다.
    for col, state_index in ((1,0),(2,4)):
        points = states[:,state_index]
        lo, hi = points.min(axis=0)-1.7, points.max(axis=0)+1.7
        span = hi-lo
        scene = dict(aspectmode="manual",aspectratio=dict(zip("xyz",span/span.max())),
                     camera=dict(eye=dict(x=1.6,y=1.6,z=1.1)),uirevision="fixed-camera")
        for j, axis in enumerate("xyz"):
            scene[axis+"axis"] = dict(title=axis,range=[lo[j],hi[j]],autorange=False)
        fig.update_layout(**{("scene" if col==1 else "scene2"):scene})
    fig.update_layout(template="plotly_white",height=820,margin=dict(l=20,r=20,t=145,b=190),
        title=dict(text="2022학년도 1차 A 9번 · 표준틀로 만든 곡선 β"
            "<br><sup>대표 예시 κ=1, τ=f=√3−2(t−1) · 벡터는 모두 실제 길이의 0.4배로 표시</sup>",x=.5),
        legend=dict(orientation="h",y=-.25),
        sliders=[dict(active=25,y=-.06,currentvalue=dict(prefix="t = "),steps=[
            dict(label=f"{t[i]:.2f}",method="animate",args=[[str(i)],dict(mode="immediate",
                frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i in chosen])])
    fig.add_annotation(x=.5,y=1.13,xref="paper",yref="paper",showarrow=False,
        text="|β′| = κ√(1+f²) > 0：β는 정칙곡선 · κβ = |f′| / [κ(1+f²)³ᐟ²]")
    fig.add_annotation(x=.5,y=-.37,xref="paper",yref="paper",showarrow=False,
        text="t=1：f=√3, f′=−2 → τ(1)κβ(1)=√3/4 ≈ 0.433013 (대표 예시 선택과 무관)")
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
