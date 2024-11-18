from pico2d import *
import random
import game_framework
import game_world
from state_machine import StateMachine


class Idle:
    @staticmethod
    def enter(monster, event):
        monster.dir_x = 0
        monster.dir_y = 0
        monster.speed = 0
        monster.frame_time_accumulator = 0

    @staticmethod
    def exit(monster, event):
        pass

    @staticmethod
    def do(monster):
        # 프레임 처리
        frame_speed = 0.1
        monster.frame_time_accumulator += game_framework.frame_time

        if monster.frame_time_accumulator >= frame_speed:
            monster.frame = (monster.frame + 1) % 7  # 7개의 프레임
            monster.frame_time_accumulator = 0

    @staticmethod
    def draw(monster):
        frame_width = 3530 // 7
        frame_height = 500
        monster.image.clip_draw(monster.frame * frame_width, 0, frame_width, frame_height,
                                monster.x, monster.y, 300, 400)


class Patrol:
    @staticmethod
    def enter(monster, event):
        monster.dir_x = random.choice([-1, 1])  # 랜덤한 x 방향
        monster.dir_y = random.choice([-1, 1]) if monster.is_on_any_stair() else 0
        monster.speed = 0.1
        monster.frame_time_accumulator = 0

    @staticmethod
    def exit(monster, event):
        pass

    @staticmethod
    def do(monster):
        # x축 이동
        monster.x += monster.dir_x * monster.speed

        # y축 이동은 계단 위에서만
        if monster.is_on_any_stair():
            monster.y += monster.dir_y * monster.speed
        else:
            monster.dir_y = 0  # 계단 밖에서는 y축 이동 불가

        # 경계 처리 (x축만 제한)
        if monster.x < 0 or monster.x > 1600:
            monster.dir_x *= -1

        # 프레임 처리
        frame_speed = 0.1
        monster.frame_time_accumulator += game_framework.frame_time

        if monster.frame_time_accumulator >= frame_speed:
            monster.frame = (monster.frame + 1) % 7
            monster.frame_time_accumulator = 0

    @staticmethod
    def draw(monster):
        frame_width = 3530 // 7  # 각 프레임의 너비
        frame_height = 500  # 이미지 높이
        flip = 'h' if monster.dir_x < 0 else ''  # 왼쪽으로 이동 시 플립
        monster.image.clip_composite_draw(monster.frame * frame_width, 0, frame_width, frame_height,
                                          0, flip, monster.x, monster.y, 300, 400)

class Monster:
    def __init__(self, x, y,girl, stairs):
        self.x = x
        self.y = y
        self.dir_x = 0
        self.dir_y = 0
        self.speed = 1
        self.frame = 0
        self.frame_time_accumulator = 0
        self.image = load_image('monster_idle.png')
        self.state_machine = StateMachine(self)
        self.stairs = stairs  # 계단 리스트
        self.transition_boxes = []  # TransitionBox 리스트

        # 상태 머신 초기화
        self.state_machine.start(Patrol)
        self.state_machine.set_transitions({
            Patrol: {
                lambda monster: False: Idle  # 상태 전환 조건 (현재는 없음)
            },
            Idle: {
                lambda monster: True: Patrol  # 항상 Patrol로 전환
            }
        })

    def is_on_stair(self, stair):
        """몬스터가 특정 계단 위에 있는지 확인"""
        monster_left = self.x - 50
        monster_bottom = self.y - 50
        monster_right = self.x + 50
        monster_top = self.y + 50

        stair_left, stair_bottom, stair_right, stair_top = stair.get_bb()

        return (
            monster_right > stair_left and
            monster_left < stair_right and
            monster_top > stair_bottom and
            monster_bottom < stair_top
        )

    def is_on_any_stair(self):
        """몬스터가 계단 위에 있는지 확인"""
        return any(self.is_on_stair(stair) for stair in self.stairs)

    def set_transition_boxes(self, transition_boxes):
        """TransitionBox 리스트 설정"""
        self.transition_boxes = transition_boxes

    def check_transition_box(self):
        """TransitionBox와의 충돌 확인"""
        for transition_box in self.transition_boxes:
            box_left, box_bottom, box_right, box_top = transition_box.get_bb()

            if (self.x + 50 > box_left and
                self.x - 50 < box_right and
                self.y + 50 > box_bottom and
                self.y - 50 < box_top):
                return transition_box
        return None

    def update(self):
        # 상태 머신 업데이트
        self.state_machine.update()

        # TransitionBox와의 충돌 확인
        transition_box = self.check_transition_box()
        if transition_box:
            next_mode = transition_box.next_mode  # TransitionBox에 연결된 모드 가져오기
            import game_framework
            game_framework.change_mode(next_mode)

    def draw(self):
        self.state_machine.draw()
