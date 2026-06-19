# Unity 기능 — UI 시스템

> 상위 노트: [[unity-feature-notes]] (전체 인덱스 디스패처)
> 다루는 축: Canvas·Button·LayoutGroup·EventSystem·ScrollRect·TMP
> 다루지 않는 축: [[unity-feature-core|Unity 기능 — 코어·라이프사이클]] / [[unity-feature-misc|Unity 기능 — 오디오·렌더링·에디터·유틸]]

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
| 46 | RectMask2D | 2D 사각형 클리핑 마스크 — `Mask`(스텐실 버퍼 2 드로우콜 추가) 대신 RectTransform 경계로 자식 콘텐츠 클리핑. 드로우콜 추가 없음. 원형·커스텀 shape 불가, 축 정렬 직사각형만. `MaskableGraphic` 하위 컴포넌트에 자동 반응 (항목 44 참조) | `#Unity전용` `#uGUI` |
| 47 | LayoutElement | LayoutGroup 내 개별 요소 크기 강제 — `minWidth/Height`(최소 보장), `preferredWidth/Height`(여유 있으면 우선), `flexibleWidth/Height`(비율 분배). `ignoreLayout=true`로 레이아웃 제외. `preferredHeight` 0↔목표값 코루틴 보간이 아코디언 애니메이션의 핵심 API | `#Unity전용` `#uGUI` |

---

# 풀노트

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


#UI #uGUI #렌더링
> 관련: [[unity-feature-notes]] 항목 7 Canvas/CanvasGroup/RectTransform, 항목 32 ICanvasRaycastFilter | 종속성: `#Unity전용` `#uGUI`