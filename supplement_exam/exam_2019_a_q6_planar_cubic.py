r"""2019학년도 1차 A 6번: 평면 공간곡선의 비틀림과 곡률.

C_a(t)=(t,t³-at+a,t-1)는 항상 평면 z=x-1에 놓인다.
C'=(1,3t²-a,1), C''=(0,6t,0), C'''=(0,6,0).
kappa(t)=6sqrt(2)|t|/[2+(3t²-a)²]^(3/2).
t≠0에서 비틀림은 0. t=0은 곡률 0인 변곡점이므로 표준 Frenet 비틀림은
정의되지 않는다(연속 연장값은 0). p=(1,1,0)는 모든 a에서 곡선 위에 있다.
kappa(1)=3은 [2+(3-a)²]^(3/2)=2sqrt(2)와 동치이므로 a=3.
표시 구간은 -0.5≤t≤1.7, 비교 매개변수는 0≤a≤6이다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2019_a_q6_planar_cubic.py
저장: 위 명령에 --output output/exam_2019_a_q6.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def curve(t: np.ndarray | float, a: float) -> np.ndarray:
    """곡선의 공간 좌표를 반환한다."""
    t=np.asarray(t)
    return np.stack((t,t**3-a*t+a,t-1),axis=-1)


def curvature(t: np.ndarray | float, a: np.ndarray | float) -> np.ndarray:
    """외적 공식으로 얻은 곡률."""
    t=np.asarray(t)
    return 6*np.sqrt(2)*np.abs(t)/(2+(3*t*t-a)**2)**1.5


# 이 문항의 시각화 구성
def moving_traces(a: float) -> list:
    """곡선, p의 접선, 변곡점과 곡률 그래프 대응점."""
    p=curve(np.linspace(-.5,1.7,601),a)
    tangent=np.array([1,3-a,1.]); tangent/=np.linalg.norm(tangent)
    line=np.array([1,1,0])+np.array([-.7,.7])[:,None]*tangent
    return [go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",line=dict(color="#7040A0",width=7),name="C_a"),
            go.Scatter3d(x=line[:,0],y=line[:,1],z=line[:,2],mode="lines",line=dict(color="#E45756",width=5),name="p에서의 접선"),
            go.Scatter3d(x=[0],y=[a],z=[-1],mode="markers",marker=dict(size=5,color="#777777"),
                         name="t=0: 곡률 0",hovertemplate="변곡점: 표준 비틀림 정의 안 됨<extra></extra>"),
            go.Scatter(x=[a],y=[curvature(1,a)],mode="markers",marker=dict(size=12,color="#E45756"),showlegend=False,
                       hovertemplate="a=%{x:.2f}<br>κ(p)=%{y:.5f}<extra></extra>")]


def build_figure() -> go.Figure:
    """고정된 평면과 곡률 그래프에서 a를 비교한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],horizontal_spacing=.1,
                      subplot_titles=("모든 a에서 C_a는 평면 z=x−1 위에 있음","p=(1,1,0)의 곡률: a=3에서 최대 3"))
    x,y=np.meshgrid([-.7,1.9],[-2,7.5])
    fig.add_trace(go.Surface(x=x,y=y,z=x-1,opacity=.25,showscale=False,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],name="평면 z=x−1",showlegend=True),row=1,col=1)
    fig.add_trace(go.Scatter3d(x=[1],y=[1],z=[0],mode="markers+text",text=["p=(1,1,0)"],
                              textposition="top center",marker=dict(size=6,color="#222222"),showlegend=False),row=1,col=1)
    values=np.linspace(0,6,401)
    fig.add_trace(go.Scatter(x=values,y=curvature(1,values),mode="lines",line=dict(color="#4C78A8",width=4),name="κ(p)"),row=1,col=2)
    fig.add_trace(go.Scatter(x=[0,6],y=[3,3],mode="lines",line=dict(color="#777777",dash="dash"),name="조건 κ=3"),row=1,col=2)
    indices=list(range(len(fig.data),len(fig.data)+4))
    for i,trace in enumerate(moving_traces(3)):
        fig.add_trace(trace,row=1,col=2 if i==3 else 1)
    parameters=np.linspace(0,6,31)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(a)),traces=indices) for i,a in enumerate(parameters)]
    fig.update_xaxes(title_text="상수 a",range=[0,6],autorange=False,row=1,col=2)
    fig.update_yaxes(title_text="κ(p)",range=[0,3.3],autorange=False,row=1,col=2)
    fig.update_layout(title=dict(text="2019학년도 1차 A 6번 · 평면곡선의 비틀림과 곡률"
                                 "<br><sup>τ=0 (t≠0) · κ(p)=6√2/[2+(3−a)²]³ᐟ²=3 → a=3</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=25,r=30,t=115,b=180),
                      scene=dict(xaxis=dict(title="x",range=[-.8,2],autorange=False),
                                 yaxis=dict(title="y",range=[-2,9.3],autorange=False),
                                 zaxis=dict(title="z",range=[-1.8,1],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=2.8/11.3,y=1,z=2.8/11.3),uirevision="camera",
                                 camera=dict(eye=dict(x=1.5,y=1,z=1.6))),legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=15,y=-.07,currentvalue=dict(prefix="a = "),steps=[
                          dict(label=f"{a:.1f}",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,a in enumerate(parameters)])])
    fig.add_annotation(text="곡선 전체가 평면 위에 있습니다. t=0에서는 κ=0이므로 표준 비틀림은 정의되지 않으며, 연속 연장값은 0입니다.",
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
