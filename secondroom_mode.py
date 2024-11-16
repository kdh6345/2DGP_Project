from pico2d import *
import game_framework
import game_world
from girl import Girl
from background import Background
class TransitionBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # 히트박스 범위 계산
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top

def enter():
    global background, girl,transition_box

    # 새로운 배경 설정
    background = Background('secondroom.png', x=800, y=400)  # 두 번째 방 배경 이미지 및 위치

    # 소녀 객체 가져오기
    girl = [obj for obj in game_world.objects_at(1) if isinstance(obj, Girl)][0]

    # 소녀 위치 초기화 (이미 Idle 상태라면 추가 상태 초기화는 필요 없음)
    girl.x, girl.y = 1000, 800

    transition_box = TransitionBox(1000, 800, 100, 100)

    # game_world에 추가
    game_world.add_object(background, 0)
    game_world.add_object(girl, 1)

def exit():
    global background
    del background

def update():
    # 소녀 및 게임 월드 업데이트
    game_world.update()
    # 소녀의 위치 확인 및 화면 전환
    if check_for_transition(girl):
        import rooftop_mode
        game_framework.change_mode(rooftop_mode)

def draw():
    # 화면 그리기
    clear_canvas()
    game_world.render()
    transition_box.draw()
    update_canvas()

def handle_events():
    # 이벤트 처리
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            girl = [obj for obj in game_world.objects_at(1) if isinstance(obj, Girl)][0]
            girl.handle_event(event)  # 소녀 이벤트 처리

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

