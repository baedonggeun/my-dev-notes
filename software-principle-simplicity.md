# 소프트웨어 원칙 — 단순성

> 상위 노트: [[software-principle-notes]] (전체 인덱스 디스패처)
> 다루는 축: YAGNI·KISS·DRY·AHA·보이 스카우트 등
> 다루지 않는 축: [[software-principle-design|소프트웨어 원칙 — 설계]] / [[software-principle-quality-laws|소프트웨어 원칙 — 코드품질·법칙]]

---


## 태그 목록

### 분류
- `#설계` `#구현` `#리팩토링` `#팀워크` `#성능` `#테스팅` `#타입` `#관찰`

### 적용 레벨
- `#코드` `#모듈` `#아키텍처` `#프로세스` `#조직`

### 종속성
- `#언어독립` `#엔진독립` `#OOP` `#FP` `#타입시스템`


---


# 인덱스

### A. 코드 양/추상화 (`#설계`)

| # | 원칙 | 한 줄 정의 | 본인 적용 |
|---|------|----------|----------|
| 1 | **YAGNI** (You Ain't Gonna Need It) | 추측 기반 기능/추상화 도입 금지 | 추상화 비용 > 회피 비용일 때만 도입 — CasualStrategy 4원칙 항목 2 Simplicity First로 명문화, plan 작성 시 가정 표면화로 강제 (→ 풀노트) |
| 2 | **KISS** (Keep It Simple, Stupid) | 가장 단순한 해법 우선 | 짧은 코드 + 명확한 이름이 회상/디버깅 비용 절감 — Manager Singleton, 단일 코루틴 호스트, FSM 직접 구현(엔진 패키지 회피) 같은 구조 선택의 근거 |
| 3 | **DRY** (Don't Repeat Yourself) | 지식의 중복 회피 | 추상화 임계는 *지식 중복*이지 *코드 행 중복*이 아님 — 첫 2번 비슷한 코드 본 직후 공통 base 추출 충동에서 오용 발생, 잘못된 일반화로 누적 (→ 풀노트) |
| 4 | **Rule of Three** | 같은 코드 3번 반복 시 추상화 | DRY의 트리거 임계치, 2번까지 묵인 — design-pattern-notes 항목 5 Service 분리 임계와 동일 원리. 적용: 새 패턴 발견 시 plan에서 "3번째 사례 확보 전 추상화 보류" 명문화 |
| 5 | **Premature Optimization is the Root of All Evil** (Knuth) | 측정 없는 성능 최적화 금지 | 일반 코드는 적용 / 매 프레임 핫패스(Update, 코루틴, Dice 굴림 루프, spawn)는 예외 — Unity 게임은 핫패스 사전 인지가 비용 0이므로 측정 전 NonAlloc/풀링 적용 |
| 6 | **Boy Scout Rule** | 캠프 떠날 때 더 깨끗하게 | 채택 안 함 — Surgical Changes(4원칙 항목 3) 위배. 대안: cleanup 필요 시 별 묶음 plan으로 분리, 같은 commit에 끼우지 않음 (→ 풀노트) |
| 7 | **AHA** (Avoid Hasty Abstractions, Kent C. Dodds) | 중복보다 잘못된 추상화가 더 비쌈 — Rule of Three 강화판 | F-4 단일 행 정의로 32건 오판을 만든 사례가 직접 증거 — 코드 중복은 fixable, 잘못된 base 추출은 마이그레이션 폭발. idea-notes 항목 14 sub-pattern 분기 보정의 상위 원칙 (→ 풀노트) |
| 8 | **WET** (Write Everything Twice) | DRY 반대 표어 — 3번째에야 추출 | Rule of Three(항목 4)의 보조 표어 — 적용은 항목 4와 동일. 회상 시점에 "어, WET이라는 말도 있었지" 단서로 등재 |

---

# 풀노트

## 1. YAGNI (You Ain't Gonna Need It)

_추측 기반 기능/추상화 도입 금지. 현재 명시적으로 필요한 것만 구현._

**왜 본인이 이렇게 다루는가**
CasualStrategy 4원칙 항목 2 Simplicity First로 명문화된 *프로젝트 강제*. plan 작성 시점에 가정을 표면화하면 "이 추상화는 현재 요구사항이 아니라 *내가 미래에 필요할 거라 추측한 것*"이 드러남. AI(Claude) 협업에서 특히 중요 — AI는 *완전성 편향*으로 abstract base, 인터페이스, 매개변수를 선제적으로 추가하는 경향이 있음. 사용자가 plan에서 "현재 사례 1건"이라 명시하면 AI가 over-engineering 회피.

**적용 사례**
- CasualStrategy 4원칙 항목 2 Simplicity First — 모든 plan의 가정 표면화 단계가 YAGNI 강제 메커니즘
- F-1~F-N 시너지 효과를 추가할 때 abstract `SynergyEffectBase` 미신설 — 각 효과는 ScriptableObject + `SynergyEffectType` enum + switch dispatch로 충분. 두 번째 시너지 효과를 본 시점에서 base 추출 충동이 컸으나, *세 번째 효과의 형태를 모르므로* 보류
- /commit-msg의 "묶음 토글"이 단일 plan 1건 stateless 추론으로 단순 — 다중 plan 매핑 시스템(ADR-047 회귀 대상)을 안 만든 결정의 근거

**오용 / 반대 원칙**
- 반대 원칙: **Speculative Generality**(항목 36) — YAGNI의 코드 스멜 짝. 검출 신호: 호출처 1곳뿐인 인터페이스, 단일 자식만 가진 abstract base, 사용 안 되는 매개변수
- 오용 가능 지점: "현재 X 1건이지만 *근시일 내* Y 2건 추가 예정"인 경우 → YAGNI 엄격 적용 시 마이그레이션 비용 폭발. 해결: plan에서 *근시일 내 예정 사례*를 명시적으로 노출 후 추상화 시점 판단


#설계 #코드 #아키텍처
> 종속성: `#언어독립` `#엔진독립`

---

## 3. DRY (Don't Repeat Yourself)

_지식의 중복 회피. *코드 행*의 중복이 아닌 *의사결정·도메인 지식*의 중복만 추출 대상._

**왜 본인이 이렇게 다루는가**
DRY의 통상 해석은 "같은 코드 보이면 추출"이지만 — 비슷해 *보이는* 두 코드가 *다른 변경 이유*를 가질 수 있음. 두 번째 만남에서 추출하면 세 번째 사례가 *다른 형태*로 나타날 때 base가 폭발 (idea-notes 항목 14 F-4 32건 오판이 직접 증거). DRY 본문은 "지식의 중복"이라 명시했는데도 코드 행 단위로 오용되는 현상이 잦음.

**적용 사례 (적용 + 비적용 분리)**
- **적용**: SO 데이터 매핑 빌드 로직(idea-notes 항목 19) — itemId 추출 + Dictionary 빌드는 *동일한 지식*이라 헬퍼 추출
- **적용**: Manager Singleton MonoSingleton<T> CRTP base — 인스턴스 보존 라이프사이클은 *동일한 지식*
- **비적용**: HealthService와 ManaService의 비슷한 구조 — *변경 이유가 다름*(체력 규칙 vs 마나 규칙). base 추출 보류, 3번째 자원 타입 출현 시 재검토
- **비적용**: View와 Sequence의 비슷한 초기화 패턴 — *책임이 다름*(데이터 holder vs 연출). base 추출 시 SRP(항목 9) 위반

**오용 / 반대 원칙**
- 반대 원칙: **AHA**(항목 7) — "잘못된 추상화가 중복보다 비싸다"는 DRY 과적용 방지 표어
- 짝 원칙: **Rule of Three**(항목 4), **WET**(항목 8) — 추출 임계치는 3번째 만남
- 오용 가능 지점: AI 협업 시 특히 위험 — AI는 *시각적 유사성*에 반응해 base 추출을 제안. 사용자가 "변경 이유가 같은가?" 1줄 검증 필요


#설계 #코드 #리팩토링
> 종속성: `#언어독립` `#엔진독립`

---

## 5. Premature Optimization (Knuth)

_"조기 최적화는 모든 악의 근원" — Knuth. 단, *게임의 핫패스*에서는 측정 전 사전 인지 비용이 0이므로 예방 적용이 허용._

**왜 본인이 이렇게 다루는가**
Knuth의 원문은 "premature optimization is the root of all evil — in about 97% of the time". 나머지 3%는 *critical sections* — 게임에서는 `Update`, `FixedUpdate`, spawn 루프, 코루틴 yield 루프가 여기 해당. 이 구분을 무시하고 "모든 최적화는 측정 후"로 해석하면 핫패스에서 GC alloc이 누적되다가 나중에 대규모 리팩토링이 필요해짐.

기준:
- **일반 코드**: 측정 없는 최적화 금지. LINQ, 박싱, 람다, string + 자유롭게 쓰고 성능 문제가 실측될 때 교체
- **핫패스 (Update, yield 루프, 매 프레임 이벤트)**: 사전 인지 비용이 0이므로 처음부터 `NonAlloc`, `List` 재사용, 배열 사전 할당, 풀링 적용. 리팩토링 비용 > 처음부터 올바르게 하는 비용

**적용 사례**
- **적용 (일반)**: SO 빌드 코드, Service 로직, UI 바인딩 — 명확성 우선. LINQ 사용, 빌드 시점 1회라 허용
- **사전 최적화 허용 (핫패스)**: `Physics2D.RaycastNonAlloc` — Update에서 매 프레임 호출되는 경우 NonAlloc 버전을 처음부터 사용. "매 프레임 GC alloc = 나쁨"이 사전 인지 가능
- **사전 최적화 허용 (풀링)**: `PopupSpawner` 풀 패턴 — Instantiate/Destroy가 Spawn loop에서 반복됨이 자명. 측정 전 풀 적용
- **사전 최적화 허용 (배열)**: `game-misc 항목 12 Array.Empty<T>()` — 빈 배열을 함수 반환마다 `new T[0]`으로 할당하는 것이 자명한 낭비 → 정적 공유 배열

**오용 / 반대 원칙**
- 오용: "나중에 병목이 될 것 같아" → abstract cache layer, 사전 메모이제이션. 실측 없이 추가하는 복잡성 = 전형적 조기 최적화
- 오용: 알고리즘 선택을 "나중에 최적화"로 미루는 것 → O(N²)을 O(N log N)으로 바꾸는 것은 *측정 전 판단 가능*한 영역
- 짝 원칙: **YAGNI**(항목 1) — 성능 기능도 YAGNI 대상
- 반대 원칙: **Make It Work, Make It Right, Make It Fast**(항목 26) — "Make It Fast"는 마지막 단계
- 검출: Unity Profiler / Memory Profiler 실측 근거. `GC.Collect` 빈도와 프레임 타임 spike가 핵심 지표


#성능 #구현 #코드
> 종속성: `#언어독립` `#성능`

---

## 6. Boy Scout Rule (채택 안 함)

_"캠프 떠날 때 더 깨끗하게" — 코드 수정 시 주변 cleanup 동반. **본인은 채택 안 함**._

**왜 본인이 이렇게 다루는가**
CasualStrategy 4원칙 항목 3 Surgical Changes("요청 라인만 수정, 주변 cleanup 금지")와 정면 충돌. Boy Scout Rule이 작동하려면 (a) cleanup 비용 < 회피 비용, (b) cleanup 후 회귀 위험 < 잠재 이득이 성립해야 하는데 — AI 협업 환경에서는 두 가정 모두 깨짐:
- (a) AI는 *주변 코드 정리*를 무한히 발견하므로 cleanup 비용이 폭주
- (b) Surgical 외 변경이 리뷰 시 *원래 요청과 cleanup의 경계*를 흐려 회귀 검토 곤란

**적용 사례 (대안)**
- 대안 1: cleanup 필요 인지 시 **별 묶음 plan으로 분리** (`docs/plan-{cleanup-topic}.md`). 같은 commit에 끼우지 않음
- 대안 2: cleanup이 *trivial*이면 (오타·포맷·주석) `/check-done clean` 메뉴에서 묶음 처리 — 단, 의미 변경은 금지
- 대안 3: cleanup이 *떨어진 코드*면 followup 짝(`plan-{topic}-followup.md`)에 누적 후 별 plan으로 분리
- 사례: ShopController 5분리(idea-notes 항목 16) 시 "코디네이터는 코디네이터 책임만, sub-Controller 내부 cleanup은 별 plan"으로 분리. 단일 commit이 700행 변경되는 빅뱅 회피

**오용 / 반대 원칙**
- 정합 원칙: **Surgical Changes**(CasualStrategy 4원칙 항목 3), **Chesterton's Fence**(항목 35) — 둘 다 *주변에 손대지 마라* 계열
- 짝 원칙: **Rule of Three**(항목 4) — cleanup도 3번째 만남에 plan화하는 게 본인 룰
- 본 원칙이 채택될 환경: 다수 개발자 + CI 강제 + 작은 commit 룰이 합의된 환경. 1인 개발 + AI 협업에서는 *경계 흐림*이 더 큰 비용


#설계 #프로세스 #팀워크
> 종속성: `#언어독립` `#엔진독립`

---

## 7. AHA (Avoid Hasty Abstractions)

_"잘못된 추상화는 중복보다 비싸다" — Kent C. Dodds. Rule of Three의 강화판._

**왜 본인이 이렇게 다루는가**
DRY(항목 3)의 통상 적용이 "2번째 만남에 base 추출"인데, *2번째 만남에서 발견한 공통점이 우연*인 경우가 많음. 3번째가 다른 형태로 나타나면 잘못된 base를 깨고 재추출하는 비용 > 처음부터 중복 유지하는 비용. AI 협업에서 특히 빈번 — AI는 시각적 유사성으로 base를 제안하지만 도메인 지식이 부족해 *우연한 유사성*을 잡아냄.

**적용 사례**
- idea-notes 항목 14 sub-pattern 분기 보정 — F-4 단일 행 정의가 32건 오판을 만든 사례가 직접 증거. 단일 정의가 *실제 코드의 회색지대*를 흡수 못 함 → sub-pattern 분기로 정의 정확도 회복
- SynergyEffect와 AttributeEffect의 비슷한 Apply 패턴 — 1차 base `EffectBase` 도입 시도했으나 시너지는 *카운터 트리거*이고 속성은 *조건 트리거*라 base가 빈 껍데기로 전락. base 폐기 후 각자 ScriptableObject 별도
- ItemDataSO와 UsableItemDataSO — abstract base 만들지 않고 *2 베이스 + 매핑 시점 통합 Dictionary*로 처리(idea-notes 항목 19)

**오용 / 반대 원칙**
- 짝 원칙: **Rule of Three**(항목 4), **WET**(항목 8) — 추출 임계치
- 반대 원칙: **DRY**(항목 3) — DRY 과적용 방지가 AHA의 본질
- 검출 신호: base를 만든 후 *자식이 base 메서드를 거의 안 쓰거나*, *base에 자식별 분기 if/else가 생기는* 경우 → 잘못된 추상화 신호


#설계 #코드 #리팩토링
> 종속성: `#언어독립` `#엔진독립`