# play_mode.py
from pico2d import *
from background import Background
from girl import Girl

background = None
girl = None

def init():
    global background, girl
    background = Background('start room1.png')  # 배경 이미지 경로
    girl = Girl(x=200, y=100, velocity=5)  # 소녀 캐릭터 생성

def update():
    pass

def draw():
    clear_canvas()
    background.draw(575.5, 300)  # 캔버스 중앙에 배경 그리기
    girl.draw()  # 소녀 캐릭터 그리기
    update_canvas()
