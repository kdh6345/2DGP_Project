from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from state_machine import *
import game_world
import game_framework

class Idle:
    @staticmethod
    def enter(girl, e):
        if start_event(e):
            girl.action = 3
        elif right_down(e) or left_up(e):
            girl.action = 2
        elif left_down(e) or right_up(e):
            girl.action = 3

        girl.frame = 0
        girl.wait_time = get_time()

    @staticmethod
    def exit(girl, e):
        pass

    @staticmethod
    def do(girl):
        frame_speed = 0.1  # Idle 상태에서 프레임 변경 주기 (초)
        girl.frame_time_accumulator += game_framework.frame_time

        if girl.frame_time_accumulator >= frame_speed:
            girl.frame = (girl.frame + 1) % 3  # Idle 상태에서 3개의 프레임 반복
            girl.frame_time_accumulator = 0  # 누적 시간 초기화

    @staticmethod
    def draw(girl):
        frame_width = 1354 // 3  # Idle 스프라이트 한 프레임의 너비
        frame_height = 500  # Idle 스프라이트 높이

        if girl.face_dir == 1:  # 오른쪽을 바라보는 경우
            girl.idle_image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                      girl.x, girl.y, girl.width, girl.height)
        else:  # 왼쪽을 바라보는 경우
            girl.idle_image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                                0, 'h', girl.x, girl.y, girl.width, girl.height)


class Walk:
    @staticmethod
    def enter(girl, e):
        if right_down(e):  # 오른쪽 이동
            girl.dir_x, girl.face_dir = 1, 1
        elif left_down(e):  # 왼쪽 이동
            girl.dir_x, girl.face_dir = -1, -1
        elif up_down(e):  # 위쪽 이동
            girl.dir_y = 1
        elif down_down(e):  # 아래쪽 이동
            girl.dir_y = -1

        girl.frame_time_accumulator = 0  # Walk 상태에서 프레임 시간 초기화

    @staticmethod
    def exit(girl, e):
        girl.dir_x = 0  # 이동 멈춤
        girl.dir_y = 0  # 이동 멈춤

    @staticmethod
    def do(girl):
        # Walk 상태에서 프레임 변경 속도
        frame_speed = 0.1
        girl.frame_time_accumulator += game_framework.frame_time

        if girl.frame_time_accumulator >= frame_speed:
            girl.frame = (girl.frame + 1) % 6  # Walk 상태에서 6개의 프레임 반복
            girl.frame_time_accumulator = 0

        # 이동 처리
        girl.x += girl.dir_x * 1  # X축 이동
        girl.y += girl.dir_y * 1  # Y축 이동

    @staticmethod
    def draw(girl):
        frame_width = 717  # 각 프레임의 너비
        frame_height = 800  # 이미지 높이

        if girl.face_dir == 1:
            girl.image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                 girl.x, girl.y, girl.width, girl.height)
        else:
            girl.image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                           0, 'h', girl.x, girl.y, girl.width, girl.height)

class Girl:
    def __init__(self):
        self.x, self.y = 400, 210  # 소녀의 초기 위치
        self.face_dir = 1  # 얼굴 방향
        self.dir_x, self.dir_y = 0, 0  # X축과 Y축 이동 방향
        self.action = 3  # 초기 상태
        self.frame = 0
        self.frame_time_accumulator = 0
        self.image = load_image('character_walk.png')  # 걷는 상태 이미지
        self.idle_image = load_image('character_idle.png')  # Idle 상태 이미지
        self.width = 120
        self.height = 120
        self.state_machine = StateMachine(self)

        # 상태 머신 초기화
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {
                right_down: Walk, left_down: Walk, up_down: Walk, down_down: Walk,
                right_up: Idle, left_up: Idle, up_up: Idle, down_up: Idle,
                space_down: Idle,
            },
            Walk: {
                right_down: Walk, left_down: Walk, up_down: Walk, down_down: Walk,
                right_up: Idle, left_up: Idle, up_up: Idle, down_up: Idle,
                space_down: Walk,
            },
        })

    def is_on_stair(self, stair):
        """
        소녀가 계단 영역 안에 있는지 확인
        """
        girl_left = self.x - self.width // 2
        girl_bottom = self.y - self.height // 2
        girl_right = self.x + self.width // 2
        girl_top = self.y + self.height // 2

        stair_left, stair_bottom, stair_right, stair_top = stair.get_bb()

        # 소녀가 계단 영역에 있는지 확인
        if girl_right > stair_left and girl_left < stair_right and girl_top > stair_bottom and girl_bottom < stair_top:
            return True
        return False

    def update(self):
        # 상태 머신 업데이트
        self.state_machine.update()

    def handle_event(self, event):
        # 상태 머신에 이벤트 전달
        self.state_machine.add_event(('INPUT', event))
        # 위/아래 키 제한
        if event.type == SDL_KEYDOWN:
            if event.key in (SDLK_UP, SDLK_DOWN):
                # 계단 위에 있는지 확인
                on_any_stair = any(self.is_on_stair(stair) for stair in stairs)
                if not on_any_stair:
                    return  # 계단에 없으면 위/아래 키 이벤트 무시

    def draw(self):
        # 현재 상태의 그리기 로직 호출
        self.state_machine.draw()
