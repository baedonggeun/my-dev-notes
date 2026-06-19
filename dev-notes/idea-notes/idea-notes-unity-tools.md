# 아이디어 — Unity·도구·메타

> 상위 노트: [[idea-notes]] (전체 인덱스 디스패처)
> 다루는 축: Unity 특화·도구·프로세스·자체관찰
> 다루지 않는 축: 아이디어 — 아키텍처·패턴 / 아이디어 — 법칙·원칙·테스트

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


# 인덱스

| # | 아이디어명 | 분야 | 한 줄 요약 | 상태 |
|---|----------|------|----------|------|
| 28 | Unity 동적 Canvas 자식 생성 4대 함정 | `#패턴` `#Unity전용` `#렌더링` | 런타임에 Canvas 직속 자식 GameObject를 동적 생성할 때 반드시 지켜야 할 4가지: (1) **RectTransform BEFORE SetParent** — `AddComponent<RectTransform>()` 후 `SetParent(canvas.transform, false)`. 역순이면 Canvas가 자식을 렌더 대상으로 추적 못해 화면 미표시. (2) **Lazy Canvas init** — UIManager가 Instantiate 이후 Canvas에 부모 설정하는 구조(ContentUI 등)라면 Awake 캐싱 불가. lazy `EnsureCanvas()` 를 코루틴/메서드 진입 시점에 호출. (3) **overrideSorting 필수** — 임시 fly card 등 Canvas 자식은 다른 Canvas 자식(sortingOrder > 0)에 가려짐. `AddComponent<Canvas>(); c.overrideSorting=true; c.sortingOrder=rootCanvas.sortingOrder+50`. (4) **InverseTransformPoint** — World→Canvas 좌표 변환은 `WorldToScreenPoint + ScreenPointToLocalPointInRectangle` 조합이 CanvasScaler 스케일 의존 오류 있음. `canvasRT.InverseTransformPoint(worldPos)` 한 줄로 모드 무관 정확 변환. 첫 사례: CasualStrategy GachaSequence fly card (2026-05-26). 연관: Sequence 컴포넌트 내 동적 연출 UI, 피격 팝업, 픽업 연출 등 | `#1회검증` |
| 28 | SFX Voice Limit Pool (Hard Cap) | `#패턴` `#Unity전용` `#성능` | SFX 동시 발화를 단일 AudioSource PlayOneShot 중첩으로 처리하면 (a) 호출 직전 `source.pitch = pitch` 가 진행 중 클립 pitch 덮어씀 + (b) voice steal 로 두 번째 사운드 미발화. `AudioSource[]` 풀(N=8) + 라운드 로빈으로 source 분리 → 각 source 가 자기 클립만 재생 → race 해결. `AcquireSource` 가 비어있는(`!isPlaying`) 우선 선택, 모두 재생 중이면 가장 오래된 source steal — Hard Cap 으로 audio mud(phase cancellation/clipping) 절대 상한 보장. `PlayOneShot` 시그니처 무변경이라 호출지/매핑/채널 라우팅 그대로. mud 체감 사다리: Same-Clip Cooldown(50~100ms dedup) → Priority Eviction(SoundDataSO.priority enum) → pitchRange variation(0.95~1.05) 단계 추가 (YAGNI). 적용 가능성: SFX 시스템이 있는 모든 Unity 프로젝트. 함정: (a) 인스펙터 `sfxPoolSize` 변경 시 기존 source GameObject.AddComponent 후 풀 재생성 정책 필요(현 구현은 풀 길이 변화 감지 시 통째 재할당, 진행 중 클립은 끊김), (b) 풀이 작으면 9번째 호출에서 가장 오래된 SFX 끊김 — 게임 jam scale 비현실적이나 콘텐츠 확장 시 인스펙터 튜닝, (c) 동적 확장 풀(필요 시 source 추가 생성)은 mud 절대 상한 부재 → audio clutter — 기각 권장. 사례: CasualStrategy `AudioManager.sfxSources` (2026-05-21) | `#1회검증` |
| 29 | 활성 상태 통지 Service POCO (UI 갱신 표면 단일 채널) | `#패턴` `#아키텍처` `#디자인원리` | 매니저(BattleManager 등)에 새로 추가되는 *활성 상태 컬렉션*(활성 버프, 활성 효과, 활성 디버프)을 매니저 필드로 두고 OnXxxChanged 이벤트를 매니저에 직접 추가하면 매니저 책임 비대화 + 기존 매니저 상태 변경 위험. 해결: 도메인별 POCO Service(`ActiveBuffService`, MonoBehaviour 미상속) + `IReadOnlyList<Entry> Items` snapshot + `Register/Remove/Reset` + `OnXxxChanged` event 단일 통지 표면. 매니저는 Service 인스턴스만 노출(`public ActiveBuffService Buffs { get; } = new()`). UI Binder는 그 event 1개만 구독해 Refresh. Service Reset 시점은 매니저 라이프사이클 hook(StartBattle/EndBattle)에 1줄 추가로 통합. 적용 가능성: 매니저 상태가 다채로워질 때마다 신설 — RPG 디버프 풀, 카드 게임 활성 효과, 시뮬레이션 활성 이벤트 등 *목록형 활성 상태*. 트레이드오프: Service 1 파일 + 매니저 프로퍼티 1줄 비용 vs 매니저 비대화/통지 책임 분산 해결. 함정: (a) Service의 Register 시점이 매니저 상태 변경과 시간차가 있으면 race — handler 안에서 매니저 mutation 직후 Register 호출 권장, (b) Remove 시점이 다중 — 턴 종료/전투 종료/효과 소진 등 각 lifecycle 위치 호출 강제, 누락 시 zombie entry. (c) UI Binder가 패널 자체를 SetActive(false)로 비활성화하면 OnEnable 미호출 → Subscribe 안 됨 → 영원히 dead. 패널은 항상 active 유지하고 자식 슬롯만 토글. 사례: CasualStrategy `BattleManager.Buffs` (`ActiveBuffService`, 2026-05-21) | `#1회검증` |
| 30 | enum별 게임 룰 분류 정적 helper (SO 필드 회피) | `#패턴` `#아키텍처` `#디자인원리` | enum별 정책 판정(중복 허용 여부, 사용 가능 컨텍스트, 슬롯 표시 여부 등)을 SO 스키마에 bool 필드로 추가하면 (a) 기존 SO 에셋 일괄 마이그레이션 필요, (b) 룰 변경 시 SO 모두 재저장 필요, (c) 디자이너가 enum 멤버 간 일관성 못 보고 잘못 셋. 정적 helper(`XxxRules.IsStackable(type)` switch) 1 메서드로 분류 → SO 스키마 무변경, 룰 변경은 enum case 추가만, 디자이너는 인식 안 함(데이터가 아니라 코드 룰). 적용 가능성: enum 분류가 *게임 룰에서 파생*되는 모든 시스템(아이템 효과 분류, 스킬 타입 분류, 상태이상 분류, 데미지 타입 분류). 트레이드오프: 룰 변경 시 디자이너 SO 편집 불가 — 코드 수정 PR 필요. *디자이너 튜닝 필요한 값(damage 수치 등)은 SO에, 게임 룰 분류(이 효과는 중첩 가능한가?)는 helper에*가 자연 경계. 함정: (a) enum 멤버 추가 시 helper 갱신 누락 → switch default 처리(보수적 false/null) + Debug.LogWarning 권장, (b) helper가 매니저/Service 의존성을 가지면 정적 유틸 위배 — 분류 룰은 enum 자체에 닫혀야 함 (다른 컨텍스트 의존 X), (c) 분류 차원이 여러 개면(2축, 3축) helper 메서드 분리 권장(`IsStackable` + `IsUsableInContent` 등 단일 책임). 사례: CasualStrategy `UsableEffectTypeRules.IsStackable` (2026-05-21) | `#1회검증` |
| 31 | TMP SDF 폰트 atlas 누락 문자 ⇒ □ 폴백 + 매 렌더 경고 | `#Unity전용` `#TMP` `#L10N` `#폴리싱` | TMP_FontAsset 은 ttf 전체 글리프가 아닌 *atlas 빌드 시점에 포함된 글리프만* 보유 → atlas에 없는 codepoint는 fallback(`U+25A1` □)으로 치환 + 매 렌더마다 `Debug.LogWarning` 발생(콘솔 노이즈). 한국어 메인 폰트(Mulmaru SDF 등)는 한글+기본 ASCII만 포함하고 박스 드로잉(`└ ┌ ─ │ ├` U+2500~257F)은 누락 일반적. L10N 리소스에 트리 들여쓰기/특수 기호 넣기 전에 *기존 폰트 사용 문자 풀*에서 골라 쓰기(예: middle dot `·` U+00B7은 element_desc 류에서 이미 사용 중이라 안전 확인됨). 적용 가능성: TMP 사용하는 모든 Unity 프로젝트 + L10N JSON/string 리소스에 특수 문자 넣는 모든 케이스. 트레이드오프: 폰트 atlas에 글리프 추가는 별도 빌드 작업(atlas 재생성 + 메모리 증가) — 가벼운 들여쓰기 표시는 atlas 확장보다 안전 문자 대체가 비용 낮음. 함정: (a) 에디터 미리보기에서는 fallback 폰트 chain이 작동해 정상 표시되어 보일 수 있음 — 실제 런타임 콘솔에서만 경고 노출, (b) `·` 자체도 SDF 매핑 없는 폰트면 동일 문제 — 신규 폰트 도입 시 사용 중인 모든 특수문자 재검증 필요, (c) atlas regenerate를 미루다 누락 문자가 누적되면 일괄 점검 비용 — 신규 키 추가 시 즉시 검증이 저렴. 사례: CasualStrategy `tooltip_hp_*_fmt` 키의 `└`(U+2514) → `·`(U+00B7) 교체 (2026-05-21) | `#1회검증` |
| 32 | Push-based Materialized Spec invalidation | `#패턴` `#아키텍처` `#디자인원리` | 여러 소스(SO + 누적 상태 + 외부 조회)를 lazy 합산해 *사용 시점*(공격 신호 등)에 산출하면 "현재 최종값이 어디에도 존재하지 않음" — UI/툴팁/예측창이 그 값을 표시할 방법이 없음. push-based 전환: invalidation 트리거(슬롯 변경/소모품 사용/외부 상태 변경)마다 산출 후 컨테이너에 저장, UI는 값만 읽음. 3 책임 분리: `*Service`(POCO, 외부 상태 수집 + Calculator 호출, Manager 위임), `*Calculator`(static pure function, 정적 매니저 의존 0, 단위 테스트 가능), `*Controller`(UIBinderBase, 외부 이벤트 → Recalculate wiring + SerializeField 의존 가드). 단일 진입점 `Recalculate(InvalidationSource src)` + enum N종 source (`SynergyTier`/`BattleStart`/`Usable`/`MapMove`/`Dev`/`Init`). spec 반영 기준 정책 — *확정 가산/곱*만 spec, *확률 발동값*은 spec 미반영 + 라벨 표시: "spec.finalMax를 보장" 약속을 깨지 않기 위함 (실제 데미지는 발동 여부에 따라 변동). 의존 추적 3축 SOT — ADR §의존 필드 표(정답) + `[*Dependency]` 어트리뷰트(필드 한정, grep 가시화 부속, 메서드 호출 결과는 어트리뷰트 마킹 불가) + enum source 일치. 신규 의존 추가 3-step: ADR 표 → 어트리뷰트 → enum + wiring. 호버 중 갱신 race는 *stale 허용* 정책으로 회피 (이벤트 미발화 + UI 재계산 부담 회피, 호버 떼고 재호버 시 최신값). 적용 가능성: 합산 결과를 UI/툴팁/예측창에 표시해야 하는 모든 시스템 — 데미지 산출, 디버프 누적 시각화, 리소스 생산률 미리보기, 스탯 시뮬레이션, 데미지 캘큘레이터 UI(RPG/카드/대전략 전반). 트레이드오프: invalidation 트리거 누락 시 spec stale → 3-step 의무 + 정기 grep 검증으로 차단. lazy 단순성 포기 대신 UI 표시성 + 책임 분리 명확화 획득. 함정: (a) 확률 발동값을 spec에 합산하면 "spec.finalMax 보장" 약속 깨짐 — 정책으로 spec 미반영 + 라벨 분리 표시 강제, (b) 인스펙터 SerializeField 의존 누락 시 Controller 동작 0건 → 3중 가드(Subscribe 런타임 LogError + OnValidate 인스펙터 경고 + 빌더 단언). 사례: CasualStrategy `WeaponRuntimeSpec`/`WeaponSpecService`/`WeaponSpecCalculator`/`WeaponSpecsController` (2026-05-21, plan-materialized-weapon-spec 5묶음) | `#1회검증` |
| 33 | Slot N축 layered vignette + panel-level binder + 동적 sprite | `#패턴` `#Unity전용` `#렌더링` | 슬롯형 UI에 다중 상태(N효과)를 동시 시각화할 때 슬롯당 N Image stretch 정적 배치 + 각 Image color로 상태 식별 + GameObject.SetActive 토글. sprite는 외곽 fade-out white 1장 공유(view Awake에서 코드 동적 생성, 항목 20 procedural sprite 적용) — PNG 자산 0개 + Image.color로 색 분기 + alpha 가산색 중첩 표현. **panel-level binder 1개가 M 슬롯 view 일괄 갱신** (slot-level binder 인스턴스 M개 패턴은 OnEnable M번 발화 + Refresh 분산 + 디버깅 분기 비용 증가, 기존 panel-level binder 사례 0건이면 panel-level 채택). binder는 SerializeField `views[M]` 배열 인스펙터 와이어 — 정렬이 슬롯 인덱스와 1:1 일치 필수 (인스펙터 수동 설정, 빌더 단언 미보유). `raycastTarget=false` 필수 (view AssignSprite에서 코드 1줄 안전망 권장) — vignette이 슬롯 드래그/클릭 가로채지 않게. 적용 가능성: 슬롯형 UI(인벤토리/큐/장비/카드 슬롯)에 N 상태 동시 표시가 필요한 모든 시스템 — 강화/디버프/속성/임시 효과 등 다축 시각화. 트레이드오프: prefab YAML에 슬롯당 N+1 GameObject 추가 작업(5슬롯×4효과 = 20 Image entry, Builder 미사용 시 인스펙터 수동 — Ctrl+D 복제로 일관성 보장). 함정: (a) 5 슬롯의 N Image color 인스펙터 입력 반복 시 alpha 슬라이더 누락 빈발 (항목 34 참조), (b) raycastTarget true로 두면 vignette이 슬롯 인터랙션 가로챔 — 코드 안전망 1줄 추가, (c) Awake에서 sprite 동적 생성 시 OnDestroy cleanup 필수 (Destroy(sprite) + Destroy(texture), UnityEngine.Object GC 미수거). 사례: CasualStrategy `WeaponSlotVignetteView`/`WeaponSlotVignetteUIBinder` 4 효과 (slot0 DmgUp/전 슬롯 DmgUp/속성/Stun, 2026-05-21 slot-enhancement-lifecycle ADR §D-3) | `#1회검증` |
| 34 | 인스펙터 alpha 슬라이더 누락 함정 (multi-Image color 반복 입력) | `#Unity전용` `#관찰` `#폴리싱` | M 슬롯 × N Image 색 입력을 인스펙터에서 반복 작업 시 Color picker의 alpha 슬라이더는 RGB와 별개 입력 필요 — (a) 6자리 hex(`#RRGGBB`) 입력 시 alpha 변경 안 됨 (이전 default 유지, 새 picker는 alpha=0이 default일 수 있음), (b) RGB 슬라이더와 alpha 슬라이더가 분리돼 다수 칸 반복 입력 시 한두 칸 alpha 누락 발생, (c) Color picker 새로 열렸을 때 default alpha가 이전 작업 잔존값으로 표시될 수 있음. 증상: 코드 경로/데이터 모두 정상이고 `GameObject.SetActive(true)` 호출까지 검증되는데도 특정 슬롯의 특정 Image만 runtime 화면에 안 보임 — 디버깅 시 코드부터 의심해서 시간 낭비. 진단: 의심 슬롯의 Image Color picker A 슬라이더 직접 확인 — 0이면 의도값(예: 100/255)으로 수정. 예방: **슬롯 1개 prefab 완성 후 Ctrl+D 복제** (RGBA 일관성 보존, M회 반복 입력 회피). 적용 가능성: 인스펙터에서 다수 UI 요소 색 반복 입력하는 모든 Unity 작업 — vignette 패턴, 멀티 슬롯 grade backround, 카드 색 분류, ability 아이콘 tint 등. 디자이너 인계 시 "alpha 슬라이더 별도 확인" 체크리스트 필수. 함정: 8자리 hex 입력(`#RRGGBBAA`)으로 alpha까지 한 번에 설정 가능하지만 디자이너가 8자리 사용 습관 없으면 무의미. 트레이드오프: 정적 sprite (외부 PNG에 alpha 포함) 사용 시 인스펙터 alpha 무관 — 동적 색 분기가 필요한 경우만 발생. 사례: CasualStrategy WeaponSlot_1/_2 Element Image alpha=0 → Wind 풍속성 버프 vignette 안 보임 (2026-05-21, 항목 33 사례에서 발견) | `#1회검증` |
| 35 | 이벤트 vs 직접 호출 분리 (같은 시점, 각 메커니즘 단일 진입점) | `#패턴` `#아키텍처` `#디자인원리` | 같은 트리거 시점(예: 소모품 사용)에서 두 메커니즘(spec 재계산 + UI vignette 갱신)을 모두 구동해야 할 때, 두 메커니즘을 같은 이벤트 1개에 구독시키면 (a) 이벤트 구독자가 늘수록 발화 비용 증가, (b) 발화 순서 비결정성, (c) 일부 구독자만 디버깅 분리 어려움. 해결: **각 메커니즘 단일 진입점 보존** — spec 재계산은 발화 책임자(handler)가 직접 호출(`Recalculate(InvalidationSource.X)`), UI 갱신은 이벤트(`OnXxxChanged`) 발화로 분리. 같은 시점에 두 경로 병렬 진행하되 이중 호출 회피 + 각 메커니즘의 진입점이 1개라 디버깅·테스트 명확. 발화 순서는 결정 (예: 직접 호출 → 이벤트). 적용 가능성: UI 갱신·캐시 무효화·로깅·analytics 등 *부수 효과*가 *핵심 도메인 로직*과 같은 시점에 발생하는 모든 시스템. 핵심 도메인은 직접 호출(컴파일 타임 추적 가능), 부수 효과는 이벤트(런타임 동적 구독). 트레이드오프: 발화 위치 N개 모두에서 두 경로(직접 호출 + 이벤트 발화) 호출 코드 중복 — 헬퍼 함수로 묶을 수 있지만 추상화 비용. 함정: 발화 위치 누락 시 두 메커니즘 중 하나만 stale 가능 — 발화 위치 enumeration ADR에 명시 + 신규 추가 시 의무화. 사례: CasualStrategy `BattleManager.OnUsableModsChanged` 이벤트는 vignette 전용, `WeaponSpecs.Recalculate(Usable)` 직접 호출과 분리 (2026-05-21 slot-enhancement-lifecycle ADR §D-4). 같은 3 발화 위치(Apply/RunPlayerTurn 말미/StartBattle)에서 두 호출 병렬 | `#1회검증` |
| 36 | 자식 ADR이 부모 ADR 사전 hook 위탁 (계층 plan 협업 패턴) | `#패턴` `#프로세스` `#디자인원리` | 부모 plan/ADR이 향후 자식 plan/ADR에서 추가될 의존을 알면서 인프라를 사전 제공할 때 — **시그니처 hook + `_ = unused;` 자리표시 + 주석 명시**로 자식 plan 진입 비용을 줄이고 코드 정합 보장. 예: 부모 ADR이 `Calculator.Compute(int slotIdx, ...)` 시그니처에 `slotIdx` 인자를 추가하면서 본문에 `_ = slotIdx; // 후속 plan-X에서 slot0 합산 시 사용` 주석 hook을 남김 → 자식 plan은 이 인자를 활용해 1줄 추가만으로 결합 완료, Calculator 시그니처 변경(부모 ADR 짝 갱신) 불필요. 또한 부모 ADR §의존 필드 표에 자식이 추가할 필드 행을 미리 마련하거나 enum source(`InvalidationSource.Usable`)를 사전 정의. 적용 가능성: 다중 plan 계층으로 도메인을 점진 확장하는 모든 협업 환경 — ADR 단위 작업이 여러 sprint/세션에 걸쳐 진행되는 경우. 메타: 부모 plan이 "내가 모든 걸 다 하지 않고 일부는 자식 plan에 위임"이라는 책임 분담 명시 + 자식이 진입 시 부모의 hook을 즉시 발견 가능(`_ = unused;` 주석 + ADR §의존 필드 표 빈 행). 트레이드오프: 부모 ADR이 자식의 구체 사항을 미리 알아야 한다는 결합 — 자식 plan 폐기 시 hook이 dead code로 잔존(주석으로 의도 명시 필수). 함정: (a) hook이 너무 모호하면 자식 plan 작성자가 의도 못 읽음 → 주석에 자식 plan 파일명 또는 GitHub issue 링크 명시, (b) 부모 hook과 자식 plan 사이 시간 격차가 길면 부모 hook이 잊혀짐 → ADR `Future Work` 섹션에 자식 plan 트리거 명시. 사례: CasualStrategy weapon-runtime-spec ADR §D-2 (Calculator `slotIdx` 인자 + `_ = slotIdx;` 주석 hook + §라이프사이클 의존 행 "후속 plan-slot-enhancement-lifecycle" 명시) → 자식 slot-enhancement-lifecycle ADR이 1줄(`if (slotIdx == 0) ...`) 추가로 결합 완료 (2026-05-21) | `#1회검증` |
| 37 | Claude Code 듀얼 모델 라우팅 / settings.local.json env 우선순위 함정 | `#프로세스` `#관찰` | `settings.local.json` `env` 블록이 셸 $PROFILE env보다 우선 주입됨 → DeepSeek 기본 + Claude opt-in 구성에서 이 블록이 잘못 남아있으면 모든 세션이 덮어씌워짐. 해결: 블록 삭제 대신 DeepSeek/Claude 값을 명시적으로 기록, toggle 스크립트로 전환 | `#1회검증` |
| 38 | Caveman — LLM 출력 토큰 압축 skill | `#프로세스` `#관찰` | AI 코딩 에이전트 응답을 "원시인 스타일"로 압축해 출력 토큰 ~65% 절감. SKILL.md 1파일로 /caveman opt-in 또는 SessionStart hook으로 자동 활성화. caveman-compress로 CLAUDE.md 등 입력 파일도 영구 압축 가능 | `#1회검증` |
| 39 | 전 Tier plan-first (T1~T4 plan 승인 대기) | `#프로세스` `#디자인원리` `#관찰` | AI 코딩에서 DeepSeek 등 외부 구현자 handoff를 위해 T1/T2 단순 작업도 plan 먼저 작성 후 사용자 승인 대기. 외부 구현자가 읽고 질문 없이 구현 가능한 수준의 상세도 강제 | `#1회검증` |
| 40 | 단일 Controller type 분기 → N specialized Controller + prefab 분리 | `#패턴` `#아키텍처` `#디자인원리` | 단일 Controller가 N type을 if/switch로 분기 처리 → 각 type별 specialized Controller로 분리 + 각자 prefab + 각자 필요한 SerializeField만 보유 + Fill 시그니처 간소화. N=3 정도면 추상화 비용 없이 중복 허용(N=1회는 분리 비용＞효과, N=3+는 반응적 분리 시점). 호출자(Manager/UIBinder)는 type 검사로 분기 결정, 시그니처 감소로 호출 단순화. 공통 로직(TooltipBase)은 상속 유지, 공통 helper(GetFirstSynergyIcon)는 중복 허용. 적용 가능성: 동일 prefab에서 type별 표시가 다른 슬롯형 UI(툴팁/카드/인벤토리 슬롯/스탯 창). 사례: CasualStrategy SlotItemTooltipController → BasicWeapon/CombinedItem/AttrStack 3종 분리 (2026-06-04) | `#1회검증` |
| 41 | Hover Tooltip 내 Action Button (gold 소비 강화) | `#패턴` `#게임UI` `#디자인원리` | 아이템 hover tooltip을 단순 정보 표시를 넘어 Action 엔트리포인트로 활용 — 툴팁 안에 Button 배치 + static event → Manager 핸들링 → gold 차감 → slot 갱신. 드래그-겹치기(같은 아이템 투입해서 강화)를 UI 툴팁 내 1-click button으로 대체. 필수 조건: (a) static event로 Manager 요청 (Tooltip 컴포넌트가 Manager 직접 mutation 금지, rules.md §1 금지 사항), (b) click 직후 TooltipManager.Hide() 자동 호출 UI 클린업, (c) gold 부족 시 버튼 interactable=false (disabled color), MAX 도달 시 텍스트 "MAX" 전환. 적용 가능성: hover 시 추가 Action이 필요한 게임 시스템 — 인벤토리 강화, 소모품 사용, 아이템 분해, 캐릭터 귀속/해제, 장비합성 미리보기 "합성 가능" 뱃지 등을 툴팁에 통합. 트레이드오프: 드래그-겹치기(2회 Drag) → click(1회) 상호작용 축소, 버튼이 있는 툴팁은 hover 유지 시 click 가능 영역이 추가돼 PointerExit 타이밍 관리 복잡 → EventTrigger 포인터 델리게이트에 cancel/freeze 타이머 유지. 함정: (a) 툴팁 보통 Destroy 직전까지 PointerExit race → enhanceButton.onClick과 TooltipManager.Hide 타이밍 충돌 (클릭 후 즉시 Hide면 click 핸들링 전에 툴팁 사라짐). 해결: click handler에서 먼저 event 발화 + 그 후 Hide(), (b) 여러 Action을 같은 툴팁에 두면 버튼 영역 혼잡 → 1 Action per tooltip 유지 권장, (c) Builder가 툴팁 프리팹과 동시에 버튼 위치/색상/크기 결정해야 해서 툴팁 빌더 코드 복잡 소폭 증가. 사례: CasualStrategy CombinedItemTooltipController.enhanceButton + OnEnhanceRequested event (2026-06-05) | `#1회검증` |
| 42 | Graceful Multi-Pull Degradation (여유분만큼 뽑기) | `#게임UI` `#디자인원리` | X회 일괄 뽑기에서 티켓 부족 시 보유량만큼만 뽑기 제공. reject 대신 부분 허용 → 마찰 감소. 버튼 텍스트 "10회(3장)" 동적 표시 결합 권장. 보유량 ≥ 1일 때만 활성화 | `#1회검증` |
| 43 | Global Dismiss Gesture (어디서든 닫기) | `#패턴` `#게임UI` `#디자인원리` | 열린 플로팅 UI(툴팁/드롭다운)를 전역 InputHandler/Manager가 제스처(우클릭/ESC) 감지 후 닫기 — UI 자체가 닫힘 트리거를 모름. 내부 버튼은 `eventData.Use()` 또는 포인터 영역 검사로 propagation 차단 | `#1회검증` |

---

## 항목별 노트

## 37. Claude Code 듀얼 모델 라우팅 / settings.local.json env 우선순위 함정

_`settings.local.json`의 `env` 블록은 셸 $PROFILE env보다 우선 주입된다 — DeepSeek 기본 + Claude opt-in 구성에서 이 블록이 잘못 남아있으면 모든 Claude Code 세션이 덮어씌워진다._

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

**추가 발견 (2026-05-29) — LiteLLM 프록시 필수 + 함정 3종**

Claude Code는 Anthropic SDK로 `/v1/messages` 엔드포인트에 요청하며 `role: system` 메시지를 포함한다. DeepSeek의 Anthropic 호환 엔드포인트(`api.deepseek.com/anthropic`)는 이를 거부(400). LiteLLM 프록시를 중간에 두어 Anthropic→OpenAI 포맷 변환 필수.

LiteLLM config 3종 함정:
1. **`api_base` 누락** → LiteLLM이 OpenAI로 라우팅, `deepseek-v4-pro` 모델 없다고 404
2. **`openai/` 프리픽스** → `/v1/messages` 라우팅 실패. `deepseek/` 프리픽스 필수
3. **`drop_params` 누락** → Anthropic 전용 파라미터가 DeepSeek로 넘어가 에러

정상 작동 config:
```yaml
litellm_params:
  model: deepseek/deepseek-v4-pro   # openai/ 아닌 deepseek/ 필수
  api_base: https://api.deepseek.com/v1
  api_key: sk-...
litellm_settings:
  drop_params: true
```

---

## 38. Caveman — LLM 출력 토큰 압축 skill

_AI 코딩 에이전트 응답을 "원시인 스타일"로 압축해 출력 토큰 ~65% 절감. SKILL.md 1파일이면 충분, SessionStart hook으로 자동 활성화도 가능._

**출처/맥락**
- 출처: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) 오픈소스 / 유튜브 소개 영상 (2026-05-25 발견)
- 원리: `SKILL.md` frontmatter + 압축 규칙 본문 → Claude Code 스킬로 로드 → 이후 응답에 규칙 적용
- 핵심 효과: 출력 토큰 ~65% 절감 (벤치마크 기준 최대 87%), 컨텍스트 성장 속도 감소로 입력 토큰도 간접 절감
- 논문 근거: 2026-03 논문 — LLM에 짧게 답하도록 강제 시 정확도 오히려 상승 (말 늘리다 논리 꼬이는 현상 방지)

**구조 / 채택 방식**

| 컴포넌트 | 역할 | 채택 여부 |
|----------|------|----------|
| `/caveman` SKILL.md | 압축 모드 opt-in (lite/full/ultra 3단계) | ✅ CasualStrategy |
| `/caveman-compress` SKILL.md | CLAUDE.md 등 입력 파일 영구 압축 (Python 없이 Claude 세션 직접) | ✅ CasualStrategy |
| SessionStart hook | 매 세션 자동 주입 (깜빡 방지 + 컨텍스트 압축 후 재주입) | ✅ CasualStrategy |
| Stats 추적 (Node.js) | 절감 토큰량 누적 시각화 | ❌ 불채택 (복잡도 대비 가치 낮음) |
| Wenyan 한자 모드 | 한자 문언문으로 극한 압축 | ❌ 불채택 (한국어 프로젝트 불필요) |

**자동 주입 vs 수동 /caveman 토큰 차이**
- 차이 없음. 둘 다 동일한 SKILL.md 내용(~500토큰)을 컨텍스트에 추가.
- SessionStart의 가치는 토큰이 아닌 **신뢰성** — 깜빡 방지 + 컨텍스트 압축 후 drift 방지.
- 절감 본체는 출력 토큰 감소. 평균 응답 500토큰 기준 약 325토큰/턴 절감 → SKILL.md 비용 2턴 이내 회수.

**적용 가능성**
- Claude Code, Cursor, Windsurf, Cline, Copilot 등 40+ 에이전트 지원 (원본 도구 기준)
- Claude Code 한정: `.claude/skills/caveman/SKILL.md` 하나로 충분. Node.js 불필요.
- `caveman-compress`: CLAUDE.md / MEMORY.md 등 매 세션 로드되는 대용량 자연어 파일에 효과 최대. 코드 파일(.cs/.json 등)은 압축 대상 아님.
- karpathy 원칙 2(사용자 자율) 정합: opt-in(/caveman) 또는 session-scoped 자동(SessionStart). 강제 차단 없음.