#main.py
from pico2d import open_canvas, delay, close_canvas
import game_framework
from game_framework import init_bgm

import rooftop_mode as start_mode

open_canvas(1600, 800)
if __name__ == '__main__':
    init_bgm()  # 게임 시작 시 BGM 초기화
    game_framework.run(start_mode)
close_canvas()

