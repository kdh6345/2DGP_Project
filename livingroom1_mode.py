from pico2d import *
import game_framework
import game_world
from girl import Girl
from monster import Monster
from background import Background
from stair import Stair
from transition_box import TransitionBox

def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)

def enter():
    global background, girl, monster, transition_boxes, black_screen, stairs

    # 기존 객체 제거
    game_world.clear()

    # 새로운 객체 생성
    background = Background('livingroom1.png', 800, 400)  # 홀 이미지 생성
    girl = Girl()  # 소녀 객체 생성
    game_world.set_girl(girl)  # 소녀 객체를 game_world에 설정
    girl.set_y_bounds(200, 700)  # y 좌표 제한
    stairs=[]


    transition_boxes = [

        TransitionBox(100, 200, 10, 100),
        TransitionBox(1500, 200, 10, 100),

    ]

    # 몬스터 생성 (맵 내 자유롭게 돌아다니도록 설정)


    black_screen = load_image('black.png')  # 검정 화면 배경
    game_framework.set_room_name("living room")
    # 소녀 초기 위치
    girl.x, girl.y = girl_position

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(girl, 1)

def exit():
    global background
    del background

def update():
    # 소녀와 몬스터 업데이트
    game_world.update()

    # 소녀의 위치 확인 및 화면 전환
    for i, transition_box in enumerate(transition_boxes):
        if check_for_transition(girl, transition_box):
            if i == 0:
                import hall1_mode
                hall1_mode.set_girl_position(1500, 200)
                game_framework.change_mode(hall1_mode)
            elif i == 1:
                import livingroom2_mode
                livingroom2_mode.set_girl_position(200, 200)
                game_framework.change_mode(livingroom2_mode)


def draw():
    # 화면 그리기
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)  # 검정 배경
    game_world.render()
    game_framework.draw_room_name()
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

def check_for_transition(obj, transition_box):
    obj_left = obj.x - obj.width // 2
    obj_bottom = obj.y - obj.height // 2
    obj_right = obj.x + obj.width // 2
    obj_top = obj.y + obj.height // 2

    box_left, box_bottom, box_right, box_top = transition_box.get_bb()

    if obj_left > box_right or obj_right < box_left:
        return False
    if obj_bottom > box_top or obj_top < box_bottom:
        return False
    return True

def finish():
    pass
