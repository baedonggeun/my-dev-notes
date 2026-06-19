# C# 문법 / 키워드 노트

> 상위 노트: [[README]]
> 다루는 축: C# 언어 자체의 키워드 / 연산자 / 문법. 빠른 회상용 cheatsheet
> 다루지 않는 축: 디자인 패턴(→ design-pattern-notes), Unity API(→ unity-feature-notes), 단편 트릭(→ game-misc-notes)
> 적용 범위: C# 전 버전 (사용 시점 C# 버전을 항목에 명시)
> 관련 노트: design-pattern-notes 항목 19 CRTP, game-misc-notes 항목 12 Array.Empty
> 등재 기준: **본인이 코드에 한 번이라도 쓴 것**. Microsoft Learn 문서를 옮기는 게 아니라 "내가 실제 사용한 것만" 누적
> 풀노트 작성 기준: 인덱스 1줄만으로 이해/적용이 불충분한 항목. 자명한 항목만 인덱스로 종료
> 작성 시작: 2026-05-15

---

**서브 노트:**
- [[csharp-syntax-type-null-pattern|C# 문법 — 타입·null·패턴]] — 접근/상속 제어자·null 처리·패턴 매칭
- [[csharp-syntax-generic-expression-type|C# 문법 — 제네릭·표현식·자료형]] — 제네릭/제약·표현식/람다·자료형 정의
- [[csharp-syntax-async-infra-collection|C# 문법 — 비동기·인프라·컬렉션]] — 컴파일러 지시문/속성·비동기/이터레이터·생성자/파괴자·LINQ/컬렉션


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
| 32 | `where T : Foo<T>` | **CRTP** 자기 참조 | → design-pattern-notes 항목 19 |
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
| 59 | `[Serializable]` | 직렬화 가능 표시 | → unity-feature-notes 항목 4 |
| 60 | `[CallerMemberName]` | 호출자 이름 자동 주입 | `void Log([CallerMemberName] string n="")` |

## 비동기 / 이터레이터

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 61 | `yield return` | 이터레이터 한 항목 반환 (지연 실행) | `yield return new WaitForSeconds(1);` |
| 62 | `yield break` | 이터레이터 종료 | `if (done) yield break;` |
| 63 | `IEnumerable<T>` / `IEnumerator` | 이터레이터 인터페이스 | → Unity 코루틴은 `IEnumerator` |
| 64 | `async` / `await` | 비동기 메서드 (`#C#5`) | Unity에선 코루틴 대신 선택 사용 |
| 65 | `Task` / `Task<T>` | 비동기 작업 표현 | `async Task<int> Fetch()` |

## 생성자 / 파괴자

| # | 키워드 | 한 줄 설명 | 예시 |
|---|---|---|---|
| 74 | 인스턴스 생성자 | 인스턴스 생성 시 호출. 오버로딩 가능 | `public Foo(int x) { _x = x; }` |
| 75 | `this(...)` 생성자 위임 | 같은 클래스의 다른 생성자에 체이닝 | `public Foo() : this(0) {}` |
| 76 | `base(...)` 부모 생성자 호출 | 자식 생성자에서 부모 생성자 명시 호출 | `public Bar(int x) : base(x) {}` |
| 77 | `static` 생성자 | 클래스 최초 접근 시 1회, 파라미터 없음 | `static Foo() { _cache = Build(); }` |
| 78 | Primary constructor (`#C#12`) | 클래스 선언부에 파라미터 직접 명시 | `class Foo(int x) { int _x = x; }` |
| 79 | Finalizer (`~Foo()`) | GC 수거 전 호출. 비결정론적, 비관리 리소스 전용 | `~Foo() { _handle.Free(); }` |
| 80 | `IDisposable` / `Dispose()` | 명시적 결정론적 리소스 해제 패턴 | `void Dispose() { _stream.Dispose(); }` |
| 81 | `using` 구문 | 스코프 끝에 `Dispose()` 자동 호출 | `using var r = new Resource();` |

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
| 73 | `Array.Empty<T>()` | GC 회피 빈 배열 | → game-misc-notes 항목 12 |


---
## 분류 메모

- **vs design-pattern-notes**: CRTP는 *문법 기법*인 동시에 *디자인 패턴*이라 양쪽에 등재 (design-pattern 항목 19에 등재)
- **vs game-misc-notes**: `Array.Empty<T>()` 같은 GC 트릭은 *언어 기법*이지만 *성능 트릭* 측면이 강해 game-misc에 등재
- **vs unity-feature-notes**: `[Serializable]` 같은 속성은 *C# 문법*이지만 Unity 의미와 분리 불가능 → unity-feature에 등재
- **승격 규칙**: 단순 문법은 인덱스 표에서 종료, 함정/응용 누적 시 풀노트로
