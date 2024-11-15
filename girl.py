# girl.py
from pico2d import *

class Girl:
    image = None

    def __init__(self, x=200, y=100, velocity=5):
        if Girl.image is None:
            Girl.image = load_image('character_walk.png')  # 스프라이트 시트 이미지 로드
        self.x, self.y = x, y
        self.velocity = velocity
        self.dir = 1  # 오른쪽이 1, 왼쪽이 -1
        self.frame = 0
        self.width = 130  # 소녀의 그릴 너비
        self.height = 150  # 소녀의 그릴 높이

    def draw(self):
        frame_width = 717  # 스프라이트 한 프레임의 너비
        frame_height = 800  # 스프라이트 한 프레임의 높이
        if self.dir == 1:
            self.image.clip_draw(
                int(self.frame) * frame_width, 0, frame_width, frame_height,
                self.x, self.y, self.width, self.height
            )
        else:
            self.image.clip_composite_draw(
                int(self.frame) * frame_width, 0, frame_width, frame_height,
                0, 'h', self.x, self.y, self.width, self.height
            )

    def update(self):
       pass
