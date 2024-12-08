from pico2d import open_canvas, close_canvas, load_music
import game_framework
import startscreen_mode as start_mode  # 시작 화면 모드로 변경

open_canvas(1600, 800)
if __name__ == '__main__':
    # 배경음악 로드 및 재생
    background_music = load_music('sound.mp3')
    background_music.set_volume(50)  # 볼륨 조절 (0~100)
    background_music.repeat_play()

    game_framework.run(start_mode)  # 시작 화면 모드 실행
close_canvas()
