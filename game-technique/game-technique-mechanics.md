# 게임 기법 노트 — 게임필·시각 기법

> 상위 노트: [[game-technique-notes]] (전체 인덱스 디스패처)
> 다루는 축: 조작감·시각 연출·물리 판정·AI 이동 기법
> 다루지 않는 축: 전투·수치·확률 / 시스템·아키텍처

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
| 1 | 2D 점프 곡선 | Asymmetric Jump (Variable Gravity) | 상승/하강에 서로 다른 중력 → 묵직한 무게감 + 빠른 응답성 | `#게임엔진일반` |
| 10 | 길게 누르기 반복 입력 | Hold-to-Repeat (Initial Delay + Interval) | 버튼을 길게 누르면 초기 딜레이 후 일정 간격으로 onClick 반복 발동 | `#게임엔진일반` |
| 11 | 2D 배경 깊이감 | Parallax Scrolling (속도 차 레이어) | 카메라 이동량에 거리 반비례 계수를 곱해 배경 레이어를 이동시켜 원근감 생성 — 멀수록 적게 이동 | `#게임엔진일반` |
| 19 | VFX 블렌딩 모드 | 가산(Additive) / 곱하기(Multiply) 블렌딩 | 색상값을 더해 밝아지거나(Additive), 곱해 어두워지는(Multiply) 렌더링 합성 — 빛 이펙트는 어두운 배경에서, 그림자는 밝은 배경에서 효과적. 배경 의존성 이해가 핵심 | `#엔진독립` |
| 20 | 시야·충돌 판정 | 레이캐스팅 (Raycasting) | 오브젝트에서 선을 쏘아 충돌을 검사. 몬스터 시야 판정·2D→3D 연출·지형 탐지까지 활용. 거리→시야각→레이 순 3단계 필터로 연산량 절감 | `#엔진독립` |
| 21 | 지형 적응 애니메이션 | 절차적 애니메이션 + 역운동학 (IK) | 발 목적지를 먼저 정하고 관절 각도를 역산(IK). 고정 애니메이션 없이 불규칙 지형에서 자연스러운 보행 실시간 생성 | `#엔진독립` |
| 22 | 길찾기 | 다익스트라 / A* / 플로우 필드 | 지형을 그래프로 변환 후 최단 경로 탐색. 단일 유닛은 A*(휴리스틱으로 탐색 범위 축소), 대량 유닛은 플로우 필드(맵 전체 방향 사전 계산)로 연산량 절감 | `#언어독립` |
| 23 | 픽셀 아트 품질 기법 | 더블픽셀 제거 / 서브픽셀 애니메이션 / 디더링 | 낮은 해상도·제한된 팔레트에서 품질을 높이는 4가지 기법. 선 규칙(더블픽셀·재기), 서브픽셀 애니메이션, 컬러 외곽선, 디더링 | `#언어독립` |

---

# 풀노트

## 1. 비대칭 점프 (Asymmetric Jump)

_상승과 하강에 서로 다른 중력을 적용해 떨어질 때 더 빠르게 낙하시키는 점프 곡선. 묵직한 무게감 + 빠른 응답성._

**설명**
순수 포물선(상승 시간 = 하강 시간)은 물리적으로는 맞지만 체감상 "둥둥 뜨는" 느낌을 준다. 하강 중력을 상승의 1.5~2.5배로 키우면 게임필이 즉시 개선됨.

표준 패키지로 묶이는 보조 기법:
- **Variable Jump Height** — 점프 버튼을 떼면 상승 중력 증가 → "짧은 점프 / 긴 점프"
- **Coyote Time** — 절벽에서 떨어진 후 짧은 윈도우 동안 점프 입력 허용
- **Jump Buffering** — 착지 직전 입력 저장해 착지 즉시 발동
- **Apex Modifier** — 최고점 근처 중력 약화 (체공감 강조)

이 다섯을 모두 적용한 것이 현대 플랫포머의 "점프 관용성 세트". 대표: Super Mario Bros, Celeste, Hollow Knight.

**구현**
```
// 매 프레임
if velocity.y < 0:
    // 하강 — 추가 중력
    velocity.y += gravity * (fallMultiplier - 1) * dt
elif velocity.y > 0 and not jumpHeld:
    // 상승 중 버튼 뗌 — 짧은 점프
    velocity.y += gravity * (lowJumpMultiplier - 1) * dt

// Coyote Time
if grounded:
    coyoteTimer = COYOTE_DURATION
elif coyoteTimer > 0:
    coyoteTimer -= dt

if jumpPressed and coyoteTimer > 0:
    velocity.y = jumpPower
    coyoteTimer = 0
```

권장 파라미터 시작점:
- `fallMultiplier`: 2.0~2.5
- `lowJumpMultiplier`: 2.0
- `coyoteDuration` / `jumpBufferDuration`: 0.1~0.15s

⚠ **주의점**
- 물리 엔진과 충돌 가능 — `velocity` 직접 조작 대신 `Rigidbody.gravityScale` 동적 변경이 더 안전 (Unity)
- `fallMultiplier`가 너무 크면 공중 제어 시간이 짧아져 플랫폼 안착 어려움 — 레벨 디자인과 함께 튜닝
- Coyote/Buffer 타이머를 디버그 UI로 노출하면 튜닝 속도 ↑


#점프 항목 2D #플랫포머 #게임필 #응답성
> 관련: game-design-notes 항목 1 (관용성 디자인 원리), math-algorithm-notes 항목 17 오일러 적분 (매 프레임 `velocity += accel * dt`로 비대칭 중력을 구현하는 수학 빌딩블록) | 종속성: `#게임엔진일반` (개념 독립, 구현은 물리/시간 시스템 필요)

## 10. Hold-to-Repeat 버튼 (길게 누르기 반복 입력)

_버튼을 누르고 있으면 초기 딜레이 후 일정 간격으로 클릭 이벤트가 반복 발동되는 입력 패턴._

**설명**
키보드/게임패드의 "키 반복(key repeat)"과 동일한 원리를 UI 버튼에 적용. 수량 조정 버튼(+/-), 가챠 연속 구매, 슬라이더 미세 조정 등 "여러 번 클릭이 필요한 동작"에서 표준 UX.

핵심 파라미터 2개:
- **Initial Delay (~0.4s)** — 첫 입력과 반복 시작 사이의 간격. 짧으면 짧은 클릭이 반복으로 오인됨, 길면 답답함
- **Repeat Interval (~0.1s)** — 반복 발동 간격. 10Hz 정도가 표준

대표 적용:
- OS 키보드 반복 입력 (Windows/macOS 모두 동일 원리)
- 수량 조정 위젯 (쇼핑 카트 +/-)
- 게임 내 가챠 "10연차" + "롱프레스로 연속 구매"
- 디버그 도구의 값 조정

**구현**
```
// 상태
initialDelay = 0.4s
repeatInterval = 0.1s
repeatRoutine = null

// 입력 이벤트
function OnPointerDown():
    StopRepeat()
    repeatRoutine = StartCoroutine(RepeatLoop())

function OnPointerUp():    StopRepeat()
function OnPointerExit():  StopRepeat()    // 드래그 이탈 시도 정지
function OnDisable():      StopRepeat()    // 비활성화 안전망

// 코루틴
function RepeatLoop():
    yield WaitForSecondsRealtime(initialDelay)
    while button.interactable:
        button.onClick.Invoke()
        yield WaitForSecondsRealtime(repeatInterval)
```

⚠ **주의점**
- **PointerExit 처리 필수** — 누른 채로 버튼 밖으로 드래그하면 OnPointerUp이 발동 안 됨. 드래그 이탈 시점에 명시적으로 정지
- **OnDisable 안전망** — 패널 닫힘/씬 전환 시 코루틴이 살아있으면 NRE 가능
- **Realtime vs scaled** — 일시정지 메뉴에서도 동작해야 하면 `WaitForSecondsRealtime` 사용. 게임 속도에 종속이면 `WaitForSeconds`
- **터치 vs 마우스** — 모바일에서 손가락이 살짝 움직이면 OnPointerExit 발동 가능. 허용 임계값 두거나 `EventSystem.pixelDragThreshold` 조정
- **interactable=false 동안 발동 방지** — 매 루프에서 검사. 도중에 버튼이 비활성화되면 즉시 정지


#입력 #UI #응답성 #관용성 #코루틴
> 종속성: `#게임엔진일반` (PointerEvent 인터페이스가 있는 UI 시스템 필요)

## 11. Parallax Scrolling (시차 스크롤)

_카메라 이동량에 레이어별 `parallaxFactor ∈ [0, 1]`를 곱해 배경 레이어를 이동. 멀수록 느리게 → 시각적 원근감 생성._

**설명**
2D 게임에서 원근감을 표현하는 고전 기법. 실세계에서 멀리 있는 물체는 이동 중에 느리게 지나가는 것과 동일 원리. 뇌는 속도 차이를 깊이로 해석.

`parallaxFactor`:
- `0` → 카메라와 함께 이동 (최전경, HUD처럼 고정된 느낌)
- `0 < f < 1` → 카메라보다 느리게 이동 (배경 레이어)
- `1` → 이동 안 함 (무한히 먼 배경 — 하늘 등)

실용 레이어 구성 예:
| 레이어 | factor | 의미 |
|---|---|---|
| 전경 나뭇잎 | 0.1 | 가장 가까움 |
| 근경 건물 | 0.4 | 중간 |
| 원경 산 | 0.7 | 멀리 |
| 하늘 | 1.0 | 이동 안 함 |

**구현**
```
// 방법 A: 카메라 절대 위치 기반 (누적 오차 없음, 권장)
function Update():
    parallaxOffset = cameraPos.x * parallaxFactor
    layer.position.x = startPosition.x + parallaxOffset

// 방법 B: 카메라 델타 누적 (시작 위치가 임의적일 때)
function Update():
    cameraDelta = cameraPos.x - lastCameraPos.x
    layer.position.x += cameraDelta * parallaxFactor
    lastCameraPos = cameraPos.x
```

```csharp
// Unity C# (방법 A, LateUpdate에서 실행)
public class ParallaxLayer : MonoBehaviour
{
    [SerializeField] private float parallaxFactor;   // 0~1
    private Transform _cam;
    private float _startX;

    private void Awake()
    {
        _cam = Camera.main.transform;
        _startX = transform.position.x;
    }

    private void LateUpdate()   // 카메라 이동 후 적용
    {
        float offset = _cam.position.x * parallaxFactor;
        transform.position = new Vector3(
            _startX + offset,
            transform.position.y,
            transform.position.z);
    }
}
```

무한 타일링:
```csharp
// 카메라가 textureUnitWidth 절반 이상 벗어나면 레이어 재배치
if (Mathf.Abs(_cam.position.x - transform.position.x) >= textureUnitWidth)
{
    float offset = (_cam.position.x - transform.position.x) % textureUnitWidth;
    transform.position = new Vector3(
        _cam.position.x + offset,
        transform.position.y,
        transform.position.z);
}
```

⚠ **주의점**
- **LateUpdate 사용** — 카메라가 Update에서 이동한다면 동일 프레임 Update에서 레이어를 이동시키면 1프레임 lag. `LateUpdate`에서 카메라 위치 참조가 정확
- **방법 A vs B** — 방법 A(절대 위치 기반)는 누적 오차 없음. 방법 B(델타)는 카메라가 순간이동해도 자연스럽게 동작. 통상 방법 A 권장
- **카메라 방향과 레이어 이동 방향** — 카메라 오른쪽 이동 시 배경은 왼쪽으로 보여야 함(실세계). 위 공식 `startX + cameraPos * factor`는 카메라 방향과 같은 방향으로 레이어가 이동하므로 배경이 카메라보다 느리게 스크롤 — 의도한 시차 효과 달성
- **Y축 parallax** — 수직 스크롤 게임에서 Y factor를 추가. 통상 `Y_factor = X_factor / 2~3`으로 약하게
- **z값 처리 (2D)** — Unity 2D에서는 SortingOrder로 렌더 순서 제어. z값을 깊이로 쓰는 방식도 가능하나 orthographic 카메라에서는 시차 없음


항목 2D #카메라 #게임필 #이동
> 종속성: `#게임엔진일반`

## 19. 가산·곱하기 블렌딩 (Additive / Multiply Blending)

_두 이미지의 색상값을 더하거나(Additive) 곱해(Multiply) 합성하는 렌더링 블렌딩 방식. 빛 이펙트는 어두운 배경 위 Additive로 강조하고, 그림자는 밝은 배경 위 Multiply로 처리._

**설명**
컴퓨터 그래픽에서 색상값 범위는 검정=0, 흰색=1. 두 이미지를 합성하는 방법(블렌딩 모드)에 따라 결과가 전혀 달라진다.

**가산 블렌딩 (Additive)**
```
결과 = 배경색 + 이펙트색
```
- 두 값을 더하면 항상 밝아짐 (0.5 + 0.7 = 1.0 → 흰색에 수렴)
- 배경이 어두울수록 이펙트가 뚜렷, 밝은 배경에서는 이펙트가 묻힘
- 실무 팁: Additive 이펙트 주변에 어두운 코어(내부 어두운 색)를 배치해 대비를 만든다
- 대표 용도: 불꽃, 레이저, 마법 이펙트, 파티클, 빛 발산

**곱하기 블렌딩 (Multiply)**
```
결과 = 배경색 × 이펙트색
```
- 두 값을 곱하면 항상 어두워짐 (0.8 × 0.3 = 0.24)
- 이펙트색이 0(검정)에 가까울수록 배경이 더 어두워짐. 흰색(1.0) 이펙트는 배경에 영향 없음
- 배경이 밝을수록 효과 뚜렷, 어두운 배경에서는 거의 안 보임
- 대표 용도: 그림자, 오염, 혈흔, 얼룩, 야간 환경 필터

**두 방식 비교**
| | Additive | Multiply |
|---|---|---|
| 연산 | 배경 + 이펙트 | 배경 × 이펙트 |
| 결과 방향 | 밝아짐 | 어두워짐 |
| 어두운 배경 | 이펙트 뚜렷 ✓ | 효과 거의 없음 |
| 밝은 배경 | 이펙트 묻힘 | 이펙트 뚜렷 ✓ |
| 주 용도 | 빛, 불꽃, 마법 | 그림자, 오염, 필터 |

**그 외 블렌딩 방식**
- **Alpha (표준 투명도)** — `결과 = 배경 × (1-α) + 이펙트 × α`. 배경에 무관하게 일정한 투명도
- **Screen** — `결과 = 1 - (1-배경) × (1-이펙트)`. Additive보다 부드럽게 밝아짐. 이미 밝은 영역이 날아가지 않음
- **Overlay** — 배경이 0.5 미만이면 Multiply, 이상이면 Screen. 명암 대비 강화

**구현**
```
// Unity ShaderLab 블렌드 설정
Blend SrcAlpha One                    // Additive
Blend DstColor Zero                   // Multiply
Blend SrcAlpha OneMinusSrcAlpha       // Alpha (표준 투명)

// Unity ParticleSystem
// Inspector → Renderer → Material에서 Particles/Additive, Particles/Multiply 셰이더 사용
```

⚠ **주의점**
- **Additive는 어두운 배경 전용** — 밝은 UI 위에 Additive 파티클을 쓰면 이펙트가 거의 안 보임. 배경 밝기를 항상 고려
- **Multiply는 밝은 배경 전용** — 어두운 영역에 Multiply 그림자를 얹으면 효과 없음. 실내 밝은 타일, 밝은 스테이지에서 사용
- **알파 역할이 모드마다 다름** — Alpha 블렌딩에서 알파는 투명도지만, Additive에서 알파는 이펙트 강도(색상에 알파를 곱한 값을 더함). 동일한 텍스처도 모드에 따라 다르게 보임
- **Z-Write 비활성화 필수** — 반투명/블렌딩 오브젝트는 `ZWrite Off`. ZWrite 켜두면 뒤의 오브젝트가 렌더링되지 않는 깊이 버그 발생
- **렌더링 순서** — 블렌딩 오브젝트는 불투명 오브젝트 이후에 렌더링. Unity 렌더 큐 Transparent(3000) 이상으로 설정


#VFX #렌더링 #게임필
> 관련: game-design-notes 항목 6 빌보드 기법 (동일 렌더링 범주), unity-feature-notes 항목 17 Shader Graph (셰이더 구현) | 종속성: `#엔진독립` (개념), 구현은 `#게임엔진일반`

## 20. 레이캐스팅 (Raycasting)

_오브젝트에서 방향 벡터(선)를 쏘아 충돌 여부·거리·법선을 검사하는 기법. 몬스터 시야 판정, 2D→3D 원근 연출, 지형 탐지 등 다양한 용도의 공통 빌딩블록._

**개념**
레이캐스팅은 "한 지점에서 특정 방향으로 선을 쏘고, 그 선이 어떤 물체에 먼저 닿는지"를 묻는 연산이다. 결과로 충돌 여부, 거리, 교차 지점, 법선(표면 방향)을 얻는다.

대표 활용 3가지:
1. **몬스터 시야 판정** — 몬스터 → 플레이어 방향으로 레이를 쏴 장애물이 없으면 "보인다"고 판정. 장애물이 막으면 시야 차단.
2. **2D 공간을 3D처럼 렌더링** — 카메라에서 좌→우 방향으로 레이를 쏘아 벽까지 거리를 측정. 가까운 벽은 높게, 먼 벽은 낮게 화면에 그린다. 《둠》·《울펜슈타인 3D》의 원리.
3. **지형 탐지 (이동 가능 여부)** — 캐릭터 위로 레이를 쏘아 천장 교차점의 기울기를 측정. 경사가 완만하면 통과 가능, 급격하면 불가 판정. 《젤다의 전설: 왕국의 눈물》의 트레루프(Ascend) 스킬.

**연산 최적화 — 3단계 필터**
게임 내 모든 오브젝트를 대상으로 레이를 쏘면 비용이 선형 증가한다. 실제 시스템은 레이를 쏘기 전에 두 단계를 먼저 거른다:

```
1단계 (거리 필터)  — 시야 범위 내 오브젝트만 추린다
2단계 (시야각 필터) — 1단계 통과 오브젝트 중 시야각 내에 있는 것만 추린다
3단계 (레이캐스팅)  — 2단계 통과 오브젝트에만 실제 레이 발사
```

실제 레이를 쏘는 대상은 전체의 일부에 불과하게 되어 프레임당 연산 비용이 대폭 절감된다.

**구현 (의사코드)**
```
// 시야 판정 예시
function CanSeeTarget(self, target):
    dist = Distance(self, target)
    if dist > sightRange:          // 1단계: 거리
        return false
    angle = Angle(self.forward, target - self)
    if angle > sightAngle / 2:     // 2단계: 시야각
        return false
    hit = Raycast(self.position, direction: target - self)
    return hit.collider == target  // 3단계: 장애물 검사

// 2D → 3D 렌더링 예시 (Doom 방식)
for x in 0..screenWidth:
    rayDir = CalcRayDirection(camera, x)
    hit = Raycast2D(camera.position, rayDir)
    wallHeight = screenHeight / hit.distance   // 가까울수록 높게
    DrawVerticalLine(x, wallHeight)

// 지형 탐지 예시 (트레루프 방식)
function CanAscend(character):
    hit = Raycast(character.position, direction: UP)
    if not hit: return false
    slope = AngleBetween(hit.normal, Vector3.UP)
    return slope < MAX_ASCEND_ANGLE    // 기울기 임계값 비교
```

⚠ **주의점**
- **레이 거리(maxDistance) 설정** — 무한 레이는 씬 전체를 탐색. 항상 거리 상한을 지정해 불필요한 원거리 충돌 제외
- **레이어 마스크 활용** — 몬스터·플레이어·지형은 서로 다른 Physics Layer에 배치하고, 레이 검사 대상 레이어를 한정. "아군끼리 서로 시야 차단" 같은 오작동 방지
- **빈도 최적화** — 매 프레임 레이를 쏘지 않아도 되는 경우가 많음. 0.1~0.2초 간격 업데이트나 FixedUpdate 활용으로 비용 절감
- **시야 시각화** — 여러 개의 레이를 쏘면 시야 영역을 화면에 폴리곤으로 렌더링 가능 (미니맵 시야 표시 등). 단, 레이 수가 늘어날수록 비용 증가 — LOD 필요
- **3단계 필터 순서** — 비용이 낮은 연산(거리 비교 → 벡터 각도 계산)을 먼저, 비용이 높은 레이캐스팅은 마지막에. 순서를 바꾸면 최적화 효과 없음


#충돌 #전투 #카메라 항목 3D 항목 2D
> 관련: math-algorithm-notes (벡터 내적으로 시야각 판정), [[game-technique-notes]] 항목 11 Parallax Scrolling (2D 배경 깊이감 — 다른 방식의 원근 표현) | 종속성: `#엔진독립` (개념), 구현은 `#게임엔진일반`

## 21. 절차적 애니메이션 + 역운동학 (Procedural Animation + IK)

_미리 제작된 고정 애니메이션 대신 게임 엔진이 실시간으로 자세를 계산. 발 목적지를 먼저 정하고 관절 각도를 역산하는 IK로 불규칙 지형에서 자연스러운 보행을 구현._

**절차적 애니메이션 (Procedural Animation)**
고정 클립 재생 방식은 현재 상태에 따라 미리 만들어 둔 애니메이션을 전환한다. 절차적 애니메이션은 그 대신 매 프레임 물리·수학 계산으로 자세를 직접 생성한다. 지형·물리·입력에 즉각 반응하므로 고정 클립이 커버할 수 없는 불규칙 환경에서 생동감이 높다. 대표 사례: 《레인월드(Rain World)》의 몬스터 이동.

**역운동학 (IK, Inverse Kinematics)**
관절 계산에는 두 방향이 있다:
- **순운동학 (FK)** — 루트 관절 → 자식 관절 순으로 각도를 지정 → 말단(발) 위치가 결정된다. 말단을 정확한 위치에 맞추려면 역산이 어렵다.
- **역운동학 (IK)** — 말단(발)의 목적지 위치를 먼저 지정 → 그에 맞게 관절 각도들을 역산. 발이 어디를 밟을지 알고 있을 때 직관적.

IK를 쓰면 계단·경사·장애물에서 발이 정확히 지면을 딛는 자세를 자동 계산할 수 있다.

**2D vs 3D 무릎 위치 계산**

| | 2D | 3D |
|---|---|---|
| 풀어야 할 문제 | 두 링크 길이 + 발 위치 → 무릎 위치 1개 | 두 링크 길이 + 발 위치 → 무릎이 구부러지는 방향이 무한히 존재 |
| 해법 | 컴퍼스 작도(원 교차점) — 기하학적으로 1~2개의 해 | **힌트 축(Pole Target)** 을 추가 지정해 방향을 확정 |
| 특이점 | 발이 너무 멀면 해가 없음 (팔 완전히 뻗음) | 힌트 축 없으면 무릎이 뒤집히거나 떨림 발생 가능 |

3D에서 "무릎이 앞을 향해야 한다" 같은 Pole Target을 하나 추가하면 유일한 해가 결정된다.

**다관절 IK — FABRIK 알고리즘**
곤충·괴물처럼 관절이 3개 이상이면 해석적 역산이 복잡해진다. 반복법(iterative)으로 근사값을 수렴시킨다.

```
// FABRIK (Forward And Backward Reaching IK) 의사코드
joints = [root, ..., end_effector]
target = 발이 디뎌야 할 목표 지점

repeat until converged:
    // ① Backward pass: 말단 → 루트 방향으로 당기기
    joints[last] = target
    for i = last-1 downto 0:
        dir = normalize(joints[i] - joints[i+1])
        joints[i] = joints[i+1] + dir * segmentLength[i]

    // ② Forward pass: 루트 → 말단 방향으로 밀기
    joints[0] = originalRoot   // 루트 위치 고정
    for i = 1 to last:
        dir = normalize(joints[i] - joints[i-1])
        joints[i] = joints[i-1] + dir * segmentLength[i-1]
```

보통 5~10회 반복으로 충분히 수렴한다.

**보행 구현 흐름**
```
1. 발 스텝 결정
   각 발마다 '현재 발 위치'와 '몸통 이동에 따른 목표 위치'를 비교
   거리가 임계값을 초과하면 스텝 트리거

2. 발 이동 (공중 궤적)
   현재 위치 → 목표 위치를 Lerp/bezier 곡선으로 들어올렸다 내림
   착지점은 Raycast로 지면을 탐지해 결정

3. IK 적용
   각 발 위치 확정 후 다리 관절 전체에 IK 계산
   무릎 방향은 Pole Target으로 고정
```

⚠ **주의점**
- **발 동기화** — 4족 보행에서 두 발이 동시에 공중에 뜨면 불안정. 발 스텝 간격에 위상 오프셋(0.5 주기 차이 등)을 줘서 교차 보행 강제
- **몸통 높이 보정** — 발이 높낮이가 다른 지형에 닿으면 몸통도 그에 맞게 높이를 조정해야 기울지 않음. 발 위치 평균으로 몸통 높이 계산
- **특이점(Singularity) 처리** — 목표가 팔다리의 최대 도달 거리 밖이면 IK 해가 없음. 완전히 뻗은 상태로 클램프하거나 목표를 가능 범위로 제한
- **Unity IK 활용** — Unity Animator에 내장된 IK Pass(`OnAnimatorIK`)와 `SetIKPositionWeight`, `SetIKPosition`으로 빠르게 적용 가능. 커스텀 완전 절차적 구현은 그 위에 쌓는다
- **성능** — 관절 수·반복 횟수·발 수가 늘어날수록 비용 증가. 카메라에서 멀수록 반복 횟수를 줄이는 LOD 적용 권장


#애니메이션 #이동 항목 3D #게임필
> 관련: [[game-technique-notes]] 항목 20 레이캐스팅 (발 착지점 탐지에 Raycast 활용), math-algorithm-notes (벡터 연산·Lerp·삼각함수가 기반) | 종속성: `#엔진독립` (FABRIK 개념), 구현은 `#게임엔진일반` (Unity IK Pass 등)

## 22. 길찾기 알고리즘 (Pathfinding)

_지형을 그래프로 변환 후 최단 경로를 탐색. 단일 유닛은 A*, 대량 유닛은 플로우 필드(Flow Field)가 표준 선택._

**공통 전제 — 지형의 그래프화**
모든 길찾기의 첫 단계는 지형을 탐색 가능한 그래프로 변환하는 것이다. 구현 방식 3가지:

| 방식 | 설명 | 적합한 게임 |
|---|---|---|
| 타일 그리드 | 맵을 고정 크기 격자로 분할 — 각 셀이 노드 | 2D 전략·RPG |
| 내비메시 (NavMesh) | 이동 가능 표면을 다각형 메시로 표현 | 3D 게임 |
| 웨이포인트 그래프 | 수동 지정 노드를 엣지로 연결 | 복잡한 실내 공간 |

각 노드는 인접 노드로의 **이동 비용(가중치)**을 가진다. 장애물 = 연결 없음. 진흙·물 = 높은 비용.

---

**① 다익스트라 알고리즘 (Dijkstra)**
시작점에서 방사형으로 퍼져 나가며 모든 노드까지의 최단 거리를 확정한다.

```
open = PriorityQueue  // 비용 오름차순
open.push(start, cost=0)
visited = {}

while open not empty:
    current, cost = open.pop()          // 현재까지 비용이 가장 낮은 노드
    if current in visited: continue
    visited[current] = cost

    for neighbor, edgeCost in current.neighbors:
        newCost = cost + edgeCost
        if neighbor not in visited:
            open.push(neighbor, newCost)
```

- **장점**: 목적지가 여러 개이거나 전체 맵 최단 거리가 필요할 때 확실한 최적해 보장
- **단점**: 목적지 방향을 모르므로 사방으로 탐색 → 탐색 노드 수 많음

---

**② A* 알고리즘**
다익스트라에 **휴리스틱(heuristic)** 을 추가해 목적지 방향을 우선 탐색한다.

```
f(n) = g(n) + h(n)

g(n) = 시작점 → n까지 실제 이동 비용
h(n) = n → 목적지까지 추정 비용 (휴리스틱)
```

- **h(n)** 은 장애물을 무시한 직선 거리(유클리드) 또는 맨해튼 거리로 계산
- f 값이 낮은 노드를 우선 탐색 → 목적지 방향으로 집중 → 탐색 노드 수 대폭 감소

```
open = PriorityQueue  // f값 오름차순
open.push(start, f=h(start))

while open not empty:
    current = open.pop()
    if current == goal: return ReconstructPath()

    for neighbor in current.neighbors:
        tentative_g = g[current] + edgeCost(current, neighbor)
        if tentative_g < g[neighbor]:
            g[neighbor] = tentative_g
            f = tentative_g + h(neighbor)
            open.push(neighbor, f)
```

**h(n) 선택 기준**:
| 방식 | 수식 | 적합 상황 |
|---|---|---|
| 맨해튼 거리 | `|dx| + |dy|` | 4방향 격자 이동 |
| 유클리드 거리 | `sqrt(dx²+dy²)` | 자유 방향 이동 |
| 체비쇼프 거리 | `max(|dx|, |dy|)` | 8방향 격자 이동 |

> 《스타크래프트》 사례: 유닛 이동 명령(우클릭) 시 A*로 경로 재계산. 명령을 자주 줄수록 경로가 빈번하게 갱신되어 막힌 구간 없이 이동하는 것처럼 느껴지는 시각적 효과 발생.

---

**③ 플로우 필드 (Flow Field)**
유닛 수백~수천 마리가 동일한 목적지를 향할 때 개별 A* 호출은 비용이 선형 증가한다. 플로우 필드는 **목적지를 고정하고 맵 전체의 방향 벡터를 한 번만 사전 계산**해 둔다.

```
// 사전 계산 (목적지 변경 시 1회 실행)
1. 목적지에서 Dijkstra/BFS로 모든 셀까지 비용 계산
2. 각 셀에서 비용이 낮아지는 방향을 화살표로 저장

// 런타임 (유닛마다 매 프레임)
direction = flowField[unit.currentCell]  // 테이블 조회 1회로 끝
unit.velocity = direction * speed
```

- **장점**: 유닛이 아무리 많아도 런타임 비용은 O(1)/유닛 (테이블 조회만)
- **단점**: 목적지가 바뀌면 전체 맵 재계산 필요. 유닛별 개별 목적지에는 부적합

---

**알고리즘 선택 기준**

| 상황 | 권장 알고리즘 |
|---|---|
| 단일 유닛, 목적지 1개 | A* |
| 목적지가 여러 개이거나 전체 맵 경로 필요 | 다익스트라 |
| 유닛 100+ 이 같은 목적지로 이동 | 플로우 필드 |
| 목적지가 자주 바뀌는 대규모 | 플로우 필드 + 부분 재계산 |

⚠ **주의점**
- **동적 장애물** — A*는 경로 계산 시점의 스냅샷 기반. 장애물이 이동하면 재계산 필요. 재계산 빈도와 비용 균형 필요 (0.2~0.5초 간격 등)
- **경로 스무딩** — 격자 기반 A*는 지그재그 경로가 나옴. 직선 가시성 체크(Line of Sight)로 불필요한 중간 노드를 제거하는 String Pulling 후처리 적용
- **타이 브레이킹** — 동일한 f 값 노드가 여러 개이면 탐색 방향이 제멋대로 퍼짐. h에 미세 가중치를 추가해 목적지 방향을 우선하도록 타이 브레이킹
- **NavMesh와의 조합** — Unity에서는 NavMesh(지형 전처리) + NavMeshAgent(A* 내장)로 대부분 해결. 커스텀 비용·플로우 필드는 그 위에 추가 레이어로 구현
- **플로우 필드 메모리** — 맵이 클수록 방향 벡터 배열 크기 증가. 해상도 조정(플로우 필드 셀을 게임 타일보다 크게) 또는 청크 단위 계산으로 메모리 절감


#이동 #전략 #액션 #예측가능성
> 관련: [[game-technique-notes]] 항목 20 레이캐스팅 (장애물 감지에 Raycast 활용 가능), math-algorithm-notes (우선순위 큐·BFS·그래프 탐색) | 종속성: `#언어독립`

## 23. 픽셀 아트 품질 기법

_낮은 해상도와 제한된 팔레트 안에서 품질을 끌어올리는 4가지 핵심 기법. 선 규칙 두 가지(더블픽셀·재기), 서브픽셀 애니메이션, 컬러 외곽선, 디더링._

**배경**
과거 하드웨어는 해상도와 색상 수가 극도로 제한되어 있었다. 이 제약 안에서 이미지를 깔끔하고 풍부하게 보이도록 만들기 위해 예술가·개발자들이 체계화한 기법들이다. 제약이 사라진 현대에도 의도적인 픽셀 아트 스타일을 만들 때 동일하게 적용된다.

---

**① 선 규칙 — 더블픽셀(Double Pixel) 제거 + 재기(Jaggies) 방지**

**더블픽셀** — 꺾이는 부분에서 픽셀이 두 개 이상 뭉쳐 선이 국부적으로 두꺼워지는 현상. 코너 처리 시 가장 흔하게 발생하며 가장 먼저 제거해야 한다.

```
나쁜 예 (더블픽셀):        좋은 예:
█ █                        █
  █ █                        █
```

**재기(Jaggies)** — 기울기가 불규칙한 선에서 생기는 울퉁불퉁한 계단 현상.

해결 규칙:
- **직선**: 기울기(픽셀 수 비율)를 일정하게 유지. `1:1`, `1:2`, `1:3` 등 한 가지 비율로만 구성.
- **곡선**: 선을 이루는 픽셀 수를 단계적으로 증가 또는 감소시켜 그라데이션처럼 구성.

```
나쁜 직선 (기울기 불규칙):   좋은 직선 (기울기 1:2 고정):
█                            █ █
  █ █                              █ █
      █                                  █ █

나쁜 곡선:    좋은 곡선 (픽셀 수 단계적 변화 1→2→3→2→1):
█ █ █ █      █
█ █            █ █
  █              █ █ █
                   █ █
                     █
```

---

**② 서브픽셀 애니메이션 (Subpixel Animation)**

낮은 해상도에서 오브젝트를 1픽셀 이동시키면 실제 이동 거리가 너무 크게 느껴진다. 1픽셀 미만의 미세한 이동감을 주기 위해 **형태를 옮기지 않고 명암(색)만 조금씩 바꾸는 방법**이다.

```
// 오른쪽으로 0.5픽셀 이동하는 느낌
Before:  [밝 밝 밝]
After:   [중 밝 밝 어]   ← 왼쪽 끝을 어둡게, 오른쪽에 희미한 픽셀 추가
```

눈은 명암 변화를 무게 중심 이동으로 인식한다. 실제 픽셀을 움직이지 않고 색 변화만으로 서브픽셀 단위의 움직임 착시를 만든다.

대표 사례: 《메탈슬러그》 — 극도로 작은 해상도에서도 캐릭터와 기계의 움직임이 매끄럽고 실감 나는 이유.

---

**③ 컬러 외곽선 (Selective Outline)**

외곽선을 획일적인 검은색으로만 처리하지 않는다. 빛이 오는 방향과 인접한 배경 색을 고려해 부위별로 다른 색을 사용한다.

```
적용 원칙:
- 빛이 닿는 면의 외곽선 → 배경보다 밝은 색 or 오브젝트 본체의 밝은 파생색
- 그림자 면의 외곽선   → 짙은 색 or 검정에 가까운 색
- 투명하게 보이게 하려면 → 외곽선을 배경색과 동일하게 (Invisible Outline)
```

효과: 적은 픽셀로도 입체감과 광원 방향이 명확하게 전달된다.

---

**④ 디더링 (Dithering)**

제한된 색상 수 안에서 부드러운 그라데이션 효과를 만드는 기법. 두 색의 픽셀을 일정한 패턴으로 교차 배치하면 눈이 두 색의 평균 색으로 인식한다.

대표 패턴:

```
체커보드 (50:50 혼합):   점진적 전환 (왼쪽 → 오른쪽):
A B A B A               A A A B A B B B
B A B A B               A A B A B B B B
A B A B A               A B A B B B B B
```

디더링 없이 색상을 강제 축소 → 이미지가 경계에서 뚝뚝 끊겨 거칠게 보임.
디더링 적용 → 두 색의 경계가 자연스럽게 블렌딩되어 풍부한 명암 표현.

디더링 패턴 종류:
| 패턴 | 특징 |
|---|---|
| 체커보드 | 50:50 혼합. 가장 균등한 블렌딩 |
| 점진 체커보드 | 비율을 단계적으로 바꿔 그라데이션 생성 |
| 베이어 행렬 | 수학적 행렬 기반 규칙 패턴 (오래된 모니터 최적화) |
| 플로이드-스타인버그 | 오차 확산 방식 — 더 자연스럽지만 픽셀 아트에서는 드물게 사용 |

⚠ **주의점**
- **디더링 과다 사용** — 모든 색 전환에 디더링을 쓰면 화면 전체가 노이즈처럼 보임. 그라데이션이 필요한 그림자·하이라이트 경계에만 선택적으로 사용
- **더블픽셀 자동화** — 도구(Aseprite 등)가 자동으로 잡아주지 않으면 완성 후 전체 선을 다시 점검하는 습관 필요. 특히 애니메이션 프레임 간 전환 시 코너 처리에서 자주 발생
- **서브픽셀과 해상도 업스케일** — 업스케일(2x, 4x) 적용 시 서브픽셀 트릭이 의도와 다르게 보일 수 있음. 업스케일 알고리즘(EPX, hq2x 등)이 명암 변화를 이동으로 처리하지 않을 수 있음
- **팔레트 수 제약과 컬러 외곽선** — 외곽선 전용 색을 추가하면 팔레트 슬롯 소모. 오브젝트 본체의 어두운 파생색을 외곽선에 재활용하는 방식으로 팔레트 절약
- **현대 픽셀 아트 vs 레트로 제약** — 현대 도구는 색상 수 제한이 없으므로 위 규칙을 일부 완화할 수 있다. 그러나 의도적 레트로 스타일이라면 원본 하드웨어의 팔레트·해상도 제약을 참고해 적용 범위를 결정


#VFX #애니메이션 #UI #게임필
> 관련: [[game-technique-notes]] 항목 19 가산·곱하기 블렌딩 (색상 합성 — 렌더링 범주 공통), game-design-notes (픽셀 아트 스타일 선택의 디자인 의도) | 종속성: `#언어독립` (도구는 Aseprite·Photoshop 등 독립)
