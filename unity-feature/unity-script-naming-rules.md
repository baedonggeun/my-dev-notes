# Unity 스크립트 네이밍 규칙

## UI 3축

> View + UIBinder를 Binder 단일 접미사로 통합. 4축 → 3축.

### Binder

| 항목 | 내용 |
|------|------|
| **역할** | SerializeField 참조 보유 + `Bind(data)` setter + 이벤트 구독 후 UI 갱신 |
| **배치** | 해당 UI 요소 또는 패널에 직접 부착 |
| **기반** | `BinderBase` 상속 — OnEnable: Subscribe → SyncState / OnDisable: Unsubscribe |
| **허용** | `[SerializeField]` 참조 보유, `Bind(data)` setter(파라미터 → 필드 직접 대입), 이벤트 구독(소스 제한 없음 — Manager/Controller/static/버튼 onClick), 핸들러 내에서 setter 호출 또는 Controller 메서드 호출 |
| **금지** | 이벤트 핸들러 내 비즈니스 로직 inline, Manager 상태 직접 변경, 연출 코드(DOTween/WaitForSeconds) |

**Binder vs Sequence 경계**

```
타이밍 없는 즉각 SetActive / 색상 변경  →  Binder
타이밍 있는 연출 (Lerp / DOTween / 딜레이)  →  Sequence
```

---

### Controller

| 항목 | 내용 |
|------|------|
| **역할** | 도메인 로직, 상태 판단, Sequence 트리거, 이벤트 발화 |
| **배치** | Manager 하위 오브젝트 또는 도메인 패널 직부착 |
| **허용** | 로직 코루틴(흐름 제어 목적), `sequence.Play(data, onComplete)` 호출, Manager/Service 쿼리, 이벤트 발화 |
| **금지** | DOTween/Animator 직접 제어, WaitForSeconds(시각 딜레이 목적), Image/Text/SetActive 직접 호출 |

**TooltipBase 상속 시 추가 제약**

Controller 접미사를 유지하되 TooltipBase를 상속한 클래스는 표시/숨김/바인딩만 허용. 게임 로직, 상태 머신, Manager 깊은 참조 금지.

---

### Sequence

| 항목 | 내용 |
|------|------|
| **역할** | 타이밍 기반 시각 연출 전담 |
| **배치** | Controller와 같은 GameObject, UI prefab 위, Manager 하위 모두 허용 |
| **허용** | DOTween/Animator, SetActive(연출 목적), CanvasGroup.alpha, WaitForSeconds/연출 코루틴, Binder getter로 RT 참조 |
| **금지** | 비즈니스 로직, Manager 상태 변경(데이터 쓰기), Manager 직접 읽기(파라미터로만 수신), FlowRequest/GameManager.RequestTransition 직접 호출(onComplete 콜백 사용) |

---

## 인프라 접미사 12종

### Manager

- MonoSingleton 진입점, Service 컴포지션, 도메인 이벤트 발화, FSM hook
- **UI 조작 화이트리스트** (4개만 허용): `UIManager / TooltipManager / AnimationManager / AudioManager`
- 금지: View 참조 보유(화이트리스트 외), 도메인 setter 체이닝, 비즈니스 로직 본문 비대(Service 분리)
- 회색: 다른 도메인 Manager 읽기 호출 — 즉시 정리 의무 없음

### Service

- 비즈니스 로직 전담, POCO (MonoBehaviour 미상속)
- Manager가 ctor 또는 메서드 인자로 의존 주입
- Reset/Dispose 대칭 필수
- 금지: 외부 Manager.Instance 직접 참조
- 회색: 부모 Manager.Instance 역참조 — 즉시 정리 의무 없음

### State

- FSM 노드: Enter / Update / Exit + FlowDirector 전환 요청
- 금지: UI 직접 참조(UIManager 경유), 상태 데이터 보유(FSM 노드는 무상태)

### SO

- `[SerializeField]` 데이터 필드 + 순수 헬퍼 `Get*` 메서드
- 금지: 런타임 mutable 상태, Instance 패턴, Awake/Update 라이프사이클, Manager 호출

### Effect

- **Apply** (per-attack 수치 변경) + **Describe** (툴팁 텍스트) 2종, 효과 1종 책임
- Emit 없음 — 팝업/로그 발화는 호출자 Controller가 직접 처리
- 금지: 다중 효과 분기, UI 직접 호출, ctx 미주입 매니저 우회

### Entry

- POCO 데이터 + 헬퍼 getter
- 금지: 동작 메서드(Execute/Trigger), Manager 참조, 상태 변경 메서드

### Drawer *(기존 Pool)*

- 확률 기반 데이터 추첨 (등급 시프트 + 후보 균등 선택)
- POCO, `[Serializable]`, MonoBehaviour 미상속
- Initialize / Reset 대칭
- 금지: Manager.Instance 직접 참조, 게임 로직 분기

### Spawner

- 풀 등록/해제 + 큐 처리 코루틴 + OnDisable cleanup
- 코루틴 내 `try/finally` 필수 (silent 정지 deadlock 방지)
- 금지: 게임 로직, try/finally 부재

### Handler *(EventSystem 전용)*

- MonoBehaviour + `UnityEngine.EventSystems` 인터페이스 구현
- ResolveAction → Execute 위임 패턴
- 금지: 게임 로직 inline, UI 직접 조작

### Dispatcher *(기존 Domain Action Handler)*

- `static class` + 단일 진입점 (`Execute` / `Apply`)
- Manager 내 Service 다중 조작 디스패처 (switch 분기 또는 단발 발동)
- 금지: 다중 도메인 조작, 필드 setter 체이닝

### Spec

- 여러 소스 합산 최종값의 materialized 컨테이너
- `struct`, read-only, push 갱신

**도입 체크리스트** — 3개 모두 YES일 때만 도입

| # | 조건 |
|---|------|
| ① | modifier 소스가 **3개 이상** |
| ② | **2개 이상의 독립 클래스**가 같은 최종값을 읽음 |
| ③ | 소스들이 **서로 다른 타이밍**에 변경됨 (단일 이벤트로 cover 불가) |

1개라도 NO → Calculator만 두거나 inline 계산

### Calculator

- Spec 산출 전용 `static` pure function 모음
- 외부 상태 의존 0, 사이드 이펙트 금지
- Spec 도입 조건 충족 시에만 짝으로 도입

---

## 단발 패턴 6종

| 접미사 | 기준 | 신규 도입 |
|--------|------|:---------:|
| **Base** | 추상 기반 클래스 — 직접 인스턴스화 불가, 상속 전용 | ✓ |
| **Core** | FSM 내부 핵심 상태 머신 컨테이너 | ✗ FSM 전용 봉인 |
| **Director** | FSM 전환 조율자 | ✗ FSM 전용 봉인 |
| **RaycastMask** | `ICanvasRaycastFilter` 구현 전용 — `IsRaycastLocationValid` 재정의만 허용 | ✓ |
| **Detector** | EventSystem 인터페이스 구현 + 조건 감지 후 이벤트 발화만 (로직 없음) | ✓ |
| **Router** | 조건 기반 분기 — 어느 패널/경로로 보낼지 결정. Binder 상속 허용 | ✓ |

**Detector vs Handler 구분**

- **Handler**: 이벤트 수신 → 도메인 로직 실행 또는 위임
- **Detector**: 이벤트 수신 → 조건 감지 → 이벤트 발화만 (로직 없음)

---

## 자가 점검 룰

- 새 클래스 작성 / 리네이밍 시 위 표 자가 점검
- 위 표에 없는 접미사가 필요하면 **표 확장 + ADR 신설**. 즉흥 명명 금지
- Manager UI 조작은 화이트리스트 4개 외 전면 금지
- Spec/Calculator는 도입 체크리스트 3개 통과 시에만 도입
