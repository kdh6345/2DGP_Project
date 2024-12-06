from pico2d import *

class Obstacle:
    def __init__(self, x, y, width, height):
        """장애물 초기화"""
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

    def update(self):
        """장애물은 업데이트가 필요 없으므로 빈 메서드로 유지"""
        pass

    def draw(self):
        """장애물 히트박스 시각화 (디버깅용)"""
        draw_rectangle(*self.get_bb())
