#bathroom_mode.py
from pico2d import *
import game_framework
import game_world
from girl import Girl
from background import Background
from monster import Monster
from transition_box import TransitionBox
from item import Potion

def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)

def enter():
    global background, girl, transition_box, black_screen,stairs,key, potion

    # 기존 객체 제거
    game_world.clear()

    # 새로운 객체 생성
    background = Background('bathroom.png', 800, 440)  # 화장실 배경 이미지
    girl = Girl()  # 소녀 객체 생성
    game_world.set_girl(girl)

    # 포션 상태 확인 및 복원
    if not game_world.is_item_used(1):  # 아이템 ID 1인 포션이 습득되지 않았다면 생성
        potion = Potion(550, 200, 1)  # 포션 생성 (ID = 1)
        game_world.add_object(potion, 1)  # 포션을 게임 월드에 추가
    else:
        potion = None  # 이미 습득된 경우 포션을 생성하지 않음

    transition_box = TransitionBox(1600, 200, 100, 100)  # 전환 박스 생성
    black_screen = load_image('black.png')  # 검정 화면 배경
    game_framework.set_room_name("bathroom")
    stairs=[]

    girl.set_y_bounds(210, 250)  # secondroom에서의 y 좌표 제한
    girl.set_x_bounds(550, 1500)  # secondroom에서의 y 좌표 제한
    #key = Key2(560, 300)  # 키 위치 설정

    # 소녀 초기 위치
    girl.x, girl.y = girl_position  # 전환 박스 밖

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(girl, 1)
    game_world.add_object(potion, 1)  # 포션 추가
    #game_world.add_object(key, 1)


def exit():
    global background
    del background

def update():
    # 소녀 및 게임 월드 업데이트
    game_world.update()

    global potion
    # 포션 상태 업데이트 및 제거 처리
    if potion and potion.throwing and (potion.x < 0 or potion.x > 1600):  # 화면 밖으로 나가면
        print("Potion went out of bounds and is removed.")
        game_world.remove_object(potion)
        potion = None

    # 소녀의 위치 확인 및 화면 전환
    if check_for_transition(girl, transition_box):
        import secondroom_mode
        # 소녀의 위치 설정 후 모드 전환
        secondroom_mode.set_girl_position(100, 210)
        game_framework.change_mode(secondroom_mode)

def draw():
    # 화면 그리기
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)  # 전체 화면에 검정 배경
    game_world.render()
    game_framework.draw_room_name()
    # 슬롯 및 하트 그리기
    game_world.draw_slots()
    if potion and not potion.picked_up:  # 포션이 습득되지 않은 경우만 그리기
        potion.draw()
    # TransitionBox의 히트박스 그리기
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
            girl.handle_event(event,stairs)

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
