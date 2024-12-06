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
        self.chase_image = load_image('monster_chase.png')
        self.sniff_image = load_image('monster_finding.png')  # 킁킁거리는 상태 이미지 추가

        self.girl = girl
        self.width = 200
        self.height = 200
        self.detection_rangex = 200
        self.detection_rangey = 100
        self.is_detecting = False

        self.sniff_timer = 0  # 킁킁 상태로 전환을 위한 타이머
        self.sniff_duration = 2.0  # 킁킁 상태 지속 시간
        self.sniff_cooldown = random.uniform(5, 10)  # 킁킁 상태로 진입 간격 (5~10초 랜덤)

        self.current_state = Patrol  # 현재 상태

    def is_girl_in_detection(self):
        """소녀가 감지 범위 내에 있는지 확인"""
        if isinstance(self.girl.state_machine.cur_state, Hide):
            print("Girl is in Hide state. Not detecting.")
            return False

        if self.girl.action == 4:
            print("Girl action is 4 (hiding). Not detecting.")
            return False

        girl_left, girl_bottom, girl_right, girl_top = self.girl.get_bb()
        monster_left, monster_bottom, monster_right, monster_top = self.get_detection_bb()

        detected = not (
            girl_right < monster_left or
            girl_left > monster_right or
            girl_top < monster_bottom or
            girl_bottom > monster_top
        )

        if detected:
            print("Girl detected!")
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
        self.is_detecting = self.is_girl_in_detection()

        # 킁킁 상태로 전환 조건
        if self.current_state == Patrol:
            self.sniff_timer += game_framework.frame_time
            if self.sniff_timer >= self.sniff_cooldown:
                self.sniff_timer = 0  # 타이머 초기화
                self.change_state(Sniff)

        # 상태 전환 처리
        if self.is_detecting and self.current_state != Chase:
            self.change_state(Chase)
        elif not self.is_detecting and self.current_state == Chase:
            self.change_state(Patrol)

        # 현재 상태의 행동 수행
        self.current_state.do(self)

    def draw(self):
        self.current_state.draw(self)
        draw_rectangle(*self.get_detection_bb())  # 감지 히트박스 시각화

    def change_state(self, new_state):
        """상태 변경 처리"""
        if self.current_state:
            self.current_state.exit(self)
        self.current_state = new_state
        self.current_state.enter(self)


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

        # 경계 처리
        if monster.x < 0 or monster.x > 1600:
            monster.dir_x *= -1

        # 프레임 업데이트 (0.1초 주기로 변경)
        frame_speed = 0.1
        monster.frame_time_accumulator += game_framework.frame_time
        if monster.frame_time_accumulator >= frame_speed:
            monster.frame = (monster.frame + 1) % 7  # 프레임 개수에 따라 반복
            monster.frame_time_accumulator = 0

    @staticmethod
    def draw(monster):
        frame_width = 3530 // 7  # 이미지의 총 너비 / 프레임 수
        frame_height = 500
        flip = 'h' if monster.dir_x > 0 else ''  # 이동 방향에 따라 플립
        monster.image.clip_composite_draw(monster.frame * frame_width, 0, frame_width, frame_height,
                                          0, flip, monster.x, monster.y, 250, 250)


class Sniff:
    """킁킁거리는 상태"""
    @staticmethod
    def enter(monster):
        print("Monster entered Sniff state.")
        monster.speed = 0.0  # 정지 상태
        monster.sniff_timer = 0  # 상태 지속 시간을 위한 타이머 초기화

    @staticmethod
    def exit(monster):
        pass

    @staticmethod
    def do(monster):
        # 상태 지속 시간 관리
        monster.sniff_timer += game_framework.frame_time
        if monster.sniff_timer >= monster.sniff_duration:
            monster.change_state(Patrol)  # Patrol 상태로 복귀

        # 프레임 업데이트
        frame_speed = 0.1
        monster.frame_time_accumulator += game_framework.frame_time
        if monster.frame_time_accumulator >= frame_speed:
            monster.frame = (monster.frame + 1) % 10  # 킁킁 상태 프레임
            monster.frame_time_accumulator = 0

    @staticmethod
    def draw(monster):
        frame_width = 4845 // 10  # 킁킁거리는 이미지의 총 너비 / 프레임 수
        frame_height = 500
        monster.sniff_image.clip_draw(monster.frame * frame_width, 0, frame_width, frame_height,
                                      monster.x, monster.y, 250, 250)


class Chase:
    @staticmethod
    def enter(monster):
        print("Monster entered Chase state.")
        monster.speed = 1.0  # 추격 속도

    @staticmethod
    def exit(monster):
        pass

    @staticmethod
    def do(monster):
        if monster.girl.x > monster.x:
            monster.dir_x = 1
        elif monster.girl.x < monster.x:
            monster.dir_x = -1

        monster.x += monster.dir_x * monster.speed

        # 프레임 업데이트 (0.1초 주기로 변경)
        frame_speed = 0.1
        monster.frame_time_accumulator += game_framework.frame_time
        if monster.frame_time_accumulator >= frame_speed:
            monster.frame = (monster.frame + 1) % 8  # 프레임 개수에 따라 반복
            monster.frame_time_accumulator = 0

    @staticmethod
    def draw(monster):
        frame_width = 3420 // 8  # 이미지의 총 너비 / 프레임 수
        frame_height = 500
        flip = 'h' if monster.dir_x > 0 else ''  # 이동 방향에 따라 플립
        monster.chase_image.clip_composite_draw(monster.frame * frame_width, 0, frame_width, frame_height,
                                                0, flip, monster.x, monster.y, 250, 250)
