r"""2016학년도 1차 B 5번: 원뿔의 측지선과 전개도.

밑면 반지름 1, 모선 길이 4, 높이 sqrt(15).
꼭짓점으로부터 모선 거리 rho, 회전각 phi에 대해
X=(rho cos(phi)/4,rho sin(phi)/4,sqrt(15)(1-rho/4)).
전개 각 theta=phi/4이므로 한 바퀴는 부채꼴의 π/2에 대응한다.
q의 전개점 (4,0), p의 전개점 (0,3)을 잇는 직선 길이는 5이다.
p에서 주곡률은 안쪽 법선 기준 0, sqrt(15)/3이다.
측지선 단위접선의 위도선 성분 크기는 4/5이므로
kappa=|kappa_n|=(sqrt(15)/3)(4/5)²=16sqrt(15)/75.
꼭짓점은 정칙점이 아니며 주곡률 계산 대상에서 제외한다.

필요 라이브러리: numpy, plotly
실행: python supplement_exam/exam_2016_b_q5_cone_geodesic.py
저장: 위 명령에 --output output/exam_2016_b_q5.html --no-show 추가
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def cone(rho: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """모선 거리와 회전각을 공간 좌표로 변환한다."""
    rho,phi=np.broadcast_arrays(rho,phi)
    return np.stack((rho*np.cos(phi)/4,rho*np.sin(phi)/4,np.sqrt(15)*(1-rho/4)),axis=-1)


def developed(t: np.ndarray | float) -> np.ndarray:
    """q에서 p까지의 전개 직선. t∈[0,1], 속력은 5."""
    t=np.asarray(t)
    return np.stack((4*(1-t),3*t),axis=-1)


def geodesic(t: np.ndarray | float) -> np.ndarray:
    """전개 직선을 원뿔 위로 되감는다."""
    p=developed(t)
    return cone(np.linalg.norm(p,axis=-1),4*np.arctan2(p[...,1],p[...,0]))


# 이 문항의 시각화 구성
def markers(t: float) -> list:
    """원뿔과 전개도의 대응점을 반환한다."""
    p=geodesic(t)
    q=developed(t)
    return [go.Scatter3d(x=[p[0]],y=[p[1]],z=[p[2]],mode="markers",marker=dict(size=7,color="#E45756"),showlegend=False),
            go.Scatter(x=[q[0]],y=[q[1]],mode="markers",marker=dict(size=12,color="#E45756"),showlegend=False)]


def build_figure() -> go.Figure:
    """고정 축척에서 측지선과 부채꼴 전개도를 비교한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],horizontal_spacing=.1,
                      subplot_titles=("원뿔을 한 바퀴 도는 측지선","전개도: 중심각 π/2, 직선 qp의 길이 5"))
    r,v=np.meshgrid(np.linspace(.02,4,61),np.linspace(0,2*np.pi,101))
    p=cone(r,v)
    fig.add_trace(go.Surface(x=p[...,0],y=p[...,1],z=p[...,2],opacity=.3,showscale=False,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],hoverinfo="skip"),row=1,col=1)
    ts=np.linspace(0,1,801)
    p=geodesic(ts)
    fig.add_trace(go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",line=dict(color="#7040A0",width=7),name="측지선 γ"),row=1,col=1)
    p=cone(np.array([0,4]),0)
    fig.add_trace(go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",line=dict(color="#777777",width=4),name="p,q가 놓인 모선"),row=1,col=1)
    p=geodesic(np.array([0,1]))
    fig.add_trace(go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="markers+text",text=["q","p: pq=1"],
                              textposition="top center",marker=dict(size=5,color="#222222"),showlegend=False),row=1,col=1)
    theta=np.linspace(0,np.pi/2,201)
    fig.add_trace(go.Scatter(x=np.r_[0,4*np.cos(theta),0],y=np.r_[0,4*np.sin(theta),0],mode="lines",fill="toself",
                            fillcolor="rgba(185,215,234,0.3)",line=dict(color="#4C78A8",width=3),name="반지름 4인 부채꼴"),row=1,col=2)
    flat=developed(ts)
    fig.add_trace(go.Scatter(x=flat[:,0],y=flat[:,1],mode="lines",line=dict(color="#7040A0",width=5),name="전개된 측지선"),row=1,col=2)
    fig.add_trace(go.Scatter(x=[0,4,0],y=[0,0,3],mode="markers+text",text=["꼭짓점","q (4,0)","p (0,3)"],
                            textposition="top right",marker=dict(size=7,color="#222222"),showlegend=False),row=1,col=2)
    indices=[len(fig.data),len(fig.data)+1]
    a,b=markers(0)
    fig.add_trace(a,row=1,col=1)
    fig.add_trace(b,row=1,col=2)
    parameters=np.linspace(0,1,41)
    fig.frames=[go.Frame(name=str(i),data=markers(float(t)),traces=indices) for i,t in enumerate(parameters)]
    fig.update_xaxes(title_text="전개 좌표 X",range=[-.5,4.7],autorange=False,row=1,col=2)
    fig.update_yaxes(title_text="전개 좌표 Y",range=[-.5,4.7],autorange=False,scaleanchor="x",scaleratio=1,row=1,col=2)
    fig.update_layout(title=dict(text="2016학년도 1차 B 5번 · 원뿔의 측지선"
                                 "<br><sup>p에서 주곡률 0, √15/3 · 곡선의 곡률 κ=16√15/75</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=25,r=30,t=115,b=180),
                      scene=dict(xaxis=dict(title="x",range=[-1.2,1.2],autorange=False),
                                 yaxis=dict(title="y",range=[-1.2,1.2],autorange=False),
                                 zaxis=dict(title="z",range=[-.2,4.1],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=2.4/4.3,y=2.4/4.3,z=1),uirevision="camera-zoom-out",
                                 camera=dict(eye=dict(x=1.8,y=1.8,z=1.3))),legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=0,y=-.07,currentvalue=dict(prefix="q에서 진행한 호길이 = "),steps=[
                          dict(label=f"{5*t:.2f}",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,t in enumerate(parameters)])])
    fig.add_annotation(text="측지곡률 κ_g=0 → κ=|κ_n|. p의 접선 위도선 성분은 4/5 → κ=(√15/3)·16/25.",
                       xref="paper",yref="paper",x=.5,y=-.34,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def main() -> None:
    """그림을 생성하고 저장 또는 화면 표시를 실행한다."""
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
