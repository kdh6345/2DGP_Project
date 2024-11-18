#transition_box.py
from pico2d import draw_rectangle

class TransitionBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        # 히트박스를 시각화
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # 히트박스 범위 계산
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top
