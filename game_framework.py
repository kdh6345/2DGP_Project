#game_framework.py
import time
from pico2d import load_font, load_music
import game_world

running = True
stack = []
frame_time = 0.0  # 프레임 간 경과 시간
background_music = None
room_name = None
font = None  # 폰트 변수 초기화
room_name_timer = 0

# 메시지 표시 관련 변수
sent_message = None
sent_message_timer = 0  # 메시지 표시 시간
sent_message_duration = 0  # 메시지 지속 시간

bgm = None  # 전역 BGM 변수

def init_bgm():
    global bgm
    if bgm is None:  # BGM이 초기화되지 않았을 때만 로드
        bgm = load_music('backgroundmusic.mp3')
        bgm.set_volume(32)
        bgm.repeat_play()  # 반복 재생

def stop_bgm():
    global bgm
    if bgm:
        bgm.stop()  # BGM 정지

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

def draw_sent():
    """특정 메시지를 일정 시간 동안 그리기"""
    global sent_message, sent_message_timer, font
    if sent_message and sent_message_timer > 0:
        if font is None:  # 폰트가 아직 로드되지 않았다면 로드
            font = load_font('ENCR10B.TTF', 20)  # 폰트 크기 조정
        font.draw(900, 100, sent_message, (255, 0, 0))  # 메시지를 화면에 그리기
        sent_message_timer -= frame_time  # 표시 시간을 줄임
        if sent_message_timer <= 0:
            sent_message = None  # 메시지 초기화


def set_sent_message(message, duration=3.0):
    """특정 메시지를 일정 시간 동안 설정"""
    global sent_message, sent_message_timer
    sent_message = message
    sent_message_timer = duration

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
    global running, stack, frame_time, background_music

    # 배경음악 로드 및 재생
    if background_music is None:
        background_music = load_music('sound.mp3')
        background_music.set_volume(50)  # 볼륨 조절 (0~100)
        background_music.repeat_play()

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
