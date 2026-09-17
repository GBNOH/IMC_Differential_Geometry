r"""2018학년도 1차 A 6번: 직교 조건과 곡률.

beta(t)=∫₂ᵗ(alpha(s)+s²N(s))ds 이므로
beta''=(1-t²kappa)T+2tN+t²tau B.
<alpha'(2),beta''(2)>=1-4kappa(2)=0 → kappa(2)=1/4.
곡선 전체는 주어진 조건으로 유일하게 정해지지 않는다.
시각화는 alpha(2)=0인 평면 원(비틀림 0)을 대표 예시로 사용한다.
슬라이더의 kappa≠1/4인 예시는 직교 조건이 성립하지 않는 비교 대상이다.
일반 공간곡선에서도 B 성분은 T에 수직이므로 답은 동일하다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2018_a_q6_orthogonal_vectors.py
저장: 위 명령에 --output output/exam_2018_a_q6.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def alpha(s: np.ndarray | float, kappa: float) -> np.ndarray:
    """alpha(2)=0, T(2)=(1,0), N(2)=(0,1)인 단위속력 원."""
    if not np.isfinite(kappa) or kappa<=0:
        raise ValueError("곡률은 유한한 양수여야 합니다.")
    angle=kappa*(np.asarray(s)-2)
    return np.stack((np.sin(angle)/kappa,(1-np.cos(angle))/kappa),axis=-1)


def beta_second(kappa: float, tau: float = 0.) -> np.ndarray:
    """t=2에서 beta''의 T,N,B 성분을 반환한다."""
    return np.array([1-4*kappa,4.,4*tau])


# 이 문항의 시각화 구성
def arrow(vector: np.ndarray, name: str, color: str) -> go.Scatter:
    """원점에서 시작하는 벡터를 실제 길이로 표시한다."""
    return go.Scatter(x=[0,vector[0]],y=[0,vector[1]],mode="lines+markers",
                      line=dict(color=color,width=5),marker=dict(size=[0,12],symbol="arrow",angleref="previous"),name=name)


def moving_traces(kappa: float) -> list:
    """대표 곡선과 beta''의 접선·법선 성분을 반환한다."""
    p=alpha(np.linspace(0,4,401),kappa)
    v=beta_second(kappa)
    return [go.Scatter(x=p[:,0],y=p[:,1],mode="lines",line=dict(color="#7040A0",width=5),name="대표 원곡선 α"),
            arrow(v,"β″(2) (비틀림 0 예시)","#7040A0"),
            arrow(np.array([v[0],0]),"접선 성분 (1−4κ)T","#E45756"),
            go.Scatter(x=[v[0],v[0]],y=[0,4],mode="lines",line=dict(color="#239B56",width=3,dash="dash"),name="법선 성분 4N"),
            go.Scatter(x=[0],y=[4.55],mode="text",text=[f"κ={kappa:.2f} · T·β″={v[0]:.2f}"+
                       (" · 직교 조건 성립" if np.isclose(v[0],0) else " · 직교하지 않음")],showlegend=False,hoverinfo="skip")]


def build_figure() -> go.Figure:
    """곡률을 바꾸며 직교 조건을 비교하는 두 평면 그림."""
    fig=make_subplots(rows=1,cols=2,horizontal_spacing=.12,
                      subplot_titles=("대표 곡선: α(2)=0, τ=0","t=2의 벡터: β″=(1−4κ)T+4N"))
    for col in (1,2):
        fig.add_trace(arrow(np.array([1.,0]),"T=α′(2)","#E45756"),row=1,col=col)
        fig.add_trace(arrow(np.array([0.,1]),"N(2)","#239B56"),row=1,col=col)
    fig.add_trace(go.Scatter(x=[0],y=[0],mode="markers+text",text=["α(2)=0"],textposition="bottom center",
                            marker=dict(size=7,color="#222222"),showlegend=False),row=1,col=1)
    indices=list(range(len(fig.data),len(fig.data)+5))
    for i,trace in enumerate(moving_traces(.25)):
        fig.add_trace(trace,row=1,col=1 if i==0 else 2)
    parameters=np.linspace(.05,.5,19)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(k)),traces=indices) for i,k in enumerate(parameters)]
    for col in (1,2):
        fig.update_xaxes(title_text="T 방향",range=[-2.3,2.3],autorange=False,row=1,col=col)
        fig.update_yaxes(title_text="N 방향",range=[-.7,4.9],autorange=False,
                          scaleanchor="x" if col==1 else "x2",scaleratio=1,row=1,col=col)
    fig.update_layout(title=dict(text="2018학년도 1차 A 6번 · 직교 조건으로 곡률 구하기"
                                 "<br><sup>T·β″(2)=1−4κ(2)=0 → κ(2)=1/4</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=30,r=30,t=115,b=180),legend=dict(orientation="h",y=-.24),
                      sliders=[dict(active=8,y=-.07,currentvalue=dict(prefix="비교 예시의 곡률 κ = "),steps=[
                          dict(label=f"{k:.3f}",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,k in enumerate(parameters)])])
    fig.add_annotation(text="일반식 β″(2)=(1−4κ)T+4N+4τB. N,B는 T에 수직이므로 비틀림과 무관하게 κ=1/4.",
                       xref="paper",yref="paper",x=.5,y=-.35,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def main() -> None:
    """그림을 생성하고 HTML 저장 또는 화면 표시를 실행한다."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,help="HTML 저장 경로")
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
