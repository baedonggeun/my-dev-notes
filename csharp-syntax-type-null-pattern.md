# C# 문법 — 타입·null·패턴

> 상위 노트: [[csharp-syntax-notes]] (전체 인덱스 디스패처)
> 다루는 축: 접근/상속 제어자·null 처리·패턴 매칭
> 다루지 않는 축: [[csharp-syntax-generic-expression-type|C# 문법 — 제네릭·표현식·자료형]] / [[csharp-syntax-async-infra-collection|C# 문법 — 비동기·인프라·컬렉션]]

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

---

# 풀노트

## 접근/상속 제어자

### 1. 접근 한정자 (`public` / `private` / `protected` / `internal`)

클래스·메서드·필드에 접근 가능한 범위를 제한한다.

C#의 기본 접근자는 `private` — 의도적으로 공개할 것만 명시하는 방향이 원칙.

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

메서드가 다형성에 참여하는 방식을 제어한다.

부모 타입 변수로 자식 인스턴스를 담았을 때 어떤 버전이 호출되는가.

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

값의 변경 가능 여부와 인스턴스/클래스 소속을 제어한다.

세 키워드가 해결하는 문제가 다르다.

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

null 체크를 간결하게 표현하는 연산자 3종.

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

타입 수준에서 null 허용 여부를 선언한다.

`?`가 값 타입에 붙는 것과 참조 타입에 붙는 것은 완전히 다른 메커니즘이다.

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

null 비교. `is null`은 `==` 연산자 오버로딩을 우회한다.

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

값이 특정 타입·조건에 부합하는지 검사하고, 동시에 변수를 바인딩한다.

C# 버전마다 `is` 한 줄이 표현하는 범위가 확장되었다.

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

값을 반환하는 표현식 형태 switch. (`#C#8`)

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

여러 값을 동시에 매칭해 조합별 결과를 하나의 표현식으로 표현한다.

N개의 독립적인 if-else 중첩을 N×M 매트릭스로 펼쳐 가독성을 높인다. 조합 수가 많을수록 중첩 if보다 유리하다.


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
