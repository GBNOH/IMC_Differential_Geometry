# Teacher Recruitment Examination

이 폴더는 교원임용시험(Teacher Recruitment Examination)의 미분기하학 관련 내용을
시각화하는 코드와 자료를 정리하기 위한 공간입니다.

## 목표

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

## 실행

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
