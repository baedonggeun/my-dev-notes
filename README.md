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

### 파일 구조 (2단 분리)

각 노트는 `# 인덱스` → `---` → `# 풀노트` 2단 구조를 따른다.

- **# 인덱스**: 인덱스 표 + 태그 목록 + SOT 선언
- **# 풀노트**: 모든 항목 상세 기술
- 풀노트 항목 제목의 번호 범위: 단일 `N.` / 연속 `N~M.` / 비연속 `N, M, P.`

### 등재 트리거
- **두 번째 만남** — 같은 패턴을 두 번 마주치면 인덱스 한 줄 추가 + 즉시 풀노트 작성
- **두 번째 회상 실패** — 작성한 인덱스를 다시 봐도 "왜 그랬지?"가 떠오르지 않으면 풀노트로 승격
- **프로젝트 종료 시** — lessons learned 일괄 통합
- **idea-notes 예외** — 인박스이므로 한 번 만남도 등재 OK. 단, 7개 본 노트로 승격하려면 2개 이상 프로젝트 검증 필요
- **능동 적용 룰** — 7개 본 노트의 "두 번째 만남" 트리거 미달인 portable 후보는 idea-notes 인덱스에 없으면 1줄 등재. 1회성 관찰을 buried 시키지 않고 인박스에 안전 보관 → 추후 두 번째 만남 시 본 노트로 승격 (CasualStrategy `/check-done` 통합과 동일 의도)

### 인덱스 표 = SOT
모든 노트의 인덱스 표가 단일 진실의 원천. 풀노트는 모든 항목 작성.

### 노트별 풀노트 템플릿

공통 메타 블록 (모든 노트 마지막에 동일):
```
**메타**
- 종속성: {`#언어독립` / `#Unity전용` 등}
- 첫 도출: {프로젝트명 + 날짜}
- 태그: {태그들}
```

**design-pattern-notes** — 유사 패턴 비교표 + 정의·호출 양쪽 코드
```
## N. 패턴명

**한 줄 요약** {패턴이 해결하는 문제 1줄}

**설명** {왜 이 패턴인지. 유사 패턴과 비교표}

**구현** {의사코드/C# — 정의 + 호출 양쪽}

**주의점** {흔한 오용, 안티패턴}

**메타**
```

**software-principle-notes** — 본인 해석 + 적용 경계 (코드 최소)
```
## N. 원칙명

**한 줄 요약** {원칙 정의 1줄}

**왜 본인이 이렇게 다루는가** {채택·조건·기각의 실질 근거 — 라벨 아닌 본문}

**적용 사례 / 비적용 영역** {어디서 적용, 어디서 의도적으로 안 적용}

**오용 사례 / 반대 원칙** (선택) {함정, 반대 원칙과의 관계}

**메타**
```

**math-algorithm-notes** — 수식 + 의사코드 + 경계값·정밀도 주의점
```
## N. 알고리즘/공식명

**한 줄 요약** {수식 포함 핵심 1줄}

**설명** {왜 이 수식인지, 어떤 문제를 푸는가}

**구현** {언어독립 의사코드 + 엔진별 빌트인 부록}

**주의점** {0·∞ 경계값, 수치 정밀도, 흔한 실수}

**메타**
```

**game-technique-notes** — 구현 의사코드 + 파라미터 권장값
```
## N. 기법명

**한 줄 요약** {기법의 핵심 효과 1줄}

**설명** {왜 이 기법인지, 어떤 체감/문제를 해결하는가}

**구현** {의사코드 + 파라미터 권장값 포함}

**주의점** {구현 함정, 튜닝 주의사항}

**메타**
```

**game-design-notes** — 플레이어 경험 관점 + 대표 게임 사례 (구현 블록 없음)
```
## N. 원리명

**한 줄 요약** {디자인 원리 1줄}

**설명** {왜 이 원리가 필요한가 — 플레이어 경험 관점}

**대표 사례** {어떤 게임이 이 원리를 어떻게 구현했는가}

**메타**
```

**game-misc-notes** — 최소 실제 코드 + 언제/대안 (간결하게)
```
## N. 항목명

**한 줄 요약** {트릭/가드의 핵심}

**코드** {최소한의 실제 구현 코드}

**언제 / 대안** {어떤 상황, 대안과의 비교}

**주의점** (선택)

**메타**
```

**unity-feature-notes** — Inspector 설정 + C# 코드 + Unity 특유 함정
```
## N. 기능명

**한 줄 요약** {Unity 기능의 핵심}

**설명 + 구현** {Inspector 설정 순서 + C# 코드 (정의+호출 양쪽)}

**주의점** {Unity 특유의 직렬화·라이프사이클·도메인 리로드 함정}

**메타**
```

**csharp-syntax-notes** — mental model + 비교표 + 정의·호출 예시 + 함정 이유
```
## N. 키워드/문법명  (단일 N. / 연속 N~M. / 비연속 N, M, P.)

{핵심 개념 — mental model 1-2줄}

**비교** (있을 경우) {비교표}

**용법** {정의 + 호출 양쪽 예시}

**함정** {왜 함정인지 이유 포함}

**대표 용도** {한 줄 요약}
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
