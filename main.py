from pico2d import open_canvas, close_canvas
import game_framework
import startscreen_mode as start_mode  # 시작 화면 모드로 변경

open_canvas(1600, 800)
if __name__ == '__main__':
    game_framework.run(start_mode)  # 시작 화면 모드 실행
close_canvas()
