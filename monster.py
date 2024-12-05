from pico2d import *
import random

import game_framework
from girl import *


class Monster:
    def __init__(self, x, y, girl):
        self.x = x
        self.y = y
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])
        self.speed = 0.2
        self.frame = 0
        self.frame_time_accumulator = 0
        self.image = load_image('monster_idle.png')
        self.chase_image=load_image('monster_chase.png')
        self.visible = False
        self.current_room = 'hall1_mode'  # 몬스터의 현재 방 위치

        self.girl = girl
        self.width = 200
        self.height = 200
        self.detection_rangex = 200
        self.detection_rangey = 100
        self.is_detecting = False
        self.current_state = Patrol  # 현재 상태

    def is_girl_in_detection(self):
        # 현재 게임 월드에서 실제 소녀 객체 가져오기
        current_girl = game_world.get_girl()  # game_world에 get_girl() 함수 추가 필요

        if isinstance(current_girl.state_machine.cur_state, Hide):
            return False

        if current_girl.action == 4:
            return False

        girl_left, girl_bottom, girl_right, girl_top = current_girl.get_bb()
        monster_left, monster_bottom, monster_right, monster_top = self.get_detection_bb()

        detected = not (
                girl_right < monster_left or
                girl_left > monster_right or
                girl_top < monster_bottom or
                girl_bottom > monster_top
        )

        return detected

    def get_detection_bb(self):
        """몬스터의 감지 히트박스 반환"""
        if self.dir_x > 0:  # 오른쪽을 바라보는 경우
            left = self.x - self.detection_rangex * 0.5
            right = self.x + self.detection_rangex * 2
        else:  # 왼쪽을 바라보는 경우
            left = self.x - self.detection_rangex * 2
            right = self.x + self.detection_rangex * 0.5

        bottom = self.y - self.detection_rangey
        top = self.y + self.detection_rangey

        return left, bottom, right, top

    def update(self):
        self.check_same_room()
        # 같은 방에 있을 때만 감지 및 추적 로직 실행
        if self.visible:
            # 히트박스 내에 있을 때만 감지 상태로 변경
            if self.is_girl_in_detection():
                self.is_detecting = True
                if self.current_state != Chase:
                    self.change_state(Chase)
            else:
                self.is_detecting = False
                if self.current_state != Patrol:
                    self.change_state(Patrol)

            self.current_state.do(self)

    def check_same_room(self):
        previous_visible = self.visible
        self.visible = (game_world.current_mode == self.current_room)
        if previous_visible != self.visible:
            self.is_detecting = False
            self.change_state(Patrol)

    def check_visibility(self):
        current_mode = game_world.current_mode
        # hall1_mode에서 시작
        if current_mode == 'hall1_mode':
            self.visible = True
        else:
            self.visible = False

    def draw(self):
        if self.visible:
            self.current_state.draw(self)
            draw_rectangle(*self.get_detection_bb())  # 감지 히트박스 시각화



    def change_state(self, new_state):
        """상태 변경 처리"""
        if self.current_state:
            self.current_state.exit(self)
        self.current_state = new_state
        self.current_state.enter(self)

def check_for_transition(self, transition_box):  # self 매개변수 추가
    monster_left = self.x - self.width // 2
    monster_bottom = self.y - self.height // 2
    monster_right = self.x + self.width // 2
    monster_top = self.y + self.height // 2

    box_left, box_bottom, box_right, box_top = transition_box.get_bb()

    if monster_left > box_right or monster_right < box_left:
        return False
    if monster_bottom > box_top or monster_top < box_bottom:
        return False
    return True

def handle_monster_transition(self, transition_box):  # Monster 클래스 메소드로 이동
    # 각 방의 전환 지점에 따른 몬스터 위치 설정
    if self.current_room == 'hall1_mode':
        if transition_box.x < 100:  # 왼쪽 출구
            self.current_room = 'secondroom_mode'
            self.x = 1500
        elif transition_box.x > 1500:  # 오른쪽 출구
            self.current_room = 'livingroom1_mode'
            self.x = 200

class Patrol:
    @staticmethod
    def enter(monster):
        print("Monster entered Patrol state.")
        monster.speed = 0.2  # 순찰 속도

    @staticmethod
    def exit(monster):
        pass

    @staticmethod
    def do(monster):
        monster.x += monster.dir_x * monster.speed

        # 경계 처리 및 방 전환 체크
        current_mode = game_world.current_mode  # 현재 모드 직접 접근
        if hasattr(current_mode, 'transition_boxes'):
            for transition_box in current_mode.transition_boxes:
                if monster.check_for_transition(transition_box):
                    monster.handle_monster_transition(transition_box)
                    return

        # 기존 방향 전환 로직
        if monster.x < -100 or monster.x > 1700:
            monster.dir_x *= -1

        # 프레임 업데이트
        frame_speed = 0.1
        monster.frame_time_accumulator += game_framework.frame_time
        if monster.frame_time_accumulator >= frame_speed:
            monster.frame = (monster.frame + 1) % 7
            monster.frame_time_accumulator = 0



    @staticmethod
    def draw(monster):
        frame_width = 3530 // 7  # 이미지의 총 너비 / 프레임 수
        frame_height = 500
        flip = 'h' if monster.dir_x > 0 else ''  # 이동 방향에 따라 플립
        monster.image.clip_composite_draw(monster.frame * frame_width, 0, frame_width, frame_height,
                                          0, flip, monster.x, monster.y, 250, 250)


class Chase:
    @staticmethod
    def enter(monster):
        print("Monster entered Chase state.")
        monster.speed = 0.5

    @staticmethod
    def exit(monster):
        pass

    @staticmethod
    def do(monster):
        direction_change_buffer = 200

        if monster.girl.x > monster.x + direction_change_buffer:
            monster.dir_x = 1
        elif monster.girl.x < monster.x - direction_change_buffer:
            monster.dir_x = -1

        monster.x += monster.dir_x * monster.speed

        frame_speed = 0.1
        monster.frame_time_accumulator += game_framework.frame_time
        if monster.frame_time_accumulator >= frame_speed:
            monster.frame = (monster.frame + 1) % 8
            monster.frame_time_accumulator = 0

    @staticmethod
    def draw(monster):
        frame_width = 3420 // 8
        frame_height = 500
        # Changed flip logic to face the girl's direction
        flip = '' if monster.dir_x < 0 else 'h'
        monster.chase_image.clip_composite_draw(monster.frame * frame_width, 0, frame_width, frame_height,
                                          0, flip, monster.x, monster.y, 250, 250)
