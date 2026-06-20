# 아이디어 — 법칙·원칙·테스트

> 상위 노트: [[idea-notes]] (전체 인덱스 디스패처)
> 다루는 축: 소프트웨어 법칙·원칙·TDD
> 다루지 않는 축: 아이디어 — 아키텍처·패턴 / 아이디어 — Unity·도구·메타

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
| 21 | Mechanical Sympathy (Martin Thompson) | `#패턴` `#성능` `#관찰` | "하드웨어 동작 방식과 호흡 맞추기" — 캐시 라인, branch prediction, false sharing 등을 인지한 코드. CasualStrategy(캐주얼 전략)는 본격 적용 영역 없음. 부분 적용: NonAlloc Physics2D / 풀링뿐. 차후 data-oriented design 또는 Unity DOTS 도입 시 정식 등재 후보. 출처: LMAX Disruptor 구현자, "Mechanical Sympathy" 블로그/컨퍼런스 강연 | `#본인적용미정` |
| 22 | Conway's Law (Mel Conway, 1968) | `#아키텍처` `#팀워크` `#관찰` | "소프트웨어 구조는 그것을 설계한 조직의 통신 구조를 반영한다". 1인 개발이라 직접 적용 N/A. 다만 인간+AI(Claude) 협업 구조가 `docs/decisions/`(인간 SOT) / `.claude/skills/agents/`(AI 호출 구조) / `CLAUDE.md`(공통 컨텍스트) 분리에 반영 가능성 관찰. 차후 *다인 협업* 또는 *AI 협업 구조 변경* 시 검증 | `#본인적용미정` |
| 23 | Brooks's Law (Fred Brooks "Mythical Man-Month", 1975) | `#팀워크` `#프로세스` `#관찰` | "늦은 소프트웨어 프로젝트에 인력을 추가하면 더 늦어진다". 1인 + AI 협업이라 직접 적용 N/A. 응용: Plan followup 짝 룰("가정 차이/누락은 즉시 수정 X, 누적 후 일괄")의 동기 — 즉시 수정 = 작업 큐 폭발 + 컨텍스트 전환 비용. 차후 다인 협업 시 정식 검증 | `#본인적용미정` |
| 24 | Wirth's Law (Niklaus Wirth, 1995) | `#성능` `#관찰` | "소프트웨어가 하드웨어보다 빨리 느려진다". Unity 6 + URP가 본 법칙의 사례 — 엔진 기능 추가가 GPU 성능 압박. CasualStrategy(캐주얼 전략)는 GPU 여유라 묵인. 차후 모바일 빌드 또는 저사양 타겟 시 정식 적용 검토. 출처: "A Plea for Lean Software" 논문 | `#본인적용미정` |
| 25 | AAA (Arrange, Act, Assert) | `#테스팅` `#패턴` | 테스트 3구조: 사전 상태 셋업 / 동작 호출 / 결과 검증. CasualStrategy 자동화 테스트 미운영(Unity Test Framework 도입 안 함). 차후 도입 시 정식 등재 — `software-principle-notes` 신규 카테고리 H 신설 후보 | `#본인적용미정` |
| 26 | F.I.R.S.T. (Fast/Independent/Repeatable/Self-validating/Timely) | `#테스팅` `#패턴` | 단위 테스트가 갖춰야 할 5속성. Robert C. Martin "Clean Code" 출처. CasualStrategy 자동화 테스트 미운영. 차후 테스트 도입 시 AAA(항목 25), Given-When-Then(항목 27)과 함께 카테고리 H 신설 | `#본인적용미정` |
| 27 | Given-When-Then (BDD) | `#테스팅` `#패턴` | BDD 시나리오 구조: 사전 조건 / 동작 / 기대 결과. Daniel Terhorst-North BDD 출처. CasualStrategy 자동화 테스트 미운영. AAA(항목 25)의 자연어 버전 — 도입 시 둘 중 1개 선택 또는 영역별 분리 | `#본인적용미정` |

---

## 항목별 노트
