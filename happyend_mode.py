from pico2d import *
import game_framework

# BGM 관련 변수
bgm = None

def enter():
    global background, font, white_screen,bgm
    background = load_image('happy_ending.png')  # 게임 오버 배경 이미지
    font = load_font('ENCR10B.TTF', 64)  # 폰트 로드
    white_screen = load_image('white.png')

    # BGM 로드 및 재생
    bgm = load_music('happy_ending.mp3')  # BGM 파일 경로 설정
    bgm.set_volume(64)  # 볼륨 조절 (0~128)
    bgm.repeat_play()

def exit():
    global background
    del background

def update():
   pass

def draw():
    clear_canvas()
    white_screen.draw(800, 400, 1600, 800)  # 전체 화면에 검정 배경
    background.draw(800, 400)  # 배경 그리기
    #font.draw(600, 400, "YOU WIN", (255, 0, 255))  # 게임 오버 메시지
    font.draw(450, 200, "Press ESC to finish", (0, 255, 0))  # 재시작 메시지
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def finish():
    pass
