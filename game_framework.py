#game_framework.py
import time
from pico2d import load_font
import game_world

running = True
stack = []
frame_time = 0.0  # 프레임 간 경과 시간

room_name = None
font = None  # 폰트 변수 초기화
room_name_timer = 0

def set_room_name(name, duration=2.0):
    """방 이름과 표시 시간을 설정"""
    global room_name, room_name_timer
    room_name = name
    room_name_timer = duration

def draw_room_name():
    """방 이름을 화면에 항상 그리기"""
    global room_name, font
    if room_name:
        if font is None:  # 폰트가 아직 로드되지 않았다면 로드
            font = load_font('ENCR10B.TTF', 40)  # 업로드된 폰트 파일 사용
        font.draw(750, 750, room_name, (255, 255, 255))  # 화면 중앙에 흰색 텍스트로 그리기

def change_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.enter()
    game_world.set_current_mode(mode.__name__)  # 모드 변경시 현재 모드 업데이트

def push_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(mode)
    mode.enter()

def pop_mode():
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    if len(stack) > 0:
        stack[-1].resume()

def quit():
    global running
    running = False

def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]
    start_mode.enter()

    current_time = time.time()  # 현재 시간을 기록

    while running:
        # frame_time 계산
        new_time = time.time()
        frame_time = new_time - current_time
        current_time = new_time

        # 현재 모드 실행
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while len(stack) > 0:
        stack[-1].finish()
        stack.pop()
