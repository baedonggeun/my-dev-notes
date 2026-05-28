# 수학 / 알고리즘 노트

> 다루는 축: 수학 빌딩블록과 알고리즘. 여러 *기법*이 공유하는 한 단계 아래 도구
> 다루지 않는 축: 빌딩블록의 게임 응용(→ [[game-technique-notes]]), 엔진 API 형태(→ [[unity-feature-notes]])
> 적용 범위: 언어/엔진 완전 독립 — 가장 portable한 노트
> 관련 노트: [[game-technique-notes]] (수학 응용 기법), [[unity-feature-notes]] #27 (Mathf 빌트인)
> 평생 노트 정책: 인덱스 표는 portable, 풀노트는 공식 + 의사코드 + 주의점
> 승격 임계치: 일반 지식 섹션이 30개 이상 누적 시 카테고리 분리 검토
> 풀노트 작성 기준: 인덱스 1줄만으로 구현/적용이 불충분한 항목. 자명한 항목만 인덱스로 종료
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

# 인덱스

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

# 풀노트

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

## 2. Linear↔dB 로그 변환 (20·log₁₀)

**한 줄 요약**
인간 청각의 로그 특성을 선형 슬라이더 값(0~1)에 매핑하는 변환. `dB = 20 · log₁₀(linear)`, 역변환 `linear = 10^(dB/20)`.

**설명**
소리의 진폭(amplitude)과 인간이 *지각하는* 크기는 선형 비례가 아니라 로그 비례다. 슬라이더를 0.5(50%)로 놓으면 "반쯤 들린다"가 아니라 "약간 줄었다"는 느낌이 난다 — 이를 보정하는 것이 dB 변환.

**왜 20이고 10이 아닌가**:
- 전력(power) 기준: `dB = 10 · log₁₀(P₂/P₁)`
- 음압/진폭(amplitude) 기준: `dB = 20 · log₁₀(A₂/A₁)`
- 이유: `P ∝ A²` → `10 · log₁₀(A²) = 20 · log₁₀(A)`. 오디오 슬라이더는 *진폭* 제어이므로 20 사용.

게임 대표 사용:
- BGM/SFX 볼륨 슬라이더 (0~1 선형 → dB 로그 변환 → AudioMixer 파라미터)
- 마스터 볼륨 컨트롤
- 커스텀 거리 감쇠 설계

**구현**
```
// 선형 슬라이더(0~1) → dB
function LinearToDB(linear):
    if linear <= 0:
        return -80.0    // -∞ 방지 — 무음 바닥값
    return 20.0 * log10(linear)

// dB → 선형
function DBToLinear(dB):
    return 10.0 ^ (dB / 20.0)

// Unity AudioMixer 적용 예
AudioMixer.SetFloat("MasterVolume", LinearToDB(sliderValue))
```

엔진별 빌트인:
- Unity: `Mathf.Log10(v) * 20f` (log10 직접), `AudioMixer.SetFloat(param, db)` 범위는 통상 -80~0
- Unity AudioMixer Exposed Parameter는 *dB 단위*로 받음 — 선형 값 직접 주면 잘못된 결과

**주의점**
- **log10(0) = -∞ 처리 필수** — `if (linear <= 0) return -80f;` 없으면 NaN/Infinity가 AudioMixer에 전달됨. Unity는 이 경우 파라미터가 locked 상태가 되어 이후 SetFloat도 무시되는 버그 발생
- **바닥값 -80dB 관행** — AudioMixer의 기본 최솟값. `-80dB ≈ 1/10000 진폭`이므로 실용적 무음. -144dB 등 극단값 전달 시 일부 Unity 버전에서 오동작
- **`Mathf.Log10` vs `Mathf.Log` 혼동** — `Mathf.Log(v)` = 자연로그(ln). dB 계산에는 `Mathf.Log10(v)` 필수
- **역변환 필요 시** — 현재 dB를 읽어 UI를 업데이트할 때 `AudioMixer.GetFloat` + `DBToLinear`로 슬라이더 복원 필요
- **PlayerPrefs 저장** — 볼륨을 저장할 때 *선형*(0~1)으로 저장하고 로드 시 dB 변환 권장. dB 저장 후 역변환 시 -∞ 처리가 복잡해짐

**메타**
- 종속성: `#언어독립` (수학), 적용은 `#오디오엔진`
- 관련 노트: [[game-technique-notes]] #6 AudioMixer Linear→dB (Unity 적용), [[unity-feature-notes]] #14 AudioMixer, #27 Mathf.Log10
- 첫 도출: CasualStrategy (2026-05-15) — SoundManager dB 볼륨 제어
- 태그: `#변환` `#오디오` `#O(1)` `#결정론` `#밸런싱`

---

## 5. 가중 랜덤 (Weighted Random Sampling)

**한 줄 요약**
항목별 가중치에 비례한 확률로 하나를 선택. 총합 `R = Σw_i`, 균등 랜덤 `r ∈ [0, R)`, 누적합이 r을 처음 초과하는 항목 반환.

**설명**
균등 랜덤이 모든 항목을 동일 확률로 뽑는다면, 가중 랜덤은 가중치 비율만큼 뽑힌다. 드롭 테이블, 가챠 등급, 스폰 확률, BGM 선택 등 게임 핵심 확률 메커니즘.

두 가지 구현 전략:
1. **선형 탐색 (O(N))** — 가중치 배열 순회하며 누적합. 단순, 항목 수 ~100 이하에서 충분
2. **Alias Method (O(1) 샘플링)** — O(N) 전처리 후 O(1) 샘플링. 항목 수 1000+ 또는 매 프레임 고빈도 호출 시

게임 대표 사용:
- 가챠 등급 확률 (UR 0.3%, SR 5%, R 20%, N 74.7%)
- 몬스터 드롭 아이템 (희귀 아이템 낮은 가중치)
- 맵 랜덤 스폰 위치 (특정 구역 가중치 ↑)
- 랜덤 배경음악 (덜 자주 듣고 싶은 트랙 가중치 ↓)

**구현**
```
// 선형 탐색 — O(N), 단순
function WeightedRandom(items[], weights[]):
    total = sum(weights)
    r = Random(0, total)    // 0 이상 total 미만
    cumulative = 0
    for i in range(len(items)):
        cumulative += weights[i]
        if r < cumulative:
            return items[i]
    return items[last]      // float 오차 안전망

// Unity C# 예시
float total = weights.Sum();
float r = Random.value * total;
float cumulative = 0f;
for (int i = 0; i < items.Length; i++) {
    cumulative += weights[i];
    if (r < cumulative) return items[i];
}
return items[^1];
```

Alias Method (O(1)):
```
// 전처리: O(N) — 확률을 [작음/큰 것] 쌍으로 분류
function BuildAlias(weights[]):
    n = len(weights)
    probs = [w * n / sum(weights) for w in weights]
    alias = array(n)
    small, large = [], []
    for i, p in enumerate(probs):
        (small if p < 1 else large).append(i)
    while small and large:
        s, l = small.pop(), large.pop()
        alias[s] = l
        probs[l] = probs[l] + probs[s] - 1
        (small if probs[l] < 1 else large).append(l)
    return probs, alias

// 샘플링: O(1)
function SampleAlias(probs, alias):
    i = RandomInt(0, len(probs))
    return i if Random01() < probs[i] else alias[i]
```

**주의점**
- **가중치 정규화 불필요** — total을 계산해 상대 비율로 샘플링하므로 `[1, 2, 3]`이나 `[0.167, 0.333, 0.5]`나 동일. 단, `total == 0` 가드 필수
- **float 누적 오차** — 항목 수 많을수록 `cumulative += weights[i]` 정밀도 저하. 마지막 항목이 뽑히지 않는 버그로 나타남. 마지막 항목 안전망 `return items[^1]` 항상 추가
- **`Random.value` 범위** — Unity `Random.value ∈ [0, 1]` (양 끝 포함). `r == total`인 경우를 위해 마지막 항목 fallback 필수
- **O(N) vs O(1) 분기점** — 항목 수 < 100 + 호출 빈도 낮음 → 선형 탐색으로 충분. 항목 수 1000+ 또는 매 프레임 1000회+ 호출 → Alias Method. CasualStrategy 가챠는 항목 수 ~10이라 선형 탐색 적용
- **가중치 동적 변경** — Alias Method는 가중치 변경 시 재전처리(O(N)) 필요. pity 누적처럼 매 호출마다 가중치가 달라지면 선형 탐색이 더 실용적

**메타**
- 종속성: `#언어독립`
- 관련 노트: [[game-technique-notes]] #2 가챠 Pity 시스템 (응용), [[math-algorithm-notes]] #6 Pity 누적 시프트
- 첫 도출: CasualStrategy (2026-05-15) — 가챠 등급 산출
- 태그: `#확률` `#가챠` `#O(N)` `#확률적`

---

## 6. Pity 누적 시프트 (Cumulative Probability Shift)

**한 줄 요약**
실패 누적 횟수 `n`에 따라 성공 확률을 점진 상승시키고, 임계점(`ceiling`)에서 100%로 보장. 소프트 pity + 하드 pity 2단 구조.

**설명**
순수 고정 확률 시스템은 "10000번 시도해도 안 나옴"이 수학적으로 가능해 사용자 이탈의 직접 원인. Pity는 이 분산을 제어하는 공식 메커니즘.

2단 구조:
- **소프트 pity**: 특정 횟수 이후 확률 점진 증가. "슬슬 나올 것 같다" 기대감 생성
- **하드 pity (천장)**: N번째 시도에서 반드시 지급. 분산의 절대 상한선

확률 함수 모델:
```
P(n) =
    base_rate                                        if n < soft_threshold
    base_rate + (n - soft_threshold) * increment     if soft_threshold ≤ n < hard_ceiling
    1.0                                              if n ≥ hard_ceiling
```

기대 소요 횟수 `E[X]`는 수치 시뮬레이션(Monte Carlo, 10만 회 이상)으로 확인하는 것이 실용적.

게임 사례:
- 원신: 5성 0.6%, soft pity 74번째부터 증가, hard pity 90번
- FGO: SSR 1%, 천장은 간접 구현
- CasualStrategy: Tier별 별도 pity 카운터

**구현**
```
// 상태 (per-pool 저장, 영속)
pityCount = 0

// 매 가챠 시도
function TryGacha(pool) -> Grade:
    p = CalcProbability(pool.baseRate, pityCount,
                        pool.softThreshold, pool.increment, pool.hardCeiling)
    roll = Random01()
    if roll < p:
        pityCount = 0   // 성공 시 리셋
        return pool.GetGrade()
    else:
        pityCount += 1
        return pool.GetFallback()

function CalcProbability(base, n, soft, incr, ceiling):
    if n >= ceiling: return 1.0
    if n >= soft:    return min(1.0, base + (n - soft) * incr)
    return base
```

**주의점**
- **pity 카운터 리셋 타이밍** — 성공 *직후* 리셋. 결과 처리 전 리셋 누락 시 다음 시도도 확률이 오염
- **천장 도달 후 리셋** — `n >= ceiling` 강제 지급 후 `pityCount = 0` 필수. 누락 시 다음 시도도 확률 100%
- **등급별 독립 카운터** — SR pity와 UR pity가 같은 카운터를 공유하면 SR 성공이 UR 카운터를 리셋하는 설계 오류. 각 pool마다 별도 카운터
- **소프트 pity 시작점** — `soft_threshold`를 너무 낮게 잡으면 초반 확률이 급등해 기댓값이 낮아짐. 원신 74/90이 경험적 참조값
- **영속 저장** — pity 카운터는 앱 재시작 후에도 유지 필수. PlayerPrefs 또는 서버 저장. 메모리에만 두면 재시작 시 리셋 (치트 가능)

**메타**
- 종속성: `#언어독립`
- 관련 노트: [[game-technique-notes]] #2 Pity 등급 시프트 (게임 기법 레벨), [[math-algorithm-notes]] #5 가중 랜덤
- 첫 도출: CasualStrategy (2026-05-15)
- 태그: `#확률` `#가챠` `#O(1)` `#결정론`

---

## 9. Easing Functions (이징 함수)

**한 줄 요약**
선형 시간 `t ∈ [0, 1]`을 비선형으로 변환해 가속/감속 곡선 생성. `Lerp(a, b, ease(t))`로 모든 보간에 적용.

**설명**
선형 이동(Linear)은 시각적으로 기계적으로 느껴진다. 물체가 자연스럽게 움직이려면 시작·끝에서 가속/감속이 필요. Easing Function은 `t → t'` 매핑으로 그 곡선을 만든다.

세 기본 타입:
- **Ease-In**: 시작 느리고 끝에서 빠름 (운동 가속)
- **Ease-Out**: 시작 빠르고 끝에서 느림 (관성으로 멈춤 — 가장 자연스러운 UI 전환)
- **Ease-In-Out**: 양쪽 모두 감속 (S커브)

Robert Penner 함수 계열 (사실상 표준):
```
// Quad (t²)
EaseInQuad(t)    = t²
EaseOutQuad(t)   = 1 - (1-t)²
EaseInOutQuad(t) = t < 0.5 ? 2t² : 1 - (-2t+2)²/2

// Cubic, Quart, Quint — 지수만 증가
EaseInCubic(t)   = t³
EaseOutCubic(t)  = 1 - (1-t)³

// Sine — 부드러운 S커브
EaseInSine(t)    = 1 - cos(t * π / 2)
EaseOutSine(t)   = sin(t * π / 2)
EaseInOutSine(t) = -(cos(π * t) - 1) / 2

// Elastic — 스프링 과진동
EaseOutElastic(t) = 2^(-10t) * sin((t*10-0.75) * 2π/3) + 1

// Back — 살짝 반대로 당겼다 가는 느낌 (c1=1.70158)
EaseOutBack(t)   = 1 + (c1+1)*(t-1)³ + c1*(t-1)²

// Bounce — 공 튀기듯 반복 감소 충격
EaseOutBounce(t) = 구간별 포물선 조합
```

**구현**
```
// 범용 적용
function TweenValue(from, to, t, easeFunc):
    return Lerp(from, to, easeFunc(Clamp01(t)))

// Unity — elapsed 기반 t 계산
elapsed += Time.deltaTime
t = Clamp01(elapsed / duration)
value = Lerp(from, to, EaseOutQuad(t))
```

엔진별 빌트인:
- Unity: `AnimationCurve.Evaluate(t)` — Inspector에서 곡선 직접 편집 가능 ([[unity-feature-notes]] #35)
- DOTween: `Ease.OutQuad`, `Ease.InBack` 등 Penner 계열 내장
- CSS: `cubic-bezier(x1,y1,x2,y2)` (다른 표현법이지만 동일 결과)

**주의점**
- **Ease-In vs Ease-Out 혼동** — UI 팝업 *등장*은 Ease-Out (빠르게 나타나 자리 안착), *사라짐*은 Ease-In (천천히 당겼다 빠르게 나감). 반대로 하면 어색함
- **`t` 범위 초과** — `elapsed > duration`이면 `t > 1`. Penner 함수는 t > 1 정의 밖. `Clamp01(t)` 필수
- **Elastic/Back 오버슈팅** — `t ∈ [0,1]`이어도 출력이 [0,1] 범위 초과 (Back: -0.1~1.1). 색상/알파 등 경계가 의미있는 값에 주의
- **AnimationCurve가 실용적** — Unity에서는 Penner 함수 직접 구현보다 `AnimationCurve` Inspector 편집이 더 유연하고 디자이너 조정 가능. 단, `Evaluate` 반복 호출 비용이 있으므로 대량 호출 시 측정 필요
- **프레임률 독립성** — `t = elapsed/duration` 구조라 dt를 올바르게 누적하면 프레임률 독립. `Lerp(current, target, 0.1)` 매 프레임 방식([[math-algorithm-notes]] #1)과는 다른 개념

**메타**
- 종속성: `#언어독립` `#엔진독립` (개념). Unity `AnimationCurve`는 `#Unity전용`
- 관련 노트: [[math-algorithm-notes]] #1 Lerp (이징의 백본), [[unity-feature-notes]] #35 AnimationCurve
- 첫 도출: CasualStrategy (2026-05-28) — 두 번째 만남 확률 최고로 등재. 본 프로젝트는 AnimationCurve 일부 사용, DOTween 미사용
- 태그: `#보간` `#게임필` `#UI` `#애니메이션`

---

*#3, #4, #7, #8, #10~#16 풀노트는 작성 기준 충족 시 추가.*

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
