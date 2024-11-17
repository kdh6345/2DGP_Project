from pico2d import *

class Stair:
    def __init__(self, x, y, width, height):
        """
        계단 초기화
        x, y: 계단 중심 좌표
        width, height: 계단 크기
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        """
        계단 히트박스 시각화
        """
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        """
        계단 히트박스 반환
        """
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top
