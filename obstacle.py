from pico2d import *

class Obstacle:
    def __init__(self, x, y, width, height):
        """
        장애물 초기화
        x, y: 장애물 중심 좌표
        width, height: 장애물 크기
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        """
        장애물 히트박스 시각화
        """
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        """
        장애물 히트박스 반환
        """
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top
