# Unity 엔진 기능 노트

> 상위 노트: [[Dev Notes README]]
> 다루는 축: Unity 빌트인 API / 패키지 / 에디터 기능 카탈로그. "이 기능을 어디서 어떻게 썼더라" reference
> 다루지 않는 축: Unity 독립적 개념/패턴(→ design-pattern-notes, math-algorithm-notes)
> 적용 범위: **Unity 전용** — 본 노트는 의도적으로 엔진 종속. 다른 엔진 이주 시 대부분 폐기 대상
> 관련 노트: game-misc-notes (Unity API 응용 트릭), math-algorithm-notes (Mathf 개념 본체)
> 평생 노트 정책: 인덱스 표는 카탈로그 형식, 풀노트는 C# 실제 코드 + Unity 함정
> 승격 임계치: 카테고리당 항목 10개 이상 시 카테고리별 분리 검토
> 풀노트 작성 기준: 인덱스 1줄만으로 구현/적용이 불충분한 항목. 자명한 항목만 인덱스로 종료
> 작성 시작: 2026-05-15

---

**서브 노트:**
- [[unity-feature-core|Unity 기능 — 코어·라이프사이클]] — 라이프사이클·ScriptableObject·코루틴·SerializeField·DontDestroyOnLoad
- [[unity-feature-ui|Unity 기능 — UI 시스템]] — Canvas·Button·LayoutGroup·EventSystem·ScrollRect·TMP
- [[unity-feature-misc|Unity 기능 — 오디오·렌더링·에디터·유틸]] — 오디오·렌더링·물리·입력·애니메이션·데이터·에디터·유틸


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
| 7 | Canvas / CanvasGroup / RectTransform | UI 렌더 루트 + 페이드/인터랙션 토글 + UI 좌표계 | `#Unity전용` `#uGUI` `#필수` |
| 8 | Button / Image / TextMeshProUGUI | 기본 UI 위젯 트리오 | `#Unity전용` `#uGUI` `#TMP` |
| 9 | LayoutGroup (Horizontal/Vertical/Grid) + ContentSizeFitter | 자동 레이아웃 + 자식 크기 기반 컨테이너 | `#Unity전용` `#uGUI` |
| 10 | EventSystem + IBegin/Drag/EndDragHandler | 마우스/터치 이벤트 인터페이스 (드래그 시퀀스) | `#Unity전용` `#uGUI` |
| 11 | ScrollRect | 가변 컨텐츠 스크롤 컨테이너 | `#Unity전용` `#uGUI` |
| 12 | Canvas RenderMode (ScreenSpaceOverlay / WorldSpace) | UI 렌더 모드 (오버레이 vs 월드 공간) | `#Unity전용` `#uGUI` |
| 13 | RectTransformUtility (Screen↔Canvas 좌표 변환) | 스크린 좌표 ↔ Canvas 로컬 좌표 변환 | `#Unity전용` `#uGUI` |
| 14 | AudioMixer + AudioMixerGroup + Exposed Parameter | 볼륨/이펙트 그룹 라우팅 + 외부 노출 파라미터 | `#Unity전용` |
| 15 | AudioSource / AudioClip / PlayOneShot | 사운드 재생 기본 API | `#Unity전용` `#필수` |
| 16 | URP (Universal Render Pipeline) | 모바일 친화 렌더 파이프라인 | `#Unity전용` `#URP` |
| 17 | Shader Graph | 노드 기반 셰이더 작성 | `#Unity전용` `#ShaderGraph` |
| 18 | Camera + RenderTexture | 보조 카메라로 텍스처에 렌더 (미니맵/포털/다중 화면) | `#Unity전용` |
| 19 | `Physics2D.OverlapPoint` | 점 좌표가 어느 2D 콜라이더와 겹치는지 판정 | `#Unity전용` `#Physics2D` |
| 20 | com.unity.feature.2d 모듈 | 2D 전용 패키지 번들 (Sprite/Tilemap/Physics2D) | `#Unity전용` `항목 2DFeature` |
| 21 | PlayerPrefs | 키-값 영속 저장 (int/float/string 한정, 플랫폼별 저장 위치 자동) | `#Unity전용` |
| 22 | `Resources.Load<T>` (TextAsset / SO / AudioMixer) | Resources 폴더 자산을 런타임 경로 기반 로드 | `#Unity전용` |
| 23 | TextAsset + 커스텀 JSON Regex 파싱 | 텍스트 파일을 임포트 + 정규식 파싱 (JsonUtility 한계 회피) | `#Unity전용` |
| 24 | `[MenuItem]` + EditorUtility / AssetDatabase | 에디터 메뉴 추가 + 에셋 조작 API | `#Unity전용` `#에디터` |
| 25 | `#if UNITY_EDITOR` 조건부 컴파일 | 에디터 전용 코드 분리 (빌드에서 제외) | `#Unity전용` `#에디터` |
| 26 | PrefabBuilders 패턴 | 에디터 스크립트로 `.prefab` 생성 (런타임 Instantiate/YAML 직접 작성 회피) | `#Unity전용` `#에디터` |
| 27 | Mathf (Clamp01, Log10, Lerp, Vector2/3) | 수학 빌트인 래퍼 (개념 본체는 math-algorithm-notes) | `#Unity전용` |
| 28 | `Time.deltaTime` / `timeScale` / `unscaledDeltaTime` | 프레임 시간 + 게임 속도 조절 + UI 일시정지 우회 | `#Unity전용` `#필수` |
| 29 | Color 유틸 | RGB/HSV 변환, 색상 lerp, 알파 조작 | `#Unity전용` |
| 30 | `Debug.Log` / `LogError` / `LogWarning` | 콘솔 로깅 (개발 필수, 빌드에선 일부 stripped) | `#Unity전용` `#필수` |
| 31 | `[RequireComponent(typeof(T))]` | 동일 GameObject에 의존 컴포넌트 자동 추가 + Awake에서 GetComponent 보장 | `#Unity전용` |
| 32 | `ICanvasRaycastFilter` | UI 컴포넌트에서 raycast 통과 영역을 커스터마이징 (튜토리얼 cutout, 도넛 hole 등) | `#Unity전용` `#uGUI` |
| 33 | `WaitForSecondsRealtime` | `Time.timeScale` 무관 대기 — 일시정지 중에도 동작 필요한 코루틴 (설정/툴팁/Hold-to-Repeat) | `#Unity전용` |
| 34 | `OnValidate` | Inspector에서 SerializeField 값 변경 시 호출되는 에디터 콜백 — 배열 정규화, 값 검증, 의존 자산 동기화 | `#Unity전용` `#에디터` |
| 35 | `AnimationCurve` | Inspector에서 곡선을 시각적으로 정의하는 직렬화 타입. `Evaluate(t)`로 보간값 조회 (HP 스케일링, 이징, 밸런스 곡선) | `#Unity전용` |
| 36 | `[DefaultExecutionOrder(N)]` | 컴포넌트 Awake/Update 등의 실행 순서를 정수값으로 강제 — 매니저 초기화 순서 의존 시 사용 | `#Unity전용` |
| 36 | CanvasGroup 기반 UI Pool | `SetActive` 대신 `CanvasGroup.alpha=0 + blocksRaycasts=false`로 풀 인스턴스 hidden 처리 — OnEnable/OnDisable 발화 없이 렌더링만 차단, 풀 복귀 시 parent 재배치 후 재사용 | `#Unity전용` `#uGUI` `#Pool` |
| 37 | Physics2D Layer Collision Matrix | Project Settings → Physics 2D에서 레이어 쌍별 충돌 활성/비활성 매트릭스 — 스크립트 if 분기 제거 | `#Unity전용` `#Physics2D` |
| 38 | `Physics2D.RaycastNonAlloc` / `OverlapXxxNonAlloc` | 사전 할당 버퍼를 재사용해 결과 수신 — heap alloc 0 (센서/감지 hot path) | `#Unity전용` `#Physics2D` |
| 39 | Input System (New) + InputAction | `.inputactions` 에셋에 키 바인딩 정의 → 콜백/PlayerInput으로 입력 수신. Command 패턴과 결합해 입력→액션 매핑 분리 | `#Unity전용` |
| 40 | Animator Layer + Avatar Mask | Layer를 인덱스 별로 쌓고 Avatar Mask로 본 영역(상체/하체) 제한 — "이동 중 공격" 같은 합성 동작. 인덱스 ↑가 우선, Override/Additive 블렌딩 | `#Unity전용` |
| 41 | GameObject 비활성화 시 코루틴 silent 정지 함정 | `SetActive(false)` 시 Unity가 자식 코루틴을 예외 없이 정지 → `isRunning`/`isPlaying` 같은 진행 플래그가 reset 안 되어 다음 활성화 시 dead-lock. 대응 3중 안전망: (1) **호스트 이동** — 코루틴 호스트 GameObject를 토글되는 부모 밖으로 옮겨 silent 정지 자체를 차단(원천 해결), (2) **`try/finally`** — `StopCoroutine`/`StopAllCoroutines` 명시 정지 경로의 플래그 누락 방지(단 SetActive 경로는 finally 실행 보장 안 됨), (3) **`OnDisable` cleanup** — 다른 부모 비활성 시나리오 대비 잔여 플래그/큐 reset. 외부 정지는 `Cancel{Op}()` 래핑으로 정상 흐름과 분리 | `#Unity전용` `#코루틴` |
| 42 | `[SerializeReference]` + 커스텀 `SubclassSelector` PropertyDrawer | abstract/interface 필드를 SO 인라인으로 직렬화 + 인스펙터 드롭다운으로 자식 타입 선택. `[Serializable]` 부모 + 자식 N종, `[SerializeReference, SubclassSelector] public TParent field;`로 선언. struct→reference 마이그레이션은 `FormerlySerializedAs` 미지원 → 1회 마이그레이션 메뉴 필수(legacy 필드 임시 보존하는 2단계 묶음 + 검증 후 삭제). 폴리모피즘 인스턴스 1개로 데이터+동작 응집 (Strategy 패턴의 SO 친화 단순화). 자식이 시너지 enum 등 외부 도메인을 모르고 의존 필드명만 알게 해 결합점 좁힘 | `#Unity전용` `#데이터` `#직렬화` |
| 43 | `AnimatorOverrideController` 런타임 clip 스왑 + 즉시 평가 + 풀 결합 | base controller 1개에 `placeholder_*` key state를 두고 런타임에 `aoc[key] = data.clip` override로 N개 변형 재생 (적별 모션, 무기별 이펙트 등). `animator.Play(state, 0, 0f)` 직후 `animator.Update(0f)` 호출로 첫 프레임 즉시 평가 — 풀에서 꺼낸 인스턴스가 직전 클립 잔상을 1프레임 노출하는 깜빡임 차단(짧은 클립 4~6프레임에서 두드러짐). 풀+큐 패턴과 결합 시 `animator.enabled = (data.clip != null)` toggle로 Animator/Curve 두 재생 경로 공존. AOC는 Native Object라 GC 대상 아님 → `OnDisable`/`OnDestroy`에서 `Destroy(aoc); aoc = null` 명시 정리 필수 | `#Unity전용` `#Animator` |
| 44 | Custom MaskableGraphic + OnPopulateMesh | `MaskableGraphic` 상속 + `OnPopulateMesh`에서 버텍스 직접 조립 — 스프라이트 없이 도형/그라디언트/테두리 페이드 구현 | `#Unity전용` `#uGUI` |
| 45 | L10N 언어별 TMP 폰트 사이즈 | 언어 전환 이벤트에서 `TMP_Text.fontSize`를 언어별 값으로 교체 — `ApplyFontSize(koSize, enSize)`. 0이면 기본값 유지 | `#Unity전용` `#TMP` |
| 46 | RectMask2D | 2D 사각형 클리핑 마스크 — `Mask`(스텐실 버퍼 2 드로우콜 추가) 대신 RectTransform 경계로 자식 콘텐츠 클리핑. 드로우콜 추가 없음. 원형·커스텀 shape 불가, 축 정렬 직사각형만. `MaskableGraphic` 하위 컴포넌트에 자동 반응 (항목 44 참조) | `#Unity전용` `#uGUI` |
| 47 | LayoutElement | LayoutGroup 내 개별 요소 크기 강제 — `minWidth/Height`(최소 보장), `preferredWidth/Height`(여유 있으면 우선), `flexibleWidth/Height`(비율 분배). `ignoreLayout=true`로 레이아웃 제외. `preferredHeight` 0↔목표값 코루틴 보간이 아코디언 애니메이션의 핵심 API | `#Unity전용` `#uGUI` |

---