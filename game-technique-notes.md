# 게임 기법 노트

> 다루는 축: 게임 *기능*별 구현 기법. "어떻게 묵직한 점프를 만드는가?" 같은 질문에 답
> 다루지 않는 축: 왜 그렇게 느껴지는가(→ [[game-design-notes]]), 일반 코드 구조(→ [[design-pattern-notes]])
> 적용 범위: 개념은 엔진 독립, 구현은 대부분 게임엔진 일반에 종속
> 관련 노트: [[game-design-notes]] (원리), [[math-algorithm-notes]] (빌딩블록)
> 평생 노트 정책: 인덱스 표는 portable, 풀노트는 구현 의사코드 + 파라미터 권장값 포함
> 승격 임계치: 항목 9개 이상 시 카테고리(이동/전투/오디오) 단위 분리 검토
> 풀노트 작성 기준 (둘 이상 해당 시):
>   - 코드만 봐선 "왜 이렇게 했는지" 안 보이는 정성적 이유가 있다
>   - 다른 프로젝트/맥락에서도 재사용 가능한 일반 원리다
>   - 자주 잊는 함정/엣지케이스가 있다
>   - 응용 사례가 3개 이상이다
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

## 인덱스

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

## 1. 비대칭 점프 (Asymmetric Jump)

**한 줄 요약**
상승과 하강에 서로 다른 중력을 적용해 떨어질 때 더 빠르게 낙하시키는 점프 곡선. 묵직한 무게감 + 빠른 응답성.

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

**주의점**
- 물리 엔진과 충돌 가능 — `velocity` 직접 조작 대신 `Rigidbody.gravityScale` 동적 변경이 더 안전 (Unity)
- `fallMultiplier`가 너무 크면 공중 제어 시간이 짧아져 플랫폼 안착 어려움 — 레벨 디자인과 함께 튜닝
- Coyote/Buffer 타이머를 디버그 UI로 노출하면 튜닝 속도 ↑

**메타**
- 종속성: `#게임엔진일반` (개념 독립, 구현은 물리/시간 시스템 필요)
- 관련 노트: [[game-design-notes]] #1 (관용성 디자인 원리)
- 첫 도출: CasualStrategy (2026-05-15)
- 태그: `#점프` `#2D` `#플랫포머` `#게임필` `#응답성`

---

## 항목별 노트 (#2~#9)
*풀노트는 요청 시 작성. 위 인덱스 표가 SOT.*

---

## 10. Hold-to-Repeat 버튼 (길게 누르기 반복 입력)

**한 줄 요약**
버튼을 누르고 있으면 초기 딜레이 후 일정 간격으로 클릭 이벤트가 반복 발동되는 입력 패턴.

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

**주의점**
- **PointerExit 처리 필수** — 누른 채로 버튼 밖으로 드래그하면 OnPointerUp이 발동 안 됨. 드래그 이탈 시점에 명시적으로 정지
- **OnDisable 안전망** — 패널 닫힘/씬 전환 시 코루틴이 살아있으면 NRE 가능
- **Realtime vs scaled** — 일시정지 메뉴에서도 동작해야 하면 `WaitForSecondsRealtime` 사용. 게임 속도에 종속이면 `WaitForSeconds`
- **터치 vs 마우스** — 모바일에서 손가락이 살짝 움직이면 OnPointerExit 발동 가능. 허용 임계값 두거나 `EventSystem.pixelDragThreshold` 조정
- **interactable=false 동안 발동 방지** — 매 루프에서 검사. 도중에 버튼이 비활성화되면 즉시 정지

**메타**
- 종속성: `#게임엔진일반` (PointerEvent 인터페이스가 있는 UI 시스템 필요)
- 첫 도출: CasualStrategy (2026-05-15)
- 태그: `#입력` `#UI` `#응답성` `#관용성` `#코루틴`

---
