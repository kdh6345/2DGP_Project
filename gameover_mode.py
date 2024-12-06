from pico2d import *
import game_framework

class GameOver:
    def __init__(self):
        self.image = None
        self.time_elapsed = 0
        self.display_duration = 3.0
        self.__name__ = "GameOver"  # 모드 이름 추가

    def enter(self):
        self.image = load_image('youlose.png')
        self.time_elapsed = 0

    def exit(self):
        del self.image

    def update(self):
        self.time_elapsed += game_framework.frame_time
        if self.time_elapsed > self.display_duration:
            # 타이틀 화면으로 전환 또는 초기화
            pass

    def draw(self):
        clear_canvas()
        if self.image:
            self.image.draw(800, 400)
        update_canvas()
    def finish(self):
        pass

    def handle_events(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
                game_framework.quit()

# `game_framework`에서 사용할 객체 생성
gameover_state = GameOver()
