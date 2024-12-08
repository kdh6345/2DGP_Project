from pico2d import *
import game_framework
import random

# 흔들림 효과 관련 변수
shake_offset_x = 0
shake_offset_y = 0
shake_duration = 0.0
shake_intensity = 0

# BGM 관련 변수
bgm = None

def start_shake(duration=1.0, intensity=5):
    """흔들림 효과를 시작"""
    global shake_duration, shake_intensity
    shake_duration = duration
    shake_intensity = intensity

def update_shake():
    """흔들림 효과를 업데이트"""
    global shake_duration, shake_offset_x, shake_offset_y

    if shake_duration > 0:
        shake_duration -= game_framework.frame_time
        shake_offset_x = random.randint(-shake_intensity, shake_intensity)
        shake_offset_y = random.randint(-shake_intensity, shake_intensity)
    else:
        shake_offset_x = 0
        shake_offset_y = 0

def enter():
    global background, font, black_screen, bgm

    # 이미지 로드
    background = load_image('bad_ending.png')  # 게임 오버 배경 이미지
    black_screen = load_image('black.png')    # 검정 배경 이미지

    # 폰트 로드
    font = load_font('ENCR10B.TTF', 64)

    # BGM 로드 및 재생
    bgm = load_music('game_over_bgm.mp3')  # BGM 파일 경로 설정
    bgm.set_volume(64)                     # 볼륨 조절 (0~128)
    bgm.play()                      # 반복 재생

    # 흔들림 효과 시작
    start_shake(duration=3.0, intensity=10)  # 3초 동안 강도 10으로 흔들림

def exit():
    global background, bgm
    del background

    # BGM 정지
    if bgm:
        bgm.stop()
        del bgm

def update():
    pass

def draw():
    update_shake()
    clear_canvas()

    # 검정 배경 그리기
    black_screen.draw(800, 400, 1600, 800)

    # 흔들림 효과 적용된 배경 그리기
    background.draw(800 + shake_offset_x, 400 + shake_offset_y)  # 흔들림 반영

    # 텍스트 그리기
    font.draw(600, 400, "GAME OVER", (255, 0, 0))
    font.draw(500, 300, "Press R to Restart", (255, 255, 255))

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_r:
                import startscreen_mode  # 시작 화면으로 이동
                game_framework.change_mode(startscreen_mode)

def finish():
    pass  # 특별히 정리할 내용이 없으므로 pass
