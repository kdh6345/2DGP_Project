from pico2d import *
import game_framework
import game_world
from girl import Girl
from item import Key
from stair import Stair
from background import Background, Fence
from transition_box import TransitionBox
import secondroom_mode  # secondroom_mode 임포트 필요

# 소녀의 초기 위치를 저장하는 변수
girl_position = (400, 200)
monster_walk_sound = load_music('monster_walk.mp3')
is_monster_walk_sound_playing = False  # 사운드 상태 확인 변수

def set_girl_position(x, y):
    global girl_position
    girl_position = (x, y)

def enter():
    global girl, background, transition_box, stairs, black_screen, fence
    global monster_walk_sound, is_monster_walk_sound_playing

    # 기존 객체 제거
    game_world.clear()
    girl = Girl()  # 소녀 객체 생성
    game_world.set_girl(girl)  # 소녀 객체를 game_world에 설정
    girl.set_y_bounds(100, 200)  # rooftop에서의 y 좌표 제한
    girl.set_x_bounds(300, 1200)  # x 좌표 범위 확장

    # 몬스터 걷기 사운드 로드

    monster_walk_sound.set_volume(20)
    is_monster_walk_sound_playing = False  # 초기화

    # 소녀가 들고 있는 아이템 복원
    holding_item = game_world.load_girl_holding_item()
    if holding_item:
        if game_world.is_item_used(holding_item.id):
            print(f"[DEBUG] Used item detected in girl's hand: {holding_item.id}")
            girl.set_holding_item(None)  # 들고 있는 아이템 초기화
            game_world.save_girl_holding_item(None)
        else:
            girl.set_holding_item(holding_item)

    # 키 생성 조건
    if not game_world.is_item_used(0):  # Key ID가 0인지 확인
        key = Key(300, 150)
        game_world.add_object(key, 1)
    else:
        key = None

    # 새로운 객체 생성
    background = Background('start room2.png', 800, 400)  # 열린 Jail 배경
    game_framework.set_room_name("Rooftop")
    fence = Fence()
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
    game_world.add_object(girl, 1)
    game_world.add_object(fence, 2)
    for stair in stairs:
        game_world.add_object(stair, 2)

def exit():
    global background, monster_walk_sound, is_monster_walk_sound_playing
    del background
    if monster_walk_sound and is_monster_walk_sound_playing:
        monster_walk_sound.stop()  # 사운드 정지
        is_monster_walk_sound_playing = False

def update():
    global girl, monster_walk_sound, is_monster_walk_sound_playing

    # 게임 월드 업데이트
    game_world.update()
    import secondroom_mode
    # secondroom_mode의 secondroom_monster 상태 확인
    if secondroom_mode.secondroom_monster:
        if not is_monster_walk_sound_playing:  # 사운드가 재생 중이 아니면
            monster_walk_sound.repeat_play()  # 사운드 반복 재생
            is_monster_walk_sound_playing = True
    else:
        if is_monster_walk_sound_playing:  # 몬스터가 죽었거나 방을 나갔으면 멈춤
            monster_walk_sound.stop()
            is_monster_walk_sound_playing = False

    # 소녀의 위치 확인 및 화면 전환
    if check_for_transition(girl):
        # 방을 나갈 때 사운드 정지
        if monster_walk_sound and is_monster_walk_sound_playing:
            monster_walk_sound.stop()
            is_monster_walk_sound_playing = False

        girl_position = (1050, 100)
        import secondroom_mode
        secondroom_mode.set_girl_position(850, 600)  # Secondroom에서 소녀의 초기 위치 설정
        game_framework.change_mode(secondroom_mode)

def draw():
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)  # 배경 그리기
    game_world.render()
    game_framework.draw_room_name()
    # 하트가 수집된 상태라면 화면 특정 위치에 그리기
    # 슬롯 및 하트 그리기
    game_world.draw_slots()
    transition_box.draw()  # 전환 박스 그리기
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

    box_left, box_bottom, box_right, box_top = transition_box.get_bb()

    # 충돌 여부 확인
    if girl_left > box_right or girl_right < box_left:
        return False
    if girl_bottom > box_top or girl_top < box_bottom:
        return False
    return True

def finish():
    pass
