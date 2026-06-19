# 소프트웨어 원칙 — 설계

> 상위 노트: [[software-principle-notes]] (전체 인덱스 디스패처)
> 다루는 축: SOLID·GRASP·결합도·응집도
> 다루지 않는 축: 소프트웨어 원칙 — 단순성 / 소프트웨어 원칙 — 코드품질·법칙

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

---

# 풀노트

## 9. SRP (Single Responsibility Principle)

_"한 클래스는 한 변경 이유만 가진다" — Uncle Bob. *변경 이유* 단위지 *기능 개수* 단위가 아님._

**왜 본인이 이렇게 다루는가**
SRP의 통상 오용은 "한 클래스 = 한 메서드/기능"으로 해석. 그러나 본 원칙의 본질은 *변경 이유*(reason to change) — 같은 변경 요구로 같이 수정되는 코드는 한 클래스에 모이고, 다른 변경 요구로 수정되는 코드는 분리. CasualStrategy의 UI 4축(View/Binder/Controller/Sequence)과 인프라 11종 접미사 분류가 본 원칙의 *분류 체계화*. 단순히 "책임 1개"가 아니라 "변경 이유 1개 + 책임 유형 명명"으로 강제.

**적용 사례**
- **UI 4축**: View(데이터 holder, 변경 이유 = prefab 구조 변경), Binder(UI 데이터 바인딩, 변경 이유 = 이벤트→UI 매핑), Controller(로직, 변경 이유 = 사용자 인터랙션), Sequence(연출, 변경 이유 = 시각 표현)
- **인프라 11종**: Manager(라이프사이클), Service(비즈니스 로직), Effect(3종 효과), Entry(데이터), Pool(추첨), Spawner(풀+큐), Handler(이벤트), 단발 패턴(Director/Core/Base/Filter/Detector/Router) — 각 접미사가 *변경 이유*의 표식
- **ShopController 5분리** (idea-notes 항목 16): 700행 Controller → 144행 코디네이터 + 5 sub-Controller(아이템슬롯/소비/등급업/벤치/드롭률뷰). 각 sub는 *변경 이유*가 독립

**오용 / 반대 원칙**
- 오용: "한 클래스 = 한 메서드" 해석 → 클래스 수 폭발, 호출 그래프 비대
- 짝 원칙: **Separation of Concerns**(항목 22) — SRP의 모듈 단위 적용
- 검출 신호: 한 클래스의 메서드를 두 그룹으로 자를 수 있다 = SRP 위반 후보. 단, 그룹이 *같은 변경 요구로 함께 수정*되면 위반 아님 (코드량과 무관)
- 회색지대: Manager+Service 컴포지션에서 Manager가 *라이프사이클* + *최상위 dispatch*를 동시 보유 — 본 책임은 *함께 변경*되므로 SRP 정합


#설계 #모듈 #아키텍처
> 종속성: `#OOP` `#언어독립`

---

## 19. Law of Demeter (디미터 법칙)

_메서드는 (자신의 필드 / 파라미터 / 자신이 생성한 객체 / 자신)의 메서드만 호출. `a.b.c.d()` 같은 체인 호출은 중간 레이어에 *구조 의존*을 만든다._

**왜 본인이 이렇게 다루는가**
Law of Demeter가 강조하는 비용은 *결합도* — `manager.GetPlayer().GetStats().Attack`에서 Manager, Player, Stats 내부 구조 3개에 의존. Player 내부가 바뀌면 이 호출자도 수정 필요. 반면 `manager.GetPlayerAttack()` 위임은 의존이 1개.

단, UI 4축 구조에서 View→Controller 데이터 조회는 예외를 허용한다. Binder가 Controller의 모든 속성을 위임 메서드로 래핑하면 Binder가 비대해지고 위임 메서드가 폭발한다. *위임 메서드 폭증을 만들면서까지 강요하지 않는다*.

기준:
- **적용**: 도메인 서비스 간 호출 — target 내부 구조 직접 탐색 금지, Manager 위임 메서드 사용
- **적용**: Manager 간 호출 — `runManager.GetSynergyBonus()` 위임, 내부 SynergyService 직접 접근 금지
- **비적용 허용**: View가 Controller/Binder 데이터를 체인으로 읽는 경우 — 위임 메서드 폭증이 더 비쌈
- **비적용 허용**: 데이터 객체(struct, POCO) 필드 접근 체인 — `config.damage.base`처럼 *데이터 컨테이너*는 로직 캡슐화 대상이 아님

**적용 사례**
- **적용**: `RunManager.GetTotalDamage()` — 내부에서 `_battleService.GetBase() * _synergyService.GetBonus()`. 외부 호출자는 `manager.GetTotalDamage()` 1단계만
- **비적용 (데이터 체인)**: `weaponData.stats.damage` — WeaponDataSO 안의 중첩 struct. 강제하면 `weaponData.GetDamage()` 래퍼 폭발. struct 데이터 체인은 실용적 예외
- **회색지대 (UI 4축)**: `_controller.Items[i].Name` — Binder가 Controller Items에 접근해 Name 읽기. 위임 래퍼 추가하면 불필요한 API 폭발. 실용적으로 허용

**오용 / 반대 원칙**
- 짝 원칙: **Tell, Don't Ask**(항목 21) — Law of Demeter의 *동작 위임* 측면을 강조한 표현
- 오용: "체인이 보이면 무조건 래퍼 추가" → 모든 중간 객체에 위임 메서드 추가 → API 폭증 + 얇은 wrapper proliferation
- 검출: 호출 체인 깊이 > 2인 *도메인 로직* 호출이 반복되면 래핑 검토. *데이터 접근*은 깊이가 있어도 묵인


#설계 #코드 #결합도
> 종속성: `#언어독립` `#OOP`