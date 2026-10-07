from pathlib import Path
from time import perf_counter
from math import hypot

from pico2d import *


CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 1024
SPRITE_WIDTH, SPRITE_HEIGHT = 100, 100
FRAME_COUNT = 8
ANIMATION_FPS = 10
MOVE_SPEED = 200
MAX_DELTA_TIME = 0.1

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
ASSET_DIR = Path(__file__).resolve().parent
tuk_ground = load_image(str(ASSET_DIR / 'TUK_GROUND.png'))
character = load_image(str(ASSET_DIR / 'animation_sheet.png'))


pressed_keys = set()
MOVEMENT_KEYS = {SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN}


def handle_events():
    global running

    events = get_events()
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

running = True
x, y = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2
frame = 0
dir = 0
facing = 1  # ???: 1, ??: -1
sprite_row = 300
animation_time = 0.0
last_time = perf_counter()

# fill here
while running:
    now = perf_counter()
    dt = min(now - last_time, MAX_DELTA_TIME)
    last_time = now
    clear_canvas()
    tuk_ground.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
                    CANVAS_WIDTH, CANVAS_HEIGHT)
    character.clip_draw(frame * SPRITE_WIDTH, sprite_row,
                        SPRITE_WIDTH, SPRITE_HEIGHT, x, y)
    update_canvas()
    handle_events()
    dir = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    vertical = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    if dir:
        facing = dir
    previous_row = sprite_row
    moving = bool(dir or vertical)
    sprite_row = (100 if facing > 0 else 0) if moving else (300 if facing > 0 else 200)
    if sprite_row != previous_row:
        frame = 0
        animation_time = 0.0
    animation_time += dt
    frame_steps = int(animation_time * ANIMATION_FPS)
    frame = (frame + frame_steps) % FRAME_COUNT
    animation_time -= frame_steps / ANIMATION_FPS
    length = hypot(dir, vertical)
    if length:
        x += dir / length * MOVE_SPEED * dt
        y += vertical / length * MOVE_SPEED * dt
    x = max(SPRITE_WIDTH / 2, min(CANVAS_WIDTH - SPRITE_WIDTH / 2, x))
    y = max(SPRITE_HEIGHT / 2, min(CANVAS_HEIGHT - SPRITE_HEIGHT / 2, y))
    delay(0.01)

close_canvas()

