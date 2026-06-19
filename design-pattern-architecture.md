# 디자인 패턴 노트 — 아키텍처 패턴

> 상위 노트: [[design-pattern-notes]] (전체 인덱스 디스패처)
> 다루는 축: 시스템 수준 설계: 계층 분리·의존성 관리·스트리밍·데이터 조직
> 다루지 않는 축: 행위 패턴 / 생성·구조 패턴

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


# 인덱스

| # | 패턴 | 분류 | 한 줄 요약 | 종속성 |
|---|------|------|----------|--------|
| 3 | Service Locator | `#아키텍처` `#서비스` | 서비스 인스턴스를 키로 조회하는 중앙 레지스트리 | `#OOP` `#언어독립` |
| 5 | Service Layer 분리 (Service ↔ Manager) | `#아키텍처` `#계층` | 비즈니스 로직(Service)과 라이프사이클(Manager)을 별도 계층으로 | `#아키텍처` `#언어독립` |
| 20 | DI (Dependency Injection) | `#아키텍처` `#서비스` `#결합도감소` `#테스트용이` | 의존성을 외부에서 *주입*받아 결합도 ↓ — Service Locator(항목 3)와 반대 방향(pull vs push) | `#OOP` `#언어독립` |
| 21 | Domain-Scoped Injection Interface | `#아키텍처` `#인터페이스` `#테스트용이` | 단일 `IInjectable` 대신 도메인별 분리(`IMonsterInjectable`, `IItemInjectable` 등) — 잘못된 인젝터/대상 결합 컴파일 타임 차단 + 도메인 단위 mock 테스트 | `#OOP` `#언어독립` |
| 22 | Streaming Pattern (영역 토글 / 거리 링) | `#아키텍처` `#성능` | 플레이어 주변만 활성화해 비가시 영역의 CPU·GPU 비용 절감. 원형은 단일 영역 SetActive 토글, 확장형은 거리 링(Active/Warm/Unload) + Pool + Addressables | `#게임엔진일반` |
| 24 | 카테고리 SO 분리 vs 번들 SO (Domain Resource Split) | `#아키텍처` `#구조` `#재사용` `#컴포지션` `#ScriptableObject` | 아이템처럼 여러 도메인 정보(스탯·아이콘·애니메이션·SFX·이펙트)를 가진 데이터 자산을, 도메인별 SO + 매핑 테이블로 *분리*할지 / 하나의 완전체 SO로 *번들*할지의 선택. 변종 간 자원 공유 비율이 분기 기준 | `#OOP` `#언어독립` |

---

# 풀노트

## 3. Service Locator

_서비스 인스턴스를 타입 키로 조회하는 중앙 레지스트리. 의존성을 pull 방식으로 해소._

**직관**
전화번호부 — "IAudioService 주세요"라고 요청하면 등록된 구현체를 돌려줌. 사용자는 내부 구현이 누구인지 모름.

**문제 상황**
Singleton을 직접 참조하면 구체 타입이 고정돼 교체/테스트 불가:
```csharp
class Enemy
{
    void Die() { AudioManager.Instance.Play("death"); }
    //           ^^^^^^^^^^^^^^^^ 구체 타입 고정 — Mock 불가, 교체 불가
}
```
Service Locator는 인터페이스 키로 조회 → 테스트 시 Mock 등록으로 교체 가능:
```csharp
ServiceLocator.Register<IAudioService>(new MockAudioService()); // 테스트
ServiceLocator.Register<IAudioService>(new AudioService());     // 실제
// 사용처 코드는 동일
ServiceLocator.Get<IAudioService>().Play("death");
```

**설명**
```csharp
static class ServiceLocator
{
    static Dictionary<Type, object> _services = new();
    public static void Register<T>(T service) => _services[typeof(T)] = service;
    public static T Get<T>() => (T)_services[typeof(T)];
}

// 등록
ServiceLocator.Register<IAudioService>(new AudioService());
// 사용
ServiceLocator.Get<IAudioService>().Play("hit");
```

**DI(항목 20)와의 차이**

| | Service Locator | DI |
|---|---|---|
| 방향 | pull (사용자가 꺼냄) | push (컨테이너가 주입) |
| 의존성 명시 | 숨김 | 명시 (생성자/필드) |
| 테스트 | 전역 상태 교체 필요 | Mock 생성자 주입으로 충분 |
| Unity 적합성 | 높음 | 중간 (프레임워크 필요) |

**언제 쓰나 / 피할 때**
- ✅ DI 프레임워크 없이 인터페이스 기반 교체가 필요할 때
- ✅ Unity에서 전역 서비스를 Singleton보다 유연하게 관리할 때
- ❌ 의존성을 명시적으로 드러내야 할 때 — 숨은 의존성 문제 (DI(항목 20) 선택)
- ❌ 테스트 격리가 중요한 코드 — 전역 상태 오염 주의

⚠ **주의점**
- **숨은 의존성** — 클래스 생성자만 보면 어떤 서비스에 의존하는지 모름
- **미등록 서비스** — Get 시 `KeyNotFoundException`. NullService fallback 또는 TryGet 패턴 권장
- **테스트 격리** — 전역 딕셔너리이므로 테스트 간 상태 오염. teardown에서 Clear 필수


#아키텍처 #서비스 #전역
> 관련: [[design-pattern-notes]] 항목 2 Singleton (더 단순한 전역 접근), 항목 20 DI (push 방향 대안) | 종속성: `#OOP` `#언어독립`

## 5. Service Layer 분리 (Service ↔ Manager)

_비즈니스 로직(Service, 순수 C#)과 MonoBehaviour 라이프사이클(Manager)을 별도 클래스로 분리해 로직의 테스트 가능성을 확보._

**직관**
요리사(Service)와 홀 매니저(Manager) — 요리사는 요리 로직만, 매니저는 손님 응대와 주방 연결만 담당. 요리 레시피는 주방 밖에서도 테스트 가능.

**문제 상황**
비즈니스 로직이 MonoBehaviour 안에 있으면 단위 테스트 불가:
```csharp
class InventoryManager : MonoBehaviour
{
    List<ItemEntry> _items = new();
    public void AddItem(string id)
    {
        if (_items.Count >= MaxSlots) return;
        var data = Resources.Load<ItemDataSO>($"Items/{id}");
        _items.Add(new ItemEntry(data));
        // 이 로직을 테스트하려면 Unity 에디터에서 씬을 실행해야 함
    }
}
```
`AddItem` 로직을 순수 C# `InventoryService`로 분리하면 `new InventoryService(mockDb).AddItem("sword")` 형태로 단위 테스트 가능.

**설명**
```csharp
// Service — 순수 C#, new로 생성 가능 → 단위 테스트 가능
class InventoryService
{
    readonly ItemDatabase _db;
    List<ItemEntry> _items = new();
    public InventoryService(ItemDatabase db) { _db = db; }
    public void AddItem(string id) => _items.Add(new ItemEntry(_db.Get(id)));
}

// Manager — MonoBehaviour 껍데기, 의존성 구성 + 위임
class InventoryManager : MonoBehaviour
{
    [SerializeField] ItemDatabase itemDatabase;
    public InventoryService Service { get; private set; }
    void Awake() => Service = new InventoryService(itemDatabase);
}
```

**언제 쓰나 / 피할 때**
- ✅ 비즈니스 로직을 단위 테스트하고 싶을 때
- ✅ 같은 로직을 여러 MonoBehaviour에서 공유해야 할 때
- ❌ 메서드 3개 이하의 단순 Manager — 분리 오버헤드가 이득보다 큼
- ❌ Service에 코루틴/GetComponent가 필요한 경우 — 분리 의미 없음, Manager에 유지

⚠ **주의점**
- **Service에 MonoBehaviour 메서드 금지** — `StartCoroutine`, `GetComponent` 사용 시 분리 의미 없음. 코루틴이 필요하면 Manager에서 호스팅
- **분리 임계점** — 메서드 3개 이하면 Manager에 합쳐도 무방. 테스트/재사용 필요성이 보일 때 분리
- **Manager의 Facade 역할** — Manager가 Service 메서드를 그대로 위임 노출하면 Facade(항목 8) 겸임


#아키텍처 #계층 #서비스
> 관련: [[design-pattern-notes]] 항목 2 Singleton (Manager 구현 매체), 항목 8 Facade (Manager의 역할 겸임), 항목 20 DI (Service 의존성 주입) | 종속성: `#아키텍처` `#언어독립`

## 20. DI (Dependency Injection) + 생성자 주입

_객체가 의존성을 직접 생성/탐색하는 대신 외부에서 주입받아 결합도를 낮추고 테스트 가능성을 높이는 패턴. 세 가지 주입 방식 중 생성자 주입이 가장 명시적이고 권장._

**직관**
IKEA 가구 조립 — 나사를 직접 만들지 않고 외부에서 가져다 끼움. 나사 규격이 바뀌어도 조립 도면(클래스)은 그대로.

**문제 상황**
클래스 내부에서 `new SynergyService()`를 직접 생성하면 구체 타입이 고정 → Mock 교체 불가, 생성자 파라미터 변경 시 모든 사용처 수정 필요. 설명 내 코드 블록 참조.

**설명**
```csharp
// DI 없이 — 강결합
class BattleService { SynergyService _synergy = new SynergyService(); }  // 교체 불가

// 생성자 주입 — 의존성이 명시적 계약
class BattleService
{
    readonly IRunDataRepository _repo;
    readonly ISynergyService    _synergy;

    public BattleService(IRunDataRepository repo, ISynergyService synergy)
    {
        _repo    = repo;
        _synergy = synergy;
    }
}

var svc = new BattleService(new RunDataRepository(), new SynergyService()); // 실제
var svc = new BattleService(new FakeRepo(), new FakeSynergyService());       // 테스트
```

**세 가지 주입 방식 비교**:
| 방식 | 예시 | 의존성 가시성 | null 위험 | 언제 쓰나 |
|---|---|---|---|---|
| **생성자 주입** | `new Foo(dep)` | 명시적 (필수) | 없음 (`readonly`) | 필수 의존성 |
| **프로퍼티 주입** | `foo.Dep = dep` | 숨겨짐 (선택적) | 있음 | 선택적 의존성 |
| **메서드 주입** | `foo.Init(dep)` | 호출 시점 한정 | 있음 | 호출마다 다른 의존성 |

생성자 주입의 세 가지 이점:
1. **의존성이 명시적** — 클래스 선언만 봐도 "이걸 만들려면 뭐가 필요한지" 알 수 있다
2. **readonly 보장** — 생성 후 의존성 교체 불가 → 상태 예측 가능
3. **테스트 용이** — Mock/Stub을 주입하면 단위 테스트 가능

Unity에서는 `[SerializeField]`로 Inspector에서 참조를 끌어다 놓는 것도 프로퍼티 주입의 일종.

**Unity에서의 제약과 대안**

`MonoBehaviour`는 `new()`로 생성 불가 → 생성자 주입을 직접 쓸 수 없다.

```csharp
// 방법 1 — Initialize() 메서드 주입 (가장 흔한 Unity 패턴)
public class BattleUIBinder : MonoBehaviour
{
    private BattleService _battle;

    public void Initialize(BattleService battle)
    {
        _battle = battle;
    }
}

// 방법 2 — Service는 MonoBehaviour 미상속 → 생성자 주입 그대로 사용
public class SynergyService           // MonoBehaviour 상속 안 함
{
    private readonly IRunDataRepository _repo;
    public SynergyService(IRunDataRepository repo) { _repo = repo; }
}

// Manager(MonoBehaviour)가 Service를 생성할 때 주입
public class BattleManager : MonoSingleton<BattleManager>
{
    private SynergyService _synergyService;

    private void Awake()
    {
        // Manager가 의존성을 조립해서 Service에 주입
        _synergyService = new SynergyService(RunDataRepository.Instance);
    }
}
```

CasualStrategy의 구조가 정확히 이 패턴 — Manager는 MonoBehaviour 싱글턴, Service는 비MonoBehaviour이므로 Service는 생성자 주입 사용. Manager가 진입점이자 조립 지점 역할.

**언제 쓰나 / 피할 때**
- ✅ 테스트나 런타임 교체 가능성이 있는 의존성
- ✅ 의존성을 명시적으로 드러내야 할 때 (생성자가 계약 역할)
- ❌ 교체 계획이 전혀 없는 구체 클래스 — 인터페이스까지 만드는 것은 오버엔지니어링
- ❌ 생성자 파라미터 5개 이상 — DI가 아니라 클래스를 쪼개야 하는 신호

⚠ **주의점**
- **생성자 파라미터 폭발** — 의존성 5개 이상이면 SRP(software-principle 항목 9) 위반 신호. 책임 분리 필요
- **인터페이스 남발** — 교체/테스트 계획 없는 의존성에 인터페이스 만드는 것은 오버엔지니어링. 구체 클래스 직접 주입도 충분한 경우 많음
- **MonoBehaviour 메서드 주입의 타이밍** — `Initialize()`를 Awake/Start 어느 시점에 호출하느냐에 따라 의존성이 null인 채로 Update가 돌 수 있음. `Initialize` 미호출 시 guard 필요
- **Unity DI 프레임워크** — VContainer, Zenject 등이 있지만 간단한 프로젝트는 수동 DI(Manager → Service 패턴)로 충분. 프레임워크 도입은 의존성 그래프가 복잡해진 시점에 검토


#아키텍처 #서비스 #결합도감소 #테스트용이
> 관련: [[design-pattern-notes]] 항목 3 Service Locator (pull 방향 대안), 항목 5 Service Layer (Service를 주입받는 대표 패턴), 항목 21 Domain-Scoped Injection Interface, csharp-syntax-notes 항목 74~76 생성자/this()/base() (생성자 주입의 언어 기반) | 종속성: `#OOP` `#언어독립`

## 21. Domain-Scoped Injection Interface

_단일 `IInjectable` 대신 도메인별로 인터페이스를 분리(`IMonsterInjectable`, `IItemInjectable` 등)해 잘못된 의존성 결합을 컴파일 타임에 차단._

**직관**
업무 출입증 분리 — 개발팀 카드로는 서버실 못 들어가고, 서버실 카드로는 회의실 못 들어감. 잘못된 의존성 조합을 컴파일 타임에 차단.

**문제 상황**
단일 `IInjectable`에 모든 서비스를 넣으면 MonsterUI가 ItemService를 강제로 받아야 함. 설명 내 안티패턴 코드 참조.

**설명**
```csharp
// 안티패턴 — 단일 인터페이스
interface IInjectable
{
    void Inject(MonsterService m, ItemService i, AudioService a, ...);
    // 모든 클래스가 필요 없는 서비스도 받아야 함 → 결합도 폭발
}

// 도메인별 분리
interface IMonsterInjectable { void Inject(MonsterService s); }
interface IItemInjectable    { void Inject(ItemService s); }

class MonsterUI : IMonsterInjectable
{
    MonsterService _monsters;
    public void Inject(MonsterService s) { _monsters = s; }
}

// 주입기도 도메인별로
class MonsterDomainInjector
{
    void InjectAll(IMonsterInjectable[] targets, MonsterService service)
        => Array.ForEach(targets, t => t.Inject(service));
}
```

**언제 쓰나 / 피할 때**
- ✅ 도메인이 3개 이상이고 클래스마다 필요한 서비스가 다를 때
- ✅ 도메인 단위 Mock 테스트가 필요할 때
- ❌ 도메인 2개 이하 — 단일 IInjectable로 충분
- ❌ 모든 클래스가 동일한 서비스 세트를 필요로 할 때 — 분리 의미 없음

⚠ **주의점**
- **인터페이스 수 증가** — 도메인마다 인터페이스가 생기므로 도메인 3개 이하라면 단일 인터페이스도 무방
- **부분 구현 강제 안 됨** — 인터페이스 분리는 컴파일 타임 가이드일 뿐. 어떤 클래스에 어떤 인터페이스가 필요한지는 여전히 사람이 결정
- **Mock 테스트** — 도메인 단위로 Mock 생성 가능 → DI(항목 20) 대비 테스트 범위가 작아짐


#아키텍처 #인터페이스 #테스트용이
> 관련: [[design-pattern-notes]] 항목 20 DI (기반 패턴) | 종속성: `#OOP` `#언어독립`

## 22. Streaming Pattern (영역 토글 / 거리 링)

_플레이어 주변만 활성화하고 멀리 있는 오브젝트는 비활성/언로드해서 비가시 영역의 CPU·GPU·메모리 비용을 절감하는 공간 단위 라이프사이클 패턴._

**직관**
방에 들어갈 때만 조명 켜기 — 먼 방 조명을 굳이 켜둘 이유 없음. 플레이어 주변만 "살아있는" 영역으로 유지.

**문제 상황**
씬의 모든 오브젝트가 매 프레임 Update를 돌면 비가시 영역에서 CPU 낭비:
```
NPC 200마리 × Update() = 200 메서드 호출/프레임
카메라에서 50마리만 보임 → 150마리는 연산 낭비
물리 시뮬레이션도 비가시 영역까지 계산
```
플레이어 반경 내 액터만 SetActive(true) → 비가시 영역의 Update/물리 비용 0.

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

**언제 쓰나 / 피할 때**
- ✅ 동시 활성 액터 수 > 50, 비가시 영역이 클 때
- ✅ 모바일/저사양 타겟에서 CPU 예산이 빠듯할 때
- ❌ 액터 수 < 20 — SetActive 토글 비용 대비 이득 미미
- ❌ 단순 소규모 씬 — 확장형(Pool + Addressables) 선도입은 오버엔지니어링

⚠ **주의점**
- **원형 → 확장형 점프 금지** — 액터 수십 개 게임에서 거리 링 + Pool + Addressables는 명백한 오버엔지니어링. 액터 수 + 프레임 부담 측정 후 확장
- **위치 리셋 의도** — 원형에서 비활성 시 위치를 리셋하지 않으면 플레이어가 다시 영역에 들어왔을 때 액터가 "마지막 위치"에 남아 부자연스러움. 순찰/스폰 의도면 리셋 필수
- **경계 진동 (boundary thrash)** — 경계 근처에서 액터가 빠르게 in/out을 반복하면 `SetActive` 토글이 매 프레임 발생. 히스테리시스(inside/outside 임계 거리 분리) 또는 N프레임 디바운스 필요
- **확장형 비동기 함정** — Addressables 로드 완료 전에 다른 상태로 전이되면 핸들 누수. `AsyncOperationHandle`을 chunk에 보관 + Release 시 명시적 해제
- **Find 비용** — `FindObjectsByType`는 무겁다. 원형에서도 Awake 한 번이지만 동적 스폰이 있으면 `OnSpawn`에서 명시적 등록으로 전환
- **물리 비용은 SetActive로 충분히 줄지 않음** — 정적 콜라이더는 SetActive(false)로 사라지지만, 매 프레임 충돌 검사 자체가 없는 layer 분리가 더 효과적인 경우 있음


#아키텍처 #성능 #시스템 #씬
> 관련: [[design-pattern-notes]] 항목 18 Object Pooling (확장형의 필수 구성요소) | 종속성: `#게임엔진일반` (Unity, Unreal, Godot 모두 적용 가능)

## 24. 카테고리 SO 분리 vs 번들 SO (Domain Resource Split)

_아이템처럼 여러 도메인 정보(스탯·아이콘·애니메이션·SFX·이펙트)를 가진 데이터 자산을, 도메인별 SO + 매핑 테이블로 분리할지 / 하나의 완전체 SO로 번들할지의 선택. 자원이 *변종 간 공유*되면 분리, *1:1 고유*면 번들이 유리._

**직관**
마트 상품 vs 공유 포장재 — 상품 라벨(번들)은 각자 고유, 테이프/포장재(분리)는 창고에서 꺼내 여러 제품이 공유.

**문제 상황**
공유되는 자원을 모든 SO에 inline하면 변경 비용 폭발:
```
SwordA_SO: attackAnim = SwordSwing.anim  ← 동일
SwordB_SO: attackAnim = SwordSwing.anim  ← 동일 (× 21개)
// SwordSwing 교체 시 21개 SO 전부 수정 필요
```
`AnimationConfigSO`에 `weaponType → clip` 매핑을 분리하면 변경이 한 곳에서만.

**설명**
게임 데이터 자산은 보통 다음 도메인을 함께 가진다:

- Identity / Stats (스탯, 가격, 등급)
- Visual (아이콘, 심볼, 프리팹/모델)
- Audio (타격/획득/사용 SFX)
- Animation (사용 이펙트, VFX 클립)
- Effect / Behavior (능력 로직)
- Localization (이름/설명)

이를 한 SO에 모두 넣을지(번들), 도메인별 SO + 외부 매핑 테이블로 분리할지가 데이터 설계의 첫 분기점.

**(A) 카테고리 분리 + 매핑 (Category Split + Mapping)**
- `ItemDataSO`는 스탯·아이콘·식별자만 보유
- `AnimationConfigSO`/`AudioConfigSO` 등이 `itemId`(또는 `weaponType`, `grade`) → 자원 매핑 테이블 보유
- 자원은 별도 `ResourceSO`로 존재, 여러 아이템이 참조 공유
- 게임 업계의 마스터 데이터베이스 + 룩업 패턴 (Diablo/PoE, RPG Maker, 대부분 RPG)

**(B) 완전체 번들 (Bundled / All-in-One)**
- `ItemDataSO` 하나에 모든 필드 inline (icon, sfx, animClip, ...)
- 외부 매핑 테이블 불필요. SO 하나를 보면 그 아이템 전부 파악
- 디자이너 친화 (한 곳에서 편집)

**분기 기준 — 자원 종류별 통상 처리** (RPG/액션/카드 게임 업계 일반)

| 자원 종류 | 통상 처리 | 이유 |
|---|---|---|
| 스탯·숫자·식별자 | **번들** (아이템 SO에 inline) | 각 아이템마다 고유, 공유될 일 없음 |
| 아이콘 (Sprite) | **번들** (개별 참조) | 대부분 1:1, 같은 아이콘 공유 드묾 |
| 무기군 타격 애니메이션·SFX | **분리** (weaponType/category 매핑) | Sword/Bow/Staff 같은 *카테고리* 단위 공유 |
| 등급/희귀도 글로우 (Normal/Rare/Epic) | **분리** (grade 매핑) | 모든 Rare가 같은 빛 사용 |
| 시너지/세트 발동 이펙트 | **분리** (synergy/setId 매핑) | 시너지가 아이템보다 적음, 다대일 |
| 유니크 무기 전용 효과 | **번들** (해당 SO에 inline) | 그 아이템에만 존재 → 분리 의미 없음 |
| 능력/효과 로직 (Strategy) | 번들 + `SerializeReference` | 폴리모피즘 + inline 조합 |
| Localization 텍스트 | **별도 시스템** (Localization Table) | 언어×문자열 다대다, SO 외부 |

**판단 휴리스틱**: "이 자원이 *몇 개의 아이템*에 쓰이는가?"
- 1:1 (각 아이템 고유) → 번들
- 1:N (N≥3, 카테고리/등급/시너지 단위 공유) → 분리
- 또는 "디자이너가 이 자원 하나를 튜닝할 때 *한 군데에서* 하길 원하는가?"가 yes면 분리

**업계 사례**
- **Diablo / Path of Exile**: ItemBase + Affix(공유 풀) + Visual(타입 매핑). 자원 거의 100% 공유 풀
- **RPG Maker**: Database에 Items / Animations / SE를 별 탭으로 분리, Item이 Animation ID·SE ID 참조 (전형적 분리 + 매핑)
- **Unity Atoms / 일반 data-driven**: "ScriptableObject describes things, MonoBehaviour does things" — SO를 atomic하게 쪼개 컴포지션 권장
- **AAA 그래픽 엔진**: mesh/texture/material/animation 각각 마스터 DB → 인스턴스가 ID 참조 (asset pooling, type object 패턴)
- **CasualStrategy (2026-05)**: 53개 아이템(BasicItems 21 + CombinedItems 32) / 2개 `AnimationDataSO` → **26:1 공유 비율**. `ItemDataSO` + `AnimationConfigSO(itemRules, synergyRules)` 매핑. SoundConfigSO도 동일 패턴 예정

**구현 — (A) 카테고리 분리 + 매핑 (의사코드)**
```
// Resource SO (공유 단위)
class AnimationDataSO : ScriptableObject:
    animationId: string
    clip: AnimationClip
    duration: float

// Mapping SO (카테고리 → resource)
class AnimationConfigSO : ScriptableObject:
    itemRules: List<{itemId, AnimationDataSO}>
    synergyRules: List<{synergyType, AnimationDataSO}>

// Consumer (lookup via dictionary cache)
GetAnimation(itemId):
    return itemAnimDict[itemId]   // built in Awake from itemRules
```

**구현 — (B) 번들 (의사코드)**
```
class ItemDataSO : ScriptableObject:
    stats: ...
    icon: Sprite
    attackAnimClip: AnimationClip      // inline
    attackSfx: AudioClip               // inline
    onUseEffect: AbilityEffect         // SerializeReference 폴리모피즘
```

**구현 — (C) 혼합 (실전 표준)**
```
class ItemDataSO : ScriptableObject:
    stats: ...
    icon: Sprite                       // 번들 (1:1)
    weaponType: enum                   // 분리 키 (애니/사운드 룩업용)
    uniqueEffect: AbilityEffect?       // 번들 (있을 때만)

class AnimationConfigSO : ...           // weaponType → clip 분리
class AudioConfigSO : ...               // weaponType → sfx 분리
class GradeVisualConfigSO : ...         // grade → glow material 분리
```

⚠ **주의점**
- **너무 일찍 분리하지 말 것** — 자원 수가 적고(<5) 공유 빈도 모를 때는 번들로 시작. 같은 자원이 3번째 참조될 때 분리 리팩토링 (Rule of Three). 반대로, 처음부터 카테고리 단위 공유가 명백하면 분리 시작이 마이그레이션 비용 절감
- **매핑 키 타입 결정** — `string itemId`는 오타 위험 → enum, hash, 또는 SO 직접 참조 권장. 컴파일 타임 검증 vs 디자이너 편의 트레이드오프 (CasualStrategy의 `AnimationConfigSO.itemRules`는 string 키 → 약점, enum 마이그레이션 후보)
- **카테고리 매핑 룩업 비용** — 매 호출마다 List 순회면 호출자 수 × N → Awake/OnEnable에서 Dictionary 캐싱 필수 (CasualStrategy `DataManager` 패턴)
- **혼합 정책 권장** — 모든 자원을 같은 방식으로 처리할 필요 없음. 자원별 공유 빈도에 따라 분리/번들 혼용이 일반적. 위 (C) 패턴이 실전 표준
- **Localization은 항상 별도** — 언어 추가 시 모든 아이템 SO 건드리는 사태 방지. JSON/CSV 테이블 + key 참조가 표준 (Unity Localization Package 또는 자체 시스템)
- **분리 시 매핑 누락 검증** — 새 아이템 추가했는데 매핑 표에 빠뜨리면 "왜 이펙트 안 나오지" 디버그. fallback 로그 + 에디터 검증 스크립트(MenuItem) 권장
- **번들에서 폴리모피즘 필요 시** — 효과처럼 종류가 다양한 필드는 inline이라도 abstract base + `[SerializeReference, SubclassSelector]`로 (Unity feature-note 항목 42 참조)
- **재배치 비용 비대칭** — 초기 번들 → 후기 분리는 마이그레이션 메뉴 1회로 가능 (값 → 매핑 표로 평탄화). 반대(분리 → 번들)는 매핑 데이터를 모든 SO에 다시 inline해야 해 더 번거로움. **의심되면 분리 쪽으로 기울이기**
- **AssetDatabase 의존 함정** — 매핑 SO가 빈 List/null인 채로 빌드되면 런타임 NRE. OnEnable 캐싱 시 null 가드 + Editor에서 OnValidate로 중복 itemId/null entry 검출
- **번들의 inspector 무게** — 한 SO에 필드 20+개면 Inspector 스크롤 지옥. Header 그룹화 + `[FoldoutGroup]`(OdinInspector) 또는 분리로 회귀

**언제 쓰나 / 피할 때**
- ✅ 동일 자원을 3개 이상의 아이템이 공유할 때 (카테고리/등급/시너지 단위)
- ✅ 공유 자원이 독립적으로 튜닝될 때 — 디자이너가 "한 곳에서 조정"을 원할 때 분리
- ❌ 자원이 1:1 고유 (각 아이템에만 존재) — 분리 후 매핑 테이블이 더 복잡
- ❌ 아이템/데이터 수 < 5 — 번들로 시작, 공유 패턴이 보이면 분리 (Rule of Three)


#아키텍처 #구조 #재사용 #컴포지션 #ScriptableObject #데이터
> 종속성: `#OOP` `#언어독립` (개념). Unity SO는 구현 매체일 뿐 — UE의 DataTable + DataAsset, Godot의 Resource, 일반 JSON 데이터베이스에도 동일 적용
