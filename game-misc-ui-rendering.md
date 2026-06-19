# 게임 잡기술 — UI·렌더링

> 상위 노트: [[game-misc-notes]] (전체 인덱스 디스패처)
> 다루는 축: UI 연출·렌더링 트릭·입력 최적화
> 다루지 않는 축: 게임 잡기술 — 아키텍처·데이터

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
| 2 | Tooltip Lazy Component Cache | `#캐시` `#성능` | FindAnyObjectByType을 첫 호출만 사용하고 결과 캐시 | `#Unity전용` |
| 3 | SortingOrder 레이어 상수 | `#렌더링경계` `#UI` | UI 깊이를 상수 그룹(Base/Tutorial)으로 관리 | `#Unity전용` |
| 4 | Drag-Drop Transient Visual Ghost | `#UX` `#UI` | 정적 DragContext + 임시 시각화로 드래그 시 원본 분리 | `#게임엔진일반` |
| 11 | Tutorial Raycast Cutout (`ICanvasRaycastFilter`) | `#UI` `#가드` | Rect 배열 안쪽만 raycast 통과시켜 튜토리얼에서 특정 영역만 클릭 가능 | `#Unity전용` |
| 13 | LayoutElement Accordion | `#UI` `#트릭` | `LayoutElement.preferredHeight` 0↔목표값 코루틴 애니메이션 → LayoutGroup 자동 리플로우로 smooth expand/collapse | `#Unity전용` |
| 14 | Custom MaskableGraphic | `#UI` `#렌더링경계` | `MaskableGraphic` 상속 + `OnPopulateMesh` override → RectMask2D·CanvasGroup·Raycaster 자동 통합 커스텀 Canvas 그래픽 | `#Unity전용` |
| 15 | L10N 언어별 폰트 사이즈 매핑 | `#UX` `#UI` | 언어마다 폰트 사이즈 테이블 분리. CJK는 같은 pt가 라틴보다 시각적으로 커 보여 언어별 조정 필요 | `#Unity전용` |

---

# 풀노트

## 2. Tooltip Lazy Component Cache

_`FindAnyObjectByType`을 첫 호출에만 실행하고 결과를 필드에 캐시. 이후 호출은 캐시 반환._

**코드**
```csharp
// TooltipManager (CasualStrategy)
private SynergyController cachedSynergyCtrl;

protected override void InitSingleton()
{
    mainCanvas = FindAnyObjectByType<Canvas>();
    cachedSynergyCtrl = FindAnyObjectByType<SynergyController>(); // 초기 캐시 시도
}

private SynergyController GetSynergyCtrl()
{
    if (cachedSynergyCtrl == null)
        cachedSynergyCtrl = FindAnyObjectByType<SynergyController>(); // 실패 시 재시도
    return cachedSynergyCtrl;
}
```

**언제 / 대안**
✅ 초기화 시점에 특정 씬 오브젝트 참조가 불확실할 때 (씬 로드 순서 미보장)
⚡ 대안: SerializeField Inspector 주입 — 가장 안전하지만 씬 구조 변경 시 연결 끊어짐
⚡ 대안: `??=` 연산자 (C#8+) — `cachedSynergyCtrl ??= FindAnyObjectByType<SynergyController>()`

⚠ **주의점**
- Unity 파괴된 오브젝트는 `== null` true지만 `is null` false. null 체크는 반드시 `== null`
- 씬 전환 후 오브젝트 파괴 시 캐시가 "fake null"이 되어 다음 접근에서 FindAnyObjectByType 재발화. 새 씬에 해당 타입 없으면 null 반환 반복
- 씬에 동일 타입 복수 존재 시 어느 것을 반환할지 불확정


#캐시 #성능
> 관련: unity-feature-notes FindAnyObjectByType | 종속성: `#Unity전용`

---

## 3. SortingOrder 레이어 상수

_Canvas SortingOrder 숫자를 Manager 상수로 중앙화. 레이어 간 상대 관계를 이름으로 표현._

**코드**
```csharp
// UIManager (CasualStrategy)
public const int SORT_ORDER_PLAY_VIEW  = 4;
public const int SORT_ORDER_POPUP      = 5;
public const int SORT_ORDER_BUILD_VIEW = 6;
public const int SORT_ORDER_REWARD     = 9;
public const int SORT_ORDER_OVERLAY    = 10;
public const int SORT_ORDER_SETTING    = 11;
public const int SORT_ORDER_FLOATING   = 20;  // 툴팁, 드래그 고스트
public const int SORT_ORDER_TUTORIAL   = 30;  // 항상 최상위

// 사용
UIManager.SetSortingOrder(go, UIManager.SORT_ORDER_FLOATING, addRaycaster: false);
```

**언제 / 대안**
✅ Canvas가 여러 레이어로 쌓이는 프로젝트. 팝업·오버레이·툴팁 등 깊이 충돌이 잦을 때
⚡ 대안: Inspector에서 직접 숫자 입력 — 분산되어 관계 파악 불가, 이름 없이 숫자만 남음

⚠ **주의점**
- 상수 간 간격이 1이면 중간 삽입 불가. CasualStrategy는 9, 10, 11로 촘촘 — 새 레이어 추가 시 재배치 필요. 최초 설계 시 10 단위 간격 권장
- `public const`는 컴파일 타임 인라인. 값 변경 후 참조 어셈블리 재컴파일 필수 (Unity는 대부분 자동)


#렌더링경계 #UI
> 관련: unity-feature-notes Canvas SortingOrder | 종속성: `#Unity전용`

---

## 4. Drag-Drop Transient Visual Ghost

_정적 DragContext가 드래그 상태(데이터 + 고스트 오브젝트)를 보유. 드래그 시작 시 고스트 생성, 종료 시 파괴._

**코드**
```csharp
// DragContext.cs (CasualStrategy)
public static class DragContext
{
    public static bool IsDragging { get; private set; }
    public static ItemInstance DraggedItem { get; private set; }
    public static SlotAddress Source { get; private set; }
    public static GameObject DragVisual { get; private set; }

    public static void Begin(ItemInstance item, SlotAddress source, Sprite icon, Canvas rootCanvas)
    {
        DraggedItem = item; Source = source; IsDragging = true;

        var go = new GameObject("DragVisual");
        var rt = go.AddComponent<RectTransform>();
        rt.SetParent(rootCanvas.transform, false);
        rt.sizeDelta = new Vector2(64f, 64f);
        UIManager.SetSortingOrder(go, UIManager.SORT_ORDER_FLOATING, addRaycaster: false);

        var img = go.AddComponent<Image>();
        img.sprite = icon;
        img.raycastTarget = false; // 드롭 영역 레이캐스트 차단 방지
        img.color = new Color(1f, 1f, 1f, 0.8f);
        DragVisual = go;
    }

    public static void UpdatePosition(Vector2 screenPos, Camera cam)
    {
        if (DragVisual == null) return;
        var rt = DragVisual.GetComponent<RectTransform>();
        RectTransformUtility.ScreenPointToLocalPointInRectangle(
            rt.parent as RectTransform, screenPos, cam, out var localPos);
        rt.anchoredPosition = localPos;
    }

    public static void End()
    {
        IsDragging = false; DraggedItem = null;
        if (DragVisual != null) { Object.Destroy(DragVisual); DragVisual = null; }
    }
}
```

드래그 핸들러에서:
```csharp
void IBeginDragHandler.OnBeginDrag(PointerEventData e)
{
    DragContext.Begin(item, address, icon, rootCanvas);
    originalImage.enabled = false;
}
void IDragHandler.OnDrag(PointerEventData e)
    => DragContext.UpdatePosition(e.position, e.pressEventCamera);
void IEndDragHandler.OnEndDrag(PointerEventData e)
{
    originalImage.enabled = true;
    DragContext.End();
}
```

**언제 / 대안**
✅ 인벤토리·큐 슬롯 간 아이템 드래그 앤 드롭
⚡ 대안: 원본 오브젝트 자체를 포인터와 함께 이동 — 드롭 취소 시 원위치 복구 로직 필요. 원본이 드롭 영역의 레이캐스트를 차단하는 문제 발생

⚠ **주의점**
- `img.raycastTarget = false` 필수. 고스트가 레이캐스트를 받으면 드롭 영역의 IDropHandler가 고스트에 막혀 이벤트를 받지 못함
- 예외로 드래그가 중단될 경우 `IsDragging = true`로 고착 가능. OnEndDrag 외 IPointerUpHandler에서도 End() 호출 고려


#UX #UI
> 관련: unity-feature-notes EventSystem IDragHandler | 종속성: `#게임엔진일반`

---

## 11. Tutorial Raycast Cutout (ICanvasRaycastFilter)

_전체 화면 오버레이에 `ICanvasRaycastFilter`를 붙여, 지정 Rect 안에서만 오버레이가 레이캐스트를 차단 해제 → 클릭이 아래 UI로 통과._

**코드**
```csharp
// TutorialHighlightFilter (CasualStrategy) — 오버레이 Image와 같은 오브젝트에 배치
public class TutorialHighlightFilter : MonoBehaviour, ICanvasRaycastFilter
{
    private Rect[] cutoutRects;

    public void SetCutoutRects(Rect[] screenRects) => cutoutRects = screenRects;

    // false = 이 위치에서 오버레이가 레이캐스트를 안 받음 → 클릭이 아래 요소로 통과
    public bool IsRaycastLocationValid(Vector2 sp, Camera cam)
    {
        if (cutoutRects == null || cutoutRects.Length == 0) return true;
        for (int i = 0; i < cutoutRects.Length; i++)
            if (cutoutRects[i].Contains(sp)) return false;
        return true;
    }
}
```

RT → screen rect 변환 후 세트:
```csharp
var rects = new Rect[targets.Length];
for (int i = 0; i < targets.Length; i++)
    rects[i] = GetScreenRect(targets[i]);
highlightFilter.SetCutoutRects(rects);

private Rect GetScreenRect(RectTransform rt)
{
    var corners = new Vector3[4];
    rt.GetWorldCorners(corners);
    Vector2 min = RectTransformUtility.WorldToScreenPoint(cam, corners[0]);
    Vector2 max = RectTransformUtility.WorldToScreenPoint(cam, corners[2]);
    return new Rect(min.x, min.y, max.x - min.x, max.y - min.y);
}
```

**언제 / 대안**
✅ 튜토리얼에서 특정 버튼만 클릭 가능하고 나머지 UI는 잠글 때
⚡ 대안: CanvasGroup.interactable = false를 개별 UI에 적용 — 동적 추가 UI 대응 어려움
⚡ 대안: 투명 차단 패널에 구멍 — 런타임 mesh 편집 필요

⚠ **주의점**
- 이 컴포넌트는 **오버레이 Image와 같은 오브젝트**에 붙어야 함. Image의 `raycastTarget = true`여야 EventSystem이 IsRaycastLocationValid를 호출
- 오버레이 Canvas SortingOrder가 차단 대상 UI보다 높아야 정상 차단


#UI #가드
> 관련: unity-feature-notes ICanvasRaycastFilter | 종속성: `#Unity전용`

---

## 13. LayoutElement Accordion

_Unity Layout 시스템에서 `LayoutElement.preferredHeight`를 0 ↔ 목표값으로 코루틴 애니메이션해 부드러운 expand/collapse를 구현하는 트릭._

**코드**
```csharp
// AttrGroupAccordionController (CasualStrategy)
[SerializeField] private LayoutElement layoutElement;
[SerializeField] private float expandedHeight = 120f;
[SerializeField] private float duration = 0.2f;

private Coroutine _anim;

public void SetExpanded(bool expanded)
{
    float target = expanded ? expandedHeight : 0f;
    if (_anim != null) StopCoroutine(_anim);
    _anim = StartCoroutine(Animate(target));
}

private IEnumerator Animate(float target)
{
    float start = layoutElement.preferredHeight;
    float elapsed = 0f;
    while (elapsed < duration)
    {
        elapsed += Time.deltaTime;
        layoutElement.preferredHeight = Mathf.Lerp(start, target, elapsed / duration);
        yield return null;
    }
    layoutElement.preferredHeight = target;
    _anim = null;
}
```

LayoutGroup(Vertical/Horizontal/Grid) 부모가 있으면 `preferredHeight` 변경 시 자동 리플로우.

**언제 / 대안**
✅ 접히는 카테고리 헤더, 아코디언 UI, 드롭다운 패널
⚡ 대안: `RectTransform.sizeDelta` 직접 조작 — LayoutGroup 리플로우가 트리거되지 않음. LayoutGroup 밖 단독 오브젝트에서만 유효
⚡ 대안: `gameObject.SetActive(false)` — 즉시 사라짐. 부드러운 연출 불가

⚠ **주의점**
- `preferredHeight = 0`으로 접혀도 자식 오브젝트는 살아있음(`SetActive(false)` 아님). 레이캐스트·이벤트가 그대로 발화되므로 필요 시 `CanvasGroup.blocksRaycasts = false` 병행
- `expandedHeight`를 런타임에 `LayoutUtility.GetPreferredHeight()` 또는 `RectTransform.rect.height`로 자동 계산하면 콘텐츠 길이에 따라 동적 대응 가능 (단 Start/Awake 이후 레이아웃 확정 시점에 호출)
- 코루틴이 중단되지 않으면 이전 애니메이션이 새 애니메이션과 겹침 — `StopCoroutine` 후 재시작


#UI #트릭
> 관련: unity-feature-notes LayoutGroup, LayoutElement | 종속성: `#Unity전용`

---

## 14. Custom MaskableGraphic

_`MaskableGraphic`을 상속하고 `OnPopulateMesh(VertexHelper)`만 override하면 RectMask2D·CanvasGroup alpha·GraphicRaycaster에 자동 통합되는 커스텀 Canvas 그래픽을 만들 수 있다._

**코드**
```csharp
// VignetteGraphic (CasualStrategy) — 테두리 페이드 커스텀 그래픽
[RequireComponent(typeof(CanvasRenderer))]
public class VignetteGraphic : MaskableGraphic
{
    [SerializeField] private float edgeWidth = 40f;
    [SerializeField] private Color vignetteColor = new Color(0f, 0f, 0f, 0.6f);

    protected override void OnPopulateMesh(VertexHelper vh)
    {
        vh.Clear();
        var rect = rectTransform.rect;
        Color transparent = new Color(vignetteColor.r, vignetteColor.g, vignetteColor.b, 0f);

        // 외곽(불투명) 4꼭지점 + 내부(투명) 4꼭지점으로 테두리 링 구성
        // vh.AddVert(pos, color, uv) / vh.AddTriangle(i0, i1, i2)
    }

#if UNITY_EDITOR
    protected override void OnValidate()
    {
        base.OnValidate();
        SetVerticesDirty();  // Inspector 수정 시 재렌더
    }
#endif
}
```

핵심 규칙:
- `MaskableGraphic` 상속 (not `MonoBehaviour`)
- `[RequireComponent(typeof(CanvasRenderer))]` 필수
- `OnPopulateMesh(VertexHelper vh)`에서 정점 정의, 첫 줄은 반드시 `vh.Clear()`
- 파라미터 변경 시 `SetVerticesDirty()` 호출로 재렌더 요청

**언제 / 대안**
✅ 프로그래밍 방식으로 생성해야 하는 UI 그래픽 (진행도 링, 테두리 그라디언트, 커스텀 다각형)
✅ RectMask2D 클리핑 영역 내에서 함께 잘려야 하는 커스텀 비주얼
⚡ 대안: Image + Shader — 텍스처/셰이더로 해결 가능한 경우 이쪽이 더 단순
⚡ 대안: UI Toolkit VisualElement — Unity 6+ 프로젝트에서는 대안 고려

⚠ **주의점**
- `raycastTarget = false` 권장 — 그래픽만 표시하고 이벤트는 받지 않을 때 성능 절감
- `material = null`로 두면 기본 UI 머티리얼 사용 (일반적으로 적절)
- 크기/색상 등 파라미터 변경 시 `SetVerticesDirty()` / `SetMaterialDirty()` 명시 호출 필수 (`OnValidate`, `OnRectTransformDimensionsChange` 등에서)


#UI #렌더링경계
> 관련: unity-feature-notes MaskableGraphic, CanvasRenderer | 종속성: `#Unity전용`

---

## 15. L10N 언어별 폰트 사이즈 매핑

_로컬라이제이션 시 언어마다 폰트 사이즈 테이블을 분리해서 관리. CJK(한중일)는 같은 pt가 라틴 문자보다 시각적으로 커 보여 언어별 조정이 필요._

**배경**
한글·한자·일본어는 글자당 정보 밀도가 영어보다 높아 같은 pt에서 영어보다 크게 보인다:
```
fontSize = 24 / "진행" (한글 2글자) ↔ "Progress" (영어 8글자)
→ 한글이 시각적으로 두꺼워 보임 — 버튼·레이블 공간에서 불균형 발생
```

**코드**
```csharp
// L10NFontSizeSO (CasualStrategy) — 언어별 사이즈 테이블 SO
[CreateAssetMenu]
public class L10NFontSizeSO : ScriptableObject
{
    [Serializable]
    public class Entry { public string key; public float korean; public float english; }
    public List<Entry> entries;
}

// LocalizedText — 언어 변경 시 폰트 사이즈 자동 적용
public class LocalizedText : MonoBehaviour
{
    [SerializeField] private TMP_Text label;
    [SerializeField] private string fontSizeKey;
    [SerializeField] private L10NFontSizeSO fontSizeTable;

    private void Apply(Language lang)
    {
        label.text = LocalizationManager.Get(locKey, lang);
        if (fontSizeTable == null || string.IsNullOrEmpty(fontSizeKey)) return;
        var entry = fontSizeTable.entries.FirstOrDefault(e => e.key == fontSizeKey);
        if (entry != null)
            label.fontSize = lang == Language.Korean ? entry.korean : entry.english;
    }
}
```

**언제 / 대안**
✅ CJK를 지원하고, 공간이 제한된 버튼·레이블이 있을 때
⚡ 대안: `TextMeshPro Auto Size` — 글자 수에 맞게 자동 축소. 레이아웃이 유동적이라면 더 단순
⚡ 대안: TMP Font Asset Scale Factor — 폰트 에셋 수준에서 일괄 조정. 해당 폰트 쓰는 모든 텍스트에 적용

⚠ **주의점**
- 키를 `string`으로 관리하면 오타 위험 — enum 또는 SO 직접 참조로 컴파일 타임 검증 고려
- 폰트 사이즈 외에 Line Spacing, Character Spacing도 CJK↔라틴 차이가 있을 수 있음
- TMP의 `enableAutoSizing`이 켜져 있으면 폰트 사이즈 설정이 무시됨 — 수동 사이즈 매핑과 AutoSize는 동시 사용 불가


#UX #UI
> 관련: unity-feature-notes TextMeshPro | 종속성: `#Unity전용` (구조 자체는 `#언어독립`)