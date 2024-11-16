from pico2d import *

from pico2d import *

class Background:
    def __init__(self, image_path, x=800, y=300):
        self.image = load_image(image_path)  # 동적으로 이미지 경로 설정
        self.x = x  # 배경의 X 위치
        self.y = y  # 배경의 Y 위치

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)  # 설정된 위치에 배경 그리기



class Fence:
    def __init__(self):
        self.image=load_image('fence.png')
        self.x = 185  # 중심 x 좌표
        self.y = 210  # 중심 y 좌표
        self.width = 200  # 철창의 너비
        self.height = 100  # 철창의 높이

    def update(self):
        pass
    def draw(self):
        self.image.draw(185,210,210,170)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 120, self.y - 100, self.x + 150, self.y + 100


