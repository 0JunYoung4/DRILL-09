from pathlib import Path

from pico2d import *


CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 1024
SPRITE_WIDTH, SPRITE_HEIGHT = 100, 100
FRAME_COUNT = 8

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
ASSET_DIR = Path(__file__).resolve().parent
tuk_ground = load_image(str(ASSET_DIR / 'TUK_GROUND.png'))
character = load_image(str(ASSET_DIR / 'animation_sheet.png'))


pressed_keys = set()
MOVEMENT_KEYS = {SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN}


def handle_events():
    global running

    for event in get_events():
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

# fill here
while running:
    clear_canvas()
    tuk_ground.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
                    CANVAS_WIDTH, CANVAS_HEIGHT)
    character.clip_draw(frame * SPRITE_WIDTH, 100,
                        SPRITE_WIDTH, SPRITE_HEIGHT, x, y)
    update_canvas()
    handle_events()
    frame = (frame + 1) % FRAME_COUNT
    dir = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    vertical = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    x += dir * 5
    y += vertical * 5
    delay(0.05)

close_canvas()

