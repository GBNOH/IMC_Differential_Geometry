# Teacher Recruitment Examination

이 폴더는 교원임용시험(Teacher Recruitment Examination)의 미분기하학 관련 내용을
시각화하는 코드와 자료를 정리하기 위한 공간입니다.

## 2022학년도 1차 A 9번

- `exam_2022_a_q9_frenet_curve.py`: 조건을 만족하는 대표 곡선 α와 β를 비교하고,
  β′=τT+κB의 벡터 분해와 τ(1)κβ(1)=√3/4를 표시합니다.
- 실행: `python supplement_exam/exam_2022_a_q9_frenet_curve.py --output output/exam_2022_a_q9.html --no-show`

## 목표

- 2025학년도 1차 B 2번: `exam_2025_b_q2_cardioid.py`에서 카디오이드의 진행 방향,
  첨점, 누적 길이와 곡률 적분을 비교합니다.
  실행: `python supplement_exam/exam_2025_b_q2_cardioid.py --output output/exam_2025_b_q2.html --no-show`

- 2025학년도 1차 A 9번: `exam_2025_a_q9_catenoid.py`에서 카테노이드의 접평면,
  두 주방향과 방향별 법곡률을 비교합니다.
  실행: `python supplement_exam/exam_2025_a_q9_catenoid.py --output output/exam_2025_a_q9.html --no-show`

- 2024학년도 1차 B 7번: `exam_2024_b_q7_gauss_map.py`에서 타원면의 영역과
  가우스 사상의 대응을 비교합니다. 점에서의 곡률과 전체 곡률 적분을 표시합니다.
  실행: `python supplement_exam/exam_2024_b_q7_gauss_map.py --output output/exam_2024_b_q7.html --no-show`

- 2024학년도 1차 A 4번: `exam_2024_a_q4_exponential_curve.py`에서 공간곡선,
  주어진 점을 통과하는 접선 및 접촉원을 비교합니다.
  실행: `python supplement_exam/exam_2024_a_q4_exponential_curve.py --output output/exam_2024_a_q4.html --no-show`

- 2023학년도 1차 B 9번: `exam_2023_b_q9_intersection_curvature.py`에서 두 곡면의 교선과
  곡률벡터의 법선·접평면 성분을 비교합니다. 위쪽 법선을 기준으로 법곡률 부호를 표시합니다.
  실행: `python supplement_exam/exam_2023_b_q9_intersection_curvature.py --output output/exam_2023_b_q9.html --no-show`

- 2023학년도 1차 A 3번: `exam_2023_a_q3_osculating_circle.py`에서 곡선과 접촉원,
  접선 및 곡률중심을 슬라이더로 비교합니다. t=0의 특이점은 접촉원 계산에서 제외합니다.
  실행: `python supplement_exam/exam_2023_a_q3_osculating_circle.py --output output/exam_2023_a_q3.html --no-show`

- 임용시험에 출제되는 주요 미분기하학 개념을 시각적으로 설명합니다.
- 곡선과 곡면의 기하적 성질을 Python 코드로 구현합니다.
- 문제의 계산 결과와 기하적 의미를 함께 이해할 수 있도록 구성합니다.

## 주요 주제

- 평면곡선과 공간곡선
- 곡률과 비틀림
- Frenet 표준틀
- 곡면의 제1·제2 기본형
- Gaussian 곡률과 평균곡률
- 측지선

주제와 디렉터리 구조는 구현이 진행됨에 따라 변경될 수 있습니다.

## 파일 작성 원칙

- 각 파일은 수학적 정의와 계산, 문항별 시각화, 실행 옵션과 HTML 저장 순서로 구성합니다.
- `build_figure()`는 그림만 반환하고 `main()`에서 저장과 화면 표시를 처리합니다.
- 현재 문항들은 각각 독립 실행 파일로 유지합니다. 앞으로 여러 문항에서 반복되는
  기능이 확인되면 공통 모듈로 옮깁니다.

- 파일명만으로 시각화 대상을 알 수 있도록 작성합니다.
- 코드 상단에 관련 개념 또는 문제에 관한 간단한 설명을 추가합니다.
- 가능한 경우 수식에 사용한 기호와 코드의 변수명을 일치시킵니다.
- 시각화에 필요한 라이브러리와 실행 방법을 각 파일에 명시합니다.

## 2009학년도 시험 시각화

| 문항 | 파일 | 시각화 내용 |
|---:|---|---|
| 35 | `exam_2009_q35_torsion.py` | `beta(t)=2 alpha(-2t)`에서 확대와 재매개화가 비틀림에 미치는 영향, Frenet 표준틀 |
| 36 | `exam_2009_q36_developable_surface.py` | `x(u,v)=(u,v,u^3+2v)`의 선직면 구조, `K=0`, 등거리 전개와 측지삼각형 |

두 시각화는 마우스로 회전·확대하고 각 곡선과 곡면 위의 값을 확인할 수 있는 Plotly
대화형 그래프로 작성되어 있습니다.

## 2010학년도 시험 시각화

| 문항 | 파일 | 시각화 내용 |
|---:|---|---|
| 19 | `exam_2010_q19_normal_plane.py` | 두 곡면의 교선, 접선, 법평면과 보기의 위치 |
| 20 | `exam_2010_q20_geodesic_curvature.py` | 원 위의 관찰점을 이동하며 곡률벡터의 법선·접평면 성분과 측지곡률 확인 |

마우스로 회전·확대할 수 있으며, 버튼으로 두 곡면을 숨겨 접선과 법평면을 관찰할 수 있습니다.

```powershell
python .\supplement_exam\exam_2010_q19_normal_plane.py
python .\supplement_exam\exam_2010_q19_normal_plane.py --output .\output\exam_2010_q19.html --no-show
python .\supplement_exam\exam_2010_q20_geodesic_curvature.py --output .\output\exam_2010_q20.html --no-show
```

## 2011학년도 시험 시각화

| 문항 | 파일 | 시각화 내용 |
|---:|---|---|
| 35 | `exam_2011_q35_helix_length.py` | P에서 Q까지의 원나선과 원기둥 전개도, 세 바퀴의 이동과 호길이 |
| 36 | `exam_2011_q36_catenoid_curvature.py` | 현수면의 곡률 색상과 K 그래프, 위치에 따른 단면과 최솟값 |

슬라이더로 원나선과 전개도의 대응점을 함께 이동할 수 있습니다.

```powershell
python .\supplement_exam\exam_2011_q35_helix_length.py
python .\supplement_exam\exam_2011_q35_helix_length.py --output .\output\exam_2011_q35.html --no-show
python .\supplement_exam\exam_2011_q36_catenoid_curvature.py --output .\output\exam_2011_q36.html --no-show
```

## 실행 환경 및 기존 예제

2021학년도 1차 B 10번 `exam_2021_b_q10_total_curvature.py`는 회전면 띠의
가우스곡률 부호와 높이별 누적 면적분을 비교합니다. 전체 적분은 0입니다.

```powershell
python .\supplement_exam\exam_2021_b_q10_total_curvature.py --output .\output\exam_2021_b_q10.html --no-show
```

2021학년도 1차 A 4번 `exam_2021_a_q4_spherical_circle.py`는 구면 위 작은 원의
종법선과 구면 법선이 이루는 60도 각, 법선의 직교 성분을 비교합니다.

```powershell
python .\supplement_exam\exam_2021_a_q4_spherical_circle.py --output .\output\exam_2021_a_q4.html --no-show
```

2020학년도 1차 B 8번 `exam_2020_b_q8_mean_curvature.py`는 접평면과 방향별
법곡률을 비교합니다. 해설의 L=0과 달리 직접 계산한 L=√2를 사용하며 H=√2/18입니다.

```powershell
python .\supplement_exam\exam_2020_b_q8_mean_curvature.py --output .\output\exam_2020_b_q8.html --no-show
```

2019학년도 1차 B 5번 `exam_2019_b_q5_tangent_plane.py`는 4차 곡면과
이동하는 평면의 접촉을 단면과 함께 표시합니다. d=3/2에서 접하며 접점의 K=1입니다.

```powershell
python .\supplement_exam\exam_2019_b_q5_tangent_plane.py --output .\output\exam_2019_b_q5.html --no-show
```

2019학년도 1차 A 6번 `exam_2019_a_q6_planar_cubic.py`는 평면 z=x-1 위의
곡선과 상수 a에 따른 p의 곡률을 비교합니다. a=3일 때 곡률이 3입니다.

```powershell
python .\supplement_exam\exam_2019_a_q6_planar_cubic.py --output .\output\exam_2019_a_q6.html --no-show
```

2018학년도 1차 B 5번 `exam_2018_b_q5_normal_curvature.py`는 회전면 z=1/r의
주방향과 지정된 단위벡터 w의 법곡률을 비교합니다. 슬라이더의 w 위치가 문제의 조건입니다.

```powershell
python .\supplement_exam\exam_2018_b_q5_normal_curvature.py --output .\output\exam_2018_b_q5.html --no-show
```

2018학년도 1차 A 6번 `exam_2018_a_q6_orthogonal_vectors.py`는 대표 평면 원과
beta''의 벡터 분해를 표시합니다. 곡률 슬라이더에서 1/4일 때 직교 조건이 성립합니다.

```powershell
python .\supplement_exam\exam_2018_a_q6_orthogonal_vectors.py --output .\output\exam_2018_a_q6.html --no-show
```

2017학년도 1차 B 5번 `exam_2017_b_q5_sphere_cylinder.py`는 반구와 원기둥의
교선, xy 투영과 q=(0,0,2)의 곡률 분해를 표시합니다. q에서 측지곡률의 절댓값은 1입니다.

```powershell
python .\supplement_exam\exam_2017_b_q5_sphere_cylinder.py --output .\output\exam_2017_b_q5.html --no-show
```

2017학년도 1차 A 8번 `exam_2017_a_q8_tangent_normal.py`는 원곡선의 T,N과
위치벡터 β=T/2+N의 합을 나란히 표시합니다. 고정 축척의 슬라이더에서 s=1을 확인할 수 있습니다.

```powershell
python .\supplement_exam\exam_2017_a_q8_tangent_normal.py --output .\output\exam_2017_a_q8.html --no-show
```

2016학년도 1차 B 5번 `exam_2016_b_q5_cone_geodesic.py`는 원뿔의 측지선과
90도 부채꼴 전개도를 비교합니다. 슬라이더는 두 화면의 대응점을 같은 호길이로 이동합니다.

```powershell
python .\supplement_exam\exam_2016_b_q5_cone_geodesic.py --output .\output\exam_2016_b_q5.html --no-show
```

2015학년도 1차 B 3번은 `exam_2015_b_q3_principal_curvature.py`에서 4차 회전면의
접평면, 주방향과 Euler 공식을 표시합니다. 문제의 곡면 식을 기준으로 계산하며,
제시된 해설의 미분식과의 불일치를 명시합니다.

```powershell
python .\supplement_exam\exam_2015_b_q3_principal_curvature.py --output .\output\exam_2015_b_q3.html --no-show
```

2014학년도 12번 `exam_2014_q12_boundary_curvature.py`는 포물면의 반원 영역과
매개변수 영역의 경계를 대응시킵니다. 바깥 반원의 측지곡률 적분은 π/√2이며,
두 자오선의 기여는 0입니다. 슬라이더와 축 범위는 고정된 축척으로 동작합니다.

```powershell
python .\supplement_exam\exam_2014_q12_boundary_curvature.py --output .\output\exam_2014_q12.html --no-show
```

2014학년도 11번 `exam_2014_q11_integrated_normal.py`는 원곡선의 주법선과
이를 적분한 원의 접벡터를 비교합니다. `--tau`로 원곡선의 비틀림을 설정합니다.

```powershell
python .\supplement_exam\exam_2014_q11_integrated_normal.py --tau 1 --output .\output\exam_2014_q11.html --no-show
```

2013학년도 2차 3-2 (II) `exam_2013_second_q3_2_projected_sphere.py`는 사영된
타원체와 q의 주단면을 표시합니다. 방향 슬라이더로 법곡률을 비교하며 K=3을 확인합니다.

```powershell
python .\supplement_exam\exam_2013_second_q3_2_projected_sphere.py --output .\output\exam_2013_second_q3_2.html --no-show
```

2013학년도 1차 34번 `exam_2013_q34_torus_normal_curvature.py`는 토러스와 평면의 교선,
접선 방향에 따른 법곡률을 표시합니다. 제시된 해설의 제2기본형 계수 부호와 달리
직접 계산하면 문제의 방향에서 법곡률은 0입니다. 시각화에도 이 불일치를 명시했습니다.

```powershell
python .\supplement_exam\exam_2013_q34_torus_normal_curvature.py --output .\output\exam_2013_q34.html --no-show
```

2013학년도 1차 33번은 `exam_2013_q33_reflected_helices.py`에서 거울상 원나선의
곡률·비틀림과 Frenet 표구를 비교합니다. 슬라이더로 두 곡선의 대응점을 이동합니다.

```powershell
python .\supplement_exam\exam_2013_q33_reflected_helices.py --output .\output\exam_2013_q33.html --no-show
```

Python 3.10 이상과 NumPy, Plotly가 필요합니다.

```powershell
pip install numpy plotly
python .\supplement_exam\exam_2009_q35_torsion.py
python .\supplement_exam\exam_2009_q36_developable_surface.py
```

브라우저를 열지 않고 공유 가능한 단일 HTML 파일로 저장할 수도 있습니다.

```powershell
python .\supplement_exam\exam_2009_q35_torsion.py --output .\output\exam_2009_q35.html --no-show
python .\supplement_exam\exam_2009_q36_developable_surface.py --output .\output\exam_2009_q36.html --no-show
```

## 기여

작업은 별도의 브랜치에서 진행하고, 완료한 변경 사항은 Pull Request를 통해
`main` 브랜치에 병합합니다.
