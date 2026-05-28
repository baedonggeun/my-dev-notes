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

## 접근/상속 제어자

### 1. 접근 한정자 (`public` / `private` / `protected` / `internal`)

**기능**: 클래스·메서드·필드에 접근 가능한 범위를 제한한다. C#의 기본값은 `private`.

**비교**:
| 한정자 | 접근 가능 범위 |
|---|---|
| `public` | 어디서든 |
| `private` | 선언 클래스 내부만 (기본값) |
| `protected` | 선언 클래스 + 자식 클래스 |
| `internal` | 같은 어셈블리(프로젝트) 내 |
| `protected internal` | protected **또는** internal |
| `private protected` | protected **이면서** internal (`#C#7.2`) |

**용법**:
```csharp
public class Character { }              // 외부 어디서든 접근
private int _hp;                        // 이 클래스 내부만
protected virtual void OnDead() { }     // 자식 클래스에서 재정의 가능
internal class DebugHelper { }          // 같은 프로젝트 내부용
```

**대표 용도**:
- `private`: 내부 상태 캡슐화, 외부 API 최소화
- `protected`: 상속 계층에서만 공유할 훅 메서드 (`OnInit`, `OnDead` 등)
- `internal`: Editor 전용 유틸, 테스트용 헬퍼, 외부 패키지에 노출 안 할 내부 서비스

---

### 2~7. 상속 제어 (`abstract` / `virtual` / `override` / `sealed` / `new`)

**기능**: 메서드가 다형성에 참여하는 방식을 제어한다.

**비교**:
| 부모 선언 | 자식 override 가능? | 자식 override 의무? | 부모 구현 있음? |
|---|---|---|---|
| `virtual` | O | X | O |
| `abstract` | O | O | X |
| 일반 메서드 | X (`new`로 숨기기만 가능) | — | O |

**override vs new 핵심 차이**:
```csharp
Base b = new Child();
b.Foo();  // virtual + override → Child.Foo() 호출 (다형성 작동)
b.Bar();  // new (숨기기) → Base.Bar() 호출 (다형성 작동 안 함)
```
`new`는 부모 타입 변수로 참조 시 부모 버전이 호출된다. 실수로 `override` 대신 쓰면 다형성이 작동하지 않아 버그 원인이 됨.

**sealed 두 위치**:
```csharp
sealed class FinalState { }              // 이 클래스 상속 불가
sealed override void Enter() { }         // 이 override 이후 추가 재정의 불가
```

**대표 용도**:
- `abstract class`: 템플릿 메서드 패턴 — 공통 알고리즘 골격 제공, 세부 구현은 자식
- `virtual`: 기본 동작 제공하되 자식이 커스터마이징할 훅 포인트
- `sealed class`: 의도 명시(이 클래스는 확장 불필요) + JIT devirtualization 최적화

---

### 8~10. 수정자 (`readonly` / `const` / `static`)

**기능**: 값의 변경 가능 여부와 인스턴스/클래스 소속을 제어한다.

**비교**:
| | 값 결정 시점 | 변경 가능 시점 | 인스턴스별? | 암묵적 static |
|---|---|---|---|---|
| `const` | 컴파일 타임 | 불가 | X | O |
| `readonly` | 런타임 (생성자) | 생성자 내만 | O (`static readonly` 제외) | X |
| `static` | 런타임 | 자유 | X | — |

**용법**:
```csharp
const float MaxHp = 100f;                  // 컴파일 타임 고정값 — 암묵적 static
readonly List<int> _ids;                   // 생성자에서 할당 가능, 이후 재할당 불가
static int _instanceCount;                // 모든 인스턴스가 공유
static readonly int[] Empty = new int[0]; // 런타임 계산값을 불변으로
```

**함정**:
- `const`는 다른 어셈블리에서 참조 시 컴파일 타임에 값이 인라인됨 → 값 변경 후 참조 쪽 어셈블리를 재빌드하지 않으면 구버전 값 사용. 외부 노출 상수는 `static readonly` 권장
- `readonly List<T>`: 참조 변경(재할당)은 불가하지만 `.Add()` 등 내용 변경은 가능

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

**비교**:
| | 대상 | 의미 |
|---|---|---|
| `int?` | 값 타입 | `Nullable<int>` — null을 값으로 가질 수 있음 |
| `string?` | 참조 타입 | nullable reference type — null 가능함을 명시 (`#C#8`, NRT 활성화 필요) |
| `x!` | 표현식 | null-forgiving — 컴파일러에 "여기는 null 아님" 단언 |

**용법**:
```csharp
int? score = null;
if (score.HasValue) Use(score.Value);   // or: score ?? 0

string? playerName = GetName();         // NRT 활성화 시 "null 가능" 명시
playerName!.ToUpper();                  // null-forgiving: 개발자가 null 아님을 보증
```

**함정**: `!` (null-forgiving)은 컴파일러 경고를 억제할 뿐, 런타임 null을 막지 않음 — 실제로 null이면 NRE 발생.

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

**기능**: 값이 특정 타입·조건에 부합하는지 검사한다. C# 버전에 따라 표현력이 점진적으로 확장됨.

```csharp
// C#6 이전: 타입 검사 + 별도 캐스트
if (x is string) { string s = (string)x; }

// C#7: 검사 + 바인딩 동시
if (x is string s) { Use(s); }

// C#8: 속성 패턴 (필드·프로퍼티 값 매칭)
if (unit is { Hp: 0, Team: Team.Enemy }) { }

// C#9: 관계 패턴 + 논리 패턴 결합
if (x is > 0 and < 100) { }
if (c is (>= 'a' and <= 'z') or (>= 'A' and <= 'Z')) { }
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

**기능**: 여러 값을 동시에 매칭해 조합별 결과를 표현한다.

```csharp
float multiplier = (attackType, defenseType) switch {
    (ElementType.Fire,  ElementType.Wind)  => 1.5f,
    (ElementType.Water, ElementType.Fire)  => 1.5f,
    (var a, var d) when a == d            => 0.5f,   // 같은 속성
    _                                      => 1.0f
};
```

**대표 용도**: 속성 상성 테이블, 상태 전이 조건 (현재 상태 + 입력 → 다음 상태), 가위바위보류 판정.

---

## 제네릭 / 제약

### 26~27. 제네릭 기본

**기능**: 타입을 파라미터로 받아 재사용 가능한 코드를 작성한다. 런타임에 타입별 코드가 JIT로 생성됨.

**용법**:
```csharp
// 제네릭 클래스
class Repository<T> {
    private List<T> _items = new();
    public void Add(T item) => _items.Add(item);
    public T Get(int i) => _items[i];
}

// 제네릭 메서드
T FindFirst<T>(Predicate<T> match) where T : Component
    => GetComponentsInChildren<T>().FirstOrDefault(match.Invoke);
```

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

**기능**: 컴파일 타임 메타 정보 접근.

```csharp
// nameof: 심볼을 문자열로 — 리팩토링 시 자동 추적됨
Debug.Log(nameof(PlayerManager));        // "PlayerManager"
PropertyChanged?.Invoke(nameof(Hp));     // INotifyPropertyChanged 패턴

// typeof: 런타임 Type 객체
Type t = typeof(int);
if (obj.GetType() == typeof(EnemyState)) { }

// default: 타입의 기본값 (C#7.1부터 타입 추론)
int x = default;     // 0
string s = default;  // null
T item = default;    // 제네릭에서 T의 기본값
```

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

**기능**: 이름 있는 정수 상수 집합. `[Flags]`를 붙이면 비트 조합을 지원한다.

```csharp
// 일반 enum: 하나의 값만 가짐
enum State { Idle, Running, Dead }
State s = State.Running;

// Flags enum: 비트 조합 가능
[Flags] enum Permission { None = 0, Read = 1, Write = 2, Execute = 4 }
Permission p = Permission.Read | Permission.Write;  // 조합
bool canRead = (p & Permission.Read) != 0;           // 검사
bool canRead2 = p.HasFlag(Permission.Read);          // 동일 — 약간 느림
```

**함정**: `[Flags]` enum은 값을 2의 거듭제곱으로 수동 지정해야 함. 자동 증가(0, 1, 2, 3...)하면 조합이 겹침.

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
