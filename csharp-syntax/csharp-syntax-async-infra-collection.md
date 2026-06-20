# C# 문법 — 비동기·인프라·컬렉션

> 상위 노트: [[csharp-syntax-notes]] (전체 인덱스 디스패처)
> 다루는 축: 컴파일러 지시문/속성·비동기/이터레이터·생성자/파괴자·LINQ/컬렉션
> 다루지 않는 축: C# 문법 — 타입·null·패턴 / C# 문법 — 제네릭·표현식·자료형

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

# 풀노트

## 컴파일러 지시문 / 속성

### 54~56. 조건부 컴파일 (`#if` / `#pragma warning`)

특정 심볼이 정의된 환경에서만 코드를 포함시킨다.

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

둘 다 조건부 실행이지만 작동 방식이 다름.

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

컴파일 타임에 호출자의 메서드/프로퍼티 이름을 문자열로 자동 주입한다.

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

메서드를 일시 중단하고 값을 하나씩 반환하는 이터레이터를 만든다. Unity 코루틴의 핵심 메커니즘.

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

C# 표준 비동기 프로그래밍 모델. Unity에서는 코루틴 대신 사용 가능.

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

## 생성자 / 파괴자

### 74~78. 생성자 (Constructor)

인스턴스 생성 시 초기 상태를 설정한다. C#은 생성자 오버로딩, 체이닝, static 생성자를 지원한다.

생성자는 "이 객체를 올바른 상태로 만드는 진입점". 여러 오버로드가 있을 때 `this(...)`로 중복을 제거하고, 상속 계층에서는 `base(...)`로 부모를 초기화한다.


**인스턴스 생성자 + 체이닝**:
```csharp
class Weapon {
    private readonly string _name;
    private readonly int    _atk;
    private readonly float  _speed;

    // 주 생성자 — 모든 필드 초기화
    public Weapon(string name, int atk, float speed) {
        _name  = name;
        _atk   = atk;
        _speed = speed;
    }

    // this(...)로 주 생성자에 위임 — 기본값 제공
    public Weapon(string name, int atk) : this(name, atk, 1.0f) { }
    public Weapon(string name)          : this(name, 0)          { }
}
```

**base(...) — 부모 생성자 호출**:
```csharp
class Animal {
    protected string Name;
    public Animal(string name) { Name = name; }
}

class Dog : Animal {
    private string _breed;
    public Dog(string name, string breed) : base(name) {   // 부모 생성자 먼저 실행
        _breed = breed;
    }
}
```

자식 생성자에서 `base(...)`를 명시하지 않으면 **부모의 기본 생성자(파라미터 없는 것)** 가 자동 호출됨. 부모에 기본 생성자가 없으면 컴파일 에러.

**호출 순서**: `base(...)` → 부모 필드 초기화 → 부모 생성자 본문 → 자식 필드 초기화 → 자식 생성자 본문.

**static 생성자**:
```csharp
class Config {
    public static readonly Dictionary<string, int> Table;

    static Config() {             // 파라미터 없음, 접근자 없음
        Table = BuildTable();     // 클래스 최초 접근 시 1회만 실행
    }

    private static Dictionary<string, int> BuildTable() { ... }
}
```

**Primary constructor (C# 12)**:
```csharp
// 선언부에 파라미터 → 클래스 전체 스코프에서 사용 가능
class Weapon(string name, int atk) {
    public string Name => name;
    public int    Atk  => atk;
    public string Display() => $"{name} (atk={atk})";
}
```

record는 C# 9부터 이미 동일 문법. class/struct로 확장된 것이 C# 12.

**함정**:
- **MonoBehaviour에서 생성자 금지** — Unity는 오브젝트를 자체 방식으로 생성하므로 `new MyComponent()`를 직접 호출하면 경고/오동작. 초기화는 `Awake()`에서
- **`this(...)` 체이닝 실행 순서** — `: this(...)` 호출이 현재 생성자 본문보다 *먼저* 실행됨. 본문에서 `this(...)` 결과를 기대하는 로직이 있으면 순서에 유의
- **static 생성자 예외** — static 생성자에서 예외가 발생하면 `TypeInitializationException`으로 래핑되어 해당 타입이 AppDomain에서 영구적으로 사용 불가. try/catch로 예외 흡수 권장
- **Primary constructor 파라미터 캡처** — primary constructor 파라미터는 숨겨진 필드로 캡처됨. `public string Name => name;`처럼 프로퍼티에서 참조하면 필드가 살아있지만, 사용하지 않으면 JIT이 제거할 수 있음. 의도적으로 저장이 필요하면 `private readonly string _name = name;` 명시

**대표 용도 요약**:
- `this(...)`: 오버로드 생성자의 기본값 제공, 중복 초기화 코드 제거
- `base(...)`: 부모 필수 초기화 전달 (이름, ID, 의존성 등)
- `static` 생성자: 클래스 수준 캐시/테이블 빌드, 1회 초기화 보장
- Primary constructor: 단순 DI 컨테이너, record-style 불변 데이터 클래스

> **생성자 주입 패턴** — 생성자를 이용해 의존성을 명시적으로 받는 DI 패턴. Unity 제약(MonoBehaviour new() 불가)과 대안 포함 → design-pattern-notes 항목 20 DI

---

### 79~81. 파괴자 (Finalizer + IDisposable + using)

객체가 소멸될 때 리소스를 해제한다. C#에는 두 가지 해제 메커니즘이 있다.

Finalizer와 Dispose의 차이가 핵심.

- **Finalizer (`~Foo()`)**: GC가 결정하는 *비결정론적* 해제. 타이밍 보장 없음. 비관리 리소스(네이티브 핸들 등) 전용
- **`IDisposable.Dispose()`**: 호출자가 결정하는 *결정론적* 해제. `using`으로 스코프 끝에 자동 호출. 파일/소켓/DB연결 등

```csharp
// Finalizer 단독 — 드물게 사용, 비관리 리소스만
class NativeHandle {
    private IntPtr _handle;
    public NativeHandle() { _handle = AllocNative(); }
    ~NativeHandle() { FreeNative(_handle); }   // GC가 언젠가 호출 (타이밍 불명)
}

// IDisposable 단독 — 관리 리소스 해제 (가장 흔한 패턴)
class FileReader : IDisposable {
    private StreamReader _reader;
    public FileReader(string path) { _reader = new StreamReader(path); }
    public void Dispose() { _reader?.Dispose(); }
}

// 표준 Dispose 패턴 — 관리 + 비관리 리소스 모두 처리
class ResourceManager : IDisposable {
    private bool _disposed;
    private IntPtr _nativeHandle;       // 비관리
    private StreamReader _reader;       // 관리

    protected virtual void Dispose(bool disposing) {
        if (_disposed) return;
        if (disposing) {
            _reader?.Dispose();         // 관리 리소스 — Dispose()에서만 해제
        }
        FreeNative(_nativeHandle);      // 비관리 — 항상 해제
        _disposed = true;
    }

    public void Dispose() {
        Dispose(disposing: true);
        GC.SuppressFinalize(this);      // Finalizer 억제 — 이미 정리했으므로
    }

    ~ResourceManager() {
        Dispose(disposing: false);      // Finalizer 경로 — 관리 리소스는 이미 수거됨
    }
}
```

**using 구문 두 가지**:
```csharp
// using 블록 — 블록 끝에 Dispose() 호출
using (var reader = new StreamReader("file.txt")) {
    var content = reader.ReadToEnd();
}   // ← 여기서 Dispose() 자동 호출 (예외 발생해도)

// using 선언 (C# 8+) — 변수 스코프 끝에 Dispose() 호출
using var reader = new StreamReader("file.txt");
var content = reader.ReadToEnd();
// 메서드 끝 또는 중괄호 스코프 끝에서 Dispose() 자동 호출
```

**함정**:
- **Finalizer는 마지막 안전망** — 사용자가 `Dispose()`를 잊었을 때의 보험. 정상 흐름은 `using`/`Dispose()` 호출이어야 함. Finalizer에만 의존하면 해제 타이밍 불명 + GC 부하 증가
- **`Dispose()` 중복 호출 방어** — `if (_disposed) return;` 가드 필수. `using` 블록이 중첩되거나 예외 핸들러에서 이중 호출 가능
- **`GC.SuppressFinalize(this)` 필수** — `Dispose()`에서 이미 정리했으면 Finalizer가 다시 정리하지 않도록 억제. 빠뜨리면 GC가 Finalizer도 실행해 이중 해제 가능 (비관리 핸들 이중 해제 = crash)
- **Unity에서 Finalizer 사용 제한** — Unity의 Native Object(Texture, AudioClip, AOC 등)는 GC가 아닌 Unity 엔진이 소유. Finalizer에서 `Destroy(nativeObj)` 호출 시 이미 파괴된 객체 접근 위험. 대신 `OnDisable`/`OnDestroy`에서 명시 `Destroy()` 호출
- **`using` 선언은 스코프 주의** — C# 8+ `using var`는 변수가 선언된 *블록의 끝*에 해제. 블록이 없으면 메서드 끝. 의도한 해제 시점이 중간이라면 `using (...)` 명시 블록 사용

**대표 용도**:
- Finalizer: Unity `AnimatorOverrideController` 같은 Native Object 누수 방지 안전망 (본 역할은 `OnDisable`의 `Destroy()`)
- `IDisposable` + `using`: 파일/소켓/DB 연결, 임시 리소스 스코프 해제, `CancellationTokenSource`
- `using` 선언: 메서드 내 짧은 스코프 리소스 (C# 8+, Unity 2021+ 지원)

---

## LINQ / 컬렉션

### 66~73. 지연 평가 vs 즉시 실행

LINQ 메서드 체인은 기본적으로 지연 평가 — 실제로 값이 필요한 시점에 실행된다.

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
