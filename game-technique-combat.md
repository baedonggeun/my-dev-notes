# 게임 기법 노트 — 전투·수치·확률

> 상위 노트: [[game-technique-notes]] (전체 인덱스 디스패처)
> 다루는 축: 데미지 산출·강화 곡선·시너지 시스템·가챠 확률
> 다루지 않는 축: [[game-technique-mechanics|게임필·시각 기법]] / [[game-technique-systems|시스템·아키텍처]]

---


## 태그 목록

### 카테고리 (무엇)
- `#이동` `#점프` `#카메라` `#입력` `#충돌`
- `#전투` `#데미지` `#난수` `#가챠` `#밸런싱`
- `#오디오` `#UI` `#피드백` `#애니메이션` `#VFX`
- `#슬롯` `#시너지` `#곡선` `#튜토리얼` `#시퀀스`

### 장르 (어디)
- `항목 2D` `항목 3D` `#플랫포머` `#액션` `#전략` `#로그라이크` `#캐주얼`

### 효과/의도 (왜)
- `#게임필` `#응답성` `#관용성` `#예측가능성` `#몰입` `#결정론`

### 구현 매체 (어떻게)
- `#물리엔진` `#커스텀적분` `#보간` `#콜백` `#게이팅`

---


# 인덱스

| # | 기능 | 기법 이름 | 한 줄 요약 | 종속성 |
|---|------|----------|----------|--------|
| 2 | 가챠 등급 보정 | Pity 등급 시프트 + Fallback | 누적 실패 시 확률 점진 증가, 천장 도달 시 등급 보장 | `#언어독립` |
| 3 | 강화 보상 스케일링 | Power-Law Enhancement Curve | 멱함수로 후반 보상이 가파르게(또는 완만하게) 변하는 곡선 | `#언어독립` |
| 4 | 시너지 카운팅 | Unique-ID Synergy Counter | HashSet으로 동일 ID 중복 제거하며 종류 수 카운트 | `#언어독립` |
| 5 | 데미지 산출 | D20 Lerp 보간 데미지 | 굴림값(1~20)을 min/max 데미지 범위에 Lerp로 매핑 | `#언어독립` |
| 13 | 데미지 판정 | 주사위 합산값(summaryValue) 판정 | 슬롯 배치 주사위를 합산한 summaryValue를 diceMin/diceMax/criticalValue와 비교 — D20과 달리 플레이어 주사위 선택이 결과에 직결 | `#언어독립` |
| 14 | 속성·시너지 효과 분리 | AttrEffect / SynergyAttrEffect 이중 호출 | 속성 기본 효과(AttrEffect)와 시너지 보너스 효과(SynergyAttrEffect)를 독립 클래스로 분리 → DiceController가 순차 호출. 기각 대안: baseOnly 플래그 — 책임 혼재 | `#언어독립` |
| 15 | 시너지 데이터 소스 관리 | SynergyDataSO 단일 소스 원칙 | 시너지 보너스 수치는 SynergyDataSO에만 보관 — weapon SO에 분산 시 툴팁 미반영. 기각 대안: reinforced 필드 패러다임 유지 | `#언어독립` |
| 16 | 시드 기반 의사난수 | 의사난수 시드 결정론 (RNG Manipulation) | 컴퓨터는 시드 초기값으로 결정론적 난수 배열을 생성 — 시드 조건을 플레이어가 제어하면 모든 결과가 예측/확정 가능. 포켓몬·마리오의 고전 사례와 현대 방어 설계 | `#언어독립` |

---

# 풀노트

## 2. 가챠 Pity 시스템 (Pity 등급 시프트 + Fallback)

_누적 실패 횟수에 따라 고등급 확률을 점진 상승시키고(소프트 pity), 천장 도달 시 강제 지급(하드 pity). Rate-up 실패 시 fallback counter 별도 누적._

**설명**
가챠의 핵심 불만은 *분산* — 운 나쁜 사용자는 기댓값의 10배를 써야 할 수 있다. Pity는 이 분산의 상한을 제어해 "최악의 경우"를 보장.

2단 Pity 구조:
- **소프트 pity** — N회 이후 확률 점진 상승. "곧 나올 것 같다"는 심리적 기대감 형성
- **하드 pity (천장)** — M회에서 반드시 지급. 최악 케이스 절대 보장

Rate-up 시스템 (추가 레이어):
- 픽업 캐릭터/아이템 확률 boost. 고등급이 나왔을 때 픽업 50%, 비픽업 50%
- 비픽업으로 실패 시 다음 고등급에서 픽업 보장 (fallback guarantee counter)

전체 구조:
```
pity_counter = 0        // 고등급 pity
guarantee_counter = 0   // 픽업 보장 — 비픽업 실패 시 1

function Roll():
    grade = RollGrade(pity_counter)   // math-algorithm 항목 6 소프트+하드 pity 적용
    pity_counter = (grade == HIGH ? 0 : pity_counter + 1)
    
    if grade == HIGH:
        if guarantee_counter >= 1 or Random() < 0.5:
            guarantee_counter = 0
            return RATE_UP_ITEM
        else:
            guarantee_counter = 1
            return NON_RATE_UP_ITEM
    return NORMAL_ITEM
```

**구현**
```csharp
// CasualStrategy 패턴 (GachaService)
public class GachaService
{
    private int _pityCount;
    private int _guaranteeCount;
    private GachaPoolConfigSO _config;

    public GachaResult Roll()
    {
        float p = CalcProbability(_pityCount);
        bool isHigh = Random.value < p;
        _pityCount = isHigh ? 0 : _pityCount + 1;

        if (isHigh)
        {
            bool isRateUp = _guaranteeCount >= 1 || Random.value < 0.5f;
            _guaranteeCount = isRateUp ? 0 : _guaranteeCount + 1;
            return new GachaResult(isRateUp ? Grade.RateUp : Grade.OffRateUp);
        }
        return new GachaResult(Grade.Normal);
    }

    private float CalcProbability(int n)
    {
        if (n >= _config.hardCeiling) return 1f;
        if (n >= _config.softThreshold)
            return Mathf.Min(1f, _config.baseRate + (n - _config.softThreshold) * _config.rateIncrement);
        return _config.baseRate;
    }
}
```

권장 파라미터 참조:
| 게임 | base | soft 시작 | ceiling |
|---|---|---|---|
| 원신 5성 | 0.6% | 74 | 90 |
| 일반 SSR | 1~3% | 60~80% ceiling | 100~200 |

⚠ **주의점**
- **pity_counter 리셋 타이밍** — 고등급 지급 *직후* 리셋. 결과 처리 전 리셋 로직에 오류 시 다음 시도도 pity 오염
- **guarantee_counter와 pity_counter 독립** — 같은 변수 공유 시 픽업 fallback이 pity 카운터를 초기화하는 설계 혼선 발생
- **영속 저장 필수** — 두 카운터 모두 앱 재시작 후에도 유지. PlayerPrefs 또는 서버. 클라이언트만 보관 시 치트 위험
- **Monte Carlo 검증** — 파라미터 조정 전 10만 회 시뮬레이션으로 평균 소요 횟수, 90th percentile, 천장 도달 빈도 측정 필수
- **소프트 pity 투명성** — 공개하면 사용자가 "74회부터 올라간다"는 기대를 품어 이탈 방지. 일부 게임은 비공개로 운영 (커뮤니티가 역산으로 발견)


#가챠 #확률 #밸런싱 #게임필
> 관련: [[math-algorithm-notes]] 항목 5 가중 랜덤, 항목 6 Pity 누적 시프트 (수학 기반) | 종속성: `#언어독립`

## 3. Power-Law 강화 곡선 (Power-Law Enhancement Curve)

_강화 단계 `x ∈ [0, max]`를 멱함수 `f(x) = (x/max)^n`으로 정규화. 지수 `n`으로 후반 보상 곡선 형태 제어. `n > 1`: 후반 가파름, `n < 1`: 초반 가파름._

**설명**
선형 스케일링(n=1)은 각 강화 단계가 동일한 보상을 준다 — 드라마틱하지 않고 단조롭다. 멱함수는 `n` 하나로 곡선 형태를 조절.

`n`별 형태:
| n | 형태 | 게임 의도 |
|---|---|---|
| < 1 (e.g. 0.5) | 오목 (Concave) | 초반 빠른 성장 → 후반 수렴 (신규 유저 동기 ↑) |
| = 1 | 직선 (Linear) | 균등 보상 |
| 2~3 | 볼록 (Convex) | 초반 느린 성장 → 후반 폭발 (하드코어/과금 포인트) |
| 5+ | 초반 거의 0 → 끝에서 급등 | 고인물 게임, 거의 사용 안 함 |

패턴 변형:
- **비용 곡선**: 강화 비용이 n>1인 멱함수 → 후반 강화에 기하급수 비용 (과금 포인트)
- **성능 곡선**: 강화 스탯이 n<1 → 초반 빠른 성장 → 후반 수렴 (파워 크리프 완화)
- **비용 체증 + 수익 체감** 조합이 경제 설계 황금률

**구현**
```
// 정규화 멱함수 곡선
function PowerCurve(step, maxStep, n):
    t = step / maxStep    // [0, 1]
    return t ^ n          // [0, 1]

// 스탯 계산: base + (max - base) * curve
function EnhancedStat(base, max, step, maxStep, n):
    return Lerp(base, max, PowerCurve(step, maxStep, n))
```

```csharp
// Unity C#
float t = (float)step / maxStep;
float stat = Mathf.Lerp(baseStat, maxStat, Mathf.Pow(t, n));

// AnimationCurve 대안 — Inspector에서 디자이너가 직접 곡선 편집
[SerializeField] private AnimationCurve enhanceCurve;
float stat = Mathf.Lerp(baseStat, maxStat, enhanceCurve.Evaluate(t));
```

AnimationCurve는 `n` 수식 없이 조정 가능하나 코드에서 공식 추적이 어려움. 멱함수 수식 + `n`만 인스펙터 노출이 타협점.

⚠ **주의점**
- **step == 0에서 pow(0, n) = 0** — `Lerp(base, max, 0) = base`가 정확. 특수 처리 불필요
- **n 값 선택** — n=2(Quad)가 가장 자연스러운 가파름 시작점. n=1.5는 선형과 Quad의 중간. 시뮬레이션으로 검증 권장
- **maxStep == 0 나누기** — `step / maxStep`에서 maxStep=0이면 Divide by Zero. 가드 필수
- **비용 곡선과 성능 곡선 분리 설계** — 비용 n>1 + 성능 n<1 조합 시 "비용은 올라가는데 성능 체감은 줄어드는" 수익체감 구조 성립


#밸런싱 #곡선 #게임필
> 관련: [[math-algorithm-notes]] 항목 4 멱함수 곡선 (수학 빌딩블록), [[unity-feature-notes]] 항목 35 AnimationCurve (Unity 대안) | 종속성: `#언어독립`

## 4. Unique-ID Synergy Counter

_HashSet으로 동일 ID 중복을 제거하며 "종류 수"를 카운트. 배치된 유닛의 계열/직업/속성 등 다양한 시너지 조건에 재사용._

**설명**
시너지 시스템은 "같은 종류의 유닛을 몇 종류 배치했는가"로 발동 조건을 판단한다. 단순히 유닛 수를 세면 안 된다 — 동일 유닛을 3개 배치해도 1종류로만 카운트. HashSet은 이 중복 제거를 O(1) 평균 시간으로 해결.

일반화된 시너지 카운팅 구조 (CasualStrategy 적용):
```
// 인벤토리의 모든 유닛을 순회하며 각 시너지 조건 그룹의 유니크 ID를 카운트
for each unit in inventory:
    unit.teamId -> teamSet.Add(unit.charId)      // 팀 시너지
    unit.tier -> tierSets[unit.tier].Add(id)      // 등급별 시너지
    unit.faction -> factionSets[unit.type].Add(id) // 진영 시너지
```

발동 조건식:
- 1종류 = 기본 효과
- 3종류 = 강화 효과
- 5종류 = 궁극 효과

**구현**
```csharp
// CasualStrategy 패턴 (대략)
public class SynergyCounter
{
    private Dictionary<SynergyType, HashSet<int>> _synergySets;

    public int CountUnique(SynergyType type)
    {
        return _synergySets.TryGetValue(type, out var set) ? set.Count : 0;
    }

    // 유닛 배치/회수 시 호출
    public void AddUnit(Unit unit)
    {
        foreach (var synergy in unit.synergies)
        {
            if (!_synergySets.ContainsKey(synergy.type))
                _synergySets[synergy.type] = new HashSet<int>();
            _synergySets[synergy.type].Add(synergy.id);
        }
    }

    public void RemoveUnit(Unit unit)
    {
        foreach (var synergy in unit.synergies)
        {
            if (_synergySets.TryGetValue(synergy.type, out var set))
                set.Remove(synergy.id);
        }
    }
}
```

경고 주의점:
- HashSet 순회 중 Add/Remove 금지 — 배치/회수 시 시너지 재계산이 필요한 경우, 먼저 수정 후 계산. 수정 중 조회는 버그 발생
- 다중 시너지 중복 방지 — 하나의 유닛이 여러 시너지 조건(진영 + 직업)에 동시 기여 가능. 각 SynergyType별 독립 HashSet 관리
- 시너지 카운터 변경 시 UI 갱신 — Count 변경 시 이전/이후 값을 비교해 차이만 전파. 매 프레임 전체 재계산 지양
- RemoveUnit 누락 — 유닛 회수/판매 시 반드시 RemoveUnit 호출. 누락되면 시너지가 영구 유지되어 밸런스 붕괴
- HashSet 대신 Dictionary — Count만 필요하면 HashSet, 추가 데이터(레벨 합계 등)가 필요하면 Dictionary<id, data> 사용


#시너지 #카운팅 #게임필
> 관련: [[math-algorithm-notes]] 항목 8 HashSet 유니크 카운트 (수학 빌딩블록), [[math-algorithm-notes]] 항목 1 Lerp | 종속성: `#언어독립`

## 5. D20 Lerp 보간 데미지

_굴림값(1~20)을 min/max 데미지 범위에 Lerp(선형 보간)로 매핑. diceRoll 1 = minDmg, 20 = maxDmg. 중간값은 비례 배분._

**설명**
주사위 게임의 전통 공식 `1d20 + modifier`는 고정된 범위에서 균등 분포의 결과를 제공한다. 여기에 *min/max 데미지* 개념을 더하면: diceRoll 1을 쳤는데 maxDmg가 나오면 안 된다. diceRoll이 높을수록 높은 데미지가 나와야 자연스럽다.

D20 Lerp 변환:
```
diceRoll (1~20) -> t (0~1) -> Lerp(minDmg, maxDmg, t)
```

파생 변형:
- **치명타 (Critical)**: diceRoll == 20 -> 강제 maxDmg 또는 maxDmg * 1.5
- **빗나감 (Miss)**: diceRoll == 1 -> minDmg 또는 0 + 추가 효과 없음
- **클램프 구간**: 1~20을 벗어난 버프/디버프는 Clamp01(t)로 안전 처리

**구현**
```csharp
// 기본 데미지 계산
public int CalcDamage(int diceRoll, int minDmg, int maxDmg)
{
    float t = (diceRoll - 1) / 19f;     // [1..20] -> [0..1]
    return (int)Mathf.Lerp(minDmg, maxDmg, t);
}

// 치명타/빗나감 포함
public DamageResult CalcDamageFull(int diceRoll, DamageSpec spec)
{
    if (diceRoll == 1)
        return new DamageResult(spec.minDmg, isMiss: true);  // 최소 데미지
    if (diceRoll == 20)
        return new DamageResult((int)(spec.maxDmg * 1.5f), isCrit: true);

    float t = (diceRoll - 1) / 19f;
    int dmg = (int)Mathf.Lerp(spec.minDmg, spec.maxDmg, t);
    return new DamageResult(dmg);
}
```

경고 주의점:
- diceRoll 1~20이 아닌 범위 — 외부 버프로 diceRoll < 1이나 > 20이 들어올 수 있음. Clamp01 가드 필수
- 정수 vs 실수 데미지 — `(int)Lerp`는 소수점 버림. minDmg가 1, maxDmg가 20이면 diceRoll 2에서도 데미지 1이 될 수 있음. Round/Ceil 고려
- MISS 시너지 규칙 — 빗나간 공격(diceRoll 1)은 시너지 카운터를 누적하지 않음 (게임 규약, 절대 변경 금지)
- 치명타율 이중 적용 주의 — diceRoll==20 자체가 5%. 별도 critRate 스탯이 있으면 이중 적용되지 않도록 설계. (방법 A: diceRoll 20은 자동 치명타, 방법 B: critRate는 diceRoll과 독립)
- 로그/피드백 — diceRoll 값을 UI에 표시하면 플레이어가 운의 영향을 직관적으로 이해. "1이 떴다 = 오늘 운 없음"


#전투 #데미지 #게임필
> 관련: [[math-algorithm-notes]] 항목 1 Lerp (수학 기반), [[math-algorithm-notes]] 항목 3 Clamp/Clamp01 (안전망) | 종속성: `#언어독립`

## 13. 주사위 합산값(summaryValue) 판정

_슬롯에 배치된 주사위(D4/D6/D8 등)를 굴려 합산한 summaryValue를 diceMin/diceMax/criticalValue와 비교해 MISS/일반/치명타를 판정. 플레이어의 주사위 조합이 기대값과 분산을 결정하므로 선택에 전략적 의미가 생김._

**설명**
D20 단일 롤과의 핵심 차이:
| | D20 Lerp | summaryValue |
|---|---|---|
| 주사위 구성 | 고정 (1d20) | 플레이어가 슬롯에 배치 |
| 결과 제어 | 불가 (순수 운) | 기대값/분산 조절 가능 |
| 전략성 | 없음 | 주사위 선택 = 리스크 관리 |

판정 흐름:
```
슬롯별 주사위 롤 → 합산 (summaryValue)
    summaryValue < diceMin              → MISS
diceMin ≤ summaryValue < criticalValue  → 일반 데미지 (Lerp)
    summaryValue ≥ criticalValue        → 치명타
```

주사위별 기대값:
| 주사위 | 기대값 | 최대값 |
|---|---|---|
| D4 | 2.5 | 4 |
| D6 | 3.5 | 6 |
| D8 | 4.5 | 8 |

슬롯이 2개이고 D8 × 2를 배치하면 summaryValue 기대값 9, 최대 16.

**구현 (의사코드)**
```
summaryValue = 0
for each slot:
    if slot.dice != null:
        summaryValue += Random.Range(1, slot.dice.maxFace + 1)

if summaryValue < spec.finalDiceMin:
    result = MISS
elif summaryValue >= spec.finalCriticalValue:
    result = CRITICAL
else:
    t = Clamp01((summaryValue - finalDiceMin) / (finalDiceMax - finalDiceMin))
    damage = Lerp(minDamage, maxDamage, t)
    result = NORMAL(damage)
```

⚠ **주의점**
- **빈 슬롯** — 주사위 없는 슬롯은 summaryValue 기여 0. 모든 슬롯이 비면 summaryValue=0 → 항상 MISS. 무기 장착 시 빈 슬롯 체크 권장
- **파라미터 정합** — `criticalValue > diceMax_이론최대합`이면 치명타 불가. `diceMin = diceMax`이면 일반 구간 없음. 파라미터 설계 시 주사위 조합별 최대합 계산 필요
- **MISS 시너지 규칙** — MISS 결과는 시너지 카운터를 증가시키지 않음 (게임 규약). summaryValue 판정 로직 재설계 시에도 반드시 보존
- **적 판정** — 적도 DiceSO를 보유하고 동일 summaryValue 흐름으로 판정. 적의 주사위 구성이 난이도 조절 변수


#전투 #데미지 #밸런싱 #게임필
> 관련: [[game-technique-notes]] 항목 5 D20 Lerp 보간 데미지 (이전 방식 — D20은 이 프로젝트에서 summaryValue로 대체됨), [[math-algorithm-notes]] 항목 1 Lerp, 항목 3 Clamp | 종속성: `#언어독립`

## 14. 속성·시너지 효과 분리 (AttrEffect / SynergyAttrEffect 이중 호출)

_속성 기본 효과와 시너지 보너스 효과를 독립 클래스로 분리하고 순서를 보장해 호출하는 구조. 각 클래스는 자신의 컨텍스트만 알고 상대를 참조하지 않는다._

**문제**
시너지 효과가 속성 효과(AttrEffect)와 같은 Apply 메서드에 섞이면:
- `baseOnly` 플래그를 추가하거나 조건 분기가 생김
- AttrEffect가 시너지 상태를 참조해야 해서 결합도가 높아짐
- 시너지 효과 N종이 각각 AttrEffect의 if 블록으로 들어가면 수정 범위가 커짐

**해결: 두 클래스로 분리, 순차 호출**
```
// 호출 측 (DiceController)
attrEffect.Apply(baseContext);           // 1단계: 기본 속성 효과
synergyAttrEffect.Apply(synergyContext); // 2단계: 시너지 보너스 효과
```

- `AttrEffect` — 속성 종류별 기본 효과 (Fire 연소, Water 치유, Wind 방어 등)
- `SynergyAttrEffect` — 시너지 임계값 달성 시 추가 보너스 (Fire 임계 4 → 공격력 +N% 등)
- 두 클래스는 각각 독립 컨텍스트(`AttrEffectContext`, `SynergyEffectContext`)를 받음

**기각 대안**
- `AttrEffect.Apply(ctx, bool baseOnly)` 플래그 방식 → AttrEffect가 시너지 조건을 알아야 해서 결합도 상승. 기각.

⚠ **주의점**
- **호출 순서 고정** — 기본 효과가 먼저, 시너지 보너스가 나중. 순서가 바뀌면 보너스 계산 기준이 달라질 수 있음
- **컨텍스트 타입 분리** — AttrEffectContext와 SynergyEffectContext는 별도 타입. 합치면 두 클래스가 공유 상태를 읽어 결합이 재발생

#시너지 #전투 #OOP
> 관련: [[game-technique-notes]] 항목 4 시너지 카운팅, 항목 15 시너지 데이터 중앙화 | 종속성: `#언어독립`

## 15. 시너지 데이터 SO 중앙화 (reinforced 패러다임 제거)

_시너지 효과에 관련된 수치를 SynergyDataSO 한 곳에만 보관하는 원칙. weapon SO에 분산된 reinforced 필드 패러다임을 제거._

**문제: reinforced 필드 패러다임**
- 무기 SO에 `reinforcedHealAmount`, `reinforcedGoldAmount` 등 시너지 보너스 수치가 분산
- 시너지 툴팁이 `SynergyDataSO`를 기준으로 렌더링 → weapon SO 값이 툴팁에 미반영
- 시너지 관련 수치를 수정하려면 weapon SO 전수를 탐색해야 함

**해결: SynergyDataSO effectType enum으로 이전**
```
// 기존 (weapon SO마다 개별 관리)
weapon.reinforcedHealAmount = 21;

// 변경 (SynergyDataSO 1개에서 관리)
synergy.effectType = WaterHealBonus;
synergy.effectValue = 21;
```
툴팁은 `SynergyDataSO`만 참조하므로 자동으로 정합.

**적용 기준**
툴팁, 설명 텍스트, 런타임 능력치 중 *어느 하나라도* 시너지 SO에서 읽는다면 → 해당 수치는 시너지 SO에 있어야 함.

**기각 대안**
- reinforced 패러다임 유지 → weapon SO 값이 시너지 툴팁에 미반영. 기각.

⚠ **주의점**
- **effectType 수 증가** — 시너지 종류가 늘어나면 enum 값이 많아짐. 항목 10+ 시 카테고리 분리 검토
- **weapon SO 마이그레이션** — 기존 reinforced 필드를 가진 SO는 일괄 업데이트 필요. 필드 제거 시 없는 참조 런타임 에러 주의

#시너지 #데이터 #아키텍처
> 관련: [[game-technique-notes]] 항목 14 속성·시너지 효과 분리, 항목 4 시너지 카운팅 | 종속성: `#언어독립`

## 16. 의사난수 시드 결정론 (RNG Manipulation)

_컴퓨터는 진정한 무작위를 생성하지 못하며, 시드(Seed) 초기값으로부터 결정론적 난수 배열을 생성한다. 플레이어가 시드 생성 조건을 제어하면 모든 난수 결과를 예측하거나 원하는 결과를 확정 입수할 수 있다._

**개념**
고전 컴퓨터는 스스로 진정한 무작위 수를 만들어내지 못한다. 대신 시드(초기값)를 입력받아 그로부터 무작위처럼 보이는 숫자 배열(의사난수 수열)을 결정론적으로 생성한다. 시드가 같으면 배열이 항상 동일하다. 플레이어가 시드를 결정하는 조건을 파악·제어할 수 있으면 모든 이후 결과를 예측하거나 원하는 조건을 재현할 수 있다.

**플랫폼별 사례**

**포켓몬스터 에메랄드 (3세대) — 경과 시간 단일 시드**
- 시드 = 게임 기동 후 경과 시간. 경과 시간이 같으면 동일한 난수 배열
- 색이 다른 레쿠쟈가 나온 타이밍(예: 기동 3.3초 후)을 재현하면 매번 동일한 결과
- 플레이어 대응: 스톱워치로 경과 시간을 초 단위로 맞춰 희귀 포켓몬 확정 포획

**포켓몬스터 디아루가·펄기아 (4세대) — 이중 변수 시드**
- 시드 = 게임기 설정 시각 × 세이브 파일 로드까지 걸린 시간 (두 변수 곱)
- 플레이어 대응: 난수 검색 도구로 원하는 개체값이 나오는 시드 역산 → 게임기 시각 수동 조정 + 로드 타이밍 정밀 제어로 원하는 포켓몬 확정 입수

**뉴 슈퍼 마리오브라더스 — 다중 변수 시드 (스피드런 활용)**
- 시드 = 게임기 고유 번호 × 기동 타이밍 × 더블 점프 수행 횟수 (조합)
- 스피드런 플레이어: 더블 점프 횟수를 의도적으로 조정해 원하는 아이템 드롭을 확정시키는 기술로 활용

**방어 설계 — 현대 게임의 개선 방향**
이후 포켓몬 시리즈를 비롯한 현대 게임들의 대응:
- 시드 생성에 플레이어가 관측·조작 불가능한 변수(하드웨어 타이머, 복수 엔트로피 소스)를 결합
- 또는 시드 조건 자체를 외부에서 추적할 수 없도록 내부 카운터·OS 타임스탬프 복수 조합

**설계 판단 기준**
- 공정성이 중요한 PvP·경쟁 요소: 플레이어가 제어 가능한 단일 변수(경과 시간 등)를 시드로 쓰지 않는다.
- 튜토리얼·결정론 보장이 목적인 경우: 역으로 시드를 노출·고정해 재현 가능성을 의도적으로 제공 ([[game-technique-notes]] 항목 8).
- 스피드런 커뮤니티에서는 RNG 조작이 합법적 기술로 인정되기도 함 — 설계 구멍인지 의도된 깊이인지는 커뮤니티와 개발사 정책이 결정.


#난수 #결정론 #예측가능성
> 관련: [[game-technique-notes]] 항목 8 튜토리얼 결정론 (고정 큐로 RNG 대체 — 결정론을 의도적으로 활용하는 정반대 사례) | 종속성: `#언어독립`
