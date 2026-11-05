r"""2017학년도 1차 A 8번: beta=T/2+N의 길이와 원곡선의 곡률.

평면곡선에서 T'=kN, N'=-kT이므로 beta'=k(N/2-T).
||beta'||=sqrt(5)k/2. 모든 t>0에 대해 길이가 3t이므로 s>0에서
||beta'||=3, k=6/sqrt(5). 특히 k(1)=6/sqrt(5).
시각화에는 이 조건을 만족하는 대표 원 gamma(s)=R(cos(ks),sin(ks)),
R=sqrt(5)/6을 사용한다. 음의 s에 대한 모양을 조건에서 단정하지 않는다.
beta는 원점에서 시작하는 위치벡터 T/2+N의 끝점이며 gamma에 더하지 않는다.
beta의 반지름은 sqrt(5)/2, 속력은 3이다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2017_a_q8_tangent_normal.py
저장: 위 명령에 --output output/exam_2017_a_q8.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

KAPPA = 6 / np.sqrt(5)


# 수학적 정의와 계산
def frame(s: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
    """대표 원곡선의 단위 접벡터와 주법선벡터를 반환한다."""
    angle=KAPPA*np.asarray(s)
    return (np.stack((-np.sin(angle),np.cos(angle)),axis=-1),
            np.stack((-np.cos(angle),-np.sin(angle)),axis=-1))


def gamma(s: np.ndarray | float) -> np.ndarray:
    """양의 구간 조건을 만족하는 단위속력 대표 원곡선."""
    _,normal=frame(s)
    return -normal/KAPPA


def beta(s: np.ndarray | float) -> np.ndarray:
    """위치벡터 beta=T/2+N을 반환한다."""
    tangent,normal=frame(s)
    return tangent/2+normal


# 이 문항의 시각화 구성
def vector_trace(start: np.ndarray, vector: np.ndarray, label: str, color: str) -> go.Scatter:
    """선분 끝의 삼각형으로 벡터의 방향을 표시한다."""
    end=start+vector
    return go.Scatter(x=[start[0],end[0]],y=[start[1],end[1]],mode="lines+markers",
                      line=dict(color=color,width=4),marker=dict(size=[0,11],symbol="arrow",angleref="previous"),
                      name=label,hovertemplate=label+f"<br>길이={np.linalg.norm(vector):.4f}<extra></extra>")


def moving_traces(s: float) -> list:
    """두 화면의 관찰점과 벡터 합, 누적 길이를 반환한다."""
    p=gamma(s)
    tangent,normal=frame(s)
    q=beta(s)
    return [go.Scatter(x=[p[0]],y=[p[1]],mode="markers",marker=dict(size=9,color="#222222"),showlegend=False),
            vector_trace(p,tangent,"T · 길이 1","#E45756"),
            vector_trace(p,normal,"N · 길이 1","#239B56"),
            vector_trace(np.zeros(2),tangent/2,"T/2","#E45756"),
            vector_trace(tangent/2,normal,"N (평행이동)","#239B56"),
            vector_trace(np.zeros(2),q,"β=T/2+N","#7040A0"),
            go.Scatter(x=[q[0]],y=[q[1]],mode="markers",marker=dict(size=10,color="#222222"),showlegend=False),
            go.Scatter(x=[0],y=[-1.43],mode="text",text=[f"s={s:.2f} · γ의 길이={s:.2f} · β의 길이={3*s:.2f}"],showlegend=False,hoverinfo="skip")]


def build_figure() -> go.Figure:
    """같은 좌표 축척의 두 평면 그림과 대응 슬라이더를 만든다."""
    fig=make_subplots(rows=1,cols=2,horizontal_spacing=.1,
                      subplot_titles=("γ: 반지름 √5/6 · 속력 1","β: 반지름 √5/2 · 속력 3"))
    samples=np.linspace(0,2*np.pi/KAPPA,501)
    for col,points,name in ((1,gamma(samples),"대표 원곡선 γ"),(2,beta(samples),"β의 전체 원 궤적")):
        fig.add_trace(go.Scatter(x=points[:,0],y=points[:,1],mode="lines",line=dict(color="#8796A5",width=3),name=name),row=1,col=col)
    indices=list(range(2,10))
    for i,trace in enumerate(moving_traces(0)):
        fig.add_trace(trace,row=1,col=1 if i<3 else 2)
    parameters=np.linspace(0,2,41)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(s)),traces=indices) for i,s in enumerate(parameters)]
    for col in (1,2):
        fig.update_xaxes(title_text="x",range=[-1.65,1.65],autorange=False,constrain="domain",row=1,col=col)
        fig.update_yaxes(title_text="y",range=[-1.65,1.65],autorange=False,
                          scaleanchor="x" if col==1 else "x2",scaleratio=1,row=1,col=col)
    fig.update_layout(title=dict(text="2017학년도 1차 A 8번 · 접벡터와 주법선의 합"
                                 "<br><sup>||β′||=(√5/2)κ=3 → κ(1)=6/√5 ≈ 2.6833</sup>",x=.5),
                      template="plotly_white",height=800,margin=dict(l=30,r=30,t=115,b=180),
                      legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=0,y=-.07,currentvalue=dict(prefix="호길이 매개변수 s = "),steps=[
                          dict(label=f"{s:.2f}",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,s in enumerate(parameters)])])
    fig.add_annotation(text="오른쪽 β는 원점에서 그린 벡터 합입니다. 두 화면은 동일한 축척이며 슬라이더 이동 중 고정됩니다.",
                       xref="paper",yref="paper",x=.5,y=-.36,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def main() -> None:
    """그림을 생성하고 저장 또는 화면 표시를 실행한다."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,help="HTML 저장 경로")
    parser.add_argument("--no-show",action="store_true",help="브라우저 창을 열지 않음")
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
