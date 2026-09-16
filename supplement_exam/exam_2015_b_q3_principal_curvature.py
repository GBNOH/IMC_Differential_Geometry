r"""2015학년도 1차 B 3번: 4차 회전면의 주곡률과 Euler 공식.

M: x=(y²+z²)²/4, p=(u⁴/4,u,0), u>0.
양의 x 성분을 갖는 법선을 택한다. 자오선 주방향을 e1, (0,0,1)을 e2라 하면
k1=3u²/(1+u⁶)^(3/2), k2=u²/sqrt(1+u⁶), K=3u⁴/(1+u⁶)².
w=sin(theta)e1+cos(theta)e2에 대해 kn=k1 sin²(theta)+k2 cos²(theta).
theta=π/6에서 a=1/4,b=3/4이므로 ab=3/16 (주곡률 순서를 바꾸어도 동일).
제시된 해설의 X_u=(u,1,0)는 위 4차 곡면의 미분과 불일치한다.
이 코드는 문제의 곡면 식과 점 p를 기준으로 계산한다.

필요 라이브러리: numpy, plotly
실행 예:
    python .\supplement_exam\exam_2015_b_q3_principal_curvature.py
    python .\supplement_exam\exam_2015_b_q3_principal_curvature.py --output output/exam_2015_b_q3.html --no-show
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 수학적 정의와 계산
def surface(y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """4차 회전면의 공간 좌표를 반환한다."""
    y,z=np.broadcast_arrays(y,z)
    return np.stack(((y*y+z*z)**2/4,y,z),axis=-1)


def geometry(u: float) -> tuple:
    """p, 두 단위 주방향, 단위법선, 두 주곡률을 반환한다."""
    if not np.isfinite(u) or u<=0:
        raise ValueError("u는 유한한 양수여야 합니다.")
    d=np.sqrt(1+u**6)
    return (surface(u,0),np.array([u**3,1,0])/d,np.array([0.,0.,1.]),
            np.array([1,-u**3,0])/d,3*u*u/d**3,u*u/d)


def normal_curvature(u: float, theta: np.ndarray | float) -> np.ndarray:
    """e2와의 각 theta에 대한 Euler 공식."""
    *_,k1,k2=geometry(u)
    return k1*np.sin(theta)**2+k2*np.cos(theta)**2


# 이 문항의 시각화 구성
def moving_traces(u: float) -> list:
    """접평면, 주방향, 30도 방향과 곡률 그래프를 갱신한다."""
    p,e1,e2,n,k1,k2=geometry(u)
    a,b=np.meshgrid([-.45,.45],[-.45,.45])
    plane=p+a[...,None]*e1+b[...,None]*e2
    traces=[go.Surface(x=plane[...,0],y=plane[...,1],z=plane[...,2],opacity=.3,
                      colorscale=[[0,"#F2A541"],[1,"#F2A541"]],showscale=False,
                      name="접평면",showlegend=True),
            go.Scatter3d(x=[p[0]],y=[p[1]],z=[p[2]],mode="markers",marker=dict(size=5,color="#222222"),
                         name="p",hovertemplate=f"u={u:.2f}<br>K={k1*k2:.6f}<extra></extra>")]
    w=.5*e1+np.sqrt(3)/2*e2
    for vector,label,color in ((e1,"e₁: 자오선 주방향","#7040A0"),(e2,"e₂=(0,0,1)","#239B56"),(w,"w: e₂와 30°","#E45756")):
        end=p+vector
        traces.append(go.Scatter3d(x=[p[0],end[0]],y=[p[1],end[1]],z=[p[2],end[2]],mode="lines",
                                  line=dict(color=color,width=7),name=label))
        traces.append(go.Cone(x=[end[0]],y=[end[1]],z=[end[2]],u=[vector[0]],v=[vector[1]],w=[vector[2]],
                              anchor="tip",sizemode="absolute",sizeref=.12,colorscale=[[0,color],[1,color]],showscale=False,hoverinfo="skip"))
    angle=np.linspace(0,np.pi/6,31)
    arc=p+.35*(np.sin(angle)[:,None]*e1+np.cos(angle)[:,None]*e2)
    traces.append(go.Scatter3d(x=arc[:,0],y=arc[:,1],z=arc[:,2],mode="lines",line=dict(color="#222222",width=3),showlegend=False))
    angles=np.linspace(0,np.pi/2,181)
    traces.append(go.Scatter(x=np.degrees(angles),y=normal_curvature(u,angles),mode="lines",name="κₙ(θ)",line=dict(color="#4C78A8",width=4)))
    traces.append(go.Scatter(x=[30],y=[normal_curvature(u,np.pi/6)],mode="markers",marker=dict(size=12,color="#E45756"),
                            name="θ=30°",hovertemplate=f"κ₁={k1:.5f}<br>κ₂={k2:.5f}<br>K={k1*k2:.5f}<br>κₙ=%{{y:.5f}}<extra></extra>"))
    return traces


def build_figure() -> go.Figure:
    """u를 이동하며 접평면과 방향별 법곡률을 비교한다."""
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type="scene"),dict(type="xy")]],horizontal_spacing=.12,
                      subplot_titles=("M: 4x=(y²+z²)² · 단위벡터 e₁,e₂,w","Euler 공식 · θ는 e₂와 이루는 각"))
    r,v=np.meshgrid(np.linspace(0,1.65,71),np.linspace(0,2*np.pi,101))
    p=surface(r*np.cos(v),r*np.sin(v))
    fig.add_trace(go.Surface(x=p[...,0],y=p[...,1],z=p[...,2],opacity=.35,
                            colorscale=[[0,"#B9D7EA"],[1,"#B9D7EA"]],showscale=False,hoverinfo="skip"),row=1,col=1)
    traces=moving_traces(1.)
    indices=list(range(1,len(traces)+1))
    for i,trace in enumerate(traces):
        fig.add_trace(trace,row=1,col=2 if i>=9 else 1)
    parameters=np.linspace(.25,1.5,26)
    fig.frames=[go.Frame(name=str(i),data=moving_traces(float(u)),traces=indices) for i,u in enumerate(parameters)]
    fig.update_xaxes(title_text="θ (도)",range=[0,90],autorange=False,tickvals=[0,30,60,90],row=1,col=2)
    fig.update_yaxes(title_text="법곡률 κₙ",range=[0,1.5],autorange=False,row=1,col=2)
    fig.update_layout(title=dict(text="2015학년도 1차 B 3번 · 주곡률과 법곡률"
                                 "<br><sup>K(u)=3u⁴/(1+u⁶)² · κ(w)=κ₁/4+3κ₂/4 → ab=3/16</sup>",x=.5),
                      template="plotly_white",height=850,margin=dict(l=25,r=30,t=115,b=195),
                      scene=dict(xaxis=dict(title="x",range=[-.5,2.5],autorange=False),
                                 yaxis=dict(title="y",range=[-1.8,2.5],autorange=False),
                                 zaxis=dict(title="z",range=[-1.8,1.8],autorange=False),
                                 aspectmode="manual",aspectratio=dict(x=3,y=4.3,z=3.6),uirevision="camera",
                                 camera=dict(eye=dict(x=1.5,y=1.5,z=1.2))),
                      legend=dict(orientation="h",y=-.24),
                      sliders=[dict(active=15,y=-.07,currentvalue=dict(prefix="점 p의 매개변수 u = "),steps=[
                          dict(label=f"{u:.2f}",method="animate",args=[[str(i)],dict(mode="immediate",frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                          for i,u in enumerate(parameters)])])
    fig.add_annotation(text="문제의 4차 곡면을 기준으로 계산. 제시된 해설의 미분식은 해당 곡면 식과 불일치합니다.",
                       xref="paper",yref="paper",x=.5,y=-.37,showarrow=False)
    return fig


# 실행 옵션과 HTML 저장
def main() -> None:
    """그림을 생성하고 HTML 저장 또는 화면 표시를 실행한다."""
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
