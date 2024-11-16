from pico2d import *
import game_framework

import game_world
from background import Background, Fence
from girl import Girl

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
    global fence

    # Background 객체 추가
    back = Background()
    game_world.add_object(back, 0)  # 배경을 가장 아래 레이어에 추가

    # Girl 객체 추가
    girl = Girl()
    game_world.add_object(girl, 1)  # 소녀를 두 번째 레이어에 추가

    # Fence 객체 추가
    fence = Fence()
    game_world.add_object(fence, 3)  # Fence를 가장 위 레이어에 추가

def finish():
    game_world.clear()

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
