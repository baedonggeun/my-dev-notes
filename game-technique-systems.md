# 게임 기법 노트 — 시스템·아키텍처

> 상위 노트: [[game-technique-notes]] (전체 인덱스 디스패처)
> 다루는 축: 슬롯 확장·큐 흐름 제어·세이브·오디오·잡기술
> 다루지 않는 축: [[game-technique-mechanics|게임필·시각 기법]] / [[game-technique-combat|전투·수치·확률]]

---


## 태그 목록

### 카테고리 (무엇)
- `#이동` `#점프` `#카메라` `#입력` `#충돌`
- `#전투` `#데미지` `#난수` `#가챠` `#밸런싱`
- `#오디오` `#UI` `#피드백` `#애니메이션` `#VFX`
- `#슬롯` `#시너지` `#곡선` `#튜토리얼` `#시퀀스`

### 장르 (어디)
- `항목 2D` `항목 3D` `#플랫포머` `#액션` `#전략` `#로그라이크` `#캐주얼`

### 효과/의도 (왜)
- `#게임필` `#응답성` `#관용성` `#예측가능성` `#몰입` `#결정론`

### 구현 매체 (어떻게)
- `#물리엔진` `#커스텀적분` `#보간` `#콜백` `#게이팅`

---


# 인덱스

| # | 기능 | 기법 이름 | 한 줄 요약 | 종속성 |
|---|------|----------|----------|--------|
| 6 | 볼륨 슬라이더 | AudioMixer Linear→dB 지각 변환 | 선형 슬라이더를 로그 dB로 변환해 청각 지각에 일치 | `#오디오엔진` |
| 7 | 슬롯 확장 시스템 | Unlocked vs Max 게이팅 | 활성/최대 슬롯을 분리해 점진적 콘텐츠 확장 | `#언어독립` |
| 8 | 튜토리얼 결정론 | 고정 큐 주입으로 랜덤 대체 | RNG 호출 지점에 사전 정의 큐를 주입해 결정론 보장 | `#언어독립` |
| 9 | 시퀀스 연결 | onComplete 콜백으로 호출자가 전이 결정 | 시퀀스가 종료를 알리되 다음 전이는 호출자가 결정 | `#OOP` `#FP` `#언어독립` |
| 12 | 순차 큐 + 즉시 우회 팝업 | Sequential Queue + Concurrent Bypass | 애니메이션 효과를 Queue로 순차 재생하되 동시 표시가 의도인 효과(힐/쉴드)는 별도 SpawnInstant 진입점으로 큐 우회 — 데이터 흐름에 WaitForSeconds 재추가 없이 시각 타이밍 분리 | `#게임엔진일반` |
| 17 | 세이브 데이터 직렬화 | 패스워드 세이브 시스템 (Password Save) | 게임 상태를 수치화 + 랜덤 솔트 + 체크섬으로 인코딩해 문자열로 출력 — 배터리 칩 없이 플레이어가 직접 기록·입력하는 아날로그 세이브 방식 | `#언어독립` |
| 18 | 메모리 취약점 익스플로잇 | 임의 코드 실행 (ACE, Arbitrary Code Execution) | 코드·데이터가 동일 RAM에 공존하는 폰노이만 구조의 특성 + 프로그램 카운터 오염으로 데이터 영역이 실행 코드가 됨 — 컨트롤러 입력으로 새 프로그램을 즉석 작성하는 스피드런 기법 | `#언어독립` |

---

# 풀노트

## 6. AudioMixer Linear→dB 지각 변환 (볼륨 슬라이더)

_UI 슬라이더의 선형 값(0~1)을 `dB = 20·log₁₀(linear)` 변환 후 `AudioMixer.SetFloat`에 전달. 슬라이더 50% = 약 -6dB ≈ 인간 귀에 "반쯤 줄었다"는 느낌._

**설명**
`AudioMixer.SetFloat("Volume", linearValue)`에 선형 값(0~1)을 그대로 전달하면 볼륨 조절이 부자연스럽다 — 슬라이더 90%에서 10%까지는 차이가 적게 느껴지다가 마지막 10%에서 급격히 줄어드는 느낌. 인간 청각이 로그 특성이기 때문.

AudioMixer의 볼륨 파라미터는 **dB 단위**. 일반 범위: -80dB (무음) ~ 0dB (원본). dB로 전달하면 슬라이더 절반 = 볼륨 절반의 *지각*을 달성.

**구현**
```csharp
// SoundManager (CasualStrategy 패턴)
public class SoundManager : MonoSingleton<SoundManager>
{
    [SerializeField] private AudioMixer audioMixer;
    private const float MIN_DB = -80f;

    public void SetMasterVolume(float linear)  // linear ∈ [0, 1]
    {
        float db = linear <= 0f ? MIN_DB : Mathf.Log10(linear) * 20f;
        audioMixer.SetFloat("MasterVolume", db);
    }

    public void SetBGMVolume(float linear)
    {
        float db = linear <= 0f ? MIN_DB : Mathf.Log10(linear) * 20f;
        audioMixer.SetFloat("BGMVolume", db);
    }

    public void SetSFXVolume(float linear)
    {
        float db = linear <= 0f ? MIN_DB : Mathf.Log10(linear) * 20f;
        audioMixer.SetFloat("SFXVolume", db);
    }
}
```

AudioMixer 셋업:
1. AudioMixer 에셋 → Master + BGM/SFX 자식 그룹 생성
2. 각 그룹 Volume 파라미터 Expose: Inspector 우클릭 → "Expose to script" → 이름 지정
3. `audioMixer.SetFloat(exposedName, dbValue)` 호출

⚠ **주의점**
- **`Mathf.Log10(0)` = -Infinity** — `linear <= 0f ? MIN_DB : Mathf.Log10(linear) * 20f` 가드 필수. 가드 없으면 AudioMixer 파라미터가 locked 상태가 되어 이후 SetFloat 무시됨 (볼륨 0 → 복구 불가 버그)
- **-80dB가 관행** — AudioMixer Inspector 기본 최솟값. -144dB 등 극단값 전달 시 일부 Unity 버전에서 오동작
- **Exposed Parameter 이름 오타** — `SetFloat("MaterVolume", db)` 같은 오타는 silent fail (false 반환, 예외 없음). const 문자열 상수 관리 권장
- **PlayerPrefs 저장 단위** — 선형(0~1)으로 저장, 로드 시 dB 변환. dB 저장 후 역변환은 -∞ 처리가 복잡
- **GetFloat로 UI 동기화** — 초기화 시 `GetFloat → DBToLinear → slider.value`. `DBToLinear: Mathf.Pow(10f, db / 20f)`


#오디오 #밸런싱 #게임필
> 관련: [[math-algorithm-notes]] 항목 2 Linear↔dB 로그 변환 (수학 기반), [[unity-feature-notes]] 항목 14 AudioMixer, 항목 27 Mathf.Log10 | 종속성: `#Unity전용` (AudioMixer API), 수학 개념은 `#언어독립`

## 7. Unlocked vs Max 게이팅 (슬롯 확장 시스템)

_활성 슬롯 개수(unlocked)와 최대 슬롯 개수(max)를 분리해 점진적 콘텐츠 확장. "N/M 슬롯" UI로 현재 진행도와 잠재력을 동시 표시._

**설명**
플레이어에게 모든 기능을 처음부터 열어주면 압도된다. 반면 계속 잠금만 풀면 "언제 다 열리지?"라는 불안감이 든다. Unlocked/Max 이중 게이팅은 *현재*와 *목표*를 동시에 제시한다.

핵심 개념:
- **Max**: 시스템이 허용하는 절대 상한. 게임 디자인으로 결정 (예: 인벤토리 최대 60칸)
- **Unlocked**: 플레이어가 현재 사용 가능한 수. 게임 진행/재화 소모로 증가
- **Locked**: `Max - Unlocked`. 잠겨 있지만 "언젠가 열 수 있다"는 기대감 제공

게임 대표 사용:
- 인벤토리/가방 슬롯 (Path of Exile, 디아블로 시리즈)
- 유닛 배치 슬롯 (전략 게임 진영 업그레이드)
- 장비 장착 슬롯 (레벨/직업 해금)
- 제작 슬롯 (스토리 진행으로 해금)
- CasualStrategy: 유닛 배치 슬롯 (레벨업 + 재화 소모로 unlock)

**구현**
```csharp
// 슬롯 데이터 구조
[System.Serializable]
public class SlotSystem
{
    public int unlocked;    // 현재 사용 가능 슬롯
    public int max;         // 최대 슬롯

    public bool CanAdd => unlocked > currentCount;
    public bool CanUnlock => unlocked < max;

    public bool TryUnlock()
    {
        if (unlocked >= max) return false;
        unlocked++;
        return true;
    }
}

// UI 표시 (Unlocked vs Max)
// "{current}/{unlocked} (Max: {max})"
// 프로그레스 바: current / unlocked
// 시각적 Lock 표시: hidden slot = 잠김 아이콘
```

경고 주의점:
- Max는 절대 변경 금지(게임 디자인 범위) — 런타임에 Max를 줄이면 저장 데이터와 충돌. Max는 기획 데이터(ScriptableObject)로 고정
- Unlocked 저장 영속성 — PlayerPrefs에 unlocked 값 저장. 버전 업데이트로 Max 증가 시 unlocked은 그대로 (기존 플레이어 불이익 없음)
- UI 표시 규칙 — "5/10"만 보여주면 "앞으로 5개 더?"라는 혼동. "5/8 (Max: 10)" 또는 프로그레스 바 + Max 라벨로 명확히 구분
- 중간 저장(Partial Unlock) 금지 — 슬롯 unlock은 한 번에 1개 단위. "반만 해금"이라는 상태가 없어야 함
- Unlock 비용 증가 곡선 — 후반 슬롯일수록 unlock 비용 증가 (멱함수 곡선, [[math-algorithm-notes]] 항목 4). 곡선 구체적 검증은 시뮬레이션 필수


#슬롯 #게이팅 #게임필
> 관련: [[math-algorithm-notes]] 항목 4 멱함수 곡선 (비용 곡선), [[math-algorithm-notes]] 항목 8 HashSet (시너지 카운팅과 조합) | 종속성: `#언어독립`

## 8. 고정 큐 주입으로 랜덤 대체 (튜토리얼 결정론)

_RNG 호출 지점에 사전 정의된 고정 큐(seed queue)를 주입해 튜토리얼 중 결정론적 결과 보장. 플레이어가 항상 같은 경험을 하도록 제어._

**설명**
랜덤 요소(가챠, 드롭, 크리티컬)가 있는 게임에서 튜토리얼은 "운 나쁜" 시나리오를 방지해야 한다. 첫 가챠가 꽝이면 이탈률 급증. 해결책: 튜토리얼 구간에만 주입 가능한 고정 큐를 RNG 시스템 앞단에 설치.

동작 방식:
1. 보통 때는 진짜 RNG(System.Random, Unity.Random) 사용
2. 튜토리얼 전용 큐를 준비: `[0.05, 0.72, 0.99, ...]` (0.05 = 5% 확률 = UR)
3. RNG 호출 시 큐가 비어있지 않으면 큐에서 꺼내서 반환
4. 튜토리얼 종료 시 큐 비우기

장점:
- 테스트 가능: 특정 큐를 넣으면 항상 같은 결과
- 저장 불필요: 튜토리얼 상태 = 큐 소진 여부
- 기존 RNG 코드 수정 최소화: 한 겹의 추상화만 추가

**구현**
```csharp
public class DeterministicRNG
{
    private Queue<float> _fixedQueue;
    private System.Random _rng;

    public float Next()
    {
        if (_fixedQueue != null && _fixedQueue.Count > 0)
            return _fixedQueue.Dequeue();
        return (float)_rng.NextDouble();
    }

    // 튜토리얼 시작 시 호출
    public void InjectQueue(float[] values)
    {
        _fixedQueue = new Queue<float>(values);
    }

    // 튜토리얼 종료 시 호출
    public void ClearQueue()
    {
        _fixedQueue = null;
    }
}
```

경고 주의점:
- 큐 길이 부족 — 튜토리얼 중 RNG 호출 횟수보다 큐가 짧으면 이후는 진짜 RNG 사용. "우리는 공정합니다"라는 인상을 주려면 큐가 완전히 소진될 때만 진짜 RNG 전환
- 큐 재사용 금지 — 한 번 소진된 큐는 재사용 금지. 튜토리얼 재시작 시 새 큐 필요
- 디버그 전용 큐 — 개발자 메뉴에서 큐 주입 기능 추가하면 버그 재현에 탁월. "이번 플레이 RNG 시드: XXXXX" 로그와 함께 큐 저장
- 확률 값의 범위 — 큐에 저장된 값은 `[0, 1)`. 외부에서 확률 비교 시 일관성 유지. "0.05 미만 = UR" 로직과 동일
- 멀티플레이어/온라인 — 큐 주입은 클라이언트 로컬 전용. 서버 RNG는 주입 불가 (치트 방지). 온라인 튜토리얼은 서버에서 별도 시드 관리


#튜토리얼 #결정론 #테스트 #관용성
> 종속성: `#언어독립`

## 9. onComplete 콜백으로 호출자가 전이 결정 (시퀀스 연결)

_시퀀스(애니메이션, 연출)가 종료를 onComplete 콜백으로 알리되, *다음 시퀀스 선택*은 호출자가 결정. 각 시퀀스는 자기 완료만 책임._

**설명**
게임 시퀀스(공격 연출, 대화, 이벤트)는 여러 단계로 연결된다. 각 단계가 *다음 단계로 무엇을 할지*까지 결정하면 **순환 의존성**(A가 B를 알고, B가 A를 아는)이 발생하고, 수정 시 연쇄 변경이 일어난다.

onComplete 패턴의 핵심 원칙:
1. 각 시퀀스는 자기 완료만 책임 (단일 책임)
2. 완료 시 "끝났다"는 신호만 보냄 (어떤 값/상태와 함께)
3. 호출자(Controller/Manager)가 신호를 받고 다음 시퀀스 결정

```
호출자(Controller)  --시작-->  Sequence A
                                    |
                              (onComplete)
                                    |
호출자(Controller)  <--결과------  A 끝남
호출자(Controller)  --조건 판단-->  Sequence B 또는 C
```

**구현 (CasualStrategy 패턴)**
```csharp
// 시퀀스 인터페이스
public interface ISequence
{
    void Play(Action onComplete);
}

// 호출자: 시퀀스 전이 결정
public class PlayerTurnController
{
    private ISequence _current;

    private void StartTurn()
    {
        PlaySequence(new DrawCardSequence(), OnDrawComplete);
    }

    private void OnDrawComplete()
    {
        if (HasSynergyActivation())
            PlaySequence(new SynergySequence(), OnSynergyComplete);
        else
            PlaySequence(new AttackSequence(), OnAttackComplete);
    }

    private void PlaySequence(ISequence seq, Action onComplete)
    {
        _current = seq;
        _current.Play(onComplete);
    }
}
```

경고 주의점:
- 콜백 중첩 깊이 주의 — 연속된 if-else가 깊어지면 콜백 지옥. 복잡한 상태 기계는 FSM(유한 상태 기계)으로 전환 고려
- Dispose/취소 처리 — 시퀀스 도중 씬 전환/종료 시 onComplete가 호출되지 않을 수 있음. CancellationToken 또는 isActive 플래그 추가
- 콜백 파라미터 오염 — onComplete에 여러 정보를 담고 싶은 유혹. 그 결과 인터페이스 변경 시 연쇄 수정. 최소 정보만 전달하거나 Result 객체로 캡슐화
- 순환 참조 방지 — 시퀀스가 호출자를 직접 알면 onComplete 우회 가능. 인터페이스/델리게이트로 분리
- 유닛 테스트 — 각 시퀀스는 단독 테스트 가능해야 함 (onComplete만 Mock). 호출자 테스트는 Mock 시퀀스로 전이 로직 검증


#시퀀스 #콜백 #OOP #FP
> 종속성: `#언어독립`

## 12. 순차 큐 + 즉시 우회 팝업 (Sequential Queue + Concurrent Bypass)

_애니메이션 효과를 Queue로 순차 재생하되, 동시 표시가 의도인 효과(힐/쉴드)는 별도 SpawnInstant 진입점으로 큐를 우회. 데이터 흐름에 WaitForSeconds 재추가 없이 시각 타이밍 분리._

**설명**
전투 로그 같은 이벤트 스트림을 UI로 표시할 때 기본 설계는 **순차 재생**(Sequential Queue)이다. 공격A -> 공격B -> 힐C 순서로 표시. 그런데 "동시에 처리된 힐 여러 개를 하나씩 순차 재생"하면 5힐에 5초가 걸리는 어색한 UX가 된다.

해결책: 큐를 우회하는 **SpawnInstant** 진입점. 일반 효과는 큐를 경유(순차 + 전환 대기), 동시 표시 효과는 즉시 생성(중첩 허용).

```
데이터 흐름:
  Event Stream
    |-- 효과가 순차 의존? (버프/디버프) --> Queue.Enqueue --> Sequence.Play
    |-- 효과가 동시 표시? (힐/쉴드)   --> SpawnInstant --> 독립적 Popup
```

**구현**
```csharp
// QueueSequence (순차 전용)
public class QueueSequence : MonoBehaviour
{
    private Queue<System.Action> _queue = new();
    private bool _isPlaying;

    public void Enqueue(System.Action effect)  // 전환 대기 필요
    {
        _queue.Enqueue(effect);
        if (!_isPlaying) PlayNext();
    }

    public void SpawnInstant(System.Action effect)  // 우회 - 즉시 실행
    {
        effect?.Invoke();
    }

    private void PlayNext()
    {
        if (_queue.Count == 0) { _isPlaying = false; return; }
        _isPlaying = true;
        var effect = _queue.Dequeue();
        effect?.Invoke();
        // onComplete에서 PlayNext() 호출 (시퀀스가 완료를 알림)
    }
}

// 사용 예
void OnDamage(DamageEvent e)
{
    _queue.Enqueue(() => ShowDamagePopup(e));  // 순차: 공격 순서대로
}

void OnHeal(HealEvent e)
{
    _queue.SpawnInstant(() => ShowHealPopup(e));  // 즉시: 모든 힐 동시 표시
}
```

경고 주의점:
- SpawnInstant 오용 — 모든 이벤트를 SpawnInstant로 처리하면 큐가 무의미해짐. 기준: "이 이펙트가 *순서대로* 보여야 UX에 중요한가?" 아니면 SpawnInstant
- 동시 팝업 겹침 — 힐 10개가 동시에 뜨면 화면이 난잡. SpawnInstant 팝업 위치에 오프셋(스택) 적용. "HIT! x5" 형식의 병합 표시도 고려
- 데이터와 시각의 분리 — 데이터 처리는 이미 완료된 상태. Queue/SpawnInstant는 *시각적 재생*만 제어. 데이터 흐름에 WaitForSeconds 재추가 금지
- Mix 사용 시 주의 — Queue 중인 효과와 SpawnInstant 효과가 같은 위치에 뜨면 순서 혼동. SpawnInstant는 별도 레이어/영역에 표시
- 테스트 — Queue가 비어있을 때 SpawnInstant만 호출되면 isPlaying 플래그 오염 없음 (안전). 반대로 Queue 실행 중 SpawnInstant는 자유롭게 호출 가능 (독립적)


#시퀀스 #UI #게임필
> 종속성: `#게임엔진일반` (UI 시스템 + 애니메이션/시퀀스 시스템)

## 17. 패스워드 세이브 시스템 (Password Save)

_게임 상태를 수치화 + 랜덤 솔트 + 체크섬으로 인코딩해 문자열로 출력, 플레이어가 직접 기록·재입력하는 세이브 방식. 배터리 백업 칩이 없던 1980년대 하드웨어 한계의 소프트웨어 대안._

**개념**
1980년대 게임 카트리지는 배터리가 달린 메모리 칩이 없으면 데이터를 저장할 수 없었다. 악마성 드라큘라 2(Castlevania II)는 비용 문제로 배터리 칩 대신 세이브 데이터를 문자열(비밀번호)로 인코딩해 플레이어가 직접 메모하도록 하는 방식을 택했다.

**인코딩 4단계**

**① 불필요한 정보 생략**
현재 위치 좌표처럼 복원 불필요한 데이터는 아예 저장하지 않는다. 재개 시 캐릭터는 항상 해당 스테이지 시작 지점에서 리스폰. 저장 대상 최소화 → 비밀번호 길이 단축.

**② 게임 상태 수치화**
캐릭터 레벨과 아이템 소지 상태를 단일 숫자로 매핑:
```
레벨 1 + 단검       → 1
레벨 5 + 황금 단검  → 52
...
```
상태 조합표를 숫자 1개로 치환해 데이터 압축.

**③ 랜덤 솔트 추가**
인코딩된 데이터에 무작위 값을 혼합한다. 동일한 게임 상태라도 매번 다른 비밀번호가 출력되게 하기 위함. 복호화 시 솔트를 제거하면 원본 데이터가 복원된다.

**④ 체크섬 추가**
모든 인코딩 데이터의 합계를 비밀번호 끝에 덧붙인다. 복호화 시 수신한 데이터의 합을 재계산해 체크섬과 대조 — 일치하지 않으면 조작된 비밀번호로 판별하고 차단.

```
인코딩:  state_num + salt → data
출력:    data + checksum(data)

복호화:  checksum 검증 → 불일치 시 차단
         → salt 제거 → state 디코딩 → 게임 재개
```

**설계 판단 기준**
- 체크섬은 완벽한 방어가 아니다. 인코딩 알고리즘이 역산되면 유효한 조작 비밀번호 생성이 가능하다 — 당시에도 치트 비밀번호를 공유하는 문화가 존재했다.
- 현대 세이브 파일 무결성 검증(HMAC 해시 서명)은 같은 원리의 발전형이다.

대표 사례:
- **악마성 드라큘라 2 (Castlevania II, 1987)** — 수치화 + 솔트 + 체크섬 조합의 대표 사례
- **메가맨** 시리즈 — 4자리 숫자로 스테이지 클리어 상태 저장
- **당시 게임 문화** — 비밀번호를 공책에 빽빽이 기록하거나 친구 간 공유하는 아날로그 세이브 문화


#난수 #결정론
> 관련: [[game-technique-notes]] 항목 16 의사난수 시드 결정론 (솔트에 쓰이는 난수), [[math-algorithm-notes]] (체크섬 알고리즘) | 종속성: `#언어독립`

## 18. 임의 코드 실행 (ACE, Arbitrary Code Execution)

_코드와 데이터가 동일한 RAM에 공존하는 폰노이만 구조의 특성을 이용해, 프로그램 카운터를 데이터 영역으로 오염시킴으로써 컨트롤러 입력값을 실행 명령어로 만드는 취약점 기법._

**개념**
슈퍼 마리오 화면에서 핑퐁 게임이 구동되거나 젤다에서 다른 게임의 연출이 재현되는 현상들이 존재한다. 외부 프로그램 없이 순정 소프트웨어 + 기기 + 컨트롤러 조작만으로 구현된다. 핵심은 고전 컴퓨터의 메모리 구조다.

**핵심 원리**

**폰노이만 구조 — 코드와 데이터의 동거**
고전 게임은 실행 시 게임 로직(어셈블리 명령어)과 게임 데이터(캐릭터 위치, 그래픽, 컨트롤러 입력값)를 동일한 RAM에 적재한다. CPU 입장에서는 두 가지 모두 동일한 이진수(0과 1)일 뿐이다. CPU는 프로그램 카운터(PC)로 현재 실행 위치를 추적하며 메모리를 순차 실행한다.

**ACE 발생 메커니즘**
```
정상:  PC → [코드 영역] → 순차 실행
ACE:   버그 → PC가 [데이터 영역]으로 점프 → 데이터가 명령어로 실행
```
1. 버그·오버플로로 데이터 영역 값이 덮어쓰여진다.
2. 게임이 이를 감지·차단하지 못하면 PC가 데이터 영역 주소로 이동한다.
3. CPU는 그 이진수를 정상 명령어로 착각하고 실행한다.

**컨트롤러 입력 = 데이터 = 코드**
컨트롤러 버튼 입력값도 게임 데이터의 일종이다. ACE 트리거 직후 정교하게 계산된 패드 입력을 연속 주입하면 CPU가 그 값을 새 명령어로 인식·실행한다 — 컨트롤러로 게임을 즉석 프로그래밍하는 것이 가능해진다.

**저수준 언어의 구조적 취약성**
어셈블리·C·C++은 메모리 주소를 직접 접근·조작한다. 경계 검사를 개발자가 직접 책임지므로 버퍼 오버플로 버그가 발생하기 쉽다. 현대 관리형 언어(Java, C#, Python)는 런타임이 경계를 강제해 ACE를 구조적으로 차단한다.

**극단적 활용 — 로봇 컨트롤러 입력**
여러 컨트롤러를 로봇에 연결해 초고속 정밀 입력을 주입 → 메모리 내부에 완전히 새로운 프로그램을 통째로 작성·실행. 성공 조건: 해당 게임의 메모리 맵과 취약점을 1바이트 오차 없이 완벽히 분석.

대표 사례:
- **슈퍼 마리오** 시리즈 — ACE로 핑퐁 게임·Bad Apple!! 영상 구동
- **젤다의 전설: 시간의 오카리나** — ACE로 야생의 숨결 연출 재현
- **글로벌 스피드런 대회** — ACE를 합법적 기술 카테고리로 운영

**방어 설계 (현대 플랫폼)**
- DEP (Data Execution Prevention): 데이터 영역 코드 실행을 하드웨어 수준에서 차단
- ASLR (Address Space Layout Randomization): 메모리 주소 자체를 무작위화해 PC 오염 대상 예측 불가로 만듦
- 관리형 언어 런타임: 배열 경계·포인터를 자동 검사


#결정론 #입력
> 관련: [[game-technique-notes]] 항목 16 의사난수 시드 결정론 (메모리 예측 가능성 같은 맥락), 항목 17 패스워드 세이브 (같은 저수준 메모리 시대의 기법) | 종속성: `#언어독립`
