# LEC10 입력 처리 실습 준비

확인일: 2026-10-07. 강의 자료: `../../Slides/LEC10_입력처리.pdf` (23쪽).
강의 PDF의 텍스트와 실습 예제 3개를 확인했다. 이 문서는 준비용이며 예제의 빈칸은 아직 구현하지 않았다.

## 핵심 흐름 (3쪽)

1. `get_events()`로 발생한 이벤트 목록을 가져온다.
2. `for event in events`에서 `event.type`으로 종류를 구분한다.
3. 해당 종류의 입력값(`event.key`, `event.x`, `event.y` 등)을 읽는다.
4. 종료 여부나 위치·방향 상태를 변경한다. 메인 루프는 그 상태로 화면을 갱신한다.

`handle_events()`는 매 루프마다 호출한다. 함수에서 바깥 변수에 값을 대입하면 `global running, x, y`처럼 선언해야 한다. 필요한 변수만 선언한다.

| 이벤트 | 읽는 값 | 용도 |
| --- | --- | --- |
| `SDL_QUIT` | 별도 입력값 없음 | 창 닫기 |
| `SDL_KEYDOWN` | `event.key` | 키 누름, ESC 종료 |
| `SDL_KEYUP` | `event.key` | 키 뗌, 연속 이동 중단 |
| `SDL_MOUSEMOTION` | `event.x`, `event.y` | 마우스 위치 추적 |
| `SDL_MOUSEBUTTONDOWN/UP` | `event.button`, `event.x`, `event.y` | 클릭·버튼 해제 |
| `SDL_MOUSEWHEEL` | 강의 표에서는 `event.wheel.x/y` | 휠 스크롤; 이번 예제에서는 사용하지 않음 |

주요 키 상수는 `SDLK_ESCAPE`, `SDLK_LEFT`, `SDLK_RIGHT`. 버튼 상수는 `SDL_BUTTON_LEFT`, `SDL_BUTTON_MIDDLE`, `SDL_BUTTON_RIGHT` (8~9쪽).

## 실습 순서와 채울 위치

### 1. `character_runs_esc.py`: ESC 종료 (4~11쪽)

- 함수 밖에 `running = True`를 둔다.
- `handle_events()`에서 `global running`을 선언한다.
- `SDL_QUIT` 또는 `SDL_KEYDOWN` + `SDLK_ESCAPE`이면 `running = False`.
- 기존 `for x in range(0, 800, 5)` 루프에서 `update_canvas()` 다음에 `handle_events()`를 호출한다.
- 바로 뒤에 `if not running: break`를 넣는다. `for` 루프는 `running`을 바꾸는 것만으로 중단되지 않는다.
- 애니메이션은 `frame = (frame + 1) % 8`, `delay(0.05)`를 유지한다.

### 2. `move_character_with_key.py`: 좌우 이동 (12~17쪽)

먼저 기본 이동(13~14쪽)을 완성한다.

- `handle_events()`에서 `global running, x`.
- 오른쪽 `KEYDOWN`: `x += 10`, 왼쪽: `x -= 10`, ESC: 종료.
- `running = True`, `x = 800 // 2`, `frame = 0`은 이미 있다.
- 마지막 빈칸에 `while running` 루프: 화면 지우기 → 잔디·캐릭터 그리기 → 화면 갱신 → 입력 처리 → 프레임 증가 → 지연.
- 기본 예제의 클립 영역은 `(frame * 100, 100, 100, 100)`, 표시 위치는 `(x, 90)`.

이어서 연속 이동(15~17쪽)으로 바꾼다.

- `dir = 0` 초기화. `dir`은 방향 상태: 오른쪽 `+1`, 왼쪽 `-1`, 중립 `0`.
- 함수 선언은 `global running, dir`로 바꾼다. 위치 갱신은 메인 루프에서 한다.
- 아래 표처럼 누름과 해제를 짝지어 처리한다.
- 메인 루프에 `x += dir * 5`를 넣는다. 강의 16쪽의 클립 Y값은 `0`이다(기본 예제의 `100`과 다름).

| 키 | `KEYDOWN` | `KEYUP` |
| --- | --- | --- |
| 오른쪽 | `dir += 1` | `dir -= 1` |
| 왼쪽 | `dir -= 1` | `dir += 1` |

기본 이동은 키 입력 이벤트마다 위치를 변경하고, 연속 이동은 방향을 저장해서 매 루프마다 위치를 변경한다. 양쪽 키를 함께 누르면 방향이 상쇄되고, 한쪽을 떼면 남은 키 방향으로 움직이는지 확인한다.

### 3. `move_character_with_mouse.py`: 마우스 추적 (18~23쪽)

- 맨 위 빈칸: `TUK_WIDTH, TUK_HEIGHT = 1280, 1024`, `open_canvas(TUK_WIDTH, TUK_HEIGHT)`, `tuk_ground = load_image('TUK_GROUND.png')`.
- `handle_events()`에서 `global running, x, y`.
- `SDL_MOUSEMOTION`에서 `x, y = event.x, TUK_HEIGHT - 1 - event.y`.
- 창 닫기·ESC 종료도 처리한다.
- 루프 전 빈칸: `x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2`, `hide_cursor()`.
- 그리기 빈칸: 배경을 화면 중앙에 그리고, 캐릭터를 `(x, y)`에 그린다.
- 강의 클립 영역은 `(frame * 100, 100, 100, 100)`.

좌표 원점이 다르다. 마우스 좌표는 왼쪽 위, pico2d는 왼쪽 아래이므로 **`y = 높이 - 1 - event.y`**로 뒤집는다. 높이 1024에서 마우스 Y=0은 화면 Y=1023, Y=1023은 화면 Y=0이 된다.

## 실행 준비와 빠른 확인

예제는 이미지 경로가 상대 경로이므로 저장소 루트에서 파일 경로만 지정해 실행하면 이미지 로딩이 실패할 수 있다. 실습 폴더로 이동해서 실행한다.

```powershell
cd Labs/LEC10_HandlingInputs
python character_runs_esc.py
python move_character_with_key.py
python move_character_with_mouse.py
```

위 실행은 각각 해당 빈칸을 완성한 뒤 진행한다. 현재 `pico2d` 설치 여부와 필요한 이미지 파일의 존재는 확인했으며, GUI 실행 검증은 하지 않았다.

- 공통: 창 닫기와 ESC가 동작하는가? `handle_events()`를 매 루프 호출하는가?
- 키보드: 좌우 입력, 키를 뗐을 때 정지, 양쪽 키를 함께 누른 뒤 하나를 떼는 상황을 확인한다.
- 마우스: 위·아래로 움직일 때 캐릭터가 같은 방향으로 따라가는가? 배경·창 크기는 1280×1024인가?
- `global` 누락, 초기 위치 누락, `KEYUP` 누락, Y좌표 변환 누락을 먼저 확인한다.
- 강의의 `dir` 누적 방식은 누름/해제가 짝을 이룬다는 전제다. 반복 KEYDOWN이 발생해 방향값이 누적된다면 이후 확장에서 눌린 키 상태를 따로 관리할 수 있다.
- 화면 경계 제한과 이동 방향별 스프라이트 선택은 현재 예제에 구현되어 있지 않으므로 별도 요구가 나오면 추가한다.

## LEC09 Sonic 코드에 연결할 때 참고

`../LEC09/sonic_animation_viewer.py`의 `main()`은 이미 매 루프 `get_events()`를 처리하고 창 닫기·ESC 종료를 지원한다. `AnimationPlayer.update(dt)`는 자동 이동과 동작 순환을 담당한다.

Sonic에 입력 이동을 추가하는 요구가 나오면 먼저 자동 이동을 대체할지, 어떤 동작을 키에 연결할지 정한 뒤 입력 상태와 위치 갱신을 연결한다. 마우스 변환에는 그 코드의 `CANVAS_HEIGHT`(720)를 사용한다. 현재 Sonic 코드는 변경하지 않았다.
