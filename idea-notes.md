# 아이디어 노트

> 다루는 축: 미구현 아이디어 / 관찰한 기법 / 학습한 개념 — *검증 전* 인박스
> 다루지 않는 축: 검증된 패턴 (→ 기존 7개 노트 중 적합한 곳으로 승격)
> 적용 범위: 모든 영역 (장르/엔진/언어 전체)
> 관련 노트: 전 노트 (승격 시 이주 대상)
> 평생 노트 정책: 인덱스 표 = SOT, 가벼운 4블록 템플릿, 구현·검증 시 기존 노트로 승격
> 등재 트리거: **한 번 만남도 OK** (기존 노트는 "두 번 만남" 트리거, 본 노트는 인박스이므로 완화)
> 승격 트리거 (둘 이상 해당 시 기존 노트로 이주):
>   - 2개 이상 프로젝트에서 구현·검증
>   - 함정/엣지케이스가 명확히 정리됨
>   - README의 풀노트 작성 기준 충족
> 작성 시작: 2026-05-16

---

## 태그 목록

### 상태
- `#미구현` — 아이디어만 존재
- `#실험중` — 일부 구현, 검증 진행
- `#1회검증` — 1개 프로젝트에서 구현 완료 (승격 대기)
- `#승격됨→{노트}` — 기존 노트로 이주 완료 (본 노트는 strike-through로 유지)
- `#기각` — 더 나은 대안 발견 또는 비현실적 판명

### 분야
- `#시뮬레이션` `#시간시스템` `#네트워크` `#렌더링` `#AI` `#월드시스템`
- `#아키텍처` `#알고리즘` `#패턴` `#디자인원리`

### 출처
- `#자체관찰` `#논문` `#컨퍼런스` `#타게임분석` `#서적`

---

## 인덱스

| # | 아이디어명 | 분야 | 한 줄 요약 | 상태 |
|---|----------|------|----------|------|
| 1 | 결정론적 시간축 양자 예측 (달력 SOT 시뮬레이션) | `#시뮬레이션` `#시간시스템` `#아키텍처` | 시뮬레이션은 게임 내 달력 시간에만 종속 — 가속/스킵해도 동일 결과 | `#1회검증` |
| 2 | Rewind 시스템 (시간 되감기 / Replay) | `#시간시스템` `#아키텍처` `#알고리즘` | 플레이어 행동·과거 상태를 되돌리거나 재생. 동기화 표면이 커서 함정 큼 | `#미구현` |
| 3 | Sequence(연출) ↔ Data 흐름 분리 | `#아키텍처` `#패턴` `#디자인원리` | 데이터 코루틴은 수치+이벤트만, 시각 연출은 자체 Sequence가 독립 관리. 연출 OFF에도 데이터 흐름 무손상 | `#1회검증` |
| 4 | 동시 이벤트 발행이 UI 단계 표시 회귀 | `#아키텍처` `#디자인원리` `#패턴` | N개 슬롯/엔티티가 동시 코루틴으로 OnEvent N번 즉시 발행 → UI가 단계 1→2→3 보여줄 frame 없이 즉시 점프. 슬롯 순차 진행이 UX 우위 | `#1회검증` |
| 5 | 동일 카테고리 효과의 시점·대상·경로 일관성 | `#디자인원리` `#패턴` | 동일 카테고리(강화 시너지) 효과가 자기/적, 즉시/지연, 단일/이중 경로로 비대칭이면 사용자 인지 혼란. 통합 SOT + 시점·대상 통일 | `#1회검증` |
| 6 | 결과 객체에 재계산 가능 필드 추가 | `#패턴` `#아키텍처` | 이미 생성된 결과 객체(dice roll)에 reinforced/final* 필드 추가 → 원본 입력(rollValue) 유지하며 보정 델타만 더해 type 재판정. 호출 위치 변경 없이 재계산 | `#1회검증` |
| 7 | 외부 대기 카운터의 모든 발행 경로 노출 | `#아키텍처` `#패턴` `#디자인원리` | 비동기 작업이 큐/즉시/지연 등 다중 발행 경로를 가질 때, 외부 대기가 추적하는 카운터·플래그가 *모든* 경로를 노출하지 않으면 누락 경로 활성 중에도 대기가 race로 풀린다. 신규 경로 도입 시 추적 메커니즘 확장이 강제 — try/finally로 카운터 보호 | `#1회검증` |
| 8 | SerializeReference 자식 인스턴스 deep clone | `#패턴` `#아키텍처` | `Activator.CreateInstance(src.GetType())` + `JsonUtility.ToJson/FromJsonOverwrite` 라운드트립. 새 자식 추가 시 필드 복사 코드 갱신 불필요. SerializeReference 인스턴스 공유로 인한 의도치 않은 전파 방지 (Editor 마이그레이션/SO 일괄 동기화 유틸에 유용). 단, `[SerializeField]`/public 외 필드는 기본값으로 리셋되므로 데이터 전용 자식에만 안전 | `#1회검증` |
| 9 | 풀별 spawn 위치 캡슐화 (Pool-Position Encapsulation) | `#패턴` `#아키텍처` `#디자인원리` | 동적 UI(popup/floating text) 풀의 Hierarchy 위치 자체가 spawn 위치. 호출자가 `parentRT`를 인자로 안 받고 메서드 이름(`SpawnEnemyDamage`/`SpawnPlayerInstant`)이 풀(=위치) 선택. 효과: 호출 시그니처 축소 + null fallback 누더기 제거 + 디자이너가 씬에서 위치 변경(코드 0). 트레이드오프: 동적 위치 대응 불가 → 적 단일/위치 고정 게임에서 적합. 다중 대상 게임이면 부적합. 함정: 런타임에 형제 GameObject가 추가되면 풀이 first sibling으로 밀려 popup 가려짐 → 매 spawn 시 `transform.SetAsLastSibling()` 호출로 보정 | `#1회검증` |
| 10 | 단계 표식과 값 reset 책임 분리 (Mark/Reset) | `#패턴` `#아키텍처` `#디자인원리` | 다단계 흐름(단계1=표식 단계, 단계2=실제 적용 단계)에서 단계1은 *플래그만* 설정(Mark), 값 reset은 단계2가 진입 직후 mods 캐싱 후 즉시 호출(Reset). 단일 메서드가 플래그+값 reset을 합쳐 수행하면 단계2 진입 시점에 이미 값이 0이라 가산이 봉쇄되는 함정의 해법. `firstSlotPending` 등 별도 플래그로 단계2 진입 조건 표식. 함정: 단계1 내부에 `yield` 추가 시 `!flag` 체크+셋 동시 통과 race 가능 — atomic check-and-set 또는 단일 컨텍스트 보장 필요 | `#1회검증` |
| 11 | View 가 인터랙션 컴포넌트 SerializeField 소유 + Binder는 참조만 | `#패턴` `#아키텍처` `#디자인원리` | 슬롯형 UI에서 DragHandler/DropHandler/EventTrigger 같은 인터랙션 컴포넌트를 UIBinder가 런타임 `AddComponent`로 부착하면 (a) Binder가 슬롯 구성·생성 책임까지 떠안고 (b) 인스펙터에서 슬롯이 어떤 입력을 받는지 한눈에 안 보이고 (c) prefab의 인스펙터 미세 조정과 충돌. 해결: 슬롯 View(`InventorySlotView` 등)가 `[SerializeField] ItemDragHandler dragHandler` 등을 직접 소유 → prefab YAML에 정적 부착 → Binder는 `view.DragHandler.address = ...` 주입만. 트레이드오프: prefab YAML에 컴포넌트 N×3 추가 작업 필요(슬롯 16개면 48 entry). 마이그레이션 전이성: SlotView 필드 null이면 GetComponent/AddComponent 폴백 유지 → prefab 와이어 작업을 별 묶음으로 분리 가능. 적용 가능성: 인스펙터 와이어 보존 원칙을 따르는 모든 슬롯형 UI(인벤토리/큐/장비창/상점). 동적 풀 패턴(Instantiate per item)에는 부적합 (정적 슬롯형에서만 효과) | `#1회검증` |
| 12 | 중첩 prefab 컴포넌트 직접 직렬화 우회 (Transform[] + GetComponent) | `#패턴` `#아키텍처` | 부모 prefab의 `[SerializeField] ChildComponent[]` 가 *중첩 prefab 인스턴스 내부 component* 를 직접 참조하면 Unity가 stripped MonoBehaviour entry를 자동 생성하지 않아 모든 슬롯이 null로 직렬화됨. YAML 직접 편집으로 stripped MB 블록(`--- !u!114 &{id} stripped` + `m_CorrespondingSourceObject` + `m_PrefabInstance`) 수동 작성도 Unity가 인식 안 함. **우회**: 필드 타입을 `Transform[]` 또는 `GameObject[]` 로 변경 → 중첩 prefab의 stripped *RectTransform* fileID(자동 생성됨) 참조 가능 → `OnInitialize/Awake` 에서 `GetComponent<T>()` 로 캐싱. 사례: 12 SynergyType 슬롯을 SynergyUIBinder.slots에 wire 시도 → null 직렬화 → Transform[] 우회 + GetComponent 캐싱으로 해결. 적용 가능성: 정적 슬롯 UI에서 nested prefab 인스턴스의 custom component를 부모가 참조해야 할 때 (인벤토리 슬롯, 시너지 행, 보상 카드, 능력 슬롯 등). 검증: Unity MCP `mcpforunity://scene/gameobject/{id}/component/{type}` 리소스 조회로 SerializeField null 즉시 검출 가능. 트레이드오프: 한 단계 간접 (`view.SomeComponent` 대신 캐싱 배열 lookup) | `#1회검증` |
| 13 | 단일 매니저 이벤트의 N회 발화 batching (Begin/End + dirty 플래그) | `#패턴` `#아키텍처` `#디자인원리` | 단일 작업(가챠 draw 등)에서 매니저 이벤트(`OnQueueChanged`)가 여러 변경에 의해 N회 발화 → 구독자(UIBinder)가 race 회피용 상태 플래그(`suppressAutoRefresh`)를 보유하던 안티패턴 폐기. `BeginX()` / `EndX()` public 메서드 + `bool batchActive` + `bool batchDirty` 1쌍, private `NotifyX()` 헬퍼가 batch 진행 중이면 dirty만 set + 발화 보류, End에서 dirty가 누적됐으면 1회만 발화. 호출자는 try/finally로 EndX 보장(코루틴 중단/예외 안전). 효과: 구독자가 상태 추적 책임 없음(View/Binder 정의 회복), 발화 책임자가 일관된 상태 시점을 알므로 race 원천 차단. 적용 가능성: 단일 매니저가 다수 이벤트 발행 지점을 가진 모든 도메인(인벤토리/큐/상점/슬롯 시스템). 함정: 일괄 replace_all로 직접 invoke 호출을 헬퍼 위임으로 교체할 때 헬퍼 본문의 invoke까지 같이 치환되어 자기 자신 호출 무한 재귀 발생 — 헬퍼 정의는 replace 후 별도 검수 필수. 사례: `RunManager.BeginQueueBatch/EndQueueBatch` (CasualStrategy 2026-05-20) | `#1회검증` |
| 14 | 명명 규약의 sub-pattern 분기 보정 (정의 정확도 회복) | `#패턴` `#아키텍처` `#디자인원리` | 코드 감사 기준(예: F-4 "다른 Manager 호출 = DI 우회 위반")이 실제 코드 패턴보다 좁으면 정합 코드를 위반으로 오판. 해결: 단일 행 정의를 *2~3 sub-pattern* 으로 분기 — 명확 위반 / 회색 (정리 의무 없음) / 정합 화이트리스트 (예: FlowDirector 호출). 기준 자체에 회색지대 인정 명시. 효과: (a) 위반 오판 0, (b) 회귀 감사 grep 헬퍼 정확도 ↑, (c) 사용자 결정 단순화 (회색은 메모만, 위반만 sub-plan 분기). 적용 가능성: 모든 lint 룰/코드 컨벤션/책임 분리 정의. 한 번 만남 (CasualStrategy plan-suffix-discipline-audit, F-4 6행 보정 — Effect/Pool/Handler/Service/Manager/Controller). 트레이드오프: 정의가 복잡해져 처음 보는 사람이 회색 vs 위반 구분에 시간 소요. 단순 룰 사회/조직에는 부적합 (단일 binary 정의가 더 강제력 있음) | `#1회검증` |
| 15 | 부모 Manager 역참조 회색지대 (ctor 폭발 트레이드오프) | `#패턴` `#아키텍처` `#디자인원리` | Manager + Service 컴포지션 패턴에서 자식 Service가 부모 Manager.Instance 를 직접 호출하는 안티패턴 — 정합 모델은 ctor 주입이지만 부모 Manager가 자식 Service 의 *모든 의존*을 알아야 해 ctor 폭발 (Service 7개 × 각 의존 5개 = ctor 인자 35개). 해결: 외부 Manager 호출 (다른 도메인 — 명확 위반) vs 부모 Manager 역참조 (자기 컴포지션 부모 — 회색 메모) 명시 분리. 외부는 메서드 인자 주입으로 정리 가능 (단순 정리 sub-plan), 부모 역참조는 회색지대 인정 (즉시 정리 의무 없음). 효과: DI 정합 모델이 비현실적인 영역에서 트레이드오프 명시 — 모든 매니저 호출을 위반으로 분류하면 30+ 건 광범위 위반이 되어 정리 비현실적. 적용 가능성: Singleton + Service 컴포지션이 있는 모든 도메인 (RPG/시뮬레이션/대전략). 본 패턴은 #14 (sub-pattern 분기 보정)의 *구체 적용 사례*. 사례: CasualStrategy `HealthService`/`RewardService` BattleManager.Instance 역참조 10건 (2026-05-20). 트레이드오프: 회색 누적이 코드 결합도 증가의 *방치*로 이어질 위험 — 정기 감사로 회색 건수 모니터링 필요 | `#1회검증` |
| 16 | Controller 비대 분리 = 코디네이터 + 같은 GameObject 동거 sub-Controller | `#패턴` `#아키텍처` `#디자인원리` | 700+ 라인 단일 Controller가 N 책임(데이터↔UI↔버튼 풀스택) 혼재할 때 → 같은 GameObject에 N sub-Controller 컴포넌트로 동거 + 원 Controller는 코디네이터화. 자식 GameObject 추가 X → SerializeField만 prefab YAML 직접 편집으로 재분배 (Builder 재실행 없이 인스펙터 수동 조정 보존). 코디네이터 = sub 참조 + 이벤트 라우팅 + top-level UI(공통 텍스트 등). sub끼리 직접 참조 금지, 코디네이터만 라우팅 권한 (분리 의도 보존). 비교: POCO Service 분리는 비즈니스 로직만 가져가 UI 책임 잔존 → 비대 미해소. Binder + Service 분리는 *데이터↔UI↔버튼 풀스택* 단일 책임을 깰 수 없어 결합도 부정합. 적용 가능성: UI Controller가 N 섹션 혼재한 모든 도메인 (상점/인벤토리/장비창/캐릭터 시트). 한 도메인 내 책임이 서로 독립이어야 효과적 (책임 간 cross-cutting state가 강하면 코디네이터 라우팅이 비대해짐). 함정: (a) Header inspector 항목 5+개 모이면 group 정리 필요, (b) 같은 GameObject 컴포넌트가 늘어 직렬화 항목 증가 — 인스펙터 스크롤 부담, (c) `MonoBehaviour` 파생 sub 참조에 `?.` 사용 금지(G-023) — Unity overloaded `==` 우회되므로 `if (x != null) x.Method()` 명시 패턴 필수. 사례: CasualStrategy `ShopController` 700→144 라인 5 sub-Controller 분리 (`ShopItemSlotController` / `UsableShopController` / `GradeUpController` / `BenchSlotController` / `ShopDropRateView`, 2026-05-20) | `#1회검증` |
| 17 | 메타 강제 메커니즘의 3단 자가 가드 (자율 인지 + 비차단 hint + 사후 검증) | `#아키텍처` `#패턴` `#디자인원리` | "반드시 지키도록 강제"를 자동 차단 hook 없이 달성. 1차 정책 SOT를 상시 컨텍스트 노출(LLM/사람 자율 인지) → 2차 PostToolUse 같은 즉각 hint hook(위반을 systemMessage로 가시화, exit 0 비차단) → 3차 명시 호출 사후 검증(전수 점검). 강제력은 *가시화*에서 발생, 자율 차단은 보존. 트레이드오프: 1·2차 모두 비차단이라 의도적으로 무시 가능 → 3차가 backstop. 차단 hook 단독은 화이트리스트 비대화 + 회피 압력. Soft hint 단독은 1차 자가 인지 없으면 재작성 비용. 자가 인지만은 사후 검증 지연. 3단을 동시 작동시켜 어느 단도 차단하지 않으면서 매 신규 진입 시점에 위반 가시화. 적용 가능성: 명명 규약, 책임 분리 룰, 코드 컨벤션, 사내 정책 등 "차단 시 비용 크지만 위반 시 누적 비용도 큰" 메타 룰. 사례: CasualStrategy `harness/suffix-discipline` ADR (2026-05-20) — 차단 hook 폐기한 ADR-033 정합 유지하면서 4축+11종 접미사 명명 강제. 함정: 1·2차가 너무 친절하면 사람이 3차 호출을 잊음 → 3차는 PR 직전 hook 또는 정기 호출 룰로 강제하는 게 효과적 | `#1회검증` |
| 18 | enum 멤버 rename + 정수값 보존 (SerializeField/SO YAML 호환) | `#패턴` `#아키텍처` | enum이 SO YAML/세이브 파일에 정수로 직렬화되는 환경(Unity SerializeField, 직접 직렬화 시스템 일반)에서 enum 멤버 의미를 변경하려 할 때 — **이름만 rename + 정수값 보존**으로 직렬화 자산 무손상 마이그레이션 가능. 단순 사례: `SwordMasterMaxHpBonus = 14` → `SwordMasterBattleShield = 14`. SO 에셋의 `effectType: 14` YAML 값은 그대로 유지되어 12개 시너지 SO 모두 재저장 불필요. 적용 가능성: SO/세이브/네트워크 패킷에 enum이 정수 직렬화되는 모든 시스템 (RPG 능력치 효과, 카드 게임 효과, 스킬 트리). 함정: (a) enum 멤버를 *삭제*하거나 정수값을 *재배치*하면 SO YAML의 잔존 값이 다른 의미로 매핑되어 silent corruption — 폐기 멤버는 정수값을 *영구 점유*시키고 새 멤버는 다음 정수값 사용 (CasualStrategy SynergyEffectType의 "폐기 멤버 3·5~13 정수 재사용 금지" 룰), (b) Inspector dropdown의 의미는 enum 이름이므로 디자이너는 새 이름을 보지만 YAML diff는 변화 없음 — review 시 의미 변경을 놓치기 쉬움 → 커밋 메시지/ADR History에 *의미 변경* 명시 필수. 사례: CasualStrategy SynergyEffectType #14 SwordMaster MaxHp → BattleShield (2026-05-20). 트레이드오프: enum 값을 점유하는 dead 멤버가 누적되어 enum 가독성 저하 — 정기 정리 필요 vs 직렬화 호환 우선 | `#1회검증` |

*인덱스 표가 SOT, 풀노트는 위 승격 트리거 임박 시 작성.*

---

## 4블록 템플릿

```markdown
## N. 아이디어명

**한 줄 요약**
{핵심 1줄}

**출처/맥락**
{어디서 봤는가, 언제, 왜 흥미로운가}

**적용 가능성**
{어떤 장르/상황에 쓸 수 있을까}

**미해결 질문**
{구현 시 막힐 만한 지점, 검증 필요한 가정}

**메타**
- 상태: `#미구현` / `#실험중` / `#1회검증` / `#승격됨→{노트}` / `#기각`
- 분야: {태그}
- 출처: {태그}
- 등재: {날짜}
```

---

## 항목별 노트

## 1. 결정론적 시간축 양자 예측 (달력 SOT 시뮬레이션)

**한 줄 요약**
시뮬레이션 결과는 *실제 흘러간 시간(real time)*이 아니라 *게임 내 달력 시간(in-game calendar)*에만 의존하도록 설계 — 가속/슬로우/스킵해도 동일 시점 = 동일 결과.

**출처/맥락**
- 첫 도출: CasualStrategy (2026-05-16) — 본인 구현 후 일반 원리로 추출
- 비교 참조: Paradox 그랜드 스트래티지(EU4/CK3/Stellaris), Rimworld, Factorio (모두 "tick 단위 결정론" 표준 어휘 사용)
- 반례: 초창기 Paradox 게임의 고속 시뮬 desync, Dark Souls의 프레임 종속 무기 내구도 버그

**핵심 원리 3층**
업계에서 "결정론"은 세 가지 다른 층위로 분리됨:

1. **입력→출력 결정론** — 같은 입력 = 같은 출력. 리플레이·네트코드 기반. 거의 모든 게임 필요
2. **프레임레이트 독립성** — 60fps와 144fps 결과 동일. `Time.deltaTime` 곱셈의 원칙
3. **달력/시간축 SOT** ← *본 항목* — 시간 가속/스킵해도 동일 결과. 시간 조작 UI가 있는 게임만 필요

본 항목은 3번. 1·2번을 전제로 함.

**적용 가능성**

| 장르 | 필요성 | 이유 |
|---|---|---|
| 실시간 대전략 (Paradox류) | 필수 | 1x~5x 속도 조절 |
| 콜로니 심 (Rimworld, DF) | 필수 | 가속 중 인과 일관성 |
| 라이프 심 (Stardew, 동물의 숲) | 필수 | 잠자기·시간 스킵 |
| 아이들/방치형 | 필수 | 오프라인 진행 계산 |
| 자동화 (Factorio) | 필수 | UPS 독립 시뮬 |
| 오픈월드 RPG (위처3, BOTW) | 부분 | 명상/모닥불 스킵 시점만 |
| 스포츠 매니저 (FM, MyGM) | 부분 | 시즌 시뮬 모드만 |
| FPS / 격투 / 레이싱 / 리듬 / 퍼즐 | **불필요** | 가속 개념 없음 → 오버엔지니어링 |
| 턴제 (Civ류) | 불필요 | 한 턴 안에서 계산 완결 |

**미해결 질문 (다른 프로젝트 적용 시 검증 필요)**
- 결정론 시드 관리: 게임 시간 + 엔티티 ID 해시로 충분한가? 멀티 스레드 시 충돌은?
- 부동소수점 누적 오차 회피: 정수 틱 기반이 정답인가, fixed-point 산술이 정답인가?
- 가속 시 양자 예측(미래 상태 미리 계산)의 비용 vs 정확도 트레이드오프
- 멀티스레드 시뮬레이션 환경에서 결정론 유지 — 작업 순서 보장 비용
- 세이브/로드 시 시뮬레이션 상태 직렬화 — 전체 dump 아닌 incremental 가능한가?
- 양자 예측이 빗나갔을 때(플레이어 개입) 분기 처리 — rollback인가, branch-and-merge인가?

**메타**
- 상태: `#1회검증` (CasualStrategy에서 구현 검증)
- 분야: `#시뮬레이션` `#시간시스템` `#아키텍처`
- 출처: `#자체관찰`
- 등재: 2026-05-16
- 승격 후보 노트: [[design-pattern-notes]] 또는 [[game-technique-notes]] — 2개 이상 프로젝트 검증 시 결정

## 2. Rewind 시스템 (시간 되감기 / Replay)

**한 줄 요약**
플레이어 행동을 일정 시간 되돌리거나, 과거 상태를 재생하는 기능. 구현 시 *동기화 대상이 너무 많아* 함정이 큰 패턴.

**출처/맥락**
- 첫 도출: 복수 프로젝트 회상 (2026-05-15 등재 시 명시적 보류)
- README 기록: "Rewind 1건은 구현 함정(Animator/물리/AI 상태 동기화 어려움)으로 미등재 — 실제 채택 시점에 등재"
- 비교 참조: Braid, Prince of Persia: Sands of Time, Forza Horizon, SUPERHOT (역행 메커니즘), Celeste 어시스트 모드

**적용 가능성**
- 액션/플랫포머: 죽음 후 되감기, 시간 되돌리기 메커니즘 (Braid)
- 레이싱: 트랙 이탈/사고 후 되돌리기 (Forza)
- 퍼즐: 마지막 행동 취소, 시도 무한화
- 리플레이/관전: 베스트 플레이 녹화·공유

**미해결 질문 (이래서 미구현)**
- **Animator 상태**: 현재 클립 / `normalizedTime` / transition 진행도 → 매 프레임 캡처 비용 vs 정확도
- **물리 상태**: Rigidbody position/velocity/angularVelocity → 결정론 보장 어려움 (PhysX는 본래 비결정론)
- **AI 상태**: BT/FSM 노드 인덱스 + 블랙보드 변수 + 인식 큐 → 직렬화 표면이 너무 큼
- **사운드/이펙트**: 진행 중 SFX/VFX를 되감기 시점에 재배치? 단순 stop? Foley 동기 문제
- **메모리**: 60fps × 분 단위 × 다수 객체 → 압축 전략 필수 (delta encoding? keyframe interval?)
- **대안**: 차라리 [[idea-notes#1. 결정론적 시간축 양자 예측 (달력 SOT 시뮬레이션)|결정론적 시뮬레이션]]처럼 입력 + 시드만 저장하고 *재시뮬레이션*하는 rollback netcode 패턴이 나을 수 있음

**메타**
- 상태: `#미구현` (어느 프로젝트에서도 아직 구현 안 됨)
- 분야: `#시간시스템` `#아키텍처` `#알고리즘`
- 출처: `#자체관찰` (복수 프로젝트에서 후보로 등장했으나 매번 보류)
- 등재: 2026-05-16
- 승격 후보 노트: [[game-technique-notes]] — 1개 프로젝트라도 구현 검증 시

## 3. Sequence(연출) ↔ Data(데이터) 흐름 분리

**한 줄 요약**
데이터 코루틴/로직은 수치 계산과 이벤트 발행만 책임지고, 시각 연출은 별도 Sequence가 자체 코루틴/Tween으로 관리. 데이터 흐름이 시각 대기에 발목 잡히지 않도록 분리.

**출처/맥락**
- 첫 도출: CasualStrategy (Gotcha G-030, content-state-flow ADR)
- 트리거 사례: 전투 시스템 stub 단계 — `*Sequence` / `BattleAnimUtil` / `PlayerTurnController.PlayWeaponAttack` 본문이 모두 stub(즉시 완료)이어도 데이터 흐름(`DiceController.RollAll`, `ExecuteAttack`)이 정상 동작해야 함
- 응용 사례: **Binder ↔ Sequence 분리** (2026-05-20 SynergyCounterShakeSequence) — 같은 이벤트의 두 구독자 책임 분리. Binder는 매핑(type→slot) + 완료 이벤트(`OverlayRefreshed`)만 노출, prev/state 비교와 연출 코루틴은 Sequence가 보유. Binder에 prev tracking을 추가하면 책임 위배 (UIBinder ≠ 상태 추적자)
- 일반 "MVC View 분리"와의 차이: **시각 타임라인 자체를 데이터 코루틴에서 떼어낸다**는 점이 핵심

**원리**
- 데이터 코루틴은 **수치 계산 + 이벤트 발행**만 책임
- 시각 동기화 필요 시 **`Action onComplete` 콜백** 또는 **이벤트 hook**(`OnDiceRolling` / `OnDamageDealt` / `OnSlotsChanged`)으로 통지
- *Sequence 본문은 stub이어도 동일 시그니처 유지 → 빈 시퀀스/Tween 반환 + `if (seq != null) yield return seq.WaitForCompletion();` null 가드
- `WaitForSeconds` 등 시각 대기를 데이터 코루틴 본문에 끼워 넣지 않음 (한 번 끼우면 시각 ON/OFF 토글 시 데이터 타이밍 변함)
- 결과: 연출 ON/OFF 토글이 데이터 흐름에 영향 0, 디버깅 시 연출 통째로 비활성화 가능, 빠른 모드/스킵 옵션 자연 지원

**적용 가능성**
- 턴제/카드: 카드 효과 계산(데이터) ↔ 카드 이동/이펙트(연출)
- 격투: 데미지 판정 ↔ 히트 이펙트/슬로우모션
- RPG 전투: 스킬 데미지 ↔ 스킬 시전 애니메이션
- 빌더/시뮬레이션: 건설 완료 처리 ↔ 건설 애니메이션
- **본질**: "연출 없이도 게임이 동작해야 한다" 원칙 — 테스트성 + 스킵 옵션 + 디버깅 모드 모두 자연 지원

**미해결 질문**
- 시각이 데이터에 *영향을 줘야 하는* 경우 (히트스톱, 슬로우모션 중 입력 처리) 처리법
- 연출이 무겁고 데이터가 빠르면 큐가 쌓이는 문제 — 큐 한도 / 스킵 정책
- 멀티플레이에서 클라이언트별 연출 길이 차이가 데이터 동기에 영향
- 본 패턴의 **언어/엔진 독립 형태**는? Unity 외(Godot, UE)에서 동일 분리 가능한가?
- 연출이 데이터 결과를 "예고"하는 경우 (다이스 굴림 결과를 미리 알아야 연출 가능) 분리 위반 또는 lookahead 패턴 필요

**메타**
- 상태: `#1회검증` (CasualStrategy 전투 시스템 전체에 적용)
- 분야: `#아키텍처` `#패턴` `#디자인원리`
- 출처: `#자체관찰`
- 등재: 2026-05-16
- 승격 후보 노트: [[design-pattern-notes]] (구조 패턴) 또는 [[game-technique-notes]] (게임 기능) — 2프로젝트 검증 시 결정
