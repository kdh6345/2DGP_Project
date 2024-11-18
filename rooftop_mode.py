#rooftop_mode.py
from pico2d import *
import game_framework
import game_world
from girl import Girl
from item import Key
from monster import Monster
from stair import Stair
from background import Background,Fence
from transition_box import TransitionBox

# 소녀의 초기 위치를 저장하는 변수
girl_position = (400, 200)
open_jail=False

def set_girl_position(x, y):

    global girl_position
    girl_position = (x, y)

def enter():
    global girl, background, transition_box, stairs, black_screen, key, fence

    # 기존 객체 제거
    game_world.clear()
    girl = Girl()  # 소녀 객체 생성
    girl.set_y_bounds(100, 200)  # rooftop에서의 y 좌표 제한
    key = Key(300, 150)  # 키 위치 설정 (x=700, y=150)

    # 새로운 객체 생성
    if not open_jail:
        background = Background('start room1.png', 800, 400)  # 닫힌 Jail 배경
        girl.set_x_bounds(300, 550)
    else:
        background = Background('start room2.png', 800, 400)  # 열린 Jail 배경
        girl.set_x_bounds(300, 1600)

    fence = Fence()  # 철창 객체 생성
    transition_box = TransitionBox(1050, 100, 100, 10)  # 전환 박스 생성
    black_screen = load_image('black.png')

    if not open_jail:
        key = Key(300, 150)  # 키 위치 설정
        game_world.add_object(key, 1)

    # 계단 리스트 생성
    stairs = [
        Stair(1050, 200, 100, 200,-50,200)  # 계단 1개
    ]

    # 소녀의 초기 위치 설정
    girl.x, girl.y =  girl_position

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(key, 1)

    game_world.add_object(girl, 1)
    game_world.add_object(fence, 2)
    for stair in stairs:
        game_world.add_object(stair, 2)

def exit():
    global background
    del background

def update():
    global girl, key

    # 소녀와 키 상태 업데이트
    game_world.update()

    # 키 업데이트 (소녀와의 충돌 처리)
    key.update()

    # 소녀의 위치 확인 및 화면 전환
    if check_for_transition(girl):
        girl_position = (1050, 100)
        import secondroom_mode
        secondroom_mode.set_girl_position(850, 600)  # Secondroom에서 소녀의 초기 위치 설정
        game_framework.change_mode(secondroom_mode)

def draw():
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)
    game_world.render()
    transition_box.draw()
    update_canvas()

def handle_events():
    global girl, key
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
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

