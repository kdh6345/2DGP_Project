#play_mode.py
from pico2d import *
import game_framework

import game_world
from background import Background
from girl import Girl

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            girl.handle_event(event)

def init():
    global back
    global girl

    back=Background()
    game_world.add_object(back, 0)

    girl=Girl()
    game_world.add_object(girl, 1)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

