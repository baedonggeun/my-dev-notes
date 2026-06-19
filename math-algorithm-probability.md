# 수학/알고리즘 — 확률·통계·집합

> 상위 노트: [[math-algorithm-notes]] (전체 인덱스 디스패처)
> 다루는 축: 확률·통계·분포·집합론
> 다루지 않는 축: [[math-algorithm-interpolation|수학/알고리즘 — 보간·변환·곡선]] / [[math-algorithm-spatial-algo|수학/알고리즘 — 공간·알고리즘]]

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
| 5 | 가중 랜덤 (Weighted Random Sampling) | `#확률` `#가챠` | 항목별 가중치에 비례한 확률로 선택 | `#언어독립` |
| 6 | Pity 누적 시프트 (Cumulative Probability Shift) | `#확률` `#가챠` | 실패 누적 시 확률 점진 증가, 임계점 도달 시 보장 | `#언어독립` |
| 8 | HashSet 유니크 카운트 (집합 연산) | `#이산` `#시너지` | O(1) 평균 시간으로 중복 제거 + 카운트 | `#언어독립` |
| 15 | 정규분포 샘플링 (Box-Muller) | `#확률` | 균등 난수 2개로 정규분포 난수 생성 | `#언어독립` |
| 16 | Reservoir Sampling | `#확률` `#O(N)` | 크기 미상 스트림에서 균등 확률로 N개 샘플 | `#언어독립` |

---

# 풀노트

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

---

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

---

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

---

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

---

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