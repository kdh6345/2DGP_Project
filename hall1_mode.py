from pico2d import *
import game_framework
import game_world
from girl import Girl
from background import Background
from transition_box import TransitionBox

def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)

def enter():
    global background, girl, transition_boxes, black_screen

    # 기존 객체 제거
    game_world.clear()

    # 새로운 객체 생성
    background = Background('hall.png', 800, 400)  #홀 이미지 생성
    girl = Girl()  # 소녀 객체 생성

    # 전환 박스들 생성
    transition_boxes = [
        TransitionBox(-50, 200, 100, 100),   # 첫 번째 전환 박스
        TransitionBox(100, 850, 100, 100),    # 두 번째 전환 박스
        TransitionBox(1500, 850, 100, 100),    # 세 번째 전환 박스
        TransitionBox(1650, 200, 100, 100)  # 네 번째 전환 박스
    ]
    black_screen = load_image('black.png')  # 검정 화면 배경

    # 소녀 초기 위치
    girl.x, girl.y = girl_position

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
    for i, transition_box in enumerate(transition_boxes):
        if check_for_transition(girl, transition_box):
            if i == 0:
                import secondroom_mode
                secondroom_mode.set_girl_position(1500, 200)
                game_framework.change_mode(secondroom_mode)
            elif i == 1:
                import hall2_mode
                hall2_mode.set_girl_position(200, 200)  # 첫 번째 Hall1 전환 위치
                game_framework.change_mode(hall2_mode)
            elif i == 2:
                import hall2_mode
                hall2_mode.set_girl_position(1400, 200)  # 두 번째 Hall1 전환 위치
                game_framework.change_mode(hall2_mode)

def draw():
    # 화면 그리기
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)  # 전체 화면에 검정 배경
    game_world.render()
    # 각 TransitionBox의 히트박스 그리기
    for transition_box in transition_boxes:
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

def check_for_transition(girl, transition_box):
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
