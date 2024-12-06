#secondroom_mode.py

from pico2d import *
import game_framework
import game_world
from game_framework import draw_room_name
from girl import Girl
from background import Background
from monster import Monster
from transition_box import TransitionBox
from stair import Stair

girl_position = (400, 700)  # 기본 초기 위치

def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)

def enter():
    global background, girl, transition_boxes, black_screen, stairs, monster

    # 기존 객체 제거
    game_world.clear()

    # 새로운 객체 생성
    background = Background('secondroom.png', 800, 400)  # 두 번째 방 배경 이미지
    girl = Girl()  # 소녀 객체 생성
    game_world.set_girl(girl)  # 소녀 객체를 game_world에 설정
    girl.set_y_bounds(210, 700)  # secondroom에서의 y 좌표 제한

    # 전환 박스들 생성
    transition_boxes = [
        TransitionBox(850, 700, 50, 50),  # 첫 번째 박스
        TransitionBox(0, 200, 50, 50),  # 두 번째 박스
        TransitionBox(1600, 200, 50, 50)  # 세 번째 박스
    ]
    black_screen = load_image('black.png')
    game_framework.set_room_name("room 1")

    stairs = [
        Stair(850, 400, 100, 500, 200, 850)  # 계단 1개
    ]

    # 저장된 몬스터 위치 확인
    monster_position = game_world.get_monster_position_for_room('rooftop')
    if monster_position:
        monster = Monster(*monster_position, girl)
    else:
        monster = Monster(800, 260, girl)  # 기본 위치

    game_world.set_monster_for_room('rooftop', monster)
    game_world.add_object(monster, 1)

    # 소녀의 초기 위치 설정
    girl.x, girl.y = girl_position

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(girl, 1)
    for stair in stairs:
        game_world.add_object(stair, 2)


def exit():
    global background
    del background
    global monster
    if monster:  # 몬스터가 존재하면 위치 저장
        game_world.set_monster_position_for_room('rooftop', (monster.x, monster.y))
        game_world.remove_monster_for_room('rooftop')
        del monster

def update():
    # 게임 월드 업데이트
    game_world.update()

    # 소녀의 위치 확인 및 화면 전환
    for i, transition_box in enumerate(transition_boxes):
        if check_for_transition(girl, transition_box):
            if i == 0:
                import rooftop2_mode
                rooftop2_mode.set_girl_position(1050, 210)  # Rooftop 초기 위치 설정
                game_framework.change_mode(rooftop2_mode)
            elif i == 1:
                import bathroom_mode
                bathroom_mode.set_girl_position(1300, 210)  # Bathroom 초기 위치 설정
                game_framework.change_mode(bathroom_mode)
            elif i == 2:
                import hall2_mode
                hall2_mode.set_girl_position(100, 250)  # Hall2 초기 위치 설정
                game_framework.change_mode(hall2_mode)

def draw():
    # 화면 그리기
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)
    game_world.render()
    game_framework.draw_room_name()
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
            girl.handle_event(event, stairs)

def check_for_transition(entity, transition_box):
    """소녀와 전환 박스 충돌 여부 확인"""
    entity_left = entity.x - entity.width // 2
    entity_bottom = entity.y - entity.height // 2
    entity_right = entity.x + entity.width // 2
    entity_top = entity.y + entity.height // 2

    box_left, box_bottom, box_right, box_top = transition_box.get_bb()

    # 충돌 여부 확인
    if entity_left > box_right or entity_right < box_left:
        return False
    if entity_bottom > box_top or entity_top < box_bottom:
        return False
    return True

def finish():
    pass
