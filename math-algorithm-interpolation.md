# 수학/알고리즘 — 보간·변환·곡선

> 상위 노트: [[math-algorithm-notes]] (전체 인덱스 디스패처)
> 다루는 축: 선형보간·비선형·곡선·회전·좌표변환
> 다루지 않는 축: [[math-algorithm-probability|수학/알고리즘 — 확률·통계·집합]] / [[math-algorithm-spatial-algo|수학/알고리즘 — 공간·알고리즘]]

---


## 태그 목록

### 분야
- `#선형대수` `#보간` `#곡선` `#확률` `#변환` `#이산` `#기하` `#해싱` `#노이즈` `#수치해석`

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
| 9 | Easing Functions (Quad/Cubic/Elastic/Back) | `#보간` | 시간 t를 비선형 변환해 가속/감속 곡선 생성 | `#언어독립` |
| 10 | Bezier / Hermite 곡선 | `#보간` `#곡선` | 제어점 기반 부드러운 곡선 (경로/애니메이션) | `#언어독립` |

---

# 풀노트

## 1. 선형 보간 (Lerp)

_두 값 사이를 비율 `t∈[0,1]`로 섞는 가장 기본적인 보간. `Lerp(a, b, t) = a + (b - a) * t`_

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

⚠ **주의점**
- **프레임률 의존성**: `Lerp(a, b, 0.1)`을 매 프레임 호출하면 60fps와 30fps에서 결과가 다르다. 정확하려면 `t = 1 - pow(1 - rate, dt)` 또는 SmoothDamp 같은 함수 사용
- **각도 보간 함정**: 두 각도(0°와 350°) 사이 Lerp는 큰 쪽으로 돌아간다. 짧은 방향 보간이 필요하면 `LerpAngle` 또는 `Slerp` 사용
- **clamped vs unclamped**: `t > 1` 또는 `t < 0`이 의도된 외삽인지 확인. 빌트인은 자동 clamp하는 경우가 많아 외삽 의도 시 명시적 함수(`LerpUnclamped` 등) 필요


#보간 `#O(1)` #결정론 #수치매핑 #게임필
> 종속성: `#언어독립` `#엔진독립`

---

## 2. Linear↔dB 로그 변환 (20·log₁₀)

_인간 청각의 로그 특성을 선형 슬라이더 값(0~1)에 매핑하는 변환. `dB = 20 · log₁₀(linear)`, 역변환 `linear = 10^(dB/20)`._

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

⚠ **주의점**
- **log10(0) = -∞ 처리 필수** — `if (linear <= 0) return -80f;` 없으면 NaN/Infinity가 AudioMixer에 전달됨. Unity는 이 경우 파라미터가 locked 상태가 되어 이후 SetFloat도 무시되는 버그 발생
- **바닥값 -80dB 관행** — AudioMixer의 기본 최솟값. `-80dB ≈ 1/10000 진폭`이므로 실용적 무음. -144dB 등 극단값 전달 시 일부 Unity 버전에서 오동작
- **`Mathf.Log10` vs `Mathf.Log` 혼동** — `Mathf.Log(v)` = 자연로그(ln). dB 계산에는 `Mathf.Log10(v)` 필수
- **역변환 필요 시** — 현재 dB를 읽어 UI를 업데이트할 때 `AudioMixer.GetFloat` + `DBToLinear`로 슬라이더 복원 필요
- **PlayerPrefs 저장** — 볼륨을 저장할 때 *선형*(0~1)으로 저장하고 로드 시 dB 변환 권장. dB 저장 후 역변환 시 -∞ 처리가 복잡해짐


#변환 #오디오 `#O(1)` #결정론 #밸런싱
> 관련: [[game-technique-notes]] 항목 6 AudioMixer Linear→dB (Unity 적용), [[unity-feature-notes]] 항목 14 AudioMixer, 항목 27 Mathf.Log10 | 종속성: `#언어독립` (수학), 적용은 `#오디오엔진`

---

## 3. Clamp / Clamp01 정규화

값을 [min, max] 범위로 강제(Clamp)하거나 [0, 1]로 정규화(Clamp01). 입력이 경계를 초과해도 안전한 폐구간 보장.

**설명**
대부분의 게임 시스템은 입력이 예상 범위를 초과해도 정상 동작해야 한다. 체력이 maxHP를 넘으면 maxHP로, 볼륨 슬라이더가 1을 넘으면 1로, 퍼센트가 음수면 0으로. Clamp는 이 *안전 경계*를 단순명료하게 만든다.

Clamp와 정규화의 차이:
- **Clamp**: v in [a, b] 유지. v가 a 미만 -> a, b 초과 -> b. 경계의 물리적 의미 유지
- **Clamp01**: v를 [0, 1]로 clamp. 확률, t값, 정규화 계수 보호에 특화
- **정규화(Normalize)**: v를 t = (v - min) / (max - min) 변환으로 [0, 1]로 매핑. Clamp와 달리 *선형 변환*

게임 대표 사용:
- 체력/마나 배럭 (Clamp: health = Clamp(health, 0, maxHP))
- 확률/퍼센트 안전망 (Clamp01: dropRate = Clamp01(dropRate + buff))
- 입력 범위 일반화 (정규화: t = (diceRoll - 1) / (20 - 1) -> Lerp(minDmg, maxDmg, t))
- 색상 채널 (Clamp01: RGB 각 채널 [0, 1] 유지)
- Lerp의 t값 안전망 (Clamp01: value = Lerp(a, b, Clamp01(t)))

**구현**
```
function Clamp(value, min, max):
    return max(min, min(max, value))

function Clamp01(value):
    return Clamp(value, 0, 1)

function SafeRemap(x, inMin, inMax, outMin, outMax):
    t = (x - inMin) / (inMax - inMin)
    return Lerp(outMin, outMax, Clamp01(t))
```

엔진별 빌트인:
- Unity: Mathf.Clamp(v, min, max), Mathf.Clamp01(v)
- Unreal: FMath::Clamp(v, min, max)
- C#: Math.Clamp(v, min, max) (.NET 6+)

경고 주의점:
- min > max인 경우 -- Unity Mathf.Clamp는 min > max이면 return min. 호출 전 검증
- inMin == inMax 0나누기 -- SafeRemap에서 (x - inMin) / 0 = Infinity. if (inMax == inMin) return outMin 가드
- 정규화 != Clamp -- (v - min) / (max - min)은 출력이 [0, 1]을 초과할 수 있음. Clamp 생략 금지
- 성능 -- JIT/AOT에서 branch는 무료. 가독성 우선


#변환 #안전 `#O(1)` #결정론
> 관련: [[math-algorithm-notes]] 항목 1 Lerp (Remap의 백본) | 종속성: `#언어독립`

---

## 4. 멱함수 곡선 (x^n, Power-Law)

입력 x in [0,1]에 지수 n을 적용한 곡선. f(x) = x^n. n > 1: 볼록(초반 완만 후반 가파름), n < 1: 오목(초반 급상승 후반 수렴), n = 1: 선형.

**설명**
선형이 항상 정답은 아니다의 첫 교과서. 선형은 변화율이 일정해 시각적으로 단조롭다. 멱함수는 지수 n 하나로 곡선의 성격을 바꾼다.

n별 형태:
| n | 형태 | 게임 의도 |
|---|------|----------|
| < 1 (0.3~0.7) | 오목 (Concave) | 초반 빠른 수익 -> 후반 체감 둔화. 신규 유저 동기 부여 |
| = 1 | 직선 (Linear) | 균등 변화. 기준점 |
| 2~3 | 볼록 (Convex) | 초반 느림 -> 후반 폭발. 하드 컨텐츠/과금 포인트 |
| 5+ | 초반 거의 0 | 극단적 후반 편중. 특수 목적 외 사용 드묾 |

게임 대표 사용:
- 강화 곡선 -- 강화 레벨당 스탯 증가량. n = 0.5~0.7: 초반 효율 좋음 -> 후반 수렴
- 레벨업 필요 경험치 -- n = 1.5~2: 레벨당 필요 경험치 가파르게 상승
- 난이도 커브 -- n = 1.2~1.5: 후반 난이도만 급증
- 거리 감쇠 -- n = 2: 1/d^2 역제곱 법칙 (현실 물리), n = 1: 1/d (게임에서 더 관용적)

**구현**
```
function PowerCurve(x, n):
    return pow(x, n)

function CurveStat(step, maxStep, base, max, n):
    t = step / maxStep
    curve = pow(t, n)
    return Lerp(base, max, curve)
```

Unity C#:
```
float t = (float)currentLevel / maxLevel;
float damageMult = Mathf.Lerp(1f, 5f, Mathf.Pow(t, 0.7f));

float cost = Mathf.Lerp(100f, 10000f, Mathf.Pow(t, 2f));
```

경고 주의점:
- pow(0, 0)는 1 -- 일부 언어에서 0^0 = 1 (C# 포함). 대부분 게임 컨텍스트에서 자연스러움
- n 값 해석 혼동 -- n = 2가 '2배 빠른 성장'이 아님. 곡선 형태가 달라지는 것
- pow 성능 -- Mathf.Pow는 곱셈보다 느림. n이 정수(2, 3, 4)면 x*x, x*x*x로 대체 가능
- n < 0 금지 -- x = 0에서 pow(0, -n) = +inf. 게임에서 거의 사용 안 함
- 비용 + 수익 조합 -- 비용 곡선 n > 1과 수익 곡선 n < 1을 분리하면 전형적 수익체감 구조 완성


#곡선 #밸런싱 `#O(1)` #결정론
> 관련: [[game-technique-notes]] 항목 3 Power-Law 강화 곡선, [[math-algorithm-notes]] 항목 1 Lerp | 종속성: `#언어독립`

---

## 9. Easing Functions (이징 함수)

_선형 시간 `t ∈ [0, 1]`을 비선형으로 변환해 가속/감속 곡선 생성. `Lerp(a, b, ease(t))`로 모든 보간에 적용._

**설명**
선형 이동(Linear)은 시각적으로 기계적으로 느껴진다. 물체가 자연스럽게 움직이려면 시작·끝에서 가속/감속이 필요. Easing Function은 `t → t'` 매핑으로 그 곡선을 만든다.

세 기본 타입:
- **Ease-In**: 시작 느리고 끝에서 빠름 (운동 가속)
- **Ease-Out**: 시작 빠르고 끝에서 느림 (관성으로 멈춤 — 가장 자연스러운 UI 전환)
- **Ease-In-Out**: 양쪽 모두 감속 (S커브)

**부드러운 이징의 수학적 조건**
등속(Linear)이 부자연스러운 이유는 시작·끝 순간에 속도가 즉시 점프하기 때문. "자연스럽다"는 조건을 수학으로 표현하면:
- **1차 부드러움** — 시작·끝 속도(1차 도함수 f') = 0. 가장 단순한 다항식: `Smoothstep = 3t² - 2t³`
- **2차 부드러움** — 시작·끝 가속도(2차 도함수 f'')까지 = 0. `Smootherstep = 6t⁵ - 15t⁴ + 10t³`

조건이 높을수록 양 끝이 더 부드럽고, 중간 구간 속도 변화가 더 극적이 됨.

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

// Bounce — 낙하+반동을 포물선 4구간으로 근사 (n1=7.5625, d1=2.75)
EaseOutBounce(t):
    if t < 1/2.75:      return 7.5625 * t * t
    elif t < 2/2.75:    t -= 1.5/2.75;   return 7.5625 * t * t + 0.75
    elif t < 2.5/2.75:  t -= 2.25/2.75;  return 7.5625 * t * t + 0.9375
    else:               t -= 2.625/2.75; return 7.5625 * t * t + 0.984375
    // 각 구간이 포물선 하나 = 물리적 반동 1회. 4번 튀기며 수렴

// Smoothstep — f'(0)=f'(1)=0 (시작·끝 속도 0)
Smoothstep(t)   = 3t² - 2t³

// Smootherstep — f'(0)=f'(1)=0, f''(0)=f''(1)=0 (속도+가속도 모두 0)
Smootherstep(t) = 6t⁵ - 15t⁴ + 10t³    // Perlin Noise fade 함수와 동일 (항목 11 참조)
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
- Unity: `AnimationCurve.Evaluate(t)` — Inspector에서 곡선 직접 편집 가능 ([[unity-feature-notes]] 항목 35)
- DOTween: `Ease.OutQuad`, `Ease.InBack` 등 Penner 계열 내장
- CSS: `cubic-bezier(x1,y1,x2,y2)` (다른 표현법이지만 동일 결과)

⚠ **주의점**
- **Ease-In vs Ease-Out 혼동** — UI 팝업 *등장*은 Ease-Out (빠르게 나타나 자리 안착), *사라짐*은 Ease-In (천천히 당겼다 빠르게 나감). 반대로 하면 어색함
- **`t` 범위 초과** — `elapsed > duration`이면 `t > 1`. Penner 함수는 t > 1 정의 밖. `Clamp01(t)` 필수
- **Elastic/Back 오버슈팅** — `t ∈ [0,1]`이어도 출력이 [0,1] 범위 초과 (Back: -0.1~1.1). 색상/알파 등 경계가 의미있는 값에 주의
- **AnimationCurve가 실용적** — Unity에서는 Penner 함수 직접 구현보다 `AnimationCurve` Inspector 편집이 더 유연하고 디자이너 조정 가능. 단, `Evaluate` 반복 호출 비용이 있으므로 대량 호출 시 측정 필요
- **프레임률 독립성** — `t = elapsed/duration` 구조라 dt를 올바르게 누적하면 프레임률 독립. `Lerp(current, target, 0.1)` 매 프레임 방식([[math-algorithm-notes]] 항목 1)과는 다른 개념


#보간 #게임필 #UI #애니메이션
> 관련: [[math-algorithm-notes]] 항목 1 Lerp (이징의 백본), 항목 10 Bezier/Hermite 곡선 (실무 대안 — 베지에로 이징 근사), 항목 11 Perlin Noise (Smootherstep = Perlin fade 함수 `6t⁵-15t⁴+10t³` 동일), [[unity-feature-notes]] 항목 35 AnimationCurve | 종속성: `#언어독립` `#엔진독립` (개념). Unity `AnimationCurve`는 `#Unity전용`
---

---

---

## 10. Bezier / Hermite 곡선

_제어점(control points) 기반의 매개변수 곡선. Bezier: de Casteljau 알고리즘으로 점진적 보간. Hermite: 시작/끝 위치 + 접선(tangent)으로 곡선 정의._

**설명**
두 점 사이를 부드럽게 연결하는 방법은 Lerp(직선) 외에도 무한히 많다. Bezier와 Hermite는 곡선의 형태를 제어하는 추가 파라미터를 제공한다.

Bezier 곡선:
- 2차 Bezier (3점): B(t) = (1-t)^2 * P0 + 2(1-t)t * P1 + t^2 * P2
- 3차 Bezier (4점): B(t) = (1-t)^3 * P0 + 3(1-t)^2*t * P1 + 3(1-t)*t^2 * P2 + t^3 * P3
- 제어점을 움직여 곡선 형태 조정. 게임 경로/UI/폰트에 광범위 사용
- Unity AnimationCurve가 3차 Bezier 기반

Hermite 곡선:
- H(t) = (2t^3 - 3t^2 + 1) * P0 + (-2t^3 + 3t^2) * P1 + (t^3 - 2t^2 + t) * T0 + (t^3 - t^2) * T1
- 시작점 P0, 끝점 P1, 시작 접선 T0, 끝 접선 T1으로 곡선 정의
- 접선(tangent)을 직접 제어하므로 지정된 방향으로 부드럽게 연결할 때 유리
- Catmull-Rom Spline: Hermite의 변형으로 제어점이 접선을 자동 계산

게임 대표 사용:
- 카메라 경로 (스크립트된 무비 시퀀스)
- UI 모션 경로 (팝업 등장 궤적)
- 길찾기 경로 부드럽게 연결
- 2D/3D 곡선 도로, 레일

**구현**
```
function BezierQuad(p0, p1, p2, t):
    return (1-t)*(1-t)*p0 + 2*(1-t)*t*p1 + t*t*p2

function BezierCubic(p0, p1, p2, p3, t):
    u = 1-t
    return u*u*u*p0 + 3*u*u*t*p1 + 3*u*t*t*p2 + t*t*t*p3

function Hermite(p0, p1, t0, t1, t):
    t2 = t*t
    t3 = t2*t
    h1 = 2*t3 - 3*t2 + 1
    h2 = -2*t3 + 3*t2
    h3 = t3 - 2*t2 + t
    h4 = t3 - t2
    return h1*p0 + h2*p1 + h3*t0 + h4*t1
```

경고 주의점:
- 제어점 배치 난이도 -- Bezier 제어점을 예측 가능한 곡선으로 배치하는 것은 직관적이지 않음. 에디터 도구(Unity Scene View 핸들) 필수
- t 균등 샘플링은 등속 아님 -- t에 등간격으로 샘플링하면 곡선의 곡률에 따라 속도가 변함. 등속 경로는 t를 호 길이로 재매개변수화 필요
- Hermite 접선 크기가 곡선 형태 결정 -- 접선이 너무 짧으면 곡선이 거의 직선, 너무 길면 과도한 루프. 통상 시작/끝 거리의 1/3 권장
- 고차 Bezier(5점+)는 수치 불안정 -- 4점(3차) 이상은 de Casteljau로 분할하거나 B-Spline 사용 고려


#보간 #곡선 `#O(1)` #결정론
> 종속성: `#언어독립`