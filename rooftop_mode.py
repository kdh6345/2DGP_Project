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
        # 히트박스를 시각화
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # 히트박스 범위 계산
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top


def enter():
    global girl, background, transition_box
    girl = Girl()  # 소녀 객체 생성
    background = Background('start room1.png',800,400)  # 옥상 배경 이미지

    # 전환 박스 생성
    transition_box = TransitionBox(1050, 100, 100, 100)

    game_world.add_object(background, 0)
    game_world.add_object(girl, 1)

def exit():
    global background
    del background
    game_world.clear()

def update():
    global girl

    # 소녀의 상태 업데이트
    game_world.update()

    # 소녀의 위치 확인 및 화면 전환
    if check_for_transition(girl):
        import secondroom_mode
        game_framework.change_mode(secondroom_mode)

def draw():
    clear_canvas()
    game_world.render()
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
            girl.handle_event(event)

def check_for_transition(girl):
    # 특정 좌표 (400, 0)의 범위를 설정
    target_x = 1050
    target_y = 100
    threshold = 50

    if abs(girl.x - target_x) <= threshold and abs(girl.y - target_y) <= threshold:
        return True
    return False

def finish():
    # 모드 종료 시 호출될 메서드
    pass
