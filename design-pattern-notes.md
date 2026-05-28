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

# 인덱스

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
| 24 | 카테고리 SO 분리 vs 번들 SO (Domain Resource Split) | `#아키텍처` `#구조` `#재사용` `#컴포지션` `#ScriptableObject` | 아이템처럼 여러 도메인 정보(스탯·아이콘·애니메이션·SFX·이펙트)를 가진 데이터 자산을, 도메인별 SO + 매핑 테이블로 *분리*할지 / 하나의 완전체 SO로 *번들*할지의 선택. 변종 간 자원 공유 비율이 분기 기준 | `#OOP` `#언어독립` |

---

# 풀노트

## 1. HFSM (Hierarchical State Machine)

**한 줄 요약**
상태가 계층으로 중첩되어 부모가 공통 전이·공통 동작을 담당하고, 자식이 세부 동작을 처리하는 상태머신.

**설명**
일반 FSM은 상태 수가 늘수록 전이 수가 N²으로 증가한다. `Standing`, `Crouching`, `Running` 각각에서 `Attacking`으로 전이하면 3개 전이 필요. HFSM에서는 `Moving` 부모 하나에서 `Attacking`으로 전이하면 1개로 처리된다.

전이 순서: `현재 자식.Exit → 현재 부모.Exit → 새 부모.Enter → 새 자식.Enter`. 같은 부모 내 전이면 부모 Exit/Enter 생략.

**구현**
```
abstract class State:
    parent: State?
    virtual Enter(): parent?.Enter()
    virtual Exit():  parent?.Exit()   // 자식 먼저, 부모 나중
    abstract Update()

class MoveState(State):
    Enter(): SetAnimation("move")

class RunState(MoveState):        // MoveState의 자식
    Enter(): base.Enter(); SetSpeed(fast)
```

**주의점**
- **같은 부모 내 전이** — 부모 Enter/Exit를 재호출하지 않으려면 전이 로직에서 공통 조상 탐색 필요. 안 하면 공통 초기화가 매번 리셋됨
- **깊이 제한** — 3단계 이상이면 Enter/Exit 호출 순서 추적이 어려워짐. 2단계로 충분한 경우가 대부분
- **HFSM vs FSM 선택** — 공통 전이가 3개 이상 반복될 때 HFSM이 유효. 상태 수 < 8이면 일반 FSM이 더 단순

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #4 State (기본 FSM)
- 태그: `#행위` `#상태머신` `#시스템`

---

## 2. Singleton

**한 줄 요약**
인스턴스를 전역에서 단 하나만 보장하는 패턴. 전역 접근점 제공 + 라이프사이클 제어.

**설명**
두 계열:

**(A) 순수 C#** — 라이프사이클을 직접 제어:
```csharp
class GameConfig
{
    static GameConfig _instance;
    public static GameConfig Instance => _instance ??= new GameConfig();
    private GameConfig() { }
}
```

**(B) Unity MonoSingleton** — MonoBehaviour 라이프사이클이 필요할 때:
```csharp
abstract class MonoSingleton<T> : MonoBehaviour where T : MonoSingleton<T>
{
    public static T Instance { get; private set; }
    protected virtual void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = (T)this;
        DontDestroyOnLoad(gameObject);
    }
}
class SoundManager : MonoSingleton<SoundManager> { }
```

**주의점**
- **테스트 불가** — `Instance`를 직접 호출하는 코드는 Mock 교체 불가. 테스트가 필요한 로직은 Service 계층으로 분리 + DI(#20) 경유
- **DontDestroyOnLoad 남용** — 씬 종속 오브젝트에 붙이면 씬 재로드 시 중복 인스턴스 생성
- **초기화 순서** — Awake에서 다른 Singleton을 참조하면 아직 초기화 안 된 상태일 수 있음. Start로 분리하거나 lazy initialization 사용

**메타**
- 종속성: `#OOP` `#언어독립` (B는 `#Unity`)
- 관련 노트: [[design-pattern-notes]] #19 CRTP (MonoSingleton<T> 구현 매체), #3 Service Locator (대안), #20 DI (테스트 가능한 대안)
- 태그: `#생성` `#전역` `#시스템`

---

## 3. Service Locator

**한 줄 요약**
서비스 인스턴스를 타입 키로 조회하는 중앙 레지스트리. 의존성을 pull 방식으로 해소.

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

**DI(#20)와의 차이**

| | Service Locator | DI |
|---|---|---|
| 방향 | pull (사용자가 꺼냄) | push (컨테이너가 주입) |
| 의존성 명시 | 숨김 | 명시 (생성자/필드) |
| 테스트 | 전역 상태 교체 필요 | Mock 생성자 주입으로 충분 |
| Unity 적합성 | 높음 | 중간 (프레임워크 필요) |

**주의점**
- **숨은 의존성** — 클래스 생성자만 보면 어떤 서비스에 의존하는지 모름
- **미등록 서비스** — Get 시 `KeyNotFoundException`. NullService fallback 또는 TryGet 패턴 권장
- **테스트 격리** — 전역 딕셔너리이므로 테스트 간 상태 오염. teardown에서 Clear 필수

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #2 Singleton (더 단순한 전역 접근), #20 DI (push 방향 대안)
- 태그: `#아키텍처` `#서비스` `#전역`

---

## 4. State (Enter/Exit + 브로드캐스트)

**한 줄 요약**
Enter/Exit 훅으로 상태 전이를 캡슐화하고, 전이 발생 시 Observer로 외부에 통지하는 FSM 노드 패턴.

**설명**
```csharp
abstract class State
{
    public virtual void Enter() { }
    public virtual void Update() { }
    public virtual void Exit() { }
}

class StateMachine
{
    State _current;
    public event Action<State, State> OnTransition;  // (from, to)

    public void Change(State next)
    {
        _current?.Exit();
        var prev = _current;
        _current = next;
        OnTransition?.Invoke(prev, next);  // UI/Sound 등 외부 통지
        _current.Enter();
    }
    public void Update() => _current?.Update();
}
```

**주의점**
- **Exit → Enter 순서** — Exit 먼저, Enter 나중. 반대면 새 상태의 Enter가 이전 리소스를 참조할 때 충돌
- **Enter 내부 재전이** — Enter()에서 Change()를 호출하면 재귀 전이. Guard flag 또는 큐 방식으로 방어
- **이벤트 구독 해제** — StateMachine 파괴 시 OnTransition 구독 해제 안 하면 memory leak

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #1 HFSM (계층 확장), #16 Observer (브로드캐스트 구현 매체)
- 태그: `#행위` `#상태머신` `#시스템`

---

## 5. Service Layer 분리 (Service ↔ Manager)

**한 줄 요약**
비즈니스 로직(Service, 순수 C#)과 MonoBehaviour 라이프사이클(Manager)을 별도 클래스로 분리해 로직의 테스트 가능성을 확보.

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

**주의점**
- **Service에 MonoBehaviour 메서드 금지** — `StartCoroutine`, `GetComponent` 사용 시 분리 의미 없음. 코루틴이 필요하면 Manager에서 호스팅
- **분리 임계점** — 메서드 3개 이하면 Manager에 합쳐도 무방. 테스트/재사용 필요성이 보일 때 분리
- **Manager의 Facade 역할** — Manager가 Service 메서드를 그대로 위임 노출하면 Facade(#8) 겸임

**메타**
- 종속성: `#아키텍처` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #2 Singleton (Manager 구현 매체), #8 Facade (Manager의 역할 겸임), #20 DI (Service 의존성 주입)
- 태그: `#아키텍처` `#계층` `#서비스`

---

## 6. Template Method

**한 줄 요약**
부모 클래스가 알고리즘의 골격(호출 순서)을 정의하고, 세부 단계는 자식 클래스가 override로 채우는 패턴.

**설명**
```csharp
abstract class EnemyAI
{
    public void ExecuteTurn()   // 템플릿 메서드 — 순서 고정, sealed 권장
    {
        Perceive();
        if (ShouldAttack()) Attack();
        else Move();
        PostTurn();             // 선택적 훅 — 기본 구현 있음
    }

    protected abstract void Perceive();
    protected abstract bool ShouldAttack();
    protected abstract void Attack();
    protected abstract void Move();
    protected virtual void PostTurn() { }
}

class MeleeEnemy : EnemyAI
{
    protected override void Perceive() { /* 근거리 감지 */ }
    protected override bool ShouldAttack() => distanceToPlayer < 2f;
    protected override void Attack() { /* 근접 공격 */ }
    protected override void Move() { /* 플레이어 방향 이동 */ }
}
```

**Strategy(#7)와의 차이**

| | Template Method | Strategy |
|---|---|---|
| 확장 방법 | 상속 (자식 클래스) | 컴포지션 (다른 객체) |
| 런타임 교체 | 불가 | 가능 |
| 결합도 | 부모-자식 강결합 | 느슨한 결합 |

**주의점**
- **골격 메서드 보호** — `ExecuteTurn`은 자식이 override 못하도록 `sealed` 처리
- **상속 깊이** — 2단계 이상 깊어지면 Strategy로 전환 검토
- **선택적 훅** — override 강제가 아닌 `virtual` + 빈 기본 구현으로 선택지 부여

**메타**
- 종속성: `#OOP` `#상속`
- 관련 노트: [[design-pattern-notes]] #7 Strategy (상속 대신 컴포지션 대안)
- 태그: `#행위` `#상속`

---

## 7. Strategy

**한 줄 요약**
동일 시그니처의 알고리즘을 인터페이스/함수로 캡슐화해서 런타임에 교체 가능하게 하는 패턴.

**설명**
**(A) 인터페이스 방식** — 전략 객체가 상태를 가질 때:
```csharp
interface IAttackStrategy { void Execute(Character attacker, Character target); }

class MeleeAttack : IAttackStrategy
{
    public void Execute(Character a, Character t) => t.TakeDamage(a.PhysicalPower);
}

class Character
{
    public IAttackStrategy AttackStrategy { get; set; } = new MeleeAttack();
    public void Attack(Character t) => AttackStrategy.Execute(this, t);
}
// 런타임 교체: character.AttackStrategy = new MagicAttack();
```

**(B) 함수형** — 단순 무상태 전략:
```csharp
class Character
{
    public Action<Character, Character> AttackStrategy;
}
// character.AttackStrategy = (a, t) => t.TakeDamage(a.Power * 2);
```

**주의점**
- **상태 유무** — 전략 객체가 상태를 가져야 하면 인터페이스 방식, 순수 함수라면 `Action`/`Func`이 더 단순
- **런타임 교체 없으면** — Template Method(#6)가 더 단순한 선택
- **전략 생성 비용** — 매 호출마다 `new Strategy()`면 GC 압력. 미리 생성해두거나 Pool(#18) 사용

**메타**
- 종속성: `#OOP` `#FP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #6 Template Method (상속 기반 대안), #17 Callback (함수형 Strategy)
- 태그: `#행위` `#확장성`

---

## 8. Facade

**한 줄 요약**
복잡한 서브시스템(여러 클래스의 협력)에 단순화된 단일 진입점 인터페이스를 제공하는 패턴.

**설명**
```csharp
// 서브시스템 (복잡한 내부)
class AudioLoader  { public AudioClip Load(string path) { ... } }
class AudioMixer   { public void SetVolume(string group, float v) { ... } }
class AudioPlayer  { public void Play(AudioClip clip, Vector3 pos) { ... } }

// Facade — 외부에서는 이것만 사용
class SoundFacade
{
    AudioLoader _loader = new(); AudioMixer _mixer = new(); AudioPlayer _player = new();

    public void PlaySfx(string id, Vector3 pos)
    {
        var clip = _loader.Load($"Sounds/{id}");
        _mixer.SetVolume("SFX", 0.8f);
        _player.Play(clip, pos);
    }
}
```

**주의점**
- **서브시스템 직접 접근** — Facade가 있어도 서브시스템 클래스에 직접 접근 가능하면 절반짜리. `internal`로 외부 접근 차단 권장
- **비대화 방지** — 모든 기능을 Facade에 추가하면 God Object가 됨. 고급 기능은 서브시스템에 남기기
- **Service(#5)와 중첩** — Manager가 Service들을 조합해서 공개하는 구조는 Facade 역할 겸임

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #5 Service Layer 분리 (Manager의 Facade 겸임 패턴)
- 태그: `#구조`

---

## 9. Memento

**한 줄 요약**
객체 내부 상태를 외부에 캡슐화해 저장하고 나중에 복원하는 패턴. 내부 구조를 노출하지 않음.

**설명**
```csharp
// Memento — 불변 스냅샷 (record 사용 권장)
record CharacterMemento(int Hp, int Mp, Vector3 Position);

// Originator — 상태를 가진 원본
class Character
{
    public int Hp, Mp; public Vector3 Position;
    public CharacterMemento Save() => new(Hp, Mp, Position);
    public void Restore(CharacterMemento m) { Hp = m.Hp; Mp = m.Mp; Position = m.Position; }
}

// Caretaker — 스냅샷 관리
class CheckpointSystem
{
    Stack<CharacterMemento> _history = new();
    public void Push(Character c) => _history.Push(c.Save());
    public void Pop(Character c) { if (_history.Count > 0) c.Restore(_history.Pop()); }
}
```

**주의점**
- **얕은 복사 함정** — 상태에 `List<T>` 같은 참조 타입이 있으면 스냅샷 저장 시 깊은 복사 필요. 아니면 원본 변경 시 Memento도 변경됨
- **메모리 비용** — 저장 빈도 높으면 메모리 증가. 저장 필드 최소화 또는 압축 검토
- **Command(#10)와 조합** — Undo/Redo 시스템은 Command(실행 내역) + Memento(상태 스냅샷) 조합

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #10 Command (Undo와 조합), [[csharp-syntax-notes]] record (Memento 구현체로 적합)
- 태그: `#행위`

---

## 10. Command

**한 줄 요약**
요청(동작)을 객체로 캡슐화해 나중에 실행·취소·큐잉·로깅할 수 있게 하는 패턴.

**설명**
```csharp
interface ICommand { void Execute(); void Undo(); }

class MoveCommand : ICommand
{
    Character _target; Vector3 _delta, _prevPos;
    public MoveCommand(Character target, Vector3 delta) { _target = target; _delta = delta; }
    public void Execute() { _prevPos = _target.Position; _target.Position += _delta; }
    public void Undo()    { _target.Position = _prevPos; }
}

class CommandHistory
{
    Stack<ICommand> _done = new();
    public void Execute(ICommand cmd) { cmd.Execute(); _done.Push(cmd); }
    public void Undo() { if (_done.Count > 0) _done.Pop().Undo(); }
}
```

**주의점**
- **Undo의 완전성** — 부수효과(사운드, 이펙트)까지 Undo하면 복잡도 폭발. 부수효과는 Undo 대상에서 제외하는 것이 일반적
- **Command 생성 비용** — 고빈도 입력에서 매 입력마다 `new`면 GC 압력. Pool(#18) 사용
- **Macro** — 여러 Command를 묶어 실행하는 CompositeCommand = Command + Composite(#15) 조합

**메타**
- 종속성: `#OOP` `#FP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #9 Memento (Undo 상태 복원), #15 Composite (CompositeCommand), #18 Object Pooling (Command 객체 재사용)
- 태그: `#행위`

---

## 11. Adapter

**한 줄 요약**
기존 클래스의 인터페이스를 클라이언트가 기대하는 형태로 변환하는 래퍼. 서로 맞지 않는 두 코드를 연결.

**설명**
```csharp
// 기존 코드 (변경 불가)
class LegacyAudioSystem { public void PlaySound(string path, float vol) { ... } }

// 클라이언트가 기대하는 인터페이스
interface IAudioService { void Play(string id); }

// Adapter — 번역기 (Object Adapter, 컴포지션)
class LegacyAudioAdapter : IAudioService
{
    LegacyAudioSystem _legacy = new();
    public void Play(string id) => _legacy.PlaySound($"Assets/Sounds/{id}.wav", 1.0f);
}
```

Object Adapter(컴포지션) vs Class Adapter(상속) — C#은 단일 상속 제한으로 Object Adapter가 일반적.

**주의점**
- **남용 금지** — 새 코드를 처음부터 올바른 인터페이스로 짜는 대신 Adapter를 쓰면 복잡도만 증가. 레거시/외부 라이브러리 연결 전용
- **변환 비용** — 경로 변환, 타입 캐스팅 등 Adapter 내부 작업이 무거우면 캐싱 고려
- **불일치가 심할 때** — Adapter 한 겹으로 해결 안 되면 Facade(#8)로 추상화 추가

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #8 Facade (더 넓은 단순화), #13 Decorator (동일 인터페이스 유지 래퍼)
- 태그: `#구조`

---

## 12. Chain of Responsibility

**한 줄 요약**
요청을 처리할 핸들러를 체인으로 연결하고, 각 핸들러가 처리하거나 다음으로 넘기는 패턴.

**설명**
```csharp
abstract class InputHandler
{
    protected InputHandler _next;
    public InputHandler SetNext(InputHandler next) { _next = next; return next; }
    public virtual bool Handle(InputEvent e) => _next?.Handle(e) ?? false;
}

class UIInputHandler : InputHandler
{
    public override bool Handle(InputEvent e)
    {
        if (EventSystem.IsPointerOverUI()) return true;  // UI가 소비
        return base.Handle(e);
    }
}

class PlayerInputHandler : InputHandler
{
    public override bool Handle(InputEvent e)
    {
        if (e.type == InputType.Attack) { player.Attack(); return true; }
        return base.Handle(e);
    }
}

// 체인 구성: UI → Player → ...
var chain = new UIInputHandler();
chain.SetNext(new PlayerInputHandler());
```

**주의점**
- **체인 끝 처리** — 모든 핸들러가 처리 못 할 때를 위한 NullHandler를 체인 끝에 추가 권장
- **순서 의존성** — 체인 순서가 곧 우선순위. UI가 Player보다 먼저여야 하는 것처럼 순서 실수 = 버그
- **디버깅 어려움** — 어디서 소비됐는지 추적하기 어려움. 처리 로그 추가 권장

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #16 Observer (이벤트 기반 대안)
- 태그: `#행위` `#이벤트`

---

## 13. Decorator

**한 줄 요약**
객체를 동일 인터페이스의 wrapper로 감싸서 기존 코드 수정 없이 기능을 동적으로 추가/조합하는 패턴.

**설명**
```csharp
interface IWeaponEffect { int ApplyDamage(int baseDamage); }

class BaseWeapon : IWeaponEffect { public int ApplyDamage(int b) => b; }

class PoisonDecorator : IWeaponEffect
{
    IWeaponEffect _inner;
    public PoisonDecorator(IWeaponEffect inner) { _inner = inner; }
    public int ApplyDamage(int b) { ApplyPoison(); return _inner.ApplyDamage(b); }
}

class FireDecorator : IWeaponEffect { /* 동일 구조 */ }

// 조합: 독 + 불 — 런타임에 자유롭게
IWeaponEffect weapon = new FireDecorator(new PoisonDecorator(new BaseWeapon()));
```

상속과 비교: 상속은 조합 수만큼 클래스 폭발(PoisonFireSword, PoisonSword...), Decorator는 클래스 수 선형.

**주의점**
- **중첩 깊이** — 3단계 이상이면 call stack 추적 어려움. 이 수준이면 `List<IEffect>` 순회 방식 검토
- **동일성 비교** — `wrapper == original`이 false. ID 시스템 또는 내부 객체 노출 필요
- **무상태 Decorator** — 상태 없는 Decorator는 싱글톤/재사용 가능해 GC 압력 없음

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #15 Composite (트리 구조 대안)
- 태그: `#구조`

---

## 14. Factory

**한 줄 요약**
객체 생성 로직을 별도 메서드/클래스로 분리해서 생성 방법 변경이 호출 코드에 영향을 주지 않게 하는 패턴.

**설명**
세 변종:

**(A) Static Factory** — 가장 단순. 의미있는 이름의 정적 생성 메서드:
```csharp
class Bullet
{
    public static Bullet FromPlayer(float speed) => new Bullet { Speed = speed, Friendly = true };
    public static Bullet FromEnemy(float speed)  => new Bullet { Speed = speed, Friendly = false };
}
```

**(B) Factory Method** — 서브클래스가 어떤 객체를 만들지 결정:
```csharp
abstract class EnemySpawner
{
    public Enemy Spawn() { var e = CreateEnemy(); e.Initialize(); return e; }
    protected abstract Enemy CreateEnemy();
}
class GoblinSpawner : EnemySpawner { protected override Enemy CreateEnemy() => new Goblin(); }
```

**(C) Abstract Factory** — 관련 객체 세트를 함께 생성:
```csharp
interface IEnemyFactory { Enemy CreateEnemy(); Projectile CreateProjectile(); }
class GoblinFactory : IEnemyFactory { ... }
class OrcFactory    : IEnemyFactory { ... }
```

**주의점**
- **변종 선택 기준** — Static Factory는 생성 방법 1-2가지. Factory Method는 서브클래스마다 다른 타입. Abstract Factory는 관련 세트를 통째로 교체할 때
- **Pool(#18)과 조합** — 팩토리가 `new` 대신 Pool에서 꺼내면 GC 없는 팩토리
- **과도한 추상화 주의** — 객체 종류 2개에 Abstract Factory는 오버엔지니어링. 직접 `new`가 더 명확한 경우 많음

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #18 Object Pooling (Pool + Factory 조합)
- 태그: `#생성`

---

## 15. Composite

**한 줄 요약**
단일 객체와 객체 집합을 동일한 인터페이스로 다루어, 트리 구조를 균일하게 처리하는 패턴.

**설명**
```csharp
interface IDamageSource { int CalculateDamage(); }

// Leaf — 단일 객체
class WeaponEffect : IDamageSource
{
    int _damage;
    public int CalculateDamage() => _damage;
}

// Composite — 컬렉션
class ComboEffect : IDamageSource
{
    List<IDamageSource> _effects = new();
    public void Add(IDamageSource e) => _effects.Add(e);
    public int CalculateDamage() => _effects.Sum(e => e.CalculateDamage());
}

// 클라이언트는 Leaf/Composite 구분 없이 동일하게 호출
IDamageSource effect = new ComboEffect();
// ... Add Leaf or ComboEffect (중첩 가능) ...
int total = effect.CalculateDamage();
```

**주의점**
- **인터페이스에 Add/Remove 강제 문제** — Leaf도 Add/Remove를 구현해야 하면 어색. Composite 타입만 Add/Remove를 가지도록 분리
- **트리 순환 참조** — Composite가 자기 자신을 자식으로 추가하면 무한 루프. Guard 필요
- **집계 캐싱** — 깊은 트리에서 매 프레임 순회 비용이 크면 캐싱 고려

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #13 Decorator (래퍼 방식 대안), #10 Command (CompositeCommand)
- 태그: `#구조`

---

## 16. Observer

**한 줄 요약**
주체(Subject)가 상태 변경을 구독자(Observer)에게 자동으로 통지하는 패턴. 느슨한 결합으로 1:N 의존성 구현.

**설명**
C#에서는 세 가지 방식:

**(A) event/delegate** — 가장 일반적:
```csharp
class PlayerStatus
{
    public event Action<int> OnHpChanged;
    int _hp;
    public int Hp { get => _hp; set { _hp = value; OnHpChanged?.Invoke(_hp); } }
}
// 구독
player.OnHpChanged += UpdateHpUI;
// 해제 (OnDestroy에서 반드시!)
player.OnHpChanged -= UpdateHpUI;
```

**(B) IObservable/IObserver** — UniRx 스타일. 스트림 조합이 필요할 때:
```csharp
var hpStream = new Subject<int>();
hpStream.Where(hp => hp < 20).Subscribe(_ => ShowLowHpWarning());
```

**(C) UnityEvent** — Inspector에서 구독 가능. 디자이너 친화:
```csharp
[SerializeField] UnityEvent<int> onHpChanged;
```

**주의점**
- **구독 해제 누수** — 가장 흔한 버그. `OnDestroy`에서 `-=` 또는 `Dispose()` 반드시
- **이벤트 순환** — A의 핸들러에서 B 상태 변경 → B의 핸들러에서 A 상태 변경 → 무한 루프. Guard flag 필요
- **정적 이벤트 위험** — `static event`는 인스턴스 파괴 후에도 구독이 GC되지 않음. 수동 해제 필수

**메타**
- 종속성: `#OOP` `#FP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #4 State (브로드캐스트 구현), #23 단일 이벤트 + 추상 Entry (이종 이벤트 통합)
- 태그: `#행위` `#이벤트`

---

## 17. Callback

**한 줄 요약**
함수를 인자로 전달해서 피호출자가 결정한 시점에 실행하게 하는 패턴. 완료 통지와 결과 반환에 사용.

**설명**
```csharp
// (A) Action/Func 델리게이트
void LoadAsync(string path, Action<Sprite> onLoaded)
{
    var sprite = Resources.Load<Sprite>(path);
    onLoaded?.Invoke(sprite);
}
LoadAsync("Icons/sword", sprite => iconImage.sprite = sprite);

// (B) 코루틴 완료 콜백
IEnumerator FadeOut(float duration, Action onComplete)
{
    yield return new WaitForSeconds(duration);
    onComplete?.Invoke();
}

// (C) async/await — C#의 콜백 평탄화
async Task<Sprite> LoadAsync(string path) { return await LoadSpriteAsync(path); }
```

**Observer(#16)과의 차이**
- Observer: 1:N, 구독자가 등록/해제. 상태 변경 통지 목적
- Callback: 1:1, 호출자가 함수 직접 전달. 완료 통지/결과 반환 목적

**주의점**
- **콜백 지옥** — 콜백 중첩이 깊어지면 들여쓰기 폭발. async/await 또는 코루틴 + 완료 콜백으로 평탄화
- **null 체크** — `onComplete?.Invoke()`
- **캡처 변수 수명** — 람다가 외부 변수를 캡처할 때 변수가 파괴된 뒤에 콜백이 실행되면 NRE

**메타**
- 종속성: `#OOP` `#FP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #16 Observer (1:N 이벤트 대안), [[csharp-syntax-notes]] async/await
- 태그: `#행위`

---

## 18. Object Pooling

**한 줄 요약**
자주 생성/파괴되는 객체를 재사용 가능한 풀에서 꺼내쓰고 돌려놓아 GC 스파이크와 생성 비용을 제거.

**설명**
```csharp
// 직접 구현
class ObjectPool<T> where T : class, new()
{
    Stack<T> _pool = new();
    public T Get() => _pool.Count > 0 ? _pool.Pop() : new T();
    public void Release(T obj) => _pool.Push(obj);  // 상태 리셋은 호출자 책임
}

// Unity — UnityEngine.Pool.ObjectPool<T> 권장
var pool = new ObjectPool<Bullet>(
    createFunc:      () => Instantiate(bulletPrefab),
    actionOnGet:     b => b.gameObject.SetActive(true),
    actionOnRelease: b => b.gameObject.SetActive(false),
    actionOnDestroy: b => Destroy(b.gameObject)
);
```

**주의점**
- **상태 오염** — Get 시 이전 사용 상태가 남아 있으면 버그. Get 또는 Release 시 반드시 Reset
- **Release 누락** — 돌려주지 않으면 풀이 비어서 결국 계속 `new` 발생. 수명 관리 객체에서 자동 Release 설계
- **풀 상한** — 상한 없이 풀이 커지면 메모리 증가. 최대 크기 + 초과 시 파괴 또는 경고
- **씬 전환** — `DontDestroyOnLoad`가 아닌 풀은 씬 전환 시 파괴됨. 풀 오브젝트 수명 맞추기

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #22 Streaming Pattern (확장형의 필수 구성요소), #14 Factory (Pool + Factory 조합)
- 태그: `#생성` `#성능`

---

## 19. CRTP (Curiously Recurring Template Pattern)

**한 줄 요약**
`class Foo<T> where T : Foo<T>` — 부모 제네릭이 자식 타입을 타입 파라미터로 받아서 타입 안전한 자기 참조를 구현.

**설명**
```csharp
// MonoSingleton — 대표 사용 사례
abstract class MonoSingleton<T> : MonoBehaviour where T : MonoSingleton<T>
{
    public static T Instance { get; private set; }
    protected virtual void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = (T)this;  // T가 자식 타입이므로 캐스팅 안전
    }
}

class AudioManager : MonoSingleton<AudioManager> { }
// AudioManager.Instance는 AudioManager 타입 — 캐스팅 불필요
AudioManager.Instance.Play("hit");

// CRTP 없이는
((AudioManager)MonoSingleton.Instance).Play("hit");  // 매번 캐스팅 필요
```

**주의점**
- **where 제약 필수** — `where T : MonoSingleton<T>` 없으면 `(T)this` 캐스팅이 컴파일 타임 검증 불가
- **손자 클래스** — `class C : B` (`B : A<B>`)에서 C는 `A<C>`가 아님. CRTP는 1단계 상속에서만 완벽
- **남용 주의** — 타입 안전한 `this` 반환과 Singleton 외에 용도가 드묾. 명확한 이유 없으면 일반 제네릭으로 충분

**메타**
- 종속성: `#OOP` `#C#제네릭`
- 관련 노트: [[design-pattern-notes]] #2 Singleton (CRTP의 대표 적용 사례)
- 태그: `#생성` `#구조` `#제네릭`

---

## 20. DI (Dependency Injection)

**한 줄 요약**
객체가 의존성을 직접 생성/탐색하는 대신 외부에서 주입받아 결합도를 낮추고 테스트 가능성을 높이는 패턴.

**설명**
```csharp
// DI 없이 — 강결합
class PlayerAttack { AudioService _audio = new AudioService(); }  // 교체 불가

// 생성자 주입 (가장 명시적, 권장)
class PlayerAttack
{
    readonly IAudioService _audio;
    public PlayerAttack(IAudioService audio) { _audio = audio; }
}
var attack = new PlayerAttack(new AudioService());    // 실제
var attack = new PlayerAttack(new MockAudioService()); // 테스트
```

세 가지 주입 방식:
- **생성자 주입** — 의존성이 필수일 때. 가장 명시적
- **프로퍼티 주입** — 선택적 의존성. `public IAudioService Audio { get; set; }`
- **메서드 주입** — 특정 호출 시점에만 필요. `void Init(IAudioService audio)`

Unity에서는 `[SerializeField]`로 Inspector에서 참조를 끌어다 놓는 것도 Property Injection의 일종.

**주의점**
- **생성자 파라미터 폭발** — 의존성 5개 이상이면 너무 많은 일을 하는 클래스 신호. 책임 분리 필요
- **인터페이스 남발** — 교체 계획 없는 의존성에 인터페이스 만드는 것은 오버엔지니어링. 테스트/교체 가능성이 실제로 있을 때만
- **Unity DI 프레임워크** — VContainer, Zenject 등이 있지만 간단한 프로젝트는 수동 DI(Manager → Service 패턴)로 충분

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #3 Service Locator (pull 방향 대안), #5 Service Layer (Service를 주입받는 대표 패턴), #21 Domain-Scoped Injection Interface
- 태그: `#아키텍처` `#서비스` `#결합도감소` `#테스트용이`

---

## 21. Domain-Scoped Injection Interface

**한 줄 요약**
단일 `IInjectable` 대신 도메인별로 인터페이스를 분리(`IMonsterInjectable`, `IItemInjectable` 등)해 잘못된 의존성 결합을 컴파일 타임에 차단.

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

**주의점**
- **인터페이스 수 증가** — 도메인마다 인터페이스가 생기므로 도메인 3개 이하라면 단일 인터페이스도 무방
- **부분 구현 강제 안 됨** — 인터페이스 분리는 컴파일 타임 가이드일 뿐. 어떤 클래스에 어떤 인터페이스가 필요한지는 여전히 사람이 결정
- **Mock 테스트** — 도메인 단위로 Mock 생성 가능 → DI(#20) 대비 테스트 범위가 작아짐

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #20 DI (기반 패턴)
- 태그: `#아키텍처` `#인터페이스` `#테스트용이`

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

## 23. 단일 이벤트 + 추상 Entry 디스패치

**한 줄 요약**
`Action<TBase>` 단일 이벤트 + abstract base class로 이종 데이터를 하나의 채널로 발행하고, 수신자가 다형성으로 처리하는 패턴.

**설명**
```csharp
// 나쁜 방법 — 종류마다 이벤트 채널 → 수신자가 N개 구독 필요
event Action<AttackEntry> OnAttack;
event Action<HealEntry>   OnHeal;
event Action<BuffEntry>   OnBuff;

// 좋은 방법 — 단일 채널 + 다형성 분기
abstract class CombatEntry { }
class AttackEntry : CombatEntry { public int Damage; }
class HealEntry   : CombatEntry { public int Amount; }
class BuffEntry   : CombatEntry { public BuffType Buff; }

event Action<CombatEntry> OnCombatEvent;

// 발행
OnCombatEvent?.Invoke(new AttackEntry { Damage = 10 });

// 수신 — 패턴 매칭
OnCombatEvent += entry =>
{
    switch (entry)
    {
        case AttackEntry a: HandleAttack(a); break;
        case HealEntry h:   HandleHeal(h);   break;
        case BuffEntry b:   HandleBuff(b);   break;
        default: Debug.LogWarning($"Unhandled: {entry.GetType()}"); break;
    }
};
```

새 이벤트 종류 추가 시 `CombatEntry` 서브클래스만 추가 — 이벤트 선언/구독 코드 변경 없음.

**주의점**
- **switch 누락** — 새 Entry 서브클래스를 추가했는데 수신자 switch에 case가 없으면 조용히 무시됨. `default: Debug.LogWarning` 또는 throw 권장
- **단일 채널 과부하** — 의미적으로 다른 이벤트를 한 채널에 넣으면 수신자 switch가 길어짐. 의미적으로 묶이는 이벤트들만 같은 채널로
- **Entry 불변성** — 이벤트는 여러 수신자에게 전달되므로 수신자가 Entry를 수정하면 다음 수신자에 영향. `readonly` 필드 또는 `record` 타입으로 불변 설계

**메타**
- 종속성: `#OOP` `#언어독립`
- 관련 노트: [[design-pattern-notes]] #16 Observer (기반 이벤트 패턴), [[csharp-syntax-notes]] #패턴매칭 (switch expression)
- 태그: `#행동` `#이벤트`

---

## 24. 카테고리 SO 분리 vs 번들 SO (Domain Resource Split)

**한 줄 요약**
아이템처럼 여러 도메인 정보(스탯·아이콘·애니메이션·SFX·이펙트)를 가진 데이터 자산을, 도메인별 SO + 매핑 테이블로 분리할지 / 하나의 완전체 SO로 번들할지의 선택. 자원이 *변종 간 공유*되면 분리, *1:1 고유*면 번들이 유리.

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

**주의점**
- **너무 일찍 분리하지 말 것** — 자원 수가 적고(<5) 공유 빈도 모를 때는 번들로 시작. 같은 자원이 3번째 참조될 때 분리 리팩토링 (Rule of Three). 반대로, 처음부터 카테고리 단위 공유가 명백하면 분리 시작이 마이그레이션 비용 절감
- **매핑 키 타입 결정** — `string itemId`는 오타 위험 → enum, hash, 또는 SO 직접 참조 권장. 컴파일 타임 검증 vs 디자이너 편의 트레이드오프 (CasualStrategy의 `AnimationConfigSO.itemRules`는 string 키 → 약점, enum 마이그레이션 후보)
- **카테고리 매핑 룩업 비용** — 매 호출마다 List 순회면 호출자 수 × N → Awake/OnEnable에서 Dictionary 캐싱 필수 (CasualStrategy `DataManager` 패턴)
- **혼합 정책 권장** — 모든 자원을 같은 방식으로 처리할 필요 없음. 자원별 공유 빈도에 따라 분리/번들 혼용이 일반적. 위 (C) 패턴이 실전 표준
- **Localization은 항상 별도** — 언어 추가 시 모든 아이템 SO 건드리는 사태 방지. JSON/CSV 테이블 + key 참조가 표준 (Unity Localization Package 또는 자체 시스템)
- **분리 시 매핑 누락 검증** — 새 아이템 추가했는데 매핑 표에 빠뜨리면 "왜 이펙트 안 나오지" 디버그. fallback 로그 + 에디터 검증 스크립트(MenuItem) 권장
- **번들에서 폴리모피즘 필요 시** — 효과처럼 종류가 다양한 필드는 inline이라도 abstract base + `[SerializeReference, SubclassSelector]`로 (Unity feature-note #42 참조)
- **재배치 비용 비대칭** — 초기 번들 → 후기 분리는 마이그레이션 메뉴 1회로 가능 (값 → 매핑 표로 평탄화). 반대(분리 → 번들)는 매핑 데이터를 모든 SO에 다시 inline해야 해 더 번거로움. **의심되면 분리 쪽으로 기울이기**
- **AssetDatabase 의존 함정** — 매핑 SO가 빈 List/null인 채로 빌드되면 런타임 NRE. OnEnable 캐싱 시 null 가드 + Editor에서 OnValidate로 중복 itemId/null entry 검출
- **번들의 inspector 무게** — 한 SO에 필드 20+개면 Inspector 스크롤 지옥. Header 그룹화 + `[FoldoutGroup]`(OdinInspector) 또는 분리로 회귀

**메타**
- 종속성: `#OOP` `#언어독립` (개념). Unity SO는 구현 매체일 뿐 — UE의 DataTable + DataAsset, Godot의 Resource, 일반 JSON 데이터베이스에도 동일 적용
- 관련 노트:
  - [[unity-feature-notes]] #2 ScriptableObject (구현 매체), #42 SerializeReference + SubclassSelector (번들에서 폴리모피즘)
  - [[design-pattern-notes]] #15 Composite (분리 + 매핑의 한 형태), #14 Factory (매핑 룩업이 사실상 자원 팩토리), #7 Strategy (effect를 번들 inline)
- 첫 도출: CasualStrategy (2026-05-20) — `ItemDataSO` + `AnimationConfigSO(itemRules)` 매핑 구조 분석에서 도출. 53 items / 2 animations (26:1 공유) → 분리가 명백한 정답인 케이스
- 적용 사례:
  - CasualStrategy: `ItemDataSO` + `AnimationConfigSO`(itemRules/synergyRules), 추가 예정 `SoundConfigSO` 동일 패턴, `GradeVisualConfigSO` 후보
  - 업계: Diablo/PoE (Item + Affix + Visual), RPG Maker Database (Items/Animations/SE 분리), AAA asset pooling
- 태그: `#아키텍처` `#구조` `#재사용` `#컴포지션` `#ScriptableObject` `#데이터`

---
