r"""2019학년도 1차 B 5번: 4차 곡면에 접하는 평행한 평면.

M: z=(x⁴+y⁴)/4, H: z=x+y-d. 접점에서는 f_x=f_y=1이므로
x³=y³=1, p=(1,1,1/2), d=3/2.
K=9x²y²/(1+x⁶+y⁶)²이므로 K(p)=1.
f(x,y)-x-y는 p의 평면좌표 (1,1)에서 유일한 전역 최솟값 -3/2.
d>3/2에서는 평면이 곡면 아래, d=3/2에서는 접촉, d<3/2에서는 교차한다.
오른쪽은 x=y=t인 단면으로, 가로 좌표는 실제 거리 sqrt(2)t이다.
슬라이더는 평면만 이동하며 p는 문제의 접점으로 고정 표시한다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2019_b_q5_tangent_plane.py
저장: 위 명령에 --output output/exam_2019_b_q5.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def height(x: np.ndarray | float, y: np.ndarray | float) -> np.ndarray:
    """곡면의 높이."""
    return (np.asarray(x)**4+np.asarray(y)**4)/4


def gaussian_curvature(x: float, y: float) -> float:
    """그래프 곡면의 가우스곡률."""
    return 9*x*x*y*y/(1+x**6+y**6)**2


# 이 문항의 시각화 구성
def moving_traces(d: float) -> list:
    """평면과 단면의 직선을 반환한다."""
    x,y=np.meshgrid(np.linspace(-.6,1.8,31),np.linspace(-.6,1.8,31))
    t=np.linspace(-.6,1.8,201)
    state="접함" if np.isclose(d,1.5) else ("곡면 아래" if d>1.5 else "곡면과 교차")
    return [go.Surface(x=x,y=y,z=x+y-d,opacity=.4,showscale=False,
                       colorscale=[[0,"#F2A541"],[1,"#F2A541"]],name="평면 H",showlegend=True),
            go.Scatter(x=np.sqrt(2)*t,y=2*t-d,mode="lines",line=dict(color="#F2A541",width=4),name="평면의 단면"),
            go.Scatter(x=[.7],y=[5.1],mode="text",text=[f"d={d:.2f} · {state}"],showlegend=False,hoverinfo="skip")]


def build_figure() -> go.Figure:
    """고정 축척에서 평면의 이동과 접촉을 비교한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],horizontal_spacing=.1,
                      subplot_titles=("M과 평면 H: x+y−z=d","x=y 단면 · 접점에서 기울기도 일치"))
    x,y=np.meshgrid(np.linspace(-.6,1.8,81),np.linspace(-.6,1.8,81))
    fig.add_trace(go.Surface(x=x,y=y,z=height(x,y),opacity=.65,showscale=False,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],name="M",showlegend=True),row=1,col=1)
    fig.add_trace(go.Scatter3d(x=[1],y=[1],z=[.5],mode="markers+text",text=["p=(1,1,1/2)"],
                              textposition="top center",marker=dict(size=6,color="#E45756"),showlegend=False),row=1,col=1)
    t=np.linspace(-.6,1.8,401)
    fig.add_trace(go.Scatter3d(x=t,y=t,z=height(t,t),mode="lines",line=dict(color="#7040A0",width=6),name="x=y 단면"),row=1,col=1)
    fig.add_trace(go.Scatter(x=np.sqrt(2)*t,y=height(t,t),mode="lines",line=dict(color="#7040A0",width=4),name="곡면의 단면"),row=1,col=2)
    fig.add_trace(go.Scatter(x=[np.sqrt(2)],y=[.5],mode="markers+text",text=["p: K=1"],textposition="top left",
                            marker=dict(size=10,color="#E45756"),showlegend=False),row=1,col=2)
    indices=list(range(len(fig.data),len(fig.data)+3))
    for i,trace in enumerate(moving_traces(1.5)):
        fig.add_trace(trace,row=1,col=1 if i==0 else 2)
    parameters=np.linspace(.5,2.5,41)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(d)),traces=indices) for i,d in enumerate(parameters)]
    fig.update_xaxes(title_text="단면 내 거리 √2 t",range=[-1,2.7],autorange=False,row=1,col=2)
    fig.update_yaxes(title_text="z",range=[-4,5.6],autorange=False,row=1,col=2)
    fig.update_layout(title=dict(text="2019학년도 1차 B 5번 · 접평면과 가우스곡률"
                                 "<br><sup>f_x=f_y=1 → p=(1,1,1/2), d=3/2 · K(p)=1</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=25,r=30,t=115,b=175),
                      scene=dict(xaxis=dict(title="x",range=[-.7,1.9],autorange=False),
                                 yaxis=dict(title="y",range=[-.7,1.9],autorange=False),
                                 zaxis=dict(title="z",range=[-4,5.6],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=2.6/9.6,y=2.6/9.6,z=1),uirevision="camera",
                                 camera=dict(eye=dict(x=1.5,y=1.5,z=1.2))),legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=20,y=-.07,currentvalue=dict(prefix="평면 상수 d = "),steps=[
                          dict(label=f"{d:.2f}",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,d in enumerate(parameters)])])
    fig.add_annotation(text="K=f_xx f_yy/(1+f_x²+f_y²)² = 9x²y²/(1+x⁶+y⁶)². p에서 9/9=1.",
                       xref="paper",yref="paper",x=.5,y=-.34,showarrow=False)
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
