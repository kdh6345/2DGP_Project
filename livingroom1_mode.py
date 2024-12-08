from pico2d import *
import game_framework
import game_world
from girl import Girl
from monster import Monster
from background import Background
from stair import Stair
from transition_box import TransitionBox
living_monster=True
potion_used=False

def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)

def enter():
    global background, girl, monster, transition_boxes, black_screen, stairs
    global living_monster, potion_used

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

    # 소녀가 들고 있는 아이템 복원
    holding_item = game_world.load_girl_holding_item()
    if holding_item:
        if game_world.is_item_used(holding_item.id):
            print(f"[DEBUG] Used item detected in girl's hand: {holding_item.id}")
            girl.set_holding_item(None)  # 들고 있는 아이템 초기화
            game_world.save_girl_holding_item(None)
        else:
            girl.set_holding_item(holding_item)

    # 몬스터 생성 여부 확인
    if living_monster and not game_world.is_item_used(3):  # 'hall1_monster'가 죽지 않은 경우
        monster = Monster(800, 250, girl, 3)
        game_world.set_monster_for_room('hall1', monster)
        game_world.add_object(monster, 1)
    else:
        monster = None

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

    if living_monster and monster:
        game_world.set_monster_position_for_room('living room', (monster.x, monster.y))
        game_world.remove_monster_for_room('living room')
        del monster

        # 소녀가 들고 있는 아이템 상태 저장
    if girl.holding_item:
        game_world.save_girl_holding_item(girl.holding_item)
    else:
        game_world.save_girl_holding_item(None)


def update():
    global monster, living_monster
    # 소녀와 몬스터 업데이트
    game_world.update()

    # 몬스터 상태 확인
    if monster:
        if monster.is_dying and monster.dying_time > 1.0:
            hall1 = True  # 몬스터 제거 후 다시 생성 가능 상태로 설정
            game_world.remove_object(monster)
            game_world.remove_monster_for_room('living room')  # 해당 방에서 몬스터 제거
            print("Monster removed from living room.")

    # 소녀의 위치 확인 및 화면 전환
    for i, transition_box in enumerate(transition_boxes):
        if check_for_transition(girl, transition_box):
            if i == 0:
                import hall1_mode
                hall1_mode.set_girl_position(1500, 200)
                game_framework.change_mode(hall1_mode)
            elif i == 1:
                if game_world.are_all_slots_filled():
                    import livingroom3_mode
                    livingroom3_mode.set_girl_position(200, 210)
                    game_framework.change_mode(livingroom3_mode)
                else:
                    import livingroom2_mode
                    livingroom2_mode.set_girl_position(200, 210)
                    game_framework.change_mode(livingroom2_mode)


def draw():
    # 화면 그리기
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)  # 검정 배경
    game_world.render()
    game_framework.draw_room_name()
    # 하트가 수집된 상태라면 화면 특정 위치에 그리기
    # 슬롯 및 하트 그리기
    game_world.draw_slots()
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
