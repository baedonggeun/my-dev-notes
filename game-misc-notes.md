# 게임 기타 노트

> 다루는 축: 단편 트릭/가드/캐시 — 디자인 패턴이라기엔 작고, Unity API라기엔 응용된 구현 단편
> 다루지 않는 축: 일반화된 패턴(→ [[design-pattern-notes]]), 게임 *기능*별 기법(→ [[game-technique-notes]])
> 적용 범위: 다수 항목이 게임엔진/Unity 종속, 일부 언어 독립
> 관련 노트: [[design-pattern-notes]] (승격 후보), [[unity-feature-notes]] (API 자체)
> 평생 노트 정책: 인덱스 표는 portable, 풀노트는 구현 의사코드 포함
> 승격 임계치: 동일 트릭이 3프로젝트 이상 반복 시 design-pattern으로 승격
> 풀노트 작성 기준: 인덱스 1줄만으로 구현/적용이 불충분한 항목. 자명한 항목만 인덱스로 종료
> 작성 시작: 2026-05-15

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
| 2 | Tooltip Lazy Component Cache | `#캐시` `#성능` | FindAnyObjectByType을 첫 호출만 사용하고 결과 캐시 | `#Unity전용` |
| 3 | SortingOrder 레이어 상수 | `#렌더링경계` `#UI` | UI 깊이를 상수 그룹(Base/Tutorial)으로 관리 | `#Unity전용` |
| 4 | Drag-Drop Transient Visual Ghost | `#UX` `#UI` | 정적 DragContext + 임시 시각화로 드래그 시 원본 분리 | `#게임엔진일반` |
| 5 | SO + Lazy Dictionary Cache + Resources Fallback | `#캐시` `#데이터` | SO 룩업을 첫 접근 시 dict 캐시, 없으면 Resources에서 fallback | `#Unity전용` |
| 6 | Combination Callback Transaction Batching | `#트랜잭션` `#일관성` | 호출자가 slot 변경을 한 콜백 내에서 일괄 commit | `#언어독립` |
| 7 | 수동적 View 컴포지션 | `#UI` | View는 RectTransform/Image만 노출, Controller가 모든 로직 주입 | `#게임엔진일반` |
| 8 | Service 지연 주입 | `#초기화` `#race회피` | OnInitialize에서 Manager 조회로 init race 회피 | `#게임엔진일반` |
| 9 | SO Registry + 사전 캐시 | `#캐시` `#데이터` | 시작 시 룰을 dict로 빌드해 O(1) 룰 조회 | `#Unity전용` |
| 10 | PlayerPrefs Wrapper + 변경 브로드캐스트 | `#매니저` | 영속 설정 wrapper + 변경 시 이벤트 통지 | `#Unity전용` |
| 11 | Tutorial Raycast Cutout (`ICanvasRaycastFilter`) | `#UI` `#가드` | Rect 배열 안쪽만 raycast 통과시켜 튜토리얼에서 특정 영역만 클릭 가능 | `#Unity전용` |
| 12 | `Array.Empty<T>()` GC 회피 | `#성능` `#캐시` | 빈 배열 반복 할당 대신 정적 공유 빈 배열 사용 — heap alloc 0 | `#언어독립` |

---

## 분류 메모

- **왜 여기에 들어왔는가**: 디자인 패턴이라기엔 너무 작은 트릭(EnsureInitialized 가드), Unity API라기엔 응용 트릭(Tooltip Lazy Cache, SortingOrder 레이어 상수), 기법이라기엔 일반화 어려운 구현 단편(Combination Callback Batching).
- **승격 후보**: 같은 트릭이 다른 프로젝트에서도 반복되면 → `design-pattern-notes.md`로 승격 검토.

---

---

# 풀노트

## 6. Combination Callback Transaction Batching

**한 줄 요약**
복수 슬롯/상태 변경을 `BeginBatch() → 변경들 → EndBatch()` 패턴으로 묶어 `OnChanged` 콜백을 단 1회만 발화. 중간 상태에 반응하는 race 조건 차단.

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

**주의점**
- **EndBatch 빠뜨림** — `BeginBatch`만 호출하고 `EndBatch` 누락 시 이후 단일 변경도 콜백이 영원히 발화 안 됨. `try/finally` 패턴으로 누락 차단
- **CQS 부분 위반 (의도적)** — `EndBatch`는 상태 변경(batchActive=false) + 이벤트 발화를 동시에 함. "완료 시점에 정확히 1회 통지"라는 원자성이 목적이므로 분리가 의미 없음 ([[software-principle-notes]] #29 CQS 의도된 위반 참조)
- **batch 중 예외** — 변경 중 예외가 나면 `batchActive=true` 채로 스택이 풀릴 수 있음. `try/finally` 없으면 Manager가 영구 배치 상태로 고착
- **재진입 (nested batch)** — `BeginBatch` 내부에서 또 `BeginBatch`가 불리면 두 번째 `EndBatch`가 첫 batch를 닫아버림. 재진입 가능성이 있으면 `int _batchDepth`로 교체: `++_batchDepth`, `--_batchDepth; if (_batchDepth == 0) fire`

**메타**
- 종속성: `#언어독립`
- 관련 노트: [[software-principle-notes]] #29 CQS (의도된 위반), [[design-pattern-notes]] Observer (OnChanged 패턴 기반)
- 첫 도출: CasualStrategy (2026-05-15) — RunManager OnQueueChanged 배치
- 태그: `#트랜잭션` `#일관성` `#race회피`

---

---
