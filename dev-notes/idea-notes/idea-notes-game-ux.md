# 아이디어 — 게임 UX

> 상위 노트: [[idea-notes]] (전체 인덱스 디스패처)
> 다루는 축: 게임 UI·UX 설계 패턴 (인터랙션 흐름·제스처·연출 UX)
> 다루지 않는 축: 아이디어 — 아키텍처·패턴 / 아이디어 — Unity 엔진·렌더링 / 아이디어 — 프로세스·AI 도구

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
- `#게임UI` `#패턴` `#디자인원리`

### 출처
- `#자체관찰` `#타게임분석`


---


# 인덱스

| # | 아이디어명 | 분야 | 한 줄 요약 | 상태 |
|---|----------|------|----------|------|
| 41 | Hover Tooltip 내 Action Button (gold 소비 강화) | `#패턴` `#게임UI` `#디자인원리` | 아이템 hover tooltip을 단순 정보 표시를 넘어 Action 엔트리포인트로 활용 — 툴팁 안에 Button 배치 + static event → Manager 핸들링 → gold 차감 → slot 갱신. 드래그-겹치기(같은 아이템 투입해서 강화)를 UI 툴팁 내 1-click button으로 대체. 필수 조건: (a) static event로 Manager 요청 (Tooltip 컴포넌트가 Manager 직접 mutation 금지, rules.md §1 금지 사항), (b) click 직후 TooltipManager.Hide() 자동 호출 UI 클린업, (c) gold 부족 시 버튼 interactable=false (disabled color), MAX 도달 시 텍스트 "MAX" 전환. 적용 가능성: hover 시 추가 Action이 필요한 게임 시스템 — 인벤토리 강화, 소모품 사용, 아이템 분해, 캐릭터 귀속/해제, 장비합성 미리보기 "합성 가능" 뱃지 등을 툴팁에 통합. 트레이드오프: 드래그-겹치기(2회 Drag) → click(1회) 상호작용 축소, 버튼이 있는 툴팁은 hover 유지 시 click 가능 영역이 추가돼 PointerExit 타이밍 관리 복잡 → EventTrigger 포인터 델리게이트에 cancel/freeze 타이머 유지. 함정: (a) 툴팁 보통 Destroy 직전까지 PointerExit race → enhanceButton.onClick과 TooltipManager.Hide 타이밍 충돌 (클릭 후 즉시 Hide면 click 핸들링 전에 툴팁 사라짐). 해결: click handler에서 먼저 event 발화 + 그 후 Hide(), (b) 여러 Action을 같은 툴팁에 두면 버튼 영역 혼잡 → 1 Action per tooltip 유지 권장, (c) Builder가 툴팁 프리팹과 동시에 버튼 위치/색상/크기 결정해야 해서 툴팁 빌더 코드 복잡 소폭 증가. 사례: CasualStrategy CombinedItemTooltipController.enhanceButton + OnEnhanceRequested event (2026-06-05) | `#1회검증` |
| 42 | Graceful Multi-Pull Degradation (여유분만큼 뽑기) | `#게임UI` `#디자인원리` | X회 일괄 뽑기에서 티켓 부족 시 보유량만큼만 뽑기 제공. reject 대신 부분 허용 → 마찰 감소. 버튼 텍스트 "10회(3장)" 동적 표시 결합 권장. 보유량 ≥ 1일 때만 활성화 | `#1회검증` |
| 43 | Global Dismiss Gesture (어디서든 닫기) | `#패턴` `#게임UI` `#디자인원리` | 열린 플로팅 UI(툴팁/드롭다운)를 전역 InputHandler/Manager가 제스처(우클릭/ESC) 감지 후 닫기 — UI 자체가 닫힘 트리거를 모름. 내부 버튼은 `eventData.Use()` 또는 포인터 영역 검사로 propagation 차단 | `#1회검증` |

---

## 항목별 노트
