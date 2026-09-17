r"""2021학년도 1차 B 10번: 회전면 띠 영역의 가우스곡률 적분.

r(u)=u⁴-2u²+5, X(u,v)=(r(u)cos v,r(u)sin v,u), -1≤u≤1.
K=-r''/[r(1+r'²)²], dA=r sqrt(1+r'²) du dv.
∫∫K dA=-2π[r'/sqrt(1+r'²)]₋₁¹=0 (r'(±1)=0).
|u|<1/sqrt(3)에서는 K>0, 그 바깥에서는 K<0이다.
영역은 원환형 띠로 Euler 지표 0, 양쪽 경계는 r'=0이므로 측지곡률 0.
가우스-보네 정리로도 전체 곡률 적분은 0이다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2021_b_q10_total_curvature.py
저장: 위 명령에 --output output/exam_2021_b_q10.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def radius(u: np.ndarray | float) -> np.ndarray:
    """회전 반지름."""
    u=np.asarray(u)
    return u**4-2*u*u+5


def derivatives(u: np.ndarray | float) -> tuple:
    """r의 1계와 2계 도함수."""
    u=np.asarray(u)
    return 4*u**3-4*u,12*u*u-4


def curvature(u: np.ndarray | float) -> np.ndarray:
    """가우스곡률."""
    first,second=derivatives(u)
    return -second/(radius(u)*(1+first*first)**2)


def cumulative(u: np.ndarray | float) -> np.ndarray:
    """z=-1부터 u까지의 곡률 면적분."""
    first,_=derivatives(u)
    return -2*np.pi*first/np.sqrt(1+first*first)


# 이 문항의 시각화 구성
def moving_traces(u: float) -> list:
    """선택한 평행원과 누적 적분의 대응점."""
    v=np.linspace(0,2*np.pi,201)
    return [go.Scatter3d(x=radius(u)*np.cos(v),y=radius(u)*np.sin(v),z=np.full_like(v,u),mode="lines",
                        line=dict(color="#222222",width=6),name="선택한 높이",hovertemplate=f"u={u:.2f}<br>K={float(curvature(u)):.5f}<extra></extra>"),
            go.Scatter(x=[u],y=[cumulative(u)],mode="markers",marker=dict(size=12,color="#222222"),showlegend=False)]


def build_figure() -> go.Figure:
    """곡률 부호와 누적 적분을 나란히 표시한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],horizontal_spacing=.13,
                      subplot_titles=("영역 S: 파랑 K<0, 빨강 K>0","z=−1부터 선택한 높이까지의 ∫K dA"))
    u,v=np.meshgrid(np.linspace(-1,1,121),np.linspace(0,2*np.pi,121))
    fig.add_trace(go.Surface(x=radius(u)*np.cos(v),y=radius(u)*np.sin(v),z=u,
                            surfacecolor=curvature(u),cmin=-2,cmax=2,colorscale="RdBu_r",
                            colorbar=dict(title="K",x=.47,len=.65,thickness=12),opacity=.85,
                            customdata=curvature(u),hovertemplate="z=%{z:.3f}<br>K=%{customdata:.5f}<extra></extra>"),row=1,col=1)
    v=np.linspace(0,2*np.pi,201)
    for h,color,name in ((-1,"#7040A0","경계 z=−1"),(1,"#7040A0","경계 z=1"),
                          (-1/np.sqrt(3),"#999999","K=0인 평행원"),(1/np.sqrt(3),"#999999","K=0인 평행원")):
        fig.add_trace(go.Scatter3d(x=radius(h)*np.cos(v),y=radius(h)*np.sin(v),z=np.full_like(v,h),mode="lines",
                                  line=dict(color=color,width=4),name=name,showlegend=bool(h!=1/np.sqrt(3))),row=1,col=1)
    values=np.linspace(-1,1,501)
    fig.add_trace(go.Scatter(x=values,y=cumulative(values),mode="lines",line=dict(color="#7040A0",width=4),name="누적 적분"),row=1,col=2)
    fig.add_trace(go.Scatter(x=[-1,1],y=[0,0],mode="markers+text",text=["시작: 0","전체: 0"],
                            textposition="top center",marker=dict(size=9,color="#E45756"),showlegend=False),row=1,col=2)
    indices=[len(fig.data),len(fig.data)+1]
    a,b=moving_traces(1)
    fig.add_trace(a,row=1,col=1); fig.add_trace(b,row=1,col=2)
    parameters=np.linspace(-1,1,41)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(u)),traces=indices) for i,u in enumerate(parameters)]
    fig.update_xaxes(title_text="상한 높이 u",range=[-1.1,1.1],autorange=False,row=1,col=2)
    fig.update_yaxes(title_text="누적 곡률 면적분",range=[-6,6],autorange=False,zeroline=True,row=1,col=2)
    fig.update_layout(title=dict(text="2021학년도 1차 B 10번 · 회전면의 전체 곡률"
                                 "<br><sup>∫∫S K dA = −2π[r′/√(1+r′²)]₋₁¹ = 0</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=25,r=30,t=115,b=180),
                      scene=dict(xaxis=dict(title="x",range=[-5.5,5.5],autorange=False),
                                 yaxis=dict(title="y",range=[-5.5,5.5],autorange=False),
                                 zaxis=dict(title="z",range=[-1.3,1.3],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=1,y=1,z=2.6/11),uirevision="camera",
                                 camera=dict(eye=dict(x=1.6,y=1.6,z=.8))),legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=40,y=-.07,currentvalue=dict(prefix="적분 상한 u = "),steps=[
                          dict(label=f"{u:.2f}",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for i,u in enumerate(parameters)])])
    fig.add_annotation(text="χ(S)=0, 경계 z=±1은 r′=0인 측지선 → 가우스–보네 정리에서도 ∫∫K dA=0.",
                       xref="paper",yref="paper",x=.5,y=-.35,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def main() -> None:
    """그림을 생성하고 저장 또는 표시한다."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--no-show",action="store_true")
    args=parser.parse_args(); fig=build_figure()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        fig.write_html(args.output,include_plotlyjs=True)
        print(f"저장 완료: {args.output.resolve()}")
    if not args.no_show:
        fig.show()


if __name__ == "__main__":
    main()
