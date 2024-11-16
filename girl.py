#girl.py
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from state_machine import *
import game_world
import game_framework

class Idle:
    @staticmethod
    def enter(girl, e):
        if start_event(e):
            girl.action = 3
            girl.face_dir = 1
        elif right_down(e) or left_up(e):
            girl.action = 2
            girl.face_dir = -1
        elif left_down(e) or right_up(e):
            girl.action = 3
            girl.face_dir = 1

        girl.frame = 0
        girl.wait_time = get_time()

    @staticmethod
    def exit(girl, e):
       pass
    @staticmethod
    def do(girl):
        girl.frame = (girl.frame + 1) % 3

    @staticmethod
    def draw(girl):
        frame_width = 1354 // 3  # Idle 스프라이트 한 프레임의 너비
        frame_height = 500  # Idle 스프라이트 높이
        girl.idle_image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                  girl.x, girl.y, girl.width, girl.height)

class Walk:
    @staticmethod
    def enter(girl, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            girl.dir, girl.face_dir, girl.action = 1, 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            girl.dir, girl.face_dir, girl.action = -1, -1, 0

    @staticmethod
    def exit(girl, e):
        pass


    @staticmethod
    def do(girl):
        girl.frame = (girl.frame + 1) % 6
        girl.x += girl.dir*0.1

    @staticmethod
    def draw(girl):
        frame_width = 717  # 각 프레임의 너비
        frame_height = 800  # 이미지 높이
        
        girl.image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                             girl.x, girl.y, girl.width, girl.height)  # 화면에 100x150 크기로 출력


from pico2d import *

class Girl:
    def __init__(self):
        self.x, self.y = 200, 100
        self.face_dir = 1
        self.dir = 0
        self.action = 3  # 초기 상태
        self.frame = 0
        self.wait_time = 0
        self.image = load_image('character_walk.png')  # 걷는 상태 이미지
        self.idle_image = load_image('character_idle.png')  # Idle 상태 이미지
        self.width = 100
        self.height = 100
        self.state_machine = StateMachine(self)

        # 상태 머신 초기화
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, space_down: Idle},
            Walk: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Walk},
        })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
