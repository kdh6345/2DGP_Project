from pico2d import *
import game_framework
import rooftop_mode  # 다음 모드로 이동

class StartScreen:
    def __init__(self):
        self.image = load_image('start_image.png')  # 시작 화면 이미지 로드
        self.start_bgm = load_music('start_bgm.mp3')  # 시작 화면 BGM
        self.start_bgm.set_volume(64)
        self.start_bgm.repeat_play()

    def draw(self):
        self.image.draw(800, 400)  # 이미지 중앙에 그리기

    def update(self):
        pass  # 업데이트가 필요하지 않음

    def handle_events(self, events):
        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()  # 게임 종료
            elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
                self.start_bgm.stop()  # BGM 정지
                game_framework.change_mode(rooftop_mode)  # 다음 모드로 이동


def enter():
    global start_screen,black_screen
    start_screen = StartScreen()
    black_screen = load_image('black.png')  # 검정 화면 배경


def exit():
    global start_screen
    del start_screen


def update():
    start_screen.update()


def draw():
    clear_canvas()
    black_screen.draw(800, 400, 1600, 800)  # 전체 화면에 검정 배경
    start_screen.draw()
    update_canvas()


def handle_events():
    events = get_events()
    start_screen.handle_events(events)


def finish():
    pass
