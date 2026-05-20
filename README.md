# my-dev-notes

평생 사용하는 개발 노트 모음. 프로젝트와 독립적으로 누적되는 패턴/기법/언어/엔진 지식.

작성 시작: 2026-05-15
도구: Obsidian (wikilink 자동 처리) + git
원격: github.com/baedonggeun/my-dev-notes (private)
첫 도출 프로젝트: [CasualStrategy](https://github.com/baedonggeun/CasualStrategy) — `docs/decisions/harness/cross-repo-knowledge.md` ADR

---

## 노트 구조 (9개)

### 검증된 패턴 (8개)
| 노트 | 다루는 축 | 적용 범위 |
|------|----------|----------|
| [design-pattern-notes](design-pattern-notes.md) | 코드 구조 패턴 (GoF + 아키텍처). 재사용 가능한 *관계*의 추상화 | OOP/FP 언어 독립 |
| [software-principle-notes](software-principle-notes.md) | 일반 소프트웨어 개발 원칙·휴리스틱·해석. 코드 *형태*가 아닌 *판단 기준* | 언어/엔진/도메인 완전 독립 |
| [math-algorithm-notes](math-algorithm-notes.md) | 게임에 자주 쓰는 수학 빌딩블록과 알고리즘 | 언어/엔진 완전 독립 |
| [game-technique-notes](game-technique-notes.md) | 게임 *기능*별 구현 기법. "어떻게 묵직한 점프를 만드는가?" | 개념 독립, 구현은 게임엔진 일반 |
| [game-design-notes](game-design-notes.md) | 디자인 도메인 원리 — 페이싱, 난이도, 피드백 루프, 게임필 | 엔진/언어/장르 독립 |
| [game-misc-notes](game-misc-notes.md) | 단편 트릭/가드/캐시 — 패턴이라기엔 작고 API라기엔 응용된 단편 | 다수 게임엔진/Unity 종속 |
| [unity-feature-notes](unity-feature-notes.md) | Unity 빌트인 API / 패키지 / 에디터 기능 카탈로그 | Unity 전용 (의도적) |
| [csharp-syntax-notes](csharp-syntax-notes.md) | C# 키워드/연산자/문법 cheatsheet | C# 전 버전 |

### 인박스 (1개)
| 노트 | 다루는 축 | 적용 범위 |
|------|----------|----------|
| [idea-notes](idea-notes.md) | 미구현 아이디어 / 관찰한 기법 / 학습한 개념 — *검증 전* | 전 영역, 승격 시 위 7개 중 하나로 이주 |

각 노트 상단 메타 헤더에 다루는 축 / 다루지 않는 축 / 관련 노트 / 평생 노트 정책이 명시되어 있다.

---

## 운영 룰

### 등재 트리거
- **두 번째 만남** — 같은 패턴을 두 번 마주치면 인덱스 한 줄 추가. 한 번에 풀노트 작성하지 않음
- **두 번째 회상 실패** — 작성한 인덱스를 다시 봐도 "왜 그랬지?"가 떠오르지 않으면 풀노트로 승격
- **프로젝트 종료 시** — lessons learned 일괄 통합
- **idea-notes 예외** — 인박스이므로 한 번 만남도 등재 OK. 단, 7개 본 노트로 승격하려면 2개 이상 프로젝트 검증 필요
- **능동 적용 룰** — 7개 본 노트의 "두 번째 만남" 트리거 미달인 portable 후보는 idea-notes 인덱스에 없으면 1줄 등재. 1회성 관찰을 buried 시키지 않고 인박스에 안전 보관 → 추후 두 번째 만남 시 본 노트로 승격 (CasualStrategy `/check-done` 통합과 동일 의도)

### 인덱스 표 = SOT
모든 노트의 인덱스 표가 단일 진실의 원천. 풀노트는 항목 일부만 작성.

### 풀노트 작성 기준 (둘 이상 해당 시)
- 코드만 봐선 "왜 이렇게 했는지" 안 보이는 정성적 이유가 있다
- 다른 프로젝트/맥락에서도 재사용 가능한 일반 원리다
- 자주 잊는 함정/엣지케이스가 있다
- 응용 사례가 3개 이상이다

csharp-syntax-notes는 예외 — 함정 있는 항목만 풀노트.

### 6블록 풀노트 템플릿
```markdown
## N. 항목명

**한 줄 요약**
{공식 or 핵심 아이디어 1줄}

**설명**
{왜, 언제, 어떤 문제를 푸는가}

**구현** (game-design은 생략)
{언어 독립 의사코드 + 엔진별 빌트인 부록}

**주의점** (선택)
{함정/엣지케이스}

**메타**
- 종속성: {`#언어독립` / `#Unity전용` 등}
- 첫 도출: {프로젝트명 + 날짜}
- 태그: {태그들}
```

### 항목 번호 정책
- **추가 전용 (renumber 금지)** — 교차 참조 안정성 보장
- 삭제는 strike-through (`~~삭제됨~~`) 또는 "이주" 표시
- 새 항목은 `max(번호)+1`

### 분류 임계치
- 노트 내 카테고리 항목 3개 누적 → 분리 검토
- 같은 항목이 3 프로젝트에서 반복 → 다른 노트로 승격
- 새 언어/엔진 종속 항목 3개 누적 → 별도 노트 신설

### 종속성 태그
- `#언어독립` `#엔진독립` — 가장 portable
- `#OOP` `#FP` `#제네릭` — 패러다임 종속
- `#게임엔진일반` — 라이프사이클/시간 시스템 가정
- `#Unity전용` `#오디오엔진` — 특정 엔진 종속
- `#C#7` ~ `#C#12` — 문법 버전

---

## 워크플로우

### 하네스 통합 (CasualStrategy 기준)
- `/check-done` T2 메뉴 `[7]` / T3 `[11]` / T4 `[8]`에 **my-dev-notes 갱신 점검** 항목 통합
- 하네스 docs 갱신 시점에 portable 패턴이 노트로 자연 흐름
- 다른 프로젝트로 카피 시: 본 repo 경로(`d:\git_repository\my-dev-notes\`)가 하드코딩되어 있으므로 `/check-done` 스킬 수정 필요

### 새 프로젝트 시작 시
1. 새 프로젝트 폴더 생성
2. 이 repo도 IDE에서 함께 열기 (또는 Obsidian vault로 열기)
3. 작업 중 패턴 발견 → 즉시 인덱스에 등재
4. "첫 도출" 메타에 새 프로젝트명 추가 (기존 항목 재발견 시)
5. 프로젝트 종료 시 노트 갱신 + commit

### 분기/연 단위 리뷰
- 인덱스 표 훑어보기
- outdated 항목 정리 (실제 사용 안 하는 패턴은 삭제 후보)
- 분리 임계치 도달한 카테고리 별도 노트로 분리
- 새 노트가 생겼다면 메타 헤더의 "관련 노트" 갱신

---

## 도구

### Obsidian
- 본 폴더를 vault로 지정 (Open folder as vault)
- 이미 적용된 wikilink (`[[note-name]]`)가 자동으로 백링크/그래프 처리됨
- 추천 플러그인: Tag Wrangler, Outliner, Templater
- `.obsidian/workspace*.json`은 .gitignore에 포함 (per-user state)

### IDE
- VS Code: Markdown Preview Enhanced
- 검색: Obsidian의 전역 검색 또는 `git grep`

### Git
- 평생 노트는 commit이 갱신 기록 — `git log`가 회상 도구
- 큰 재구성 시 commit 메시지에 "이주/승격/분리" 명시
- 분기에 1회 force push 없이 push (히스토리 보존)

---

## 첫 도출 기록

- **CasualStrategy** (2026-05-15) — Unity 6 캐주얼 전략 게임. 7개 노트 최초 정립. 약 100+ 인덱스 항목, 풀노트 3개(Lerp / Asymmetric Jump / Coyote Time / Hold-to-Repeat)
- **복수 프로젝트** (구일자 미상, 2026-05-15에 회상 등재) — 액션 2D 추정. 본 노트 누락 항목 9개 등재: DefaultExecutionOrder, Physics2D Layer Matrix, Physics2D NonAlloc, Input System (New), Parallax Scrolling, DI 패턴, Domain-Scoped Injection Interface, Streaming Pattern, Animator Layer + Avatar Mask. Rewind 1건은 구현 함정(Animator/물리/AI 상태 동기화 어려움)으로 미등재 — 실제 채택 시점에 등재
- **idea-notes 신설** (2026-05-16) — 미구현 아이디어/관찰 기법 인박스. 3건 등재: ① 결정론적 시간축 양자 예측(달력 SOT 시뮬레이션, CasualStrategy 도출), ② Rewind 시스템(복수 프로젝트에서 보류, `#미구현`), ③ Sequence ↔ Data 흐름 분리(CasualStrategy G-030 기반, `#1회검증`)
- **software-principle-notes 신설** (2026-05-21) — CasualStrategy 4원칙(Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven) 정착 후 일반 소프트웨어 원칙으로 추출. 47개 인덱스(카테고리 A~G), 풀노트 9개(#1 YAGNI / #3 DRY / #6 Boy Scout Rule **채택 안 함** / #7 AHA / #9 SRP / #32 SLAP / #38 Make Illegal States Unrepresentable / #42 Hyrum's Law / #43 Postel's Law). idea-notes 인박스 #21~#27 동시 등재(Mechanical Sympathy / Conway's Law / Brooks's Law / Wirth's Law / AAA / F.I.R.S.T. / Given-When-Then — 모두 `#본인적용미정`). 본인 입장 표기 룰: 라벨(`#수용` 등) 금지, *왜 + 어디 적용 / 대안 / 오용 지점* 1줄
