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
- `#본인적용미정` — 외부 출처에서 검증된 원칙·기법이지만 본인 프로젝트에 적용 사례 없음 (관찰만)
- `#승격됨→{노트}` — 기존 노트로 이주 완료 (본 노트는 strike-through로 유지)
- `#기각` — 더 나은 대안 발견 또는 비현실적 판명

### 분야
- `#시뮬레이션` `#시간시스템` `#네트워크` `#렌더링` `#AI` `#월드시스템`
- `#아키텍처` `#알고리즘` `#패턴` `#디자인원리`
- `#팀워크` `#프로세스` `#성능` `#관찰` `#테스팅`

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
| 14 | 명명 규약의 sub-pattern 분기 보정 (정의 정확도 회복) | `#패턴` `#아키텍처` `#디자인원리` | 코드 감사 기준(예: F-4 "다른 Manager 호출 = DI 우회 위반", G-023 "Unity Object 에 `?.` 금지")이 실제 코드 패턴보다 좁으면 정합 코드를 위반으로 오판. 해결: 단일 행 정의를 *2~3 sub-pattern* 으로 분기 — 명확 위반 / 회색 (정리 의무 없음) / 정합 화이트리스트. 기준 자체에 회색지대 인정 명시. 효과: (a) 위반 오판 0, (b) 회귀 감사 grep 헬퍼 정확도 ↑, (c) 사용자 결정 단순화 (회색은 메모만, 위반만 sub-plan 분기). 적용 가능성: 모든 lint 룰/코드 컨벤션/책임 분리 정의. 사례 ①: CasualStrategy plan-suffix-discipline-audit, F-4 6행 보정 — Effect/Pool/Handler/Service/Manager/Controller (2026-05-20). 사례 ②: G-023 Unity null conditional 룰의 화이트리스트 확장 — `*Manager.Instance?.Method(...)` 가 MonoSingleton getter 자동 복구 로직(quit 시 C# null + destroyed 시 CreateInstance)으로 안전한 sub-pattern임을 description 에 명시 (SFX 시스템 도입 시 code-guard agent 가 14건을 위반으로 표면 grep 검출 → 실제 안전 확인 후 예외 조항 확장으로 metric 32→18 복구, 2026-05-21). 트레이드오프: 정의가 복잡해져 처음 보는 사람이 회색 vs 위반 구분에 시간 소요. 단순 룰 사회/조직에는 부적합 (단일 binary 정의가 더 강제력 있음) | `#2회검증` |
| 15 | 부모 Manager 역참조 회색지대 (ctor 폭발 트레이드오프) | `#패턴` `#아키텍처` `#디자인원리` | Manager + Service 컴포지션 패턴에서 자식 Service가 부모 Manager.Instance 를 직접 호출하는 안티패턴 — 정합 모델은 ctor 주입이지만 부모 Manager가 자식 Service 의 *모든 의존*을 알아야 해 ctor 폭발 (Service 7개 × 각 의존 5개 = ctor 인자 35개). 해결: 외부 Manager 호출 (다른 도메인 — 명확 위반) vs 부모 Manager 역참조 (자기 컴포지션 부모 — 회색 메모) 명시 분리. 외부는 메서드 인자 주입으로 정리 가능 (단순 정리 sub-plan), 부모 역참조는 회색지대 인정 (즉시 정리 의무 없음). 효과: DI 정합 모델이 비현실적인 영역에서 트레이드오프 명시 — 모든 매니저 호출을 위반으로 분류하면 30+ 건 광범위 위반이 되어 정리 비현실적. 적용 가능성: Singleton + Service 컴포지션이 있는 모든 도메인 (RPG/시뮬레이션/대전략). 본 패턴은 #14 (sub-pattern 분기 보정)의 *구체 적용 사례*. 사례: CasualStrategy `HealthService`/`RewardService` BattleManager.Instance 역참조 10건 (2026-05-20). 트레이드오프: 회색 누적이 코드 결합도 증가의 *방치*로 이어질 위험 — 정기 감사로 회색 건수 모니터링 필요 | `#1회검증` |
| 16 | Controller 비대 분리 = 코디네이터 + 같은 GameObject 동거 sub-Controller | `#패턴` `#아키텍처` `#디자인원리` | 700+ 라인 단일 Controller가 N 책임(데이터↔UI↔버튼 풀스택) 혼재할 때 → 같은 GameObject에 N sub-Controller 컴포넌트로 동거 + 원 Controller는 코디네이터화. 자식 GameObject 추가 X → SerializeField만 prefab YAML 직접 편집으로 재분배 (Builder 재실행 없이 인스펙터 수동 조정 보존). 코디네이터 = sub 참조 + 이벤트 라우팅 + top-level UI(공통 텍스트 등). sub끼리 직접 참조 금지, 코디네이터만 라우팅 권한 (분리 의도 보존). 비교: POCO Service 분리는 비즈니스 로직만 가져가 UI 책임 잔존 → 비대 미해소. Binder + Service 분리는 *데이터↔UI↔버튼 풀스택* 단일 책임을 깰 수 없어 결합도 부정합. 적용 가능성: UI Controller가 N 섹션 혼재한 모든 도메인 (상점/인벤토리/장비창/캐릭터 시트). 한 도메인 내 책임이 서로 독립이어야 효과적 (책임 간 cross-cutting state가 강하면 코디네이터 라우팅이 비대해짐). 함정: (a) Header inspector 항목 5+개 모이면 group 정리 필요, (b) 같은 GameObject 컴포넌트가 늘어 직렬화 항목 증가 — 인스펙터 스크롤 부담, (c) `MonoBehaviour` 파생 sub 참조에 `?.` 사용 금지(G-023) — Unity overloaded `==` 우회되므로 `if (x != null) x.Method()` 명시 패턴 필수. 사례: CasualStrategy `ShopController` 700→144 라인 5 sub-Controller 분리 (`ShopItemSlotController` / `UsableShopController` / `GradeUpController` / `BenchSlotController` / `ShopDropRateView`, 2026-05-20) | `#1회검증` |
| 17 | 메타 강제 메커니즘의 3단 자가 가드 (자율 인지 + 비차단 hint + 사후 검증) | `#아키텍처` `#패턴` `#디자인원리` | "반드시 지키도록 강제"를 자동 차단 hook 없이 달성. 1차 정책 SOT를 상시 컨텍스트 노출(LLM/사람 자율 인지) → 2차 PostToolUse 같은 즉각 hint hook(위반을 systemMessage로 가시화, exit 0 비차단) → 3차 명시 호출 사후 검증(전수 점검). 강제력은 *가시화*에서 발생, 자율 차단은 보존. 트레이드오프: 1·2차 모두 비차단이라 의도적으로 무시 가능 → 3차가 backstop. 차단 hook 단독은 화이트리스트 비대화 + 회피 압력. Soft hint 단독은 1차 자가 인지 없으면 재작성 비용. 자가 인지만은 사후 검증 지연. 3단을 동시 작동시켜 어느 단도 차단하지 않으면서 매 신규 진입 시점에 위반 가시화. 적용 가능성: 명명 규약, 책임 분리 룰, 코드 컨벤션, 사내 정책 등 "차단 시 비용 크지만 위반 시 누적 비용도 큰" 메타 룰. 사례: CasualStrategy `harness/suffix-discipline` ADR (2026-05-20) — 차단 hook 폐기한 ADR-033 정합 유지하면서 4축+11종 접미사 명명 강제. 함정: 1·2차가 너무 친절하면 사람이 3차 호출을 잊음 → 3차는 PR 직전 hook 또는 정기 호출 룰로 강제하는 게 효과적 | `#1회검증` |
| 18 | enum 멤버 rename + 정수값 보존 (SerializeField/SO YAML 호환) | `#패턴` `#아키텍처` | enum이 SO YAML/세이브 파일에 정수로 직렬화되는 환경(Unity SerializeField, 직접 직렬화 시스템 일반)에서 enum 멤버 의미를 변경하려 할 때 — **이름만 rename + 정수값 보존**으로 직렬화 자산 무손상 마이그레이션 가능. 단순 사례: `SwordMasterMaxHpBonus = 14` → `SwordMasterBattleShield = 14`. SO 에셋의 `effectType: 14` YAML 값은 그대로 유지되어 12개 시너지 SO 모두 재저장 불필요. 적용 가능성: SO/세이브/네트워크 패킷에 enum이 정수 직렬화되는 모든 시스템 (RPG 능력치 효과, 카드 게임 효과, 스킬 트리). 함정: (a) enum 멤버를 *삭제*하거나 정수값을 *재배치*하면 SO YAML의 잔존 값이 다른 의미로 매핑되어 silent corruption — 폐기 멤버는 정수값을 *영구 점유*시키고 새 멤버는 다음 정수값 사용 (CasualStrategy SynergyEffectType의 "폐기 멤버 3·5~13 정수 재사용 금지" 룰), (b) Inspector dropdown의 의미는 enum 이름이므로 디자이너는 새 이름을 보지만 YAML diff는 변화 없음 — review 시 의미 변경을 놓치기 쉬움 → 커밋 메시지/ADR History에 *의미 변경* 명시 필수. 사례: CasualStrategy SynergyEffectType #14 SwordMaster MaxHp → BattleShield (2026-05-20). 트레이드오프: enum 값을 점유하는 dead 멤버가 누적되어 enum 가독성 저하 — 정기 정리 필요 vs 직렬화 호환 우선 | `#1회검증` |
| 19 | SO 데이터 매핑 키: string ID → SO 직접 참조 전환 (인스펙터 안전성) | `#패턴` `#아키텍처` `#Unity전용` | SO 기반 매핑 테이블(item→animation, monster→drop table 등)에서 키를 `string itemId` 로 두면 인스펙터에서 직접 문자열 입력 → 오타 위험 + 리네임 자동 추적 불가. **개선**: 매핑 룰의 키 필드를 `string` → `TargetSO` 직접 참조로 전환 (`public ItemDataSO sourceItem;`). 인스펙터 드래그앤드롭 + 컴파일 타임 타입 안전 + 리네임/이동 자동 추적. **호출자 무변경 트릭**: 런타임 캐시 빌드 단계에서만 `sourceItem.itemId` 추출하여 기존 `Dictionary<string, T>` 단일 유지 → `Get(string id)` API + 모든 호출자(`Play(inst.data.itemId)` 등) 그대로. 즉 *인스펙터 wiring 시점에만* SO 참조로 안전성 확보, 런타임은 string 유지. 마이그레이션: YAML `itemId: rod` 라인을 `sourceItem: {fileID, guid, type}` 로 일괄 치환(.asset 파일 직접 편집). 적용 가능성: SO 기반 매핑/룩업 테이블이 있는 모든 Unity 시스템 (아이템→이펙트, 적→드롭, 스킬→애니메이션, 카드→아트). 트레이드오프: 매핑 키로 사용할 SO들이 공통 베이스를 안 가지면 매핑 리스트가 베이스별로 N개 분리됨 (예: `ItemDataSO` ↔ `UsableItemDataSO` 분리 베이스 → `itemRules`/`usableItemRules` 2 리스트 + 런타임 캐시는 1 Dictionary 통합). 사례: CasualStrategy `AnimationConfigSO.ItemMappingRule.itemId(string) → sourceItem(ItemDataSO)` + `UsableItemMappingRule` 신설 (2026-05-20). 함정: 매핑 베이스가 abstract면 인스펙터는 파생 SO를 모두 받지만, 파생이 `itemId` 필드를 빈 문자열로 두면 캐시에서 silent 누락 → 빌드 시점 `IsNullOrEmpty` 가드 + 누락 시 `Debug.LogWarning` 권장 | `#1회검증` |
| 20 | Procedural UI Sprite 런타임 생성 (prefab/asset 추가 없는 단순 효과) | `#패턴` `#렌더링` `#Unity전용` | `Awake`에서 `Texture2D` + `Sprite.Create` 로 procedural sprite 동적 생성 → `image.sprite` 할당. vignette/gradient/border/mask 등 단순 절차적 패턴을 외부 sprite asset 추가 없이 단일 컴포넌트 안에서 self-contained 구현. 파라미터(threshold/power/color 등)를 `[SerializeField]` 로 노출하면 디자이너가 인스펙터에서 미세 조정 + Builder 재실행 불필요. 예: max-norm 사각형 vignette (`d = max(|nx|, |ny|)` + threshold/power smoothstep) → RectTransform stretch 에도 외곽 두께 균일. 적용 가능성: prefab/asset 추가 비용이 크거나, 1-2개 인스턴스만 쓰거나, 파라미터로 런타임에 패턴 모양을 바꾸고 싶은 단순 효과 (피격 vignette, scope mask, focus highlight, health bar gradient). 트레이드오프: (a) 텍스처가 인스턴스별 메모리 점유 — 다수 인스턴스 / 큰 해상도는 정적 asset이 효율적, (b) `OnDestroy`에서 `Destroy(sprite)` + `Destroy(texture)` 명시 호출 필수 — UnityEngine.Object는 GC 미수거이므로 leak 위험, (c) `hideFlags = HideAndDontSave` 로 에디터 인스펙트에 노출 안 되게 처리 권장. 함정: `Image.type = Sliced` 와 procedural sprite 조합 시 border 미설정으로 stretch 깨짐 → `Simple` + `preserveAspect = false` 가 max-norm 패턴엔 자연. 사례: CasualStrategy `HitOverlayFlasher` 256×256 max-norm vignette (`vignetteThreshold = 0.55` / `vignettePower = 1.6`, 2026-05-21). 가장자리 vignette 으로 화면 전체 단색 fill 대비 시야 가림 / 눈 피로 감소 | `#1회검증` |
| 21 | Mechanical Sympathy (Martin Thompson) | `#패턴` `#성능` `#관찰` | "하드웨어 동작 방식과 호흡 맞추기" — 캐시 라인, branch prediction, false sharing 등을 인지한 코드. CasualStrategy(캐주얼 전략)는 본격 적용 영역 없음. 부분 적용: NonAlloc Physics2D / 풀링뿐. 차후 data-oriented design 또는 Unity DOTS 도입 시 정식 등재 후보. 출처: LMAX Disruptor 구현자, "Mechanical Sympathy" 블로그/컨퍼런스 강연 | `#본인적용미정` |
| 22 | Conway's Law (Mel Conway, 1968) | `#아키텍처` `#팀워크` `#관찰` | "소프트웨어 구조는 그것을 설계한 조직의 통신 구조를 반영한다". 1인 개발이라 직접 적용 N/A. 다만 인간+AI(Claude) 협업 구조가 `docs/decisions/`(인간 SOT) / `.claude/skills/agents/`(AI 호출 구조) / `CLAUDE.md`(공통 컨텍스트) 분리에 반영 가능성 관찰. 차후 *다인 협업* 또는 *AI 협업 구조 변경* 시 검증 | `#본인적용미정` |
| 23 | Brooks's Law (Fred Brooks "Mythical Man-Month", 1975) | `#팀워크` `#프로세스` `#관찰` | "늦은 소프트웨어 프로젝트에 인력을 추가하면 더 늦어진다". 1인 + AI 협업이라 직접 적용 N/A. 응용: Plan followup 짝 룰("가정 차이/누락은 즉시 수정 X, 누적 후 일괄")의 동기 — 즉시 수정 = 작업 큐 폭발 + 컨텍스트 전환 비용. 차후 다인 협업 시 정식 검증 | `#본인적용미정` |
| 24 | Wirth's Law (Niklaus Wirth, 1995) | `#성능` `#관찰` | "소프트웨어가 하드웨어보다 빨리 느려진다". Unity 6 + URP가 본 법칙의 사례 — 엔진 기능 추가가 GPU 성능 압박. CasualStrategy(캐주얼 전략)는 GPU 여유라 묵인. 차후 모바일 빌드 또는 저사양 타겟 시 정식 적용 검토. 출처: "A Plea for Lean Software" 논문 | `#본인적용미정` |
| 25 | AAA (Arrange, Act, Assert) | `#테스팅` `#패턴` | 테스트 3구조: 사전 상태 셋업 / 동작 호출 / 결과 검증. CasualStrategy 자동화 테스트 미운영(Unity Test Framework 도입 안 함). 차후 도입 시 정식 등재 — `software-principle-notes` 신규 카테고리 H 신설 후보 | `#본인적용미정` |
| 26 | F.I.R.S.T. (Fast/Independent/Repeatable/Self-validating/Timely) | `#테스팅` `#패턴` | 단위 테스트가 갖춰야 할 5속성. Robert C. Martin "Clean Code" 출처. CasualStrategy 자동화 테스트 미운영. 차후 테스트 도입 시 AAA(#25), Given-When-Then(#27)과 함께 카테고리 H 신설 | `#본인적용미정` |
| 27 | Given-When-Then (BDD) | `#테스팅` `#패턴` | BDD 시나리오 구조: 사전 조건 / 동작 / 기대 결과. Daniel Terhorst-North BDD 출처. CasualStrategy 자동화 테스트 미운영. AAA(#25)의 자연어 버전 — 도입 시 둘 중 1개 선택 또는 영역별 분리 | `#본인적용미정` |
| 28 | SFX Voice Limit Pool (Hard Cap) | `#패턴` `#Unity전용` `#성능` | SFX 동시 발화를 단일 AudioSource PlayOneShot 중첩으로 처리하면 (a) 호출 직전 `source.pitch = pitch` 가 진행 중 클립 pitch 덮어씀 + (b) voice steal 로 두 번째 사운드 미발화. `AudioSource[]` 풀(N=8) + 라운드 로빈으로 source 분리 → 각 source 가 자기 클립만 재생 → race 해결. `AcquireSource` 가 비어있는(`!isPlaying`) 우선 선택, 모두 재생 중이면 가장 오래된 source steal — Hard Cap 으로 audio mud(phase cancellation/clipping) 절대 상한 보장. `PlayOneShot` 시그니처 무변경이라 호출지/매핑/채널 라우팅 그대로. mud 체감 사다리: Same-Clip Cooldown(50~100ms dedup) → Priority Eviction(SoundDataSO.priority enum) → pitchRange variation(0.95~1.05) 단계 추가 (YAGNI). 적용 가능성: SFX 시스템이 있는 모든 Unity 프로젝트. 함정: (a) 인스펙터 `sfxPoolSize` 변경 시 기존 source GameObject.AddComponent 후 풀 재생성 정책 필요(현 구현은 풀 길이 변화 감지 시 통째 재할당, 진행 중 클립은 끊김), (b) 풀이 작으면 9번째 호출에서 가장 오래된 SFX 끊김 — 게임 jam scale 비현실적이나 콘텐츠 확장 시 인스펙터 튜닝, (c) 동적 확장 풀(필요 시 source 추가 생성)은 mud 절대 상한 부재 → audio clutter — 기각 권장. 사례: CasualStrategy `AudioManager.sfxSources` (2026-05-21) | `#1회검증` |
| 29 | 활성 상태 통지 Service POCO (UI 갱신 표면 단일 채널) | `#패턴` `#아키텍처` `#디자인원리` | 매니저(BattleManager 등)에 새로 추가되는 *활성 상태 컬렉션*(활성 버프, 활성 효과, 활성 디버프)을 매니저 필드로 두고 OnXxxChanged 이벤트를 매니저에 직접 추가하면 매니저 책임 비대화 + 기존 매니저 상태 변경 위험. 해결: 도메인별 POCO Service(`ActiveBuffService`, MonoBehaviour 미상속) + `IReadOnlyList<Entry> Items` snapshot + `Register/Remove/Reset` + `OnXxxChanged` event 단일 통지 표면. 매니저는 Service 인스턴스만 노출(`public ActiveBuffService Buffs { get; } = new()`). UI Binder는 그 event 1개만 구독해 Refresh. Service Reset 시점은 매니저 라이프사이클 hook(StartBattle/EndBattle)에 1줄 추가로 통합. 적용 가능성: 매니저 상태가 다채로워질 때마다 신설 — RPG 디버프 풀, 카드 게임 활성 효과, 시뮬레이션 활성 이벤트 등 *목록형 활성 상태*. 트레이드오프: Service 1 파일 + 매니저 프로퍼티 1줄 비용 vs 매니저 비대화/통지 책임 분산 해결. 함정: (a) Service의 Register 시점이 매니저 상태 변경과 시간차가 있으면 race — handler 안에서 매니저 mutation 직후 Register 호출 권장, (b) Remove 시점이 다중 — 턴 종료/전투 종료/효과 소진 등 각 lifecycle 위치 호출 강제, 누락 시 zombie entry. (c) UI Binder가 패널 자체를 SetActive(false)로 비활성화하면 OnEnable 미호출 → Subscribe 안 됨 → 영원히 dead. 패널은 항상 active 유지하고 자식 슬롯만 토글. 사례: CasualStrategy `BattleManager.Buffs` (`ActiveBuffService`, 2026-05-21) | `#1회검증` |
| 30 | enum별 게임 룰 분류 정적 helper (SO 필드 회피) | `#패턴` `#아키텍처` `#디자인원리` | enum별 정책 판정(중복 허용 여부, 사용 가능 컨텍스트, 슬롯 표시 여부 등)을 SO 스키마에 bool 필드로 추가하면 (a) 기존 SO 에셋 일괄 마이그레이션 필요, (b) 룰 변경 시 SO 모두 재저장 필요, (c) 디자이너가 enum 멤버 간 일관성 못 보고 잘못 셋. 정적 helper(`XxxRules.IsStackable(type)` switch) 1 메서드로 분류 → SO 스키마 무변경, 룰 변경은 enum case 추가만, 디자이너는 인식 안 함(데이터가 아니라 코드 룰). 적용 가능성: enum 분류가 *게임 룰에서 파생*되는 모든 시스템(아이템 효과 분류, 스킬 타입 분류, 상태이상 분류, 데미지 타입 분류). 트레이드오프: 룰 변경 시 디자이너 SO 편집 불가 — 코드 수정 PR 필요. *디자이너 튜닝 필요한 값(damage 수치 등)은 SO에, 게임 룰 분류(이 효과는 중첩 가능한가?)는 helper에*가 자연 경계. 함정: (a) enum 멤버 추가 시 helper 갱신 누락 → switch default 처리(보수적 false/null) + Debug.LogWarning 권장, (b) helper가 매니저/Service 의존성을 가지면 정적 유틸 위배 — 분류 룰은 enum 자체에 닫혀야 함 (다른 컨텍스트 의존 X), (c) 분류 차원이 여러 개면(2축, 3축) helper 메서드 분리 권장(`IsStackable` + `IsUsableInContent` 등 단일 책임). 사례: CasualStrategy `UsableEffectTypeRules.IsStackable` (2026-05-21) | `#1회검증` |
| 31 | TMP SDF 폰트 atlas 누락 문자 ⇒ □ 폴백 + 매 렌더 경고 | `#Unity전용` `#TMP` `#L10N` `#폴리싱` | TMP_FontAsset 은 ttf 전체 글리프가 아닌 *atlas 빌드 시점에 포함된 글리프만* 보유 → atlas에 없는 codepoint는 fallback(`U+25A1` □)으로 치환 + 매 렌더마다 `Debug.LogWarning` 발생(콘솔 노이즈). 한국어 메인 폰트(Mulmaru SDF 등)는 한글+기본 ASCII만 포함하고 박스 드로잉(`└ ┌ ─ │ ├` U+2500~257F)은 누락 일반적. L10N 리소스에 트리 들여쓰기/특수 기호 넣기 전에 *기존 폰트 사용 문자 풀*에서 골라 쓰기(예: middle dot `·` U+00B7은 element_desc 류에서 이미 사용 중이라 안전 확인됨). 적용 가능성: TMP 사용하는 모든 Unity 프로젝트 + L10N JSON/string 리소스에 특수 문자 넣는 모든 케이스. 트레이드오프: 폰트 atlas에 글리프 추가는 별도 빌드 작업(atlas 재생성 + 메모리 증가) — 가벼운 들여쓰기 표시는 atlas 확장보다 안전 문자 대체가 비용 낮음. 함정: (a) 에디터 미리보기에서는 fallback 폰트 chain이 작동해 정상 표시되어 보일 수 있음 — 실제 런타임 콘솔에서만 경고 노출, (b) `·` 자체도 SDF 매핑 없는 폰트면 동일 문제 — 신규 폰트 도입 시 사용 중인 모든 특수문자 재검증 필요, (c) atlas regenerate를 미루다 누락 문자가 누적되면 일괄 점검 비용 — 신규 키 추가 시 즉시 검증이 저렴. 사례: CasualStrategy `tooltip_hp_*_fmt` 키의 `└`(U+2514) → `·`(U+00B7) 교체 (2026-05-21) | `#1회검증` |
| 32 | Push-based Materialized Spec invalidation | `#패턴` `#아키텍처` `#디자인원리` | 여러 소스(SO + 누적 상태 + 외부 조회)를 lazy 합산해 *사용 시점*(공격 신호 등)에 산출하면 "현재 최종값이 어디에도 존재하지 않음" — UI/툴팁/예측창이 그 값을 표시할 방법이 없음. push-based 전환: invalidation 트리거(슬롯 변경/소모품 사용/외부 상태 변경)마다 산출 후 컨테이너에 저장, UI는 값만 읽음. 3 책임 분리: `*Service`(POCO, 외부 상태 수집 + Calculator 호출, Manager 위임), `*Calculator`(static pure function, 정적 매니저 의존 0, 단위 테스트 가능), `*Controller`(UIBinderBase, 외부 이벤트 → Recalculate wiring + SerializeField 의존 가드). 단일 진입점 `Recalculate(InvalidationSource src)` + enum N종 source (`SynergyTier`/`BattleStart`/`Usable`/`MapMove`/`Dev`/`Init`). spec 반영 기준 정책 — *확정 가산/곱*만 spec, *확률 발동값*은 spec 미반영 + 라벨 표시: "spec.finalMax를 보장" 약속을 깨지 않기 위함 (실제 데미지는 발동 여부에 따라 변동). 의존 추적 3축 SOT — ADR §의존 필드 표(정답) + `[*Dependency]` 어트리뷰트(필드 한정, grep 가시화 부속, 메서드 호출 결과는 어트리뷰트 마킹 불가) + enum source 일치. 신규 의존 추가 3-step: ADR 표 → 어트리뷰트 → enum + wiring. 호버 중 갱신 race는 *stale 허용* 정책으로 회피 (이벤트 미발화 + UI 재계산 부담 회피, 호버 떼고 재호버 시 최신값). 적용 가능성: 합산 결과를 UI/툴팁/예측창에 표시해야 하는 모든 시스템 — 데미지 산출, 디버프 누적 시각화, 리소스 생산률 미리보기, 스탯 시뮬레이션, 데미지 캘큘레이터 UI(RPG/카드/대전략 전반). 트레이드오프: invalidation 트리거 누락 시 spec stale → 3-step 의무 + 정기 grep 검증으로 차단. lazy 단순성 포기 대신 UI 표시성 + 책임 분리 명확화 획득. 함정: (a) 확률 발동값을 spec에 합산하면 "spec.finalMax 보장" 약속 깨짐 — 정책으로 spec 미반영 + 라벨 분리 표시 강제, (b) 인스펙터 SerializeField 의존 누락 시 Controller 동작 0건 → 3중 가드(Subscribe 런타임 LogError + OnValidate 인스펙터 경고 + 빌더 단언). 사례: CasualStrategy `WeaponRuntimeSpec`/`WeaponSpecService`/`WeaponSpecCalculator`/`WeaponSpecsController` (2026-05-21, plan-materialized-weapon-spec 5묶음) | `#1회검증` |
| 33 | Slot N축 layered vignette + panel-level binder + 동적 sprite | `#패턴` `#Unity전용` `#렌더링` | 슬롯형 UI에 다중 상태(N효과)를 동시 시각화할 때 슬롯당 N Image stretch 정적 배치 + 각 Image color로 상태 식별 + GameObject.SetActive 토글. sprite는 외곽 fade-out white 1장 공유(view Awake에서 코드 동적 생성, #20 procedural sprite 적용) — PNG 자산 0개 + Image.color로 색 분기 + alpha 가산색 중첩 표현. **panel-level binder 1개가 M 슬롯 view 일괄 갱신** (slot-level binder 인스턴스 M개 패턴은 OnEnable M번 발화 + Refresh 분산 + 디버깅 분기 비용 증가, 기존 panel-level binder 사례 0건이면 panel-level 채택). binder는 SerializeField `views[M]` 배열 인스펙터 와이어 — 정렬이 슬롯 인덱스와 1:1 일치 필수 (인스펙터 수동 설정, 빌더 단언 미보유). `raycastTarget=false` 필수 (view AssignSprite에서 코드 1줄 안전망 권장) — vignette이 슬롯 드래그/클릭 가로채지 않게. 적용 가능성: 슬롯형 UI(인벤토리/큐/장비/카드 슬롯)에 N 상태 동시 표시가 필요한 모든 시스템 — 강화/디버프/속성/임시 효과 등 다축 시각화. 트레이드오프: prefab YAML에 슬롯당 N+1 GameObject 추가 작업(5슬롯×4효과 = 20 Image entry, Builder 미사용 시 인스펙터 수동 — Ctrl+D 복제로 일관성 보장). 함정: (a) 5 슬롯의 N Image color 인스펙터 입력 반복 시 alpha 슬라이더 누락 빈발 ([[34]] 참조), (b) raycastTarget true로 두면 vignette이 슬롯 인터랙션 가로챔 — 코드 안전망 1줄 추가, (c) Awake에서 sprite 동적 생성 시 OnDestroy cleanup 필수 (Destroy(sprite) + Destroy(texture), UnityEngine.Object GC 미수거). 사례: CasualStrategy `WeaponSlotVignetteView`/`WeaponSlotVignetteUIBinder` 4 효과 (slot0 DmgUp/전 슬롯 DmgUp/속성/Stun, 2026-05-21 slot-enhancement-lifecycle ADR §D-3) | `#1회검증` |
| 34 | 인스펙터 alpha 슬라이더 누락 함정 (multi-Image color 반복 입력) | `#Unity전용` `#관찰` `#폴리싱` | M 슬롯 × N Image 색 입력을 인스펙터에서 반복 작업 시 Color picker의 alpha 슬라이더는 RGB와 별개 입력 필요 — (a) 6자리 hex(`#RRGGBB`) 입력 시 alpha 변경 안 됨 (이전 default 유지, 새 picker는 alpha=0이 default일 수 있음), (b) RGB 슬라이더와 alpha 슬라이더가 분리돼 다수 칸 반복 입력 시 한두 칸 alpha 누락 발생, (c) Color picker 새로 열렸을 때 default alpha가 이전 작업 잔존값으로 표시될 수 있음. 증상: 코드 경로/데이터 모두 정상이고 `GameObject.SetActive(true)` 호출까지 검증되는데도 특정 슬롯의 특정 Image만 runtime 화면에 안 보임 — 디버깅 시 코드부터 의심해서 시간 낭비. 진단: 의심 슬롯의 Image Color picker A 슬라이더 직접 확인 — 0이면 의도값(예: 100/255)으로 수정. 예방: **슬롯 1개 prefab 완성 후 Ctrl+D 복제** (RGBA 일관성 보존, M회 반복 입력 회피). 적용 가능성: 인스펙터에서 다수 UI 요소 색 반복 입력하는 모든 Unity 작업 — vignette 패턴, 멀티 슬롯 grade backround, 카드 색 분류, ability 아이콘 tint 등. 디자이너 인계 시 "alpha 슬라이더 별도 확인" 체크리스트 필수. 함정: 8자리 hex 입력(`#RRGGBBAA`)으로 alpha까지 한 번에 설정 가능하지만 디자이너가 8자리 사용 습관 없으면 무의미. 트레이드오프: 정적 sprite (외부 PNG에 alpha 포함) 사용 시 인스펙터 alpha 무관 — 동적 색 분기가 필요한 경우만 발생. 사례: CasualStrategy WeaponSlot_1/_2 Element Image alpha=0 → Wind 풍속성 버프 vignette 안 보임 (2026-05-21, [[33]] 사례에서 발견) | `#1회검증` |
| 35 | 이벤트 vs 직접 호출 분리 (같은 시점, 각 메커니즘 단일 진입점) | `#패턴` `#아키텍처` `#디자인원리` | 같은 트리거 시점(예: 소모품 사용)에서 두 메커니즘(spec 재계산 + UI vignette 갱신)을 모두 구동해야 할 때, 두 메커니즘을 같은 이벤트 1개에 구독시키면 (a) 이벤트 구독자가 늘수록 발화 비용 증가, (b) 발화 순서 비결정성, (c) 일부 구독자만 디버깅 분리 어려움. 해결: **각 메커니즘 단일 진입점 보존** — spec 재계산은 발화 책임자(handler)가 직접 호출(`Recalculate(InvalidationSource.X)`), UI 갱신은 이벤트(`OnXxxChanged`) 발화로 분리. 같은 시점에 두 경로 병렬 진행하되 이중 호출 회피 + 각 메커니즘의 진입점이 1개라 디버깅·테스트 명확. 발화 순서는 결정 (예: 직접 호출 → 이벤트). 적용 가능성: UI 갱신·캐시 무효화·로깅·analytics 등 *부수 효과*가 *핵심 도메인 로직*과 같은 시점에 발생하는 모든 시스템. 핵심 도메인은 직접 호출(컴파일 타임 추적 가능), 부수 효과는 이벤트(런타임 동적 구독). 트레이드오프: 발화 위치 N개 모두에서 두 경로(직접 호출 + 이벤트 발화) 호출 코드 중복 — 헬퍼 함수로 묶을 수 있지만 추상화 비용. 함정: 발화 위치 누락 시 두 메커니즘 중 하나만 stale 가능 — 발화 위치 enumeration ADR에 명시 + 신규 추가 시 의무화. 사례: CasualStrategy `BattleManager.OnUsableModsChanged` 이벤트는 vignette 전용, `WeaponSpecs.Recalculate(Usable)` 직접 호출과 분리 (2026-05-21 slot-enhancement-lifecycle ADR §D-4). 같은 3 발화 위치(Apply/RunPlayerTurn 말미/StartBattle)에서 두 호출 병렬 | `#1회검증` |
| 36 | 자식 ADR이 부모 ADR 사전 hook 위탁 (계층 plan 협업 패턴) | `#패턴` `#프로세스` `#디자인원리` | 부모 plan/ADR이 향후 자식 plan/ADR에서 추가될 의존을 알면서 인프라를 사전 제공할 때 — **시그니처 hook + `_ = unused;` 자리표시 + 주석 명시**로 자식 plan 진입 비용을 줄이고 코드 정합 보장. 예: 부모 ADR이 `Calculator.Compute(int slotIdx, ...)` 시그니처에 `slotIdx` 인자를 추가하면서 본문에 `_ = slotIdx; // 후속 plan-X에서 slot0 합산 시 사용` 주석 hook을 남김 → 자식 plan은 이 인자를 활용해 1줄 추가만으로 결합 완료, Calculator 시그니처 변경(부모 ADR 짝 갱신) 불필요. 또한 부모 ADR §의존 필드 표에 자식이 추가할 필드 행을 미리 마련하거나 enum source(`InvalidationSource.Usable`)를 사전 정의. 적용 가능성: 다중 plan 계층으로 도메인을 점진 확장하는 모든 협업 환경 — ADR 단위 작업이 여러 sprint/세션에 걸쳐 진행되는 경우. 메타: 부모 plan이 "내가 모든 걸 다 하지 않고 일부는 자식 plan에 위임"이라는 책임 분담 명시 + 자식이 진입 시 부모의 hook을 즉시 발견 가능(`_ = unused;` 주석 + ADR §의존 필드 표 빈 행). 트레이드오프: 부모 ADR이 자식의 구체 사항을 미리 알아야 한다는 결합 — 자식 plan 폐기 시 hook이 dead code로 잔존(주석으로 의도 명시 필수). 함정: (a) hook이 너무 모호하면 자식 plan 작성자가 의도 못 읽음 → 주석에 자식 plan 파일명 또는 GitHub issue 링크 명시, (b) 부모 hook과 자식 plan 사이 시간 격차가 길면 부모 hook이 잊혀짐 → ADR `Future Work` 섹션에 자식 plan 트리거 명시. 사례: CasualStrategy weapon-runtime-spec ADR §D-2 (Calculator `slotIdx` 인자 + `_ = slotIdx;` 주석 hook + §라이프사이클 의존 행 "후속 plan-slot-enhancement-lifecycle" 명시) → 자식 slot-enhancement-lifecycle ADR이 1줄(`if (slotIdx == 0) ...`) 추가로 결합 완료 (2026-05-21) | `#1회검증` |
| 37 | Claude Code 듀얼 모델 라우팅 / settings.local.json env 우선순위 함정 | `#프로세스` `#관찰` | `settings.local.json` `env` 블록이 셸 $PROFILE env보다 우선 주입됨 → DeepSeek 기본 + Claude opt-in 구성에서 이 블록이 잘못 남아있으면 모든 세션이 덮어씌워짐. 해결: 블록 삭제 대신 DeepSeek/Claude 값을 명시적으로 기록, toggle 스크립트로 전환 | `#1회검증` |

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

## 37. Claude Code 듀얼 모델 라우팅 / settings.local.json env 우선순위 함정

**한 줄 요약**
`settings.local.json`의 `env` 블록은 셸 $PROFILE env보다 우선 주입된다 — DeepSeek 기본 + Claude opt-in 구성에서 이 블록이 잘못 남아있으면 모든 Claude Code 세션이 덮어씌워진다.

**출처/맥락**
- 첫 도출: CasualStrategy (2026-05-25) — DeepSeek 기본/$PROFILE 설정 후에도 VSCode 확장 세션이 Claude에 연결되던 문제 디버깅 중 발견
- 환경: Claude Code CLI + VSCode 확장 + PowerShell $PROFILE + DeepSeek API (Anthropic-compatible endpoint)

**문제 원인 상세**

Claude Code는 기동 시 다음 순서로 env를 결정한다:

```
settings.local.json env 블록   ← 최우선 (셸 env 덮어씀)
    ↑ 이것이 있으면 아래는 무시
$PROFILE env (DeepSeek 설정)   ← 셸 기동 시 주입
    ↑ VSCode 확장 프로세스는 이것을 안 가질 수 있음
프로세스 상속 env              ← VSCode를 어디서 열었느냐에 따라 다름
```

**발생했던 구체 시나리오 2가지**

1. **settings.local.json에 Claude URL 잔존**: 테스트/디버깅 중 `ANTHROPIC_BASE_URL = https://api.anthropic.com`을 env 블록에 넣었다가 지우지 않음 → $PROFILE에 DeepSeek 설정해도 모든 세션이 Claude로 강제됨
2. **toggle 스크립트가 "삭제"로 DeepSeek 복귀 시도**: `settings.local.json` env 블록을 삭제하면 셸 env 상속에 의존하는데, VSCode 확장 프로세스는 $PROFILE 없이 시작될 수 있음(VSCode를 시작 메뉴/바로가기로 열면 $PROFILE 미소싱) → env 없음 = Anthropic 기본값으로 폴백

**해결**

- **settings.local.json env 블록을 삭제하지 말고 명시적으로 기록**: DeepSeek 모드 ↔ Claude 모드 전환 시 해당 값을 완전히 기록
- **toggle 스크립트 수정** (`d:\AI\toggle-claude-model.ps1`): "DeepSeek 복귀 = 블록 삭제" → "DeepSeek 복귀 = DeepSeek env 블록 명시 기록"

```powershell
# DeepSeek 모드 (settings.local.json env 블록)
{
  "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
  "ANTHROPIC_AUTH_TOKEN": "sk-...",
  "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
  ...
}

# Claude 모드 (settings.local.json env 블록)
{
  "ANTHROPIC_BASE_URL": "https://api.anthropic.com"
  // AUTH_TOKEN 없음 → OAuth 사용
}
```

- **VSCode 터미널 단축 함수** ($PROFILE에 추가): `function tm { & d:\AI\toggle-claude-model.ps1 }` → `tm` 한 번으로 전환 + "Restart Claude Code session to apply." 출력

**핵심 주의사항**

- `ANTHROPIC_AUTH_TOKEN`을 Claude 모드 env 블록에 넣으면 안 됨 → Pro 플랜 OAuth가 아닌 API 크레딧으로 과금됨 ("Credit balance is too low" 에러 원인)
- settings.local.json은 `.gitignore`에 포함 → API 키 기록 안전
- 설정 변경 후 Claude Code 세션 재시작 필수 (실행 중에는 반영 안 됨)

**적용 가능성**
Claude Code + 외부 LLM API(DeepSeek/OpenAI-compatible/Azure 등) 듀얼 라우팅 구성 모든 경우. `settings.local.json` env 블록은 개발 환경 오버라이드의 최우선 채널이므로 잘못 남아있으면 $PROFILE/시스템 env를 모두 무력화한다.

**메타**
- 상태: `#1회검증` (CasualStrategy 환경 수정 완료, 2026-05-25)
- 분야: `#프로세스` `#관찰`
- 출처: `#자체관찰`
- 등재: 2026-05-25
- 승격 후보: 도구 설정 관련 항목이 3개 이상 누적되면 `devenv-notes.md` 신설 후 이주
