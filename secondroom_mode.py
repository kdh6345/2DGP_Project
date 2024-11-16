from pico2d import *
import game_framework
import game_world
from girl import Girl
from background import Background
from transition_box import TransitionBox

def enter():
    global background, girl, transition_box

    # 기존 객체 제거
    game_world.clear()

    # 새로운 객체 생성
    background = Background('secondroom.png', 800, 400)  # 두 번째 방 배경 이미지
    girl = Girl()  # 소녀 객체 생성
    transition_box = TransitionBox(850, 1000, 50, 50)  # 전환 박스 생성

    # 소녀의 초기 위치 (전환 박스 밖)
    girl.x, girl.y = 900, 700

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(girl, 1)

def exit():
    global background
    del background

def update():
    # 소녀 및 게임 월드 업데이트
    game_world.update()

    # 소녀의 위치 확인 및 화면 전환
    if check_for_transition(girl):
        import rooftop_mode
        game_framework.change_mode(rooftop_mode)

def draw():
    # 화면 그리기
    clear_canvas()
    game_world.render()
    transition_box.draw()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            girl.handle_event(event)

def check_for_transition(girl):
    # TransitionBox와 소녀의 히트박스 비교
    girl_left = girl.x - girl.width // 2
    girl_bottom = girl.y - girl.height // 2
    girl_right = girl.x + girl.width // 2
    girl_top = girl.y + girl.height // 2

    box_left, box_bottom, box_right, box_top = transition_box.get_bb()

    # 충돌 여부 확인
    if girl_left > box_right or girl_right < box_left:
        return False
    if girl_bottom > box_top or girl_top < box_bottom:
        return False
    return True
def finish():
    pass