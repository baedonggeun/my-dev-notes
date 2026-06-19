# 수학 / 알고리즘 노트

> 다루는 축: 수학 빌딩블록과 알고리즘. 여러 *기법*이 공유하는 한 단계 아래 도구
> 다루지 않는 축: 빌딩블록의 게임 응용(→ [[game-technique-notes]]), 엔진 API 형태(→ [[unity-feature-notes]])
> 적용 범위: 언어/엔진 완전 독립 — 가장 portable한 노트
> 관련 노트: [[game-technique-notes]] (수학 응용 기법), [[unity-feature-notes]] 항목 27 (Mathf 빌트인)
> 평생 노트 정책: 인덱스 표는 portable, 풀노트는 공식 + 의사코드 + 주의점
> 승격 임계치: 일반 지식 섹션이 30개 이상 누적 시 카테고리 분리 검토
> 풀노트 작성 기준: 인덱스 1줄만으로 구현/적용이 불충분한 항목. 자명한 항목만 인덱스로 종료
> 작성 시작: 2026-05-15

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
| 17 | 오일러 적분 (Euler Integration) | `#수치해석` `#근사` | 현재 상태에 `가속도 × dt`를 반복 누적해 다음 상태를 근사 — 게임 물리 루프의 핵심 빌딩블록. 비대칭 중력처럼 해석적 해가 없는 규칙을 프레임마다 단순 덧셈으로 처리 | `#언어독립` |

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

## 5. 가중 랜덤 (Weighted Random Sampling)

_항목별 가중치에 비례한 확률로 하나를 선택. 총합 `R = Σw_i`, 균등 랜덤 `r ∈ [0, R)`, 누적합이 r을 처음 초과하는 항목 반환._

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

⚠ **주의점**
- **가중치 정규화 불필요** — total을 계산해 상대 비율로 샘플링하므로 `[1, 2, 3]`이나 `[0.167, 0.333, 0.5]`나 동일. 단, `total == 0` 가드 필수
- **float 누적 오차** — 항목 수 많을수록 `cumulative += weights[i]` 정밀도 저하. 마지막 항목이 뽑히지 않는 버그로 나타남. 마지막 항목 안전망 `return items[^1]` 항상 추가
- **`Random.value` 범위** — Unity `Random.value ∈ [0, 1]` (양 끝 포함). `r == total`인 경우를 위해 마지막 항목 fallback 필수
- **O(N) vs O(1) 분기점** — 항목 수 < 100 + 호출 빈도 낮음 → 선형 탐색으로 충분. 항목 수 1000+ 또는 매 프레임 1000회+ 호출 → Alias Method. CasualStrategy 가챠는 항목 수 ~10이라 선형 탐색 적용
- **가중치 동적 변경** — Alias Method는 가중치 변경 시 재전처리(O(N)) 필요. pity 누적처럼 매 호출마다 가중치가 달라지면 선형 탐색이 더 실용적


#확률 #가챠 `#O(N)` #확률적
> 관련: [[game-technique-notes]] 항목 2 가챠 Pity 시스템 (응용), [[math-algorithm-notes]] 항목 6 Pity 누적 시프트 | 종속성: `#언어독립`

## 6. Pity 누적 시프트 (Cumulative Probability Shift)

_실패 누적 횟수 `n`에 따라 성공 확률을 점진 상승시키고, 임계점(`ceiling`)에서 100%로 보장. 소프트 pity + 하드 pity 2단 구조._

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

⚠ **주의점**
- **pity 카운터 리셋 타이밍** — 성공 *직후* 리셋. 결과 처리 전 리셋 누락 시 다음 시도도 확률이 오염
- **천장 도달 후 리셋** — `n >= ceiling` 강제 지급 후 `pityCount = 0` 필수. 누락 시 다음 시도도 확률 100%
- **등급별 독립 카운터** — SR pity와 UR pity가 같은 카운터를 공유하면 SR 성공이 UR 카운터를 리셋하는 설계 오류. 각 pool마다 별도 카운터
- **소프트 pity 시작점** — `soft_threshold`를 너무 낮게 잡으면 초반 확률이 급등해 기댓값이 낮아짐. 원신 74/90이 경험적 참조값
- **영속 저장** — pity 카운터는 앱 재시작 후에도 유지 필수. PlayerPrefs 또는 서버 저장. 메모리에만 두면 재시작 시 리셋 (치트 가능)


#확률 #가챠 `#O(1)` #결정론
> 관련: [[game-technique-notes]] 항목 2 Pity 등급 시프트 (게임 기법 레벨), [[math-algorithm-notes]] 항목 5 가중 랜덤 | 종속성: `#언어독립`

## 7. Vector2 거리/방향 (벡터 산술)

두 점 A(x1, y1), B(x2, y2) 사이의 거리 d = |B - A|와 단위 방향 벡터 dir = (B - A) / |B - A| 계산.

**설명**
벡터는 게임에서 물체 위치, 속도, 방향, 힘 등 모든 이동의 기본 단위.

핵심 연산:
- 뺄셈: v = B - A -- A에서 B로의 벡터
- 거리(크기): |v| = sqrt(v.x^2 + v.y^2) -- 유클리드 거리
- 방향(정규화): v_hat = v / |v| -- 크기가 1인 단위 벡터
- 거리 제곱: |v|^2 = v.x^2 + v.y^2 -- sqrt 생략. 거리 비교에 유용

게임 대표 사용:
- 타겟 추적: dir = (targetPos - myPos).normalized, velocity = dir * speed
- 사거리 판정: if sqrDist < range^2 (제곱으로 sqrt 회피)
- 넉백/투사체: knockbackDir = (hitPos - center).normalized * force
- UI 좌표 차이: 드래그 방향/거리 계산
- AI 시야: dot(forward, dir) > 0.7 -> 시야각 45도 이내

**구현**
```
function Distance(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    return sqrt(dx*dx + dy*dy)

function SqrDistance(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    return dx*dx + dy*dy

function Direction(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    mag = sqrt(dx*dx + dy*dy)
    if mag == 0: return (0, 0)
    return (dx / mag, dy / mag)
```

Unity C#:
```
Vector2 dir = (target.position - transform.position).normalized;
float sqrDist = dir.sqrMagnitude;
float dist = dir.magnitude;
```

경고 주의점:
- 0나누기 (영벡터) -- A == B일 때 |v| = 0 -> direction = NaN, NaN. 정규화 전 if (mag == 0) return Vector2.zero 필수
- sqrt는 비싸다 -- 거리 비교만 필요하면 sqrMagnitude 사용
- 부동소수점 정밀도 -- 매우 가까운 두 점(1e-10 차이)에서 방향이 불안정. sqrMagnitude < epsilon 가드 검토
- Manhattan distance 대안 -- |dx| + |dy|. 그리드 기반 게임에서 정확하고 빠름


#선형대수 `#O(1)` #결정론 #게임필
> 관련: [[unity-feature-notes]] 항목 27 Mathf (Vector2/3 API) | 종속성: `#언어독립`

## 8. HashSet 유니크 카운트 (집합 연산)

HashSet(또는 Set)에 요소를 추가한 후 .Count로 중복 없는 개수를 얻는 기법. O(1) 평균 삽입/탐색.

**설명**
게임에서 "종류가 몇 가지인가"를 세는 일은 빈번하다. 배열에 같은 ID가 여러 번 있어도 한 번만 세고 싶다. HashSet은 내부 해시 테이블로 중복을 자동 제거한다.

작동 원리:
- Add(element) -> 해시 함수로 버킷 계산 -> 이미 있으면 무시, 없으면 추가
- Count -> 저장된 고유 요소 수 반환
- 시간 복잡도: 평균 O(1) 삽입, O(1) 탐색. 최악 O(N)

게임 대표 사용:
- 시너지 카운팅 -- 배치된 유닛의 종류 수
- 수집 도감 -- 획득한 아이템/캐릭터 종류 수
- 업적 달성 -- 특정 조건을 만족한 스테이지/적 종류 수
- 필터링 -- 중복 제거 후 리스트 표시

**구현**
```
function CountUnique(items[]):
    set = new HashSet()
    for item in items:
        set.Add(item)
    return set.Count

function CountUniqueWhere(items[], predicate):
    set = new HashSet()
    for item in items:
        if predicate(item):
            set.Add(item.id)
    return set.Count
```

경고 주의점:
- HashSet vs Dictionary -- HashSet은 키만, Dictionary는 키+값. ID 집합만 있으면 HashSet
- Equals/GetHashCode 오버라이드 -- 커스텀 클래스는 참조 동등성 기본. 값 비교 필요 시 오버라이드
- int/string은 안전 -- 기본 타입은 값 비교가 기본. 별도 처리 불필요
- 메모리 -- HashSet은 오버헤드 있음. 소규모(수백 개 이하) 무시 가능
- LINQ Distinct().Count() 대안 -- 같은 결과지만 HashSet이 더 명시적이고 성능 우위
- foreach 수정 주의 -- HashSet 순회 중 요소 추가/삭제 -> InvalidOperationException


#이산 #시너지 `#O(N)` #결정론
> 관련: [[game-technique-notes]] 항목 4 Unique-ID Synergy Counter | 종속성: `#언어독립`


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

## 11. Perlin / Simplex Noise

_결정론적으로 부드러운 의사 랜덤 노이즈 필드를 생성. 자연스러운 지형/텍스처/움직임 패턴에 사용. Ken Perlin이 1983년 개발._

**설명**
단순 난수(white noise)를 지형 높이에 사용하면 지나치게 울퉁불퉁하고 파편화되어 게임에 쓸 수 없다 — 모든 주파수에서 동일한 에너지를 가져 인접 지점 간 연속성이 없기 때문. 자연 지형은 저주파에 높은 진폭, 고주파에 낮은 진폭(pink noise) 특성을 가진다. Perlin Noise는 이 특성을 수학적으로 모델링.

**직관적 원리 (4단계)**
1. **격자 + 무작위 그라디언트 벡터**: 공간 위에 바둑판 격자를 그리고 각 교차점마다 임의 방향의 그라디언트 벡터를 배치
2. **거리 벡터 계산**: 샘플 지점에서 주변 4개(2D) 교차점 방향으로 벡터를 그림
3. **내적(Dot Product)**: 각 교차점의 "거리 벡터 × 그라디언트 벡터" 내적 계산 → 두 벡터가 같은 방향이면 양수, 반대면 음수
4. **페이드 보간 합산**: 내적값 4개를 fade 함수(smooth step)로 부드럽게 보간·합산 → 최종 높이값

인접 지점들이 같은 교차점의 그라디언트를 공유하기 때문에 연속적이고 부드러운 필드가 자동으로 생성된다.

Perlin Noise 작동 원리 (수학 상세):
1. 정수 그리드(Integer Lattice) 각 모서리에 의사 난수 그라디언트(gradient) 벡터 할당
2. 입력 좌표의 소수부로 그라디언트를 부드럽게 보간 (fade 함수: 6t^5 - 15t^4 + 10t^3)
3. 여러 옥타브(octave)를 누적 (FBM: Fractional Brownian Motion)해 자연스러운 디테일 생성

Simplex Noise:
- Perlin의 후속작 (2002). 같은 출력을 더 적은 계산으로 생성
- N차원에서 O(N^2) vs O(N*2^N) (Perlin 대비 효율)
- Patent 이슈로 게임 엔진은 Perlin 계열 유지

게임 대표 사용:
- 절차적 지형 생성 (높이 맵) — Minecraft, No Man's Sky 등 오픈 월드 / 생존 게임의 핵심 기반
- 텍스처 (구름, 대리석, 나뭇결)
- 캐릭터/몬스터 움직임의 유기적 변이
- VFX (불, 연기, 액체)

**구현**
```
function PerlinNoise(x, y):
    xi = floor(x) & 255
    yi = floor(y) & 255
    xf = x - floor(x)
    yf = y - floor(y)
    u = fade(xf)  // 6t^5 - 15t^4 + 10t^3
    v = fade(yf)
    // Permutation table에서 그라디언트 조회 후 보간
    ...

// FBM: 여러 옥타브 누적
function FBM(x, y, octaves, lacunarity=2.0, gain=0.5):
    value = 0
    amplitude = 1
    frequency = 1
    for i in range(octaves):
        value += amplitude * PerlinNoise(x*frequency, y*frequency)
        amplitude *= gain
        frequency *= lacunarity
    return value
```

엔진별 빌트인:
- Unity: Mathf.PerlinNoise(x, y) -- 정적 2D Perlin Noise. 1D/3D 없음
- Unreal: NoiseBlueprintNode

경고 주의점:
- PerlinNoise 출력 범위는 [0, 1]이 아님 -- 실제 범위는 [-sqrt(n/4), sqrt(n/4)]. Unity Mathf.PerlinNoise는 [0, 1] 근사
- 캐싱 필수 -- FBM 6옥타브는 매 호출 pow 5회 + noise 6회. 실시간 생성 시 캐싱 또는 GPU 고려
- 시드 변경 -- 동일 permutation table은 항상 같은 노이즈. Unity는 시드 변경 기능 없음
- 결정론적 -- 같은 입력 -> 같은 출력. 절차적 생성 맵은 시드 기반 저장으로 용량 절약
- 3D+에서 Simplex 선호 -- Perlin 3D는 8개 모서리 vs Simplex 4개. 고차원일수록 Simplex 효율 압도


#노이즈 #근사 `#O(octaves)` #결정론
> 종속성: `#언어독립`

## 12. A* 경로 탐색

_시작 노드에서 목표 노드까지의 최단 경로를 휴리스틱(heuristic) 기반으로 탐색. g(실제 비용) + h(추정 비용) = f(우선순위)로 열린 집합(open set)을 관리._

**설명**
게임에서 AI가 장애물을 피해 목적지까지 찾아가는 가장 보편적인 알고리즘. Dijkstra(모든 방향 동일 탐색)에 휴리스틱 추정(목표 방향 편향)을 더해 효율성을 극대화.

핵심 개념:
- g(n): 시작 노드에서 현재 노드까지의 실제 이동 비용
- h(n): 현재 노드에서 목표 노드까지의 추정 비용 (휴리스틱)
- f(n) = g(n) + h(n): 우선순위 큐의 정렬 기준. f가 낮은 노드부터 탐색
- 휴리스틱의 조건: admissible (h가 실제 비용을 넘지 않음) -> A*가 최적 경로 보장

휴리스틱 선택 (격자 기반 게임):
- Manhattan 거리: |dx| + |dy| -- 4방향 이동에 정확
- Chebyshev 거리: max(|dx|, |dy|) -- 8방향 이동에 정확
- Euclidean 거리: sqrt(dx^2 + dy^2) -- 자유 이동에 정확

**구현**
```
function AStar(start, goal, getNeighbors, heuristic):
    openSet = PriorityQueue()     // f(n) 기준 정렬
    cameFrom = Map()
    gScore = Map(default=inf)

    gScore[start] = 0
    openSet.Enqueue(start, heuristic(start, goal))

    while openSet is not empty:
        current = openSet.Dequeue()

        if current == goal:
            return ReconstructPath(cameFrom, current)

        for neighbor in getNeighbors(current):
            tentative_g = gScore[current] + 1
            if tentative_g < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                openSet.Enqueue(neighbor, f)

    return null  // no path
```

경고 주의점:
- 휴리스틱 과대평가(overestimate) 금지 -- admissible 조건 위반 시 A*가 최적 경로를 보장하지 않음
- 격자 타입과 휴리스틱 불일치 -- 4방향 맵에 Euclidean 사용 시 admissible은 만족하지만 확장 노드 수 증가
- 메모리 -- gScore/cameFrom 맵이 탐색 영역만큼 커짐. 대규모 월드에서 IDA* 또는 HPA* 고려
- 동적 장애물 -- A*는 정적 그래프 가정. 자주 변하면 D* Lite / LPA* 고려
- 경로 평활화 -- A* 결과는 격자 기반 직선. 실제 이동은 스무딩(Bezier, Catmull-Rom) 필요
- 탐색 깊이 제한 -- 실시간 게임에서는 탐색 깊이/노드 수 제한 필수


#이산 #기하 `#O(E log V)` #결정론
> 종속성: `#언어독립`

## 13. Quaternion 회전 (Slerp)

_짐벌락(gimbal lock)이 없는 4차원 복소수 회전 표현. Slerp(Spherical Linear Interpolation)로 두 회전 사이를 부드럽게 보간._

**설명**
오일러 각(Euler angles: pitch/yaw/roll)은 직관적이지만 짐벌락이라는 치명적 문제가 있다. 축이 정렬되면 한 축의 회전이 다른 축과 겹쳐 자유도가 사라진다. Quaternion은 이 문제를 수학적으로 해결.

Quaternion의 구조:
- q = (x, y, z, w) where x^2 + y^2 + z^2 + w^2 = 1
- w는 스칼라, (x, y, z)는 3D 축 * sin(theta/2)를 인코딩
- 물리적 의미: "회전축과 회전각을 직접 저장"

Slerp 공식:
Slerp(q1, q2, t) = (sin((1-t)*theta) * q1 + sin(t*theta) * q2) / sin(theta)

게임 대표 사용:
- 카메라 회전 보간 (3인칭 시점 전환)
- 캐릭터 본 회전 (애니메이션 블렌딩)
- 오브젝트 방향 부드러운 전환
- VR/AR 헤드 트래킹

**구현**
```
function Slerp(q1, q2, t):
    dot = q1.x*q2.x + q1.y*q2.y + q1.z*q2.z + q1.w*q2.w

    // 짧은 경로 선택 (dot < 0이면 반대 방향)
    if dot < 0:
        q2 = (-q2.x, -q2.y, -q2.z, -q2.w)
        dot = -dot

    // 작은 각도는 Lerp로 근사 (수치 안정성)
    if dot > 0.9995:
        return Normalize(Lerp(q1, q2, t))

    theta = acos(dot)
    sinTheta = sin(theta)
    t1 = sin((1-t)*theta) / sinTheta
    t2 = sin(t*theta) / sinTheta

    return Quaternion(t1*q1.x + t2*q2.x, ...)
```

엔진별 빌트인:
- Unity: Quaternion.Slerp(q1, q2, t) -- t clamp 0~1
- Unity: Quaternion.Lerp -- 더 빠르지만 정확도 낮음
- Unreal: FQuat::Slerp

경고 주의점:
- Lerp로 Quaternion 보간 금지 -- 수치상 작동하지만 각속도가 균일하지 않음
- 짧은 경로 vs 긴 경로 -- Slerp는 항상 짧은 쪽을 선택하지 않음. dot < 0 시 q2 반전 필요. Unity가 자동 처리
- 180도 회전 케이스 -- sin(pi) = 0 나누기. 대부분 엔진이 epsilon 가드
- 오일러 변환 -- Quaternion.eulerAngles는 유일하지 않음. 디버그 출력 용도로만 사용
- 성능 -- Slerp는 sin/acos으로 비쌈. Lerp + 정규화가 더 빠름. 빠른 회전 전환은 Lerp 권장


#선형대수 `#O(1)` #결정론
> 종속성: `#언어독립`

## 14. 공간 분할 (Quadtree / Spatial Hash)

_2D 공간을 재귀적으로 4분할(Quadtree) 또는 그리드 셀로 분할(Spatial Hash)해 충돌 검사/검색을 가속. O(N^2) 브루트포스를 O(N log N) 또는 O(N)으로._

**설명**
게임에는 "이 영역 안에 무엇이 있는가"라는 질문이 빈번하다: 총알이 벽에 닿았는가, 유닛이 시야 범위 내에 있는가. 공간 분할은 검사가 필요한 대상만 추려내는 인덱싱 기법.

**Quadtree** (동적 분할, 불균등 분포에 강함):
1. 공간을 4개의 자식 노드로 균등 분할
2. 각 노드의 객체 수가 임계값 초과 시 재분할
3. 검색: 쿼리 영역과 겹치는 노드의 객체만 반환

**Spatial Hash** (고정 크기, 균등 분포에 효율적):
1. 공간을 고정 크기 셀로 분할 (해시 맵: cellKey = (floor(x/cellSize), floor(y/cellSize)))
2. 각 셀이 객체 리스트를 가짐
3. 검색: 쿼리 영역이 겹치는 셀의 객체만 검사

선택 기준:
| 상황 | Quadtree | Spatial Hash |
|------|----------|-------------|
| 객체 분포 불균등 | 유리 | 불리 |
| 자주 변하는 동적 객체 | 삽입/삭제 비용 | 더 유리 (O(1) 해시) |
| 대규모 정적 지형 | 유리 | 메모리 고정 |
| N차원 확장 | 2D 전용 (Octree: 3D) | 모든 차원 동일 |

**구현 (Spatial Hash)**:
```
function Insert(obj):
    minCell = CellPos(obj.min)
    maxCell = CellPos(obj.max)
    for x in range(minCell.x, maxCell.x+1):
        for y in range(minCell.y, maxCell.y+1):
            key = Hash(x, y)
            grid[key].Add(obj)

function Query(area):
    minCell = CellPos(area.min)
    maxCell = CellPos(area.max)
    result = Set()
    for x in range(minCell.x, maxCell.x+1):
        for y in range(minCell.y, maxCell.y+1):
            key = Hash(x, y)
            for obj in grid[key]:
                if area.Overlaps(obj):
                    result.Add(obj)
    return result
```

경고 주의점:
- Spatial Hash 셀 크기 선택이 핵심 -- 너무 작으면 셀 많아짐, 너무 크면 검사량 증가. 객체 평균 크기의 2~4배 권장
- Quadtree 분할 임계값 -- 너무 낮으면 깊은 트리, 너무 높으면 리프에 객체 많음. 경험적: 8~16개
- 대형 객체 처리 -- Spatial Hash에서 대형 객체는 모든 셀에 삽입됨. static/dynamic 분리 고려
- 캐시 친화성 -- Quadtree는 포인터 추적. Spatial Hash는 배열 기반으로 더 캐시 친화적
- Unity Physics2D는 Spatial Hash 계열 내부 사용 -- 별도 구현보다 Physics2D.Overlap* API 우선 고려


#기하 #해싱 #게임필
> 종속성: `#언어독립`

## 15. 정규분포 샘플링 (Box-Muller)

_균등 분포 난수 U(0,1) 두 개를 입력받아 정규분포 N(0,1) 난수 하나를 생성. z = sqrt(-2*ln(u1)) * cos(2*pi*u2)_

**설명**
게임에서 모든 확률이 균등(uniform)인 것은 아니다. 캐릭터 스탯 변동, 데미지 산출 변동, 스폰 위치 변동 등은 현실의 자연스러운 분포를 흉내내야 한다. 정규분포는 중심 극한 정리에 의해 자연 현상의 가장 보편적인 분포.

Box-Muller 공식:
- 입력: u1, u2 ~ Uniform(0, 1), 독립
- 출력: z0, z1 ~ Normal(0, 1), 독립
- z0 = sqrt(-2 * ln(u1)) * cos(2 * pi * u2)
- z1 = sqrt(-2 * ln(u1)) * sin(2 * pi * u2) (2개 동시 생성)

출력 평균 0, 표준편차 1. 원하는 평균 mu, sigma로 변환: x = mu + sigma * z

게임 대표 사용:
- 크리티컬 데미지 변동 (mu = 기본 데미지, sigma = 10~20%)
- 적 스폰 위치 (mu = 지역 중심, sigma = 지역 반경)
- NPC 행동 타이밍 변이
- 아이템 속성 랜덤 변동

**구현**
```
function BoxMuller():
    u1 = Random01()  // (0, 1), 0과 1 배제
    u2 = Random01()
    r = sqrt(-2 * log(u1))
    theta = 2 * pi * u2
    z0 = r * cos(theta)
    z1 = r * sin(theta)  // 저장해 다음 호출에 재사용
    return z0

function NormalRandom(mu, sigma):
    return mu + sigma * BoxMuller()
```

경고 주의점:
- u=0에서 log(0) = -inf -- Random01()이 0을 반환할 수 있으면 1e-10 ~ 1-1e-10으로 clamp 필수
- 균등 분포인지 확인 -- Box-Muller는 입력이 균등하다고 가정. 입력 난수 생성기가 편향되면 출력도 편향
- 저장 최적화 -- Box-Muller는 z0와 z1을 동시 생성. z1을 저장해두면 다음 호출은 저장값 반환으로 2회분 처리
- Central Limit Theorem 대안 -- 12개의 Uniform(0,1)을 더한 후 6을 빼면 근사 정규분포 N(0,1). Box-Muller보다 빠름
- 꼬리 값 핸들링 -- 게임에서 z > 3 (mu+3sigma)는 클램프 고려. 0.3% 미만 확률


#확률 `#O(1)` #확률적
> 종속성: `#언어독립`

## 16. Reservoir Sampling

_크기를 알 수 없는 스트림(또는 배열)에서 N개의 샘플을 균등 확률로 선택. O(N) 시간, O(k) 메모리. 한 번의 순차 패스로 완료._

**설명**
게임에서 "모든 항목을 배열에 저장하지 않고 랜덤하게 고르고 싶다"는 상황이 있다: 무한 맵에서 N개의 몬스터 스폰 위치 선택, 대규모 리플레이 데이터에서 N개의 키 프레임 샘플링.

알고리즘 (k=1인 경우):
1. 첫 번째 항목을 결과로 선택
2. i번째 항목에서 확률 1/i로 결과 교체
3. 종료 시 각 항목이 선택될 확률 = 1/N (동일)

k개 일반화:
1. 처음 k개 항목을 결과 배열에 저장
2. i번째 항목(k+1 <= i <= N)에서 확률 k/i로 결과 배열의 임의 위치와 교체
3. 종료 시 각 항목이 선택될 확률 = k/N

**구현**
```
// k=1: 하나의 샘플
function ReservoirSample(stream):
    result = null
    count = 0
    for item in stream:
        count += 1
        if Random01() < 1.0 / count:
            result = item
    return result

// k개: k개의 샘플
function ReservoirSampleK(stream, k):
    result = new array[k]
    count = 0
    for item in stream:
        if count < k:
            result[count] = item
        else:
            r = RandomInt(0, count)
            if r < k:
                result[r] = item
        count += 1
    return result
```

경고 주의점:
- 스트림의 크기 N을 미리 알 필요 없음 -- Reservoir의 핵심 장점
- 무작위 접근 가능하면 Fisher-Yates 셔플이 더 효율적
- 부동소수점 오차 -- i가 10^7 이상이면 RandomInt(0, count) == 0 정수 비교 권장
- 정렬된 데이터 주의 -- Reservoir는 순서를 보존하지 않음
- 대안 Weighted Reservoir -- 각 항목마다 가중치가 다르면 A-ES 알고리즘 사용


#확률 `#O(N)` #확률적
> 종속성: `#언어독립`

---

## 17. 오일러 적분 (Euler Integration)

_현재 상태(위치·속도)에 `가속도 × dt`를 반복 누적해 다음 상태를 근사하는 수치 해석 기법. 미적분 없이 단순 덧셈만으로 게임 물리 루프를 구현하는 핵심 빌딩블록._

**설명**
실제 포물선 운동은 `y = v₀t - ½gt²`로 정확히 표현된다. 그러나 게임은 두 가지 이유로 이 해석적 해(analytical solution)를 쓰지 않는다:
1. 비대칭 중력·가변 점프처럼 상태별로 가속도가 바뀌면 해석적 해 자체가 없음
2. 규칙을 바꿀 때마다 공식을 재도출해야 함

오일러 적분은 대신 "아주 짧은 시간 동안 가속도가 일정하다"는 가정 하에 덧셈만으로 근사한다:

```
속도 += 가속도 × dt
위치 += 속도   × dt
```

1프레임(~0.016s @ 60fps)을 dt로 쓰면 오차가 실용적으로 무시 가능하다. 복잡한 적분 없이 if 분기만으로 어떤 가속도 규칙도 적용할 수 있다.

**게임 점프 적용 — 비대칭 중력**
현실: 상승/하강 동일한 중력 g → 포물선이 좌우 대칭, 조작감 "둥둥 뜨는" 느낌.
게임: 상승 시 g_up(작음), 하강 시 g_down(큼) → 오일러 루프에서 조건 분기 하나로 구현.

```
// 매 프레임
if velocity.y > 0:          // 상승 중
    velocity.y -= g_up  * dt
else:                       // 하강 중
    velocity.y -= g_down * dt

position.y += velocity.y * dt
```

참고 수치 (영상 예시):
| 파라미터 | 값 | 의미 |
|---|---|---|
| g_up | 7 | 상승 중력 — 느긋하게 올라감 |
| g_down | 36 | 하강 중력 — 빠르게 떨어짐 (약 5배) |

g_down을 크게 할수록 템포 빠름 + 가변 점프 구현이 쉬워짐 (버튼 뗄 때 g를 g_down으로 교체).

**구현 — 일반화된 게임 물리 루프**
```
function Update(dt):
    accel = GetAcceleration(state)   // 상태별 가속도 결정
    velocity += accel * dt
    position += velocity * dt

function GetAcceleration(state):
    if state.isJumping and velocity.y > 0:
        return -g_up
    else:
        return -g_down
    // 이 함수에 비대칭 중력, Apex Modifier, 가변 점프, 낙하 최대 속도 등 모든 규칙 추가
```

⚠ **주의점**
- **프레임률 독립 필수** — `velocity += accel * dt`에서 dt는 반드시 `Time.deltaTime`(가변). 고정값(1/60) 하드코딩 시 프레임률 변화에 따라 물리가 달라짐
- **오차 누적** — dt가 클수록(저프레임) 오차 증가 → 물체가 벽을 통과하거나 튀는 현상. 60fps 기준 허용 오차이지만 가변 dt 사용 + 이동 후 충돌 보정을 세트로 적용
- **해석적 해 vs 오일러** — 일정 중력의 단순 포물선은 해석적 해가 더 정확. 게임 점프처럼 상태별 가속도가 다르면 해석적 해가 없어 오일러가 표준
- **Verlet 적분 대안** — 에너지 보존이 중요한 물리 퍼즐/로프 시뮬레이션에는 Verlet 적분이 더 안정적. 캐릭터 이동에서는 오일러로 충분


#수치해석 #근사 `#O(1)` #결정론
> 관련: [[game-technique-notes]] 항목 1 비대칭 점프 (Euler 적분의 직접 응용 — g_up/g_down 비대칭 구현) | 종속성: `#언어독립`

---

## 분류 메모

- **수학 vs 기법 경계**: Lerp는 *수학*이고, "D20 굴림을 데미지에 Lerp" 는 *기법*([game-technique-notes.md](game-technique-notes.md) 항목 5). 같은 Lerp가 카메라 추적에도 쓰이므로 한 단계 아래에 둔다.
- **수학 vs Unity API 경계**: Mathf.Lerp는 Unity API([unity-feature-notes.md](unity-feature-notes.md) 항목 27)이지만, "선형 보간"이라는 개념은 엔진 독립적. 본 노트는 *개념*에 집중.
- **승격 후보**: 일반 지식 섹션(항목 9~항목 16)이 본 프로젝트에 도입되면 "사용 중" 표로 이동.

### 다관점 분리 그룹 (의도된 cross-ref)
같은 코드 사례를 *수학 개념 / 게임 기법 / Unity API* 세 축에서 본다. 어느 한 곳이 SOT가 아니라 축별 진입점이 다르다.

| 공통 주제 | math (개념) | game-technique (응용) | unity-feature (API) |
|---|---|---|---|
| 선형 보간 | 항목 1 Lerp | 항목 5 D20 데미지 | 항목 27 Mathf |
| dB 변환 | 항목 2 Linear↔dB | 항목 6 AudioMixer 지각 변환 | 항목 14 AudioMixer / 항목 27 Mathf.Log10 |
| 멱함수 | 항목 4 Power-Law | 항목 3 강화 보상 곡선 | --- |
| 가중 랜덤 + Pity | 항목 5, 항목 6 | 항목 2 가챠 등급 보정 | --- |
| 벡터 산술 | 항목 7 Vector2 | --- | 항목 27 Mathf (Vector2/3) |
| 집합 카운팅 | 항목 8 HashSet | 항목 4 Unique-ID Synergy | --- |

### 통합/제거된 항목
- **단조증가 SortingOrder** -> [game-misc-notes.md](game-misc-notes.md) 항목 3 SortingOrder 레이어 상수가 SOT (수학적 색채 약함)
- **비대칭 적분 (Variable Gravity)** -> [game-technique-notes.md](game-technique-notes.md) 항목 1 Asymmetric Jump가 SOT (응용 기법 자체)

---
