from math import hypot
from pathlib import Path
from time import perf_counter

from pico2d import *


CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 1024
SPRITE_WIDTH, SPRITE_HEIGHT = 100, 100
FRAME_COUNT = 8
ANIMATION_FPS = 10
MOVE_SPEED = 200
MAX_DELTA_TIME = 0.1
ASSET_DIR = Path(__file__).resolve().parent
MOVEMENT_KEYS = {SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN}

pressed_keys = set()
running = True
x, y = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2
facing = 1  # 오른쪽: 1, 왼쪽: -1
frame = 0
sprite_row = 300
animation_time = 0.0


def handle_events():
    global running

    events = get_events()
    # pico2d는 창 포커스 이벤트를 반환하지 않으므로 SDL에서 직접 확인한다.
    if not SDL_GetKeyboardFocus():
        pressed_keys.clear()
        events = [event for event in events if event.type == SDL_QUIT]
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in MOVEMENT_KEYS:
                pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            pressed_keys.discard(event.key)


def update_character(dt):
    global x, y, facing, frame, sprite_row, animation_time

    dt = max(0.0, min(dt, MAX_DELTA_TIME))
    horizontal = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    vertical = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    if horizontal:
        facing = horizontal

    previous_row = sprite_row
    moving = bool(horizontal or vertical)
    if moving:
        sprite_row = 100 if facing > 0 else 0
    else:
        sprite_row = 300 if facing > 0 else 200
    if sprite_row != previous_row:
        frame = 0
        animation_time = 0.0

    animation_time += dt
    frame_steps = int((animation_time + 1e-9) * ANIMATION_FPS)
    frame = (frame + frame_steps) % FRAME_COUNT
    animation_time = max(0.0, animation_time - frame_steps / ANIMATION_FPS)

    length = hypot(horizontal, vertical)
    if length:
        x += horizontal / length * MOVE_SPEED * dt
        y += vertical / length * MOVE_SPEED * dt
    # 중심 좌표를 반폭/반높이 안쪽으로 제한하여 소년 전체를 화면에 유지한다.
    x = max(SPRITE_WIDTH / 2, min(CANVAS_WIDTH - SPRITE_WIDTH / 2, x))
    y = max(SPRITE_HEIGHT / 2, min(CANVAS_HEIGHT - SPRITE_HEIGHT / 2, y))


def draw_scene(tuk_ground, character):
    clear_canvas()
    tuk_ground.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
                    CANVAS_WIDTH, CANVAS_HEIGHT)
    character.clip_draw(frame * SPRITE_WIDTH, sprite_row,
                        SPRITE_WIDTH, SPRITE_HEIGHT, x, y)
    update_canvas()


def main():
    global running, x, y, facing, frame, sprite_row, animation_time

    running = True
    pressed_keys.clear()
    x, y = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2
    facing, frame, sprite_row, animation_time = 1, 0, 300, 0.0
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    tuk_ground = character = None
    try:
        tuk_ground = load_image(str(ASSET_DIR / 'TUK_GROUND.png'))
        character = load_image(str(ASSET_DIR / 'animation_sheet.png'))
        last_time = perf_counter()
        while running:
            now = perf_counter()
            dt = now - last_time
            last_time = now
            handle_events()
            if not running:
                break
            update_character(dt)
            draw_scene(tuk_ground, character)
            delay(0.01)
    finally:
        # SDL 렌더러를 닫기 전에 텍스처를 해제한다.
        del character, tuk_ground
        close_canvas()


if __name__ == '__main__':
    main()
