#secondroom_mode.py

from pico2d import *
import game_framework
import game_world
from girl import Girl, setup_walls
from background import Background
from item import Potion
from monster import Monster
from obstacle import Obstacle
#from obstacle import Obstacle
from transition_box import TransitionBox
from stair import Stair

font = None  # 폰트 객체

girl_position = (800, 700)  # 기본 초기 위치
secondroom_monster = True  # 전역 변수로 몬스터 상태 관리
potion_used = False  # 포션 사용 여부를 초기화
monster_walk_sound = None  # 몬스터 걷기 사운드
is_monster_walk_sound_playing = False  # 사운드 상태 확인 변수


def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)

def enter():
    global background, girl, transition_boxes, black_screen, stairs, potion, monster,papers
    global secondroom_monster,potion_used,obstacle
    global monster_walk_sound, is_monster_walk_sound_playing
    global font
    font = load_font('ENCR10B.TTF', 24)  # 폰트 로드

    # 기존 객체 제거
    game_world.clear()
    #game_world.init_slot_images()  # 슬롯 및 하트 이미지 초기화
    # 새로운 객체 생성
    background = Background('secondroom.png', 800, 400)  # 두 번째 방 배경 이미지
    girl = Girl()  # 소녀 객체 생성
    papers=Papers(1150,220)
    game_world.add_object(papers, 2)  # 레이어 2번에 추가
    obstacle = Obstacle(1150, 220, 200, 150)  # x, y, width, height
    game_world.add_obstacle(obstacle)  # 장애물을 game_world에 등록
    game_world.add_object(obstacle, 2)  # 레이어 2번에 추가

    game_world.set_girl(girl)  # 소녀 객체를 game_world에 설정

    map_walls = [
        (750, 300, 750, 800),  # 세로벽: x1 == x2
        (980, 300, 980, 800),  # 세로벽: x1 == x2
        (1610, 200, 1610, 300),
        (0, 280, 780, 280),  # 가로벽: y1 == y2
        (950, 280, 1600, 280),  # 가로벽: y1 == y2
        (0, 150, 1600, 150)  # 가로벽: y1 == y2
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


    # 몬스터 걷기 사운드 설정
    monster_walk_sound = load_music('monster_walk.wav')
    monster_walk_sound.set_volume(50)
    monster_walk_sound.repeat_play()
    is_monster_walk_sound_playing = True
    # 포션 상태 확인 및 생성
    if not game_world.is_item_used(1):  # 포션 ID가 사용되지 않은 경우에만 생성
        potion = game_world.load_potion_state()
        if potion:
            game_world.add_object(potion, 1)
    else:

        potion = None

    # 전환 박스들 생성
    transition_boxes = [
        TransitionBox(850, 700, 50, 50),
        TransitionBox(0, 200, 50, 50),
        TransitionBox(1600, 200, 50, 50)
    ]
    black_screen = load_image('black.png')
    game_framework.set_room_name("room 1")
    game_framework.set_sent_message("you can't enter yet..")

    stairs = [
        #Stair(850, 400, 100, 500, 200, 850)
    ]

    # 몬스터 생성
    if secondroom_monster and not game_world.is_item_used(1):  # 포션이 사용되지 않은 경우
        monster = Monster(800, 275, girl,1)

        game_world.set_monster_for_room('secondroom', monster)
        game_world.add_object(monster, 1)
        is_monster_walk_sound_playing = True
    else:
        monster = None

    # 소녀의 초기 위치 설정
    girl.x, girl.y = girl_position

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(girl, 3)
    game_world.add_object(papers, 2)

    for stair in stairs:
        game_world.add_object(stair, 2)


def exit():
    global background, monster_walk_sound, is_monster_walk_sound_playing
    del background
    global monster,potion
    # 몬스터 걷기 사운드 정지
    if monster_walk_sound and is_monster_walk_sound_playing:
        monster_walk_sound.stop()
        is_monster_walk_sound_playing = False

    if potion and potion.picked_up:  # 포션을 들었다면 사용 상태로 기록
        game_world.mark_item_used(potion.id)

    if secondroom_monster and monster:  # 몬스터가 존재하면 위치 저장
        game_world.set_monster_position_for_room('rooftop', (monster.x, monster.y))
        game_world.remove_monster_for_room('rooftop')
        del monster
        # 소녀가 들고 있는 포션 상태 저장
        if girl.holding_item and isinstance(girl.holding_item, Potion):
            game_world.save_potion_state(girl.holding_item)
            del potion

def update():
    global secondroom_monster, is_monster_walk_sound_playing

    # 게임 월드 업데이트
    game_world.update()

    # 몬스터 걷기 사운드 상태 관리
    if monster and not monster.is_dying:
        if monster.is_moving():  # 몬스터가 움직이는 상태인지 확인
            if not is_monster_walk_sound_playing:
                monster_walk_sound.repeat_play()
                is_monster_walk_sound_playing = True
        else:
            if is_monster_walk_sound_playing:
                monster_walk_sound.stop()
                is_monster_walk_sound_playing = False
    else:
        # 몬스터가 없거나 죽었으면 사운드 정지
        if is_monster_walk_sound_playing:
            monster_walk_sound.stop()
            is_monster_walk_sound_playing = False

    # 몬스터 제거 로직
    if monster and monster.is_dying:
        if monster.dying_time > 1.0:  # 죽은 후 일정 시간이 지나면 제거
            game_world.remove_object(monster)
            game_world.remove_monster_for_room('secondroom')
            secondroom_monster = False
            print("Monster removed from secondroom.")

    # 소녀의 위치 확인 및 화면 전환
    for i, transition_box in enumerate(transition_boxes):
        if check_for_transition(girl, transition_box):
            if i == 0:
                import rooftop2_mode
                rooftop2_mode.set_girl_position(1050, 210)
                game_framework.change_mode(rooftop2_mode)
            elif i == 1:
                import bathroom_mode
                bathroom_mode.set_girl_position(1300, 210)
                game_framework.change_mode(bathroom_mode)
            elif i == 2:
                if potion_used:
                    if game_world.is_hall3open():
                        import hall3_mode
                        hall3_mode.set_girl_position(100, 220)
                        game_framework.change_mode(hall3_mode)
                    else:
                        import hall2_mode
                        hall2_mode.set_girl_position(100, 220)
                        game_framework.change_mode(hall2_mode)
                else:
                    if not game_world.is_cantgo():
                        game_world.set_cantgo(True)
                        game_world.set_cantgo_start_time(get_time())

def draw():
    # 화면 그리기
    global font
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)

    game_world.render()
    game_framework.draw_room_name()
    # 하트가 수집된 상태라면 화면 특정 위치에 그리기
    # 슬롯 및 하트 그리기
    game_world.draw_slots()
    #papers.draw(1100, 220, 220, 132)

    if game_world.is_cantgo():
        elapsed_time = get_time() - game_world.get_cantgo_start_time()
        if elapsed_time < 3.0:  # 3초 동안 메시지 표시
            game_framework.draw_sent()
        else:
            game_world.set_cantgo(False)  # 3초 후 메시지 상태 초기화


    #for transition_box in transition_boxes:
    #    transition_box.draw()

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

class Papers:
    def __init__(self, x, y, width=220, height=132):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = load_image('papers.png')  # 이미지 로드

    def update(self):
        # 업데이트 로직이 필요하면 여기에 추가 (현재는 정적이므로 비워둠)
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)  # 이미지 그리기

    def get_bb(self):
        # 히트박스 반환 (필요 없으면 제거 가능)
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top
