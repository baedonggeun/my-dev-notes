# Unity 기능 — 코어·라이프사이클

> 상위 노트: [[unity-feature-notes]] (전체 인덱스 디스패처)
> 다루는 축: 라이프사이클·ScriptableObject·코루틴·SerializeField·DontDestroyOnLoad
> 다루지 않는 축: [[unity-feature-ui|Unity 기능 — UI 시스템]] / [[unity-feature-misc|Unity 기능 — 오디오·렌더링·에디터·유틸]]

---


## 태그 목록

### 카테고리
- `#코어` `#UI` `#오디오` `#렌더링` `#물리` `#에디터` `#데이터` `#수학` `#디버그`

### 패키지/모듈
- `#URP` `#TMP` `#Physics2D` `#uGUI` `#ShaderGraph` `항목 2DFeature`

### 사용 빈도
- `#필수` `#보조` `#일회성`


---


# 인덱스

### 코어 엔진
| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 1 | MonoBehaviour 라이프사이클 (Awake/OnEnable/OnDisable/Update/OnDestroy) | Unity 컴포넌트 표준 진입점 — 초기화/활성화/매 프레임/정리 시점 | `#Unity전용` `#필수` |
| 2 | ScriptableObject + `[CreateAssetMenu]` | GameObject 독립적 데이터 자산 — 씬 간 공유 + Inspector 편집 | `#Unity전용` `#필수` |
| 3 | Coroutine / IEnumerator / yield | yield 기반 비동기 흐름 (트윈/대기/순차 연출) | `#Unity전용` `#필수` |
| 4 | `[SerializeField]` / `[Serializable]` | private 필드 Inspector 노출 + 직렬화 | `#Unity전용` `#필수` |
| 5 | `DontDestroyOnLoad` + `Application.isPlaying` / `OnApplicationQuit` | 씬 전환 시에도 유지되는 GameObject + 종료 시 안전 처리 | `#Unity전용` |
| 6 | `FindObjectsByType` / `GetComponent` / `Instantiate` / `Destroy` | 런타임 객체 조회/생성/소멸 기본 API | `#Unity전용` `#필수` |
| 31 | `[RequireComponent(typeof(T))]` | 동일 GameObject에 의존 컴포넌트 자동 추가 + Awake에서 GetComponent 보장 | `#Unity전용` |
| 34 | `OnValidate` | Inspector에서 SerializeField 값 변경 시 호출되는 에디터 콜백 — 배열 정규화, 값 검증, 의존 자산 동기화 | `#Unity전용` `#에디터` |
| 36 | `[DefaultExecutionOrder(N)]` | 컴포넌트 Awake/Update 등의 실행 순서를 정수값으로 강제 — 매니저 초기화 순서 의존 시 사용 | `#Unity전용` |
| 36 | CanvasGroup 기반 UI Pool | `SetActive` 대신 `CanvasGroup.alpha=0 + blocksRaycasts=false`로 풀 인스턴스 hidden 처리 — OnEnable/OnDisable 발화 없이 렌더링만 차단, 풀 복귀 시 parent 재배치 후 재사용 | `#Unity전용` `#uGUI` `#Pool` |
| 41 | GameObject 비활성화 시 코루틴 silent 정지 함정 | `SetActive(false)` 시 Unity가 자식 코루틴을 예외 없이 정지 → `isRunning`/`isPlaying` 같은 진행 플래그가 reset 안 되어 다음 활성화 시 dead-lock. 대응 3중 안전망: (1) **호스트 이동** — 코루틴 호스트 GameObject를 토글되는 부모 밖으로 옮겨 silent 정지 자체를 차단(원천 해결), (2) **`try/finally`** — `StopCoroutine`/`StopAllCoroutines` 명시 정지 경로의 플래그 누락 방지(단 SetActive 경로는 finally 실행 보장 안 됨), (3) **`OnDisable` cleanup** — 다른 부모 비활성 시나리오 대비 잔여 플래그/큐 reset. 외부 정지는 `Cancel{Op}()` 래핑으로 정상 흐름과 분리 | `#Unity전용` `#코루틴` |

---

# 풀노트

## 2. ScriptableObject + `[CreateAssetMenu]`

_GameObject/씬에 독립적으로 존재하는 데이터 에셋. 씬 간 공유 + Inspector 편집. "설정·데이터·풀의 SOT"를 코드 대신 에셋으로 관리._

**설명**
`ScriptableObject`(SO)는 `MonoBehaviour`와 달리 GameObject에 붙지 않아도 에셋으로 저장·공유된다.

핵심 가치:
1. **씬 독립성** — 씬이 바뀌어도 SO 에셋은 유지. 여러 GameObject가 같은 에셋을 참조
2. **디자이너 편집** — 코드 수정 없이 Inspector에서 데이터 조정
3. **메모리 공유** — 100개 GameObject가 같은 SO를 참조해도 SO는 메모리에 1개만

MonoBehaviour와 결정 기준:
| 항목 | ScriptableObject | MonoBehaviour |
|---|---|---|
| 씬에 존재 필요 | 불필요 | 필요 |
| 런타임 상태 | 에셋에 직접 기록됨 | 씬 인스턴스에 기록 |
| 씬 전환 후 유지 | 유지 (에셋) | 사라짐 (씬 오브젝트) |
| 코루틴 | 불가 | 가능 |
| 생명주기 콜백 | 없음 (`OnEnable` 제한적) | Awake/Update 등 전부 |

사용 패턴 3가지:
- **데이터 컨테이너**: `WeaponDataSO`, `EnemyPresetSO` — 수치/설정 데이터 저장
- **런타임 공유 상태**: 복수 오브젝트가 같은 SO를 수정·읽기 (인스턴스 공유 함정 주의)
- **서비스 규칙 풀**: 시너지 규칙, 드롭 확률 → Manager가 로드 후 Dictionary 빌드

**구현**
```csharp
// 데이터 컨테이너 SO
[CreateAssetMenu(menuName = "CasualStrategy/WeaponData", fileName = "WeaponDataSO")]
public class WeaponDataSO : ScriptableObject
{
    [field: SerializeField] public string WeaponName { get; private set; }
    [field: SerializeField] public float BaseDamage { get; private set; }
    [SerializeField] private int _maxEnhanceLevel;
    public int MaxEnhanceLevel => _maxEnhanceLevel;
}

// 사용
[SerializeField] private WeaponDataSO _weaponData;
float dmg = _weaponData.BaseDamage;

// Resources.Load (런타임 동적 로드)
var so = Resources.Load<WeaponDataSO>("Data/Weapons/SwordSO");
```

⚠ **Unity 함정**
- **인스턴스 공유 함정** — 런타임에 SO 필드를 직접 수정하면 (`weaponData.baseDamage = 100`) *모든 참조자*에게 영향. 에디터 Play Mode에서 수정 시 에셋 파일에 영구 기록됨 (빌드에서는 기록 안 됨). 런타임에 변형이 필요하면 `Instantiate(so)`로 사본 사용
- **에디터 vs 빌드 동작 차이** — 에디터 Play Mode에서 SO 수정은 에셋에 기록. 빌드에서는 read-only. 이 차이로 에디터 테스트는 통과하지만 빌드에서 초기값이 유지되는 버그 발생 가능
- **`[CreateAssetMenu]` 경로** — `menuName`의 "/"는 에디터 메뉴 계층. `"CasualStrategy/WeaponData"` = 우클릭 → Create → CasualStrategy → WeaponData
- **Resources.Load 경로 오타** — `Resources/` 폴더 안 상대 경로, 확장자 없이. 오타는 null 반환 (silent fail) — 로드 후 null 체크 필수
- **OnEnable 제한** — SO도 `OnEnable` 콜백이 있으나 에셋 로드 시점에 호출. MonoBehaviour와 달리 씬 전환으로 재호출되지 않음
- **SerializeReference와 조합** — SO 안의 필드에 `[SerializeReference]`를 쓰면 폴리모픽 자식 타입 인라인 직렬화 가능 (항목 42 참고). 단, deep clone 요구사항이 생김


`#코어` `#데이터` `#필수`
> 관련: [[unity-feature-notes]] 항목 4 SerializeField/Serializable, 항목 42 SerializeReference, 항목 22 Resources.Load | 종속성: `#Unity전용` `#필수`
## 사용 안 한 Unity 기능 (참고)

- **Animation Clip / Animator (CasualStrategy 범위)** — 트윈 유틸로 대체. Animator Layer + Avatar Mask 자체는 항목 40으로 등재 (복수 프로젝트)
- **Cinemachine** — 카메라 단순
- **Physics 3D** — 2D 전용
- **Addressables (CasualStrategy 범위)** — Resources.Load만 사용. Addressables + Pool 조합은 design-pattern 항목 22 Streaming Pattern으로 등재 (복수 프로젝트)
- **DOTS / ECS** — N/A
- **UI Toolkit (VisualElement)** — uGUI 전용
- **Networking** — 싱글플레이어
- **Unity Localization Package** — 자체 JSON 시스템 사용

---

---

# 풀노트

---

## 36. CanvasGroup 기반 UI Hide / Pool

_`SetActive(false)` 대신 `CanvasGroup.alpha=0 + blocksRaycasts=false + interactable=false` 조합으로 UI를 hidden 처리. OnEnable/OnDisable 발화 없이 렌더링/입력만 차단해 코루틴·이벤트 구독·풀 인스턴스 상태를 보존._

**설명**
Unity의 `SetActive(false)`는 강력하지만 부작용이 크다:
- **OnDisable 발화** → 자식 코루틴 silent 정지, 이벤트 구독 해제, 캐시 무효화 등 라이프사이클 처리 트리거
- **OnEnable 재발화** → 다시 켜면 초기화 비용 반복
- **Hierarchy 재활성화 비용** → 자식 컴포넌트들의 OnEnable 연쇄

UI는 보통 "보였다 안 보였다"가 자주 발생하는데(탭 전환, 모달 토글, 풀 hidden 등) `SetActive` 토글로 처리하면 매번 라이프사이클이 돈다.

`CanvasGroup` 3종 세트가 대안:
- `alpha = 0` — 렌더링 차단 (자식 모두 투명)
- `blocksRaycasts = false` — 마우스/터치 입력 통과 (아래 UI가 받음)
- `interactable = false` — 자식 Selectable(Button 등) 비활성화 (Selectable.IsInteractable 체크 시점에 차단)

GameObject는 활성 상태를 유지하므로 OnEnable/OnDisable 발화 없음 → 라이프사이클 부작용 0.

대표 응용 패턴 2가지:

**(A) 탭/패널 전환 — 단순 hide**
같은 부모 아래 N개 패널이 alternating으로 보임/안 보임. SetActive 토글하면 매 전환마다 panel 내부 컴포넌트 OnEnable 발화 → 무거움. CanvasGroup 토글이 표준.

**(B) UI Pool — 풀 인스턴스 hidden 유지**
GameObject pool에서 사용 중이 아닌 인스턴스를 어딘가에 "숨겨" 보관. SetActive(false)로 숨기면 풀에서 꺼낼 때 OnEnable이 발화 → 매번 초기화 비용. CanvasGroup으로 숨기면 alpha만 토글 → 거의 0 비용 재사용.

**구현 — (A) TabController (CasualStrategy)**
```csharp
public class TabController : MonoBehaviour
{
    [SerializeField] private Button[] tabs;
    [SerializeField] private CanvasGroup[] panels;

    public void SelectTab(int index)
    {
        for (int i = 0; i < panels.Length; i++)
        {
            bool selected = i == index;
            panels[i].alpha = selected ? 1f : 0f;
            panels[i].blocksRaycasts = selected;
            panels[i].interactable = selected;
        }
    }
}
```

**구현 — (B) Popup Pool (CasualStrategy 변형)**
```csharp
// 풀 인스턴스 생성 시: alpha=0 + SetActive(false) 동시 적용
private GameObject CreatePooledInstance(GameObject prefab)
{
    var go = Instantiate(prefab, poolRoot);
    var cg = EnsureCanvasGroup(go);
    cg.alpha = 0f;
    cg.blocksRaycasts = false;
    // Why: prewarm 인스턴스가 active로 남아 prefab 기본 텍스트가 spawnAnchor 위치에 잔존
    //      (alpha=0이어도 TMP material 조합에 따라 흐릿하게 보임)
    go.SetActive(false);
    return go;
}

// 사용 시 (Get): SetActive(true) + alpha=1
go.SetActive(true);
cg.alpha = 1f; cg.blocksRaycasts = false;  // raycast는 hit 불필요한 popup

// 반환 시 (Release): alpha=0 + SetActive(false)
cg.alpha = 0f; cg.blocksRaycasts = false;
go.transform.SetParent(poolRoot, false);
go.SetActive(false);
pool.Enqueue(go);
```

CasualStrategy의 PopupSpawner는 "순수 CanvasGroup-only"가 아니라 **하이브리드**다. alpha=0만으로는 TMP_Text의 SDF material 조합에 따라 흐릿하게 잔존하는 케이스가 있어 풀 인스턴스에는 SetActive(false)도 함께 적용. 이는 노트 항목 36의 순수 패턴에서 한 단계 진화한 형태.

⚠ **Unity 함정**
- **`alpha=0`만으로 입력은 차단되지 않음** — 알파 0이어도 Image의 Raycast Target이 켜져있으면 마우스를 흡수한다. `blocksRaycasts=false`를 반드시 함께. 이거 빠뜨려서 "안 보이는데 클릭이 안 되는 다른 UI" 버그 자주 발생
- **`interactable=false`는 시각 효과 동반** — Selectable(Button)의 disabled color가 적용되어 회색 처리됨. 단순 입력 차단만 원하면 `blocksRaycasts=false`만으로 충분 (Button 내부 hover/press 검사는 raycast가 막히면 자동 차단)
- **TMP material 조합 함정** — alpha=0이어도 일부 TMP material(특히 outline/glow 설정)에서 흐릿하게 잔존. prewarm/풀 인스턴스는 `SetActive(false)` 병행 권장 (CasualStrategy 사례)
- **부모 CanvasGroup 곱셈** — 자식 CanvasGroup의 alpha는 부모 CanvasGroup의 alpha와 곱해진다. 자식만 alpha=1이어도 부모가 0.5면 최종 0.5. 의도 외 동작 주의
- **`ignoreParentGroups`** — 위 곱셈을 무시하고 싶으면 자식 CanvasGroup의 `ignoreParentGroups=true` (드물게 사용. 모달 dialog가 어두워진 부모 위에 또렷이 떠야 할 때)
- **layout 비용은 안 줄어듦** — alpha=0이어도 LayoutGroup은 여전히 자식 크기를 계산해 배치한다. 보이지 않아도 레이아웃 계산 비용 발생. 진짜 숨기고 layout에서도 제외하려면 SetActive(false) 또는 `LayoutElement.ignoreLayout=true`
- **draw call은 줄어듦** — alpha=0인 Image/Text는 Unity가 자동으로 batch에서 제외 (Canvas dirty 검사 후). 따라서 GPU 비용은 안 듦. CPU layout 비용만 남음
- **풀 인스턴스의 부모 변경** — pool에 반환할 때 `SetParent(poolRoot)` 호출하면 LayoutGroup이 다시 dirty되어 레이아웃 재계산. 자주 발생하면 `poolRoot`를 LayoutGroup이 없는 빈 RectTransform으로 두기
- **CanvasGroup 컴포넌트 자체의 비용** — 매 frame Canvas dirty 검사에 포함됨. 패널마다 하나씩 다는 정도는 무시 가능하지만, 수백 개 풀 인스턴스 각각에 다는 건 측정 후 결정
- **이벤트 구독은 그대로 살아있음** — GameObject active이므로 OnEnable에서 구독한 이벤트, 코루틴, Update는 모두 동작 중. hidden 상태에서 동작이 의도와 다르면 명시적으로 `enabled = false` 또는 내부 플래그로 게이팅


#UI #uGUI #Pool #성능 #라이프사이클
> 관련: [[unity-feature-notes]] 항목 7 Canvas/CanvasGroup/RectTransform, 항목 41 GameObject 비활성화 silent 코루틴 정지 함정 (대응책 중 하나) | 종속성: `#Unity전용` `#uGUI` (CanvasGroup은 uGUI 전용. UI Toolkit은 다른 메커니즘)