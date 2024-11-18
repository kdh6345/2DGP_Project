from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_RETURN, SDLK_LEFT, SDLK_RIGHT, SDLK_c

from item import Key
from state_machine import *
import game_world
import game_framework

class UseItem:
    """아이템을 사용하는 상태"""
    @staticmethod
    def enter(girl, e):
        if girl.holding_item:
            girl.use_item_callback(girl.holding_item)  # 아이템 사용 콜백 호출
            girl.holding_item = None  # 아이템 초기화

    @staticmethod
    def exit(girl, e):
        pass

    @staticmethod
    def do(girl):
        pass

    @staticmethod
    def draw(girl):
        # 소녀를 Idle 상태처럼 기본적으로 그리기
        frame_width = 1354 // 3  # Idle 스프라이트 한 프레임의 너비
        frame_height = 500  # Idle 스프라이트 높이

        if girl.face_dir == 1:  # 오른쪽을 바라보는 경우
            girl.idle_image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                      girl.x, girl.y, girl.width, girl.height)
        else:  # 왼쪽을 바라보는 경우
            girl.idle_image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                                0, 'h', girl.x, girl.y, girl.width, girl.height)

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

class Climb:
    @staticmethod
    def enter(girl, e):
        if up_down(e):  # 위로 이동
            girl.dir_y = 1
        elif down_down(e):  # 아래로 이동
            girl.dir_y = -1

        girl.dir_x = 0  # Climb 상태에서는 X축 이동 불가
        girl.frame_time_accumulator = 0  # Climb 상태에서 프레임 시간 초기화

    @staticmethod
    def exit(girl, e):
        girl.dir_y = 0  # Y축 이동 멈춤

    @staticmethod
    def do(girl):
        # Climb 상태에서 프레임 변경 속도
        frame_speed = 0.1
        girl.frame_time_accumulator += game_framework.frame_time

        if girl.frame_time_accumulator >= frame_speed:
            girl.frame = (girl.frame + 1) % 6  # Climb 상태에서 3개의 프레임 반복
            girl.frame_time_accumulator = 0

        # 이동 처리
        girl.y += girl.dir_y * 1  # Y축 이동

    @staticmethod
    def draw(girl):
        frame_width = 717  # Climb 상태 프레임 너비
        frame_height = 800  # Climb 상태 프레임 높이
        girl.image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                             girl.x, girl.y, girl.width, girl.height)

class Hide:
    @staticmethod
    def enter(girl, e):
        # 숨는 상태 진입 시, 초기화 작업
        girl.frame = 0
        girl.dir_x = 0
        girl.dir_y = 0
        girl.action = 4  # 숨는 상태의 동작 번호 (예)

    @staticmethod
    def exit(girl, e):
        # 숨는 상태에서 나올 때의 작업
        pass

    @staticmethod
    def do(girl):
        # 숨는 상태에서는 프레임 고정 또는 반복
        frame_speed = 0.1
        girl.frame_time_accumulator += game_framework.frame_time

        if girl.frame_time_accumulator >= frame_speed:
            girl.frame = (girl.frame + 1) % 6  # 숨는 상태에서 3개의 프레임 반복
            girl.frame_time_accumulator = 0

    @staticmethod
    def draw(girl):
        # 숨는 상태의 이미지 그리기
        frame_width = 452  # `character_down.png`의 각 프레임 너비
        frame_height = 500  # `character_down.png`의 높이
        if girl.face_dir == 1:  # 오른쪽을 바라보는 경우
            girl.hide_image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                      girl.x, girl.y, girl.width, girl.height)
        else:  # 왼쪽을 바라보는 경우
            girl.hide_image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                                0, 'h', girl.x, girl.y, girl.width, girl.height)
class Girl:
    def __init__(self):
        self.x, self.y = 400, 200  # 초기 위치
        self.face_dir = 1
        self.dir_x, self.dir_y = 0, 0
        self.action = 3
        self.frame = 0
        self.frame_time_accumulator = 0
        self.image = load_image('character_walk.png')
        self.idle_image = load_image('character_idle.png')
        self.hide_image = load_image('character_down.png')  # 숨는 상태 이미지
        self.key_image = load_image('key.png')  # 키 이미지 추가
        self.width = 120
        self.height = 120
        self.holding_key = False  # 키를 쥐고 있는 상태 여부
        self.state_machine = StateMachine(self)
        self.y_min, self.y_max = None, None
        self.x_min, self.x_max = None, None  # x 좌표 제한 변수

        # 상태 머신 초기화
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {
                right_down: Walk, left_down: Walk,
                enter_down: Hide,  c_down: UseItem,
                up_down: Climb, down_down: Climb,  # 계단 위에서만 Climb 상태로 전환
            },
            Walk: {
                right_down: Walk, left_down: Walk,
                up_down: Climb, down_down: Climb,  # 계단 위에서만 Climb 상태로 전환
                right_up: Idle, left_up: Idle,
                enter_down: Hide, c_down: UseItem, # space 키로 숨기 시작
            },
            Climb: {
                up_up: Idle, down_up: Idle,  # 위/아래 키를 놓으면 Idle 상태로 전환
            },
            Hide: {
                up_down: Climb, down_down: Climb,  # 계단 위에서만 Climb 상태로 전환
                enter_up: Idle,  # space 키를 떼면 숨기 종료
                c_down: UseItem,

            },
            UseItem: {
                start_event: Idle,  # UseItem 상태에서 다시 Idle로 전환
            },
        })

    def set_y_bounds(self, y_min, y_max):
        """y 좌표의 최소값과 최대값 설정"""
        self.y_min = y_min
        self.y_max = y_max

    def set_x_bounds(self, x_min, x_max):
        """x 좌표의 최소값과 최대값 설정"""
        self.x_min = x_min
        self.x_max = x_max

    def update(self):
        self.state_machine.update()

        # y 값 제한 적용
        if self.y_min is not None and self.y < self.y_min:
            self.y = self.y_min
        if self.y_max is not None and self.y > self.y_max:
            self.y = self.y_max

        # x 값 제한 적용
        if self.x_min is not None and self.x < self.x_min:
            self.x = self.x_min
        if self.x_max is not None and self.x > self.x_max:
            self.x = self.x_max

    def handle_event(self, event, stairs):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        if self.holding_key:
            # 키를 소녀의 오른손 위치에 그리기
            key_offset_x = 30 if self.face_dir == 1 else -30
            key_offset_y = 50
            self.key_image.draw(self.x + key_offset_x, self.y  , 40, 40)

    def pick_up_item(self, item):
        """소녀가 아이템을 들게 설정"""
        self.holding_item = item
        print(f"Picked up {item.__class__.__name__}")

    def use_item_callback(self, item):
        """아이템을 사용할 때의 동작"""
        if isinstance(item, Key):  # 키를 사용했을 경우
            import rooftop_mode
            rooftop_mode.open_jail = True
            print("Jail opened!")

    def get_bb(self):
        """소녀의 히트박스 반환"""
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top

