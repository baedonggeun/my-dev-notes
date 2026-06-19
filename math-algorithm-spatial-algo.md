# 수학/알고리즘 — 공간·알고리즘

> 상위 노트: [[math-algorithm-notes]] (전체 인덱스 디스패처)
> 다루는 축: 공간분할·A*·적분·행렬
> 다루지 않는 축: [[math-algorithm-interpolation|수학/알고리즘 — 보간·변환·곡선]] / [[math-algorithm-probability|수학/알고리즘 — 확률·통계·집합]]

---


## 태그 목록

### 분야
- `#선형대수` `#보간` `#곡선` `#확률` `#변환` `#이산` `#기하` `#해싱` `#노이즈` `#수치해석`

### 응용
- `#게임필` `#밸런싱` `#오디오` `#UI좌표` `#가챠` `#시너지` `#렌더링`

### 복잡도
- `#O(1)` `#O(logN)` `#O(N)` `#O(NlogN)`

### 결정성
- `#결정론` `#확률적` `#근사`


---


# 인덱스

### 본 프로젝트에서 사용 중
| # | 알고리즘/공식 | 분야 | 한 줄 요약 | 종속성 |
|---|--------|------|----------|--------|
| 7 | Vector2 거리/방향 (벡터 산술) | `#선형대수` `#UI좌표` | 두 점 사이 거리/단위 방향 벡터 계산 | `#언어독립` |
| 11 | Perlin / Simplex Noise | `#노이즈` `#근사` | 결정론적 의사 랜덤 노이즈 필드 (지형/텍스처) | `#언어독립` |
| 12 | A* 경로 탐색 | `#이산` `#기하` | 휴리스틱 기반 최단 경로 탐색 | `#언어독립` |
| 13 | Quaternion 회전 (Slerp) | `#선형대수` | 짐벌락 없는 회전 보간 | `#언어독립` |
| 14 | 공간 분할 (Quadtree / Spatial Hash) | `#기하` `#해싱` | 공간 영역 인덱싱으로 충돌/검색 가속 | `#언어독립` |
| 17 | 오일러 적분 (Euler Integration) | `#수치해석` `#근사` | 현재 상태에 `가속도 × dt`를 반복 누적해 다음 상태를 근사 — 게임 물리 루프의 핵심 빌딩블록. 비대칭 중력처럼 해석적 해가 없는 규칙을 프레임마다 단순 덧셈으로 처리 | `#언어독립` |

---

# 풀노트

## 7. Vector2 거리/방향 (벡터 산술)

두 점 A(x1, y1), B(x2, y2) 사이의 거리 d = |B - A|와 단위 방향 벡터 dir = (B - A) / |B - A| 계산.

**설명**
벡터는 게임에서 물체 위치, 속도, 방향, 힘 등 모든 이동의 기본 단위.

핵심 연산:
- 뺄셈: v = B - A -- A에서 B로의 벡터
- 거리(크기): |v| = sqrt(v.x^2 + v.y^2) -- 유클리드 거리
- 방향(정규화): v_hat = v / |v| -- 크기가 1인 단위 벡터
- 거리 제곱: |v|^2 = v.x^2 + v.y^2 -- sqrt 생략. 거리 비교에 유용

게임 대표 사용:
- 타겟 추적: dir = (targetPos - myPos).normalized, velocity = dir * speed
- 사거리 판정: if sqrDist < range^2 (제곱으로 sqrt 회피)
- 넉백/투사체: knockbackDir = (hitPos - center).normalized * force
- UI 좌표 차이: 드래그 방향/거리 계산
- AI 시야: dot(forward, dir) > 0.7 -> 시야각 45도 이내

**구현**
```
function Distance(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    return sqrt(dx*dx + dy*dy)

function SqrDistance(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    return dx*dx + dy*dy

function Direction(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    mag = sqrt(dx*dx + dy*dy)
    if mag == 0: return (0, 0)
    return (dx / mag, dy / mag)
```

Unity C#:
```
Vector2 dir = (target.position - transform.position).normalized;
float sqrDist = dir.sqrMagnitude;
float dist = dir.magnitude;
```

경고 주의점:
- 0나누기 (영벡터) -- A == B일 때 |v| = 0 -> direction = NaN, NaN. 정규화 전 if (mag == 0) return Vector2.zero 필수
- sqrt는 비싸다 -- 거리 비교만 필요하면 sqrMagnitude 사용
- 부동소수점 정밀도 -- 매우 가까운 두 점(1e-10 차이)에서 방향이 불안정. sqrMagnitude < epsilon 가드 검토
- Manhattan distance 대안 -- |dx| + |dy|. 그리드 기반 게임에서 정확하고 빠름


#선형대수 `#O(1)` #결정론 #게임필
> 관련: [[unity-feature-notes]] 항목 27 Mathf (Vector2/3 API) | 종속성: `#언어독립`

---

## 11. Perlin / Simplex Noise

_결정론적으로 부드러운 의사 랜덤 노이즈 필드를 생성. 자연스러운 지형/텍스처/움직임 패턴에 사용. Ken Perlin이 1983년 개발._

**설명**
단순 난수(white noise)를 지형 높이에 사용하면 지나치게 울퉁불퉁하고 파편화되어 게임에 쓸 수 없다 — 모든 주파수에서 동일한 에너지를 가져 인접 지점 간 연속성이 없기 때문. 자연 지형은 저주파에 높은 진폭, 고주파에 낮은 진폭(pink noise) 특성을 가진다. Perlin Noise는 이 특성을 수학적으로 모델링.

**직관적 원리 (4단계)**
1. **격자 + 무작위 그라디언트 벡터**: 공간 위에 바둑판 격자를 그리고 각 교차점마다 임의 방향의 그라디언트 벡터를 배치
2. **거리 벡터 계산**: 샘플 지점에서 주변 4개(2D) 교차점 방향으로 벡터를 그림
3. **내적(Dot Product)**: 각 교차점의 "거리 벡터 × 그라디언트 벡터" 내적 계산 → 두 벡터가 같은 방향이면 양수, 반대면 음수
4. **페이드 보간 합산**: 내적값 4개를 fade 함수(smooth step)로 부드럽게 보간·합산 → 최종 높이값

인접 지점들이 같은 교차점의 그라디언트를 공유하기 때문에 연속적이고 부드러운 필드가 자동으로 생성된다.

Perlin Noise 작동 원리 (수학 상세):
1. 정수 그리드(Integer Lattice) 각 모서리에 의사 난수 그라디언트(gradient) 벡터 할당
2. 입력 좌표의 소수부로 그라디언트를 부드럽게 보간 (fade 함수: 6t^5 - 15t^4 + 10t^3)
3. 여러 옥타브(octave)를 누적 (FBM: Fractional Brownian Motion)해 자연스러운 디테일 생성

Simplex Noise:
- Perlin의 후속작 (2002). 같은 출력을 더 적은 계산으로 생성
- N차원에서 O(N^2) vs O(N*2^N) (Perlin 대비 효율)
- Patent 이슈로 게임 엔진은 Perlin 계열 유지

게임 대표 사용:
- 절차적 지형 생성 (높이 맵) — Minecraft, No Man's Sky 등 오픈 월드 / 생존 게임의 핵심 기반
- 텍스처 (구름, 대리석, 나뭇결)
- 캐릭터/몬스터 움직임의 유기적 변이
- VFX (불, 연기, 액체)

**구현**
```
function PerlinNoise(x, y):
    xi = floor(x) & 255
    yi = floor(y) & 255
    xf = x - floor(x)
    yf = y - floor(y)
    u = fade(xf)  // 6t^5 - 15t^4 + 10t^3
    v = fade(yf)
    // Permutation table에서 그라디언트 조회 후 보간
    ...

// FBM: 여러 옥타브 누적
function FBM(x, y, octaves, lacunarity=2.0, gain=0.5):
    value = 0
    amplitude = 1
    frequency = 1
    for i in range(octaves):
        value += amplitude * PerlinNoise(x*frequency, y*frequency)
        amplitude *= gain
        frequency *= lacunarity
    return value
```

엔진별 빌트인:
- Unity: Mathf.PerlinNoise(x, y) -- 정적 2D Perlin Noise. 1D/3D 없음
- Unreal: NoiseBlueprintNode

경고 주의점:
- PerlinNoise 출력 범위는 [0, 1]이 아님 -- 실제 범위는 [-sqrt(n/4), sqrt(n/4)]. Unity Mathf.PerlinNoise는 [0, 1] 근사
- 캐싱 필수 -- FBM 6옥타브는 매 호출 pow 5회 + noise 6회. 실시간 생성 시 캐싱 또는 GPU 고려
- 시드 변경 -- 동일 permutation table은 항상 같은 노이즈. Unity는 시드 변경 기능 없음
- 결정론적 -- 같은 입력 -> 같은 출력. 절차적 생성 맵은 시드 기반 저장으로 용량 절약
- 3D+에서 Simplex 선호 -- Perlin 3D는 8개 모서리 vs Simplex 4개. 고차원일수록 Simplex 효율 압도


#노이즈 #근사 `#O(octaves)` #결정론
> 종속성: `#언어독립`

---

## 12. A* 경로 탐색

_시작 노드에서 목표 노드까지의 최단 경로를 휴리스틱(heuristic) 기반으로 탐색. g(실제 비용) + h(추정 비용) = f(우선순위)로 열린 집합(open set)을 관리._

**설명**
게임에서 AI가 장애물을 피해 목적지까지 찾아가는 가장 보편적인 알고리즘. Dijkstra(모든 방향 동일 탐색)에 휴리스틱 추정(목표 방향 편향)을 더해 효율성을 극대화.

핵심 개념:
- g(n): 시작 노드에서 현재 노드까지의 실제 이동 비용
- h(n): 현재 노드에서 목표 노드까지의 추정 비용 (휴리스틱)
- f(n) = g(n) + h(n): 우선순위 큐의 정렬 기준. f가 낮은 노드부터 탐색
- 휴리스틱의 조건: admissible (h가 실제 비용을 넘지 않음) -> A*가 최적 경로 보장

휴리스틱 선택 (격자 기반 게임):
- Manhattan 거리: |dx| + |dy| -- 4방향 이동에 정확
- Chebyshev 거리: max(|dx|, |dy|) -- 8방향 이동에 정확
- Euclidean 거리: sqrt(dx^2 + dy^2) -- 자유 이동에 정확

**구현**
```
function AStar(start, goal, getNeighbors, heuristic):
    openSet = PriorityQueue()     // f(n) 기준 정렬
    cameFrom = Map()
    gScore = Map(default=inf)

    gScore[start] = 0
    openSet.Enqueue(start, heuristic(start, goal))

    while openSet is not empty:
        current = openSet.Dequeue()

        if current == goal:
            return ReconstructPath(cameFrom, current)

        for neighbor in getNeighbors(current):
            tentative_g = gScore[current] + 1
            if tentative_g < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                openSet.Enqueue(neighbor, f)

    return null  // no path
```

경고 주의점:
- 휴리스틱 과대평가(overestimate) 금지 -- admissible 조건 위반 시 A*가 최적 경로를 보장하지 않음
- 격자 타입과 휴리스틱 불일치 -- 4방향 맵에 Euclidean 사용 시 admissible은 만족하지만 확장 노드 수 증가
- 메모리 -- gScore/cameFrom 맵이 탐색 영역만큼 커짐. 대규모 월드에서 IDA* 또는 HPA* 고려
- 동적 장애물 -- A*는 정적 그래프 가정. 자주 변하면 D* Lite / LPA* 고려
- 경로 평활화 -- A* 결과는 격자 기반 직선. 실제 이동은 스무딩(Bezier, Catmull-Rom) 필요
- 탐색 깊이 제한 -- 실시간 게임에서는 탐색 깊이/노드 수 제한 필수


#이산 #기하 `#O(E log V)` #결정론
> 종속성: `#언어독립`

---

## 13. Quaternion 회전 (Slerp)

_짐벌락(gimbal lock)이 없는 4차원 복소수 회전 표현. Slerp(Spherical Linear Interpolation)로 두 회전 사이를 부드럽게 보간._

**설명**
오일러 각(Euler angles: pitch/yaw/roll)은 직관적이지만 짐벌락이라는 치명적 문제가 있다. 축이 정렬되면 한 축의 회전이 다른 축과 겹쳐 자유도가 사라진다. Quaternion은 이 문제를 수학적으로 해결.

Quaternion의 구조:
- q = (x, y, z, w) where x^2 + y^2 + z^2 + w^2 = 1
- w는 스칼라, (x, y, z)는 3D 축 * sin(theta/2)를 인코딩
- 물리적 의미: "회전축과 회전각을 직접 저장"

Slerp 공식:
Slerp(q1, q2, t) = (sin((1-t)*theta) * q1 + sin(t*theta) * q2) / sin(theta)

게임 대표 사용:
- 카메라 회전 보간 (3인칭 시점 전환)
- 캐릭터 본 회전 (애니메이션 블렌딩)
- 오브젝트 방향 부드러운 전환
- VR/AR 헤드 트래킹

**구현**
```
function Slerp(q1, q2, t):
    dot = q1.x*q2.x + q1.y*q2.y + q1.z*q2.z + q1.w*q2.w

    // 짧은 경로 선택 (dot < 0이면 반대 방향)
    if dot < 0:
        q2 = (-q2.x, -q2.y, -q2.z, -q2.w)
        dot = -dot

    // 작은 각도는 Lerp로 근사 (수치 안정성)
    if dot > 0.9995:
        return Normalize(Lerp(q1, q2, t))

    theta = acos(dot)
    sinTheta = sin(theta)
    t1 = sin((1-t)*theta) / sinTheta
    t2 = sin(t*theta) / sinTheta

    return Quaternion(t1*q1.x + t2*q2.x, ...)
```

엔진별 빌트인:
- Unity: Quaternion.Slerp(q1, q2, t) -- t clamp 0~1
- Unity: Quaternion.Lerp -- 더 빠르지만 정확도 낮음
- Unreal: FQuat::Slerp

경고 주의점:
- Lerp로 Quaternion 보간 금지 -- 수치상 작동하지만 각속도가 균일하지 않음
- 짧은 경로 vs 긴 경로 -- Slerp는 항상 짧은 쪽을 선택하지 않음. dot < 0 시 q2 반전 필요. Unity가 자동 처리
- 180도 회전 케이스 -- sin(pi) = 0 나누기. 대부분 엔진이 epsilon 가드
- 오일러 변환 -- Quaternion.eulerAngles는 유일하지 않음. 디버그 출력 용도로만 사용
- 성능 -- Slerp는 sin/acos으로 비쌈. Lerp + 정규화가 더 빠름. 빠른 회전 전환은 Lerp 권장


#선형대수 `#O(1)` #결정론
> 종속성: `#언어독립`

---

## 14. 공간 분할 (Quadtree / Spatial Hash)

_2D 공간을 재귀적으로 4분할(Quadtree) 또는 그리드 셀로 분할(Spatial Hash)해 충돌 검사/검색을 가속. O(N^2) 브루트포스를 O(N log N) 또는 O(N)으로._

**설명**
게임에는 "이 영역 안에 무엇이 있는가"라는 질문이 빈번하다: 총알이 벽에 닿았는가, 유닛이 시야 범위 내에 있는가. 공간 분할은 검사가 필요한 대상만 추려내는 인덱싱 기법.

**Quadtree** (동적 분할, 불균등 분포에 강함):
1. 공간을 4개의 자식 노드로 균등 분할
2. 각 노드의 객체 수가 임계값 초과 시 재분할
3. 검색: 쿼리 영역과 겹치는 노드의 객체만 반환

**Spatial Hash** (고정 크기, 균등 분포에 효율적):
1. 공간을 고정 크기 셀로 분할 (해시 맵: cellKey = (floor(x/cellSize), floor(y/cellSize)))
2. 각 셀이 객체 리스트를 가짐
3. 검색: 쿼리 영역이 겹치는 셀의 객체만 검사

선택 기준:
| 상황 | Quadtree | Spatial Hash |
|------|----------|-------------|
| 객체 분포 불균등 | 유리 | 불리 |
| 자주 변하는 동적 객체 | 삽입/삭제 비용 | 더 유리 (O(1) 해시) |
| 대규모 정적 지형 | 유리 | 메모리 고정 |
| N차원 확장 | 2D 전용 (Octree: 3D) | 모든 차원 동일 |

**구현 (Spatial Hash)**:
```
function Insert(obj):
    minCell = CellPos(obj.min)
    maxCell = CellPos(obj.max)
    for x in range(minCell.x, maxCell.x+1):
        for y in range(minCell.y, maxCell.y+1):
            key = Hash(x, y)
            grid[key].Add(obj)

function Query(area):
    minCell = CellPos(area.min)
    maxCell = CellPos(area.max)
    result = Set()
    for x in range(minCell.x, maxCell.x+1):
        for y in range(minCell.y, maxCell.y+1):
            key = Hash(x, y)
            for obj in grid[key]:
                if area.Overlaps(obj):
                    result.Add(obj)
    return result
```

경고 주의점:
- Spatial Hash 셀 크기 선택이 핵심 -- 너무 작으면 셀 많아짐, 너무 크면 검사량 증가. 객체 평균 크기의 2~4배 권장
- Quadtree 분할 임계값 -- 너무 낮으면 깊은 트리, 너무 높으면 리프에 객체 많음. 경험적: 8~16개
- 대형 객체 처리 -- Spatial Hash에서 대형 객체는 모든 셀에 삽입됨. static/dynamic 분리 고려
- 캐시 친화성 -- Quadtree는 포인터 추적. Spatial Hash는 배열 기반으로 더 캐시 친화적
- Unity Physics2D는 Spatial Hash 계열 내부 사용 -- 별도 구현보다 Physics2D.Overlap* API 우선 고려


#기하 #해싱 #게임필
> 종속성: `#언어독립`

---

## 17. 오일러 적분 (Euler Integration)

_현재 상태(위치·속도)에 `가속도 × dt`를 반복 누적해 다음 상태를 근사하는 수치 해석 기법. 미적분 없이 단순 덧셈만으로 게임 물리 루프를 구현하는 핵심 빌딩블록._

**설명**
실제 포물선 운동은 `y = v₀t - ½gt²`로 정확히 표현된다. 그러나 게임은 두 가지 이유로 이 해석적 해(analytical solution)를 쓰지 않는다:
1. 비대칭 중력·가변 점프처럼 상태별로 가속도가 바뀌면 해석적 해 자체가 없음
2. 규칙을 바꿀 때마다 공식을 재도출해야 함

오일러 적분은 대신 "아주 짧은 시간 동안 가속도가 일정하다"는 가정 하에 덧셈만으로 근사한다:

```
속도 += 가속도 × dt
위치 += 속도   × dt
```

1프레임(~0.016s @ 60fps)을 dt로 쓰면 오차가 실용적으로 무시 가능하다. 복잡한 적분 없이 if 분기만으로 어떤 가속도 규칙도 적용할 수 있다.

**게임 점프 적용 — 비대칭 중력**
현실: 상승/하강 동일한 중력 g → 포물선이 좌우 대칭, 조작감 "둥둥 뜨는" 느낌.
게임: 상승 시 g_up(작음), 하강 시 g_down(큼) → 오일러 루프에서 조건 분기 하나로 구현.

```
// 매 프레임
if velocity.y > 0:          // 상승 중
    velocity.y -= g_up  * dt
else:                       // 하강 중
    velocity.y -= g_down * dt

position.y += velocity.y * dt
```

참고 수치 (영상 예시):
| 파라미터 | 값 | 의미 |
|---|---|---|
| g_up | 7 | 상승 중력 — 느긋하게 올라감 |
| g_down | 36 | 하강 중력 — 빠르게 떨어짐 (약 5배) |

g_down을 크게 할수록 템포 빠름 + 가변 점프 구현이 쉬워짐 (버튼 뗄 때 g를 g_down으로 교체).

**구현 — 일반화된 게임 물리 루프**
```
function Update(dt):
    accel = GetAcceleration(state)   // 상태별 가속도 결정
    velocity += accel * dt
    position += velocity * dt

function GetAcceleration(state):
    if state.isJumping and velocity.y > 0:
        return -g_up
    else:
        return -g_down
    // 이 함수에 비대칭 중력, Apex Modifier, 가변 점프, 낙하 최대 속도 등 모든 규칙 추가
```

⚠ **주의점**
- **프레임률 독립 필수** — `velocity += accel * dt`에서 dt는 반드시 `Time.deltaTime`(가변). 고정값(1/60) 하드코딩 시 프레임률 변화에 따라 물리가 달라짐
- **오차 누적** — dt가 클수록(저프레임) 오차 증가 → 물체가 벽을 통과하거나 튀는 현상. 60fps 기준 허용 오차이지만 가변 dt 사용 + 이동 후 충돌 보정을 세트로 적용
- **해석적 해 vs 오일러** — 일정 중력의 단순 포물선은 해석적 해가 더 정확. 게임 점프처럼 상태별 가속도가 다르면 해석적 해가 없어 오일러가 표준
- **Verlet 적분 대안** — 에너지 보존이 중요한 물리 퍼즐/로프 시뮬레이션에는 Verlet 적분이 더 안정적. 캐릭터 이동에서는 오일러로 충분


#수치해석 #근사 `#O(1)` #결정론
> 관련: [[game-technique-notes]] 항목 1 비대칭 점프 (Euler 적분의 직접 응용 — g_up/g_down 비대칭 구현) | 종속성: `#언어독립`

---

## 분류 메모

- **수학 vs 기법 경계**: Lerp는 *수학*이고, "D20 굴림을 데미지에 Lerp" 는 *기법*([game-technique-notes.md](game-technique-notes.md) 항목 5). 같은 Lerp가 카메라 추적에도 쓰이므로 한 단계 아래에 둔다.
- **수학 vs Unity API 경계**: Mathf.Lerp는 Unity API([unity-feature-notes.md](unity-feature-notes.md) 항목 27)이지만, "선형 보간"이라는 개념은 엔진 독립적. 본 노트는 *개념*에 집중.
- **승격 후보**: 일반 지식 섹션(항목 9~항목 16)이 본 프로젝트에 도입되면 "사용 중" 표로 이동.

### 다관점 분리 그룹 (의도된 cross-ref)
같은 코드 사례를 *수학 개념 / 게임 기법 / Unity API* 세 축에서 본다. 어느 한 곳이 SOT가 아니라 축별 진입점이 다르다.

| 공통 주제 | math (개념) | game-technique (응용) | unity-feature (API) |
|---|---|---|---|
| 선형 보간 | 항목 1 Lerp | 항목 5 D20 데미지 | 항목 27 Mathf |
| dB 변환 | 항목 2 Linear↔dB | 항목 6 AudioMixer 지각 변환 | 항목 14 AudioMixer / 항목 27 Mathf.Log10 |
| 멱함수 | 항목 4 Power-Law | 항목 3 강화 보상 곡선 | --- |
| 가중 랜덤 + Pity | 항목 5, 항목 6 | 항목 2 가챠 등급 보정 | --- |
| 벡터 산술 | 항목 7 Vector2 | --- | 항목 27 Mathf (Vector2/3) |
| 집합 카운팅 | 항목 8 HashSet | 항목 4 Unique-ID Synergy | --- |

### 통합/제거된 항목
- **단조증가 SortingOrder** -> [game-misc-notes.md](game-misc-notes.md) 항목 3 SortingOrder 레이어 상수가 SOT (수학적 색채 약함)
- **비대칭 적분 (Variable Gravity)** -> [game-technique-notes.md](game-technique-notes.md) 항목 1 Asymmetric Jump가 SOT (응용 기법 자체)

---