# 디자인 패턴 노트

> 다루는 축: 코드 구조 패턴 (GoF + 아키텍처). 재사용 가능한 *관계*의 추상화
> 다루지 않는 축: 게임 특화 기법(→ [[game-technique-notes]]), 단편 트릭(→ [[game-misc-notes]])
> 적용 범위: 대부분 언어/엔진 독립 (OOP 또는 FP 기반)
> 관련 노트: [[game-misc-notes]] (단편 트릭, 패턴 승격 후보)
> 평생 노트 정책: 인덱스 표는 portable, 풀노트는 구현 의사코드 포함
> 승격 임계치: 풀노트 항목이 카테고리당 8개 이상 시 분리 검토
> 풀노트 작성 기준 (둘 이상 해당 시):
>   - 코드만 봐선 "왜 이렇게 했는지" 안 보이는 정성적 이유가 있다
>   - 다른 프로젝트/맥락에서도 재사용 가능한 일반 원리다
>   - 자주 잊는 함정/엣지케이스가 있다
>   - 응용 사례가 3개 이상이다
> 작성 시작: 2026-05-15

---

## 태그 목록

### GoF 분류
- `#생성` `#구조` `#행위`

### 아키텍처 분류
- `#아키텍처` `#계층` `#서비스` `#이벤트` `#상태머신`

### 적용 레벨
- `#엔티티` `#시스템` `#씬` `#전역`

### 의도/효과
- `#결합도감소` `#재사용` `#확장성` `#테스트용이` `#성능` `#보일러플레이트감소`

### 구현 매체
- `#C#이벤트` `#인터페이스` `#상속` `#컴포지션` `#ScriptableObject`

---

## 인덱스

| # | 패턴 | 분류 | 한 줄 요약 | 종속성 |
|---|------|------|----------|--------|
| 1 | HFSM (Hierarchical State Machine) | `#행위` `#상태머신` | 상태가 계층으로 중첩되어 부모가 자식 그룹을 통제하는 상태머신 | `#OOP` `#언어독립` |
| 2 | Singleton | `#생성` `#전역` | 인스턴스를 전역에서 단 하나만 보장 (라이프사이클 관리 권장) | `#OOP` `#언어독립` |
| 3 | Service Locator | `#아키텍처` `#서비스` | 서비스 인스턴스를 키로 조회하는 중앙 레지스트리 | `#OOP` `#언어독립` |
| 4 | State (Enter/Exit + 브로드캐스트) | `#행위` `#상태머신` | Enter/Exit 훅으로 상태 전이 캡슐화 + 옵저버 통지 | `#OOP` `#언어독립` |
| 5 | Service Layer 분리 (Service ↔ Manager) | `#아키텍처` `#계층` | 비즈니스 로직(Service)과 라이프사이클(Manager)을 별도 계층으로 | `#아키텍처` `#언어독립` |
| 6 | Template Method | `#행위` `#상속` | 부모가 알고리즘 골격, 자식이 훅 메서드 오버라이드 | `#OOP` `#상속` |
| 7 | Strategy | `#행위` `#확장성` | 동일 시그니처 알고리즘을 객체/함수로 캡슐화해 런타임 교체 | `#OOP` `#FP` `#언어독립` |
| 8 | Facade | `#구조` | 복잡한 서브시스템에 단순화된 인터페이스 제공 | `#OOP` `#언어독립` |
| 9 | Memento | `#행위` | 객체 상태를 외부에 노출 없이 캡쳐/복원 | `#OOP` `#언어독립` |
| 10 | Command | `#행위` | 요청을 객체로 캡슐화해 큐잉/실행 취소 가능 | `#OOP` `#FP` `#언어독립` |
| 11 | Adapter | `#구조` | 호환되지 않는 인터페이스를 클라이언트 기대 형태로 변환 | `#OOP` `#언어독립` |
| 12 | Chain of Responsibility | `#행위` `#이벤트` | 요청을 핸들러 체인으로 전달, 각자 처리 또는 다음으로 위임 | `#OOP` `#언어독립` |
| 13 | Decorator | `#구조` | 객체를 같은 인터페이스의 wrapper로 감싸 동적으로 책임 추가 | `#OOP` `#언어독립` |
| 14 | Factory | `#생성` | 객체 생성 로직을 별도 메서드/클래스로 분리 | `#OOP` `#언어독립` |
| 15 | Composite | `#구조` | 단일 객체와 객체 집합을 동일 인터페이스로 다룸 | `#OOP` `#언어독립` |
| 16 | Observer | `#행위` `#이벤트` | 주체가 상태 변경을 구독자에게 통지 (정적/인스턴스 이벤트) | `#OOP` `#FP` `#언어독립` |
| 17 | Callback | `#행위` | 함수를 인자로 전달해 시점이 다른 코드 실행 | `#OOP` `#FP` `#언어독립` |
| 18 | Object Pooling | `#생성` `#성능` | 객체를 재사용 풀로 관리해 GC/생성 비용 절감 | `#OOP` `#언어독립` |
| 19 | CRTP (Curiously Recurring Template Pattern) | `#생성` `#구조` | `class Foo<T> where T : Foo<T>` — 부모가 자식 타입을 알아 타입 안전성 강화 (MonoSingleton 등) | `#OOP` `#제네릭` |
| 20 | DI (Dependency Injection) | `#아키텍처` `#서비스` `#결합도감소` `#테스트용이` | 의존성을 외부에서 *주입*받아 결합도 ↓ — Service Locator(#3)와 반대 방향(pull vs push) | `#OOP` `#언어독립` |
| 21 | Domain-Scoped Injection Interface | `#아키텍처` `#인터페이스` `#테스트용이` | 단일 `IInjectable` 대신 도메인별 분리(`IMonsterInjectable`, `IItemInjectable` 등) — 잘못된 인젝터/대상 결합 컴파일 타임 차단 + 도메인 단위 mock 테스트 | `#OOP` `#언어독립` |
| 22 | Streaming Pattern (영역 토글 / 거리 링) | `#아키텍처` `#성능` | 플레이어 주변만 활성화해 비가시 영역의 CPU·GPU 비용 절감. 원형은 단일 영역 SetActive 토글, 확장형은 거리 링(Active/Warm/Unload) + Pool + Addressables | `#게임엔진일반` |
| 23 | 단일 이벤트 + 추상 Entry 디스패치 | `#행동` `#이벤트` | `Action<TBase>` 단일 이벤트 + abstract base class로 이종 데이터를 하나의 채널로 발행 — 수신자는 다형성으로 처리, 종류 추가 시 이벤트/수신자 변경 없이 entry 서브클래스만 추가 | `#OOP` `#언어독립` |

---

## 항목별 노트
*풀 4블록 노트는 요청 시 작성. 위 인덱스 표가 SOT.*

---

## 22. Streaming Pattern (영역 토글 / 거리 링)

**한 줄 요약**
플레이어 주변만 활성화하고 멀리 있는 오브젝트는 비활성/언로드해서 비가시 영역의 CPU·GPU·메모리 비용을 절감하는 공간 단위 라이프사이클 패턴.

**설명**
씬의 모든 NPC/적/장식이 매 프레임 Update/물리 시뮬을 돌면 비용이 누적된다. 시야 밖에서는 시뮬레이션이 무의미하므로, 플레이어 위치 기준으로 "활성 영역"을 정의하고 그 안에 들어온 오브젝트만 살린다.

구현 복잡도에 따라 두 단계로 나눠 사용:

**원형 (Single-area Toggle)** — 작은 2D 씬, 액터 수 수십~수백 개:
- 단일 사각/원형 영역 vs `inside/outside` 이분
- 활성: `SetActive(true)` / 비활성: `SetActive(false)` + 위치 리셋
- Pool/Addressables 없음 — 씬에 모두 인스턴스화된 상태로 토글만
- 장점: 즉시 구현 가능, 디버깅 쉬움 / 단점: 액터 수만큼 메모리 상주

**확장형 (Distance Ring + Pool + Addressables)** — 오픈월드/대규모 맵:
- 거리 다단계: `Active`(시뮬) / `Warm`(인스턴스 살아있되 일시정지) / `Unload`(언로드)
- Pool로 인스턴스 재사용 → GC 압력 ↓
- Addressables로 에셋 자체를 메모리에서 내림 → 메모리 풋프린트 ↓
- 장점: 거의 무제한 콘텐츠 / 단점: 경계 전이 시 히치, 상태 관리 복잡

**구현 (원형 — Revenge 실구현)**
```
// StreamAreaWatcher (플레이어 자식, BoxCollider2D area)
void Awake():
    groups = FindObjectsByType<PatrolPointGroup>()  // 한 번만 캐시

void Update():
    bounds = area.bounds
    for g in groups:
        inside = bounds.Contains(g.position)
        g.SetActive(inside)

// PatrolPointGroup
void SetActive(bool active):
    if IsActive == active: return
    if not active:
        ResetPosition()   // 다음 진입 대비
    IsActive = active
    controlledObject.SetActive(active)
```

**구현 (확장형 의사코드)**
```
// 거리 링 — 매 프레임/N프레임마다
for chunk in chunks:
    d = distance(player, chunk)
    if d < ACTIVE_RADIUS:
        chunk.state = Active     // Update on
    elif d < WARM_RADIUS:
        chunk.state = Warm       // 인스턴스 유지, Update off
    else:
        chunk.state = Unload     // pool.Release + addressable.Release

// 상태 전이 시
on Active: pool.Get + addressable.LoadAsync (히치 회피용 prefetch는 Warm 진입 시점)
on Warm:   gameObject.SetActive(false)
on Unload: pool.Release; addressable.Release
```

**주의점**
- **원형 → 확장형 점프 금지** — 액터 수십 개 게임에서 거리 링 + Pool + Addressables는 명백한 오버엔지니어링. 액터 수 + 프레임 부담 측정 후 확장
- **위치 리셋 의도** — 원형에서 비활성 시 위치를 리셋하지 않으면 플레이어가 다시 영역에 들어왔을 때 액터가 "마지막 위치"에 남아 부자연스러움. 순찰/스폰 의도면 리셋 필수
- **경계 진동 (boundary thrash)** — 경계 근처에서 액터가 빠르게 in/out을 반복하면 `SetActive` 토글이 매 프레임 발생. 히스테리시스(inside/outside 임계 거리 분리) 또는 N프레임 디바운스 필요
- **확장형 비동기 함정** — Addressables 로드 완료 전에 다른 상태로 전이되면 핸들 누수. `AsyncOperationHandle`을 chunk에 보관 + Release 시 명시적 해제
- **Find 비용** — `FindObjectsByType`는 무겁다. 원형에서도 Awake 한 번이지만 동적 스폰이 있으면 `OnSpawn`에서 명시적 등록으로 전환
- **물리 비용은 SetActive로 충분히 줄지 않음** — 정적 콜라이더는 SetActive(false)로 사라지지만, 매 프레임 충돌 검사 자체가 없는 layer 분리가 더 효과적인 경우 있음

**메타**
- 종속성: `#게임엔진일반` (Unity, Unreal, Godot 모두 적용 가능)
- 관련 노트: [[design-pattern-notes]] #18 Object Pooling (확장형의 필수 구성요소)
- 첫 도출: Revenge (2026-05-15) — 원형만 구현. 확장형은 일반화 개념
- 적용 사례:
  - Revenge: StreamAreaWatcher + PatrolPointGroup (원형, BoxCollider2D + SetActive)
  - 확장형: 미구현 (오픈월드 프로젝트 시 후보)
- 태그: `#아키텍처` `#성능` `#시스템` `#씬`

---
