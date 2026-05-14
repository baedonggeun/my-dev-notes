# 수학 / 알고리즘 노트

> 다루는 축: 수학 빌딩블록과 알고리즘. 여러 *기법*이 공유하는 한 단계 아래 도구
> 다루지 않는 축: 빌딩블록의 게임 응용(→ [[game-technique-notes]]), 엔진 API 형태(→ [[unity-feature-notes]])
> 적용 범위: 언어/엔진 완전 독립 — 가장 portable한 노트
> 관련 노트: [[game-technique-notes]] (수학 응용 기법), [[unity-feature-notes]] #27 (Mathf 빌트인)
> 평생 노트 정책: 인덱스 표는 portable, 풀노트는 공식 + 의사코드 + 주의점
> 승격 임계치: 일반 지식 섹션이 30개 이상 누적 시 카테고리 분리 검토
> 풀노트 작성 기준 (둘 이상 해당 시):
>   - 코드만 봐선 "왜 이렇게 했는지" 안 보이는 정성적 이유가 있다
>   - 다른 프로젝트/맥락에서도 재사용 가능한 일반 원리다
>   - 자주 잊는 함정/엣지케이스가 있다
>   - 응용 사례가 3개 이상이다
> 작성 시작: 2026-05-15

---

## 태그 목록

### 분야
- `#선형대수` `#보간` `#곡선` `#확률` `#변환` `#이산` `#기하` `#해싱` `#노이즈`

### 응용
- `#게임필` `#밸런싱` `#오디오` `#UI좌표` `#가챠` `#시너지` `#렌더링`

### 복잡도
- `#O(1)` `#O(logN)` `#O(N)` `#O(NlogN)`

### 결정성
- `#결정론` `#확률적` `#근사`

---

## 인덱스

### 본 프로젝트에서 사용 중
| # | 알고리즘/공식 | 분야 | 한 줄 요약 | 종속성 |
|---|--------|------|----------|--------|
| 1 | 선형 보간 (Lerp) | `#보간` | 두 값을 비율 t로 섞는 가장 기본적 보간 | `#언어독립` `#엔진독립` |
| 2 | Linear↔dB 로그 변환 (20·log10) | `#변환` `#오디오` | 인간 청각의 로그 특성을 선형 슬라이더로 매핑 | `#언어독립` |
| 3 | Clamp / Clamp01 정규화 | `#변환` | 값을 [min, max] 또는 [0, 1] 범위로 강제 | `#언어독립` |
| 4 | 멱함수 곡선 (x^n, Power-Law) | `#곡선` `#밸런싱` | 입력에 지수를 적용해 가파른/완만한 성장 곡선 생성 | `#언어독립` |
| 5 | 가중 랜덤 (Weighted Random Sampling) | `#확률` `#가챠` | 항목별 가중치에 비례한 확률로 선택 | `#언어독립` |
| 6 | Pity 누적 시프트 (Cumulative Probability Shift) | `#확률` `#가챠` | 실패 누적 시 확률 점진 증가, 임계점 도달 시 보장 | `#언어독립` |
| 7 | Vector2 거리/방향 (벡터 산술) | `#선형대수` `#UI좌표` | 두 점 사이 거리/단위 방향 벡터 계산 | `#언어독립` |
| 8 | HashSet 유니크 카운트 (집합 연산) | `#이산` `#시너지` | O(1) 평균 시간으로 중복 제거 + 카운트 | `#언어독립` |

### 일반 지식 (참고용 — 본 프로젝트 미사용)
| # | 알고리즘/공식 | 분야 | 한 줄 요약 | 종속성 |
|---|--------|------|----------|--------|
| 9 | Easing Functions (Quad/Cubic/Elastic/Back) | `#보간` | 시간 t를 비선형 변환해 가속/감속 곡선 생성 | `#언어독립` |
| 10 | Bezier / Hermite 곡선 | `#보간` `#곡선` | 제어점 기반 부드러운 곡선 (경로/애니메이션) | `#언어독립` |
| 11 | Perlin / Simplex Noise | `#노이즈` `#근사` | 결정론적 의사 랜덤 노이즈 필드 (지형/텍스처) | `#언어독립` |
| 12 | A* 경로 탐색 | `#이산` `#기하` | 휴리스틱 기반 최단 경로 탐색 | `#언어독립` |
| 13 | Quaternion 회전 (Slerp) | `#선형대수` | 짐벌락 없는 회전 보간 | `#언어독립` |
| 14 | 공간 분할 (Quadtree / Spatial Hash) | `#기하` `#해싱` | 공간 영역 인덱싱으로 충돌/검색 가속 | `#언어독립` |
| 15 | 정규분포 샘플링 (Box-Muller) | `#확률` | 균등 난수 2개로 정규분포 난수 생성 | `#언어독립` |
| 16 | Reservoir Sampling | `#확률` `#O(N)` | 크기 미상 스트림에서 균등 확률로 N개 샘플 | `#언어독립` |

---

## 1. 선형 보간 (Lerp)

**한 줄 요약**
두 값 사이를 비율 `t∈[0,1]`로 섞는 가장 기본적인 보간. `Lerp(a, b, t) = a + (b - a) * t`

**설명**
선형 보간은 두 값 `a`, `b` 사이의 중간값을 비율 `t`로 결정한다. `t=0`이면 `a`, `t=1`이면 `b`, `t=0.5`면 정확히 중간. 단순해 보이지만 게임에서 압도적으로 자주 쓰이는 빌딩블록.

대표 용도:
- **수치 매핑** — 임의 입력 범위(예: 굴림 1~20)를 출력 범위(예: 데미지 min~max)로 선형 변환
- **부드러운 추적** — `pos = Lerp(pos, target, rate * dt)` 형태로 매 프레임 일정 비율 접근 (지수적 감속 효과)
- **색/알파 페이드** — UI 트랜지션
- **트윈 백본** — 모든 ease 함수가 결국 `Lerp(a, b, ease(t))` 형태로 환원

**구현**
```
function Lerp(a, b, t):
    return a + (b - a) * t

// 입력 범위 [in_min, in_max]를 출력 [out_min, out_max]로 매핑
function Remap(x, in_min, in_max, out_min, out_max):
    t = (x - in_min) / (in_max - in_min)
    return Lerp(out_min, out_max, t)

// 프레임률 독립 추적 (지수적 감속)
function FrameRateIndependentLerp(current, target, rate, dt):
    t = 1 - pow(1 - rate, dt)
    return Lerp(current, target, t)
```

엔진별 빌트인:
- Unity: `Mathf.Lerp(a, b, t)` (t 자동 clamp), `Mathf.LerpUnclamped` (외삽 허용)
- Unreal: `FMath::Lerp`
- 셰이더: `mix(a, b, t)` (GLSL), `lerp(a, b, t)` (HLSL)

**주의점**
- **프레임률 의존성**: `Lerp(a, b, 0.1)`을 매 프레임 호출하면 60fps와 30fps에서 결과가 다르다. 정확하려면 `t = 1 - pow(1 - rate, dt)` 또는 SmoothDamp 같은 함수 사용
- **각도 보간 함정**: 두 각도(0°와 350°) 사이 Lerp는 큰 쪽으로 돌아간다. 짧은 방향 보간이 필요하면 `LerpAngle` 또는 `Slerp` 사용
- **clamped vs unclamped**: `t > 1` 또는 `t < 0`이 의도된 외삽인지 확인. 빌트인은 자동 clamp하는 경우가 많아 외삽 의도 시 명시적 함수(`LerpUnclamped` 등) 필요

**메타**
- 종속성: `#언어독립` `#엔진독립`
- 첫 도출: CasualStrategy (2026-05-15)
- 태그: `#보간` `#O(1)` `#결정론` `#수치매핑` `#게임필`

---

## 항목별 노트 (#2~#16)
*풀 4블록 노트는 요청 시 작성. 위 인덱스 표가 SOT.*

---

## 분류 메모

- **수학 vs 기법 경계**: Lerp는 *수학*이고, "D20 굴림을 데미지에 Lerp" 는 *기법*([game-technique-notes.md](game-technique-notes.md) #5). 같은 Lerp가 카메라 추적에도 쓰이므로 한 단계 아래에 둔다.
- **수학 vs Unity API 경계**: `Mathf.Lerp`는 Unity API([unity-feature-notes.md](unity-feature-notes.md) #27)이지만, "선형 보간"이라는 개념은 엔진 독립적. 본 노트는 *개념*에 집중.
- **승격 후보**: 일반 지식 섹션(#9~#16)이 본 프로젝트에 도입되면 "사용 중" 표로 이동.

### 다관점 분리 그룹 (의도된 cross-ref)
같은 코드 사례를 *수학 개념 / 게임 기법 / Unity API* 세 축에서 본다. 어느 한 곳이 SOT가 아니라 축별 진입점이 다르다.

| 공통 주제 | math (개념) | game-technique (응용) | unity-feature (API) |
|---|---|---|---|
| 선형 보간 | #1 Lerp | #5 D20 데미지 | #27 Mathf |
| dB 변환 | #2 Linear↔dB | #6 AudioMixer 지각 변환 | #14 AudioMixer / #27 Mathf.Log10 |
| 멱함수 | #4 Power-Law | #3 강화 보상 곡선 | — |
| 가중 랜덤 + Pity | #5, #6 | #2 가챠 등급 보정 | — |
| 벡터 산술 | #7 Vector2 | — | #27 Mathf (Vector2/3) |
| 집합 카운팅 | #8 HashSet | #4 Unique-ID Synergy | — |

### 통합/제거된 항목
- **단조증가 SortingOrder** → [game-misc-notes.md](game-misc-notes.md) #3 SortingOrder 레이어 상수가 SOT (수학적 색채 약함)
- **비대칭 적분 (Variable Gravity)** → [game-technique-notes.md](game-technique-notes.md) #1 Asymmetric Jump가 SOT (응용 기법 자체)

---
