# C# 문법 / 키워드 노트

> 다루는 축: C# 언어 자체의 키워드 / 연산자 / 문법. 빠른 회상용 cheatsheet
> 다루지 않는 축: 디자인 패턴(→ [[design-pattern-notes]]), Unity API(→ [[unity-feature-notes]]), 단편 트릭(→ [[game-misc-notes]])
> 적용 범위: C# 전 버전 (사용 시점 C# 버전을 항목에 명시)
> 관련 노트: [[design-pattern-notes]] #19 CRTP, [[game-misc-notes]] #12 Array.Empty
> 등재 기준: **본인이 코드에 한 번이라도 쓴 것**. Microsoft Learn 문서를 옮기는 게 아니라 "내가 실제 사용한 것만" 누적
> 작성 시작: 2026-05-15

---

## 태그 목록

### 카테고리
- `#접근제어` `#null처리` `#패턴매칭` `#제네릭` `#표현식` `#자료형` `#지시문` `#속성` `#비동기` `#LINQ`

### C# 버전
- `#C#7` `#C#8` `#C#9` `#C#10` `#C#11` `#C#12`

### 빈도
- `#필수` `#보조` `#일회성`

---

# 인덱스

## 접근/상속 제어자

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 1 | `public` / `private` / `protected` / `internal` | 표준 접근 한정자 | `public class Foo {}` |
| 2 | `abstract` (class) | 인스턴스화 불가, 자식 구현 강제 | `abstract class Base { abstract void Foo(); }` |
| 3 | `abstract` (method) | 자식 구현 의무 | `abstract void Update();` |
| 4 | `virtual` / `override` | 가상 메서드 / 재정의 | `protected virtual void OnInit() {}` |
| 5 | `sealed` (class) | 상속 금지 (의도 명시 + 컴파일러 최적화) | `sealed class FlowDirector {}` |
| 6 | `sealed` (override) | override 추가 재정의 차단 | `sealed override void Foo()` |
| 7 | `new` (멤버) | 부모 멤버 가리기 (override 아님 — 정적 디스패치) | `new void Foo()` |
| 8 | `readonly` (필드) | 생성자 이후 변경 불가 | `readonly int max;` |
| 9 | `const` | 컴파일 타임 상수 | `const float PI = 3.14f;` |
| 10 | `static` | 인스턴스 없이 접근 | `static int counter;` |

## null 처리

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 11 | `?.` null-conditional | null이면 null 반환 (체이닝 안전) | `obj?.Method()?.Foo` |
| 12 | `??` null-coalescing | null이면 우항 | `x ?? "default"` |
| 13 | `??=` null-coalescing assign | null일 때만 대입 (`#C#8`) | `cache ??= new Dict()` |
| 14 | `?` (값 타입) nullable | 값 타입을 nullable로 (`Nullable<T>`) | `int? x = null;` |
| 15 | `?` (참조 타입) nullable annotation | nullable reference (`#C#8`, 활성화 시) | `string? name;` |
| 16 | `!` null-forgiving | "여기는 null 아님" 컴파일러 단언 | `x!.Foo()` |
| 17 | `is null` / `is not null` | null 비교 (오버로딩 회피) | `if (x is not null)` |

## 패턴 매칭

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 18 | `is` (타입 검사) | 타입 일치 여부 | `if (x is string)` |
| 19 | `is` (변수 바인딩) | 타입 검사 + 캐스트 동시 (`#C#7`) | `if (x is int n) Use(n);` |
| 20 | `is` (속성 패턴) | 객체 속성 매칭 (`#C#8`) | `if (p is { Age: > 18 })` |
| 21 | switch expression | 표현식 형태 switch (`#C#8`) | `x switch { 1 => "a", _ => "b" }` |
| 22 | tuple pattern | 튜플 매칭 (`#C#8`) | `(atk, def) switch { (Fire, Wind) => 1.2f, _ => 1f }` |
| 23 | `_` discard | 값 무시 / 와일드카드 | `(_, y) = tuple;` |
| 24 | relational pattern | 비교 연산 패턴 (`#C#9`) | `x is > 0 and < 100` |
| 25 | `and` / `or` / `not` 패턴 | 패턴 결합 (`#C#9`) | `c is >= 'a' and <= 'z'` |

## 제네릭 / 제약

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 26 | `class Foo<T>` | 제네릭 클래스 | `class Pool<T> { T Get(); }` |
| 27 | `void Foo<T>()` | 제네릭 메서드 | `T GetController<T>() where T : Component` |
| 28 | `where T : class` | 참조 타입만 | |
| 29 | `where T : struct` | 값 타입만 | |
| 30 | `where T : new()` | 기본 생성자 필요 | `new T()` 가능 |
| 31 | `where T : Foo` | Foo의 자식만 | |
| 32 | `where T : Foo<T>` | **CRTP** 자기 참조 | → [[design-pattern-notes]] #19 |
| 33 | `where T : unmanaged` | 비관리 타입만 (Span, P/Invoke) | |
| 34 | `default(T)` | T의 기본값 | `T x = default;` |

## 표현식 / 람다

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 35 | `=>` expression-bodied member | 표현식 메서드/프로퍼티 (`#C#6`) | `public int Count => list.Count;` |
| 36 | `=>` lambda | 람다식 | `x => x * 2` |
| 37 | `Action` / `Func<T>` | delegate 표준 형식 | `Action<int> handler;` |
| 38 | `delegate` 키워드 | 익명 메서드 (구식, lambda로 대체) | `delegate { return 1; }` |
| 39 | `nameof` | 컴파일 타임 이름 문자열 (`#C#6`) | `nameof(MyVar)` → `"MyVar"` |
| 40 | `typeof` | 타입 객체 | `typeof(int)` → `Type` |
| 41 | `default` 리터럴 | 타입 추론 default (`#C#7.1`) | `int x = default;` |

## 자료형 정의

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 42 | `class` | 참조 타입 | `class Foo {}` |
| 43 | `struct` | 값 타입 (스택, 복사 의미) | `struct Vec2 { float x, y; }` |
| 44 | `interface` | 인터페이스 (다중 구현) | `interface IInit { void Init(); }` |
| 45 | `enum` | 열거형 (정수 기반) | `enum Grade { Normal, Rare, Epic }` |
| 46 | `[Flags] enum` | 비트 플래그 열거형 | `[Flags] enum Layer { UI=1, FX=2, BG=4 }` |
| 47 | `delegate` | 함수 시그니처 타입 | `delegate void Handler(int v);` |
| 48 | `event` | 외부 invoke 차단된 이벤트 | `public event Action OnChanged;` |
| 49 | `record` | 값 비교 immutable 클래스 (`#C#9`) | `record Point(int x, int y);` |
| 50 | `partial` | 여러 파일에 클래스 분할 | `partial class Foo {}` |
| 51 | `using static` | 정적 멤버 직접 임포트 | `using static System.Math;` |
| 52 | 자동 프로퍼티 | `{ get; set; }` 자동 백업 필드 | `public int X { get; private set; }` |
| 53 | init-only 프로퍼티 | 생성 시에만 대입 (`#C#9`) | `public int X { get; init; }` |

## 컴파일러 지시문 / 속성

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 54 | `#if` / `#else` / `#endif` | 조건부 컴파일 | `#if UNITY_EDITOR ... #endif` |
| 55 | `#region` / `#endregion` | 코드 접기 영역 | `#region UI Setup ... #endregion` |
| 56 | `#pragma warning disable` | 특정 경고 억제 | `#pragma warning disable CS0649` |
| 57 | `[Conditional("X")]` | 심볼 없으면 호출 자체 제거 | `[Conditional("DEBUG")] void Log() {}` |
| 58 | `[Obsolete]` | 사용 시 경고/에러 | `[Obsolete("Use Foo2 instead")]` |
| 59 | `[Serializable]` | 직렬화 가능 표시 | → [[unity-feature-notes]] #4 |
| 60 | `[CallerMemberName]` | 호출자 이름 자동 주입 | `void Log([CallerMemberName] string n="")` |

## 비동기 / 이터레이터

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 61 | `yield return` | 이터레이터 한 항목 반환 (지연 실행) | `yield return new WaitForSeconds(1);` |
| 62 | `yield break` | 이터레이터 종료 | `if (done) yield break;` |
| 63 | `IEnumerable<T>` / `IEnumerator` | 이터레이터 인터페이스 | → Unity 코루틴은 `IEnumerator` |
| 64 | `async` / `await` | 비동기 메서드 (`#C#5`) | Unity에선 코루틴 대신 선택 사용 |
| 65 | `Task` / `Task<T>` | 비동기 작업 표현 | `async Task<int> Fetch()` |

## LINQ / 컬렉션

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 66 | `from ... in ... select` | 쿼리 식 (잘 안 씀, 메서드 체인 선호) | `from x in list where x>0 select x` |
| 67 | `.Where(...)` | 필터 | `list.Where(x => x.Active)` |
| 68 | `.Select(...)` | 변환 | `list.Select(x => x.Name)` |
| 69 | `.ToList()` / `.ToArray()` | 컬렉션 변환 + 즉시 실행 | |
| 70 | `.ToDictionary(k, v)` | 키-값 매핑 + dict 빌드 | `items.ToDictionary(i => i.Id, i => i)` |
| 71 | `.FirstOrDefault(...)` | 첫 매칭 또는 default | `list.FirstOrDefault(x => x.Id == id)` |
| 72 | `.Any(...)` / `.All(...)` | 존재 / 모두 검사 | `list.Any(x => x.Done)` |
| 73 | `Array.Empty<T>()` | GC 회피 빈 배열 | → [[game-misc-notes]] #12 |

---

# 풀노트

> 각 항목 형식: **핵심 개념** (mental model) → **비교표** → **전체 예시** (정의+호출 양쪽) → **함정** (왜 함정인지 이유 포함) → **대표 용도 요약**

## 접근/상속 제어자

### 1. 접근 한정자 (`public` / `private` / `protected` / `internal`)

**기능**: 클래스·메서드·필드에 접근 가능한 범위를 제한한다.

**핵심 개념**: C#의 기본 접근자는 `private` — 의도적으로 공개할 것만 명시하는 방향이 원칙.
- 타입(class/struct/interface) 수준 기본값: `internal`
- 멤버(메서드/필드/프로퍼티) 수준 기본값: `private`

**비교**:
| 한정자 | 접근 가능 범위 |
|---|---|
| `public` | 어디서든 |
| `private` | 선언 클래스 내부만 (멤버 기본값) |
| `protected` | 선언 클래스 + 자식 클래스 |
| `internal` | 같은 어셈블리(프로젝트) 내 (타입 기본값) |
| `protected internal` | `protected` **또는** `internal` — 더 넓음 |
| `private protected` | `protected` **이면서** `internal` — 더 좁음 (`#C#7.2`) |

**용법**:
```csharp
public class Character { }              // 외부 어디서든 접근
private int _hp;                        // 이 클래스 내부만
protected virtual void OnDead() { }     // 자식 클래스에서 재정의 가능
internal class DebugHelper { }          // 같은 프로젝트 내부용
```

**함정 — `protected internal` vs `private protected`**:
이름이 비슷하지만 AND/OR 조건이 반대라 혼동하기 쉽다.
```csharp
protected internal void Foo() { }  // protected OR internal — 더 넓음
private protected  void Bar() { }  // protected AND internal — 더 좁음
```
`protected internal`: 자식 클래스면 어셈블리 무관 접근 가능 + 같은 어셈블리면 상속 무관 접근 가능.
`private protected`: 자식 클래스 **중에서** 같은 어셈블리에 있는 것만. Unity 단일 어셈블리 프로젝트에서는 거의 쓸 일 없음.

**대표 용도**:
- `private`: 내부 상태 캡슐화, 외부 API 최소화
- `protected`: 상속 계층에서만 공유할 훅 메서드 (`OnInit`, `OnDead` 등)
- `internal`: Editor 전용 유틸, 테스트용 헬퍼, 외부 패키지에 노출 안 할 내부 서비스

---

### 2~7. 상속 제어 (`abstract` / `virtual` / `override` / `sealed` / `new`)

**기능**: 메서드가 다형성에 참여하는 방식을 제어한다.

**핵심 개념**: 부모 타입 변수로 자식 인스턴스를 담았을 때 어떤 버전이 호출되는가.
- `virtual` + `override` → **런타임**에 실제 인스턴스 타입 기준으로 호출 (다형성)
- `new` (숨기기) → **컴파일 타임**에 변수 타입 기준으로 호출 (다형성 차단)

**비교**:
| 부모 선언 | 자식 override 가능? | 자식 override 의무? | 부모 구현 있음? |
|---|---|---|---|
| `virtual` | O | X | O |
| `abstract` | O | O | X |
| 일반 메서드 | X (`new`로 숨기기만 가능) | — | O |

**override vs new — 정의부터 호출까지**:
```csharp
class Base {
    public virtual void Foo() => Console.WriteLine("Base.Foo");
    public         void Bar() => Console.WriteLine("Base.Bar");
}

class Child : Base {
    public override void Foo() => Console.WriteLine("Child.Foo"); // 다형성 연결
    public new      void Bar() => Console.WriteLine("Child.Bar"); // 숨기기 (hiding)
}

Base  b = new Child();  // 변수 타입 = Base, 실제 인스턴스 = Child
b.Foo();  // → Child.Foo  (런타임: 실제 타입 Child를 본다)
b.Bar();  // → Base.Bar   (컴파일 타임: 변수 타입 Base만 본다)

Child c = new Child();  // 변수 타입 = Child
c.Foo();  // → Child.Foo
c.Bar();  // → Child.Bar  (변수가 Child면 Child 버전)
```

`new`의 함정: 자식 타입 변수(`Child c`)로 직접 쓸 때는 자식 버전이 호출되어 의도대로 보인다. 그러나 `List<Base>`에 담거나 메서드 파라미터로 `Base`를 받는 순간 부모 버전이 호출되어 조용히 버그가 된다. `override` 키워드가 빠졌을 때 컴파일러가 "use `new` to suppress" 경고를 내는 이유 — 실수로 `new`를 붙이면 다형성이 의도치 않게 끊긴다.

**base 호출 — override하면서 부모 버전도 실행**:
```csharp
class Child : Base {
    public override void Foo() {
        base.Foo();   // 부모 버전 먼저 실행
        // 추가 처리
    }
}
```
`new`로 숨긴 메서드도 `base.Bar()`로 부모 버전 호출은 가능하지만, 숨기기가 목적인데 명시 호출하는 경우는 거의 없다.

**abstract 사용 규칙**:
- `abstract` 메서드가 1개라도 있으면 클래스도 반드시 `abstract class`
- `abstract class`는 인스턴스화 불가 (`new AbstractBase()` 컴파일 에러)
- 자식이 `abstract` 멤버를 모두 `override`하지 않으면 자식도 `abstract`가 됨

```csharp
abstract class State {
    public abstract void Enter();      // 구현 없음, 자식 override 의무
    public abstract void Exit();
    public virtual  void Update() {}   // 기본 구현 있음, 자식은 선택
}

class IdleState : State {
    public override void Enter() { /* ... */ }  // 필수
    public override void Exit()  { /* ... */ }  // 필수
    // Update는 override 안 해도 됨
}
```

**abstract class vs interface 선택 기준**:
| | `abstract class` | `interface` |
|---|---|---|
| 구현 포함 | O | O (default 구현, C# 8+) |
| 상태(필드) 보유 | O | X |
| 다중 상속 | X (단일) | O (다중 구현 가능) |
| 생성자 | O | X |
| 언제 쓰나 | 공통 상태 + 공통 구현이 있는 계층 | 타입과 무관한 능력(행동) 계약 |

규칙: "is-a" 관계면 `abstract class`, "can-do" 관계면 `interface`.
예: `MonoBehaviour`를 상속하는 State 계층은 abstract class. `IDamageable`은 interface.

**sealed 두 위치**:
```csharp
sealed class FinalState { }          // 이 클래스 자체를 상속 불가
class GrandChild : FinalState { }    // 컴파일 에러

class Child : Base {
    sealed override void Enter() { } // Child는 override했지만 Child의 자식은 재정의 불가
}
```
`sealed class`는 의도 명시(확장 불필요) + JIT이 vtable 조회 없이 직접 호출로 최적화(devirtualization).

**대표 용도 요약**:
- `abstract class`: 템플릿 메서드 패턴 — 공통 골격 + 세부 구현은 자식 의무
- `virtual`: 기본 동작 제공하되 자식이 커스터마이징할 훅 포인트
- `override`: virtual/abstract에 연결 — 다형성 참여 선언
- `new`: 의도적 숨기기(hiding) — 다형성을 끊는 게 목적일 때만 명시 사용
- `sealed class` / `sealed override`: 확장 차단 의도 명시 + JIT 최적화

---

### 8~10. 수정자 (`readonly` / `const` / `static`)

**기능**: 값의 변경 가능 여부와 인스턴스/클래스 소속을 제어한다.

**핵심 개념**: 세 키워드가 해결하는 문제가 다르다.
- `const`: "컴파일 타임에 값이 고정된다" — 빌드 시 소비 코드에 값 자체가 인라인됨
- `readonly`: "생성자에서만 설정 가능, 이후 변경 불가" — 런타임에 결정되는 불변값
- `static`: "클래스에 귀속, 모든 인스턴스가 공유" — 인스턴스 생성 없이 접근

**비교**:
| | 값 결정 시점 | 변경 가능 시점 | 인스턴스별? | 암묵적 static |
|---|---|---|---|---|
| `const` | 컴파일 타임 | 불가 | X | O |
| `readonly` | 런타임 (생성자) | 생성자 내만 | O (`static readonly` 제외) | X |
| `static` | 런타임 | 자유 | X | — |

**용법**:
```csharp
const float Pi = 3.14159f;             // 컴파일 타임 고정값 — 암묵적 static
readonly int _maxHp;                   // 생성자에서만 할당, 이후 불변
static int _instanceCount;            // 모든 인스턴스가 공유
static readonly int[] EmptyIds = {};  // 런타임 결정값을 전역 불변으로
```

**함정**:

`const` 인라인 함정: `const` 값은 참조하는 어셈블리에 컴파일 타임에 복사됨. 값을 변경해도 참조 어셈블리를 재빌드하지 않으면 구버전 값이 남아 있다.
```csharp
// LibA.dll
public const           int Version  = 1;  // 참조 어셈블리에 값 1이 인라인됨
public static readonly int VVersion = 1;  // 참조 어셈블리는 필드 주소를 참조

// LibA만 재빌드 후 Version=2로 변경 시:
// const 참조: 여전히 1 (LibB도 재빌드해야 2가 됨)
// static readonly 참조: 2 (LibA 재빌드만으로 반영)
```
외부에 공개하는 상수는 `static readonly` 권장.

`readonly List<T>` 함정: 참조의 재할당은 불가하지만 참조된 객체의 내용 변경은 가능.
```csharp
readonly List<int> _ids = new();
_ids = new List<int>();  // 컴파일 에러 — 참조 재할당 불가
_ids.Add(1);             // OK — 내용 변경은 가능
```

**대표 용도**:
- `const`: 타입 내부에서만 쓰는 수치 상수 (`private const float Speed = 5f;`)
- `static readonly`: 외부에 공개하는 불변값, 런타임 계산값의 전역 캐시
- `readonly`: 생성자 주입으로 설정하는 의존성 (`readonly IService _service`)

---

## null 처리

### 11~13. null 조건 연산자 (`?.` / `??` / `??=`)

**기능**: null 체크를 간결하게 표현하는 연산자 3종.

**비교**:
| 연산자 | 의미 | null일 때 결과 |
|---|---|---|
| `?.` | null이면 멤버 접근 건너뜀 | null 반환 |
| `??` | null이면 우항으로 대체 | 우항 값 |
| `??=` | null일 때만 우항을 대입 | 우항 값으로 갱신 |

**용법**:
```csharp
// ?. — 체이닝 중간에 null이 있어도 전체가 null로 안전하게 붕괴
string name = player?.Stats?.Name;        // player나 Stats가 null이면 null

// ?? — null 대체값 제공
string display = name ?? "Unknown";       // name이 null이면 "Unknown"

// ??= — 지연 초기화 (lazy init) 패턴
_cache ??= new Dictionary<int, Item>();   // null일 때만 new, 이미 있으면 유지
```

**대표 용도**:
- `?.`: 이벤트 발행 `OnChanged?.Invoke()` — 구독자 없을 때 NRE 방지
- `??`: 기본값 fallback, 선택적 파라미터 처리
- `??=`: 싱글턴 lazy init, 첫 접근 시 캐시 초기화

---

### 14~16. null 타입 선언 (`?` 값 타입 / `?` 참조 타입 / `!`)

**기능**: 타입 수준에서 null 허용 여부를 선언한다.

**핵심 개념**: `?`가 값 타입에 붙는 것과 참조 타입에 붙는 것은 완전히 다른 메커니즘이다.
- `int?`: 런타임에 실제로 `Nullable<int>` struct로 래핑됨 — null을 *값*으로 표현하는 실제 타입
- `string?`: 컴파일러 분석용 어노테이션만 — 런타임에 `string`과 완전히 동일, null을 막지 않음

**비교**:
| | 대상 | 런타임 변화 | 의미 |
|---|---|---|---|
| `int?` (`Nullable<int>`) | 값 타입 | `Nullable<T>` struct로 래핑 | null을 값으로 가질 수 있음 |
| `string?` | 참조 타입 | 없음 (어노테이션만) | null 가능함을 명시 (`#C#8`, NRT 활성화 필요) |
| `x!` | 표현식 | 없음 | "여기는 null 아님" — 컴파일러 경고 억제 |

**용법**:
```csharp
// 값 타입 nullable
int? score = null;
if (score.HasValue) Use(score.Value);  // 명시적 접근
int result = score ?? 0;               // null이면 기본값

// 참조 타입 nullable (Nullable Reference Types, C#8+)
string? playerName = GetName();        // "null 가능" 어노테이션
int len = playerName?.Length ?? 0;     // null-safe 접근

// ! null-forgiving
string name = GetMaybeNull()!;        // 경고 억제 — 개발자가 null 아님을 보증
```

**함정**:
- `!` (null-forgiving)은 컴파일러 경고만 억제, 런타임 null을 막지 않음. 실제로 null이면 NRE 발생.
- Unity는 NRT가 기본 비활성화. `<Nullable>enable</Nullable>` 설정 또는 파일 상단 `#nullable enable` 없이는 `string`과 `string?`이 동일하게 취급됨.
- `int?`의 `.Value`는 null 상태에서 호출하면 `InvalidOperationException`. `HasValue` 확인 또는 `?? 기본값` 패턴 사용.

---

### 17. `is null` vs `== null`

**기능**: null 비교. `is null`은 `==` 연산자 오버로딩을 우회한다.

**비교**:
```csharp
if (x == null) { }     // == 오버로딩 있으면 커스텀 로직 호출 가능
if (x is null) { }     // 항상 참조 null 비교 — 오버로딩 무시
if (x is not null) { } // C#9 부정 패턴
```

**Unity 주의**: `UnityEngine.Object` 계열은 `==` 오버로딩이 있어 `is null`과 동작이 다름. `Destroy()` 후 `== null`은 true지만 `is null`은 false. 의도에 맞는 쪽 선택 필요.

---

## 패턴 매칭

### 18~20. `is` 패턴의 진화

**기능**: 값이 특정 타입·조건에 부합하는지 검사하고, 동시에 변수를 바인딩한다.

**핵심 개념**: C# 버전마다 `is` 한 줄이 표현하는 범위가 확장되었다.
- C#6: 타입 검사만
- C#7: 검사 + 변수 바인딩 동시
- C#8: 객체 속성값까지 매칭 (속성 패턴)
- C#9: 비교 연산 + 논리 결합 (관계 패턴)

**버전별 비교**:
```csharp
// C#6: 타입 검사 + 별도 캐스트 (2단계)
if (x is string) { string s = (string)x; Use(s); }

// C#7: 검사 + 바인딩 동시 (1단계)
if (x is string s) { Use(s); }

// C#8: 속성 패턴 — 객체 내부 값까지 한 번에 매칭
if (unit is { Hp: 0, Team: Team.Enemy }) { }         // 타입 생략 (이미 unit 타입 앎)
if (unit is Enemy { Hp: 0 } e) { Log(e.Name); }      // 타입 검사 + 속성 + 바인딩 동시

// C#9: 관계 패턴 + 논리 패턴
if (x is > 0 and < 100) { }
if (c is (>= 'a' and <= 'z') or (>= 'A' and <= 'Z')) { }
```

**switch expression과 결합**:
속성 패턴이 가장 빛나는 곳은 switch expression.
```csharp
string Describe(Shape shape) => shape switch {
    Circle { Radius: > 10 } c  => $"큰 원 (r={c.Radius})",
    Circle c                    => $"원 (r={c.Radius})",
    Rectangle { Width: var w, Height: var h } => $"사각형 {w}x{h}",
    null                        => "없음",
    _                           => "기타"
};
```

**함정**: 패턴 바인딩 변수(`is string s`의 `s`)의 스코프는 `if` 블록 바깥까지 이어짐. 연속 `else if`에서 같은 이름으로 다시 바인딩하면 컴파일 에러.
```csharp
if (x is string s)    { Use(s); }
else if (x is int s)  { Use(s); }  // 에러: s 재선언
// 해결: 이름을 다르게 하거나 switch expression 사용
```

---

### 21. switch expression

**기능**: 값을 반환하는 표현식 형태 switch. (`#C#8`)

**비교 — switch 문 vs switch expression**:
```csharp
// switch 문: 값 반환 불가, case/break 필요
string result;
switch (grade) {
    case Grade.Normal: result = "일반"; break;
    case Grade.Rare:   result = "희귀"; break;
    default:           result = "?";    break;
}

// switch expression: 값 자체가 결과, 더 간결
string result = grade switch {
    Grade.Normal => "일반",
    Grade.Rare   => "희귀",
    _            => "?"
};
```

**대표 용도**: 타입별 분기 처리(팩토리), 상태→문자열 매핑, 상성 배율 테이블.

---

### 22. tuple pattern (조합 매트릭스)

**기능**: 여러 값을 동시에 매칭해 조합별 결과를 하나의 표현식으로 표현한다.

**핵심 개념**: N개의 독립적인 if-else 중첩을 N×M 매트릭스로 펼쳐 가독성을 높인다. 조합 수가 많을수록 중첩 if보다 유리하다.

```csharp
float multiplier = (attackType, defenseType) switch {
    (ElementType.Fire,  ElementType.Wind)  => 1.5f,   // 명확한 조합
    (ElementType.Water, ElementType.Fire)  => 1.5f,
    (var a, var d) when a == d            => 0.5f,    // when 가드: 조건식 추가
    _                                      => 1.0f    // 기본값
};
```

**`when` 가드**: 패턴 조건 외에 추가 조건이 필요할 때 `when 조건식`으로 보충. 위 예시의 `(var a, var d) when a == d`는 "두 값을 변수로 받되, 같을 때만" 매칭.

**대표 용도**: 속성 상성 테이블, 상태 전이 조건 (현재 상태 + 입력 → 다음 상태), 가위바위보류 판정.

**함정**: 열거형 조합이면 컴파일러가 exhaustiveness를 검사해 빠진 케이스에 경고가 생길 수 있음. `_` 기본값으로 해소.

---

## 제네릭 / 제약

### 26~27. 제네릭 기본

**기능**: 타입을 파라미터로 받아 타입 안전성을 유지하면서 코드를 재사용한다.

**핵심 개념**: 제네릭이 없으면 같은 로직을 타입별로 중복 작성하거나, `object`를 써서 박싱 비용과 캐스트 실패 위험을 감수해야 한다. 제네릭은 컴파일 타임에 타입을 확정해 두 문제를 동시에 해결.
```csharp
// 제네릭 없는 버전 — object 사용 시 박싱 + 런타임 캐스트 실패 가능
ArrayList items = new();
items.Add(1);
int x = (int)items[0];           // 틀리면 InvalidCastException

// 제네릭 버전 — 타입 안전 + 박싱 없음
List<int> ints = new();
ints.Add(1);
int x = ints[0];                 // 캐스트 불필요 — 컴파일 타임 확정
// ints.Add("string");           // 컴파일 에러 — 타입 안전
```

**제네릭 클래스**:
```csharp
class Repository<T> {
    private List<T> _items = new();
    public void Add(T item) => _items.Add(item);
    public T    Get(int i)  => _items[i];
    public bool Has(T item) => _items.Contains(item);
}

var repo = new Repository<Enemy>();
repo.Add(enemy);
```

**제네릭 메서드**:
```csharp
// 인자에서 T를 추론할 수 있으면 호출 시 명시 불필요
T Max<T>(T a, T b) where T : IComparable<T>
    => a.CompareTo(b) >= 0 ? a : b;

int   bigger = Max(3, 5);          // T = int 자동 추론
float fBig   = Max(1.5f, 2.3f);   // T = float 자동 추론
```

**함정**:
- 인터페이스를 통해 제네릭 타입을 사용하면 값 타입(struct)이 박싱될 수 있음. `where T : struct` 제약으로 방지 가능
- T에 기본값이 필요하면 `default(T)` — 참조면 `null`, 값 타입이면 `0`류
- Unity의 `GetComponent<T>()`는 내부에 `where T : Component` 제약이 있어 타입 안전하게 사용 가능

**대표 용도**: 풀(Pool), 저장소(Repository), 팩토리, 범용 유틸리티 메서드 (`GetOrCreate<T>`, `FindFirst<T>` 등).

---

### 28~34. 제약 (`where`)

**기능**: T에 올 수 있는 타입을 제한해, T의 멤버를 안전하게 사용하게 한다.

**비교**:
| 제약 | 허용 타입 | 사용 이유 |
|---|---|---|
| `where T : class` | 참조 타입 | `T x = null` 허용, `?.` 사용 |
| `where T : struct` | 값 타입 | boxing 없음 보증 |
| `where T : new()` | 기본 생성자 있는 타입 | `new T()` 호출 가능 |
| `where T : SomeClass` | SomeClass의 자식 | T의 멤버 접근 가능 |
| `where T : IFoo` | IFoo 구현체 | 인터페이스 메서드 호출 가능 |
| `where T : unmanaged` | 포인터 가능 타입 | `Span<T>`, unsafe 코드 |

**복수 제약 조합**:
```csharp
void Spawn<T>() where T : MonoBehaviour, new() { }
// MonoBehaviour 자식이면서 기본 생성자를 가진 타입만 허용
```

**CRTP (`where T : Foo<T>`)**: 자기 참조 제네릭. `MonoSingleton<T> where T : MonoSingleton<T>` 패턴. 상세는 [[design-pattern-notes]] #19 참조.

---

## 표현식 / 람다

### 35~36. `=>` 두 가지 의미

**기능**: `=>` 토큰은 두 가지 다른 문법에서 사용된다.

**비교**:
```csharp
// 1. Expression-bodied member — 단일 표현식으로 멤버 구현 (선언 문맥)
public int Count => _list.Count;           // 프로퍼티
public string Label => $"{Id}: {Name}";    // 계산 프로퍼티
public void Log() => Debug.Log("ping");    // void 메서드
public Item Get(int i) => _items[i];       // 반환값 있는 메서드

// 2. Lambda — 함수 값 (표현식 문맥)
Action<int> log = x => Debug.Log(x);      // 파라미터 1개: 괄호 생략 가능
Func<int, int> dbl = x => x * 2;
Func<int, int, int> add = (a, b) => a + b; // 파라미터 2개: 괄호 필요
Func<int> zero = () => 0;                  // 파라미터 없음
```

구분 방법: `=>` 왼쪽이 **타입 멤버 선언**이면 expression-bodied, **변수/파라미터**이면 lambda.

---

### 37~38. `Action` / `Func<T>` / `delegate` 비교

**기능**: 함수를 값으로 다루는 세 가지 방법.

| | 반환값 | 선언 방식 | 용도 |
|---|---|---|---|
| `Action` | void | 내장 | 이벤트 콜백, 부수효과만 있는 함수 |
| `Func<T>` | T | 내장 | 값을 반환하는 함수 |
| `delegate` | 커스텀 | 직접 선언 | 고유한 이름/시그니처 필요 시 |

```csharp
Action onDead;                       // void()
Action<int, string> log;             // void(int, string)
Func<int> getHp;                     // int()
Func<int, float> normalize;          // float(int) — 마지막 타입이 반환형

delegate void OnDamaged(int dmg);    // 이름 있는 커스텀 delegate
```

**대표 용도**:
- `Action`: `onComplete`, `onDead` 등 void 콜백 파라미터
- `Func<T>`: 팩토리, 조건 함수, 변환 함수
- 커스텀 `delegate`: `event` 선언 시, 특정 시그니처에 의미 있는 이름이 필요할 때

---

### 39~41. `nameof` / `typeof` / `default`

**기능**: 컴파일 타임에 메타 정보에 접근한다.

**핵심 개념**: 세 키워드 모두 런타임 오버헤드 없이 컴파일 타임에 값이 결정된다.

**비교**:
| 키워드 | 반환 | 결정 시점 | 용도 |
|---|---|---|---|
| `nameof(X)` | `string` | 컴파일 타임 | 심볼명을 문자열로 — 리팩토링 시 자동 추적 |
| `typeof(T)` | `Type` | 런타임 (컴파일 타임 검증) | 타입 객체 획득 |
| `default` / `default(T)` | T의 기본값 | 컴파일 타임 추론 | 타입의 기본값 표현 |

**용법**:
```csharp
// nameof — 문자열 하드코딩 대신 심볼 추적
Debug.Log(nameof(PlayerManager));        // "PlayerManager"
PropertyChanged?.Invoke(nameof(Hp));     // INotifyPropertyChanged 패턴
// Hp → Health로 리팩토링하면 nameof도 자동 변경됨

// typeof — 타입 객체 획득
Type t = typeof(int);
bool isSame = obj.GetType() == typeof(EnemyState);

// default — 타입의 기본값 (C#7.1부터 타입 추론)
int    x = default;   // 0
float  f = default;   // 0f
bool   b = default;   // false
string s = default;   // null
T item   = default;   // 제네릭에서 T의 기본값
```

**함정**:
- `nameof`는 *마지막 이름만* 반환. `nameof(Foo.Bar)` → `"Bar"` (`"Foo.Bar"` 아님)
- `typeof(Base)` vs `obj.GetType()`: `typeof`는 상속 무관 Base 그대로, `GetType()`은 실제 런타임 타입(자식 포함)
- `default`는 null 가능 타입에서 `null` 대신 쓰면 의도가 불분명해질 수 있음. 제네릭 메서드의 "빈 결과" 반환용이 가장 자연스러운 용도

**대표 용도**:
- `nameof`: `INotifyPropertyChanged`, 직렬화 키, 디버그 로그에 타입/멤버명 하드코딩 제거
- `typeof`: 타입 비교, Attribute 읽기
- `default`: 제네릭 메서드의 "빈 결과" 반환, 구조체 초기화

---

## 자료형 정의

### 42, 43, 49. `class` vs `struct` vs `record`

**기능**: 사용자 정의 타입의 세 가지 형태.

**비교**:
| | 메모리 | 대입 의미 | 기본 비교 | null 가능 | 상속 |
|---|---|---|---|---|---|
| `class` | 힙 (참조) | 참조 복사 | 참조 동일성 | O | O |
| `struct` | 스택 (값) | 값 전체 복사 | 값 동일성 | X (`Nullable<T>` 제외) | X |
| `record` | 힙 (참조) | 참조 복사 | **값 동일성** (자동 생성) | O | O (record끼리) |
| `record struct` (`#C#10`) | 스택 | 값 전체 복사 | 값 동일성 | X | X |

**용법**:
```csharp
// class: 가변 상태를 가진 엔티티, 서비스
class PlayerManager : MonoBehaviour { int _hp; }

// struct: 작고 불변에 가까운 데이터 컨테이너 (8~32 byte 권장)
struct DamageSpec { public float Base; public float Bonus; }

// record: 불변 데이터 전달 객체 (DTO), 비교가 빈번한 값 객체
record WeaponSpec(int Atk, float Speed);
var a = new WeaponSpec(10, 1.5f);
var b = new WeaponSpec(10, 1.5f);
bool eq = a == b;   // true — class였으면 false

// with 표현식: 일부만 변경한 복사본
var c = a with { Atk = 15 };
```

**함정**:
- `struct`는 대입 시 전체 복사 → 큰 struct를 메서드에 자주 넘기면 오히려 비쌀 수 있음. `in`, `ref` 키워드로 참조 전달 고려
- `record`의 `==`는 모든 프로퍼티 값 비교 — 의도치 않은 동등성 판단에 주의

---

### 44. `interface`

**기능**: 구현 없이 시그니처만 선언. 클래스는 여러 인터페이스를 동시에 구현 가능 (단일 상속의 `class`와 달리).

```csharp
interface IInitializable { void Init(); }
interface IDisposable    { void Dispose(); }

class Service : IInitializable, IDisposable {
    public void Init()    { ... }
    public void Dispose() { ... }
}
```

**대표 용도**: 의존성 역전(DI), 테스트 교체 가능한 목(mock), Unity의 `IDamageable` / `IPickupable` 같은 행동 표시자.

**공통점/차이점 — interface vs abstract class**:
| | interface | abstract class |
|---|---|---|
| 다중 구현 | O | X (단일 상속) |
| 필드 | X | O |
| 생성자 | X | O |
| 기본 구현 | C#8+에서 가능 | O |
| 용도 | "할 수 있다" 행동 표시 | "이다" 골격 제공 |

---

### 45~46. `enum` vs `[Flags] enum`

**기능**: 이름 있는 정수 상수 집합. `[Flags]`를 붙이면 여러 값을 비트 조합해 동시에 표현할 수 있다.

**핵심 개념**: 일반 `enum`은 "하나의 상태만", `[Flags] enum`은 "여러 상태의 조합"을 표현한다.

```csharp
// 일반 enum: 한 번에 하나의 값
enum State { Idle, Running, Dead }
State s = State.Running;

// Flags enum: 비트 조합으로 여러 값 동시 표현
[Flags] enum Permission { None = 0, Read = 1, Write = 2, Execute = 4 }
Permission p = Permission.Read | Permission.Write;   // 조합
bool canRead = (p & Permission.Read) != 0;            // 검사: 비트 AND
bool canRead2 = p.HasFlag(Permission.Read);           // 검사: HasFlag (읽기 쉬움, 약간 느림)
p |= Permission.Execute;                              // 추가
p &= ~Permission.Write;                               // 제거
```

**함정**:

`[Flags]` 값을 2의 거듭제곱으로 지정하지 않으면 비트 조합이 겹침:
```csharp
[Flags] enum Layer { A = 0, B = 1, C = 2, D = 3 }  // 잘못됨 — D(3)가 B|C(1|2=3)와 겹침
[Flags] enum Layer { None=0, A=1, B=2, C=4, D=8 }  // 올바름
```

**Unity SerializeField + enum 직렬화 함정**: enum은 `int`로 직렬화됨. 멤버를 **삭제하거나 정수값을 바꾸면** SO/씬 YAML에 저장된 정수값이 다른 의미로 매핑되어 silent corruption 발생.
```csharp
// 안전: 이름만 rename, 정수값 보존
enum EffectType { NewName = 3 }               // 기존 SO YAML의 3이 그대로 매핑됨

// 위험: 3 삭제 후 새 멤버에 정수값 3 재사용
enum EffectType { /* 3 삭제 */ NewEffect = 3 } // 기존 SO의 3이 NewEffect로 오매핑
```
폐기 멤버는 삭제 대신 정수값 영구 점유 — `[Obsolete] Deprecated_OldName = 3`으로 표시.

---

### 48. `event` vs `Action` 필드

**기능**: 둘 다 구독 가능한 콜백이지만 `event`는 외부에서 `Invoke()`를 차단한다.

```csharp
// Action 필드: 외부에서 직접 호출 가능 (의도치 않은 발행 위험)
public Action OnDead;
// 외부: manager.OnDead();      ← 가능 — 위험

// event: 구독/해제만 허용, 발행은 선언 클래스만 가능
public event Action OnDead;
// 외부: manager.OnDead();      ← 컴파일 에러
// 외부: manager.OnDead += Handler;  ← 가능
```

**대표 용도**: 공개 API의 이벤트는 `event` 사용. 내부 콜백 파라미터(`onComplete` 등)는 `Action`으로 충분.

---

## 컴파일러 지시문 / 속성

### 54~56. 조건부 컴파일 (`#if` / `#pragma warning`)

**기능**: 특정 심볼이 정의된 환경에서만 코드를 포함시킨다.

```csharp
#if UNITY_EDITOR
    [MenuItem("Tools/Build")]
    static void Build() { ... }
#endif

// 복수 심볼 조합
#if UNITY_IOS || UNITY_ANDROID
    // 모바일 전용 코드
#endif

// #pragma warning disable — 특정 경고 번호 억제
#pragma warning disable CS0649   // "필드가 할당되지 않음" — Unity [SerializeField]에서 발생
[SerializeField] private Button _btn;
#pragma warning restore CS0649
```

---

### 57. `[Conditional]` vs `#if` 비교

**기능**: 둘 다 조건부 실행이지만 작동 방식이 다름.

| | `#if` | `[Conditional]` |
|---|---|---|
| 제거 단위 | 블록 전체 (메서드 포함) | 호출 지점만 (메서드는 존재) |
| 타입 | 전처리기 | 특성(attribute) |
| 반환값 제약 | 없음 | void만 가능 |

```csharp
// #if: 해당 블록 자체가 컴파일 안 됨
#if DEBUG
void ValidateState() { ... }
#endif

// [Conditional]: 메서드는 컴파일되지만, 심볼 없는 빌드에서 호출 지점이 제거됨
[Conditional("DEBUG")]
void ValidateState() { ... }
// 릴리즈 빌드: ValidateState() 호출 라인 자체가 없어짐
```

**대표 용도**: 디버그 전용 검증 메서드, 로그 래퍼. 메서드 시그니처는 유지하되 릴리즈에서 오버헤드를 없애고 싶을 때.

---

### 60. `[CallerMemberName]`

**기능**: 컴파일 타임에 호출자의 메서드/프로퍼티 이름을 문자열로 자동 주입한다.

```csharp
void NotifyChanged([CallerMemberName] string propName = "")
    => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propName));

public int Hp {
    get => _hp;
    set { _hp = value; NotifyChanged(); }  // propName = "Hp" 자동 주입
}
```

**대표 용도**: `INotifyPropertyChanged` 구현 시 프로퍼티 이름 하드코딩 제거, 로그에 호출 위치 표기.

---

## 비동기 / 이터레이터

### 61~63. `yield return` / `yield break` — 이터레이터

**기능**: 메서드를 일시 중단하고 값을 하나씩 반환하는 이터레이터를 만든다. Unity 코루틴의 핵심 메커니즘.

**작동 원리**: `yield return`을 만나면 컴파일러가 상태 머신을 자동 생성. 다음 `MoveNext()` 호출 시 중단 지점부터 재개됨.

```csharp
// Unity 코루틴
IEnumerator PlaySequence() {
    yield return new WaitForSeconds(0.5f);    // 0.5초 대기
    ShowEffect();
    yield return StartCoroutine(FadeIn());    // 다른 코루틴 완료 대기
    yield return null;                         // 다음 프레임까지 대기
    if (isCancelled) yield break;             // 조기 종료
    Complete();
}

// 컬렉션 지연 생성 용도
IEnumerable<int> Range(int start, int end) {
    for (int i = start; i < end; i++)
        yield return i;   // 필요할 때만 생성 (지연 평가)
}
```

**Unity 코루틴에서 `yield return` 뒤에 올 수 있는 것**:
| 값 | 대기 |
|---|---|
| `null` | 다음 프레임 |
| `new WaitForSeconds(t)` | t초 (TimeScale 영향받음) |
| `new WaitForSecondsRealtime(t)` | t초 (TimeScale 무관) |
| `new WaitUntil(() => cond)` | 조건 true까지 |
| `StartCoroutine(other)` | 다른 코루틴 완료까지 |
| `new WaitForEndOfFrame()` | 프레임 렌더링 완료 후 |

---

### 64~65. `async` / `await` / `Task`

**기능**: C# 표준 비동기 프로그래밍 모델. Unity에서는 코루틴 대신 사용 가능.

```csharp
async Task<string> FetchDataAsync(string url) {
    HttpResponseMessage resp = await httpClient.GetAsync(url);   // 비차단 대기
    return await resp.Content.ReadAsStringAsync();
}

async void Start() {
    string data = await FetchDataAsync("...");
    ProcessData(data);
}
```

**코루틴 vs async/await 비교**:
| | 코루틴 | async/await |
|---|---|---|
| 반환형 | `IEnumerator` | `Task` / `Task<T>` |
| Unity 종속 | O (`StartCoroutine` 필요) | X (순수 C#) |
| 값 반환 | 어려움 (out/callback 필요) | 자연스러움 (`Task<T>`) |
| 취소 | 직접 플래그 관리 | `CancellationToken` |
| 예외 처리 | try/catch 제한적 | 정상 try/catch |

**함정**:
- `async void`는 예외를 잡을 수 없음 → `async Task`를 반환하고 호출부에서 처리
- UniTask(외부 패키지)를 사용하면 GC 할당 없이 Unity 생명주기와 통합 가능

---

## LINQ / 컬렉션

### 66~73. 지연 평가 vs 즉시 실행

**기능**: LINQ 메서드 체인은 기본적으로 지연 평가 — 실제로 값이 필요한 시점에 실행된다.

```csharp
var query = list.Where(x => x.Active).Select(x => x.Name);
// 이 시점엔 아무것도 실행 안 됨

foreach (var name in query) { }    // ← 여기서 실행
var result = query.ToList();        // ← ToList()가 즉시 실행 강제
```

**함정**: 지연 평가 쿼리를 여러 번 순회하면 매번 재실행됨. 결과를 재사용하려면 `.ToList()` / `.ToArray()`로 구체화.

---

### 67~72. 자주 쓰는 패턴

```csharp
// 필터 + 변환
var names = enemies
    .Where(e => e.IsAlive)
    .Select(e => e.Name)
    .ToList();

// dict 빌드 (ID 기반 O(1) 조회)
var itemById = items.ToDictionary(i => i.Id, i => i);
Item found = itemById.TryGetValue(id, out var v) ? v : null;

// 첫 매칭 (없으면 null)
var target = enemies.FirstOrDefault(e => e.Team == Team.Enemy);

// 존재 여부 — Count() > 0 대신 사용 (전체 순회 안 함)
bool hasAlive = enemies.Any(e => e.IsAlive);

// 조건 모두 충족
bool allDead = enemies.All(e => !e.IsAlive);
```

**비교 — `First` vs `FirstOrDefault` vs `Single`**:
| 메서드 | 없으면 | 복수 매칭 |
|---|---|---|
| `.First()` | 예외 | 첫 번째 반환 |
| `.FirstOrDefault()` | default (null/0) | 첫 번째 반환 |
| `.Single()` | 예외 | 예외 |
| `.SingleOrDefault()` | default | 예외 |

---

## 분류 메모

- **vs design-pattern-notes**: CRTP는 *문법 기법*인 동시에 *디자인 패턴*이라 양쪽에 등재 (design-pattern #19에 풀노트, 여기엔 인덱스 참조)
- **vs game-misc-notes**: `Array.Empty<T>()` 같은 GC 트릭은 *언어 기법*이지만 *성능 트릭* 측면이 강해 game-misc #12에 둠. 여기엔 LINQ 섹션에 참조 링크만
- **vs unity-feature-notes**: `[Serializable]` 같은 속성은 *C# 문법*이지만 Unity 의미와 분리 불가능 → unity-feature에 둠
- **승격 규칙**: 단순 문법은 인덱스 표에서 종료, 함정/응용 누적 시 풀노트로

---
