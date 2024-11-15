# main.py
from pico2d import *
import game_framework
import play_mode  # 플레이 모드를 import

def main():
    open_canvas(1151, 600)  # 1151x600 해상도로 캔버스 열기
    game_framework.run(play_mode)  # play_mode로 게임 시작
    close_canvas()

if __name__ == '__main__':
    main()
