from pico2d import *
import game_framework
import game_world
from girl import Girl
from background import Background
from transition_box import TransitionBox

def enter():
    global background, girl, transition_boxes,black_screen

    # 기존 객체 제거
    game_world.clear()

    # 새로운 객체 생성
    background = Background('secondroom.png', 800, 400)  # 두 번째 방 배경 이미지
    girl = Girl()  # 소녀 객체 생성
    # 전환 박스들 생성
    transition_boxes = [
        TransitionBox(850, 1000, 50, 50),  # 첫 번째 박스
        TransitionBox(0, 200, 50, 50),  # 두 번째 박스
        TransitionBox(1600, 200, 50, 50)  # 세 번째 박스
    ]
    black_screen = load_image('black.png')

    # 소녀의 초기 위치 (전환 박스 밖)
    girl.x, girl.y = 870, 700

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
                import rooftop_mode
                game_framework.change_mode(rooftop_mode)
            elif i == 1:
                # 다른 모드로 전환
                #화장실 구현
                print("Transition to mode 2")
            elif i == 2:
                # 또 다른 모드로 전환
                # 2층 홀 구현
                print("Transition to mode 3")

def draw():
    # 화면 그리기
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)
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