# Unity 기능 — 오디오·렌더링·에디터·유틸

> 상위 노트: [[unity-feature-notes]] (전체 인덱스 디스패처)
> 다루는 축: 오디오·렌더링·물리·입력·애니메이션·데이터·에디터·유틸
> 다루지 않는 축: Unity 기능 — 코어·라이프사이클 / Unity 기능 — UI 시스템

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
| 33 | `WaitForSecondsRealtime` | `Time.timeScale` 무관 대기 — 일시정지 중에도 동작 필요한 코루틴 (설정/툴팁/Hold-to-Repeat) | `#Unity전용` |
| 35 | `AnimationCurve` | Inspector에서 곡선을 시각적으로 정의하는 직렬화 타입. `Evaluate(t)`로 보간값 조회 (HP 스케일링, 이징, 밸런스 곡선) | `#Unity전용` |
| 37 | Physics2D Layer Collision Matrix | Project Settings → Physics 2D에서 레이어 쌍별 충돌 활성/비활성 매트릭스 — 스크립트 if 분기 제거 | `#Unity전용` `#Physics2D` |
| 38 | `Physics2D.RaycastNonAlloc` / `OverlapXxxNonAlloc` | 사전 할당 버퍼를 재사용해 결과 수신 — heap alloc 0 (센서/감지 hot path) | `#Unity전용` `#Physics2D` |
| 39 | Input System (New) + InputAction | `.inputactions` 에셋에 키 바인딩 정의 → 콜백/PlayerInput으로 입력 수신. Command 패턴과 결합해 입력→액션 매핑 분리 | `#Unity전용` |
| 40 | Animator Layer + Avatar Mask | Layer를 인덱스 별로 쌓고 Avatar Mask로 본 영역(상체/하체) 제한 — "이동 중 공격" 같은 합성 동작. 인덱스 ↑가 우선, Override/Additive 블렌딩 | `#Unity전용` |
| 42 | `[SerializeReference]` + 커스텀 `SubclassSelector` PropertyDrawer | abstract/interface 필드를 SO 인라인으로 직렬화 + 인스펙터 드롭다운으로 자식 타입 선택. `[Serializable]` 부모 + 자식 N종, `[SerializeReference, SubclassSelector] public TParent field;`로 선언. struct→reference 마이그레이션은 `FormerlySerializedAs` 미지원 → 1회 마이그레이션 메뉴 필수(legacy 필드 임시 보존하는 2단계 묶음 + 검증 후 삭제). 폴리모피즘 인스턴스 1개로 데이터+동작 응집 (Strategy 패턴의 SO 친화 단순화). 자식이 시너지 enum 등 외부 도메인을 모르고 의존 필드명만 알게 해 결합점 좁힘 | `#Unity전용` `#데이터` `#직렬화` |
| 43 | `AnimatorOverrideController` 런타임 clip 스왑 + 즉시 평가 + 풀 결합 | base controller 1개에 `placeholder_*` key state를 두고 런타임에 `aoc[key] = data.clip` override로 N개 변형 재생 (적별 모션, 무기별 이펙트 등). `animator.Play(state, 0, 0f)` 직후 `animator.Update(0f)` 호출로 첫 프레임 즉시 평가 — 풀에서 꺼낸 인스턴스가 직전 클립 잔상을 1프레임 노출하는 깜빡임 차단(짧은 클립 4~6프레임에서 두드러짐). 풀+큐 패턴과 결합 시 `animator.enabled = (data.clip != null)` toggle로 Animator/Curve 두 재생 경로 공존. AOC는 Native Object라 GC 대상 아님 → `OnDisable`/`OnDestroy`에서 `Destroy(aoc); aoc = null` 명시 정리 필수 | `#Unity전용` `#Animator` |

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


#렌더링 #UI #카메라 #좌표변환
> 관련: [[unity-feature-notes]] 항목 12 Canvas RenderMode, 항목 13 RectTransformUtility, 항목 19 Physics2D.OverlapPoint | 종속성: `#Unity전용` `#렌더링` (uGUI 또는 UI Toolkit, 2D/3D 모두 적용 가능)

---

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


#데이터 #직렬화 #에디터
> 관련: [[unity-feature-notes]] 항목 2 ScriptableObject, 항목 4 SerializeField/Serializable | 종속성: `#Unity전용` `#데이터` `#직렬화` (Unity 2019.3+, SubclassSelector 외부 라이브러리)

---

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


#애니메이션 #코어 #Pool
> 관련: [[unity-feature-notes]] 항목 40 Animator Layer + Avatar Mask, 항목 36 CanvasGroup 기반 UI Pool (풀 패턴) | 종속성: `#Unity전용` `#Animator`