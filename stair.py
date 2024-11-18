#stair.py
from pico2d import *

class Stair:
    def __init__(self, x, y, width, height,min_y,max_y):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_y = min_y  # 계단 이동 가능한 최소 y값
        self.max_y = max_y  # 계단 이동 가능한 최대 y값
    def update(self):
        pass

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
