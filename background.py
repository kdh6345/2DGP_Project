from pico2d import *

class Background:
    def __init__(self, image_path):
        self.image = load_image('start room1.png')
        self.width = int(1151)
        self.height = int(600)

    def draw(self):
        self.image.draw(400, 300)  # 화면 중앙에 배경 그리기

    def update(self):
        pass  # 필요한 경우 배경을 움직이거나 추가 효과를 처리
