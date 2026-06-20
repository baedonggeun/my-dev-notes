# C# 문법 — 제네릭·표현식·자료형

> 상위 노트: [[csharp-syntax-notes]] (전체 인덱스 디스패처)
> 다루는 축: 제네릭/제약·표현식/람다·자료형 정의
> 다루지 않는 축: C# 문법 — 타입·null·패턴 / C# 문법 — 비동기·인프라·컬렉션

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

---

# 풀노트

## 제네릭 / 제약

### 26~27. 제네릭 기본

타입을 파라미터로 받아 타입 안전성을 유지하면서 코드를 재사용한다.

제네릭이 없으면 같은 로직을 타입별로 중복 작성하거나, `object`를 써서 박싱 비용과 캐스트 실패 위험을 감수해야 한다. 제네릭은 컴파일 타임에 타입을 확정해 두 문제를 동시에 해결.

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

T에 올 수 있는 타입을 제한해, T의 멤버를 안전하게 사용하게 한다.

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

**CRTP (`where T : Foo<T>`)**: 자기 참조 제네릭. `MonoSingleton<T> where T : MonoSingleton<T>` 패턴. 상세는 design-pattern-notes 항목 19 참조.

---

## 표현식 / 람다

### 35~36. `=>` 두 가지 의미

`=>` 토큰은 두 가지 다른 문법에서 사용된다.

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

함수를 값으로 다루는 세 가지 방법.

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

컴파일 타임에 메타 정보에 접근한다.

세 키워드 모두 런타임 오버헤드 없이 컴파일 타임에 값이 결정된다.


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

사용자 정의 타입의 세 가지 형태.

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

구현 없이 시그니처만 선언. 클래스는 여러 인터페이스를 동시에 구현 가능 (단일 상속의 `class`와 달리).

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

이름 있는 정수 상수 집합. `[Flags]`를 붙이면 여러 값을 비트 조합해 동시에 표현할 수 있다.

일반 `enum`은 "하나의 상태만", `[Flags] enum`은 "여러 상태의 조합"을 표현한다.


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

둘 다 구독 가능한 콜백이지만 `event`는 외부에서 `Invoke()`를 차단한다.

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
