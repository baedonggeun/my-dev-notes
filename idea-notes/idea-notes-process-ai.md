# 아이디어 — 프로세스·AI 도구

> 상위 노트: [[idea-notes]] (전체 인덱스 디스패처)
> 다루는 축: AI 워크플로우·도구·메타 프로세스 (Claude Code, 모델 라우팅, plan 시스템 등)
> 다루지 않는 축: 아이디어 — 아키텍처·패턴 / 아이디어 — Unity 엔진·렌더링 / 아이디어 — 게임 UX

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
- `#프로세스` `#관찰` `#디자인원리` `#패턴`

### 출처
- `#자체관찰` `#논문` `#컨퍼런스`


---


# 인덱스

| # | 아이디어명 | 분야 | 한 줄 요약 | 상태 |
|---|----------|------|----------|------|
| 36 | 자식 ADR이 부모 ADR 사전 hook 위탁 (계층 plan 협업 패턴) | `#패턴` `#프로세스` `#디자인원리` | 부모 plan/ADR이 향후 자식 plan/ADR에서 추가될 의존을 알면서 인프라를 사전 제공할 때 — **시그니처 hook + `_ = unused;` 자리표시 + 주석 명시**로 자식 plan 진입 비용을 줄이고 코드 정합 보장. 예: 부모 ADR이 `Calculator.Compute(int slotIdx, ...)` 시그니처에 `slotIdx` 인자를 추가하면서 본문에 `_ = slotIdx; // 후속 plan-X에서 slot0 합산 시 사용` 주석 hook을 남김 → 자식 plan은 이 인자를 활용해 1줄 추가만으로 결합 완료, Calculator 시그니처 변경(부모 ADR 짝 갱신) 불필요. 또한 부모 ADR §의존 필드 표에 자식이 추가할 필드 행을 미리 마련하거나 enum source(`InvalidationSource.Usable`)를 사전 정의. 적용 가능성: 다중 plan 계층으로 도메인을 점진 확장하는 모든 협업 환경. 트레이드오프: 부모 ADR이 자식의 구체 사항을 미리 알아야 한다는 결합 — 자식 plan 폐기 시 hook이 dead code로 잔존. 함정: (a) hook이 너무 모호하면 자식 plan 작성자가 의도 못 읽음 → 주석에 자식 plan 파일명 명시, (b) 시간 격차가 길면 hook이 잊혀짐 → ADR `Future Work` 섹션에 명시. 사례: CasualStrategy weapon-runtime-spec ADR §D-2 → slot-enhancement-lifecycle ADR 1줄 결합 (2026-05-21) | `#1회검증` |
| 37 | Claude Code 듀얼 모델 라우팅 / settings.local.json env 우선순위 함정 | `#프로세스` `#관찰` | `settings.local.json` `env` 블록이 셸 $PROFILE env보다 우선 주입됨 → DeepSeek 기본 + Claude opt-in 구성에서 이 블록이 잘못 남아있으면 모든 세션이 덮어씌워짐. 해결: 블록 삭제 대신 DeepSeek/Claude 값을 명시적으로 기록, toggle 스크립트로 전환 | `#1회검증` |
| 38 | Caveman — LLM 출력 토큰 압축 skill | `#프로세스` `#관찰` | AI 코딩 에이전트 응답을 "원시인 스타일"로 압축해 출력 토큰 ~65% 절감. SKILL.md 1파일로 /caveman opt-in 또는 SessionStart hook으로 자동 활성화. caveman-compress로 CLAUDE.md 등 입력 파일도 영구 압축 가능 | `#1회검증` |
| 39 | 전 Tier plan-first (T1~T4 plan 승인 대기) | `#프로세스` `#디자인원리` `#관찰` | AI 코딩에서 DeepSeek 등 외부 구현자 handoff를 위해 T1/T2 단순 작업도 plan 먼저 작성 후 사용자 승인 대기. 외부 구현자가 읽고 질문 없이 구현 가능한 수준의 상세도 강제 | `#1회검증` |

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
