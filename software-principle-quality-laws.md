# 소프트웨어 원칙 — 코드품질·법칙

> 상위 노트: [[software-principle-notes]] (전체 인덱스 디스패처)
> 다루는 축: 코드품질·안티패턴·법칙
> 다루지 않는 축: [[software-principle-simplicity|소프트웨어 원칙 — 단순성]] / [[software-principle-design|소프트웨어 원칙 — 설계]]

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

# 풀노트

## 29. CQS (Command-Query Separation)

_메서드는 *명령*(상태 변경, void 반환)이거나 *쿼리*(상태 조회, 값 반환) 중 하나. 단, `EndBatch` 같은 패턴은 원자성이 목적인 *의도된 위반*으로 허용._

**왜 본인이 이렇게 다루는가**
CQS의 가치는 *예측 가능성* — 쿼리를 호출해도 상태가 바뀌지 않으므로 호출 순서가 무의미하고 테스트가 단순. `GetCurrentGrade()`를 여러 번 불러도 결과가 같고 부작용이 없음을 기대.

의도된 위반 기준: 비즈니스 로직의 원자성이 필요할 때. `EndBatch()`는 "배치 종료 + 이벤트 발화"를 분리하면 외부 호출자가 두 단계를 직접 관리해야 해서 race가 발생. "명령+통지"가 원자적이어야 하는 경우.

기준:
- **준수**: Service의 `GetX()` 메서드는 순수 쿼리, 상태 무변경
- **준수**: `ApplyDamage(target, amount)` 명령, void 반환
- **의도된 위반 허용**: `EndBatch()` — 명령(batchActive=false) + 통지(이벤트 발화). 분리가 race를 만들기 때문
- **의도된 위반 허용**: `GetOrCreate(key)` — Dictionary에서 없으면 생성 후 반환. 조회와 생성의 원자성이 필요

**적용 사례**
- **준수**: `SynergyService.GetActiveCount()` — 현재 활성 시너지 수 반환, 상태 무변경
- **준수**: `GachaService.Roll()` — 명령이므로 GachaResult 반환은 CQS 정합. "명령의 직접 출력값"으로 해석 (Bertrand Meyer 원문도 예외 허용)
- **의도된 위반**: `RunManager.EndQueueBatch()` — 배치 완료 + OnQueueChanged 발화. [[game-misc-notes]] 항목 6에 documented
- **위반 주의**: `GetNextEnemy()` 내부에서 index 증가 — CQS 위반이자 side-effect 있는 쿼리. 분리 권장: `PeekNextEnemy() + AdvanceEnemyIndex()`

**오용 / 반대 원칙**
- 오용: "CQS 위반이므로 무조건 분리" → `GetOrCreate` 같은 원자성 필요 패턴을 두 메서드로 나누면 caller가 두 단계 직접 관리 → race
- 짝 원칙: **POLA**(항목 27) — CQS를 지키면 메서드 이름만으로 부작용 유무가 자명해져 POLA 달성
- 검출 신호: `GetX()` 내부에 `_state = ...` 또는 이벤트 발화 → 의도된 위반인지 확인. 의도된 위반은 이름을 `Apply/Execute/EndBatch`로 바꿔 명시


#설계 #구현 #코드
> 종속성: `#언어독립` `#OOP`

---

## 32. SLAP (Single Level of Abstraction Principle)

_한 메서드 내 모든 호출이 같은 추상화 레벨이어야 함. 고수준 의도와 저수준 구현이 섞이면 SLAP 위반._

**왜 본인이 이렇게 다루는가**
SRP(항목 9)가 *클래스 단위*의 책임 분리라면 SLAP은 *메서드 단위*의 추상화 통일. 한 메서드 안에 "Begin 호출" + "for 루프로 인덱스 계산" + "UI 텍스트 직접 설정"이 섞이면 — 읽는 사람이 *어느 레벨에서 사고해야 할지* 매번 전환해야 함. ShopController 700행은 *클래스 책임 과다*(SRP)도 문제였지만, 각 메서드 내부에 *모든 추상화 레벨이 혼재*한 SLAP 위반이 코드 회상 비용의 주범.

**적용 사례**
- **ShopController 코디네이터화** (idea-notes 항목 16): 코디네이터의 OnDraw() 메서드는 *sub-Controller 호출* 한 레벨만(`itemSlot.Refresh(); usableSlot.Refresh(); benchSlot.Refresh();`). 각 sub의 Refresh 내부에 *저수준 구현*. 호출 그래프가 트리 형태로 정리되어 어느 레벨에서 디버깅할지 명확
- **batch 패턴** (idea-notes 항목 13): `BeginQueueBatch() { batchActive = true; batchDirty = false; }` — 메서드 내부가 *플래그 설정* 한 레벨만. dispatch는 EndQueueBatch가 별도
- **Sequence vs Controller**: Sequence는 *연출 step* 레벨(WaitForSeconds, DOTween 호출), Controller는 *비즈니스 의도* 레벨(StartSequence(), OnSequenceEnd) — 레벨 분리가 SLAP의 클래스 분리 사례

**오용 / 반대 원칙**
- 짝 원칙: **SRP**(항목 9), **Separation of Concerns**(항목 22) — SLAP는 SRP의 메서드 버전
- 검출 신호: 한 메서드의 본문을 위에서 아래로 읽었을 때 *추상화 사다리를 오르락내리락*하는 느낌 = 위반. 정합 메서드는 *수평 이동*만
- 오용 가능 지점: 모든 메서드를 SLAP 강제 시 *얇은 wrapper 메서드 폭발*. 임계는 "메서드가 3+ 레벨을 동시에 다룬다" 시점부터 분리


#설계 #코드 #리팩토링
> 종속성: `#언어독립` `#OOP`

---

## 38. Make Illegal States Unrepresentable

_잘못된 상태를 *컴파일 단계*에서 표현 불가능하게 — Yaron Minsky. 런타임 검증 대신 타입 시스템 활용._

**왜 본인이 이렇게 다루는가**
런타임 가드(if-null check, 범위 체크)는 *호출자가 잊을 가능성*이 있음. 타입으로 강제하면 *컴파일 안 됨* → 잊을 수 없음. C#의 타입 시스템 + Unity 직렬화 시스템을 활용하면 게임 도메인에서도 적용 가능. 다만 모든 상태에 적용 시 타입 폭발 → *silent corruption 위험이 큰 영역*에 선별 적용.

**적용 사례**
- **SynergyEffectType enum 정수값 영구 점유** (idea-notes 항목 18): 폐기된 enum 멤버의 정수값을 *재사용 금지*. SO YAML에 잔존 정수값이 다른 의미로 매핑되어 silent corruption 발생하는 함정 차단. 컴파일 시점에 강제는 아니지만 *명시 룰 + 코드 리뷰*로 동등 효과
- **SerializeReference 자식 인스턴스 deep clone** (idea-notes 항목 8): 같은 SerializeReference 인스턴스를 두 SO가 공유하면 한쪽 수정이 다른 쪽에 silent 전파. clone 강제로 *공유 불가능한 상태* 표현
- **string ID → SO 직접 참조** (idea-notes 항목 19): 인스펙터 wiring에서 *유효한 SO만 받을 수 있는 타입*으로 강제 — 오타로 인한 빈 문자열 자체가 컴파일/직렬화 단계에서 차단

**오용 / 반대 원칙**
- 짝 원칙: **Parse, Don't Validate**(항목 39) — 동일 철학의 함수형 표현
- 짝 원칙: **Design by Contract**(항목 30) — precondition을 타입으로 인코딩
- 오용 가능 지점: 모든 상태를 타입으로 표현하면 *제네릭 폭발*. 임계는 "런타임 가드 실패 시 silent corruption" 영역에만 적용. 단순 입력 검증은 Fail Fast(항목 25)로 충분
- C# 한계: discriminated union 없음 → enum + visitor 패턴 또는 sealed class hierarchy로 우회. F#/Rust보다 비용 큼


#설계 #타입 #코드
> 종속성: `#타입시스템` `#OOP`

---

## 42. Hyrum's Law

_"With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." — Hyrum Wright._

**왜 본인이 이렇게 다루는가**
1인 개발 + AI 협업이라 *외부 사용자*는 없지만 — *AI*와 *미래의 자신*이 사용자. 명시되지 않은 동작도 *코드의 기대로 굳어진다*는 인식이 ADR History timeline + Plan followup 룰의 동기. 예를 들어 RunManager.OnQueueChanged 이벤트의 *발화 시점*(즉시 vs batch end)을 명시 안 하면, 구독자가 *과거 발화 시점*에 의존하는 코드를 작성 → 시점 변경 시 silent 회귀.

**적용 사례**
- **ADR History timeline** 룰: 결정 번복·동작 변경은 반드시 History timeline에 1줄 추가. *명시되지 않은 과거 동작*이 새 동작으로 바뀔 때 *왜 바뀌었는지* 회상 가능
- **Plan followup 짝**: 가정 차이/누락은 즉시 수정이 아니라 followup에 누적. *수정 시점*에 *기존 동작에 의존한 코드*가 있는지 검토 후 진행
- **batch 패턴 도입**(idea-notes 항목 13): RunManager.OnQueueChanged의 발화 시점을 *명시적으로 batch end*로 변경 시, 기존 구독자 중 *즉시 발화 가정*에 의존한 코드가 있는지 grep으로 전수 확인 후 진행 — Hyrum's Law 회피 절차
- **AI 협업 적용**: AI에게 "현재 동작에 의존한 코드가 있을 수 있다" 인식을 plan에 명시. AI는 변경 영향 범위 추정 시 *명시된 contract*만 보는 경향이 있어, *observable behavior* 의존성을 놓치기 쉬움

**오용 / 반대 원칙**
- 짝 원칙: **Chesterton's Fence**(항목 35) — *이유 모르는 동작*은 의존이 있을 수 있다는 인식
- 짝 원칙: **POLA**(항목 27) — 호출자가 *놀라는* 동작 = *기존 동작에 의존*했다는 신호
- 오용 가능 지점: Hyrum's Law를 *완벽 보존*으로 해석하면 *어떤 변경도 위험*해져 stagnation. 임계는 "변경의 의도 > 의존 비용"일 때 진행 + History timeline 명시


#팀워크 #관찰 #프로세스
> 종속성: `#언어독립` `#팀워크`

---

## 43. Postel's Law (Robustness Principle)

_"Be conservative in what you send, be liberal in what you accept." — Jon Postel. 보낼 때는 엄격한 형식, 받을 때는 관대한 파싱._

**왜 본인이 이렇게 다루는가**
호출자(보내는 쪽)는 *형식 보장*으로 받는 쪽의 가드 부담 ↓, 받는 쪽은 *관대한 파싱*으로 호환성 ↑. 게임 도메인에서는 (a) SO 매핑 빌드처럼 *사용자(디자이너)가 인스펙터로 데이터 입력*하는 경계와 (b) 도메인 객체 간 호출 경계가 다름 — 전자에는 Postel's Law, 후자에는 Design by Contract(항목 30) 적용.

**적용 사례 (적용 + 비적용 분리)**
- **적용 (보낼 때 보수적)**: Service 시그니처는 엄격한 타입(`ItemDataSO`, `int amount`) — null/0 입력 시 호출자 오류로 throw. SO 매핑 빌드는 IsNullOrEmpty 가드(idea-notes 항목 19) — 빈 entry는 silent skip + LogWarning
- **적용 (받을 때 관대)**: Effect 객체 Apply에서 대상이 null이어도 silent return — 효과 발동 타이밍에 대상이 *제거된 상태*일 수 있음(코루틴 지연). LogWarning 없이 종료
- **적용 (받을 때 관대)**: 인스펙터 wiring 시점에 SO 매핑 entry가 비어있으면 빌드 단계에서 skip + LogWarning — 디자이너가 wiring을 빠뜨려도 게임이 죽지 않음
- **비적용**: Service 간 호출은 Design by Contract(항목 30) 적용 — 호출자가 precondition 위반 시 ctor throw. *내부 호출에는 관대함이 silent 버그 양산*

**오용 / 반대 원칙**
- 반대 원칙: **Fail Fast**(항목 25) — 내부 호출에는 Fail Fast가 정합, *외부 경계*에만 Postel's Law
- 짝 원칙: **Defensive Programming**(항목 33) — 본인이 채택 안 한 원칙. Postel's Law의 "받을 때 관대"가 *전 경계 적용*되면 Defensive Programming의 보일러플레이트 비대로 변질
- 현대 비판: HTTP/HTML 등 *프로토콜* 영역에서는 Postel's Law가 *불일치 누적 → 호환성 지옥*을 야기. 본 원칙은 *호출 경계*에서는 유효하나 *프로토콜 표준*에는 부적합 (RFC 9413 권장 폐기). 게임 도메인은 *외부 디자이너 입력* 경계라 적합
- 오용 가능 지점: 모든 입력에 관대함 적용 시 silent 데이터 손상 — 디자이너가 *잘못된 데이터 입력*해도 게임이 동작해버려 발견 지연. LogWarning 강제로 *관대함의 가시화* 필요


#구현 #코드 #아키텍처
> 종속성: `#언어독립`