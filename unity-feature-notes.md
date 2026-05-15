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
