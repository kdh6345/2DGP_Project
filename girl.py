from pico2d import *
import game_framework
import game_world

class Girl:
    image = None

    def __init__(self, x=400, y=90, velocity=5):
        if Girl.image is None:
            Girl.image = load_image('character_walk.png')  # 여자 캐릭터 이미지 로드
        self.x, self.y = x, y
        self.velocity = velocity
        self.dir = 1  # 오른쪽이 1, 왼쪽이 -1

    def draw(self):
        if self.dir == 1:
            self.image.draw(self.x, self.y)
        else:
            self.image.composite_draw(0, 'h', self.x, self.y)  # 왼쪽을 향할 때 뒤집기

    def update(self):
        self.x += self.velocity * self.dir * game_framework.frame_time
        if self.x < 0 or self.x > 800:  # 화면 경계에서 방향 전환
            self.dir *= -1

    def get_bb(self):
        # 충돌 박스 설정 (사각형으로 간단히)
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, other, group):
        # 충돌 처리 로직
        pass
