# 디자인 패턴 노트 — 생성·구조 패턴 (GoF Creational + Structural)

> 상위 노트: [[design-pattern-notes]] (전체 인덱스 디스패처)
> 다루는 축: GoF 생성 패턴(객체 생성) + 구조 패턴(클래스·객체 조합)
> 다루지 않는 축: 행위 패턴 / 아키텍처 패턴

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
| 2 | Singleton | `#생성` `#전역` | 인스턴스를 전역에서 단 하나만 보장 (라이프사이클 관리 권장) | `#OOP` `#언어독립` |
| 8 | Facade | `#구조` | 복잡한 서브시스템에 단순화된 인터페이스 제공 | `#OOP` `#언어독립` |
| 11 | Adapter | `#구조` | 호환되지 않는 인터페이스를 클라이언트 기대 형태로 변환 | `#OOP` `#언어독립` |
| 13 | Decorator | `#구조` | 객체를 같은 인터페이스의 wrapper로 감싸 동적으로 책임 추가 | `#OOP` `#언어독립` |
| 14 | Factory | `#생성` | 객체 생성 로직을 별도 메서드/클래스로 분리 | `#OOP` `#언어독립` |
| 15 | Composite | `#구조` | 단일 객체와 객체 집합을 동일 인터페이스로 다룸 | `#OOP` `#언어독립` |
| 18 | Object Pooling | `#생성` `#성능` | 객체를 재사용 풀로 관리해 GC/생성 비용 절감 | `#OOP` `#언어독립` |
| 19 | CRTP (Curiously Recurring Template Pattern) | `#생성` `#구조` | `class Foo<T> where T : Foo<T>` — 부모가 자식 타입을 알아 타입 안전성 강화 (MonoSingleton 등) | `#OOP` `#제네릭` |

---

# 풀노트

## 2. Singleton

_인스턴스를 전역에서 단 하나만 보장하는 패턴. 전역 접근점 제공 + 라이프사이클 제어._

**직관**
나라에 대통령은 한 명 — 전역 어디서든 "대통령"이라고 부르면 동일 인물. 두 명이 동시에 존재하면 혼란.

**문제 상황**
전역 인스턴스 없이 여러 곳에서 같은 객체가 필요하면 두 가지 선택지 모두 나쁨:
```csharp
// 방법 1: Prop Drilling — 생성 체인 전체에 주입
class GameManager  { AudioManager _audio; GameManager(AudioManager a) { _audio = a; } }
class EnemySpawner { AudioManager _audio; EnemySpawner(AudioManager a) { _audio = a; } }
// 모든 클래스 생성자가 AudioManager를 받아야 함

// 방법 2: 매번 새로 생성 — 인스턴스 중복
class Enemy { void Die() { new AudioManager().Play("death"); } }
```
Singleton으로 전역 단일 인스턴스를 보장하면 어디서든 `AudioManager.Instance`로 접근.

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

**언제 쓰나 / 피할 때**
- ✅ 앱 전체에서 하나만 존재해야 하는 시스템 (AudioManager, GameManager 등)
- ✅ 전역 접근이 빈번해 Prop Drilling이 비현실적일 때
- ❌ 테스트해야 하는 비즈니스 로직 — Mock 교체 불가. Service 분리 + DI(항목 20) 사용
- ❌ 씬 종속 오브젝트 — DontDestroyOnLoad와 씬 재로드 충돌 위험

⚠ **주의점**
- **테스트 불가** — `Instance`를 직접 호출하는 코드는 Mock 교체 불가. 테스트가 필요한 로직은 Service 계층으로 분리 + DI(항목 20) 경유
- **DontDestroyOnLoad 남용** — 씬 종속 오브젝트에 붙이면 씬 재로드 시 중복 인스턴스 생성
- **초기화 순서** — Awake에서 다른 Singleton을 참조하면 아직 초기화 안 된 상태일 수 있음. Start로 분리하거나 lazy initialization 사용


#생성 #전역 #시스템
> 관련: [[design-pattern-notes]] 항목 19 CRTP (MonoSingleton<T> 구현 매체), 항목 3 Service Locator (대안), 항목 20 DI (테스트 가능한 대안) | 종속성: `#OOP` `#언어독립` (B는 `#Unity`)

## 8. Facade

_복잡한 서브시스템(여러 클래스의 협력)에 단순화된 단일 진입점 인터페이스를 제공하는 패턴._

**직관**
리모컨 — TV·에어컨·조명을 각각 알 필요 없이 "영화 모드" 버튼 하나로 제어. 내부 협력 순서는 리모컨이 알아서.

**문제 상황**
클라이언트가 서브시스템들의 협력 순서를 직접 알아야 하면:
```csharp
// SFX 재생 — 클라이언트가 3단계를 순서대로 알아야 함
var clip = audioLoader.Load($"Sounds/{id}");
audioMixer.SetVolume("SFX", 0.8f);
audioPlayer.Play(clip, position);
// 이 3줄이 10군데 중복 → 순서 틀리면 버그, 서브시스템 변경 시 모두 수정
```
Facade로 감추면 `soundFacade.PlaySfx("hit", pos)` 한 줄.

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

**언제 쓰나 / 피할 때**
- ✅ 서브시스템 3개 이상의 협력 순서를 여러 곳에서 반복 호출할 때
- ✅ 복잡한 초기화/해제 순서를 단순화할 때
- ❌ 서브시스템이 1개 — Wrapper 정도면 충분
- ❌ 모든 기능을 Facade에 추가 — God Object 위험. 고급 기능은 서브시스템에 남기기

⚠ **주의점**
- **서브시스템 직접 접근** — Facade가 있어도 서브시스템 클래스에 직접 접근 가능하면 절반짜리. `internal`로 외부 접근 차단 권장
- **비대화 방지** — 모든 기능을 Facade에 추가하면 God Object가 됨. 고급 기능은 서브시스템에 남기기
- **Service(항목 5)와 중첩** — Manager가 Service들을 조합해서 공개하는 구조는 Facade 역할 겸임


#구조
> 관련: [[design-pattern-notes]] 항목 5 Service Layer 분리 (Manager의 Facade 겸임 패턴) | 종속성: `#OOP` `#언어독립`

## 11. Adapter

_기존 클래스의 인터페이스를 클라이언트가 기대하는 형태로 변환하는 래퍼. 서로 맞지 않는 두 코드를 연결._

**직관**
해외여행 콘센트 어댑터 — 플러그 모양이 달라도 어댑터 하나로 연결 가능. 기존 기기(레거시)와 새 소켓(인터페이스) 모두 변경 없음.

**문제 상황**
레거시/외부 라이브러리의 인터페이스가 기대하는 것과 다를 때:
```csharp
// 클라이언트가 기대하는 인터페이스
interface IAudioService { void Play(string id); }

// 변경 불가한 레거시 코드 — 서명이 다름
class LegacyAudioSystem { public void PlaySound(string path, float vol) { ... } }

IAudioService audio = new LegacyAudioSystem(); // 컴파일 에러 — 호환 불가
```
Adapter 클래스가 번역 역할 → 양쪽 코드 수정 없이 연결.

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

**언제 쓰나 / 피할 때**
- ✅ 변경 불가한 레거시/외부 라이브러리를 기존 인터페이스에 맞출 때
- ✅ 서드파티 SDK 교체 시 기존 호출 코드를 건드리지 않으려 할 때
- ❌ 처음부터 새로 작성하는 코드 — 올바른 인터페이스로 바로 작성
- ❌ 불일치가 너무 크거나 다단계 변환 — Facade(항목 8)로 더 넓은 추상화 추가

⚠ **주의점**
- **남용 금지** — 새 코드를 처음부터 올바른 인터페이스로 짜는 대신 Adapter를 쓰면 복잡도만 증가. 레거시/외부 라이브러리 연결 전용
- **변환 비용** — 경로 변환, 타입 캐스팅 등 Adapter 내부 작업이 무거우면 캐싱 고려
- **불일치가 심할 때** — Adapter 한 겹으로 해결 안 되면 Facade(항목 8)로 추상화 추가


#구조
> 관련: [[design-pattern-notes]] 항목 8 Facade (더 넓은 단순화), 항목 13 Decorator (동일 인터페이스 유지 래퍼) | 종속성: `#OOP` `#언어독립`

## 13. Decorator

_객체를 동일 인터페이스의 wrapper로 감싸서 기존 코드 수정 없이 기능을 동적으로 추가/조합하는 패턴._

**직관**
카페 음료에 샷 추가, 시럽 추가 — 기본 컵을 wrapper로 감싸며 기능을 쌓되, 항상 "음료"로 다룸. 조합은 런타임에 자유롭게.

**문제 상황**
기능 조합마다 서브클래스를 만들면 클래스 수가 폭발:
```
PoisonWeapon, FireWeapon, IceWeapon        // 3개
PoisonFireWeapon, PoisonIceWeapon, FireIceWeapon  // 조합 3개
PoisonFireIceWeapon                        // 조합 1개
// n가지 효과 → 2ⁿ 서브클래스 필요
```
Decorator는 효과별 클래스 n개만 필요. `new FireDecorator(new PoisonDecorator(base))`로 런타임 조합.

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

**언제 쓰나 / 피할 때**
- ✅ 기능을 런타임에 동적으로 조합해야 할 때 (아이템 효과, 버프 스택 등)
- ✅ 조합 수가 많아 상속으로 감당 안 될 때
- ❌ 조합 수가 3 이하 — 상속이 더 단순하고 추적 쉬움
- ❌ 중첩이 3단계 이상 — `List<IEffect>` 순회 방식 검토

⚠ **주의점**
- **중첩 깊이** — 3단계 이상이면 call stack 추적 어려움. 이 수준이면 `List<IEffect>` 순회 방식 검토
- **동일성 비교** — `wrapper == original`이 false. ID 시스템 또는 내부 객체 노출 필요
- **무상태 Decorator** — 상태 없는 Decorator는 싱글톤/재사용 가능해 GC 압력 없음


#구조
> 관련: [[design-pattern-notes]] 항목 15 Composite (트리 구조 대안) | 종속성: `#OOP` `#언어독립`

## 14. Factory

_객체 생성 로직을 별도 메서드/클래스로 분리해서 생성 방법 변경이 호출 코드에 영향을 주지 않게 하는 패턴._

**직관**
자동차 공장 — 어떤 모델을 만들지는 공장이 결정. 주문자는 "스포츠카 만들어줘"만 요청, 내부 조립 과정은 모름.

**문제 상황**
생성 로직이 호출 측에 분산되면 타입 변경 시 여러 곳 수정:
```csharp
// 레벨에 따라 적 종류가 달라지는 로직이 여러 곳에 복붙됨
if (level < 5)       enemy = new Goblin(speed: 3, hp: 10);
else if (level < 10) enemy = new Orc(speed: 2, hp: 30);
else                 enemy = new Dragon(speed: 1, hp: 100);
// Goblin 생성 파라미터 변경 시 이 if/else가 있는 모든 곳 수정 필요
```
Factory로 생성 로직을 한 곳에 모으면 변경이 Factory 하나에서만 발생.

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

**언제 쓰나 / 피할 때**
- ✅ 생성할 타입이 조건에 따라 달라질 때
- ✅ 생성 로직이 복잡하거나 여러 곳에서 중복될 때
- ❌ 단순 `new Foo()` 1-2종류 — 직접 생성이 더 명확
- ❌ Abstract Factory: 관련 세트 교체 없이 단순 생성 — 오버엔지니어링

⚠ **주의점**
- **변종 선택 기준** — Static Factory는 생성 방법 1-2가지. Factory Method는 서브클래스마다 다른 타입. Abstract Factory는 관련 세트를 통째로 교체할 때
- **Pool(항목 18)과 조합** — 팩토리가 `new` 대신 Pool에서 꺼내면 GC 없는 팩토리
- **과도한 추상화 주의** — 객체 종류 2개에 Abstract Factory는 오버엔지니어링. 직접 `new`가 더 명확한 경우 많음


#생성
> 관련: [[design-pattern-notes]] 항목 18 Object Pooling (Pool + Factory 조합) | 종속성: `#OOP` `#언어독립`

## 15. Composite

_단일 객체와 객체 집합을 동일한 인터페이스로 다루어, 트리 구조를 균일하게 처리하는 패턴._

**직관**
파일 시스템의 폴더 — 파일 하나나 폴더(여러 파일 포함) 모두 "열기"로 다룰 수 있음. 폴더 안 폴더도 동일 인터페이스.

**문제 상황**
단일 아이템과 묶음을 다르게 처리하면 클라이언트에 분기가 생김:
```csharp
void CalculateDamage(object source)
{
    if (source is WeaponEffect single)          total += single.damage;
    else if (source is List<WeaponEffect> combo) foreach (var e in combo) total += e.damage;
    // 새 "묶음 타입" 추가마다 여기에 else if 추가 필요
}
```
Composite으로 Leaf/Composite 모두 `IDamageSource`로 다루면 클라이언트는 타입 구분 없이 `source.CalculateDamage()`.

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

**언제 쓰나 / 피할 때**
- ✅ 단일 객체와 컬렉션을 동일하게 처리해야 할 때
- ✅ 트리 구조, 재귀적 포함 관계가 있을 때 (씬 계층, UI 트리, 스킬 트리)
- ❌ 구조가 flat list — `List<T>`와 LINQ가 더 단순
- ❌ Leaf와 Composite의 인터페이스 차이가 클 때 — Leaf에 빈 Add/Remove를 강제하게 됨

⚠ **주의점**
- **인터페이스에 Add/Remove 강제 문제** — Leaf도 Add/Remove를 구현해야 하면 어색. Composite 타입만 Add/Remove를 가지도록 분리
- **트리 순환 참조** — Composite가 자기 자신을 자식으로 추가하면 무한 루프. Guard 필요
- **집계 캐싱** — 깊은 트리에서 매 프레임 순회 비용이 크면 캐싱 고려


#구조
> 관련: [[design-pattern-notes]] 항목 13 Decorator (래퍼 방식 대안), 항목 10 Command (CompositeCommand) | 종속성: `#OOP` `#언어독립`

## 18. Object Pooling

_자주 생성/파괴되는 객체를 재사용 가능한 풀에서 꺼내쓰고 돌려놓아 GC 스파이크와 생성 비용을 제거._

**직관**
카페 컵 세척 재사용 — 컵을 쓸 때마다 새로 만들지 않고(new/GC) 씻어서(reset) 다시 꺼냄.

**문제 상황**
총알/이펙트를 매 발사마다 생성/파괴하면 GC 스파이크 발생:
```csharp
void Fire()
{
    var bullet = Instantiate(bulletPrefab);  // 매 발사 → Heap 할당
    bullet.Init(direction);
    // 목표 도달 시:
    Destroy(bullet.gameObject);  // 즉각 해제 → GC spike → 프레임 드랍
}
// 초당 30발 × 적 50마리 = 초당 1500 Instantiate/Destroy
```
Pool에서 꺼내고 돌려놓으면 GC 없이 재사용.

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

**언제 쓰나 / 피할 때**
- ✅ 동일 객체 생성/파괴가 초당 10회 이상 반복될 때 (총알, 이펙트, UI 아이템)
- ✅ 생성 비용이 높은 객체 (복잡한 초기화, 큰 프리팹)
- ❌ 드물게 생성되는 객체 — 풀 관리 비용이 이득보다 큼
- ❌ 씬에 고정 개수로 존재하는 정적 객체 — 풀 불필요

⚠ **주의점**
- **상태 오염** — Get 시 이전 사용 상태가 남아 있으면 버그. Get 또는 Release 시 반드시 Reset
- **Release 누락** — 돌려주지 않으면 풀이 비어서 결국 계속 `new` 발생. 수명 관리 객체에서 자동 Release 설계
- **풀 상한** — 상한 없이 풀이 커지면 메모리 증가. 최대 크기 + 초과 시 파괴 또는 경고
- **씬 전환** — `DontDestroyOnLoad`가 아닌 풀은 씬 전환 시 파괴됨. 풀 오브젝트 수명 맞추기


#생성 #성능
> 관련: [[design-pattern-notes]] 항목 22 Streaming Pattern (확장형의 필수 구성요소), 항목 14 Factory (Pool + Factory 조합) | 종속성: `#OOP` `#언어독립`

## 19. CRTP (Curiously Recurring Template Pattern)

_`class Foo<T> where T : Foo<T>` — 부모 제네릭이 자식 타입을 타입 파라미터로 받아서 타입 안전한 자기 참조를 구현._

**직관**
"나는 AudioManager야"를 부모 코드에서 컴파일 타임에 아는 것 — `Instance`를 꺼낼 때마다 캐스팅 없이 자식 타입으로 직접 반환.

**문제 상황**
CRTP 없는 Singleton은 매번 캐스팅 필요하거나, 각 클래스가 중복 코드 작성:
```csharp
// 방법 1: 기반 클래스 Instance → 매번 캐스팅 필요
class MonoSingleton : MonoBehaviour { public static MonoSingleton Instance { get; } }
((AudioManager)MonoSingleton.Instance).Play("hit"); // 런타임 캐스팅 — 틀리면 InvalidCastException

// 방법 2: 각 클래스가 중복 구현
class AudioManager : MonoBehaviour { static AudioManager _instance; ... } // 보일러플레이트 반복
class UIManager    : MonoBehaviour { static UIManager    _instance; ... } // 동일 코드 반복
```
CRTP로 `MonoSingleton<T>`로 만들면 `AudioManager.Instance`가 `AudioManager` 타입으로 직접 반환.

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

**언제 쓰나 / 피할 때**
- ✅ 부모가 자식 타입을 반환해야 하는 Singleton/Builder 패턴
- ✅ 모든 서브클래스에 타입 안전한 `Instance` 프로퍼티가 필요할 때
- ❌ Singleton 하나만 있는 경우 — 직접 `static Instance` 정의가 더 단순
- ❌ CRTP 외 복잡한 상속 계층 — 손자 클래스에서 동작 예측 어려움

⚠ **주의점**
- **where 제약 필수** — `where T : MonoSingleton<T>` 없으면 `(T)this` 캐스팅이 컴파일 타임 검증 불가
- **손자 클래스** — `class C : B` (`B : A<B>`)에서 C는 `A<C>`가 아님. CRTP는 1단계 상속에서만 완벽
- **남용 주의** — 타입 안전한 `this` 반환과 Singleton 외에 용도가 드묾. 명확한 이유 없으면 일반 제네릭으로 충분


#생성 #구조 #제네릭
> 관련: [[design-pattern-notes]] 항목 2 Singleton (CRTP의 대표 적용 사례) | 종속성: `#OOP` `#C#제네릭`
