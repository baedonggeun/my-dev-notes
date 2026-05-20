# Unity 엔진 기능 노트

> 다루는 축: Unity 빌트인 API / 패키지 / 에디터 기능 카탈로그. "이 기능을 어디서 어떻게 썼더라" reference
> 다루지 않는 축: Unity 독립적 개념/패턴(→ [[design-pattern-notes]], [[math-algorithm-notes]])
> 적용 범위: **Unity 전용** — 본 노트는 의도적으로 엔진 종속. 다른 엔진 이주 시 대부분 폐기 대상
> 관련 노트: [[game-misc-notes]] (Unity API 응용 트릭), [[math-algorithm-notes]] (Mathf 개념 본체)
> 평생 노트 정책: 인덱스 표는 카탈로그 형식, 풀노트는 C# 실제 코드 + Unity 함정
> 승격 임계치: 카테고리당 항목 10개 이상 시 카테고리별 분리 검토
> 풀노트 작성 기준 (둘 이상 해당 시):
>   - 함정/엣지케이스를 자주 까먹는다 (Unity 특유의 직렬화/도메인 리로드 등)
>   - 같은 API의 여러 사용 패턴이 있다
>   - 응용 사례가 3개 이상이다
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

## 인덱스

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

## 항목별 노트
*풀 4블록 노트는 요청 시 작성. 위 인덱스 표가 SOT.*

---

## 18. Camera + RenderTexture (월드 카메라를 UI에 투영)

**한 줄 요약**
보조 카메라가 `RenderTexture` 에셋에 렌더하고, UI의 `RawImage.texture`로 그 RT를 출력해 월드 공간을 UI 영역에 임베드하는 패턴. 미니맵/포털/캐릭터 프리뷰/장면 내 화면 등에 사용.

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

**주의점**
- **RT 해상도와 UI aspect 일치 필수** — RT 크기와 RawImage 표시 영역의 가로:세로 비가 다르면 늘어남/잘림 발생. 표시 영역이 가변이면 RT를 `dynamicResolution` 또는 코드로 `width/height` 재할당. 단, RT 재할당은 GPU 메모리 재바인딩이라 매 프레임 금지
- **카메라 Culling Mask 격리** — 메인 카메라와 보조 카메라가 같은 레이어를 그리면 메인에도 노드가 표시됨. 보조 카메라가 그릴 GameObject는 전용 layer로 분리 (CasualStrategy: 노드들을 `mapLayer`에 두고 보조 카메라 mask를 `mapLayer`만)
- **입력은 RawImage가 받지 보조 카메라가 받지 않음** — 보조 카메라의 `Camera.eventMask`나 PhysicsRaycaster는 발화 안 됨 (UI canvas가 입력을 가로챔). 따라서 hover/click 감지는 RawImage 위에 `IPointerHandler` 컴포넌트를 두고 위 4단계 변환 체인을 직접 구현
- **eventData.pressEventCamera = null 함정** — Canvas RenderMode가 ScreenSpaceOverlay면 `pressEventCamera`가 null. `ScreenPointToLocalPointInRectangle`은 null을 허용하지만, ScreenSpaceCamera/WorldSpace이면 반드시 Canvas의 `worldCamera` 전달
- **UV 경계 검사 빠뜨림** — `localPoint`가 rect 밖이어도 변환은 동작하므로 `0 <= u,v <= 1` 명시 검사 필요. 안 그러면 RawImage 밖 마우스도 hover로 인식
- **2D 카메라는 orthographic** — `ViewportToWorldPoint`에 z 인자가 들어가지만 orthographic이면 사실상 무시. perspective 카메라면 z(near plane으로부터의 거리)가 결과에 큰 영향
- **RT 메모리 비용** — `1024×1024 ARGB32 = 4MB`. 모바일에서 다중 RT 사용 시 누적 메모리 + 매 프레임 추가 draw call(보조 카메라 1대당 1패스) 고려
- **드래그 좌표 누적 함정** — `delta` 기반으로 카메라를 이동시키면 매 프레임 작은 부동소수점 오차 누적. 드래그 시작 시점의 카메라 위치와 UV를 저장해두고 매 프레임 absolute로 재계산하는 방식이 정확하지만, CasualStrategy 케이스처럼 짧은 드래그면 delta 방식도 실용 충분
- **OnPointerExit가 안 오는 경우** — 드래그 중에는 PointerExit이 발화 안 함 → hover 상태가 stuck. 드래그 시작 시 명시적으로 `ClearHover()` 호출 (CasualStrategy 패턴)

**메타**
- 종속성: `#Unity전용` `#렌더링` (uGUI 또는 UI Toolkit, 2D/3D 모두 적용 가능)
- 관련 노트: [[unity-feature-notes]] #12 Canvas RenderMode, #13 RectTransformUtility, #19 Physics2D.OverlapPoint
- 첫 도출: CasualStrategy (2026-05-18) — MapManager + MapNodeHoverDetector
- 적용 사례:
  - CasualStrategy: 맵 화면 (`MapRenderTexture` + 보조 `mapCamera` + `RawImage` + `MapNodeHoverDetector`)
- 태그: `#렌더링` `#UI` `#카메라` `#좌표변환`

---

## 36. CanvasGroup 기반 UI Hide / Pool

**한 줄 요약**
`SetActive(false)` 대신 `CanvasGroup.alpha=0 + blocksRaycasts=false + interactable=false` 조합으로 UI를 hidden 처리. OnEnable/OnDisable 발화 없이 렌더링/입력만 차단해 코루틴·이벤트 구독·풀 인스턴스 상태를 보존.

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

**주의점**
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

**메타**
- 종속성: `#Unity전용` `#uGUI` (CanvasGroup은 uGUI 전용. UI Toolkit은 다른 메커니즘)
- 관련 노트: [[unity-feature-notes]] #7 Canvas/CanvasGroup/RectTransform, #41 GameObject 비활성화 silent 코루틴 정지 함정 (대응책 중 하나)
- 첫 도출: CasualStrategy (2026-05-15) — 다수 UI controller/binder
- 적용 사례:
  - CasualStrategy: TabController (탭 전환), PopupSpawner (popup pool, 하이브리드), BattleLogBinder, TooltipManager, RewardPopupController, GachaController 등
- 태그: `#UI` `#uGUI` `#Pool` `#성능` `#라이프사이클`

---
