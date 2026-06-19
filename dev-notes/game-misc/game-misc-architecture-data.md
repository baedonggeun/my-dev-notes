# 게임 잡기술 — 아키텍처·데이터

> 상위 노트: [[game-misc-notes]] (전체 인덱스 디스패처)
> 다루는 축: 아키텍처 패턴·데이터 관리·성능 최적화
> 다루지 않는 축: 게임 잡기술 — UI·렌더링

---


## 태그 목록

### 성격
- `#가드` `#트릭` `#캐시` `#UX` `#렌더링경계` `#초기화` `#트랜잭션` `#성능`

### 도메인
- `#UI` `#데이터` `#매니저` `#서비스`

### 의도
- `#NRE방지` `#race회피` `#일관성` `#성능`


---


# 인덱스

| # | 항목 | 성격 | 한 줄 요약 | 종속성 |
|---|------|------|----------|--------|
| 1 | EnsureInitialized 가드 | `#가드` `#NRE방지` | OnEnable 중복 호출 시 listener 재구독 누수 방지 | `#게임엔진일반` |
| 5 | SO + Lazy Dictionary Cache + Resources Fallback | `#캐시` `#데이터` | SO 룩업을 첫 접근 시 dict 캐시, 없으면 Resources에서 fallback | `#Unity전용` |
| 6 | Combination Callback Transaction Batching | `#트랜잭션` `#일관성` | 호출자가 slot 변경을 한 콜백 내에서 일괄 commit | `#언어독립` |
| 7 | 수동적 View 컴포지션 | `#UI` | View는 RectTransform/Image만 노출, Controller가 모든 로직 주입 | `#게임엔진일반` |
| 8 | Service 지연 주입 | `#초기화` `#race회피` | OnInitialize에서 Manager 조회로 init race 회피 | `#게임엔진일반` |
| 9 | SO Registry + 사전 캐시 | `#캐시` `#데이터` | 시작 시 룰을 dict로 빌드해 O(1) 룰 조회 | `#Unity전용` |
| 10 | PlayerPrefs Wrapper + 변경 브로드캐스트 | `#매니저` | 영속 설정 wrapper + 변경 시 이벤트 통지 | `#Unity전용` |
| 12 | `Array.Empty<T>()` GC 회피 | `#성능` `#캐시` | 빈 배열 반복 할당 대신 정적 공유 빈 배열 사용 — heap alloc 0 | `#언어독립` |

---

# 풀노트

## 1. EnsureInitialized 가드

_OnEnable 중복 발화 시에도 초기화 로직이 1회만 실행되도록 bool 가드 + 전용 OnInitialize 메서드로 분리._

**코드**
```csharp
// UIBinderBase (CasualStrategy) — 공통 베이스 패턴
public abstract class UIBinderBase : MonoBehaviour
{
    protected bool Initialized { get; private set; }

    protected virtual void OnEnable()
    {
        EnsureInitialized();
        Subscribe();
        SyncState();
    }

    protected virtual void OnDisable() => Unsubscribe();

    protected void EnsureInitialized()
    {
        if (Initialized) return;
        OnInitialize();
        Initialized = true;
    }

    protected virtual void OnInitialize() { } // 최초 1회: heavy init, Service 조회
    protected abstract void Subscribe();      // 매 OnEnable: 이벤트 구독
    protected abstract void Unsubscribe();    // 매 OnDisable: 이벤트 해제
    protected virtual void SyncState() { }   // 매 OnEnable: 즉시 상태 동기화
}
```

서브클래스 사용:
```csharp
public class InventoryUIBinder : UIBinderBase
{
    private RunManager _run;

    protected override void OnInitialize()
        => _run = RunManager.Instance; // 1회만

    protected override void Subscribe()   => _run.OnQueueChanged += Refresh;
    protected override void Unsubscribe() => _run.OnQueueChanged -= Refresh;
    protected override void SyncState()   => Refresh();
}
```

**언제 / 대안**
✅ 탭 전환·오브젝트 활성화로 OnEnable이 반복 발화되는 UI에서 heavy init(Service 조회, dict 빌드)을 1회로 제한할 때
⚡ 대안: Awake에서 초기화 — 실행 순서 미설정 시 race 가능
⚡ 대안: OnEnable/OnDisable 대칭만 — 매 활성마다 재초기화되어 heavy 비용 중복

⚠ **주의점**
- `Initialized = true`는 OnInitialize() **이후** 세트. 예외 시 false 유지 → 다음 OnEnable에서 재시도 가능
- `Initialized`를 private set으로 막아야 서브클래스가 임의 세트 불가


#가드 #NRE방지 #초기화
> 관련: [[game-misc-notes]] 항목 8 Service 지연 주입 | 종속성: `#게임엔진일반`

---

## 5. SO + Lazy Dictionary Cache + Resources Fallback

_SO 참조를 SerializeField로 받고 초기화 시 dict로 캐시. SerializeField가 비어 있으면 Resources.Load로 fallback._

**코드**
```csharp
// DataManager (CasualStrategy)
[SerializeField] private CombinationConfigSO combinationConfig;

protected override void InitSingleton()
{
    // SerializeField 미와이어링 시 Resources fallback
    if (combinationConfig == null)
        combinationConfig = Resources.Load<CombinationConfigSO>("ScriptableObjects/CombinationConfig");

    BuildRuleCache();
}

private Dictionary<(string, AttributeType), CombinationRule> ruleCache;

private void BuildRuleCache()
{
    ruleCache = new Dictionary<(string, AttributeType), CombinationRule>();
    if (combinationConfig?.rules == null) return;
    foreach (var r in combinationConfig.rules)
    {
        if (r.weaponItem == null || r.attrType == AttributeType.None || r.resultItem == null) continue;
        ruleCache[(r.weaponItem.itemId, r.attrType)] = r;
    }
}

public CombinationRule? GetCombinationRule(string weaponId, AttributeType attrType)
    => ruleCache.TryGetValue((weaponId, attrType), out var r) ? r : null;
```

**언제 / 대안**
✅ SO 리스트 10개 이상 + 런타임 룩업이 빈번(전투 중 다수 호출)할 때
⚡ 대안: LINQ FirstOrDefault — 코드 간단하나 O(n) + GC alloc
⚡ 대안: Resources.Load만 사용 — Inspector 배치 불가. 경로 하드코딩, SO 이동 시 조용히 null

⚠ **주의점**
- Resources.Load 경로는 `Assets/Resources/` 하위 상대 경로. 대소문자 구분(Mac/iOS는 구분 있음)
- struct 튜플 `(string, Enum)` 키는 기본 GetHashCode가 필드 값 기반으로 동작 — 안전
- SO 에디터 수정 후 PlayMode 재진입 시 InitSingleton이 재실행되어 캐시 자동 갱신


#캐시 #데이터
> 관련: [[game-misc-notes]] 항목 9 SO Registry + 사전 캐시 (유사 패턴 — Awake 즉시 빌드 vs SerializeField null 방어 포함) | 종속성: `#Unity전용`

---

## 6. Combination Callback Transaction Batching

_복수 슬롯/상태 변경을 `BeginBatch() → 변경들 → EndBatch()` 패턴으로 묶어 `OnChanged` 콜백을 단 1회만 발화. 중간 상태에 반응하는 race 조건 차단._

**설명**
슬롯 교체, 장비 변경, 카드 조합처럼 *여러 상태를 동시에 바꾸는* 동작에서 변경 순서가 중요할 때 발생하는 문제:

```
slot[0] = newCard   → OnQueueChanged 발화 → 구독자가 중간 상태를 읽어 잘못된 시너지 계산
slot[1] = null
```

Batching은 이 순서 문제를 해결:
```
BeginBatch()      → batchActive = true
slot[0] = newCard → dirty만 표시, 발화 안 함
slot[1] = null    → dirty만 표시
EndBatch()        → OnQueueChanged 1회 발화 (완성된 상태)
```

**구현**
```csharp
// RunManager 예시 (CasualStrategy)
public class RunManager : MonoSingleton<RunManager>
{
    public event Action OnQueueChanged;

    private bool _batchActive;
    private bool _batchDirty;

    public void BeginQueueBatch()
    {
        _batchActive = true;
        _batchDirty = false;
    }

    public void EndQueueBatch()
    {
        _batchActive = false;
        if (_batchDirty)
        {
            _batchDirty = false;
            OnQueueChanged?.Invoke();
        }
    }

    private void NotifyQueueChanged()
    {
        if (_batchActive)
            _batchDirty = true;       // batch 중 → 예약만
        else
            OnQueueChanged?.Invoke();  // 즉시 발화
    }

    // 외부 호출 예 — BeginBatch 없이 단일 변경 시 즉시 발화
    public void SwapCards(int from, int to)
    {
        BeginQueueBatch();
        try
        {
            SetSlotInternal(from, _slots[to]);
            SetSlotInternal(to, _slots[from]);
        }
        finally
        {
            EndQueueBatch();   // 여기서 OnQueueChanged 1회
        }
    }
}
```

외부에서 복수 변경:
```csharp
runManager.BeginQueueBatch();
try
{
    runManager.SetSlot(0, newCard);
    runManager.ClearSlot(1);
    runManager.SetSlot(2, anotherCard);
}
finally
{
    runManager.EndQueueBatch();   // OnQueueChanged 1회
}
```

⚠ **주의점**
- **EndBatch 빠뜨림** — `BeginBatch`만 호출하고 `EndBatch` 누락 시 이후 단일 변경도 콜백이 영원히 발화 안 됨. `try/finally` 패턴으로 누락 차단
- **CQS 부분 위반 (의도적)** — `EndBatch`는 상태 변경(batchActive=false) + 이벤트 발화를 동시에 함. "완료 시점에 정확히 1회 통지"라는 원자성이 목적이므로 분리가 의미 없음 (software-principle-notes 항목 29 CQS 의도된 위반 참조)
- **batch 중 예외** — 변경 중 예외가 나면 `batchActive=true` 채로 스택이 풀릴 수 있음. `try/finally` 없으면 Manager가 영구 배치 상태로 고착
- **재진입 (nested batch)** — `BeginBatch` 내부에서 또 `BeginBatch`가 불리면 두 번째 `EndBatch`가 첫 batch를 닫아버림. 재진입 가능성이 있으면 `int _batchDepth`로 교체: `++_batchDepth`, `--_batchDepth; if (_batchDepth == 0) fire`


#트랜잭션 #일관성 #race회피
> 관련: software-principle-notes 항목 29 CQS (의도된 위반), design-pattern-notes Observer (OnChanged 패턴 기반) | 종속성: `#언어독립`

---

## 7. 수동적 View 컴포지션

_View는 [SerializeField] 참조만 노출하는 dumb holder. Controller/Binder가 View를 참조하고 모든 로직과 이벤트를 처리._

**코드**
```csharp
// View — 참조만, 로직/이벤트 없음
public class RewardPopupView : MonoBehaviour
{
    [SerializeField] private RewardBoxView[] rewardBoxes;
    [SerializeField] private CanvasGroup canvasGroup;
    [SerializeField] private Button confirmButton;

    public RewardBoxView[] RewardBoxes => rewardBoxes;
    public CanvasGroup CanvasGroup => canvasGroup;
    public Button ConfirmButton => confirmButton;
}

// Controller — View 참조, 모든 로직 여기에
public class RewardPopupController : MonoBehaviour
{
    [SerializeField] private RewardPopupView view;

    void OnEnable()
    {
        view.ConfirmButton.onClick.AddListener(OnConfirm);
        Fill(RunManager.Instance.PendingRewards);
    }

    void OnDisable()
        => view.ConfirmButton.onClick.RemoveListener(OnConfirm);
}
```

**언제 / 대안**
✅ prefab 자식 참조 3개 이상 + 로직 2가지 이상일 때 분리 효과 발생
⚡ 대안: 단일 MonoBehaviour — UI가 소규모(슬롯 1~2개, 로직 1개)면 분리 오버헤드가 더 큼

⚠ **주의점**
- View 프로퍼티를 public set으로 열면 외부에서 참조 교체 가능 → private set + readonly 프로퍼티 유지
- View에 이벤트 등록 코드 추가 유혹을 피할 것. `Button.onClick.AddListener`는 Controller에서만


#UI

> 관련: design-pattern-notes MVC/MVP (패턴 승격 후보) | 종속성: `#게임엔진일반`

---

## 8. Service 지연 주입

_Manager.Instance 조회를 Awake가 아닌 OnInitialize(첫 OnEnable)로 지연해 init race 회피._

**코드**
```csharp
// UIBinderBase 패턴 — OnInitialize는 EnsureInitialized가 최초 1회 호출
public class InventoryUIBinder : UIBinderBase
{
    private RunManager _run;
    private DataManager _data;

    // Bad: Awake에서 조회 — RunManager.Awake가 아직 안 돌면 null
    // void Awake() { _run = RunManager.Instance; }

    // Good: 첫 OnEnable 시점 = 씬 활성화 후 → 모든 MonoBehaviour.Awake 완료
    protected override void OnInitialize()
    {
        _run  = RunManager.Instance;
        _data = DataManager.Instance;
    }

    protected override void Subscribe()   => _run.OnQueueChanged += Refresh;
    protected override void Unsubscribe() => _run.OnQueueChanged -= Refresh;
}
```

**언제 / 대안**
✅ MonoBehaviour Awake 실행 순서 미보장 (DefaultExecutionOrder 미설정) 환경
⚡ 대안: `[DefaultExecutionOrder(-100)]`을 Manager에 부여 — 커플링 강화, Manager 추가 시 숫자 조정 필요
⚡ 대안: Start()에서 조회 — Awake보다 나중이지만 Start도 순서 보장 안 됨

⚠ **주의점**
- OnInitialize 호출은 "첫 OnEnable"이지 씬 완전 로드 후가 아님. 씬 전환 연출 중 오브젝트가 활성화되면 Manager Awake 완료 전일 수 있음
- MonoSingleton의 InitSingleton이 Awake에서 실행된다면 씬 내 Manager prefab이 UIBinder보다 먼저 배치되어야 함


#초기화 #race회피
> 관련: [[game-misc-notes]] 항목 1 EnsureInitialized 가드 (OnInitialize를 1회 호출하는 메커니즘) | 종속성: `#게임엔진일반`

---

## 9. SO Registry + 사전 캐시

_Manager Awake 시 SO 리스트를 dict로 빌드. 이후 모든 룩업은 O(1) dict 탐색._

**코드**
```csharp
// DataManager (CasualStrategy)
private Dictionary<(string, AttributeType), CombinationRule> ruleCache;

private void BuildRuleCache()
{
    ruleCache = new Dictionary<(string, AttributeType), CombinationRule>();
    if (combinationConfig?.rules == null) return;
    foreach (var r in combinationConfig.rules)
    {
        if (r.weaponItem == null || r.attrType == AttributeType.None || r.resultItem == null) continue;
        ruleCache[(r.weaponItem.itemId, r.attrType)] = r;
    }
}

public bool HasCombinationRule(string weaponId, AttributeType attrType)
    => ruleCache != null && ruleCache.ContainsKey((weaponId, attrType));

public CombinationRule? GetCombinationRule(string weaponId, AttributeType attrType)
    => ruleCache != null && ruleCache.TryGetValue((weaponId, attrType), out var r) ? r : null;
```

**언제 / 대안**
✅ SO 리스트를 반복 조회(전투 로직, 툴팁 갱신 등 프레임 단위)할 때
⚡ 대안: foreach 직접 탐색 — 리스트 10개 이하·호출 드물면 충분. 빌드 비용 없음
⚡ 대안: LINQ FirstOrDefault — 가독성 높지만 GC alloc 있음

⚠ **주의점**
- dict는 InitSingleton(Awake) 시점 SO 값으로 확정. 런타임 중 SO 내용 변경은 dict에 반영 안 됨
- 동일 키가 rules에 여러 개이면 나중 것이 덮어씀. 에디터에서 중복 방지 필요


#캐시 #데이터
> 관련: [[game-misc-notes]] 항목 5 SO + Lazy Dictionary Cache + Resources Fallback (유사 패턴 — Awake 즉시 빌드 vs lazy + null 방어) | 종속성: `#Unity전용`

---

## 10. PlayerPrefs Wrapper + 변경 브로드캐스트

_PlayerPrefs 읽기/쓰기를 정적 래퍼로 캡슐화. 키 분산·오타 방지 + 필요 시 변경 이벤트 추가._

**코드**
```csharp
// GameSettings (CasualStrategy) — 정적 래퍼
public static class GameSettings
{
    private const string KEY_PREFIX = "Skip_";
    private const string VOLUME_PREFIX = "Volume_";
    private const float DefaultVolume = 0.5f;

    public static bool ShouldSkip(SkipCategory category)
        => PlayerPrefs.GetInt(KEY_PREFIX + category, 0) == 1;

    public static void SetSkip(SkipCategory category, bool value)
    {
        PlayerPrefs.SetInt(KEY_PREFIX + category, value ? 1 : 0);
        PlayerPrefs.Save();
    }

    public static float GetVolume(AudioChannel channel)
        => PlayerPrefs.GetFloat(VOLUME_PREFIX + channel, DefaultVolume);

    public static void SetVolume(AudioChannel channel, float linear01)
    {
        PlayerPrefs.SetFloat(VOLUME_PREFIX + channel, Mathf.Clamp01(linear01));
        PlayerPrefs.Save();
    }
}
```

브로드캐스트 확장 (설정 UI가 여러 곳일 때):
```csharp
public static event Action<SkipCategory, bool> OnSkipChanged;

public static void SetSkip(SkipCategory category, bool value)
{
    PlayerPrefs.SetInt(KEY_PREFIX + category, value ? 1 : 0);
    PlayerPrefs.Save();
    OnSkipChanged?.Invoke(category, value);
}
```

**언제 / 대안**
✅ 설정 키가 3개 이상이고 여러 파일에서 읽을 때 — 키 문자열 분산 방지
✅ 브로드캐스트 확장: 설정 패널이 여러 곳에서 같은 값을 표시할 때 (변경 시 모두 갱신)
⚡ 대안: PlayerPrefs 직접 사용 — 키 오타 위험, 기본값 로직 분산

⚠ **주의점**
- `PlayerPrefs.Save()`는 I/O 비용 있음. SetVolume을 슬라이더 OnValueChanged에 직접 연결하면 드래그마다 파일 쓰기 → OnEndDrag에서 1회만 호출
- 정적 이벤트는 씬 전환 후에도 구독이 남아 있음. 구독자가 OnDisable에서 해제하지 않으면 파괴된 오브젝트 참조


#매니저

> 관련: unity-feature-notes PlayerPrefs | 종속성: `#Unity전용`

---

## 12. `Array.Empty<T>()` GC 회피

_빈 배열이 필요할 때 `new T[0]` 대신 `System.Array.Empty<T>()`. BCL 내부 정적 캐시 반환 — heap alloc 0._

**코드**
```csharp
// Before — 매 호출 heap alloc
return new RectTransform[0];

// After — 정적 공유 인스턴스, alloc 0
return System.Array.Empty<RectTransform>();
```

실제 사용 (TutorialOverlayController):
```csharp
// 첫 sub-action 진입 시 빈 배열로 초기화
ApplySubAction(System.Array.Empty<RectTransform>(), sa.arrow, sa.kind, data.completionType);

// null 방어 기본값
effectiveRts = rts ?? System.Array.Empty<RectTransform>();
```

**언제 / 대안**
⚡ 배열을 반환/전달해야 하지만 항목이 없는 경우 (null 대신 빈 배열 정책)
⚡ 대안: null 반환 — 수신 측 null 체크 강요, NullReferenceException 위험
⚡ 대안: `new T[0]` — 핫 경로가 아니면 실용적 차이 없음. 의미는 동일

⚠ **주의점**
- 반환된 배열은 길이 0의 공유 인스턴스. 쓰기 시 IndexOutOfRangeException
- foreach는 빈 배열에 안전하게 루프 0회 실행 — null 체크 없이 foreach 가능


#성능 #캐시
> 관련: csharp-syntax-notes Span/Memory (유사 GC 최적화 계열) | 종속성: `#언어독립`