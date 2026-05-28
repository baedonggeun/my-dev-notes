# 소프트웨어 원칙 노트

> 다루는 축: 일반 소프트웨어 개발 원칙·휴리스틱·해석. 코드 *형태*가 아닌 *판단 기준*의 추상화
> 다루지 않는 축: 구체 패턴 구현(→ [[design-pattern-notes]]), 게임 특화 기법(→ [[game-technique-notes]]), 단편 트릭(→ [[game-misc-notes]])
> 적용 범위: 언어/엔진/도메인 완전 독립 — 원칙은 메타 레벨
> 관련 노트: [[design-pattern-notes]] (원칙의 구체 적용), [[idea-notes]] (검증 전 원칙 후보 + 본인 적용 미정 원칙 인박스)
> 평생 노트 정책: 인덱스 표는 *왜 + 어디 적용 / 대안 / 오용 지점* 1줄, 풀노트는 본인 해석·사례 중심
> 승격 임계치: 풀노트 항목이 카테고리당 8개 이상 시 분리 검토 (design-pattern-notes와 동일)
> 풀노트 작성 기준: 인덱스 1줄만으로 적용/판단이 불충분한 항목. 자명한 항목만 인덱스로 종료
> 본인 입장 표기 룰: `#수용` `#기각` 같은 라벨 금지. 본인 적용 셀에 *왜 + 어디 적용* (조건부면 *수용/비수용 경계*, 기각이면 *대안*, 오용주의면 *오용 지점*) 실질 1줄
> 작성 시작: 2026-05-21

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
| 1 | **YAGNI** (You Ain't Gonna Need It) | 추측 기반 기능/추상화 도입 금지 | 추상화 비용 > 회피 비용일 때만 도입 — CasualStrategy 4원칙 #2 Simplicity First로 명문화, plan 작성 시 가정 표면화로 강제 (→ 풀노트) |
| 2 | **KISS** (Keep It Simple, Stupid) | 가장 단순한 해법 우선 | 짧은 코드 + 명확한 이름이 회상/디버깅 비용 절감 — Manager Singleton, 단일 코루틴 호스트, FSM 직접 구현(엔진 패키지 회피) 같은 구조 선택의 근거 |
| 3 | **DRY** (Don't Repeat Yourself) | 지식의 중복 회피 | 추상화 임계는 *지식 중복*이지 *코드 행 중복*이 아님 — 첫 2번 비슷한 코드 본 직후 공통 base 추출 충동에서 오용 발생, 잘못된 일반화로 누적 (→ 풀노트) |
| 4 | **Rule of Three** | 같은 코드 3번 반복 시 추상화 | DRY의 트리거 임계치, 2번까지 묵인 — design-pattern-notes #5 Service 분리 임계와 동일 원리. 적용: 새 패턴 발견 시 plan에서 "3번째 사례 확보 전 추상화 보류" 명문화 |
| 5 | **Premature Optimization is the Root of All Evil** (Knuth) | 측정 없는 성능 최적화 금지 | 일반 코드는 적용 / 매 프레임 핫패스(Update, 코루틴, Dice 굴림 루프, spawn)는 예외 — Unity 게임은 핫패스 사전 인지가 비용 0이므로 측정 전 NonAlloc/풀링 적용 |
| 6 | **Boy Scout Rule** | 캠프 떠날 때 더 깨끗하게 | 채택 안 함 — Surgical Changes(4원칙 #3) 위배. 대안: cleanup 필요 시 별 묶음 plan으로 분리, 같은 commit에 끼우지 않음 (→ 풀노트) |
| 7 | **AHA** (Avoid Hasty Abstractions, Kent C. Dodds) | 중복보다 잘못된 추상화가 더 비쌈 — Rule of Three 강화판 | F-4 단일 행 정의로 32건 오판을 만든 사례가 직접 증거 — 코드 중복은 fixable, 잘못된 base 추출은 마이그레이션 폭발. idea-notes #14 sub-pattern 분기 보정의 상위 원칙 (→ 풀노트) |
| 8 | **WET** (Write Everything Twice) | DRY 반대 표어 — 3번째에야 추출 | Rule of Three(#4)의 보조 표어 — 적용은 #4와 동일. 회상 시점에 "어, WET이라는 말도 있었지" 단서로 등재 |

### B. SOLID/책임 분배 (`#설계` `#OOP`)

| # | 원칙 | 한 줄 정의 | 본인 적용 |
|---|------|----------|----------|
| 9 | **SRP** (Single Responsibility) | 한 클래스는 한 변경 이유만 | 책임 ≠ "기능 1개"가 아니라 "변경 이유 1개" — UI 4축(View/Binder/Controller/Sequence)과 인프라 11종 접미사 분류의 상위 원칙. 적용: ShopController 5분리(idea-notes #16) (→ 풀노트) |
| 10 | **OCP** (Open/Closed) | 확장에는 열려, 수정에는 닫혀 | 새 SO/Strategy 등록만으로 코어 무수정이면 적용(시너지/속성 효과 SO, AnimationConfigSO 매핑) / Manager 내부 분기 추가는 직접 수정 허용 — 인터페이스 폭증을 만들면서까지 강요 X |
| 11 | **LSP** (Liskov Substitution) | 자식이 부모를 의미 손상 없이 대체 | 의미 손상 발견 즉시 *상속 → 컴포지션 또는 별 베이스 분리* — ItemDataSO/UsableItemDataSO 베이스 분리(idea-notes #19)가 본 원칙 위반 회피 사례 |
| 12 | **ISP** (Interface Segregation) | 클라이언트가 안 쓰는 메서드에 의존 X | 도메인 인터페이스는 5+ 메서드 시 분리(Effect 3종 Apply/Emit/Describe) / Unity MonoBehaviour의 생명주기 강제는 엔진 제약이므로 위반 묵인 |
| 13 | **DIP** (Dependency Inversion) | 추상에 의존, 구체에 의존 X | ctor 주입이 정합 / Manager+Service 부모 역참조는 회색지대로 허용(idea-notes #15), 외부 Manager 호출은 위반(정리 대상) — Service 7개 컴포지션에 적용 |
| 14 | **GRASP – Information Expert** | 책임은 정보를 가진 객체에 부여 | Effect 객체가 자체 Apply/Emit/Describe — 외부에서 상태 읽고 결정하지 않음. Tell-Don't-Ask(#21)의 책임 분배 측면 |
| 15 | **GRASP – Pure Fabrication** | 적합한 도메인 클래스가 없으면 신설 | Service/Director/Filter 등 인프라 11종 접미사가 본 원칙의 적용 — 도메인에 없는 책임은 가공 클래스로 |
| 16 | **GRASP – Indirection** | 결합도 ↓ 위해 중간 객체 도입 | FlowDirector가 Manager 간 라우팅 — Battle/Item Manager 직접 호출 금지의 동력 |
| 17 | **GRASP – Protected Variations** | 변동 지점을 인터페이스/추상 뒤에 격리 | OCP(#10)의 동력 — 시너지/속성 효과 SO 분리는 본 원칙이 OCP보다 정확한 표현 (어디를 격리할지 = 변동 지점 식별) |

### C. 결합도/응집도 (`#설계`)

| # | 원칙 | 한 줄 정의 | 본인 적용 |
|---|------|----------|----------|
| 18 | **High Cohesion, Low Coupling** | 모듈 내부 결속 ↑ 외부 결합 ↓ | namespace 단위 응집 + Manager 간 이벤트 의존만 허용 — Battle/Item/UI namespace 분리, FlowDirector 라우팅 |
| 19 | **Law of Demeter** (`a.b.c.d()` 금지) | 직접 협력자만 호출 | 비즈니스 로직 간 chained는 위반(정리) / View가 Binder→Controller 데이터 조회 시 chained는 자연(거부 시 Binder 위임 메서드 폭증) — UI 4축에서 오용 가능성 발생 |
| 20 | **Composition Over Inheritance** | 상속보다 컴포지션 | Unity 컴포넌트 모델 자체가 본 원칙의 강제 — Manager+Service 컴포지션, sub-Controller 동거 분리(idea-notes #16) |
| 21 | **Tell, Don't Ask** | 상태를 묻고 결정 X, 위임 | 도메인 객체에 동작 위임(Effect 객체가 자체 Apply/Emit/Describe) / View는 dumb holder 원칙으로 *물어보는 쪽* 허용 — UI 4축에서 비적용 영역 명시 |
| 22 | **Separation of Concerns** | 책임이 다른 코드는 다른 모듈로 | SRP의 모듈 단위 적용 — UI 4축 분리, 인프라 11종 접미사 분류, 데이터↔연출 분리(idea-notes #3)의 근거 |
| 23 | **Stable Dependencies Principle** | 안정한 모듈에 의존, 불안정한 모듈은 의존받지 않음 | Core(Manager Singleton) ← Battle/Item/UI 단방향 의존 — Core는 안정, 도메인 namespace는 불안정. 역의존 발견 시 즉시 인터페이스/이벤트로 역전 |
| 24 | **Acyclic Dependencies Principle** | 모듈 의존 그래프에 순환 없음 | namespace 계층 + Manager 간 이벤트 의존만 허용의 근거 — 동기 호출 순환은 차단, 비동기 이벤트는 허용 (런타임 순환은 매니저 상태로 끊김) |

### D. 구현 휴리스틱 (`#구현`)

| # | 원칙 | 한 줄 정의 | 본인 적용 |
|---|------|----------|----------|
| 25 | **Fail Fast** | 에러는 조용히 삼키지 말고 즉시 노출 | Debug.LogWarning + null 가드 또는 throw — SO 매핑 빌드 시점 IsNullOrEmpty 가드(idea-notes #19), Service 컴포지션 누락 시 ctor throw |
| 26 | **Make It Work, Make It Right, Make It Fast** (Kent Beck) | 단계적 개선 순서 | plan → 1차 구현 → /check-done → 리팩토링 묶음의 단계와 동치 — 모든 T3/T4 plan 진행 순서 |
| 27 | **POLA** (Principle of Least Astonishment) | 호출자가 놀라지 않게 | 메서드 이름 = 부수효과까지 표현(BeginQueueBatch/EndQueueBatch batch 패턴, idea-notes #13). 어디서 오용 가능: 짧은 이름을 위해 부수효과 숨기면 race/double-fire 함정 |
| 28 | **Convention over Configuration** | 합리적 기본값 + override만 노출 | SerializeField 기본값 + 인스펙터 override — Manager Singleton의 SO 자동 로드, Builder 1회 셋업 + YAML override |
| 29 | **CQS** (Command-Query Separation, Bertrand Meyer) | 메서드는 명령(상태 변경) 또는 쿼리(상태 조회), 둘 다 X | Service.GetX() vs Service.ApplyX() 분리 패턴 / 비적용: batch 패턴(BeginX/EndX, idea-notes #13)에서 EndX는 명령+이벤트 발화 동반(의도된 부분 위반) |
| 30 | **Design by Contract** (Bertrand Meyer) | preconditions/postconditions/invariants 명시 | Service 컴포지션 누락 시 ctor throw — precondition 위반은 즉시 실패(Fail Fast #25와 짝). 비적용: postcondition assert는 게임 도메인에 과한 비용 |
| 31 | **Hollywood Principle** (IoC) | "Don't call us, we'll call you" — 프레임워크가 호출, 사용자 코드는 등록만 | Unity 자체가 본 원칙의 강제 — Awake/Update/OnDestroy 라이프사이클 콜백. 도메인 코드에서는 Manager 이벤트 구독이 동일 패턴 |
| 32 | **SLAP** (Single Level of Abstraction Principle) | 한 메서드 내 모든 호출이 같은 추상화 레벨 | Controller 코디네이터화(idea-notes #16)의 근거 — 700행 Controller가 데이터/UI/버튼 풀스택 혼재했던 이유는 SLAP 위반. 같은 GameObject sub-Controller 분리로 코디네이터는 한 레벨만 (→ 풀노트) |
| 33 | **Defensive Programming** | 호출자 신뢰 X, 입력 검증 적극 | 채택 안 함 — Service 내부는 호출자 신뢰(public 시그니처에서만 가드). 대안: DIP(#13)로 타입 강제 + Fail Fast(#25)로 보일러플레이트 회피. 모든 메서드 입력 검증은 비대 |

### E. 메타·트레이드오프 (`#팀워크`)

| # | 원칙 | 한 줄 정의 | 본인 적용 |
|---|------|----------|----------|
| 34 | **Worse is Better** (Richard Gabriel) | 완벽한 설계보다 동작하는 단순함 | skill/agent 카탈로그·하네스 hook은 단순함 우선 / decisions/ ADR은 정확성 우선 — 영역별 트레이드오프 분리 적용 |
| 35 | **Chesterton's Fence** | 이유 모르는 코드는 함부로 제거 X | Surgical Changes(4원칙 #3) 정합 — 모르는 코드는 git blame + commit 메시지 확인 후 제거. /check-done clean의 PENDING 스캔 룰의 근거 |
| 36 | **Speculative Generality** (Code Smell) | 미래 가정 기반 추상화 = YAGNI 위반 | YAGNI(#1)의 코드 스멜 짝 — plan 작성 중 "나중에 X도 필요할 수 있으니" 충동, 단일 자식만 가진 abstract base 신설 충동에서 오용 발생. 검출: 호출처 1곳뿐인 인터페이스 |
| 37 | **Big Ball of Mud** (Foote & Yoder) | 구조 없는 아키텍처의 자연 상태 | 자연 상태로 회귀하지 않게 *주기적 정합 감사* 필요 — /check-done arch/adr 메뉴, docs-check.sh 정합 검증의 동기 |

### F. 타입/도메인 모델링 (`#설계` `#타입`)

| # | 원칙 | 한 줄 정의 | 본인 적용 |
|---|------|----------|----------|
| 38 | **Make Illegal States Unrepresentable** (Yaron Minsky) | 잘못된 상태를 컴파일 단계에서 표현 불가능하게 | SynergyEffectType enum + 멤버별 정수값 영구 점유 룰(idea-notes #18) — "삭제된 효과 정수 재사용 금지"가 silent corruption 차단. SerializeReference 자식 인스턴스 deep clone(idea-notes #8)도 같은 동기 (→ 풀노트) |
| 39 | **Parse, Don't Validate** (Alexis King) | 검증 대신 파싱 — 검증 결과를 타입에 인코딩 | idea-notes #19 string ID → SO 직접 참조 전환이 부분 적용 — 인스펙터 wiring 시점에 *유효한 SO만 받을 수 있는 타입*으로 강제. 비적용: 런타임 캐시는 string Dictionary 유지(호출자 무변경 트릭) |
| 40 | **Pure Functions** | 같은 입력 = 같은 출력, 부수효과 없음 | Dice 굴림 계산, 시너지 효과 보정 로직 등 *계산 부분만* — Effect.Apply는 부수효과 보유(상태 변경) 의도된 비적용 |
| 41 | **Immutability First** | 가변보다 불변 우선 | Entry POCO(readonly 필드), Effect 결과 객체 등 데이터 클래스 / 비적용: Service 내부 캐시, View 상태 |

### G. 법칙·관찰 (`#관찰` `#팀워크`)

| # | 원칙 | 한 줄 정의 | 본인 적용 |
|---|------|----------|----------|
| 42 | **Hyrum's Law** | 충분한 사용자 = 모든 observable 동작이 누군가의 의존성 | 1인 개발이라 직접 적용은 약함 / 적용: ADR History timeline + Plan followup 룰의 동기 — 명시되지 않은 동작도 *코드의 기대로 굳어진다*는 인식이 "결정 번복은 History timeline에" 룰의 근거 (→ 풀노트) |
| 43 | **Postel's Law** (Robustness Principle) | 보낼 때 보수적, 받을 때 관대 | SO 매핑 빌드 시점 IsNullOrEmpty 가드 + null 시 LogWarning(idea-notes #19) — 호출자에는 엄격한 시그니처, 매핑 빌드에는 관대한 fallback. Effect 객체 Apply에서 대상이 null이어도 silent return (→ 풀노트) |
| 44 | **Linus's Law** | "Given enough eyeballs, all bugs are shallow" | 1인 개발이라 약함 / 응용: /check-done 메뉴 + docs-check.sh가 *반복 회상*으로 검출 — 다수의 눈 대신 다수의 패스로 대체 |
| 45 | **Pareto Principle (80/20)** | 80% 효과는 20% 노력에서 | 하네스 ADR-033 회귀의 동기 — Phase 3+ 자동화 hook 12개가 효과의 20% 미만이라 폐기. 4종 agent + 4종 skill로 80% 커버 |
| 46 | **Goodhart's Law** | 측정이 목표가 되면 측정으로서의 가치를 잃음 | 하네스 self-monitoring 폐기의 동기 — 토큰 사용량 추적이 *목표*가 되면 *간결한 답변*이 *짧은 답변*으로 변질. 측정은 stateless 수집만, 임계 강제는 없음 |
| 47 | **Ninety-Ninety Rule** (Tom Cargill) | 코드 90% 작성에 시간 90%, 나머지 10%에 또 90% | T3 plan 작성 시 "1차 구현 60%, /check-done + followup 40%" 시간 분배의 근거 — 마지막 10% 비용을 plan에 미리 계상 |

*인덱스 표가 SOT, 풀노트는 위 승격 트리거 임박 시 작성.*

---

## 본인 적용 미정 (idea-notes 인박스로 등재)

다음 원칙들은 CasualStrategy에서 직접 적용 사례가 없거나 약해 [[idea-notes]] 인박스에 1줄 등재. 첫 만남 누적 시 본 노트로 승격:

- **Mechanical Sympathy** (Martin Thompson) — Unity 게임이지만 본격 적용 없음, 부분 적용은 NonAlloc/풀링뿐
- **Conway's Law** — 1인 개발이라 직접 적용 N/A, 다만 인간+AI 협업 구조 반영 가능성 관찰
- **Brooks's Law** — 1인 개발 + AI 협업이라 직접 적용 N/A
- **Wirth's Law** — Unity 6 + URP 사례 관찰 정도, 캐주얼 전략은 GPU 여유라 묵인
- **AAA** (Arrange, Act, Assert) — 자동화 테스트 미운영
- **F.I.R.S.T.** (Fast/Independent/Repeatable/Self-validating/Timely) — 자동화 테스트 미운영
- **Given-When-Then** (BDD) — 자동화 테스트 미운영

---

## 6블록 풀노트 템플릿 (원칙 변형)

```markdown
## N. 원칙명

**한 줄 요약**
{원칙 정의 1줄}

**왜 본인이 이렇게 다루는가**
{채택/조건 적용/기각/오용주의의 실질 근거 — 라벨 아닌 본문}

**적용 사례 (또는 비적용 영역)**
{어디서 어떻게 적용했는지, 또는 어디서 의도적으로 안 적용했는지}

**오용 사례 / 반대 원칙** (선택)
{함정, 트레이드오프, 반대 원칙과의 관계}

**메타**
- 종속성: {#언어독립 / #OOP / #타입시스템 등}
- 첫 도출: {프로젝트명 + 날짜}
- 태그: {태그들}
```

---

## 항목 번호 정책

- **추가 전용 (renumber 금지)** — 교차 참조 안정성 보장
- 삭제는 strike-through (`~~삭제됨~~`) 또는 "이주" 표시
- 새 항목은 `max(번호)+1`
- idea-notes에서 승격 시 본 노트의 적합 카테고리 끝 번호 + 1로 부여

---

# 풀노트

## 1. YAGNI (You Ain't Gonna Need It)

**한 줄 요약**
추측 기반 기능/추상화 도입 금지. 현재 명시적으로 필요한 것만 구현.

**왜 본인이 이렇게 다루는가**
CasualStrategy 4원칙 #2 Simplicity First로 명문화된 *프로젝트 강제*. plan 작성 시점에 가정을 표면화하면 "이 추상화는 현재 요구사항이 아니라 *내가 미래에 필요할 거라 추측한 것*"이 드러남. AI(Claude) 협업에서 특히 중요 — AI는 *완전성 편향*으로 abstract base, 인터페이스, 매개변수를 선제적으로 추가하는 경향이 있음. 사용자가 plan에서 "현재 사례 1건"이라 명시하면 AI가 over-engineering 회피.

**적용 사례**
- CasualStrategy 4원칙 #2 Simplicity First — 모든 plan의 가정 표면화 단계가 YAGNI 강제 메커니즘
- F-1~F-N 시너지 효과를 추가할 때 abstract `SynergyEffectBase` 미신설 — 각 효과는 ScriptableObject + `SynergyEffectType` enum + switch dispatch로 충분. 두 번째 시너지 효과를 본 시점에서 base 추출 충동이 컸으나, *세 번째 효과의 형태를 모르므로* 보류
- /commit-msg의 "묶음 토글"이 단일 plan 1건 stateless 추론으로 단순 — 다중 plan 매핑 시스템(ADR-047 회귀 대상)을 안 만든 결정의 근거

**오용 사례 / 반대 원칙**
- 반대 원칙: **Speculative Generality**(#36) — YAGNI의 코드 스멜 짝. 검출 신호: 호출처 1곳뿐인 인터페이스, 단일 자식만 가진 abstract base, 사용 안 되는 매개변수
- 오용 가능 지점: "현재 X 1건이지만 *근시일 내* Y 2건 추가 예정"인 경우 → YAGNI 엄격 적용 시 마이그레이션 비용 폭발. 해결: plan에서 *근시일 내 예정 사례*를 명시적으로 노출 후 추상화 시점 판단

**메타**
- 종속성: `#언어독립` `#엔진독립`
- 첫 도출: CasualStrategy (2026-05-21) — 4원칙 #2 Simplicity First가 일반 원칙으로 추출
- 태그: `#설계` `#코드` `#아키텍처`

## 3. DRY (Don't Repeat Yourself)

**한 줄 요약**
지식의 중복 회피. *코드 행*의 중복이 아닌 *의사결정·도메인 지식*의 중복만 추출 대상.

**왜 본인이 이렇게 다루는가**
DRY의 통상 해석은 "같은 코드 보이면 추출"이지만 — 비슷해 *보이는* 두 코드가 *다른 변경 이유*를 가질 수 있음. 두 번째 만남에서 추출하면 세 번째 사례가 *다른 형태*로 나타날 때 base가 폭발 (idea-notes #14 F-4 32건 오판이 직접 증거). DRY 본문은 "지식의 중복"이라 명시했는데도 코드 행 단위로 오용되는 현상이 잦음.

**적용 사례 (적용 + 비적용 분리)**
- **적용**: SO 데이터 매핑 빌드 로직(idea-notes #19) — itemId 추출 + Dictionary 빌드는 *동일한 지식*이라 헬퍼 추출
- **적용**: Manager Singleton MonoSingleton<T> CRTP base — 인스턴스 보존 라이프사이클은 *동일한 지식*
- **비적용**: HealthService와 ManaService의 비슷한 구조 — *변경 이유가 다름*(체력 규칙 vs 마나 규칙). base 추출 보류, 3번째 자원 타입 출현 시 재검토
- **비적용**: View와 Sequence의 비슷한 초기화 패턴 — *책임이 다름*(데이터 holder vs 연출). base 추출 시 SRP(#9) 위반

**오용 사례 / 반대 원칙**
- 반대 원칙: **AHA**(#7) — "잘못된 추상화가 중복보다 비싸다"는 DRY 과적용 방지 표어
- 짝 원칙: **Rule of Three**(#4), **WET**(#8) — 추출 임계치는 3번째 만남
- 오용 가능 지점: AI 협업 시 특히 위험 — AI는 *시각적 유사성*에 반응해 base 추출을 제안. 사용자가 "변경 이유가 같은가?" 1줄 검증 필요

**메타**
- 종속성: `#언어독립` `#엔진독립`
- 첫 도출: CasualStrategy (2026-05-21) — idea-notes #14 sub-pattern 분기 보정 사례에서 일반 원칙 추출
- 태그: `#설계` `#코드` `#리팩토링`

## 6. Boy Scout Rule (채택 안 함)

**한 줄 요약**
"캠프 떠날 때 더 깨끗하게" — 코드 수정 시 주변 cleanup 동반. **본인은 채택 안 함**.

**왜 본인이 이렇게 다루는가**
CasualStrategy 4원칙 #3 Surgical Changes("요청 라인만 수정, 주변 cleanup 금지")와 정면 충돌. Boy Scout Rule이 작동하려면 (a) cleanup 비용 < 회피 비용, (b) cleanup 후 회귀 위험 < 잠재 이득이 성립해야 하는데 — AI 협업 환경에서는 두 가정 모두 깨짐:
- (a) AI는 *주변 코드 정리*를 무한히 발견하므로 cleanup 비용이 폭주
- (b) Surgical 외 변경이 리뷰 시 *원래 요청과 cleanup의 경계*를 흐려 회귀 검토 곤란

**적용 사례 (대안)**
- 대안 1: cleanup 필요 인지 시 **별 묶음 plan으로 분리** (`docs/plan-{cleanup-topic}.md`). 같은 commit에 끼우지 않음
- 대안 2: cleanup이 *trivial*이면 (오타·포맷·주석) `/check-done clean` 메뉴에서 묶음 처리 — 단, 의미 변경은 금지
- 대안 3: cleanup이 *떨어진 코드*면 followup 짝(`plan-{topic}-followup.md`)에 누적 후 별 plan으로 분리
- 사례: ShopController 5분리(idea-notes #16) 시 "코디네이터는 코디네이터 책임만, sub-Controller 내부 cleanup은 별 plan"으로 분리. 단일 commit이 700행 변경되는 빅뱅 회피

**오용 사례 / 반대 원칙**
- 정합 원칙: **Surgical Changes**(CasualStrategy 4원칙 #3), **Chesterton's Fence**(#35) — 둘 다 *주변에 손대지 마라* 계열
- 짝 원칙: **Rule of Three**(#4) — cleanup도 3번째 만남에 plan화하는 게 본인 룰
- 본 원칙이 채택될 환경: 다수 개발자 + CI 강제 + 작은 commit 룰이 합의된 환경. 1인 개발 + AI 협업에서는 *경계 흐림*이 더 큰 비용

**메타**
- 종속성: `#언어독립` `#엔진독립`
- 첫 도출: CasualStrategy (2026-05-21) — 4원칙 #3 Surgical Changes가 본 원칙의 명시적 반대 입장
- 태그: `#설계` `#프로세스` `#팀워크`

## 7. AHA (Avoid Hasty Abstractions)

**한 줄 요약**
"잘못된 추상화는 중복보다 비싸다" — Kent C. Dodds. Rule of Three의 강화판.

**왜 본인이 이렇게 다루는가**
DRY(#3)의 통상 적용이 "2번째 만남에 base 추출"인데, *2번째 만남에서 발견한 공통점이 우연*인 경우가 많음. 3번째가 다른 형태로 나타나면 잘못된 base를 깨고 재추출하는 비용 > 처음부터 중복 유지하는 비용. AI 협업에서 특히 빈번 — AI는 시각적 유사성으로 base를 제안하지만 도메인 지식이 부족해 *우연한 유사성*을 잡아냄.

**적용 사례**
- idea-notes #14 sub-pattern 분기 보정 — F-4 단일 행 정의가 32건 오판을 만든 사례가 직접 증거. 단일 정의가 *실제 코드의 회색지대*를 흡수 못 함 → sub-pattern 분기로 정의 정확도 회복
- SynergyEffect와 AttributeEffect의 비슷한 Apply 패턴 — 1차 base `EffectBase` 도입 시도했으나 시너지는 *카운터 트리거*이고 속성은 *조건 트리거*라 base가 빈 껍데기로 전락. base 폐기 후 각자 ScriptableObject 별도
- ItemDataSO와 UsableItemDataSO — abstract base 만들지 않고 *2 베이스 + 매핑 시점 통합 Dictionary*로 처리(idea-notes #19)

**오용 사례 / 반대 원칙**
- 짝 원칙: **Rule of Three**(#4), **WET**(#8) — 추출 임계치
- 반대 원칙: **DRY**(#3) — DRY 과적용 방지가 AHA의 본질
- 검출 신호: base를 만든 후 *자식이 base 메서드를 거의 안 쓰거나*, *base에 자식별 분기 if/else가 생기는* 경우 → 잘못된 추상화 신호

**메타**
- 종속성: `#언어독립` `#엔진독립`
- 첫 도출: CasualStrategy (2026-05-21) — idea-notes #14 F-4 32건 오판 사례에서 추출
- 태그: `#설계` `#코드` `#리팩토링`

## 9. SRP (Single Responsibility Principle)

**한 줄 요약**
"한 클래스는 한 변경 이유만 가진다" — Uncle Bob. *변경 이유* 단위지 *기능 개수* 단위가 아님.

**왜 본인이 이렇게 다루는가**
SRP의 통상 오용은 "한 클래스 = 한 메서드/기능"으로 해석. 그러나 본 원칙의 본질은 *변경 이유*(reason to change) — 같은 변경 요구로 같이 수정되는 코드는 한 클래스에 모이고, 다른 변경 요구로 수정되는 코드는 분리. CasualStrategy의 UI 4축(View/Binder/Controller/Sequence)과 인프라 11종 접미사 분류가 본 원칙의 *분류 체계화*. 단순히 "책임 1개"가 아니라 "변경 이유 1개 + 책임 유형 명명"으로 강제.

**적용 사례**
- **UI 4축**: View(데이터 holder, 변경 이유 = prefab 구조 변경), Binder(UI 데이터 바인딩, 변경 이유 = 이벤트→UI 매핑), Controller(로직, 변경 이유 = 사용자 인터랙션), Sequence(연출, 변경 이유 = 시각 표현)
- **인프라 11종**: Manager(라이프사이클), Service(비즈니스 로직), Effect(3종 효과), Entry(데이터), Pool(추첨), Spawner(풀+큐), Handler(이벤트), 단발 패턴(Director/Core/Base/Filter/Detector/Router) — 각 접미사가 *변경 이유*의 표식
- **ShopController 5분리** (idea-notes #16): 700행 Controller → 144행 코디네이터 + 5 sub-Controller(아이템슬롯/소비/등급업/벤치/드롭률뷰). 각 sub는 *변경 이유*가 독립

**오용 사례 / 반대 원칙**
- 오용: "한 클래스 = 한 메서드" 해석 → 클래스 수 폭발, 호출 그래프 비대
- 짝 원칙: **Separation of Concerns**(#22) — SRP의 모듈 단위 적용
- 검출 신호: 한 클래스의 메서드를 두 그룹으로 자를 수 있다 = SRP 위반 후보. 단, 그룹이 *같은 변경 요구로 함께 수정*되면 위반 아님 (코드량과 무관)
- 회색지대: Manager+Service 컴포지션에서 Manager가 *라이프사이클* + *최상위 dispatch*를 동시 보유 — 본 책임은 *함께 변경*되므로 SRP 정합

**메타**
- 종속성: `#OOP` `#언어독립`
- 첫 도출: CasualStrategy (2026-05-21) — UI 4축 + 인프라 11종 접미사 분류가 SRP의 분류 체계화
- 태그: `#설계` `#모듈` `#아키텍처`

## 32. SLAP (Single Level of Abstraction Principle)

**한 줄 요약**
한 메서드 내 모든 호출이 같은 추상화 레벨이어야 함. 고수준 의도와 저수준 구현이 섞이면 SLAP 위반.

**왜 본인이 이렇게 다루는가**
SRP(#9)가 *클래스 단위*의 책임 분리라면 SLAP은 *메서드 단위*의 추상화 통일. 한 메서드 안에 "Begin 호출" + "for 루프로 인덱스 계산" + "UI 텍스트 직접 설정"이 섞이면 — 읽는 사람이 *어느 레벨에서 사고해야 할지* 매번 전환해야 함. ShopController 700행은 *클래스 책임 과다*(SRP)도 문제였지만, 각 메서드 내부에 *모든 추상화 레벨이 혼재*한 SLAP 위반이 코드 회상 비용의 주범.

**적용 사례**
- **ShopController 코디네이터화** (idea-notes #16): 코디네이터의 OnDraw() 메서드는 *sub-Controller 호출* 한 레벨만(`itemSlot.Refresh(); usableSlot.Refresh(); benchSlot.Refresh();`). 각 sub의 Refresh 내부에 *저수준 구현*. 호출 그래프가 트리 형태로 정리되어 어느 레벨에서 디버깅할지 명확
- **batch 패턴** (idea-notes #13): `BeginQueueBatch() { batchActive = true; batchDirty = false; }` — 메서드 내부가 *플래그 설정* 한 레벨만. dispatch는 EndQueueBatch가 별도
- **Sequence vs Controller**: Sequence는 *연출 step* 레벨(WaitForSeconds, DOTween 호출), Controller는 *비즈니스 의도* 레벨(StartSequence(), OnSequenceEnd) — 레벨 분리가 SLAP의 클래스 분리 사례

**오용 사례 / 반대 원칙**
- 짝 원칙: **SRP**(#9), **Separation of Concerns**(#22) — SLAP는 SRP의 메서드 버전
- 검출 신호: 한 메서드의 본문을 위에서 아래로 읽었을 때 *추상화 사다리를 오르락내리락*하는 느낌 = 위반. 정합 메서드는 *수평 이동*만
- 오용 가능 지점: 모든 메서드를 SLAP 강제 시 *얇은 wrapper 메서드 폭발*. 임계는 "메서드가 3+ 레벨을 동시에 다룬다" 시점부터 분리

**메타**
- 종속성: `#언어독립` `#OOP`
- 첫 도출: CasualStrategy (2026-05-21) — ShopController 5분리(idea-notes #16) 사례에서 SRP와 함께 추출
- 태그: `#설계` `#코드` `#리팩토링`

## 38. Make Illegal States Unrepresentable

**한 줄 요약**
잘못된 상태를 *컴파일 단계*에서 표현 불가능하게 — Yaron Minsky. 런타임 검증 대신 타입 시스템 활용.

**왜 본인이 이렇게 다루는가**
런타임 가드(if-null check, 범위 체크)는 *호출자가 잊을 가능성*이 있음. 타입으로 강제하면 *컴파일 안 됨* → 잊을 수 없음. C#의 타입 시스템 + Unity 직렬화 시스템을 활용하면 게임 도메인에서도 적용 가능. 다만 모든 상태에 적용 시 타입 폭발 → *silent corruption 위험이 큰 영역*에 선별 적용.

**적용 사례**
- **SynergyEffectType enum 정수값 영구 점유** (idea-notes #18): 폐기된 enum 멤버의 정수값을 *재사용 금지*. SO YAML에 잔존 정수값이 다른 의미로 매핑되어 silent corruption 발생하는 함정 차단. 컴파일 시점에 강제는 아니지만 *명시 룰 + 코드 리뷰*로 동등 효과
- **SerializeReference 자식 인스턴스 deep clone** (idea-notes #8): 같은 SerializeReference 인스턴스를 두 SO가 공유하면 한쪽 수정이 다른 쪽에 silent 전파. clone 강제로 *공유 불가능한 상태* 표현
- **string ID → SO 직접 참조** (idea-notes #19): 인스펙터 wiring에서 *유효한 SO만 받을 수 있는 타입*으로 강제 — 오타로 인한 빈 문자열 자체가 컴파일/직렬화 단계에서 차단

**오용 사례 / 반대 원칙**
- 짝 원칙: **Parse, Don't Validate**(#39) — 동일 철학의 함수형 표현
- 짝 원칙: **Design by Contract**(#30) — precondition을 타입으로 인코딩
- 오용 가능 지점: 모든 상태를 타입으로 표현하면 *제네릭 폭발*. 임계는 "런타임 가드 실패 시 silent corruption" 영역에만 적용. 단순 입력 검증은 Fail Fast(#25)로 충분
- C# 한계: discriminated union 없음 → enum + visitor 패턴 또는 sealed class hierarchy로 우회. F#/Rust보다 비용 큼

**메타**
- 종속성: `#타입시스템` `#OOP`
- 첫 도출: CasualStrategy (2026-05-21) — idea-notes #18 enum 멤버 rename 사례 + idea-notes #8 SerializeReference deep clone 사례에서 추출
- 태그: `#설계` `#타입` `#코드`

## 42. Hyrum's Law

**한 줄 요약**
"With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." — Hyrum Wright.

**왜 본인이 이렇게 다루는가**
1인 개발 + AI 협업이라 *외부 사용자*는 없지만 — *AI*와 *미래의 자신*이 사용자. 명시되지 않은 동작도 *코드의 기대로 굳어진다*는 인식이 ADR History timeline + Plan followup 룰의 동기. 예를 들어 RunManager.OnQueueChanged 이벤트의 *발화 시점*(즉시 vs batch end)을 명시 안 하면, 구독자가 *과거 발화 시점*에 의존하는 코드를 작성 → 시점 변경 시 silent 회귀.

**적용 사례**
- **ADR History timeline** 룰: 결정 번복·동작 변경은 반드시 History timeline에 1줄 추가. *명시되지 않은 과거 동작*이 새 동작으로 바뀔 때 *왜 바뀌었는지* 회상 가능
- **Plan followup 짝**: 가정 차이/누락은 즉시 수정이 아니라 followup에 누적. *수정 시점*에 *기존 동작에 의존한 코드*가 있는지 검토 후 진행
- **batch 패턴 도입**(idea-notes #13): RunManager.OnQueueChanged의 발화 시점을 *명시적으로 batch end*로 변경 시, 기존 구독자 중 *즉시 발화 가정*에 의존한 코드가 있는지 grep으로 전수 확인 후 진행 — Hyrum's Law 회피 절차
- **AI 협업 적용**: AI에게 "현재 동작에 의존한 코드가 있을 수 있다" 인식을 plan에 명시. AI는 변경 영향 범위 추정 시 *명시된 contract*만 보는 경향이 있어, *observable behavior* 의존성을 놓치기 쉬움

**오용 사례 / 반대 원칙**
- 짝 원칙: **Chesterton's Fence**(#35) — *이유 모르는 동작*은 의존이 있을 수 있다는 인식
- 짝 원칙: **POLA**(#27) — 호출자가 *놀라는* 동작 = *기존 동작에 의존*했다는 신호
- 오용 가능 지점: Hyrum's Law를 *완벽 보존*으로 해석하면 *어떤 변경도 위험*해져 stagnation. 임계는 "변경의 의도 > 의존 비용"일 때 진행 + History timeline 명시

**메타**
- 종속성: `#언어독립` `#팀워크`
- 첫 도출: CasualStrategy (2026-05-21) — ADR History timeline + Plan followup 룰의 일반 원칙 추출
- 태그: `#팀워크` `#관찰` `#프로세스`

## 43. Postel's Law (Robustness Principle)

**한 줄 요약**
"Be conservative in what you send, be liberal in what you accept." — Jon Postel. 보낼 때는 엄격한 형식, 받을 때는 관대한 파싱.

**왜 본인이 이렇게 다루는가**
호출자(보내는 쪽)는 *형식 보장*으로 받는 쪽의 가드 부담 ↓, 받는 쪽은 *관대한 파싱*으로 호환성 ↑. 게임 도메인에서는 (a) SO 매핑 빌드처럼 *사용자(디자이너)가 인스펙터로 데이터 입력*하는 경계와 (b) 도메인 객체 간 호출 경계가 다름 — 전자에는 Postel's Law, 후자에는 Design by Contract(#30) 적용.

**적용 사례 (적용 + 비적용 분리)**
- **적용 (보낼 때 보수적)**: Service 시그니처는 엄격한 타입(`ItemDataSO`, `int amount`) — null/0 입력 시 호출자 오류로 throw. SO 매핑 빌드는 IsNullOrEmpty 가드(idea-notes #19) — 빈 entry는 silent skip + LogWarning
- **적용 (받을 때 관대)**: Effect 객체 Apply에서 대상이 null이어도 silent return — 효과 발동 타이밍에 대상이 *제거된 상태*일 수 있음(코루틴 지연). LogWarning 없이 종료
- **적용 (받을 때 관대)**: 인스펙터 wiring 시점에 SO 매핑 entry가 비어있으면 빌드 단계에서 skip + LogWarning — 디자이너가 wiring을 빠뜨려도 게임이 죽지 않음
- **비적용**: Service 간 호출은 Design by Contract(#30) 적용 — 호출자가 precondition 위반 시 ctor throw. *내부 호출에는 관대함이 silent 버그 양산*

**오용 사례 / 반대 원칙**
- 반대 원칙: **Fail Fast**(#25) — 내부 호출에는 Fail Fast가 정합, *외부 경계*에만 Postel's Law
- 짝 원칙: **Defensive Programming**(#33) — 본인이 채택 안 한 원칙. Postel's Law의 "받을 때 관대"가 *전 경계 적용*되면 Defensive Programming의 보일러플레이트 비대로 변질
- 현대 비판: HTTP/HTML 등 *프로토콜* 영역에서는 Postel's Law가 *불일치 누적 → 호환성 지옥*을 야기. 본 원칙은 *호출 경계*에서는 유효하나 *프로토콜 표준*에는 부적합 (RFC 9413 권장 폐기). 게임 도메인은 *외부 디자이너 입력* 경계라 적합
- 오용 가능 지점: 모든 입력에 관대함 적용 시 silent 데이터 손상 — 디자이너가 *잘못된 데이터 입력*해도 게임이 동작해버려 발견 지연. LogWarning 강제로 *관대함의 가시화* 필요

**메타**
- 종속성: `#언어독립`
- 첫 도출: CasualStrategy (2026-05-21) — SO 매핑 빌드 IsNullOrEmpty 가드(idea-notes #19) 사례에서 추출
- 태그: `#구현` `#코드` `#아키텍처`
