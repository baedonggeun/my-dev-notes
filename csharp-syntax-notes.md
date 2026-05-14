# C# 문법 / 키워드 노트

> 다루는 축: C# 언어 자체의 키워드 / 연산자 / 문법. 빠른 회상용 cheatsheet
> 다루지 않는 축: 디자인 패턴(→ [[design-pattern-notes]]), Unity API(→ [[unity-feature-notes]]), 단편 트릭(→ [[game-misc-notes]])
> 적용 범위: C# 전 버전 (사용 시점 C# 버전을 항목에 명시)
> 관련 노트: [[design-pattern-notes]] #19 CRTP, [[game-misc-notes]] #12 Array.Empty
> 평생 노트 정책: 인덱스 표가 본체, 풀노트는 함정 있는 항목만 작성
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

## 인덱스

### 접근/상속 제어자

| 키워드 | 한 줄 설명 | 예시 |
|---|---|---|
| `public` / `private` / `protected` / `internal` | 표준 접근 한정자 | `public class Foo {}` |
| `abstract` (class) | 인스턴스화 불가, 자식 구현 강제 | `abstract class Base { abstract void Foo(); }` |
| `abstract` (method) | 자식 구현 의무 | `abstract void Update();` |
| `virtual` / `override` | 가상 메서드 / 재정의 | `protected virtual void OnInit() {}` |
| `sealed` (class) | 상속 금지 (의도 명시 + 컴파일러 최적화) | `sealed class FlowDirector {}` |
| `sealed` (override) | override 추가 재정의 차단 | `sealed override void Foo()` |
| `new` (멤버) | 부모 멤버 가리기 (override 아님 — 정적 디스패치) | `new void Foo()` |
| `readonly` (필드) | 생성자 이후 변경 불가 | `readonly int max;` |
| `const` | 컴파일 타임 상수 | `const float PI = 3.14f;` |
| `static` | 인스턴스 없이 접근 | `static int counter;` |

---

### null 처리

| 키워드 | 한 줄 설명 | 예시 |
|---|---|---|
| `?.` null-conditional | null이면 null 반환 (체이닝 안전) | `obj?.Method()?.Foo` |
| `??` null-coalescing | null이면 우항 | `x ?? "default"` |
| `??=` null-coalescing assign | null일 때만 대입 (`#C#8`) | `cache ??= new Dict()` |
| `?` (값 타입) nullable | 값 타입을 nullable로 (`Nullable<T>`) | `int? x = null;` |
| `?` (참조 타입) nullable annotation | nullable reference (`#C#8`, 활성화 시) | `string? name;` |
| `!` null-forgiving | "여기는 null 아님" 컴파일러 단언 | `x!.Foo()` |
| `is null` / `is not null` | null 비교 (오버로딩 회피) | `if (x is not null)` |

---

### 패턴 매칭

| 키워드 | 한 줄 설명 | 예시 |
|---|---|---|
| `is` (타입 검사) | 타입 일치 여부 | `if (x is string)` |
| `is` (변수 바인딩) | 타입 검사 + 캐스트 동시 (`#C#7`) | `if (x is int n) Use(n);` |
| `is` (속성 패턴) | 객체 속성 매칭 (`#C#8`) | `if (p is { Age: > 18 })` |
| switch expression | 표현식 형태 switch (`#C#8`) | `x switch { 1 => "a", _ => "b" }` |
| tuple pattern | 튜플 매칭 (상성 매트릭스 등) (`#C#8`) | `(atk, def) switch { (Fire, Wind) => 1.2f, _ => 1f }` |
| `_` discard | 값 무시 / 와일드카드 | `(_, y) = tuple;` |
| relational pattern | 비교 연산 패턴 (`#C#9`) | `x is > 0 and < 100` |
| `and` / `or` / `not` 패턴 | 패턴 결합 (`#C#9`) | `c is >= 'a' and <= 'z'` |

---

### 제네릭 / 제약

| 키워드 | 한 줄 설명 | 예시 |
|---|---|---|
| `class Foo<T>` | 제네릭 클래스 | `class Pool<T> { T Get(); }` |
| `void Foo<T>()` | 제네릭 메서드 | `T GetController<T>() where T : Component` |
| `where T : class` | 참조 타입만 | |
| `where T : struct` | 값 타입만 | |
| `where T : new()` | 기본 생성자 필요 | `new T()` 가능 |
| `where T : Foo` | Foo의 자식만 | |
| `where T : Foo<T>` | **CRTP** 자기 참조 | → [[design-pattern-notes]] #19 |
| `where T : unmanaged` | 비관리 타입만 (Span, P/Invoke) | |
| `default(T)` | T의 기본값 | `T x = default;` |

---

### 표현식 / 람다

| 키워드 | 한 줄 설명 | 예시 |
|---|---|---|
| `=>` expression-bodied member | 표현식 메서드/프로퍼티 (`#C#6`) | `public int Count => list.Count;` |
| `=>` lambda | 람다식 | `x => x * 2` |
| `Action` / `Func<T>` | delegate 표준 형식 | `Action<int> handler;` |
| `delegate` 키워드 | 익명 메서드 (구식, lambda로 대체) | `delegate { return 1; }` |
| `nameof` | 컴파일 타임 이름 문자열 (`#C#6`) | `nameof(MyVar)` → `"MyVar"` |
| `typeof` | 타입 객체 | `typeof(int)` → `Type` |
| `default` 리터럴 | 타입 추론 default (`#C#7.1`) | `int x = default;` |

---

### 자료형 정의

| 키워드 | 한 줄 설명 | 예시 |
|---|---|---|
| `class` | 참조 타입 | `class Foo {}` |
| `struct` | 값 타입 (스택, 복사 의미) | `struct Vec2 { float x, y; }` |
| `interface` | 인터페이스 (다중 구현) | `interface IInit { void Init(); }` |
| `enum` | 열거형 (정수 기반) | `enum Grade { Normal, Rare, Epic }` |
| `[Flags] enum` | 비트 플래그 열거형 | `[Flags] enum Layer { UI=1, FX=2, BG=4 }` |
| `delegate` | 함수 시그니처 타입 | `delegate void Handler(int v);` |
| `event` | 외부 invoke 차단된 이벤트 | `public event Action OnChanged;` |
| `record` | 값 비교 immutable 클래스 (`#C#9`) | `record Point(int x, int y);` |
| `partial` | 여러 파일에 클래스 분할 | `partial class Foo {}` |
| `using static` | 정적 멤버 직접 임포트 | `using static System.Math;` |
| 자동 프로퍼티 | `{ get; set; }` 자동 백업 필드 | `public int X { get; private set; }` |
| init-only 프로퍼티 | 생성 시에만 대입 (`#C#9`) | `public int X { get; init; }` |

---

### 컴파일러 지시문 / 속성

| 키워드 | 한 줄 설명 | 예시 |
|---|---|---|
| `#if` / `#else` / `#endif` | 조건부 컴파일 | `#if UNITY_EDITOR ... #endif` |
| `#region` / `#endregion` | 코드 접기 영역 | `#region UI Setup ... #endregion` |
| `#pragma warning disable` | 특정 경고 억제 | `#pragma warning disable CS0649` |
| `[Conditional("X")]` | 심볼 없으면 호출 자체 제거 | `[Conditional("DEBUG")] void Log() {}` |
| `[Obsolete]` | 사용 시 경고/에러 | `[Obsolete("Use Foo2 instead")]` |
| `[Serializable]` | 직렬화 가능 표시 | → [[unity-feature-notes]] #4 |
| `[CallerMemberName]` | 호출자 이름 자동 주입 | `void Log([CallerMemberName] string n="")` |

---

### 비동기 / 이터레이터

| 키워드 | 한 줄 설명 | 예시 |
|---|---|---|
| `yield return` | 이터레이터 한 항목 반환 (지연 실행) | `yield return new WaitForSeconds(1);` |
| `yield break` | 이터레이터 종료 | `if (done) yield break;` |
| `IEnumerable<T>` / `IEnumerator` | 이터레이터 인터페이스 | → Unity 코루틴은 `IEnumerator` |
| `async` / `await` | 비동기 메서드 (`#C#5`) | Unity에선 코루틴 대신 선택 사용 |
| `Task` / `Task<T>` | 비동기 작업 표현 | `async Task<int> Fetch()` |

---

### LINQ / 컬렉션

| 키워드 | 한 줄 설명 | 예시 |
|---|---|---|
| `from ... in ... select` | 쿼리 식 (잘 안 씀, 메서드 체인 선호) | `from x in list where x>0 select x` |
| `.Where(...)` | 필터 | `list.Where(x => x.Active)` |
| `.Select(...)` | 변환 | `list.Select(x => x.Name)` |
| `.ToList()` / `.ToArray()` | 컬렉션 변환 + 즉시 실행 | |
| `.ToDictionary(k, v)` | 키-값 매핑 + dict 빌드 | `items.ToDictionary(i => i.Id, i => i)` |
| `.FirstOrDefault(...)` | 첫 매칭 또는 default | `list.FirstOrDefault(x => x.Id == id)` |
| `.Any(...)` / `.All(...)` | 존재 / 모두 검사 | `list.Any(x => x.Done)` |
| `Array.Empty<T>()` | GC 회피 빈 배열 | → [[game-misc-notes]] #12 |

---

## 항목별 노트 (함정 있는 것만)

*풀노트는 셋 중 둘 이상 해당 시 작성: (1) 자주 잊는 함정 있음, (2) 응용 사례 3+, (3) 미묘한 의미 차이로 디버깅이 어려움.*

---

## 분류 메모

- **vs design-pattern-notes**: CRTP는 *문법 기법*인 동시에 *디자인 패턴*이라 양쪽에 등재 (design-pattern #19에 풀노트, 여기엔 인덱스 참조)
- **vs game-misc-notes**: `Array.Empty<T>()` 같은 GC 트릭은 *언어 기법*이지만 *성능 트릭* 측면이 강해 game-misc #12에 둠. 여기엔 LINQ 섹션에 참조 링크만
- **vs unity-feature-notes**: `[Serializable]` 같은 속성은 *C# 문법*이지만 Unity 의미와 분리 불가능 → unity-feature에 둠
- **승격 규칙**: 단순 문법은 인덱스 표에서 종료, 함정/응용 누적 시 풀노트로

---
