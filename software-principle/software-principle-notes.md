# 소프트웨어 원칙 노트

> 상위 노트: [[Dev Notes README]]
> 다루는 축: 일반 소프트웨어 개발 원칙·휴리스틱·해석. 코드 *형태*가 아닌 *판단 기준*의 추상화
> 다루지 않는 축: 구체 패턴 구현(→ design-pattern-notes), 게임 특화 기법(→ game-technique-notes), 단편 트릭(→ game-misc-notes)
> 적용 범위: 언어/엔진/도메인 완전 독립 — 원칙은 메타 레벨
> 관련 노트: design-pattern-notes (원칙의 구체 적용), idea-notes (검증 전 원칙 후보 + 본인 적용 미정 원칙 인박스)
> 평생 노트 정책: 인덱스 표는 *왜 + 어디 적용 / 대안 / 오용 지점* 1줄, 풀노트는 본인 해석·사례 중심
> 승격 임계치: 풀노트 항목이 카테고리당 8개 이상 시 분리 검토 (design-pattern-notes와 동일)
> 풀노트 작성 기준: 인덱스 1줄만으로 적용/판단이 불충분한 항목. 자명한 항목만 인덱스로 종료
> 본인 입장 표기 룰: `#수용` `#기각` 같은 라벨 금지. 본인 적용 셀에 *왜 + 어디 적용* (조건부면 *수용/비수용 경계*, 기각이면 *대안*, 오용주의면 *오용 지점*) 실질 1줄
> 작성 시작: 2026-05-21

---

**서브 노트:**
- [[software-principle-simplicity|소프트웨어 원칙 — 단순성]] — YAGNI·KISS·DRY·AHA·보이 스카우트 등
- [[software-principle-design|소프트웨어 원칙 — 설계]] — SOLID·GRASP·결합도·응집도
- [[software-principle-quality-laws|소프트웨어 원칙 — 코드품질·법칙]] — 코드품질·안티패턴·법칙


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
| 9 | **SRP** (Single Responsibility) | 한 클래스는 한 변경 이유만 | 책임 ≠ "기능 1개"가 아니라 "변경 이유 1개" — UI 4축(View/Binder/Controller/Sequence)과 인프라 11종 접미사 분류의 상위 원칙. 적용: ShopController 5분리(idea-notes 항목 16) (→ 풀노트) |
| 10 | **OCP** (Open/Closed) | 확장에는 열려, 수정에는 닫혀 | 새 SO/Strategy 등록만으로 코어 무수정이면 적용(시너지/속성 효과 SO, AnimationConfigSO 매핑) / Manager 내부 분기 추가는 직접 수정 허용 — 인터페이스 폭증을 만들면서까지 강요 X |
| 11 | **LSP** (Liskov Substitution) | 자식이 부모를 의미 손상 없이 대체 | 의미 손상 발견 즉시 *상속 → 컴포지션 또는 별 베이스 분리* — ItemDataSO/UsableItemDataSO 베이스 분리(idea-notes 항목 19)가 본 원칙 위반 회피 사례 |
| 12 | **ISP** (Interface Segregation) | 클라이언트가 안 쓰는 메서드에 의존 X | 도메인 인터페이스는 5+ 메서드 시 분리(Effect 3종 Apply/Emit/Describe) / Unity MonoBehaviour의 생명주기 강제는 엔진 제약이므로 위반 묵인 |
| 13 | **자동화 회귀 판단 기준** (karpathy-regression 해석) | 자동 강제 전면 금지가 아니라 토큰 부하 대비 가치 낮은 자동화만 폐기 | bash 50줄 이하·5초 이하 저비용 일회성 차단(PreToolUse)은 예외 — 복잡한 상태 관리/메트릭 수집/자동 분류가 진짜 폐기 대상. 판단 질문: "이 자동화의 실행 비용이 유지보수 비용보다 큰가?" Yes → 폐기, No → 유지 검토. CasualStrategy: plan-first-guard.sh 도입 근거 (2026-06-04) |
| 13 | **DIP** (Dependency Inversion) | 추상에 의존, 구체에 의존 X | ctor 주입이 정합 / Manager+Service 부모 역참조는 회색지대로 허용(idea-notes 항목 15), 외부 Manager 호출은 위반(정리 대상) — Service 7개 컴포지션에 적용 |
| 14 | **GRASP – Information Expert** | 책임은 정보를 가진 객체에 부여 | Effect 객체가 자체 Apply/Emit/Describe — 외부에서 상태 읽고 결정하지 않음. Tell-Don't-Ask(항목 21)의 책임 분배 측면 |
| 15 | **GRASP – Pure Fabrication** | 적합한 도메인 클래스가 없으면 신설 | Service/Director/Filter 등 인프라 11종 접미사가 본 원칙의 적용 — 도메인에 없는 책임은 가공 클래스로 |
| 16 | **GRASP – Indirection** | 결합도 ↓ 위해 중간 객체 도입 | FlowDirector가 Manager 간 라우팅 — Battle/Item Manager 직접 호출 금지의 동력 |
| 17 | **GRASP – Protected Variations** | 변동 지점을 인터페이스/추상 뒤에 격리 | OCP(항목 10)의 동력 — 시너지/속성 효과 SO 분리는 본 원칙이 OCP보다 정확한 표현 (어디를 격리할지 = 변동 지점 식별) |
| 18 | **High Cohesion, Low Coupling** | 모듈 내부 결속 ↑ 외부 결합 ↓ | namespace 단위 응집 + Manager 간 이벤트 의존만 허용 — Battle/Item/UI namespace 분리, FlowDirector 라우팅 |
| 19 | **Law of Demeter** (`a.b.c.d()` 금지) | 직접 협력자만 호출 | 비즈니스 로직 간 chained는 위반(정리) / View가 Binder→Controller 데이터 조회 시 chained는 자연(거부 시 Binder 위임 메서드 폭증) — UI 4축에서 오용 가능성 발생 |
| 20 | **Composition Over Inheritance** | 상속보다 컴포지션 | Unity 컴포넌트 모델 자체가 본 원칙의 강제 — Manager+Service 컴포지션, sub-Controller 동거 분리(idea-notes 항목 16) |
| 21 | **Tell, Don't Ask** | 상태를 묻고 결정 X, 위임 | 도메인 객체에 동작 위임(Effect 객체가 자체 Apply/Emit/Describe) / View는 dumb holder 원칙으로 *물어보는 쪽* 허용 — UI 4축에서 비적용 영역 명시 |
| 22 | **Separation of Concerns** | 책임이 다른 코드는 다른 모듈로 | SRP의 모듈 단위 적용 — UI 4축 분리, 인프라 11종 접미사 분류, 데이터↔연출 분리(idea-notes 항목 3)의 근거 |
| 23 | **Stable Dependencies Principle** | 안정한 모듈에 의존, 불안정한 모듈은 의존받지 않음 | Core(Manager Singleton) ← Battle/Item/UI 단방향 의존 — Core는 안정, 도메인 namespace는 불안정. 역의존 발견 시 즉시 인터페이스/이벤트로 역전 |
| 24 | **Acyclic Dependencies Principle** | 모듈 의존 그래프에 순환 없음 | namespace 계층 + Manager 간 이벤트 의존만 허용의 근거 — 동기 호출 순환은 차단, 비동기 이벤트는 허용 (런타임 순환은 매니저 상태로 끊김) |
| 25 | **Fail Fast** | 에러는 조용히 삼키지 말고 즉시 노출 | Debug.LogWarning + null 가드 또는 throw — SO 매핑 빌드 시점 IsNullOrEmpty 가드(idea-notes 항목 19), Service 컴포지션 누락 시 ctor throw |
| 26 | **Make It Work, Make It Right, Make It Fast** (Kent Beck) | 단계적 개선 순서 | plan → 1차 구현 → /check-done → 리팩토링 묶음의 단계와 동치 — 모든 T3/T4 plan 진행 순서 |
| 27 | **POLA** (Principle of Least Astonishment) | 호출자가 놀라지 않게 | 메서드 이름 = 부수효과까지 표현(BeginQueueBatch/EndQueueBatch batch 패턴, idea-notes 항목 13). 어디서 오용 가능: 짧은 이름을 위해 부수효과 숨기면 race/double-fire 함정 |
| 28 | **Convention over Configuration** | 합리적 기본값 + override만 노출 | SerializeField 기본값 + 인스펙터 override — Manager Singleton의 SO 자동 로드, Builder 1회 셋업 + YAML override |
| 29 | **CQS** (Command-Query Separation, Bertrand Meyer) | 메서드는 명령(상태 변경) 또는 쿼리(상태 조회), 둘 다 X | Service.GetX() vs Service.ApplyX() 분리 패턴 / 비적용: batch 패턴(BeginX/EndX, idea-notes 항목 13)에서 EndX는 명령+이벤트 발화 동반(의도된 부분 위반) |
| 30 | **Design by Contract** (Bertrand Meyer) | preconditions/postconditions/invariants 명시 | Service 컴포지션 누락 시 ctor throw — precondition 위반은 즉시 실패(Fail Fast 항목 25와 짝). 비적용: postcondition assert는 게임 도메인에 과한 비용 |
| 31 | **Hollywood Principle** (IoC) | "Don't call us, we'll call you" — 프레임워크가 호출, 사용자 코드는 등록만 | Unity 자체가 본 원칙의 강제 — Awake/Update/OnDestroy 라이프사이클 콜백. 도메인 코드에서는 Manager 이벤트 구독이 동일 패턴 |
| 32 | **SLAP** (Single Level of Abstraction Principle) | 한 메서드 내 모든 호출이 같은 추상화 레벨 | Controller 코디네이터화(idea-notes 항목 16)의 근거 — 700행 Controller가 데이터/UI/버튼 풀스택 혼재했던 이유는 SLAP 위반. 같은 GameObject sub-Controller 분리로 코디네이터는 한 레벨만 (→ 풀노트) |
| 33 | **Defensive Programming** | 호출자 신뢰 X, 입력 검증 적극 | 채택 안 함 — Service 내부는 호출자 신뢰(public 시그니처에서만 가드). 대안: DIP(항목 13)로 타입 강제 + Fail Fast(항목 25)로 보일러플레이트 회피. 모든 메서드 입력 검증은 비대 |
| 34 | **Worse is Better** (Richard Gabriel) | 완벽한 설계보다 동작하는 단순함 | skill/agent 카탈로그·하네스 hook은 단순함 우선 / decisions/ ADR은 정확성 우선 — 영역별 트레이드오프 분리 적용 |
| 35 | **Chesterton's Fence** | 이유 모르는 코드는 함부로 제거 X | Surgical Changes(4원칙 항목 3) 정합 — 모르는 코드는 git blame + commit 메시지 확인 후 제거. /check-done clean의 PENDING 스캔 룰의 근거 |
| 36 | **Speculative Generality** (Code Smell) | 미래 가정 기반 추상화 = YAGNI 위반 | YAGNI(항목 1)의 코드 스멜 짝 — plan 작성 중 "나중에 X도 필요할 수 있으니" 충동, 단일 자식만 가진 abstract base 신설 충동에서 오용 발생. 검출: 호출처 1곳뿐인 인터페이스 |
| 37 | **Big Ball of Mud** (Foote & Yoder) | 구조 없는 아키텍처의 자연 상태 | 자연 상태로 회귀하지 않게 *주기적 정합 감사* 필요 — /check-done arch/adr 메뉴, docs-check.sh 정합 검증의 동기 |
| 38 | **Make Illegal States Unrepresentable** (Yaron Minsky) | 잘못된 상태를 컴파일 단계에서 표현 불가능하게 | SynergyEffectType enum + 멤버별 정수값 영구 점유 룰(idea-notes 항목 18) — "삭제된 효과 정수 재사용 금지"가 silent corruption 차단. SerializeReference 자식 인스턴스 deep clone(idea-notes 항목 8)도 같은 동기 (→ 풀노트) |
| 39 | **Parse, Don't Validate** (Alexis King) | 검증 대신 파싱 — 검증 결과를 타입에 인코딩 | idea-notes 항목 19 string ID → SO 직접 참조 전환이 부분 적용 — 인스펙터 wiring 시점에 *유효한 SO만 받을 수 있는 타입*으로 강제. 비적용: 런타임 캐시는 string Dictionary 유지(호출자 무변경 트릭) |
| 40 | **Pure Functions** | 같은 입력 = 같은 출력, 부수효과 없음 | Dice 굴림 계산, 시너지 효과 보정 로직 등 *계산 부분만* — Effect.Apply는 부수효과 보유(상태 변경) 의도된 비적용 |
| 41 | **Immutability First** | 가변보다 불변 우선 | Entry POCO(readonly 필드), Effect 결과 객체 등 데이터 클래스 / 비적용: Service 내부 캐시, View 상태 |
| 42 | **Hyrum's Law** | 충분한 사용자 = 모든 observable 동작이 누군가의 의존성 | 1인 개발이라 직접 적용은 약함 / 적용: ADR History timeline + Plan followup 룰의 동기 — 명시되지 않은 동작도 *코드의 기대로 굳어진다*는 인식이 "결정 번복은 History timeline에" 룰의 근거 (→ 풀노트) |
| 43 | **Postel's Law** (Robustness Principle) | 보낼 때 보수적, 받을 때 관대 | SO 매핑 빌드 시점 IsNullOrEmpty 가드 + null 시 LogWarning(idea-notes 항목 19) — 호출자에는 엄격한 시그니처, 매핑 빌드에는 관대한 fallback. Effect 객체 Apply에서 대상이 null이어도 silent return (→ 풀노트) |
| 44 | **Linus's Law** | "Given enough eyeballs, all bugs are shallow" | 1인 개발이라 약함 / 응용: /check-done 메뉴 + docs-check.sh가 *반복 회상*으로 검출 — 다수의 눈 대신 다수의 패스로 대체 |
| 45 | **Pareto Principle (80/20)** | 80% 효과는 20% 노력에서 | 하네스 ADR-033 회귀의 동기 — Phase 3+ 자동화 hook 12개가 효과의 20% 미만이라 폐기. 4종 agent + 4종 skill로 80% 커버 |
| 46 | **Goodhart's Law** | 측정이 목표가 되면 측정으로서의 가치를 잃음 | 하네스 self-monitoring 폐기의 동기 — 토큰 사용량 추적이 *목표*가 되면 *간결한 답변*이 *짧은 답변*으로 변질. 측정은 stateless 수집만, 임계 강제는 없음 |
| 47 | **Ninety-Ninety Rule** (Tom Cargill) | 코드 90% 작성에 시간 90%, 나머지 10%에 또 90% | T3 plan 작성 시 "1차 구현 60%, /check-done + followup 40%" 시간 분배의 근거 — 마지막 10% 비용을 plan에 미리 계상 |

---