# 아이디어 — Unity 엔진·렌더링

> 상위 노트: [[idea-notes]] (전체 인덱스 디스패처)
> 다루는 축: Unity 엔진 함정·인스펙터·렌더링 (엔진 종속 구현 패턴)
> 다루지 않는 축: 아이디어 — 아키텍처·패턴 / 아이디어 — 프로세스·AI 도구 / 아이디어 — 게임 UX

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
- `#Unity전용` `#렌더링` `#성능` `#TMP` `#L10N` `#폴리싱` `#관찰`

### 출처
- `#자체관찰` `#논문` `#컨퍼런스` `#타게임분석` `#서적`


---


# 인덱스

| # | 아이디어명 | 분야 | 한 줄 요약 | 상태 |
|---|----------|------|----------|------|
| 28 | Unity 동적 Canvas 자식 생성 4대 함정 | `#패턴` `#Unity전용` `#렌더링` | 런타임에 Canvas 직속 자식 GameObject를 동적 생성할 때 반드시 지켜야 할 4가지: (1) **RectTransform BEFORE SetParent** — `AddComponent<RectTransform>()` 후 `SetParent(canvas.transform, false)`. 역순이면 Canvas가 자식을 렌더 대상으로 추적 못해 화면 미표시. (2) **Lazy Canvas init** — UIManager가 Instantiate 이후 Canvas에 부모 설정하는 구조(ContentUI 등)라면 Awake 캐싱 불가. lazy `EnsureCanvas()` 를 코루틴/메서드 진입 시점에 호출. (3) **overrideSorting 필수** — 임시 fly card 등 Canvas 자식은 다른 Canvas 자식(sortingOrder > 0)에 가려짐. `AddComponent<Canvas>(); c.overrideSorting=true; c.sortingOrder=rootCanvas.sortingOrder+50`. (4) **InverseTransformPoint** — World→Canvas 좌표 변환은 `WorldToScreenPoint + ScreenPointToLocalPointInRectangle` 조합이 CanvasScaler 스케일 의존 오류 있음. `canvasRT.InverseTransformPoint(worldPos)` 한 줄로 모드 무관 정확 변환. 첫 사례: CasualStrategy GachaSequence fly card (2026-05-26). 연관: Sequence 컴포넌트 내 동적 연출 UI, 피격 팝업, 픽업 연출 등 | `#1회검증` |
| 28 | SFX Voice Limit Pool (Hard Cap) | `#패턴` `#Unity전용` `#성능` | SFX 동시 발화를 단일 AudioSource PlayOneShot 중첩으로 처리하면 (a) 호출 직전 `source.pitch = pitch` 가 진행 중 클립 pitch 덮어씀 + (b) voice steal 로 두 번째 사운드 미발화. `AudioSource[]` 풀(N=8) + 라운드 로빈으로 source 분리 → 각 source 가 자기 클립만 재생 → race 해결. `AcquireSource` 가 비어있는(`!isPlaying`) 우선 선택, 모두 재생 중이면 가장 오래된 source steal — Hard Cap 으로 audio mud(phase cancellation/clipping) 절대 상한 보장. `PlayOneShot` 시그니처 무변경이라 호출지/매핑/채널 라우팅 그대로. mud 체감 사다리: Same-Clip Cooldown(50~100ms dedup) → Priority Eviction(SoundDataSO.priority enum) → pitchRange variation(0.95~1.05) 단계 추가 (YAGNI). 적용 가능성: SFX 시스템이 있는 모든 Unity 프로젝트. 함정: (a) 인스펙터 `sfxPoolSize` 변경 시 기존 source GameObject.AddComponent 후 풀 재생성 정책 필요(현 구현은 풀 길이 변화 감지 시 통째 재할당, 진행 중 클립은 끊김), (b) 풀이 작으면 9번째 호출에서 가장 오래된 SFX 끊김 — 게임 jam scale 비현실적이나 콘텐츠 확장 시 인스펙터 튜닝, (c) 동적 확장 풀(필요 시 source 추가 생성)은 mud 절대 상한 부재 → audio clutter — 기각 권장. 사례: CasualStrategy `AudioManager.sfxSources` (2026-05-21) | `#1회검증` |
| 31 | TMP SDF 폰트 atlas 누락 문자 ⇒ □ 폴백 + 매 렌더 경고 | `#Unity전용` `#TMP` `#L10N` `#폴리싱` | TMP_FontAsset 은 ttf 전체 글리프가 아닌 *atlas 빌드 시점에 포함된 글리프만* 보유 → atlas에 없는 codepoint는 fallback(`U+25A1` □)으로 치환 + 매 렌더마다 `Debug.LogWarning` 발생(콘솔 노이즈). 한국어 메인 폰트(Mulmaru SDF 등)는 한글+기본 ASCII만 포함하고 박스 드로잉(`└ ┌ ─ │ ├` U+2500~257F)은 누락 일반적. L10N 리소스에 트리 들여쓰기/특수 기호 넣기 전에 *기존 폰트 사용 문자 풀*에서 골라 쓰기(예: middle dot `·` U+00B7은 element_desc 류에서 이미 사용 중이라 안전 확인됨). 적용 가능성: TMP 사용하는 모든 Unity 프로젝트 + L10N JSON/string 리소스에 특수 문자 넣는 모든 케이스. 트레이드오프: 폰트 atlas에 글리프 추가는 별도 빌드 작업(atlas 재생성 + 메모리 증가) — 가벼운 들여쓰기 표시는 atlas 확장보다 안전 문자 대체가 비용 낮음. 함정: (a) 에디터 미리보기에서는 fallback 폰트 chain이 작동해 정상 표시되어 보일 수 있음 — 실제 런타임 콘솔에서만 경고 노출, (b) `·` 자체도 SDF 매핑 없는 폰트면 동일 문제 — 신규 폰트 도입 시 사용 중인 모든 특수문자 재검증 필요, (c) atlas regenerate를 미루다 누락 문자가 누적되면 일괄 점검 비용 — 신규 키 추가 시 즉시 검증이 저렴. 사례: CasualStrategy `tooltip_hp_*_fmt` 키의 `└`(U+2514) → `·`(U+00B7) 교체 (2026-05-21) | `#1회검증` |
| 33 | Slot N축 layered vignette + panel-level binder + 동적 sprite | `#패턴` `#Unity전용` `#렌더링` | 슬롯형 UI에 다중 상태(N효과)를 동시 시각화할 때 슬롯당 N Image stretch 정적 배치 + 각 Image color로 상태 식별 + GameObject.SetActive 토글. sprite는 외곽 fade-out white 1장 공유(view Awake에서 코드 동적 생성, 항목 20 procedural sprite 적용) — PNG 자산 0개 + Image.color로 색 분기 + alpha 가산색 중첩 표현. **panel-level binder 1개가 M 슬롯 view 일괄 갱신** (slot-level binder 인스턴스 M개 패턴은 OnEnable M번 발화 + Refresh 분산 + 디버깅 분기 비용 증가, 기존 panel-level binder 사례 0건이면 panel-level 채택). binder는 SerializeField `views[M]` 배열 인스펙터 와이어 — 정렬이 슬롯 인덱스와 1:1 일치 필수 (인스펙터 수동 설정, 빌더 단언 미보유). `raycastTarget=false` 필수 (view AssignSprite에서 코드 1줄 안전망 권장) — vignette이 슬롯 드래그/클릭 가로채지 않게. 적용 가능성: 슬롯형 UI(인벤토리/큐/장비/카드 슬롯)에 N 상태 동시 표시가 필요한 모든 시스템 — 강화/디버프/속성/임시 효과 등 다축 시각화. 트레이드오프: prefab YAML에 슬롯당 N+1 GameObject 추가 작업(5슬롯×4효과 = 20 Image entry, Builder 미사용 시 인스펙터 수동 — Ctrl+D 복제로 일관성 보장). 함정: (a) 5 슬롯의 N Image color 인스펙터 입력 반복 시 alpha 슬라이더 누락 빈발 (항목 34 참조), (b) raycastTarget true로 두면 vignette이 슬롯 인터랙션 가로챔 — 코드 안전망 1줄 추가, (c) Awake에서 sprite 동적 생성 시 OnDestroy cleanup 필수 (Destroy(sprite) + Destroy(texture), UnityEngine.Object GC 미수거). 사례: CasualStrategy `WeaponSlotVignetteView`/`WeaponSlotVignetteUIBinder` 4 효과 (slot0 DmgUp/전 슬롯 DmgUp/속성/Stun, 2026-05-21 slot-enhancement-lifecycle ADR §D-3) | `#1회검증` |
| 34 | 인스펙터 alpha 슬라이더 누락 함정 (multi-Image color 반복 입력) | `#Unity전용` `#관찰` `#폴리싱` | M 슬롯 × N Image 색 입력을 인스펙터에서 반복 작업 시 Color picker의 alpha 슬라이더는 RGB와 별개 입력 필요 — (a) 6자리 hex(`#RRGGBB`) 입력 시 alpha 변경 안 됨 (이전 default 유지, 새 picker는 alpha=0이 default일 수 있음), (b) RGB 슬라이더와 alpha 슬라이더가 분리돼 다수 칸 반복 입력 시 한두 칸 alpha 누락 발생, (c) Color picker 새로 열렸을 때 default alpha가 이전 작업 잔존값으로 표시될 수 있음. 증상: 코드 경로/데이터 모두 정상이고 `GameObject.SetActive(true)` 호출까지 검증되는데도 특정 슬롯의 특정 Image만 runtime 화면에 안 보임 — 디버깅 시 코드부터 의심해서 시간 낭비. 진단: 의심 슬롯의 Image Color picker A 슬라이더 직접 확인 — 0이면 의도값(예: 100/255)으로 수정. 예방: **슬롯 1개 prefab 완성 후 Ctrl+D 복제** (RGBA 일관성 보존, M회 반복 입력 회피). 적용 가능성: 인스펙터에서 다수 UI 요소 색 반복 입력하는 모든 Unity 작업 — vignette 패턴, 멀티 슬롯 grade backround, 카드 색 분류, ability 아이콘 tint 등. 디자이너 인계 시 "alpha 슬라이더 별도 확인" 체크리스트 필수. 함정: 8자리 hex 입력(`#RRGGBBAA`)으로 alpha까지 한 번에 설정 가능하지만 디자이너가 8자리 사용 습관 없으면 무의미. 트레이드오프: 정적 sprite (외부 PNG에 alpha 포함) 사용 시 인스펙터 alpha 무관 — 동적 색 분기가 필요한 경우만 발생. 사례: CasualStrategy WeaponSlot_1/_2 Element Image alpha=0 → Wind 풍속성 버프 vignette 안 보임 (2026-05-21, 항목 33 사례에서 발견) | `#1회검증` |

---

## 항목별 노트
