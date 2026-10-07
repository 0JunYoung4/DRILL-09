from pico2d import *


CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 1024
SPRITE_WIDTH, SPRITE_HEIGHT = 100, 100
FRAME_COUNT = 8

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
grass = load_image('grass.png')
character = load_image('animation_sheet.png')


def handle_events():
    global running, dir

    # fill here
    global x
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        # fill here
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir +=1
            elif event.key == SDLK_LEFT:
                dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1

running = True
x = 800 // 2
frame = 0
dir = 0

# fill here
while running:
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame*100, 100,100,100,x,90)
    update_canvas()
    handle_events()
    frame = (frame + 1) % FRAME_COUNT
    x += dir * 5
    delay(0.05)

close_canvas()

