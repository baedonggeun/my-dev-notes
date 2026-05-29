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
> 관련: [[game-design-notes]] #1 (관용성 디자인 원리) | 종속성: `#게임엔진일반` (개념 독립, 구현은 물리/시간 시스템 필요)

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