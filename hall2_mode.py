from pico2d import *
import game_framework
import game_world
from girl import Girl, setup_walls
from background import Background
from transition_box import TransitionBox
from stair import Stair
from item import Potion

def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)

def enter():
    global background, girl, transition_boxes, black_screen, stairs, potion,fence

    # 기존 객체 제거
    game_world.clear()

    fence=load_image('fence2.png')

    # 새로운 객체 생성
    background = Background('upstair.png', 800, 400)  # hall2
    girl = Girl()  # 소녀 객체 생성
    game_world.set_girl(girl)  # 소녀 객체를 game_world에 설정
    girl.set_y_bounds(100, 210)  # hall2에서의 y 좌표 제한
    girl.set_x_bounds(0, 1600)  # hall2에서의 y 좌표 제한
    stairs = [
        Stair(150, 100, 300, 200, -50, 200),  # 계단 1개
        Stair(1450, 100, 300, 200, -50, 200)  # 계단 1개
    ]

    # 전환 박스들 생성
    transition_boxes = [
        TransitionBox(-50, 200, 50, 100),   # 첫 번째 전환 박스
        TransitionBox(100, 100, 150, 10),  # 두 번째 전환 박스
        TransitionBox(1500, 100, 150, 10)  # 세 번째 전환 박스
    ]
    black_screen = load_image('black.png')  # 검정 화면 배경
    game_framework.set_room_name("hall 2")
    map_walls = [

        (0, 280, 1600, 280),  # 가로벽: y1 == y2
        (0, 110, 0, 280),  # 가로벽: y1 == y2
        (1600, 110, 1600, 280),  # 가로벽: y1 == y2
        (200, 120, 1400, 120)  # 가로벽: y1 == y2
    ]
    # 벽 설정
    setup_walls(map_walls, girl)  # 벽 데이터 추가

    # 소녀가 들고 있는 아이템 복원
    holding_item = game_world.load_girl_holding_item()
    if holding_item:
        if game_world.is_item_used(holding_item.id):
            print(f"[DEBUG] Used item detected in girl's hand: {holding_item.id}")
            girl.set_holding_item(None)  # 들고 있는 아이템 초기화
            game_world.save_girl_holding_item(None)
        else:
            girl.set_holding_item(holding_item)

    # 포션 상태 확인 및 생성
    if not game_world.is_item_picked(2) and not game_world.is_item_used(2):
        potion = Potion(800, 230, 2)  # 포션 생성
        game_world.add_object(potion, 1)  # 게임 월드에 포션 추가
    else:
        potion = None  # 이미 픽업되었거나 사용된 경우 포션 생성하지 않음

    # 소녀 초기 위치
    girl.x, girl.y = girl_position

    # 게임 월드에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(girl, 1)
    for stair in stairs:
        game_world.add_object(stair, 2)

def exit():
    global background, potion
    del background

    # 포션이 픽업되었거나 사용되었는지 확인하고 상태 저장
    if potion and potion.picked_up:
        game_world.mark_item_picked(potion.id)

    # 소녀가 들고 있는 아이템 상태 저장
    if girl.holding_item:
        game_world.save_girl_holding_item(girl.holding_item)
    else:
        game_world.save_girl_holding_item(None)

    if potion:
        del potion  # 포션 객체 삭제

def update():
    global potion

    # 게임 월드 업데이트
    game_world.update()

    # 포션이 픽업되었으면 hall3로 전환
    if potion and potion.picked_up:
        print("[DEBUG] Potion picked, transitioning to hall3.")

        # 소녀가 들고 있는 아이템 상태 저장
        if girl.holding_item:
            game_world.save_girl_holding_item(girl.holding_item)

        # hall3로 전환
        game_world.set_hall3open(True)  # Hall3 이동 가능 상태 설정
        import hall3_mode
        hall3_mode.set_girl_position(girl.x, girl.y)
        game_framework.change_mode(hall3_mode)

    # 소녀의 위치 확인 및 화면 전환
    for i, transition_box in enumerate(transition_boxes):
        if check_for_transition(girl, transition_box):
            if i == 0:
                import secondroom_mode
                secondroom_mode.set_girl_position(1500, 210)
                game_framework.change_mode(secondroom_mode)
            elif i == 1:
                import hall1_mode
                hall1_mode.set_girl_position(150, 600)  # 첫 번째 Hall1 전환 위치
                game_framework.change_mode(hall1_mode)
            elif i == 2:
                import hall1_mode
                hall1_mode.set_girl_position(1500, 600)  # 두 번째 Hall1 전환 위치
                game_framework.change_mode(hall1_mode)

def draw():
    # 화면 그리기
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)  # 전체 화면에 검정 배경

    game_world.render()
    game_framework.draw_room_name()
    # 하트가 수집된 상태라면 화면 특정 위치에 그리기
    # 슬롯 및 하트 그리기
    game_world.draw_slots()

    # 각 TransitionBox의 히트박스 그리기
    #for transition_box in transition_boxes:
    #    transition_box.draw()
    fence.draw(800, 140, 1100, 80)
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

def check_for_transition(girl, transition_box):
    girl_left = girl.x - girl.width // 2
    girl_bottom = girl.y - girl.height // 2
    girl_right = girl.x + girl.width // 2
    girl_top = girl.y + girl.height // 2

    box_left = transition_box.x - transition_box.width // 2
    box_bottom = transition_box.y - transition_box.height // 2
    box_right = transition_box.x + transition_box.width // 2
    box_top = transition_box.y + transition_box.height // 2

    if girl_left > box_right or girl_right < box_left:
        return False
    if girl_bottom > box_top or girl_top < box_bottom:
        return False
    return True

def finish():
    pass
