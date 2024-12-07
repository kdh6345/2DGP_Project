from pico2d import *
import game_world

class Heart:
    def __init__(self, x, y):
        self.image = load_image('monster_heart1.png')  # 하트 이미지 로드
        self.x = x
        self.y = y
        self.width = 50  # 하트 크기
        self.height = 50
        self.picked_up = False

    def update(self):
        girl = game_world.get_girl()
        if girl and self.is_colliding(girl):
            self.picked_up = True
            game_world.set_heart_collected(True)  # 하트 수집 상태 기록
            game_world.remove_object(self)  # 게임 월드에서 하트 제거

    def draw(self):
        if not self.picked_up:
            self.image.draw(self.x, self.y, self.width, self.height)

    def is_colliding(self, girl):
        """소녀와 하트의 충돌 여부 확인"""
        left_girl, bottom_girl, right_girl, top_girl = girl.get_bb()
        left, bottom, right, top = self.get_bb()
        return not (right_girl < left or left_girl > right or top_girl < bottom or bottom_girl > top)

    def get_bb(self):
        """하트의 히트박스 반환"""
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top
