r"""2014학년도 12번: 포물면 반원 영역의 경계 측지곡률 적분.

X(u,v)=(u cos v,u sin v,u²/2), 0≤u≤1, 0≤v≤π.
위쪽 법선과 양의 경계 방향을 택한다. 바깥 반원 u=1의 속력은 1,
측지곡률은 1/√2이며, 두 자오선은 측지곡률이 0이다.
따라서 |∫∂S κ_g ds|=π/√2.
u=0인 매개변수 변 전체는 원점 하나로 모인다. 실제 경계는 원점에서
매끄럽게 이어지고, (±1,0,1/2)의 외각만 각각 π/2이다.
가우스-보네 검산: ∫S K dA=π(1-1/√2), 외각합=π,
π(1-1/√2)+π/√2+π=2π. 모서리 외각은 요청한 선적분에 포함하지 않는다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2014_q12_boundary_curvature.py
    python .\supplement_exam\exam_2014_q12_boundary_curvature.py --output output/exam_2014_q12.html --no-show
"""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def surface(u: np.ndarray | float, v: np.ndarray | float) -> np.ndarray:
    """포물면의 공간 좌표를 반환한다."""
    u,v=np.broadcast_arrays(u,v)
    return np.stack((u*np.cos(v),u*np.sin(v),u*u/2),axis=-1)


def boundary_geometry(v: float) -> tuple[np.ndarray, ...]:
    """바깥 반원의 단위접선, 위쪽 법선, 곡률벡터를 반환한다."""
    tangent=np.array([-np.sin(v),np.cos(v),0.])
    normal=np.array([-np.cos(v),-np.sin(v),1.])/np.sqrt(2)
    acceleration=np.array([-np.cos(v),-np.sin(v),0.])
    return tangent,normal,acceleration


def geodesic_curvature(v: float) -> float:
    """양의 방향 바깥 반원의 부호 있는 측지곡률을 계산한다."""
    tangent,normal,acceleration=boundary_geometry(v)
    return float(np.dot(acceleration,np.cross(normal,tangent)))


# 이 문항의 시각화 구성
def selected_traces(v: float) -> list:
    """두 화면의 대응점과 누적 경계 적분을 표시한다."""
    p=surface(1,v)
    return [go.Scatter3d(x=[p[0]],y=[p[1]],z=[p[2]],mode="markers",
                        marker=dict(size=7,color="#222222"),showlegend=False,
                        hovertemplate=f"v={v:.3f}<br>κ_g={geodesic_curvature(v):.6f}<extra></extra>"),
            go.Scatter(x=[1],y=[v],mode="markers",marker=dict(size=12,color="#222222"),showlegend=False),
            go.Scatter(x=[.5],y=[np.pi/2],mode="text",text=[f"진행 각 v={v/np.pi:.2f}π<br>누적 적분 v/√2={v/np.sqrt(2):.4f}"],
                       showlegend=False,hoverinfo="skip")]


def build_figure() -> go.Figure:
    """실제 영역과 매개변수 영역을 대응시킨다. 축척은 프레임 전체에서 고정한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],
                      horizontal_spacing=.12,subplot_titles=("포물면 위 영역 S와 경계","매개변수 영역: 0≤u≤1, 0≤v≤π"))
    u,v=np.meshgrid(np.linspace(0,1,61),np.linspace(0,np.pi,101))
    p=surface(u,v)
    fig.add_trace(go.Surface(x=p[...,0],y=p[...,1],z=p[...,2],opacity=.65,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],showscale=False,hoverinfo="skip"),row=1,col=1)
    t=np.linspace(0,1,201)
    boundaries=[(t,np.zeros_like(t),"#4C78A8","v=0: κ_g=0"),
                (np.ones_like(t),np.pi*t,"#E45756","u=1: κ_g=1/√2"),
                (1-t,np.full_like(t,np.pi),"#239B56","v=π: κ_g=0")]
    for uu,vv,color,label in boundaries:
        p=surface(uu,vv)
        fig.add_trace(go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",
                                  line=dict(color=color,width=7),name=label),row=1,col=1)
        fig.add_trace(go.Scatter(x=uu,y=vv,mode="lines",line=dict(color=color,width=5),showlegend=False),row=1,col=2)
    fig.add_trace(go.Scatter(x=[0,0],y=[0,np.pi],mode="lines",line=dict(color="#888888",width=4,dash="dash"),
                            name="u=0: 모두 원점으로 모임"),row=1,col=2)
    corners=surface(np.array([0,1,1]),np.array([0,0,np.pi]))
    fig.add_trace(go.Scatter3d(x=corners[:,0],y=corners[:,1],z=corners[:,2],mode="markers+text",
                              text=["O: 경계가 매끄럽게 이어짐","A: 외각 π/2","B: 외각 π/2"],
                              textposition="top center",marker=dict(size=5,color="#222222"),showlegend=False),row=1,col=1)
    # 매개변수 영역에서 양의 경계 방향을 표시한다.
    for x0,y0,x1,y1 in ((.35,0,.65,0),(1,.4*np.pi,1,.6*np.pi),(.65,np.pi,.35,np.pi)):
        fig.add_annotation(x=x1,y=y1,ax=x0,ay=y0,xref="x",yref="y",axref="x",ayref="y",
                           text="",showarrow=True,arrowhead=2,arrowsize=1.3,arrowwidth=2)
    indices=list(range(len(fig.data),len(fig.data)+3))
    for i,trace in enumerate(selected_traces(0)):
        fig.add_trace(trace,row=1,col=1 if i==0 else 2)
    parameters=np.linspace(0,np.pi,33)
    fig.frames=[go.Frame(name=str(i),data=selected_traces(float(v)),traces=indices) for i,v in enumerate(parameters)]
    fig.update_xaxes(title_text="u",range=[-.18,1.18],autorange=False,tickvals=[0,.5,1],row=1,col=2)
    fig.update_yaxes(title_text="v",range=[-.3,np.pi+.3],autorange=False,tickvals=[0,np.pi/2,np.pi],ticktext=["0","π/2","π"],row=1,col=2)
    fig.update_layout(title=dict(text="2014학년도 12번 · 경계의 측지곡률 적분"
                                 "<br><sup>바깥 반원만 기여: |∫ κ_g ds|=π/√2 ≈ 2.2214</sup>",x=.5),
                      template="plotly_white",height=820,margin=dict(l=25,r=30,t=115,b=185),
                      scene=dict(xaxis=dict(title="x",range=[-1.2,1.2],autorange=False),
                                 yaxis=dict(title="y",range=[-.2,1.2],autorange=False),
                                 zaxis=dict(title="z",range=[-.15,.7],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=2.4,y=1.4,z=.85),
                                 uirevision="camera",camera=dict(eye=dict(x=1.5,y=1.5,z=1.2))),
                      legend=dict(orientation="h",y=-.23),
                      sliders=[dict(active=0,y=-.07,currentvalue=dict(prefix="바깥 경계의 v = "),steps=[
                          dict(label=f"{v/np.pi:.2f}π",method="animate",args=[[str(i)],
                               dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,v in enumerate(parameters)])])
    fig.add_annotation(text="가우스–보네 검산: π(1−1/√2) + π/√2 + π = 2π. 외각합 π는 선적분에 포함하지 않는다.",
                       xref="paper",yref="paper",x=.5,y=-.35,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def parse_args() -> argparse.Namespace:
    """출력 옵션을 읽는다."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,help="HTML 저장 경로")
    parser.add_argument("--no-show",action="store_true",help="브라우저 창을 열지 않음")
    return parser.parse_args()


def main() -> None:
    """그림을 생성하고 HTML 저장 또는 화면 표시를 실행한다."""
    args=parse_args()
    figure=build_figure()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        figure.write_html(args.output,include_plotlyjs=True)
        print(f"저장 완료: {args.output.resolve()}")
    if not args.no_show:
        figure.show()


if __name__ == "__main__":
    main()
