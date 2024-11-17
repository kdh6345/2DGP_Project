from pico2d import *
import game_framework
import game_world
from girl import Girl
from stair import Stair
from background import Background
from transition_box import TransitionBox

def enter():
    global girl, background, transition_box, stairs, black_screen

    # 기존 객체 제거
    game_world.clear()

    # 새로운 객체 생성
    background = Background('start room1.png', 800, 400)  # 옥상 배경 이미지
    girl = Girl()  # 소녀 객체 생성
    transition_box = TransitionBox(1050, -50, 100, 50)  # 전환 박스 생성
    black_screen = load_image('black.png')

    # 계단 리스트 생성
    stairs = [
        Stair(1050, 100, 100, 100)  # 계단 1개
    ]

    # 소녀의 초기 위치 설정
    girl.x, girl.y = 400, 200

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(girl, 1)
    for stair in stairs:
        game_world.add_object(stair, 2)

def exit():
    global background
    del background

def update():
    global girl

    # 소녀의 상태 업데이트
    game_world.update()

    # 소녀의 위치 확인 및 화면 전환
    if check_for_transition(girl):
        import secondroom_mode
        secondroom_mode.set_girl_position(850, 700)  # Secondroom에서 소녀의 초기 위치 설정
        game_framework.change_mode(secondroom_mode)

def draw():
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)
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
            # girl과 stairs를 전역 변수로 사용
            girl.handle_event(event, stairs)

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

def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)