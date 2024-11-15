# background.py
from pico2d import *

class Background:
    def __init__(self, image_path):
        self.image = load_image(image_path)
        self.width = self.image.w
        self.height = self.image.h

    def draw(self, x, y):
        # 이미지 크기를 캔버스에 맞춰서 그리기
        self.image.draw(x, y, 1151, 600)
