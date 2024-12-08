from pico2d import *

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_bb(self):
        """장애물의 히트박스 반환"""
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top

    def draw(self):
        draw_rectangle(*self.get_bb())  # 디버깅용 히트박스 표시

    def update(self):
        pass  # 장애물은 정적이므로 특별한 업데이트 없음
