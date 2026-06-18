# Unity 엔진 기능 노트

> 다루는 축: Unity 빌트인 API / 패키지 / 에디터 기능 카탈로그. "이 기능을 어디서 어떻게 썼더라" reference
> 다루지 않는 축: Unity 독립적 개념/패턴(→ [[design-pattern-notes]], [[math-algorithm-notes]])
> 적용 범위: **Unity 전용** — 본 노트는 의도적으로 엔진 종속. 다른 엔진 이주 시 대부분 폐기 대상
> 관련 노트: [[game-misc-notes]] (Unity API 응용 트릭), [[math-algorithm-notes]] (Mathf 개념 본체)
> 평생 노트 정책: 인덱스 표는 카탈로그 형식, 풀노트는 C# 실제 코드 + Unity 함정
> 승격 임계치: 카테고리당 항목 10개 이상 시 카테고리별 분리 검토
> 풀노트 작성 기준: 인덱스 1줄만으로 구현/적용이 불충분한 항목. 자명한 항목만 인덱스로 종료
> 작성 시작: 2026-05-15

---

## 태그 목록

### 카테고리
- `#코어` `#UI` `#오디오` `#렌더링` `#물리` `#에디터` `#데이터` `#수학` `#디버그`

### 패키지/모듈
- `#URP` `#TMP` `#Physics2D` `#uGUI` `#ShaderGraph` `#2DFeature`

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
| 41 | GameObject 비활성화 시 코루틴 silent 정지 함정 | `SetActive(false)` 시 Unity가 자식 코루틴을 예외 없이 정지 → `isRunning`/`isPlaying` 같은 진행 플래그가 reset 안 되어 다음 활성화 시 dead-lock. 대응 3중 안전망: (1) **호스트 이동** — 코루틴 호스트 GameObject를 토글되는 부모 밖으로 옮겨 silent 정지 자체를 차단(원천 해결), (2) **`try/finally`** — `StopCoroutine`/`StopAllCoroutines` 명시 정지 경로의 플래그 누락 방지(단 SetActive 경로는 finally 실행 보장 안 됨), (3) **`OnDisable` cleanup** — 다른 부모 비활성 시나리오 대비 잔여 플래그/큐 reset. 외부 정지는 `Cancel{Op}()` 래핑으로 정상 흐름과 분리 | `#Unity전용` `#코루틴` |

### UI (uGUI)
| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 7 | Canvas / CanvasGroup / RectTransform | UI 렌더 루트 + 페이드/인터랙션 토글 + UI 좌표계 | `#Unity전용` `#uGUI` `#필수` |
| 8 | Button / Image / TextMeshProUGUI | 기본 UI 위젯 트리오 | `#Unity전용` `#uGUI` `#TMP` |
| 9 | LayoutGroup (Horizontal/Vertical/Grid) + ContentSizeFitter | 자동 레이아웃 + 자식 크기 기반 컨테이너 | `#Unity전용` `#uGUI` |
| 10 | EventSystem + IBegin/Drag/EndDragHandler | 마우스/터치 이벤트 인터페이스 (드래그 시퀀스) | `#Unity전용` `#uGUI` |
| 11 | ScrollRect | 가변 컨텐츠 스크롤 컨테이너 | `#Unity전용` `#uGUI` |
| 12 | Canvas RenderMode (ScreenSpaceOverlay / WorldSpace) | UI 렌더 모드 (오버레이 vs 월드 공간) | `#Unity전용` `#uGUI` |
| 13 | RectTransformUtility (Screen↔Canvas 좌표 변환) | 스크린 좌표 ↔ Canvas 로컬 좌표 변환 | `#Unity전용` `#uGUI` |
| 32 | `ICanvasRaycastFilter` | UI 컴포넌트에서 raycast 통과 영역을 커스터마이징 (튜토리얼 cutout, 도넛 hole 등) | `#Unity전용` `#uGUI` |
| 44 | Custom MaskableGraphic + OnPopulateMesh | `MaskableGraphic` 상속 + `OnPopulateMesh`에서 버텍스 직접 조립 — 스프라이트 없이 도형/그라디언트/테두리 페이드 구현 | `#Unity전용` `#uGUI` |
| 45 | L10N 언어별 TMP 폰트 사이즈 | 언어 전환 이벤트에서 `TMP_Text.fontSize`를 언어별 값으로 교체 — `ApplyFontSize(koSize, enSize)`. 0이면 기본값 유지 | `#Unity전용` `#TMP` |
| 46 | RectMask2D | 2D 사각형 클리핑 마스크 — `Mask`(스텐실 버퍼 2 드로우콜 추가) 대신 RectTransform 경계로 자식 콘텐츠 클리핑. 드로우콜 추가 없음. 원형·커스텀 shape 불가, 축 정렬 직사각형만. `MaskableGraphic` 하위 컴포넌트에 자동 반응 (#44 참조) | `#Unity전용` `#uGUI` |
| 47 | LayoutElement | LayoutGroup 내 개별 요소 크기 강제 — `minWidth/Height`(최소 보장), `preferredWidth/Height`(여유 있으면 우선), `flexibleWidth/Height`(비율 분배). `ignoreLayout=true`로 레이아웃 제외. `preferredHeight` 0↔목표값 코루틴 보간이 아코디언 애니메이션의 핵심 API | `#Unity전용` `#uGUI` |

### 오디오
| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 14 | AudioMixer + AudioMixerGroup + Exposed Parameter | 볼륨/이펙트 그룹 라우팅 + 외부 노출 파라미터 | `#Unity전용` |
| 15 | AudioSource / AudioClip / PlayOneShot | 사운드 재생 기본 API | `#Unity전용` `#필수` |

### 렌더링
| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 16 | URP (Universal Render Pipeline) | 모바일 친화 렌더 파이프라인 | `#Unity전용` `#URP` |
| 17 | Shader Graph | 노드 기반 셰이더 작성 | `#Unity전용` `#ShaderGraph` |
| 18 | Camera + RenderTexture | 보조 카메라로 텍스처에 렌더 (미니맵/포털/다중 화면) | `#Unity전용` |

### 물리 (2D)
| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 19 | `Physics2D.OverlapPoint` | 점 좌표가 어느 2D 콜라이더와 겹치는지 판정 | `#Unity전용` `#Physics2D` |
| 20 | com.unity.feature.2d 모듈 | 2D 전용 패키지 번들 (Sprite/Tilemap/Physics2D) | `#Unity전용` `#2DFeature` |
| 37 | Physics2D Layer Collision Matrix | Project Settings → Physics 2D에서 레이어 쌍별 충돌 활성/비활성 매트릭스 — 스크립트 if 분기 제거 | `#Unity전용` `#Physics2D` |
| 38 | `Physics2D.RaycastNonAlloc` / `OverlapXxxNonAlloc` | 사전 할당 버퍼를 재사용해 결과 수신 — heap alloc 0 (센서/감지 hot path) | `#Unity전용` `#Physics2D` |

### 입력
| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 39 | Input System (New) + InputAction | `.inputactions` 에셋에 키 바인딩 정의 → 콜백/PlayerInput으로 입력 수신. Command 패턴과 결합해 입력→액션 매핑 분리 | `#Unity전용` |

### 애니메이션
| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 40 | Animator Layer + Avatar Mask | Layer를 인덱스 별로 쌓고 Avatar Mask로 본 영역(상체/하체) 제한 — "이동 중 공격" 같은 합성 동작. 인덱스 ↑가 우선, Override/Additive 블렌딩 | `#Unity전용` |

### 데이터 / 영속화 / 콘텐츠 파이프라인

> 콘텐츠 파이프라인 (에셋 임포트, 아틀라스, 빌드 사이즈, 데이터 주도 설계) 항목을 본 섹션에 누적. 별도 노트 분리는 항목 10개 도달 시 검토.

| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 21 | PlayerPrefs | 키-값 영속 저장 (int/float/string 한정, 플랫폼별 저장 위치 자동) | `#Unity전용` |
| 22 | `Resources.Load<T>` (TextAsset / SO / AudioMixer) | Resources 폴더 자산을 런타임 경로 기반 로드 | `#Unity전용` |
| 23 | TextAsset + 커스텀 JSON Regex 파싱 | 텍스트 파일을 임포트 + 정규식 파싱 (JsonUtility 한계 회피) | `#Unity전용` |
| 42 | `[SerializeReference]` + 커스텀 `SubclassSelector` PropertyDrawer | abstract/interface 필드를 SO 인라인으로 직렬화 + 인스펙터 드롭다운으로 자식 타입 선택. `[Serializable]` 부모 + 자식 N종, `[SerializeReference, SubclassSelector] public TParent field;`로 선언. struct→reference 마이그레이션은 `FormerlySerializedAs` 미지원 → 1회 마이그레이션 메뉴 필수(legacy 필드 임시 보존하는 2단계 묶음 + 검증 후 삭제). 폴리모피즘 인스턴스 1개로 데이터+동작 응집 (Strategy 패턴의 SO 친화 단순화). 자식이 시너지 enum 등 외부 도메인을 모르고 의존 필드명만 알게 해 결합점 좁힘 | `#Unity전용` `#데이터` `#직렬화` |
| 43 | `AnimatorOverrideController` 런타임 clip 스왑 + 즉시 평가 + 풀 결합 | base controller 1개에 `placeholder_*` key state를 두고 런타임에 `aoc[key] = data.clip` override로 N개 변형 재생 (적별 모션, 무기별 이펙트 등). `animator.Play(state, 0, 0f)` 직후 `animator.Update(0f)` 호출로 첫 프레임 즉시 평가 — 풀에서 꺼낸 인스턴스가 직전 클립 잔상을 1프레임 노출하는 깜빡임 차단(짧은 클립 4~6프레임에서 두드러짐). 풀+큐 패턴과 결합 시 `animator.enabled = (data.clip != null)` toggle로 Animator/Curve 두 재생 경로 공존. AOC는 Native Object라 GC 대상 아님 → `OnDisable`/`OnDestroy`에서 `Destroy(aoc); aoc = null` 명시 정리 필수 | `#Unity전용` `#Animator` |

### 에디터

> 콘텐츠 파이프라인 보조 도구 — 에디터 메뉴/툴/빌드 자동화 항목을 본 섹션에 누적.

| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 24 | `[MenuItem]` + EditorUtility / AssetDatabase | 에디터 메뉴 추가 + 에셋 조작 API | `#Unity전용` `#에디터` |
| 25 | `#if UNITY_EDITOR` 조건부 컴파일 | 에디터 전용 코드 분리 (빌드에서 제외) | `#Unity전용` `#에디터` |
| 26 | PrefabBuilders 패턴 | 에디터 스크립트로 `.prefab` 생성 (런타임 Instantiate/YAML 직접 작성 회피) | `#Unity전용` `#에디터` |

### 수학 / 시간 / Misc
| # | 기능 | 한 줄 요약 | 종속성 |
|---|------|----------|--------|
| 27 | Mathf (Clamp01, Log10, Lerp, Vector2/3) | 수학 빌트인 래퍼 (개념 본체는 [[math-algorithm-notes]]) | `#Unity전용` |
| 28 | `Time.deltaTime` / `timeScale` / `unscaledDeltaTime` | 프레임 시간 + 게임 속도 조절 + UI 일시정지 우회 | `#Unity전용` `#필수` |
| 29 | Color 유틸 | RGB/HSV 변환, 색상 lerp, 알파 조작 | `#Unity전용` |
| 30 | `Debug.Log` / `LogError` / `LogWarning` | 콘솔 로깅 (개발 필수, 빌드에선 일부 stripped) | `#Unity전용` `#필수` |
| 33 | `WaitForSecondsRealtime` | `Time.timeScale` 무관 대기 — 일시정지 중에도 동작 필요한 코루틴 (설정/툴팁/Hold-to-Repeat) | `#Unity전용` |
| 35 | `AnimationCurve` | Inspector에서 곡선을 시각적으로 정의하는 직렬화 타입. `Evaluate(t)`로 보간값 조회 (HP 스케일링, 이징, 밸런스 곡선) | `#Unity전용` |
| 36 | CanvasGroup 기반 UI Pool | `SetActive` 대신 `CanvasGroup.alpha=0 + blocksRaycasts=false`로 풀 인스턴스 hidden 처리 — OnEnable/OnDisable 발화 없이 렌더링만 차단, 풀 복귀 시 parent 재배치 후 재사용 | `#Unity전용` `#uGUI` `#Pool` |

---

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
- **SerializeReference와 조합** — SO 안의 필드에 `[SerializeReference]`를 쓰면 폴리모픽 자식 타입 인라인 직렬화 가능 (#42 참고). 단, deep clone 요구사항이 생김


`#코어` `#데이터` `#필수`
> 관련: [[unity-feature-notes]] #4 SerializeField/Serializable, #42 SerializeReference, #22 Resources.Load | 종속성: `#Unity전용` `#필수`
## 사용 안 한 Unity 기능 (참고)

- **Animation Clip / Animator (CasualStrategy 범위)** — 트윈 유틸로 대체. Animator Layer + Avatar Mask 자체는 #40으로 등재 (복수 프로젝트)
- **Cinemachine** — 카메라 단순
- **Physics 3D** — 2D 전용
- **Addressables (CasualStrategy 범위)** — Resources.Load만 사용. Addressables + Pool 조합은 design-pattern #22 Streaming Pattern으로 등재 (복수 프로젝트)
- **DOTS / ECS** — N/A
- **UI Toolkit (VisualElement)** — uGUI 전용
- **Networking** — 싱글플레이어
- **Unity Localization Package** — 자체 JSON 시스템 사용

---

---

# 풀노트

## 18. Camera + RenderTexture (월드 카메라를 UI에 투영)

_보조 카메라가 `RenderTexture` 에셋에 렌더하고, UI의 `RawImage.texture`로 그 RT를 출력해 월드 공간을 UI 영역에 임베드하는 패턴. 미니맵/포털/캐릭터 프리뷰/장면 내 화면 등에 사용._

**설명**
메인 카메라와 별도로 동작하는 카메라를 만들고, 그 카메라의 `targetTexture`에 `RenderTexture` 에셋을 할당하면 화면 대신 RT에 렌더된다. UI 쪽에서는 `RawImage`(또는 `Image` + RenderTexture 호환 머티리얼)가 그 RT를 텍스처로 표시한다.

이 패턴의 핵심 가치는 두 가지:
- **레이아웃 분리** — 월드 카메라는 정확한 월드 좌표를 보고, UI는 자유롭게 RectTransform/Canvas 시스템에 배치. 카메라 줌/팬을 UI 변환에 끼지 않고 별도 처리 가능
- **입력 좌표 변환의 명확화** — RawImage 영역 내 마우스 좌표 → UV → 보조 카메라 viewport → 월드 좌표 → 2D Physics 라는 체인이 정형화됨

대표 응용:
- 맵/미니맵 (CasualStrategy의 MapManager + MapNodeHoverDetector)
- 캐릭터 프리뷰 (장비 변경 UI에서 회전하는 모델)
- 포털/CCTV (게임 안의 다른 장소 실시간 표시)
- 다중 분할 화면 (협동 게임의 player 1/2 viewport)

**구현 — 셋업 (Inspector)**
1. `Assets/Art/RenderTextures/MapRenderTexture.renderTexture` 생성 — Size는 UI 표시 영역과 동일/배수, Format은 보통 `Default (Auto-HDR off)`
2. 보조 카메라 GameObject 추가 — `Camera.targetTexture`에 위 RT 할당, `Culling Mask`를 표시 대상 레이어만 (Default 제외하면 메인 씬과 격리)
3. UI Canvas 안에 `RawImage` 추가 — `texture` 필드에 같은 RT 할당
4. 보조 카메라 GameObject layer를 표시 대상 노드들과 동일하게 (CasualStrategy: `mapLayer`)

**구현 — 마우스 입력 → 월드 좌표 (CasualStrategy MapNodeHoverDetector)**
```csharp
// 1) 스크린 → RawImage 로컬
RectTransformUtility.ScreenPointToLocalPointInRectangle(
    rectTransform, eventData.position, eventData.pressEventCamera, out var localPoint);

// 2) 로컬 → UV (0~1)
Rect rect = rectTransform.rect;
float u = (localPoint.x - rect.x) / rect.width;
float v = (localPoint.y - rect.y) / rect.height;
if (u < 0f || u > 1f || v < 0f || v > 1f) return;  // 영역 밖

// 3) UV → 보조 카메라 월드 좌표
Vector3 worldPoint = mapCamera.ViewportToWorldPoint(new Vector3(u, v, 0f));

// 4) 월드 좌표 → 2D Physics 판정
var hit = Physics2D.OverlapPoint(worldPoint);
if (hit != null) { /* hit.GetComponent<MapNodeIdentifier>() ... */ }
```

**구현 — 월드 좌표 → RawImage 내 스크린 좌표 (툴팁 anchor)**
```csharp
// 노드의 월드 좌표 → 카메라 viewport (0~1)
Vector3 viewport = mapCamera.WorldToViewportPoint(node.position);

// viewport → RawImage 로컬 좌표
float localX = rect.x + viewport.x * rect.width;
float localY = rect.y + viewport.y * rect.height;

// 로컬 → 스크린
Vector2 screenPos = rectTransform.TransformPoint(new Vector2(localX, localY));
```

**구현 — UV 델타로 카메라 팬 (드래그 이동)**
```csharp
// 드래그 시작 UV 저장 → 매 OnDrag에서 새 UV와 델타 계산
Vector2 deltaUv = currentUv - lastUv;

// 카메라 orthographic 크기로 월드 델타 환산
float worldHeight = mapCamera.orthographicSize * 2f;
float worldWidth = worldHeight * mapCamera.aspect;
Vector3 worldDelta = new Vector3(deltaUv.x * worldWidth, deltaUv.y * worldHeight, 0f);

mapCamera.transform.position -= worldDelta;  // 드래그 방향과 반대로 카메라 이동
```

⚠ **Unity 함정**
- **RT 해상도와 UI aspect 일치 필수** — RT 크기와 RawImage 표시 영역의 가로:세로 비가 다르면 늘어남/잘림 발생. 표시 영역이 가변이면 RT를 `dynamicResolution` 또는 코드로 `width/height` 재할당. 단, RT 재할당은 GPU 메모리 재바인딩이라 매 프레임 금지
- **카메라 Culling Mask 격리** — 메인 카메라와 보조 카메라가 같은 레이어를 그리면 메인에도 노드가 표시됨. 보조 카메라가 그릴 GameObject는 전용 layer로 분리 (CasualStrategy: 노드들을 `mapLayer`에 두고 보조 카메라 mask를 `mapLayer`만)
- **입력은 RawImage가 받지 보조 카메라가 받지 않음** — 보조 카메라의 `Camera.eventMask`나 PhysicsRaycaster는 발화 안 됨 (UI canvas가 입력을 가로챔). 따라서 hover/click 감지는 RawImage 위에 `IPointerHandler` 컴포넌트를 두고 위 4단계 변환 체인을 직접 구현
- **eventData.pressEventCamera = null 함정** — Canvas RenderMode가 ScreenSpaceOverlay면 `pressEventCamera`가 null. `ScreenPointToLocalPointInRectangle`은 null을 허용하지만, ScreenSpaceCamera/WorldSpace이면 반드시 Canvas의 `worldCamera` 전달
- **UV 경계 검사 빠뜨림** — `localPoint`가 rect 밖이어도 변환은 동작하므로 `0 <= u,v <= 1` 명시 검사 필요. 안 그러면 RawImage 밖 마우스도 hover로 인식
- **2D 카메라는 orthographic** — `ViewportToWorldPoint`에 z 인자가 들어가지만 orthographic이면 사실상 무시. perspective 카메라면 z(near plane으로부터의 거리)가 결과에 큰 영향
- **RT 메모리 비용** — `1024×1024 ARGB32 = 4MB`. 모바일에서 다중 RT 사용 시 누적 메모리 + 매 프레임 추가 draw call(보조 카메라 1대당 1패스) 고려
- **드래그 좌표 누적 함정** — `delta` 기반으로 카메라를 이동시키면 매 프레임 작은 부동소수점 오차 누적. 드래그 시작 시점의 카메라 위치와 UV를 저장해두고 매 프레임 absolute로 재계산하는 방식이 정확하지만, CasualStrategy 케이스처럼 짧은 드래그면 delta 방식도 실용 충분
- **OnPointerExit가 안 오는 경우** — 드래그 중에는 PointerExit이 발화 안 함 → hover 상태가 stuck. 드래그 시작 시 명시적으로 `ClearHover()` 호출 (CasualStrategy 패턴)


`#렌더링` `#UI` `#카메라` `#좌표변환`
> 관련: [[unity-feature-notes]] #12 Canvas RenderMode, #13 RectTransformUtility, #19 Physics2D.OverlapPoint | 종속성: `#Unity전용` `#렌더링` (uGUI 또는 UI Toolkit, 2D/3D 모두 적용 가능)

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

CasualStrategy의 PopupSpawner는 "순수 CanvasGroup-only"가 아니라 **하이브리드**다. alpha=0만으로는 TMP_Text의 SDF material 조합에 따라 흐릿하게 잔존하는 케이스가 있어 풀 인스턴스에는 SetActive(false)도 함께 적용. 이는 노트 #36의 순수 패턴에서 한 단계 진화한 형태.

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


`#UI` `#uGUI` `#Pool` `#성능` `#라이프사이클`
> 관련: [[unity-feature-notes]] #7 Canvas/CanvasGroup/RectTransform, #41 GameObject 비활성화 silent 코루틴 정지 함정 (대응책 중 하나) | 종속성: `#Unity전용` `#uGUI` (CanvasGroup은 uGUI 전용. UI Toolkit은 다른 메커니즘)

## 42. `[SerializeReference]` + 커스텀 `SubclassSelector` PropertyDrawer

_abstract/interface 필드를 ScriptableObject 인라인으로 직렬화하고 인스펙터 드롭다운으로 자식 타입 선택. `[Serializable]` 자식 클래스 + `[SerializeReference, SubclassSelector]` 필드 선언으로 폴리모픽 데이터·동작 응집._

**설명**
Unity 기본 직렬화는 *구체 타입*만 지원 — `public EffectBase field;`에서 자식 타입을 인스펙터로 바꿀 수 없다. `[SerializeReference]`는 이 제한을 풀어 *런타임 타입*이 직렬화됨.

두 가지 핵심:
1. **`[SerializeReference]`** — Unity 2019.3+. 참조 타입의 실제 런타임 타입을 직렬화. 인터페이스/abstract 필드에 자식 인스턴스 저장 가능
2. **SubclassSelector PropertyDrawer** — OSS 에디터 확장. `[SerializeReference]` 필드에 인스펙터 드롭다운 제공

Strategy 패턴의 SO 친화 단순화:
- 기존: SO마다 `EffectType` enum + switch dispatch + 각 case에 필드
- SerializeReference: SO에 `[SerializeReference] IEffect effect;` 1필드, 자식 타입을 인스펙터에서 선택

**구현**
```csharp
// 부모 (abstract + Serializable)
[Serializable]
public abstract class SynergyEffect
{
    public abstract void Apply(BattleContext ctx);
}

// 자식들
[Serializable]
public class DamageBoostEffect : SynergyEffect
{
    [SerializeField] private float multiplier;
    public override void Apply(BattleContext ctx) { /* ... */ }
}

[Serializable]
public class HealEffect : SynergyEffect
{
    [SerializeField] private int amount;
    public override void Apply(BattleContext ctx) { /* ... */ }
}

// SO에서 사용
[CreateAssetMenu(menuName = "CasualStrategy/SynergyRule")]
public class SynergyRuleSO : ScriptableObject
{
    [SerializeReference, SubclassSelector]
    public SynergyEffect Effect;   // 인스펙터에서 자식 타입 드롭다운 선택
}

// 런타임 적용
synergyRule.Effect.Apply(battleContext);
```

struct→reference 마이그레이션 (`FormerlySerializedAs` 미지원):
```csharp
// 1단계: 레거시 필드 임시 보존
[SerializeField] private string legacyTypeName;   // 기존 직렬화 데이터
[SerializeReference, SubclassSelector]
public SynergyEffect Effect;                       // 새 필드

// 에디터 메뉴로 마이그레이션 실행
[MenuItem("Tools/MigrateSynergyEffects")]
static void Migrate() { /* legacyTypeName → Effect 인스턴스 생성 후 저장 */ }

// 2단계: 검증 후 legacyTypeName 제거 (별도 커밋)
```

⚠ **Unity 함정**
- **Deep Clone 필수** — 다른 SO가 같은 `[SerializeReference]` 인스턴스를 공유할 수 있음. SO 복사 시 `Instantiate(so)` 또는 직렬화 deep copy. 공유 인스턴스를 수정하면 다른 SO에도 silent 전파
- **struct는 지원 안 됨** — `[SerializeReference]`는 class만 지원. struct를 class로 변환하면 `FormerlySerializedAs` 마이그레이션 불가 → 수동 마이그레이션 메뉴 필수
- **SubclassSelector 구현 방식** — OSS(`com.mackysoft.serializereference-extensions` 등) 또는 직접 구현 모두 가능. Unity 기본 내장 아님. 직접 구현 핵심: `TypeCache.GetTypesDerivedFrom<T>()`로 서브클래스 수집 → `EditorGUI.DropdownButton` + `GenericMenu`로 드롭다운 → `Activator.CreateInstance(selectedType)` 인스턴스 생성 후 `property.managedReferenceValue`에 할당 (~100줄)
- **자식이 외부 도메인을 모르게** — `DamageBoostEffect`는 `SynergyType` enum 몰라도 됨. `BattleContext.ApplyDamageMultiplier(float)` 메서드명만 알게 설계. enum 의존 시 새 효과 추가마다 enum 수정 필요 → 결합 폭발
- **인스펙터 타입 변경 시 기존 값 소실** — 드롭다운에서 타입 변경 시 기존 직렬화 값이 사라짐. 중요 데이터는 변경 전 별도 백업


`#데이터` `#직렬화` `#에디터`
> 관련: [[unity-feature-notes]] #2 ScriptableObject, #4 SerializeField/Serializable | 종속성: `#Unity전용` `#데이터` `#직렬화` (Unity 2019.3+, SubclassSelector 외부 라이브러리)

## 43. `AnimatorOverrideController` 런타임 clip 스왑 + 즉시 평가 + 풀 결합

_Base Animator Controller의 placeholder 스테이트를 런타임에 `aoc[key] = data.clip`으로 교체해 N개 클립 변형 재생. `animator.Update(0f)` 즉시 평가로 풀 재사용 시 첫 프레임 깜빡임 차단. AOC는 Native Object → `Destroy(aoc)` 필수._

**설명**
"캐릭터별/무기별 다른 모션" 구현 방법 비교:
1. **여러 Animator Controller** — N개 캐릭터에 N개 컨트롤러. 상태 그래프 중복 관리
2. **Blend Tree** — 클립 블렌딩 목적. 완전히 다른 클립 교체에 부적합
3. **AnimatorOverrideController (AOC)** — Base Controller 1개 + 런타임 클립 교체. 상태 그래프는 공유, 재생 클립만 교체

AOC 방식 가치:
- 상태 전환 로직(idle→attack→idle)은 Base Controller에서 한 번 설계
- 캐릭터 A, B, C는 같은 상태 그래프, 각자 클립만 다름
- 런타임에 `aoc["placeholder_attack"] = characterData.attackClip`으로 스왑

**구현**
```csharp
public class EnemyViewController : MonoBehaviour
{
    [SerializeField] private Animator animator;
    [SerializeField] private RuntimeAnimatorController baseController;

    private AnimatorOverrideController _aoc;

    public void Initialize(EnemyPresetSO preset)
    {
        // 기존 AOC 정리 (풀 재사용 시 재호출 대비)
        if (_aoc != null) { Destroy(_aoc); _aoc = null; }

        _aoc = new AnimatorOverrideController(baseController);
        animator.runtimeAnimatorController = _aoc;

        _aoc["placeholder_idle"]   = preset.idleClip;
        _aoc["placeholder_attack"] = preset.attackClip;
        _aoc["placeholder_die"]    = preset.dieClip;

        // 즉시 평가 — 풀 인스턴스 직전 클립 잔상 차단
        animator.Play("Idle", 0, 0f);
        animator.Update(0f);
    }

    // clip이 없으면 Animator 비활성화 (DOTween curve 등 대체 경로 사용)
    public void SetClipEnabled(bool hasClip) => animator.enabled = hasClip;

    private void OnDisable()
    {
        // AOC는 Native Object — GC 대상 아님, 명시 정리 필수
        if (_aoc != null) { Destroy(_aoc); _aoc = null; }
    }
}
```

⚠ **Unity 함정**
- **`animator.Update(0f)` 즉시 평가** — `animator.Play` 호출 후 실제 적용은 다음 프레임. 풀에서 꺼낸 인스턴스는 직전 클립 마지막 포즈가 1프레임 노출됨 (4~6프레임 짧은 클립에서 두드러짐). `Play` 직후 `animator.Update(0f)`로 현재 프레임에 즉시 강제 평가
- **AOC는 Native Object** — `new AnimatorOverrideController(...)`는 Unity 네이티브 메모리에 할당. C# GC가 수거하지 않아 계속 만들고 버리면 네이티브 메모리 누수. `OnDisable`/`OnDestroy`에서 `Destroy(_aoc); _aoc = null;` 필수
- **`Initialize` 재호출 시 기존 AOC 정리** — 풀 재사용으로 여러 번 불리면 기존 `_aoc`를 `Destroy` 후 새 AOC 생성. `if (_aoc != null) Destroy(_aoc)` 선행 필수
- **placeholder 명명 규칙** — AOC 키는 Base Controller 내 AnimationClip 이름과 동일해야 함. 이름 불일치 시 `aoc["placeholder_attack"]` 할당이 silent fail. const 또는 enum으로 관리
- **`animator.enabled = (clip != null)` toggle** — 일부 슬롯은 Animator 대신 DOTween/Curve 경로로 재생. 클립 없으면 `animator.enabled = false`로 Animator Update 비용 차단. 풀에서 꺼낼 때 다시 `enabled = true` 필요


`#애니메이션` `#코어` `#Pool`
> 관련: [[unity-feature-notes]] #40 Animator Layer + Avatar Mask, #36 CanvasGroup 기반 UI Pool (풀 패턴) | 종속성: `#Unity전용` `#Animator`

## 44. Custom MaskableGraphic + OnPopulateMesh (커스텀 UI 그래픽)

_`MaskableGraphic`을 상속해 `OnPopulateMesh`에서 버텍스를 직접 조립. Image/RawImage 이외의 UI 그래픽을 스프라이트 없이 코드로 구현._

**설명**
Unity uGUI의 모든 시각 요소는 `Graphic`의 서브클래스다. `Image`와 `RawImage`가 대표적이지만, `MaskableGraphic`을 직접 상속하면 버텍스와 컬러를 코드로 자유롭게 조립할 수 있다.

핵심 진입점: `protected override void OnPopulateMesh(VertexHelper vh)`
- 캔버스가 dirty될 때 호출. 외부에서 재빌드 트리거는 `SetVerticesDirty()` 명시 필요
- `vh.Clear()` 후 `vh.AddVert` / `vh.AddTriangle`로 메시 조립
- `UIVertex.simpleVert`를 베이스로 position + color 지정
- Inspector의 `color` 필드 = 기본 색 (`graphic.color`)
- `raycastTarget = false` 기본값 권장 — 오버레이 전용이면 입력 방해 없음

대표 응용:
- **테두리 페이드** — 외곽 불투명 + 내부 투명 (VignetteGraphic)
- **원형/다각형** — 삼각형 부채꼴 조합
- **그라디언트 바** — 왼쪽/오른쪽 버텍스에 다른 색

**구현 — VignetteGraphic (테두리 페이드, CasualStrategy)**

버텍스 레이아웃:
```
outer(0)─────────────────outer(1)
  │   inner(2)─────inner(3)   │
  │      │   (투명)    │      │
  │   inner(4)─────inner(5)   │
outer(6)─────────────────outer(7)
```

```csharp
public class VignetteGraphic : MaskableGraphic
{
    [SerializeField] private float borderThickness = 30f;

    protected override void Reset()
    {
        base.Reset();
        raycastTarget = false;
    }

    protected override void OnPopulateMesh(VertexHelper vh)
    {
        vh.Clear();
        var r = GetPixelAdjustedRect();
        float b = Mathf.Min(borderThickness, r.width * 0.5f, r.height * 0.5f);

        var outer = color;
        var inner = new Color(outer.r, outer.g, outer.b, 0f);

        float x0 = r.xMin, x1 = r.xMin + b, x2 = r.xMax - b, x3 = r.xMax;
        float y0 = r.yMin, y1 = r.yMin + b, y2 = r.yMax - b, y3 = r.yMax;

        AddVert(vh, x0, y3, outer); // 0 TL outer
        AddVert(vh, x3, y3, outer); // 1 TR outer
        AddVert(vh, x1, y2, inner); // 2 TL inner
        AddVert(vh, x2, y2, inner); // 3 TR inner
        AddVert(vh, x1, y1, inner); // 4 BL inner
        AddVert(vh, x2, y1, inner); // 5 BR inner
        AddVert(vh, x0, y0, outer); // 6 BL outer
        AddVert(vh, x3, y0, outer); // 7 BR outer

        vh.AddTriangle(0, 1, 3); vh.AddTriangle(0, 3, 2); // top
        vh.AddTriangle(1, 7, 5); vh.AddTriangle(1, 5, 3); // right
        vh.AddTriangle(7, 6, 4); vh.AddTriangle(7, 4, 5); // bottom
        vh.AddTriangle(6, 0, 2); vh.AddTriangle(6, 2, 4); // left
    }

    private static void AddVert(VertexHelper vh, float x, float y, Color c)
    {
        var v = UIVertex.simpleVert;
        v.position = new Vector3(x, y);
        v.color = c;
        vh.AddVert(v);
    }

#if UNITY_EDITOR
    protected override void OnValidate()
    {
        base.OnValidate();
        SetVerticesDirty();
    }
#endif
}
```

⚠ **Unity 함정**
- **`SetVerticesDirty()` 명시 필요** — `SerializeField` 값이 Inspector에서 변경돼도 자동 재빌드 안 됨. `OnValidate`에서 호출해야 에디터 실시간 반영
- **`GetPixelAdjustedRect()`** — `rectTransform.rect` 대신 사용. Canvas pixel snapping을 반영해 0.5px 어긋남 방지
- **borderThickness 클램프 필수** — 두께가 rect의 절반 이상이면 내부가 음수 공간이 됨. `Mathf.Min(b, width*0.5f, height*0.5f)` 가드 필요
- **트라이앵글 인덱스 순서 (CW)** — Unity는 시계 방향(clockwise)이 front-face. 반대로 연결하면 렌더되지 않음
- **Mask 자동 지원** — `MaskableGraphic` 상속 시 Canvas Mask / RectMask2D에 자동 반응 (별도 구현 불필요)
- **`color` 기준** — 내부 버텍스 색을 파생할 때 `graphic.color` 기준으로 계산해야 CanvasGroup alpha 등이 정상 반영됨


`#UI` `#uGUI` `#렌더링`
> 관련: [[unity-feature-notes]] #7 Canvas/CanvasGroup/RectTransform, #32 ICanvasRaycastFilter | 종속성: `#Unity전용` `#uGUI`