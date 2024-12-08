from pico2d import *
import game_framework
import game_world
from girl import Girl, Wall, setup_walls
from item import Key
from stair import Stair
from background import Background, Fence
from transition_box import TransitionBox
from game_framework import set_room_name

# 소녀의 초기 위치를 저장하는 변수
girl_position = (400, 200)
open_jail = False  # Jail 상태를 나타내는 플래그


def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)


def enter():
    global girl, background, transition_box, stairs, black_screen, key, fence

    # 기존 객체 제거
    game_world.clear()
    girl = Girl()  # 소녀 객체 생성
    game_world.set_girl(girl)  # 소녀 객체를 game_world에 설정

    # 맵에 설치할 벽 데이터 (x1, y1, x2, y2)
    map_walls = [
        (260, 100, 270, 300),  # 가로벽
        (560, 100, 570, 300),  # 세로벽
        (290, 110, 560, 120),  # 또 다른 가로벽
        (290, 250, 560, 250)   # 또 다른 가로벽
    ]

    # 벽 설정
    setup_walls(map_walls, girl)  # 벽 데이터 추가

    # 새로운 객체 생성
    background = Background('start room1.png', 800, 400)  # 닫힌 Jail 배경
    set_room_name("Rooftop", 2.0)  # 방 이름과 표시 시간 설정
    fence = Fence()

    # 키 생성 조건 추가
    if not game_world.is_item_used(0):  # Key ID가 1이라고 가정
        key = Key(300, 150)  # 키 위치와 ID 설정
        game_world.add_object(key, 1)
    else:
        key = None  # 키를 생성하지 않음

    transition_box = TransitionBox(1050, 100, 100, 10)  # 전환 박스 생성
    black_screen = load_image('black.png')

    # 계단 리스트 생성
    stairs = [
        Stair(1050, 200, 100, 200, -50, 200)  # 계단 1개
    ]

    # 소녀의 초기 위치 설정
    girl.x, girl.y = girl_position

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
    global girl

    # 게임 월드 업데이트
    game_world.update()

    # Jail 열림 확인
    if open_jail:
        import rooftop2_mode
        rooftop2_mode.set_girl_position(girl.x, girl.y)
        game_framework.change_mode(rooftop2_mode)

    # 소녀의 위치 확인 및 화면 전환
    if check_for_transition(girl):
        girl_position = (1050, 100)
        import secondroom_mode
        secondroom_mode.set_girl_position(850, 600)  # Secondroom에서 소녀의 초기 위치 설정
        game_framework.change_mode(secondroom_mode)


def draw():
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)  # 배경 그리기
    game_world.render()
    #transition_box.draw()  # 전환 박스 그리기
    # 방 이름 그리기
    game_framework.draw_room_name()
    # 슬롯 및 하트 그리기
    game_world.draw_slots()

    update_canvas()


def handle_events():
    global girl
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

    box_left = transition_box.x - transition_box.width // 2
    box_bottom = transition_box.y - transition_box.height // 2
    box_right = transition_box.x + transition_box.width // 2
    box_top = transition_box.y + transition_box.height // 2

    # 충돌 여부 확인
    if girl_left > box_right or girl_right < box_left:
        return False
    if girl_bottom > box_top or girl_top < box_bottom:
        return False
    return True


def finish():
    pass
