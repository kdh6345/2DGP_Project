from pico2d import *


class Idle:
    @staticmethod
    def enter(girl, event):
        girl.frame = 0  # Idle 상태의 초기 프레임 설정

    @staticmethod
    def exit(girl, event):
        pass  # Idle 상태 종료 시 특별한 동작 없음

    @staticmethod
    def do(girl):
        girl.frame = (girl.frame + 1) % 3  # Idle 상태에서 3개의 프레임 애니메이션 반복

    @staticmethod
    def draw(girl):
        frame_width = 1354 // 3  # Idle 스프라이트 한 프레임의 너비
        frame_height = 500  # Idle 스프라이트 높이
        girl.idle_image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                  girl.x, girl.y, girl.width, girl.height)


class Walk:
    @staticmethod
    def enter(girl, event):
        if event == 'RIGHT_DOWN':
            girl.dir = 1
        elif event == 'LEFT_DOWN':
            girl.dir = -1

    @staticmethod
    def exit(girl, event):
        pass  # Walk 상태 종료 시 특별한 동작 없음

    @staticmethod
    def do(girl):
        girl.frame = (girl.frame + 1) % 6  # Walk 상태 애니메이션 프레임
        girl.x += girl.dir * girl.speed  # 이동 처리

        # 화면 경계 체크
        if girl.x < 0:
            girl.x = 0
        elif girl.x > 1151:
            girl.x = 1151

    @staticmethod
    def draw(girl):
        frame_width = 717  # Walk 스프라이트 한 프레임의 너비
        frame_height = 800  # Walk 스프라이트 높이
        if girl.dir == 1:
            girl.walk_image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                      girl.x, girl.y, girl.width, girl.height)
        elif girl.dir == -1:
            girl.walk_image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                                0, 'h', girl.x, girl.y, girl.width, girl.height)


class Girl:
    def __init__(self):
        # Idle 이미지 로드
        self.idle_image = load_image('character_idle.png')
        # Walk 이미지 로드
        self.walk_image = load_image('character_walk.png')

        self.x, self.y = 200, 100
        self.dir = 0  # 이동 방향 (0: 정지, 1: 오른쪽, -1: 왼쪽)
        self.frame = 0
        self.width = 120
        self.height = 150
        self.speed = 5  # 이동 속도
        self.state = Idle
        self.state.enter(self, None)  # Idle 상태로 진입

    def change_state(self, new_state, event):
        self.state.exit(self, event)  # 현재 상태 종료
        self.state = new_state
        self.state.enter(self, event)  # 새로운 상태로 진입

    def update(self):
        self.state.do(self)  # 현재 상태의 동작 수행

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.change_state(Walk, 'RIGHT_DOWN')
            elif event.key == SDLK_LEFT:
                self.change_state(Walk, 'LEFT_DOWN')
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_RIGHT, SDLK_LEFT):
                self.change_state(Idle, 'KEY_UP')

    def draw(self):
        self.state.draw(self)
