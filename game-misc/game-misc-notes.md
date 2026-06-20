# 게임 기타 노트

> 상위 노트: [[Dev Notes README]]
> 다루는 축: 단편 트릭/가드/캐시 — 디자인 패턴이라기엔 작고, Unity API라기엔 응용된 구현 단편
> 다루지 않는 축: 일반화된 패턴(→ design-pattern-notes), 게임 *기능*별 기법(→ game-technique-notes)
> 적용 범위: 다수 항목이 게임엔진/Unity 종속, 일부 언어 독립
> 관련 노트: design-pattern-notes (승격 후보), unity-feature-notes (API 자체)
> 평생 노트 정책: 인덱스 표는 portable, 풀노트는 구현 의사코드 포함
> 승격 임계치: 동일 트릭이 3프로젝트 이상 반복 시 design-pattern으로 승격
> 풀노트 작성 기준: 인덱스 1줄만으로 구현/적용이 불충분한 항목. 자명한 항목만 인덱스로 종료
> 작성 시작: 2026-05-15

---

**서브 노트:**
- [[game-misc-ui-rendering|게임 잡기술 — UI·렌더링]] — UI 연출·렌더링 트릭·입력 최적화
- [[game-misc-architecture-data|게임 잡기술 — 아키텍처·데이터]] — 아키텍처 패턴·데이터 관리·성능 최적화


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
| 13 | LayoutElement Accordion | `#UI` `#트릭` | `LayoutElement.preferredHeight` 0↔목표값 코루틴 애니메이션 → LayoutGroup 자동 리플로우로 smooth expand/collapse | `#Unity전용` |
| 14 | Custom MaskableGraphic | `#UI` `#렌더링경계` | `MaskableGraphic` 상속 + `OnPopulateMesh` override → RectMask2D·CanvasGroup·Raycaster 자동 통합 커스텀 Canvas 그래픽 | `#Unity전용` |
| 15 | L10N 언어별 폰트 사이즈 매핑 | `#UX` `#UI` | 언어마다 폰트 사이즈 테이블 분리. CJK는 같은 pt가 라틴보다 시각적으로 커 보여 언어별 조정 필요 | `#Unity전용` |

---