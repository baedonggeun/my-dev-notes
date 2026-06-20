# 디자인 패턴 노트 — 행위 패턴 (GoF Behavioral)

> 상위 노트: [[design-pattern-notes]] (전체 인덱스 디스패처)
> 다루는 축: GoF 행위 패턴: 객체 간 협력·통신·책임 위임
> 다루지 않는 축: 생성·구조 패턴 / 아키텍처 패턴

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
| 4 | State (Enter/Exit + 브로드캐스트) | `#행위` `#상태머신` | Enter/Exit 훅으로 상태 전이 캡슐화 + 옵저버 통지 | `#OOP` `#언어독립` |
| 6 | Template Method | `#행위` `#상속` | 부모가 알고리즘 골격, 자식이 훅 메서드 오버라이드 | `#OOP` `#상속` |
| 7 | Strategy | `#행위` `#확장성` | 동일 시그니처 알고리즘을 객체/함수로 캡슐화해 런타임 교체 | `#OOP` `#FP` `#언어독립` |
| 9 | Memento | `#행위` | 객체 상태를 외부에 노출 없이 캡쳐/복원 | `#OOP` `#언어독립` |
| 10 | Command | `#행위` | 요청을 객체로 캡슐화해 큐잉/실행 취소 가능 | `#OOP` `#FP` `#언어독립` |
| 12 | Chain of Responsibility | `#행위` `#이벤트` | 요청을 핸들러 체인으로 전달, 각자 처리 또는 다음으로 위임 | `#OOP` `#언어독립` |
| 16 | Observer | `#행위` `#이벤트` | 주체가 상태 변경을 구독자에게 통지 (정적/인스턴스 이벤트) | `#OOP` `#FP` `#언어독립` |
| 17 | Callback | `#행위` | 함수를 인자로 전달해 시점이 다른 코드 실행 | `#OOP` `#FP` `#언어독립` |
| 23 | 단일 이벤트 + 추상 Entry 디스패치 | `#행동` `#이벤트` | `Action<TBase>` 단일 이벤트 + abstract base class로 이종 데이터를 하나의 채널로 발행 — 수신자는 다형성으로 처리, 종류 추가 시 이벤트/수신자 변경 없이 entry 서브클래스만 추가 | `#OOP` `#언어독립` |
| 25 | Effect 삼분 (Apply / Emit / Describe) | `#행위` `#구조` | 하나의 Effect를 Apply(수치 계산·상태 변경) · Emit(파티클·사운드·연출) · Describe(툴팁 텍스트) 세 책임으로 고정. 효과 추가 시 기존 코드 무수정, 각 책임을 독립 테스트 가능 | `#OOP` `#언어독립` |

---

# 풀노트

## 1. HFSM (Hierarchical State Machine)

_상태가 계층으로 중첩되어 부모가 공통 전이·공통 동작을 담당하고, 자식이 세부 동작을 처리하는 상태머신._

**직관**
군 지휘 체계 — 사단장(부모 상태)이 공통 전이를 담당하고, 각 소대(자식 상태)가 세부 동작을 처리. 공통 명령은 부모 경로 하나로 내려감.

**문제 상황**
일반 FSM에서 공통 전이가 반복되면 상태가 늘수록 전이가 N²으로 증가:
```
Standing → Attacking   (전이 1)
Crouching → Attacking  (전이 2)
Running → Attacking    (전이 3)
// 이동 상태 10개가 되면 Attacking 전이만 10개 필요
```
HFSM은 `Moving(부모) → Attacking` 전이 하나로 이동 상태 전체를 대체.

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

**언제 쓰나 / 피할 때**
- ✅ 공통 전이가 3개 이상 반복될 때 (여러 자식 상태 → 같은 목적지)
- ✅ 부모 상태가 공통 Enter/Exit 동작을 공유해야 할 때
- ❌ 총 상태 수 < 8개 — 일반 FSM이 더 단순하고 추적 쉬움
- ❌ 상태 간 공통점이 없을 때 — 계층이 없으면 복잡도만 증가

⚠ **주의점**
- **같은 부모 내 전이** — 부모 Enter/Exit를 재호출하지 않으려면 전이 로직에서 공통 조상 탐색 필요. 안 하면 공통 초기화가 매번 리셋됨
- **깊이 제한** — 3단계 이상이면 Enter/Exit 호출 순서 추적이 어려워짐. 2단계로 충분한 경우가 대부분
- **HFSM vs FSM 선택** — 공통 전이가 3개 이상 반복될 때 HFSM이 유효. 상태 수 < 8이면 일반 FSM이 더 단순


#행위 #상태머신 #시스템
> 관련: [[design-pattern-notes]] 항목 4 State (기본 FSM) | 종속성: `#OOP` `#언어독립`

## 4. State (Enter/Exit + 브로드캐스트)

_Enter/Exit 훅으로 상태 전이를 캡슐화하고, 전이 발생 시 Observer로 외부에 통지하는 FSM 노드 패턴._

**직관**
신호등 — 빨강↔파랑 전환 시 "진입(켜짐)"과 "퇴장(꺼짐)" 동작이 명확히 구분되고, 바뀔 때 주변에 통지.

**문제 상황**
if/else 분기로 상태를 관리하면 상태 추가마다 모든 분기를 검토해야 함:
```csharp
void Update()
{
    if (_state == "idle")        { PlayIdleAnim(); if (moving) _state = "run"; }
    else if (_state == "run")    { PlayRunAnim();  if (attacking) _state = "attack"; }
    else if (_state == "attack") { PlayAttackAnim(); /* 종료 처리... */ }
    // 새 상태 추가 = 모든 else if 블록 검토 필요
}
```
State 패턴으로 상태별 Enter/Update/Exit를 캡슐화하면 상태 추가가 새 클래스 하나로 격리.

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

**언제 쓰나 / 피할 때**
- ✅ 상태별로 Enter/Update/Exit 동작이 명확히 다를 때
- ✅ 상태 전이를 외부(UI, Sound)에 통지해야 할 때
- ❌ 단순 bool flag 하나로 충분한 경우 — `isAttacking = true/false`가 더 단순
- ❌ 상태가 2개뿐인 토글 — if/else가 오히려 명확

⚠ **주의점**
- **Exit → Enter 순서** — Exit 먼저, Enter 나중. 반대면 새 상태의 Enter가 이전 리소스를 참조할 때 충돌
- **Enter 내부 재전이** — Enter()에서 Change()를 호출하면 재귀 전이. Guard flag 또는 큐 방식으로 방어
- **이벤트 구독 해제** — StateMachine 파괴 시 OnTransition 구독 해제 안 하면 memory leak


#행위 #상태머신 #시스템
> 관련: [[design-pattern-notes]] 항목 1 HFSM (계층 확장), 항목 16 Observer (브로드캐스트 구현 매체) | 종속성: `#OOP` `#언어독립`

## 6. Template Method

_부모 클래스가 알고리즘의 골격(호출 순서)을 정의하고, 세부 단계는 자식 클래스가 override로 채우는 패턴._

**직관**
요리 레시피 — "재료 손질 → 볶기 → 간 맞추기" 순서는 고정, 각 단계에서 뭘 넣는지는 요리마다 다름.

**문제 상황**
여러 서브클래스가 같은 알고리즘 순서를 각자 구현하면 순서 불일치 버그 발생:
```csharp
class RangedEnemy { void ExecuteTurn() { Move(); Attack(); Perceive(); } } // 감지를 나중에?
class MeleeEnemy  { void ExecuteTurn() { Perceive(); Attack(); Move(); } } // 이동을 마지막에?
// 순서를 강제할 방법 없음 → 서브클래스마다 다른 버그
```
Template Method로 골격을 부모가 고정하면 서브클래스는 "뭘 할지"만 결정, "언제 할지"는 부모가 보장.

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

**Strategy(항목 7)와의 차이**

| | Template Method | Strategy |
|---|---|---|
| 확장 방법 | 상속 (자식 클래스) | 컴포지션 (다른 객체) |
| 런타임 교체 | 불가 | 가능 |
| 결합도 | 부모-자식 강결합 | 느슨한 결합 |

**언제 쓰나 / 피할 때**
- ✅ 여러 서브클래스가 동일한 처리 순서를 따라야 할 때
- ✅ 공통 골격 코드 중복이 많을 때
- ❌ 런타임에 알고리즘을 교체해야 할 때 — Strategy(항목 7) 사용
- ❌ 상속 계층이 2단계 이상 깊어질 때 — Strategy로 전환 검토

⚠ **주의점**
- **골격 메서드 보호** — `ExecuteTurn`은 자식이 override 못하도록 `sealed` 처리
- **상속 깊이** — 2단계 이상 깊어지면 Strategy로 전환 검토
- **선택적 훅** — override 강제가 아닌 `virtual` + 빈 기본 구현으로 선택지 부여


#행위 #상속
> 관련: [[design-pattern-notes]] 항목 7 Strategy (상속 대신 컴포지션 대안) | 종속성: `#OOP` `#상속`

## 7. Strategy

_동일 시그니처의 알고리즘을 인터페이스/함수로 캡슐화해서 런타임에 교체 가능하게 하는 패턴._

**직관**
캐릭터 가방 속 무기 교체 — 공격 방식은 바뀌지만 "공격한다"는 인터페이스는 같음. 캐릭터 코드는 건드리지 않고 무기만 교체.

**문제 상황**
무기마다 다른 공격 방식을 if/else로 분기하면:
```csharp
void Attack(Character target)
{
    if (_weaponType == "sword")      target.TakeDamage(PhysicalPower);
    else if (_weaponType == "bow")   target.TakeDamage(PhysicalPower * 0.8f);
    else if (_weaponType == "staff") target.TakeDamage(MagicPower * 1.5f);
    // 새 무기 추가 = 이 메서드 수정 + 기존 분기 재테스트 필요
}
```
Strategy로 알고리즘을 캡슐화하면 새 무기 = 새 클래스 1개. 기존 코드 무수정.

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

**언제 쓰나 / 피할 때**
- ✅ 동일 시그니처 알고리즘이 3종 이상, 런타임 교체 필요 시
- ✅ 알고리즘 추가 시 기존 코드를 건드리고 싶지 않을 때 (OCP)
- ❌ 알고리즘 종류가 고정이고 교체 없음 — Template Method(항목 6)가 더 단순
- ❌ 무상태 함수 1-2개 — `Action<>`/`Func<>` 직접 사용이 더 단순

⚠ **주의점**
- **상태 유무** — 전략 객체가 상태를 가져야 하면 인터페이스 방식, 순수 함수라면 `Action`/`Func`이 더 단순
- **런타임 교체 없으면** — Template Method(항목 6)가 더 단순한 선택
- **전략 생성 비용** — 매 호출마다 `new Strategy()`면 GC 압력. 미리 생성해두거나 Pool(항목 18) 사용


#행위 #확장성
> 관련: [[design-pattern-notes]] 항목 6 Template Method (상속 기반 대안), 항목 17 Callback (함수형 Strategy) | 종속성: `#OOP` `#FP` `#언어독립`

## 9. Memento

_객체 내부 상태를 외부에 캡슐화해 저장하고 나중에 복원하는 패턴. 내부 구조를 노출하지 않음._

**직관**
게임 세이브 포인트 — "지금 상태를 스냅샷으로 저장해두고, 나중에 그 시점으로 복원". 내부 구조를 열람 없이 저장.

**문제 상황**
외부에서 상태를 저장하려면 내부 필드를 public으로 강제 노출해야 함:
```csharp
class Character
{
    public int Hp;        // 원래는 private이어야 함
    public int Mp;
    public Vector3 Pos;
}
// 저장자가 내부 구조를 알아야 함 → 캡슐화 파괴
var checkpoint = (character.Hp, character.Mp, character.Pos); // 어색한 튜플
```
Memento로 내부에서 스냅샷을 생성하면 `private` 유지 + 저장자는 Memento 타입만 보관.

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

**언제 쓰나 / 피할 때**
- ✅ Undo/Redo, 체크포인트/롤백이 필요할 때
- ✅ 내부 구현 노출 없이 상태를 저장해야 할 때
- ❌ 저장 빈도가 매 프레임 수준 — 메모리 폭발. 델타 저장 또는 Command(항목 10) 조합 검토
- ❌ 상태에 참조 타입이 많을 때 — 깊은 복사 비용 측정 필요

⚠ **주의점**
- **얕은 복사 함정** — 상태에 `List<T>` 같은 참조 타입이 있으면 스냅샷 저장 시 깊은 복사 필요. 아니면 원본 변경 시 Memento도 변경됨
- **메모리 비용** — 저장 빈도 높으면 메모리 증가. 저장 필드 최소화 또는 압축 검토
- **Command(항목 10)와 조합** — Undo/Redo 시스템은 Command(실행 내역) + Memento(상태 스냅샷) 조합


#행위
> 관련: [[design-pattern-notes]] 항목 10 Command (Undo와 조합), csharp-syntax-notes record (Memento 구현체로 적합) | 종속성: `#OOP` `#언어독립`

## 10. Command

_요청(동작)을 객체로 캡슐화해 나중에 실행·취소·큐잉·로깅할 수 있게 하는 패턴._

**직관**
식당 주문서 — "스테이크 하나"라는 행동을 종이에 적어두면 나중에 실행, 취소, 재실행, 묶음 처리가 가능.

**문제 상황**
행동을 직접 함수로 호출하면 Undo가 불가능:
```csharp
void OnMoveButton()
{
    player.Position += Vector3.right;  // 실행됨
    // 취소하려면? 이전 위치를 어디 저장했지?
    // 대기열에 넣으려면? 함수 포인터를 어떻게 저장하지?
}
```
Command 객체로 캡슐화하면 실행 내역을 스택에 보존 → Undo 가능, 큐 삽입 가능, 로깅 가능.

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

**언제 쓰나 / 피할 때**
- ✅ Undo/Redo 시스템이 필요할 때
- ✅ 행동을 큐에 넣어 나중에 실행하거나, 취소 조건부 실행이 필요할 때
- ✅ 행동 로그/리플레이 기능 필요 시
- ❌ 단순 한 번 실행, 취소/큐잉 없음 — 직접 메서드 호출이 더 명확

⚠ **주의점**
- **Undo의 완전성** — 부수효과(사운드, 이펙트)까지 Undo하면 복잡도 폭발. 부수효과는 Undo 대상에서 제외하는 것이 일반적
- **Command 생성 비용** — 고빈도 입력에서 매 입력마다 `new`면 GC 압력. Pool(항목 18) 사용
- **Macro** — 여러 Command를 묶어 실행하는 CompositeCommand = Command + Composite(항목 15) 조합


#행위
> 관련: [[design-pattern-notes]] 항목 9 Memento (Undo 상태 복원), 항목 15 Composite (CompositeCommand), 항목 18 Object Pooling (Command 객체 재사용) | 종속성: `#OOP` `#FP` `#언어독립`

## 12. Chain of Responsibility

_요청을 처리할 핸들러를 체인으로 연결하고, 각 핸들러가 처리하거나 다음으로 넘기는 패턴._

**직관**
민원 처리 체계 — 창구 직원이 처리 못 하면 팀장, 팀장이 못 하면 부서장으로 자동 넘어감. 요청자는 누가 처리할지 모름.

**문제 상황**
입력 우선순위를 하나의 메서드에서 처리하면 시스템 간 로직이 혼재:
```csharp
void HandleInput(InputEvent e)
{
    if (EventSystem.IsPointerOverUI())  { HandleUI(e);     return; }
    if (e.type == InputType.Attack)     { player.Attack(); return; }
    if (e.type == InputType.Interact)   { Interact();      return; }
    // 새 우선순위 추가 = 이 메서드 수정. UI/게임/시스템 로직이 한 메서드에 혼재
}
```
Chain으로 각 핸들러를 분리하면 독립 코드 유지 + 체인 순서만 바꿔 우선순위 변경 가능.

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

**언제 쓰나 / 피할 때**
- ✅ 처리 주체가 런타임에 달라지거나, 우선순위 체계가 명확할 때
- ✅ 처리 여부를 각 핸들러가 스스로 판단해야 할 때
- ❌ 처리 주체가 항상 고정 — 직접 호출이 더 명확
- ❌ 체인의 모든 핸들러가 처리해야 하는 경우 — Observer(항목 16)가 적합

⚠ **주의점**
- **체인 끝 처리** — 모든 핸들러가 처리 못 할 때를 위한 NullHandler를 체인 끝에 추가 권장
- **순서 의존성** — 체인 순서가 곧 우선순위. UI가 Player보다 먼저여야 하는 것처럼 순서 실수 = 버그
- **디버깅 어려움** — 어디서 소비됐는지 추적하기 어려움. 처리 로그 추가 권장


#행위 #이벤트
> 관련: [[design-pattern-notes]] 항목 16 Observer (이벤트 기반 대안) | 종속성: `#OOP` `#언어독립`

## 16. Observer

_주체(Subject)가 상태 변경을 구독자(Observer)에게 자동으로 통지하는 패턴. 느슨한 결합으로 1:N 의존성 구현._

**직관**
신문 구독 — HP가 바뀌면 "관심 있는 모든 시스템"에 자동 배송. 발행자는 구독자가 누구인지 모름.

**문제 상황**
PlayerStatus가 변경을 직접 통지하면 구독자를 하드코딩해야 함:
```csharp
class PlayerStatus
{
    HPBar _hpBar; SoundManager _sound; AchievementSystem _ach; // 구독자를 직접 알아야 함
    void TakeDamage(int dmg)
    {
        _hp -= dmg;
        _hpBar.UpdateUI(_hp);
        _sound.PlayHitSound();
        _ach.CheckLowHpAchievement(_hp);
        // 새 반응 시스템 추가 = PlayerStatus 수정
    }
}
```
Observer로 이벤트를 발행하면 `OnHpChanged?.Invoke(_hp)` 한 줄. 구독 추가는 PlayerStatus 외부에서.

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

**언제 쓰나 / 피할 때**
- ✅ 상태 변경에 3개 이상의 시스템이 반응해야 할 때
- ✅ 발행자가 구독자를 직접 참조하면 안 될 때 (계층 역방향 참조 등)
- ❌ 1:1 통지 — Callback(항목 17)이 더 단순
- ❌ 결과값이 필요한 통지 — 리턴값 없는 event 대신 함수 직접 호출

⚠ **주의점**
- **구독 해제 누수** — 가장 흔한 버그. `OnDestroy`에서 `-=` 또는 `Dispose()` 반드시
- **이벤트 순환** — A의 핸들러에서 B 상태 변경 → B의 핸들러에서 A 상태 변경 → 무한 루프. Guard flag 필요
- **정적 이벤트 위험** — `static event`는 인스턴스 파괴 후에도 구독이 GC되지 않음. 수동 해제 필수


#행위 #이벤트
> 관련: [[design-pattern-notes]] 항목 4 State (브로드캐스트 구현), 항목 23 단일 이벤트 + 추상 Entry (이종 이벤트 통합) | 종속성: `#OOP` `#FP` `#언어독립`

## 17. Callback

_함수를 인자로 전달해서 피호출자가 결정한 시점에 실행하게 하는 패턴. 완료 통지와 결과 반환에 사용._

**직관**
택배 수령 알림 — "배달 완료되면 연락해줘"를 맡기고 기다림. 배달부(피호출자)는 완료 시점에 약속된 함수를 실행.

**문제 상황**
비동기 완료를 polling으로 기다리면 매 프레임 낭비:
```csharp
bool _loadComplete; Sprite _loadedSprite;

void Update()
{
    if (_loadComplete) { _icon.sprite = _loadedSprite; _loadComplete = false; }
    // 완료 전까지 매 프레임 if 체크 + 상태 변수 관리 필요
}
```
Callback으로 "완료 시 실행할 함수"를 전달하면 Update 불필요, 상태 변수 불필요.

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

**Observer(항목 16)과의 차이**
- Observer: 1:N, 구독자가 등록/해제. 상태 변경 통지 목적
- Callback: 1:1, 호출자가 함수 직접 전달. 완료 통지/결과 반환 목적

**언제 쓰나 / 피할 때**
- ✅ 비동기 완료 통지, 결과 반환이 1:1로 필요할 때
- ✅ 함수 실행 시점을 피호출자에게 위임할 때 (비동기 로드, 애니메이션 완료 등)
- ❌ 다수 구독자 필요 — Observer(항목 16) 사용
- ❌ 콜백 중첩 3단계 이상 — async/await 또는 코루틴으로 평탄화

⚠ **주의점**
- **콜백 지옥** — 콜백 중첩이 깊어지면 들여쓰기 폭발. async/await 또는 코루틴 + 완료 콜백으로 평탄화
- **null 체크** — `onComplete?.Invoke()`
- **캡처 변수 수명** — 람다가 외부 변수를 캡처할 때 변수가 파괴된 뒤에 콜백이 실행되면 NRE


#행위
> 관련: [[design-pattern-notes]] 항목 16 Observer (1:N 이벤트 대안), csharp-syntax-notes async/await | 종속성: `#OOP` `#FP` `#언어독립`

## 23. 단일 이벤트 + 추상 Entry 디스패치

_`Action<TBase>` 단일 이벤트 + abstract base class로 이종 데이터를 하나의 채널로 발행하고, 수신자가 다형성으로 처리하는 패턴._

**직관**
"사건 접수 단일 창구" — 폭행이든 절도든 유형과 무관하게 한 창구에 접수. 처리자가 유형을 보고 분류.

**문제 상황**
이벤트 종류마다 채널을 만들면 구독자가 N개 구독 필요 + 추가 시 모든 구독자 코드 수정. 설명 내 "나쁜 방법" 코드 참조.

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

**언제 쓰나 / 피할 때**
- ✅ 의미적으로 같은 도메인의 이벤트 3종 이상이 같은 구독자 세트에 전달될 때
- ✅ 새 이벤트 종류가 자주 추가될 것으로 예상될 때
- ❌ 이벤트 종류가 1-2개 — 개별 이벤트가 더 명확하고 타입 안전
- ❌ 의미적으로 다른 이벤트를 한 채널에 — switch case가 길어지고 의미 혼탁

⚠ **주의점**
- **switch 누락** — 새 Entry 서브클래스를 추가했는데 수신자 switch에 case가 없으면 조용히 무시됨. `default: Debug.LogWarning` 또는 throw 권장
- **단일 채널 과부하** — 의미적으로 다른 이벤트를 한 채널에 넣으면 수신자 switch가 길어짐. 의미적으로 묶이는 이벤트들만 같은 채널로
- **Entry 불변성** — 이벤트는 여러 수신자에게 전달되므로 수신자가 Entry를 수정하면 다음 수신자에 영향. `readonly` 필드 또는 `record` 타입으로 불변 설계


#행동 #이벤트
> 관련: [[design-pattern-notes]] 항목 16 Observer (기반 이벤트 패턴), csharp-syntax-notes #패턴매칭 (switch expression) | 종속성: `#OOP` `#언어독립`


## 25. Effect 삼분 (Apply / Emit / Describe)

_하나의 효과를 **Apply**(수치 계산·상태 변경) · **Emit**(파티클·사운드·팝업) · **Describe**(툴팁 텍스트) 세 메서드로 고정 분리하는 abstract base class 패턴._

**직관**
"영수증 끊기 → 물건 건네기 → 전단지 쓰기" — 계산(Apply)·전달(Emit)·광고(Describe) 세 동작은 독립. 광고 문구가 바뀌어도 계산 코드를 건드릴 이유가 없다.

**문제 상황**
효과 1건에 수치 계산, VFX 재생, 툴팁 문자열 생성이 섞이면 세 가지 이유로 동시에 바뀌는 신 God-method가 된다. 로컬라이제이션 담당자가 효과 수치 코드를 건드려야 하고, VFX 프리팹을 바꾸면 배틀 로직 테스트가 깨진다.

**설명**

```csharp
// 추상 베이스 — 세 메서드를 계약으로 강제
[Serializable]
public abstract class AttributeEffect
{
    // 수치 계산 + 상태 변경 전용. UI 코드 없음.
    // 반환값은 후속 Emit/로그에 전달할 결과 데이터.
    public abstract EffectOutcome Apply(in AttrEffectContext ctx);

    // 팝업·파티클·사운드·배틀로그 전용. Apply 완료 후 호출.
    // Apply 결과(outcome)를 받아 "무엇이 일어났는지"만 표시.
    public abstract void Emit(in AttrEffectContext ctx, in EffectOutcome outcome);

    // 툴팁 텍스트 반환. 배틀 컨텍스트 없이 호출됨.
    public abstract (string main, string reinforced) Describe();
}

// 구체 구현 — Vampire 흡혈 효과
public sealed class VampireAttributeEffect : AttributeEffect
{
    public int basePercent;

    public override EffectOutcome Apply(in AttrEffectContext ctx)
    {
        int heal = Mathf.RoundToInt(ctx.DamageDealt * basePercent / 100f);
        int actual = ctx.Bm.Health.HealPlayer(heal, emitPopup: false); // Emit에서 따로 발행
        return new EffectOutcome(actual, 0, 0);
    }

    public override void Emit(in AttrEffectContext ctx, in EffectOutcome outcome)
    {
        ctx.Emitter?.SpawnPlayerHeal(outcome.Heal, allowZero: true); // 팝업만
    }

    public override (string main, string reinforced) Describe()
    {
        string main = L.GetFormat("attr_effect_vampire_fmt", basePercent);
        return (main, string.Empty);
    }
}
```

**호출 순서**
```
[배틀 루프]
  outcome = effect.Apply(ctx)        // 1. 계산·상태 변경
  effect.Emit(ctx, outcome)          // 2. 연출 발행
  log.Append(effect.BuildLogRow(…))  // 3. 로그 (선택)

[툴팁 시스템]
  (main, reinforced) = effect.Describe()  // 배틀과 무관한 경로
```

Apply가 `EffectOutcome` (readonly struct)을 반환하면 Emit이 그 값을 받아 표시. Emit이 Apply 결과를 자체 계산하지 않으므로 "표시된 숫자"와 "실제 처리된 숫자"가 항상 일치한다.

**언제 쓰나 / 피할 때**
- ✅ 하나의 효과 개념이 수치 변화 + 연출 + 텍스트 설명을 동시에 갖는 경우
- ✅ 효과 종류가 5개 이상으로 늘어날 때 — 추가는 새 서브클래스 1개 작성으로 완결
- ✅ 툴팁·배틀·테스트 세 경로를 각각 독립적으로 실행해야 할 때
- ❌ 효과가 1-2개에 불과할 때 — 일반 메서드로 충분, 추상화 오버헤드 불필요
- ❌ 연출이 아예 없는 순수 수치 효과 — Emit을 빈 메서드로 남기면 계약이 형식화됨

⚠ **주의점**
- **Emit에서 재계산 금지** — `outcome`을 다시 계산하지 말고 Apply에서 받은 값을 그대로 표시. Apply/Emit 간 수치 불일치가 생기면 디버그가 매우 어렵다
- **Describe는 무상태** — 배틀 컨텍스트(`AttrEffectContext`)를 받지 않음. 툴팁은 전투 중이 아닌 UI 단계에서도 표시되므로 ctx가 없어도 동작해야 한다
- **SynergyAttrEffect는 Describe 없음** — 시너지 효과 설명은 SynergyDataSO가 따로 보유. SynergyAttrEffect는 Apply + Emit만 계약 (game-technique-notes 항목 14 참조)
- **Apply의 부수효과** — Apply는 "상태 변경 포함"이지만 UI 발행은 금지. `HealPlayer(emitPopup: false)`처럼 팝업 억제 플래그를 명시적으로 넘겨야 한다


#행위 #구조
> 관련: design-pattern-notes 항목 16 Observer (Emit 발행 채널), game-technique-notes 항목 14 속성·시너지 효과 분리 (본 패턴의 도메인 적용) | 종속성: `#OOP` `#언어독립`
