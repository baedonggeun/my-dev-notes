# 게임 기법 노트

> 다루는 축: 게임 *기능*별 구현 기법. "어떻게 묵직한 점프를 만드는가?" 같은 질문에 답
> 다루지 않는 축: 왜 그렇게 느껴지는가(→ [[game-design-notes]]), 일반 코드 구조(→ [[design-pattern-notes]])
> 적용 범위: 개념은 엔진 독립, 구현은 대부분 게임엔진 일반에 종속
> 관련 노트: [[game-design-notes]] (원리), [[math-algorithm-notes]] (빌딩블록)
> 평생 노트 정책: 인덱스 표는 portable, 풀노트는 구현 의사코드 + 파라미터 권장값 포함
> 승격 임계치: 항목 9개 이상 시 카테고리(이동/전투/오디오) 단위 분리 검토
> 풀노트 작성 기준: 인덱스 1줄만으로 구현/적용이 불충분한 항목. 자명한 항목만 인덱스로 종료
> 작성 시작: 2026-05-15

---

## 태그 목록

### 카테고리 (무엇)
- `#이동` `#점프` `#카메라` `#입력` `#충돌`
- `#전투` `#데미지` `#난수` `#가챠` `#밸런싱`
- `#오디오` `#UI` `#피드백` `#애니메이션` `#VFX`
- `#슬롯` `#시너지` `#곡선` `#튜토리얼` `#시퀀스`

### 장르 (어디)
- `#2D` `#3D` `#플랫포머` `#액션` `#전략` `#로그라이크` `#캐주얼`

### 효과/의도 (왜)
- `#게임필` `#응답성` `#관용성` `#예측가능성` `#몰입` `#결정론`

### 구현 매체 (어떻게)
- `#물리엔진` `#커스텀적분` `#보간` `#콜백` `#게이팅`

---

# 인덱스

| # | 기능 | 기법 이름 | 한 줄 요약 | 종속성 |
|---|------|----------|----------|--------|
| 1 | 2D 점프 곡선 | Asymmetric Jump (Variable Gravity) | 상승/하강에 서로 다른 중력 → 묵직한 무게감 + 빠른 응답성 | `#게임엔진일반` |
| 2 | 가챠 등급 보정 | Pity 등급 시프트 + Fallback | 누적 실패 시 확률 점진 증가, 천장 도달 시 등급 보장 | `#언어독립` |
| 3 | 강화 보상 스케일링 | Power-Law Enhancement Curve | 멱함수로 후반 보상이 가파르게(또는 완만하게) 변하는 곡선 | `#언어독립` |
| 4 | 시너지 카운팅 | Unique-ID Synergy Counter | HashSet으로 동일 ID 중복 제거하며 종류 수 카운트 | `#언어독립` |
| 5 | 데미지 산출 | D20 Lerp 보간 데미지 | 굴림값(1~20)을 min/max 데미지 범위에 Lerp로 매핑 | `#언어독립` |
| 6 | 볼륨 슬라이더 | AudioMixer Linear→dB 지각 변환 | 선형 슬라이더를 로그 dB로 변환해 청각 지각에 일치 | `#오디오엔진` |
| 7 | 슬롯 확장 시스템 | Unlocked vs Max 게이팅 | 활성/최대 슬롯을 분리해 점진적 콘텐츠 확장 | `#언어독립` |
| 8 | 튜토리얼 결정론 | 고정 큐 주입으로 랜덤 대체 | RNG 호출 지점에 사전 정의 큐를 주입해 결정론 보장 | `#언어독립` |
| 9 | 시퀀스 연결 | onComplete 콜백으로 호출자가 전이 결정 | 시퀀스가 종료를 알리되 다음 전이는 호출자가 결정 | `#OOP` `#FP` `#언어독립` |
| 10 | 길게 누르기 반복 입력 | Hold-to-Repeat (Initial Delay + Interval) | 버튼을 길게 누르면 초기 딜레이 후 일정 간격으로 onClick 반복 발동 | `#게임엔진일반` |
| 11 | 2D 배경 깊이감 | Parallax Scrolling (속도 차 레이어) | 카메라 이동량에 거리 반비례 계수를 곱해 배경 레이어를 이동시켜 원근감 생성 — 멀수록 적게 이동 | `#게임엔진일반` |
| 12 | 순차 큐 + 즉시 우회 팝업 | Sequential Queue + Concurrent Bypass | 애니메이션 효과를 Queue로 순차 재생하되 동시 표시가 의도인 효과(힐/쉴드)는 별도 SpawnInstant 진입점으로 큐 우회 — 데이터 흐름에 WaitForSeconds 재추가 없이 시각 타이밍 분리 | `#게임엔진일반` |
| 13 | 데미지 판정 | 주사위 합산값(summaryValue) 판정 | 슬롯 배치 주사위를 합산한 summaryValue를 diceMin/diceMax/criticalValue와 비교 — D20과 달리 플레이어 주사위 선택이 결과에 직결 | `#언어독립` |
| 14 | 속성·시너지 효과 분리 | AttrEffect / SynergyAttrEffect 이중 호출 | 속성 기본 효과(AttrEffect)와 시너지 보너스 효과(SynergyAttrEffect)를 독립 클래스로 분리 → DiceController가 순차 호출. 기각 대안: baseOnly 플래그 — 책임 혼재 | `#언어독립` |
| 15 | 시너지 데이터 소스 관리 | SynergyDataSO 단일 소스 원칙 | 시너지 보너스 수치는 SynergyDataSO에만 보관 — weapon SO에 분산 시 툴팁 미반영. 기각 대안: reinforced 필드 패러다임 유지 | `#언어독립` |
| 16 | 시드 기반 의사난수 | 의사난수 시드 결정론 (RNG Manipulation) | 컴퓨터는 시드 초기값으로 결정론적 난수 배열을 생성 — 시드 조건을 플레이어가 제어하면 모든 결과가 예측/확정 가능. 포켓몬·마리오의 고전 사례와 현대 방어 설계 | `#언어독립` |
| 17 | 세이브 데이터 직렬화 | 패스워드 세이브 시스템 (Password Save) | 게임 상태를 수치화 + 랜덤 솔트 + 체크섬으로 인코딩해 문자열로 출력 — 배터리 칩 없이 플레이어가 직접 기록·입력하는 아날로그 세이브 방식 | `#언어독립` |
| 18 | 메모리 취약점 익스플로잇 | 임의 코드 실행 (ACE, Arbitrary Code Execution) | 코드·데이터가 동일 RAM에 공존하는 폰노이만 구조의 특성 + 프로그램 카운터 오염으로 데이터 영역이 실행 코드가 됨 — 컨트롤러 입력으로 새 프로그램을 즉석 작성하는 스피드런 기법 | `#언어독립` |
| 19 | VFX 블렌딩 모드 | 가산(Additive) / 곱하기(Multiply) 블렌딩 | 색상값을 더해 밝아지거나(Additive), 곱해 어두워지는(Multiply) 렌더링 합성 — 빛 이펙트는 어두운 배경에서, 그림자는 밝은 배경에서 효과적. 배경 의존성 이해가 핵심 | `#엔진독립` |
| 20 | 시야·충돌 판정 | 레이캐스팅 (Raycasting) | 오브젝트에서 선을 쏘아 충돌을 검사. 몬스터 시야 판정·2D→3D 연출·지형 탐지까지 활용. 거리→시야각→레이 순 3단계 필터로 연산량 절감 | `#엔진독립` |
| 21 | 지형 적응 애니메이션 | 절차적 애니메이션 + 역운동학 (IK) | 발 목적지를 먼저 정하고 관절 각도를 역산(IK). 고정 애니메이션 없이 불규칙 지형에서 자연스러운 보행 실시간 생성 | `#엔진독립` |
| 22 | 길찾기 | 다익스트라 / A* / 플로우 필드 | 지형을 그래프로 변환 후 최단 경로 탐색. 단일 유닛은 A*(휴리스틱으로 탐색 범위 축소), 대량 유닛은 플로우 필드(맵 전체 방향 사전 계산)로 연산량 절감 | `#언어독립` |
| 23 | 픽셀 아트 품질 기법 | 더블픽셀 제거 / 서브픽셀 애니메이션 / 디더링 | 낮은 해상도·제한된 팔레트에서 품질을 높이는 4가지 기법. 선 규칙(더블픽셀·재기), 서브픽셀 애니메이션, 컬러 외곽선, 디더링 | `#언어독립` |

---


# 풀노트

## 1. 비대칭 점프 (Asymmetric Jump)

_상승과 하강에 서로 다른 중력을 적용해 떨어질 때 더 빠르게 낙하시키는 점프 곡선. 묵직한 무게감 + 빠른 응답성._

**설명**
순수 포물선(상승 시간 = 하강 시간)은 물리적으로는 맞지만 체감상 "둥둥 뜨는" 느낌을 준다. 하강 중력을 상승의 1.5~2.5배로 키우면 게임필이 즉시 개선됨.

표준 패키지로 묶이는 보조 기법:
- **Variable Jump Height** — 점프 버튼을 떼면 상승 중력 증가 → "짧은 점프 / 긴 점프"
- **Coyote Time** — 절벽에서 떨어진 후 짧은 윈도우 동안 점프 입력 허용
- **Jump Buffering** — 착지 직전 입력 저장해 착지 즉시 발동
- **Apex Modifier** — 최고점 근처 중력 약화 (체공감 강조)

이 다섯을 모두 적용한 것이 현대 플랫포머의 "점프 관용성 세트". 대표: Super Mario Bros, Celeste, Hollow Knight.

**구현**
```
// 매 프레임
if velocity.y < 0:
    // 하강 — 추가 중력
    velocity.y += gravity * (fallMultiplier - 1) * dt
elif velocity.y > 0 and not jumpHeld:
    // 상승 중 버튼 뗌 — 짧은 점프
    velocity.y += gravity * (lowJumpMultiplier - 1) * dt

// Coyote Time
if grounded:
    coyoteTimer = COYOTE_DURATION
elif coyoteTimer > 0:
    coyoteTimer -= dt

if jumpPressed and coyoteTimer > 0:
    velocity.y = jumpPower
    coyoteTimer = 0
```

권장 파라미터 시작점:
- `fallMultiplier`: 2.0~2.5
- `lowJumpMultiplier`: 2.0
- `coyoteDuration` / `jumpBufferDuration`: 0.1~0.15s

⚠ **주의점**
- 물리 엔진과 충돌 가능 — `velocity` 직접 조작 대신 `Rigidbody.gravityScale` 동적 변경이 더 안전 (Unity)
- `fallMultiplier`가 너무 크면 공중 제어 시간이 짧아져 플랫폼 안착 어려움 — 레벨 디자인과 함께 튜닝
- Coyote/Buffer 타이머를 디버그 UI로 노출하면 튜닝 속도 ↑


`#점프` `#2D` `#플랫포머` `#게임필` `#응답성`
> 관련: [[game-design-notes]] #1 (관용성 디자인 원리), [[math-algorithm-notes]] #17 오일러 적분 (매 프레임 `velocity += accel * dt`로 비대칭 중력을 구현하는 수학 빌딩블록) | 종속성: `#게임엔진일반` (개념 독립, 구현은 물리/시간 시스템 필요)

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
    grade = RollGrade(pity_counter)   // math-algorithm #6 소프트+하드 pity 적용
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


`#가챠` `#확률` `#밸런싱` `#게임필`
> 관련: [[math-algorithm-notes]] #5 가중 랜덤, #6 Pity 누적 시프트 (수학 기반) | 종속성: `#언어독립`

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


`#밸런싱` `#곡선` `#게임필`
> 관련: [[math-algorithm-notes]] #4 멱함수 곡선 (수학 빌딩블록), [[unity-feature-notes]] #35 AnimationCurve (Unity 대안) | 종속성: `#언어독립`

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


`#시너지` `#카운팅` `#게임필`
> 관련: [[math-algorithm-notes]] #8 HashSet 유니크 카운트 (수학 빌딩블록), [[math-algorithm-notes]] #1 Lerp | 종속성: `#언어독립`

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


`#전투` `#데미지` `#게임필`
> 관련: [[math-algorithm-notes]] #1 Lerp (수학 기반), [[math-algorithm-notes]] #3 Clamp/Clamp01 (안전망) | 종속성: `#언어독립`

## 6. AudioMixer Linear→dB 지각 변환 (볼륨 슬라이더)

_UI 슬라이더의 선형 값(0~1)을 `dB = 20·log₁₀(linear)` 변환 후 `AudioMixer.SetFloat`에 전달. 슬라이더 50% = 약 -6dB ≈ 인간 귀에 "반쯤 줄었다"는 느낌._

**설명**
`AudioMixer.SetFloat("Volume", linearValue)`에 선형 값(0~1)을 그대로 전달하면 볼륨 조절이 부자연스럽다 — 슬라이더 90%에서 10%까지는 차이가 적게 느껴지다가 마지막 10%에서 급격히 줄어드는 느낌. 인간 청각이 로그 특성이기 때문.

AudioMixer의 볼륨 파라미터는 **dB 단위**. 일반 범위: -80dB (무음) ~ 0dB (원본). dB로 전달하면 슬라이더 절반 = 볼륨 절반의 *지각*을 달성.

**구현**
```csharp
// SoundManager (CasualStrategy 패턴)
public class SoundManager : MonoSingleton<SoundManager>
{
    [SerializeField] private AudioMixer audioMixer;
    private const float MIN_DB = -80f;

    public void SetMasterVolume(float linear)  // linear ∈ [0, 1]
    {
        float db = linear <= 0f ? MIN_DB : Mathf.Log10(linear) * 20f;
        audioMixer.SetFloat("MasterVolume", db);
    }

    public void SetBGMVolume(float linear)
    {
        float db = linear <= 0f ? MIN_DB : Mathf.Log10(linear) * 20f;
        audioMixer.SetFloat("BGMVolume", db);
    }

    public void SetSFXVolume(float linear)
    {
        float db = linear <= 0f ? MIN_DB : Mathf.Log10(linear) * 20f;
        audioMixer.SetFloat("SFXVolume", db);
    }
}
```

AudioMixer 셋업:
1. AudioMixer 에셋 → Master + BGM/SFX 자식 그룹 생성
2. 각 그룹 Volume 파라미터 Expose: Inspector 우클릭 → "Expose to script" → 이름 지정
3. `audioMixer.SetFloat(exposedName, dbValue)` 호출

⚠ **주의점**
- **`Mathf.Log10(0)` = -Infinity** — `linear <= 0f ? MIN_DB : Mathf.Log10(linear) * 20f` 가드 필수. 가드 없으면 AudioMixer 파라미터가 locked 상태가 되어 이후 SetFloat 무시됨 (볼륨 0 → 복구 불가 버그)
- **-80dB가 관행** — AudioMixer Inspector 기본 최솟값. -144dB 등 극단값 전달 시 일부 Unity 버전에서 오동작
- **Exposed Parameter 이름 오타** — `SetFloat("MaterVolume", db)` 같은 오타는 silent fail (false 반환, 예외 없음). const 문자열 상수 관리 권장
- **PlayerPrefs 저장 단위** — 선형(0~1)으로 저장, 로드 시 dB 변환. dB 저장 후 역변환은 -∞ 처리가 복잡
- **GetFloat로 UI 동기화** — 초기화 시 `GetFloat → DBToLinear → slider.value`. `DBToLinear: Mathf.Pow(10f, db / 20f)`


`#오디오` `#밸런싱` `#게임필`
> 관련: [[math-algorithm-notes]] #2 Linear↔dB 로그 변환 (수학 기반), [[unity-feature-notes]] #14 AudioMixer, #27 Mathf.Log10 | 종속성: `#Unity전용` (AudioMixer API), 수학 개념은 `#언어독립`

## 7. Unlocked vs Max 게이팅 (슬롯 확장 시스템)

_활성 슬롯 개수(unlocked)와 최대 슬롯 개수(max)를 분리해 점진적 콘텐츠 확장. "N/M 슬롯" UI로 현재 진행도와 잠재력을 동시 표시._

**설명**
플레이어에게 모든 기능을 처음부터 열어주면 압도된다. 반면 계속 잠금만 풀면 "언제 다 열리지?"라는 불안감이 든다. Unlocked/Max 이중 게이팅은 *현재*와 *목표*를 동시에 제시한다.

핵심 개념:
- **Max**: 시스템이 허용하는 절대 상한. 게임 디자인으로 결정 (예: 인벤토리 최대 60칸)
- **Unlocked**: 플레이어가 현재 사용 가능한 수. 게임 진행/재화 소모로 증가
- **Locked**: `Max - Unlocked`. 잠겨 있지만 "언젠가 열 수 있다"는 기대감 제공

게임 대표 사용:
- 인벤토리/가방 슬롯 (Path of Exile, 디아블로 시리즈)
- 유닛 배치 슬롯 (전략 게임 진영 업그레이드)
- 장비 장착 슬롯 (레벨/직업 해금)
- 제작 슬롯 (스토리 진행으로 해금)
- CasualStrategy: 유닛 배치 슬롯 (레벨업 + 재화 소모로 unlock)

**구현**
```csharp
// 슬롯 데이터 구조
[System.Serializable]
public class SlotSystem
{
    public int unlocked;    // 현재 사용 가능 슬롯
    public int max;         // 최대 슬롯

    public bool CanAdd => unlocked > currentCount;
    public bool CanUnlock => unlocked < max;

    public bool TryUnlock()
    {
        if (unlocked >= max) return false;
        unlocked++;
        return true;
    }
}

// UI 표시 (Unlocked vs Max)
// "{current}/{unlocked} (Max: {max})"
// 프로그레스 바: current / unlocked
// 시각적 Lock 표시: hidden slot = 잠김 아이콘
```

경고 주의점:
- Max는 절대 변경 금지(게임 디자인 범위) — 런타임에 Max를 줄이면 저장 데이터와 충돌. Max는 기획 데이터(ScriptableObject)로 고정
- Unlocked 저장 영속성 — PlayerPrefs에 unlocked 값 저장. 버전 업데이트로 Max 증가 시 unlocked은 그대로 (기존 플레이어 불이익 없음)
- UI 표시 규칙 — "5/10"만 보여주면 "앞으로 5개 더?"라는 혼동. "5/8 (Max: 10)" 또는 프로그레스 바 + Max 라벨로 명확히 구분
- 중간 저장(Partial Unlock) 금지 — 슬롯 unlock은 한 번에 1개 단위. "반만 해금"이라는 상태가 없어야 함
- Unlock 비용 증가 곡선 — 후반 슬롯일수록 unlock 비용 증가 (멱함수 곡선, [[math-algorithm-notes]] #4). 곡선 구체적 검증은 시뮬레이션 필수


`#슬롯` `#게이팅` `#게임필`
> 관련: [[math-algorithm-notes]] #4 멱함수 곡선 (비용 곡선), [[math-algorithm-notes]] #8 HashSet (시너지 카운팅과 조합) | 종속성: `#언어독립`

## 8. 고정 큐 주입으로 랜덤 대체 (튜토리얼 결정론)

_RNG 호출 지점에 사전 정의된 고정 큐(seed queue)를 주입해 튜토리얼 중 결정론적 결과 보장. 플레이어가 항상 같은 경험을 하도록 제어._

**설명**
랜덤 요소(가챠, 드롭, 크리티컬)가 있는 게임에서 튜토리얼은 "운 나쁜" 시나리오를 방지해야 한다. 첫 가챠가 꽝이면 이탈률 급증. 해결책: 튜토리얼 구간에만 주입 가능한 고정 큐를 RNG 시스템 앞단에 설치.

동작 방식:
1. 보통 때는 진짜 RNG(System.Random, Unity.Random) 사용
2. 튜토리얼 전용 큐를 준비: `[0.05, 0.72, 0.99, ...]` (0.05 = 5% 확률 = UR)
3. RNG 호출 시 큐가 비어있지 않으면 큐에서 꺼내서 반환
4. 튜토리얼 종료 시 큐 비우기

장점:
- 테스트 가능: 특정 큐를 넣으면 항상 같은 결과
- 저장 불필요: 튜토리얼 상태 = 큐 소진 여부
- 기존 RNG 코드 수정 최소화: 한 겹의 추상화만 추가

**구현**
```csharp
public class DeterministicRNG
{
    private Queue<float> _fixedQueue;
    private System.Random _rng;

    public float Next()
    {
        if (_fixedQueue != null && _fixedQueue.Count > 0)
            return _fixedQueue.Dequeue();
        return (float)_rng.NextDouble();
    }

    // 튜토리얼 시작 시 호출
    public void InjectQueue(float[] values)
    {
        _fixedQueue = new Queue<float>(values);
    }

    // 튜토리얼 종료 시 호출
    public void ClearQueue()
    {
        _fixedQueue = null;
    }
}
```

경고 주의점:
- 큐 길이 부족 — 튜토리얼 중 RNG 호출 횟수보다 큐가 짧으면 이후는 진짜 RNG 사용. "우리는 공정합니다"라는 인상을 주려면 큐가 완전히 소진될 때만 진짜 RNG 전환
- 큐 재사용 금지 — 한 번 소진된 큐는 재사용 금지. 튜토리얼 재시작 시 새 큐 필요
- 디버그 전용 큐 — 개발자 메뉴에서 큐 주입 기능 추가하면 버그 재현에 탁월. "이번 플레이 RNG 시드: XXXXX" 로그와 함께 큐 저장
- 확률 값의 범위 — 큐에 저장된 값은 `[0, 1)`. 외부에서 확률 비교 시 일관성 유지. "0.05 미만 = UR" 로직과 동일
- 멀티플레이어/온라인 — 큐 주입은 클라이언트 로컬 전용. 서버 RNG는 주입 불가 (치트 방지). 온라인 튜토리얼은 서버에서 별도 시드 관리


`#튜토리얼` `#결정론` `#테스트` `#관용성`
> 종속성: `#언어독립`

## 9. onComplete 콜백으로 호출자가 전이 결정 (시퀀스 연결)

_시퀀스(애니메이션, 연출)가 종료를 onComplete 콜백으로 알리되, *다음 시퀀스 선택*은 호출자가 결정. 각 시퀀스는 자기 완료만 책임._

**설명**
게임 시퀀스(공격 연출, 대화, 이벤트)는 여러 단계로 연결된다. 각 단계가 *다음 단계로 무엇을 할지*까지 결정하면 **순환 의존성**(A가 B를 알고, B가 A를 아는)이 발생하고, 수정 시 연쇄 변경이 일어난다.

onComplete 패턴의 핵심 원칙:
1. 각 시퀀스는 자기 완료만 책임 (단일 책임)
2. 완료 시 "끝났다"는 신호만 보냄 (어떤 값/상태와 함께)
3. 호출자(Controller/Manager)가 신호를 받고 다음 시퀀스 결정

```
호출자(Controller)  --시작-->  Sequence A
                                    |
                              (onComplete)
                                    |
호출자(Controller)  <--결과------  A 끝남
호출자(Controller)  --조건 판단-->  Sequence B 또는 C
```

**구현 (CasualStrategy 패턴)**
```csharp
// 시퀀스 인터페이스
public interface ISequence
{
    void Play(Action onComplete);
}

// 호출자: 시퀀스 전이 결정
public class PlayerTurnController
{
    private ISequence _current;

    private void StartTurn()
    {
        PlaySequence(new DrawCardSequence(), OnDrawComplete);
    }

    private void OnDrawComplete()
    {
        if (HasSynergyActivation())
            PlaySequence(new SynergySequence(), OnSynergyComplete);
        else
            PlaySequence(new AttackSequence(), OnAttackComplete);
    }

    private void PlaySequence(ISequence seq, Action onComplete)
    {
        _current = seq;
        _current.Play(onComplete);
    }
}
```

경고 주의점:
- 콜백 중첩 깊이 주의 — 연속된 if-else가 깊어지면 콜백 지옥. 복잡한 상태 기계는 FSM(유한 상태 기계)으로 전환 고려
- Dispose/취소 처리 — 시퀀스 도중 씬 전환/종료 시 onComplete가 호출되지 않을 수 있음. CancellationToken 또는 isActive 플래그 추가
- 콜백 파라미터 오염 — onComplete에 여러 정보를 담고 싶은 유혹. 그 결과 인터페이스 변경 시 연쇄 수정. 최소 정보만 전달하거나 Result 객체로 캡슐화
- 순환 참조 방지 — 시퀀스가 호출자를 직접 알면 onComplete 우회 가능. 인터페이스/델리게이트로 분리
- 유닛 테스트 — 각 시퀀스는 단독 테스트 가능해야 함 (onComplete만 Mock). 호출자 테스트는 Mock 시퀀스로 전이 로직 검증


`#시퀀스` `#콜백` `#OOP` `#FP`
> 종속성: `#언어독립`

## 10. Hold-to-Repeat 버튼 (길게 누르기 반복 입력)

_버튼을 누르고 있으면 초기 딜레이 후 일정 간격으로 클릭 이벤트가 반복 발동되는 입력 패턴._

**설명**
키보드/게임패드의 "키 반복(key repeat)"과 동일한 원리를 UI 버튼에 적용. 수량 조정 버튼(+/-), 가챠 연속 구매, 슬라이더 미세 조정 등 "여러 번 클릭이 필요한 동작"에서 표준 UX.

핵심 파라미터 2개:
- **Initial Delay (~0.4s)** — 첫 입력과 반복 시작 사이의 간격. 짧으면 짧은 클릭이 반복으로 오인됨, 길면 답답함
- **Repeat Interval (~0.1s)** — 반복 발동 간격. 10Hz 정도가 표준

대표 적용:
- OS 키보드 반복 입력 (Windows/macOS 모두 동일 원리)
- 수량 조정 위젯 (쇼핑 카트 +/-)
- 게임 내 가챠 "10연차" + "롱프레스로 연속 구매"
- 디버그 도구의 값 조정

**구현**
```
// 상태
initialDelay = 0.4s
repeatInterval = 0.1s
repeatRoutine = null

// 입력 이벤트
function OnPointerDown():
    StopRepeat()
    repeatRoutine = StartCoroutine(RepeatLoop())

function OnPointerUp():    StopRepeat()
function OnPointerExit():  StopRepeat()    // 드래그 이탈 시도 정지
function OnDisable():      StopRepeat()    // 비활성화 안전망

// 코루틴
function RepeatLoop():
    yield WaitForSecondsRealtime(initialDelay)
    while button.interactable:
        button.onClick.Invoke()
        yield WaitForSecondsRealtime(repeatInterval)
```

⚠ **주의점**
- **PointerExit 처리 필수** — 누른 채로 버튼 밖으로 드래그하면 OnPointerUp이 발동 안 됨. 드래그 이탈 시점에 명시적으로 정지
- **OnDisable 안전망** — 패널 닫힘/씬 전환 시 코루틴이 살아있으면 NRE 가능
- **Realtime vs scaled** — 일시정지 메뉴에서도 동작해야 하면 `WaitForSecondsRealtime` 사용. 게임 속도에 종속이면 `WaitForSeconds`
- **터치 vs 마우스** — 모바일에서 손가락이 살짝 움직이면 OnPointerExit 발동 가능. 허용 임계값 두거나 `EventSystem.pixelDragThreshold` 조정
- **interactable=false 동안 발동 방지** — 매 루프에서 검사. 도중에 버튼이 비활성화되면 즉시 정지


`#입력` `#UI` `#응답성` `#관용성` `#코루틴`
> 종속성: `#게임엔진일반` (PointerEvent 인터페이스가 있는 UI 시스템 필요)

## 11. Parallax Scrolling (시차 스크롤)

_카메라 이동량에 레이어별 `parallaxFactor ∈ [0, 1]`를 곱해 배경 레이어를 이동. 멀수록 느리게 → 시각적 원근감 생성._

**설명**
2D 게임에서 원근감을 표현하는 고전 기법. 실세계에서 멀리 있는 물체는 이동 중에 느리게 지나가는 것과 동일 원리. 뇌는 속도 차이를 깊이로 해석.

`parallaxFactor`:
- `0` → 카메라와 함께 이동 (최전경, HUD처럼 고정된 느낌)
- `0 < f < 1` → 카메라보다 느리게 이동 (배경 레이어)
- `1` → 이동 안 함 (무한히 먼 배경 — 하늘 등)

실용 레이어 구성 예:
| 레이어 | factor | 의미 |
|---|---|---|
| 전경 나뭇잎 | 0.1 | 가장 가까움 |
| 근경 건물 | 0.4 | 중간 |
| 원경 산 | 0.7 | 멀리 |
| 하늘 | 1.0 | 이동 안 함 |

**구현**
```
// 방법 A: 카메라 절대 위치 기반 (누적 오차 없음, 권장)
function Update():
    parallaxOffset = cameraPos.x * parallaxFactor
    layer.position.x = startPosition.x + parallaxOffset

// 방법 B: 카메라 델타 누적 (시작 위치가 임의적일 때)
function Update():
    cameraDelta = cameraPos.x - lastCameraPos.x
    layer.position.x += cameraDelta * parallaxFactor
    lastCameraPos = cameraPos.x
```

```csharp
// Unity C# (방법 A, LateUpdate에서 실행)
public class ParallaxLayer : MonoBehaviour
{
    [SerializeField] private float parallaxFactor;   // 0~1
    private Transform _cam;
    private float _startX;

    private void Awake()
    {
        _cam = Camera.main.transform;
        _startX = transform.position.x;
    }

    private void LateUpdate()   // 카메라 이동 후 적용
    {
        float offset = _cam.position.x * parallaxFactor;
        transform.position = new Vector3(
            _startX + offset,
            transform.position.y,
            transform.position.z);
    }
}
```

무한 타일링:
```csharp
// 카메라가 textureUnitWidth 절반 이상 벗어나면 레이어 재배치
if (Mathf.Abs(_cam.position.x - transform.position.x) >= textureUnitWidth)
{
    float offset = (_cam.position.x - transform.position.x) % textureUnitWidth;
    transform.position = new Vector3(
        _cam.position.x + offset,
        transform.position.y,
        transform.position.z);
}
```

⚠ **주의점**
- **LateUpdate 사용** — 카메라가 Update에서 이동한다면 동일 프레임 Update에서 레이어를 이동시키면 1프레임 lag. `LateUpdate`에서 카메라 위치 참조가 정확
- **방법 A vs B** — 방법 A(절대 위치 기반)는 누적 오차 없음. 방법 B(델타)는 카메라가 순간이동해도 자연스럽게 동작. 통상 방법 A 권장
- **카메라 방향과 레이어 이동 방향** — 카메라 오른쪽 이동 시 배경은 왼쪽으로 보여야 함(실세계). 위 공식 `startX + cameraPos * factor`는 카메라 방향과 같은 방향으로 레이어가 이동하므로 배경이 카메라보다 느리게 스크롤 — 의도한 시차 효과 달성
- **Y축 parallax** — 수직 스크롤 게임에서 Y factor를 추가. 통상 `Y_factor = X_factor / 2~3`으로 약하게
- **z값 처리 (2D)** — Unity 2D에서는 SortingOrder로 렌더 순서 제어. z값을 깊이로 쓰는 방식도 가능하나 orthographic 카메라에서는 시차 없음


`#2D` `#카메라` `#게임필` `#이동`
> 종속성: `#게임엔진일반`

## 12. 순차 큐 + 즉시 우회 팝업 (Sequential Queue + Concurrent Bypass)

_애니메이션 효과를 Queue로 순차 재생하되, 동시 표시가 의도인 효과(힐/쉴드)는 별도 SpawnInstant 진입점으로 큐를 우회. 데이터 흐름에 WaitForSeconds 재추가 없이 시각 타이밍 분리._

**설명**
전투 로그 같은 이벤트 스트림을 UI로 표시할 때 기본 설계는 **순차 재생**(Sequential Queue)이다. 공격A -> 공격B -> 힐C 순서로 표시. 그런데 "동시에 처리된 힐 여러 개를 하나씩 순차 재생"하면 5힐에 5초가 걸리는 어색한 UX가 된다.

해결책: 큐를 우회하는 **SpawnInstant** 진입점. 일반 효과는 큐를 경유(순차 + 전환 대기), 동시 표시 효과는 즉시 생성(중첩 허용).

```
데이터 흐름:
  Event Stream
    |-- 효과가 순차 의존? (버프/디버프) --> Queue.Enqueue --> Sequence.Play
    |-- 효과가 동시 표시? (힐/쉴드)   --> SpawnInstant --> 독립적 Popup
```

**구현**
```csharp
// QueueSequence (순차 전용)
public class QueueSequence : MonoBehaviour
{
    private Queue<System.Action> _queue = new();
    private bool _isPlaying;

    public void Enqueue(System.Action effect)  // 전환 대기 필요
    {
        _queue.Enqueue(effect);
        if (!_isPlaying) PlayNext();
    }

    public void SpawnInstant(System.Action effect)  // 우회 - 즉시 실행
    {
        effect?.Invoke();
    }

    private void PlayNext()
    {
        if (_queue.Count == 0) { _isPlaying = false; return; }
        _isPlaying = true;
        var effect = _queue.Dequeue();
        effect?.Invoke();
        // onComplete에서 PlayNext() 호출 (시퀀스가 완료를 알림)
    }
}

// 사용 예
void OnDamage(DamageEvent e)
{
    _queue.Enqueue(() => ShowDamagePopup(e));  // 순차: 공격 순서대로
}

void OnHeal(HealEvent e)
{
    _queue.SpawnInstant(() => ShowHealPopup(e));  // 즉시: 모든 힐 동시 표시
}
```

경고 주의점:
- SpawnInstant 오용 — 모든 이벤트를 SpawnInstant로 처리하면 큐가 무의미해짐. 기준: "이 이펙트가 *순서대로* 보여야 UX에 중요한가?" 아니면 SpawnInstant
- 동시 팝업 겹침 — 힐 10개가 동시에 뜨면 화면이 난잡. SpawnInstant 팝업 위치에 오프셋(스택) 적용. "HIT! x5" 형식의 병합 표시도 고려
- 데이터와 시각의 분리 — 데이터 처리는 이미 완료된 상태. Queue/SpawnInstant는 *시각적 재생*만 제어. 데이터 흐름에 WaitForSeconds 재추가 금지
- Mix 사용 시 주의 — Queue 중인 효과와 SpawnInstant 효과가 같은 위치에 뜨면 순서 혼동. SpawnInstant는 별도 레이어/영역에 표시
- 테스트 — Queue가 비어있을 때 SpawnInstant만 호출되면 isPlaying 플래그 오염 없음 (안전). 반대로 Queue 실행 중 SpawnInstant는 자유롭게 호출 가능 (독립적)


`#시퀀스` `#UI` `#게임필`
> 종속성: `#게임엔진일반` (UI 시스템 + 애니메이션/시퀀스 시스템)

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


`#전투` `#데미지` `#밸런싱` `#게임필`
> 관련: [[game-technique-notes]] #5 D20 Lerp 보간 데미지 (이전 방식 — D20은 이 프로젝트에서 summaryValue로 대체됨), [[math-algorithm-notes]] #1 Lerp, #3 Clamp | 종속성: `#언어독립`

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

`#시너지` `#전투` `#OOP`
> 관련: [[game-technique-notes]] #4 시너지 카운팅, #15 시너지 데이터 중앙화 | 종속성: `#언어독립`

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

`#시너지` `#데이터` `#아키텍처`
> 관련: [[game-technique-notes]] #14 속성·시너지 효과 분리, #4 시너지 카운팅 | 종속성: `#언어독립`

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
- 튜토리얼·결정론 보장이 목적인 경우: 역으로 시드를 노출·고정해 재현 가능성을 의도적으로 제공 ([[game-technique-notes]] #8).
- 스피드런 커뮤니티에서는 RNG 조작이 합법적 기술로 인정되기도 함 — 설계 구멍인지 의도된 깊이인지는 커뮤니티와 개발사 정책이 결정.


`#난수` `#결정론` `#예측가능성`
> 관련: [[game-technique-notes]] #8 튜토리얼 결정론 (고정 큐로 RNG 대체 — 결정론을 의도적으로 활용하는 정반대 사례) | 종속성: `#언어독립`

## 17. 패스워드 세이브 시스템 (Password Save)

_게임 상태를 수치화 + 랜덤 솔트 + 체크섬으로 인코딩해 문자열로 출력, 플레이어가 직접 기록·재입력하는 세이브 방식. 배터리 백업 칩이 없던 1980년대 하드웨어 한계의 소프트웨어 대안._

**개념**
1980년대 게임 카트리지는 배터리가 달린 메모리 칩이 없으면 데이터를 저장할 수 없었다. 악마성 드라큘라 2(Castlevania II)는 비용 문제로 배터리 칩 대신 세이브 데이터를 문자열(비밀번호)로 인코딩해 플레이어가 직접 메모하도록 하는 방식을 택했다.

**인코딩 4단계**

**① 불필요한 정보 생략**
현재 위치 좌표처럼 복원 불필요한 데이터는 아예 저장하지 않는다. 재개 시 캐릭터는 항상 해당 스테이지 시작 지점에서 리스폰. 저장 대상 최소화 → 비밀번호 길이 단축.

**② 게임 상태 수치화**
캐릭터 레벨과 아이템 소지 상태를 단일 숫자로 매핑:
```
레벨 1 + 단검       → 1
레벨 5 + 황금 단검  → 52
...
```
상태 조합표를 숫자 1개로 치환해 데이터 압축.

**③ 랜덤 솔트 추가**
인코딩된 데이터에 무작위 값을 혼합한다. 동일한 게임 상태라도 매번 다른 비밀번호가 출력되게 하기 위함. 복호화 시 솔트를 제거하면 원본 데이터가 복원된다.

**④ 체크섬 추가**
모든 인코딩 데이터의 합계를 비밀번호 끝에 덧붙인다. 복호화 시 수신한 데이터의 합을 재계산해 체크섬과 대조 — 일치하지 않으면 조작된 비밀번호로 판별하고 차단.

```
인코딩:  state_num + salt → data
출력:    data + checksum(data)

복호화:  checksum 검증 → 불일치 시 차단
         → salt 제거 → state 디코딩 → 게임 재개
```

**설계 판단 기준**
- 체크섬은 완벽한 방어가 아니다. 인코딩 알고리즘이 역산되면 유효한 조작 비밀번호 생성이 가능하다 — 당시에도 치트 비밀번호를 공유하는 문화가 존재했다.
- 현대 세이브 파일 무결성 검증(HMAC 해시 서명)은 같은 원리의 발전형이다.

대표 사례:
- **악마성 드라큘라 2 (Castlevania II, 1987)** — 수치화 + 솔트 + 체크섬 조합의 대표 사례
- **메가맨** 시리즈 — 4자리 숫자로 스테이지 클리어 상태 저장
- **당시 게임 문화** — 비밀번호를 공책에 빽빽이 기록하거나 친구 간 공유하는 아날로그 세이브 문화


`#난수` `#결정론`
> 관련: [[game-technique-notes]] #16 의사난수 시드 결정론 (솔트에 쓰이는 난수), [[math-algorithm-notes]] (체크섬 알고리즘) | 종속성: `#언어독립`

## 18. 임의 코드 실행 (ACE, Arbitrary Code Execution)

_코드와 데이터가 동일한 RAM에 공존하는 폰노이만 구조의 특성을 이용해, 프로그램 카운터를 데이터 영역으로 오염시킴으로써 컨트롤러 입력값을 실행 명령어로 만드는 취약점 기법._

**개념**
슈퍼 마리오 화면에서 핑퐁 게임이 구동되거나 젤다에서 다른 게임의 연출이 재현되는 현상들이 존재한다. 외부 프로그램 없이 순정 소프트웨어 + 기기 + 컨트롤러 조작만으로 구현된다. 핵심은 고전 컴퓨터의 메모리 구조다.

**핵심 원리**

**폰노이만 구조 — 코드와 데이터의 동거**
고전 게임은 실행 시 게임 로직(어셈블리 명령어)과 게임 데이터(캐릭터 위치, 그래픽, 컨트롤러 입력값)를 동일한 RAM에 적재한다. CPU 입장에서는 두 가지 모두 동일한 이진수(0과 1)일 뿐이다. CPU는 프로그램 카운터(PC)로 현재 실행 위치를 추적하며 메모리를 순차 실행한다.

**ACE 발생 메커니즘**
```
정상:  PC → [코드 영역] → 순차 실행
ACE:   버그 → PC가 [데이터 영역]으로 점프 → 데이터가 명령어로 실행
```
1. 버그·오버플로로 데이터 영역 값이 덮어쓰여진다.
2. 게임이 이를 감지·차단하지 못하면 PC가 데이터 영역 주소로 이동한다.
3. CPU는 그 이진수를 정상 명령어로 착각하고 실행한다.

**컨트롤러 입력 = 데이터 = 코드**
컨트롤러 버튼 입력값도 게임 데이터의 일종이다. ACE 트리거 직후 정교하게 계산된 패드 입력을 연속 주입하면 CPU가 그 값을 새 명령어로 인식·실행한다 — 컨트롤러로 게임을 즉석 프로그래밍하는 것이 가능해진다.

**저수준 언어의 구조적 취약성**
어셈블리·C·C++은 메모리 주소를 직접 접근·조작한다. 경계 검사를 개발자가 직접 책임지므로 버퍼 오버플로 버그가 발생하기 쉽다. 현대 관리형 언어(Java, C#, Python)는 런타임이 경계를 강제해 ACE를 구조적으로 차단한다.

**극단적 활용 — 로봇 컨트롤러 입력**
여러 컨트롤러를 로봇에 연결해 초고속 정밀 입력을 주입 → 메모리 내부에 완전히 새로운 프로그램을 통째로 작성·실행. 성공 조건: 해당 게임의 메모리 맵과 취약점을 1바이트 오차 없이 완벽히 분석.

대표 사례:
- **슈퍼 마리오** 시리즈 — ACE로 핑퐁 게임·Bad Apple!! 영상 구동
- **젤다의 전설: 시간의 오카리나** — ACE로 야생의 숨결 연출 재현
- **글로벌 스피드런 대회** — ACE를 합법적 기술 카테고리로 운영

**방어 설계 (현대 플랫폼)**
- DEP (Data Execution Prevention): 데이터 영역 코드 실행을 하드웨어 수준에서 차단
- ASLR (Address Space Layout Randomization): 메모리 주소 자체를 무작위화해 PC 오염 대상 예측 불가로 만듦
- 관리형 언어 런타임: 배열 경계·포인터를 자동 검사


`#결정론` `#입력`
> 관련: [[game-technique-notes]] #16 의사난수 시드 결정론 (메모리 예측 가능성 같은 맥락), #17 패스워드 세이브 (같은 저수준 메모리 시대의 기법) | 종속성: `#언어독립`

## 19. 가산·곱하기 블렌딩 (Additive / Multiply Blending)

_두 이미지의 색상값을 더하거나(Additive) 곱해(Multiply) 합성하는 렌더링 블렌딩 방식. 빛 이펙트는 어두운 배경 위 Additive로 강조하고, 그림자는 밝은 배경 위 Multiply로 처리._

**설명**
컴퓨터 그래픽에서 색상값 범위는 검정=0, 흰색=1. 두 이미지를 합성하는 방법(블렌딩 모드)에 따라 결과가 전혀 달라진다.

**가산 블렌딩 (Additive)**
```
결과 = 배경색 + 이펙트색
```
- 두 값을 더하면 항상 밝아짐 (0.5 + 0.7 = 1.0 → 흰색에 수렴)
- 배경이 어두울수록 이펙트가 뚜렷, 밝은 배경에서는 이펙트가 묻힘
- 실무 팁: Additive 이펙트 주변에 어두운 코어(내부 어두운 색)를 배치해 대비를 만든다
- 대표 용도: 불꽃, 레이저, 마법 이펙트, 파티클, 빛 발산

**곱하기 블렌딩 (Multiply)**
```
결과 = 배경색 × 이펙트색
```
- 두 값을 곱하면 항상 어두워짐 (0.8 × 0.3 = 0.24)
- 이펙트색이 0(검정)에 가까울수록 배경이 더 어두워짐. 흰색(1.0) 이펙트는 배경에 영향 없음
- 배경이 밝을수록 효과 뚜렷, 어두운 배경에서는 거의 안 보임
- 대표 용도: 그림자, 오염, 혈흔, 얼룩, 야간 환경 필터

**두 방식 비교**
| | Additive | Multiply |
|---|---|---|
| 연산 | 배경 + 이펙트 | 배경 × 이펙트 |
| 결과 방향 | 밝아짐 | 어두워짐 |
| 어두운 배경 | 이펙트 뚜렷 ✓ | 효과 거의 없음 |
| 밝은 배경 | 이펙트 묻힘 | 이펙트 뚜렷 ✓ |
| 주 용도 | 빛, 불꽃, 마법 | 그림자, 오염, 필터 |

**그 외 블렌딩 방식**
- **Alpha (표준 투명도)** — `결과 = 배경 × (1-α) + 이펙트 × α`. 배경에 무관하게 일정한 투명도
- **Screen** — `결과 = 1 - (1-배경) × (1-이펙트)`. Additive보다 부드럽게 밝아짐. 이미 밝은 영역이 날아가지 않음
- **Overlay** — 배경이 0.5 미만이면 Multiply, 이상이면 Screen. 명암 대비 강화

**구현**
```
// Unity ShaderLab 블렌드 설정
Blend SrcAlpha One                    // Additive
Blend DstColor Zero                   // Multiply
Blend SrcAlpha OneMinusSrcAlpha       // Alpha (표준 투명)

// Unity ParticleSystem
// Inspector → Renderer → Material에서 Particles/Additive, Particles/Multiply 셰이더 사용
```

⚠ **주의점**
- **Additive는 어두운 배경 전용** — 밝은 UI 위에 Additive 파티클을 쓰면 이펙트가 거의 안 보임. 배경 밝기를 항상 고려
- **Multiply는 밝은 배경 전용** — 어두운 영역에 Multiply 그림자를 얹으면 효과 없음. 실내 밝은 타일, 밝은 스테이지에서 사용
- **알파 역할이 모드마다 다름** — Alpha 블렌딩에서 알파는 투명도지만, Additive에서 알파는 이펙트 강도(색상에 알파를 곱한 값을 더함). 동일한 텍스처도 모드에 따라 다르게 보임
- **Z-Write 비활성화 필수** — 반투명/블렌딩 오브젝트는 `ZWrite Off`. ZWrite 켜두면 뒤의 오브젝트가 렌더링되지 않는 깊이 버그 발생
- **렌더링 순서** — 블렌딩 오브젝트는 불투명 오브젝트 이후에 렌더링. Unity 렌더 큐 Transparent(3000) 이상으로 설정


`#VFX` `#렌더링` `#게임필`
> 관련: [[game-design-notes]] #6 빌보드 기법 (동일 렌더링 범주), [[unity-feature-notes]] #17 Shader Graph (셰이더 구현) | 종속성: `#엔진독립` (개념), 구현은 `#게임엔진일반`

## 20. 레이캐스팅 (Raycasting)

_오브젝트에서 방향 벡터(선)를 쏘아 충돌 여부·거리·법선을 검사하는 기법. 몬스터 시야 판정, 2D→3D 원근 연출, 지형 탐지 등 다양한 용도의 공통 빌딩블록._

**개념**
레이캐스팅은 "한 지점에서 특정 방향으로 선을 쏘고, 그 선이 어떤 물체에 먼저 닿는지"를 묻는 연산이다. 결과로 충돌 여부, 거리, 교차 지점, 법선(표면 방향)을 얻는다.

대표 활용 3가지:
1. **몬스터 시야 판정** — 몬스터 → 플레이어 방향으로 레이를 쏴 장애물이 없으면 "보인다"고 판정. 장애물이 막으면 시야 차단.
2. **2D 공간을 3D처럼 렌더링** — 카메라에서 좌→우 방향으로 레이를 쏘아 벽까지 거리를 측정. 가까운 벽은 높게, 먼 벽은 낮게 화면에 그린다. 《둠》·《울펜슈타인 3D》의 원리.
3. **지형 탐지 (이동 가능 여부)** — 캐릭터 위로 레이를 쏘아 천장 교차점의 기울기를 측정. 경사가 완만하면 통과 가능, 급격하면 불가 판정. 《젤다의 전설: 왕국의 눈물》의 트레루프(Ascend) 스킬.

**연산 최적화 — 3단계 필터**
게임 내 모든 오브젝트를 대상으로 레이를 쏘면 비용이 선형 증가한다. 실제 시스템은 레이를 쏘기 전에 두 단계를 먼저 거른다:

```
1단계 (거리 필터)  — 시야 범위 내 오브젝트만 추린다
2단계 (시야각 필터) — 1단계 통과 오브젝트 중 시야각 내에 있는 것만 추린다
3단계 (레이캐스팅)  — 2단계 통과 오브젝트에만 실제 레이 발사
```

실제 레이를 쏘는 대상은 전체의 일부에 불과하게 되어 프레임당 연산 비용이 대폭 절감된다.

**구현 (의사코드)**
```
// 시야 판정 예시
function CanSeeTarget(self, target):
    dist = Distance(self, target)
    if dist > sightRange:          // 1단계: 거리
        return false
    angle = Angle(self.forward, target - self)
    if angle > sightAngle / 2:     // 2단계: 시야각
        return false
    hit = Raycast(self.position, direction: target - self)
    return hit.collider == target  // 3단계: 장애물 검사

// 2D → 3D 렌더링 예시 (Doom 방식)
for x in 0..screenWidth:
    rayDir = CalcRayDirection(camera, x)
    hit = Raycast2D(camera.position, rayDir)
    wallHeight = screenHeight / hit.distance   // 가까울수록 높게
    DrawVerticalLine(x, wallHeight)

// 지형 탐지 예시 (트레루프 방식)
function CanAscend(character):
    hit = Raycast(character.position, direction: UP)
    if not hit: return false
    slope = AngleBetween(hit.normal, Vector3.UP)
    return slope < MAX_ASCEND_ANGLE    // 기울기 임계값 비교
```

⚠ **주의점**
- **레이 거리(maxDistance) 설정** — 무한 레이는 씬 전체를 탐색. 항상 거리 상한을 지정해 불필요한 원거리 충돌 제외
- **레이어 마스크 활용** — 몬스터·플레이어·지형은 서로 다른 Physics Layer에 배치하고, 레이 검사 대상 레이어를 한정. "아군끼리 서로 시야 차단" 같은 오작동 방지
- **빈도 최적화** — 매 프레임 레이를 쏘지 않아도 되는 경우가 많음. 0.1~0.2초 간격 업데이트나 FixedUpdate 활용으로 비용 절감
- **시야 시각화** — 여러 개의 레이를 쏘면 시야 영역을 화면에 폴리곤으로 렌더링 가능 (미니맵 시야 표시 등). 단, 레이 수가 늘어날수록 비용 증가 — LOD 필요
- **3단계 필터 순서** — 비용이 낮은 연산(거리 비교 → 벡터 각도 계산)을 먼저, 비용이 높은 레이캐스팅은 마지막에. 순서를 바꾸면 최적화 효과 없음


`#충돌` `#전투` `#카메라` `#3D` `#2D`
> 관련: [[math-algorithm-notes]] (벡터 내적으로 시야각 판정), [[game-technique-notes]] #11 Parallax Scrolling (2D 배경 깊이감 — 다른 방식의 원근 표현) | 종속성: `#엔진독립` (개념), 구현은 `#게임엔진일반`

## 21. 절차적 애니메이션 + 역운동학 (Procedural Animation + IK)

_미리 제작된 고정 애니메이션 대신 게임 엔진이 실시간으로 자세를 계산. 발 목적지를 먼저 정하고 관절 각도를 역산하는 IK로 불규칙 지형에서 자연스러운 보행을 구현._

**절차적 애니메이션 (Procedural Animation)**
고정 클립 재생 방식은 현재 상태에 따라 미리 만들어 둔 애니메이션을 전환한다. 절차적 애니메이션은 그 대신 매 프레임 물리·수학 계산으로 자세를 직접 생성한다. 지형·물리·입력에 즉각 반응하므로 고정 클립이 커버할 수 없는 불규칙 환경에서 생동감이 높다. 대표 사례: 《레인월드(Rain World)》의 몬스터 이동.

**역운동학 (IK, Inverse Kinematics)**
관절 계산에는 두 방향이 있다:
- **순운동학 (FK)** — 루트 관절 → 자식 관절 순으로 각도를 지정 → 말단(발) 위치가 결정된다. 말단을 정확한 위치에 맞추려면 역산이 어렵다.
- **역운동학 (IK)** — 말단(발)의 목적지 위치를 먼저 지정 → 그에 맞게 관절 각도들을 역산. 발이 어디를 밟을지 알고 있을 때 직관적.

IK를 쓰면 계단·경사·장애물에서 발이 정확히 지면을 딛는 자세를 자동 계산할 수 있다.

**2D vs 3D 무릎 위치 계산**

| | 2D | 3D |
|---|---|---|
| 풀어야 할 문제 | 두 링크 길이 + 발 위치 → 무릎 위치 1개 | 두 링크 길이 + 발 위치 → 무릎이 구부러지는 방향이 무한히 존재 |
| 해법 | 컴퍼스 작도(원 교차점) — 기하학적으로 1~2개의 해 | **힌트 축(Pole Target)** 을 추가 지정해 방향을 확정 |
| 특이점 | 발이 너무 멀면 해가 없음 (팔 완전히 뻗음) | 힌트 축 없으면 무릎이 뒤집히거나 떨림 발생 가능 |

3D에서 "무릎이 앞을 향해야 한다" 같은 Pole Target을 하나 추가하면 유일한 해가 결정된다.

**다관절 IK — FABRIK 알고리즘**
곤충·괴물처럼 관절이 3개 이상이면 해석적 역산이 복잡해진다. 반복법(iterative)으로 근사값을 수렴시킨다.

```
// FABRIK (Forward And Backward Reaching IK) 의사코드
joints = [root, ..., end_effector]
target = 발이 디뎌야 할 목표 지점

repeat until converged:
    // ① Backward pass: 말단 → 루트 방향으로 당기기
    joints[last] = target
    for i = last-1 downto 0:
        dir = normalize(joints[i] - joints[i+1])
        joints[i] = joints[i+1] + dir * segmentLength[i]

    // ② Forward pass: 루트 → 말단 방향으로 밀기
    joints[0] = originalRoot   // 루트 위치 고정
    for i = 1 to last:
        dir = normalize(joints[i] - joints[i-1])
        joints[i] = joints[i-1] + dir * segmentLength[i-1]
```

보통 5~10회 반복으로 충분히 수렴한다.

**보행 구현 흐름**
```
1. 발 스텝 결정
   각 발마다 '현재 발 위치'와 '몸통 이동에 따른 목표 위치'를 비교
   거리가 임계값을 초과하면 스텝 트리거

2. 발 이동 (공중 궤적)
   현재 위치 → 목표 위치를 Lerp/bezier 곡선으로 들어올렸다 내림
   착지점은 Raycast로 지면을 탐지해 결정

3. IK 적용
   각 발 위치 확정 후 다리 관절 전체에 IK 계산
   무릎 방향은 Pole Target으로 고정
```

⚠ **주의점**
- **발 동기화** — 4족 보행에서 두 발이 동시에 공중에 뜨면 불안정. 발 스텝 간격에 위상 오프셋(0.5 주기 차이 등)을 줘서 교차 보행 강제
- **몸통 높이 보정** — 발이 높낮이가 다른 지형에 닿으면 몸통도 그에 맞게 높이를 조정해야 기울지 않음. 발 위치 평균으로 몸통 높이 계산
- **특이점(Singularity) 처리** — 목표가 팔다리의 최대 도달 거리 밖이면 IK 해가 없음. 완전히 뻗은 상태로 클램프하거나 목표를 가능 범위로 제한
- **Unity IK 활용** — Unity Animator에 내장된 IK Pass(`OnAnimatorIK`)와 `SetIKPositionWeight`, `SetIKPosition`으로 빠르게 적용 가능. 커스텀 완전 절차적 구현은 그 위에 쌓는다
- **성능** — 관절 수·반복 횟수·발 수가 늘어날수록 비용 증가. 카메라에서 멀수록 반복 횟수를 줄이는 LOD 적용 권장


`#애니메이션` `#이동` `#3D` `#게임필`
> 관련: [[game-technique-notes]] #20 레이캐스팅 (발 착지점 탐지에 Raycast 활용), [[math-algorithm-notes]] (벡터 연산·Lerp·삼각함수가 기반) | 종속성: `#엔진독립` (FABRIK 개념), 구현은 `#게임엔진일반` (Unity IK Pass 등)

## 22. 길찾기 알고리즘 (Pathfinding)

_지형을 그래프로 변환 후 최단 경로를 탐색. 단일 유닛은 A*, 대량 유닛은 플로우 필드(Flow Field)가 표준 선택._

**공통 전제 — 지형의 그래프화**
모든 길찾기의 첫 단계는 지형을 탐색 가능한 그래프로 변환하는 것이다. 구현 방식 3가지:

| 방식 | 설명 | 적합한 게임 |
|---|---|---|
| 타일 그리드 | 맵을 고정 크기 격자로 분할 — 각 셀이 노드 | 2D 전략·RPG |
| 내비메시 (NavMesh) | 이동 가능 표면을 다각형 메시로 표현 | 3D 게임 |
| 웨이포인트 그래프 | 수동 지정 노드를 엣지로 연결 | 복잡한 실내 공간 |

각 노드는 인접 노드로의 **이동 비용(가중치)**을 가진다. 장애물 = 연결 없음. 진흙·물 = 높은 비용.

---

**① 다익스트라 알고리즘 (Dijkstra)**
시작점에서 방사형으로 퍼져 나가며 모든 노드까지의 최단 거리를 확정한다.

```
open = PriorityQueue  // 비용 오름차순
open.push(start, cost=0)
visited = {}

while open not empty:
    current, cost = open.pop()          // 현재까지 비용이 가장 낮은 노드
    if current in visited: continue
    visited[current] = cost

    for neighbor, edgeCost in current.neighbors:
        newCost = cost + edgeCost
        if neighbor not in visited:
            open.push(neighbor, newCost)
```

- **장점**: 목적지가 여러 개이거나 전체 맵 최단 거리가 필요할 때 확실한 최적해 보장
- **단점**: 목적지 방향을 모르므로 사방으로 탐색 → 탐색 노드 수 많음

---

**② A* 알고리즘**
다익스트라에 **휴리스틱(heuristic)** 을 추가해 목적지 방향을 우선 탐색한다.

```
f(n) = g(n) + h(n)

g(n) = 시작점 → n까지 실제 이동 비용
h(n) = n → 목적지까지 추정 비용 (휴리스틱)
```

- **h(n)** 은 장애물을 무시한 직선 거리(유클리드) 또는 맨해튼 거리로 계산
- f 값이 낮은 노드를 우선 탐색 → 목적지 방향으로 집중 → 탐색 노드 수 대폭 감소

```
open = PriorityQueue  // f값 오름차순
open.push(start, f=h(start))

while open not empty:
    current = open.pop()
    if current == goal: return ReconstructPath()

    for neighbor in current.neighbors:
        tentative_g = g[current] + edgeCost(current, neighbor)
        if tentative_g < g[neighbor]:
            g[neighbor] = tentative_g
            f = tentative_g + h(neighbor)
            open.push(neighbor, f)
```

**h(n) 선택 기준**:
| 방식 | 수식 | 적합 상황 |
|---|---|---|
| 맨해튼 거리 | `|dx| + |dy|` | 4방향 격자 이동 |
| 유클리드 거리 | `sqrt(dx²+dy²)` | 자유 방향 이동 |
| 체비쇼프 거리 | `max(|dx|, |dy|)` | 8방향 격자 이동 |

> 《스타크래프트》 사례: 유닛 이동 명령(우클릭) 시 A*로 경로 재계산. 명령을 자주 줄수록 경로가 빈번하게 갱신되어 막힌 구간 없이 이동하는 것처럼 느껴지는 시각적 효과 발생.

---

**③ 플로우 필드 (Flow Field)**
유닛 수백~수천 마리가 동일한 목적지를 향할 때 개별 A* 호출은 비용이 선형 증가한다. 플로우 필드는 **목적지를 고정하고 맵 전체의 방향 벡터를 한 번만 사전 계산**해 둔다.

```
// 사전 계산 (목적지 변경 시 1회 실행)
1. 목적지에서 Dijkstra/BFS로 모든 셀까지 비용 계산
2. 각 셀에서 비용이 낮아지는 방향을 화살표로 저장

// 런타임 (유닛마다 매 프레임)
direction = flowField[unit.currentCell]  // 테이블 조회 1회로 끝
unit.velocity = direction * speed
```

- **장점**: 유닛이 아무리 많아도 런타임 비용은 O(1)/유닛 (테이블 조회만)
- **단점**: 목적지가 바뀌면 전체 맵 재계산 필요. 유닛별 개별 목적지에는 부적합

---

**알고리즘 선택 기준**

| 상황 | 권장 알고리즘 |
|---|---|
| 단일 유닛, 목적지 1개 | A* |
| 목적지가 여러 개이거나 전체 맵 경로 필요 | 다익스트라 |
| 유닛 100+ 이 같은 목적지로 이동 | 플로우 필드 |
| 목적지가 자주 바뀌는 대규모 | 플로우 필드 + 부분 재계산 |

⚠ **주의점**
- **동적 장애물** — A*는 경로 계산 시점의 스냅샷 기반. 장애물이 이동하면 재계산 필요. 재계산 빈도와 비용 균형 필요 (0.2~0.5초 간격 등)
- **경로 스무딩** — 격자 기반 A*는 지그재그 경로가 나옴. 직선 가시성 체크(Line of Sight)로 불필요한 중간 노드를 제거하는 String Pulling 후처리 적용
- **타이 브레이킹** — 동일한 f 값 노드가 여러 개이면 탐색 방향이 제멋대로 퍼짐. h에 미세 가중치를 추가해 목적지 방향을 우선하도록 타이 브레이킹
- **NavMesh와의 조합** — Unity에서는 NavMesh(지형 전처리) + NavMeshAgent(A* 내장)로 대부분 해결. 커스텀 비용·플로우 필드는 그 위에 추가 레이어로 구현
- **플로우 필드 메모리** — 맵이 클수록 방향 벡터 배열 크기 증가. 해상도 조정(플로우 필드 셀을 게임 타일보다 크게) 또는 청크 단위 계산으로 메모리 절감


`#이동` `#전략` `#액션` `#예측가능성`
> 관련: [[game-technique-notes]] #20 레이캐스팅 (장애물 감지에 Raycast 활용 가능), [[math-algorithm-notes]] (우선순위 큐·BFS·그래프 탐색) | 종속성: `#언어독립`

## 23. 픽셀 아트 품질 기법

_낮은 해상도와 제한된 팔레트 안에서 품질을 끌어올리는 4가지 핵심 기법. 선 규칙 두 가지(더블픽셀·재기), 서브픽셀 애니메이션, 컬러 외곽선, 디더링._

**배경**
과거 하드웨어는 해상도와 색상 수가 극도로 제한되어 있었다. 이 제약 안에서 이미지를 깔끔하고 풍부하게 보이도록 만들기 위해 예술가·개발자들이 체계화한 기법들이다. 제약이 사라진 현대에도 의도적인 픽셀 아트 스타일을 만들 때 동일하게 적용된다.

---

**① 선 규칙 — 더블픽셀(Double Pixel) 제거 + 재기(Jaggies) 방지**

**더블픽셀** — 꺾이는 부분에서 픽셀이 두 개 이상 뭉쳐 선이 국부적으로 두꺼워지는 현상. 코너 처리 시 가장 흔하게 발생하며 가장 먼저 제거해야 한다.

```
나쁜 예 (더블픽셀):        좋은 예:
█ █                        █
  █ █                        █
```

**재기(Jaggies)** — 기울기가 불규칙한 선에서 생기는 울퉁불퉁한 계단 현상.

해결 규칙:
- **직선**: 기울기(픽셀 수 비율)를 일정하게 유지. `1:1`, `1:2`, `1:3` 등 한 가지 비율로만 구성.
- **곡선**: 선을 이루는 픽셀 수를 단계적으로 증가 또는 감소시켜 그라데이션처럼 구성.

```
나쁜 직선 (기울기 불규칙):   좋은 직선 (기울기 1:2 고정):
█                            █ █
  █ █                              █ █
      █                                  █ █

나쁜 곡선:    좋은 곡선 (픽셀 수 단계적 변화 1→2→3→2→1):
█ █ █ █      █
█ █            █ █
  █              █ █ █
                   █ █
                     █
```

---

**② 서브픽셀 애니메이션 (Subpixel Animation)**

낮은 해상도에서 오브젝트를 1픽셀 이동시키면 실제 이동 거리가 너무 크게 느껴진다. 1픽셀 미만의 미세한 이동감을 주기 위해 **형태를 옮기지 않고 명암(색)만 조금씩 바꾸는 방법**이다.

```
// 오른쪽으로 0.5픽셀 이동하는 느낌
Before:  [밝 밝 밝]
After:   [중 밝 밝 어]   ← 왼쪽 끝을 어둡게, 오른쪽에 희미한 픽셀 추가
```

눈은 명암 변화를 무게 중심 이동으로 인식한다. 실제 픽셀을 움직이지 않고 색 변화만으로 서브픽셀 단위의 움직임 착시를 만든다.

대표 사례: 《메탈슬러그》 — 극도로 작은 해상도에서도 캐릭터와 기계의 움직임이 매끄럽고 실감 나는 이유.

---

**③ 컬러 외곽선 (Selective Outline)**

외곽선을 획일적인 검은색으로만 처리하지 않는다. 빛이 오는 방향과 인접한 배경 색을 고려해 부위별로 다른 색을 사용한다.

```
적용 원칙:
- 빛이 닿는 면의 외곽선 → 배경보다 밝은 색 or 오브젝트 본체의 밝은 파생색
- 그림자 면의 외곽선   → 짙은 색 or 검정에 가까운 색
- 투명하게 보이게 하려면 → 외곽선을 배경색과 동일하게 (Invisible Outline)
```

효과: 적은 픽셀로도 입체감과 광원 방향이 명확하게 전달된다.

---

**④ 디더링 (Dithering)**

제한된 색상 수 안에서 부드러운 그라데이션 효과를 만드는 기법. 두 색의 픽셀을 일정한 패턴으로 교차 배치하면 눈이 두 색의 평균 색으로 인식한다.

대표 패턴:

```
체커보드 (50:50 혼합):   점진적 전환 (왼쪽 → 오른쪽):
A B A B A               A A A B A B B B
B A B A B               A A B A B B B B
A B A B A               A B A B B B B B
```

디더링 없이 색상을 강제 축소 → 이미지가 경계에서 뚝뚝 끊겨 거칠게 보임.
디더링 적용 → 두 색의 경계가 자연스럽게 블렌딩되어 풍부한 명암 표현.

디더링 패턴 종류:
| 패턴 | 특징 |
|---|---|
| 체커보드 | 50:50 혼합. 가장 균등한 블렌딩 |
| 점진 체커보드 | 비율을 단계적으로 바꿔 그라데이션 생성 |
| 베이어 행렬 | 수학적 행렬 기반 규칙 패턴 (오래된 모니터 최적화) |
| 플로이드-스타인버그 | 오차 확산 방식 — 더 자연스럽지만 픽셀 아트에서는 드물게 사용 |

⚠ **주의점**
- **디더링 과다 사용** — 모든 색 전환에 디더링을 쓰면 화면 전체가 노이즈처럼 보임. 그라데이션이 필요한 그림자·하이라이트 경계에만 선택적으로 사용
- **더블픽셀 자동화** — 도구(Aseprite 등)가 자동으로 잡아주지 않으면 완성 후 전체 선을 다시 점검하는 습관 필요. 특히 애니메이션 프레임 간 전환 시 코너 처리에서 자주 발생
- **서브픽셀과 해상도 업스케일** — 업스케일(2x, 4x) 적용 시 서브픽셀 트릭이 의도와 다르게 보일 수 있음. 업스케일 알고리즘(EPX, hq2x 등)이 명암 변화를 이동으로 처리하지 않을 수 있음
- **팔레트 수 제약과 컬러 외곽선** — 외곽선 전용 색을 추가하면 팔레트 슬롯 소모. 오브젝트 본체의 어두운 파생색을 외곽선에 재활용하는 방식으로 팔레트 절약
- **현대 픽셀 아트 vs 레트로 제약** — 현대 도구는 색상 수 제한이 없으므로 위 규칙을 일부 완화할 수 있다. 그러나 의도적 레트로 스타일이라면 원본 하드웨어의 팔레트·해상도 제약을 참고해 적용 범위를 결정


`#VFX` `#애니메이션` `#UI` `#게임필`
> 관련: [[game-technique-notes]] #19 가산·곱하기 블렌딩 (색상 합성 — 렌더링 범주 공통), [[game-design-notes]] (픽셀 아트 스타일 선택의 디자인 의도) | 종속성: `#언어독립` (도구는 Aseprite·Photoshop 등 독립)
