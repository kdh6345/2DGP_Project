from pico2d import *


class Hall:
    def __init__(self):
        self.image = load_image('hall.png')
        self.scaled_width = int(2107*0.8)  # 0.8배 축소된 너비
        self.scaled_height = int(800 * 0.8)  # 원본 높이 유지

    def draw(self, camera_x,camera_y):
        # 카메라의 위치를 반영하여 Hall 이미지를 화면에 그리기
        self.image.draw(1400 // 2 - camera_x, 800 // 2-camera_y, self.scaled_width, self.scaled_height)


class Image1:
    def __init__(self):
        self.image = load_image('start room1.png')
        self.width = int(1151*1.5)
        self.height = int(600*1.5)

    def draw(self, camera_x,camera_y):
        # Hall 이미지 오른쪽에 추가 이미지가 오도록 위치 조정
        self.image.draw(1400 // 2 - camera_x - 1000, 800 // 2-camera_y+1000, self.width, self.height)

class Image2:
    def __init__(self):
        self.image = load_image('secondroom.png')
        self.width = int(2000)
        self.height = int(626)

    def draw(self, camera_x,camera_y):
        # Hall 이미지 오른쪽에 추가 이미지가 오도록 위치 조정
        self.image.draw(1400 // 2 - camera_x - 3000, 800 // 2-camera_y, self.width, self.height)

class Image3:
    def __init__(self):
        self.image = load_image('start room1.png')
        self.width = int(1151*1.2)
        self.height = int(600*1.2)

    def draw(self, camera_x,camera_y):
        # Hall 이미지 오른쪽에 추가 이미지가 오도록 위치 조정
        self.image.draw(1400 // 2 - camera_x - 1000, 800 // 2-camera_y+1000, self.width, self.height)


def main():
    open_canvas(1400, 800)  # 1400x600 화면 생성
    hall = Hall()  # Hall 객체 생성
    extra_image1 = Image1()  # 추가 이미지 객체 생성
    extra_image2 = Image2()  # 추가 이미지 객체 생성
    extra_image3 = Image3()  # 추가 이미지 객체 생성


    camera_x = 0  # 카메라 초기 위치
    camera_y=0

    while True:
        clear_canvas()

        # Hall과 추가 이미지를 카메라 위치에 맞춰 그리기
        hall.draw(camera_x,camera_y)
        extra_image1.draw(camera_x,camera_y)
        extra_image2.draw(camera_x, camera_y)

        update_canvas()

        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                close_canvas()
                return
            #elif event.type == SDL_KEYDOWN:
            elif event.key == SDLK_RIGHT:  # 오른쪽 화살표 키로 카메라를 오른쪽으로 이동
                    camera_x += 20
            elif event.key == SDLK_LEFT:  # 왼쪽 화살표 키로 카메라를 왼쪽으로 이동
                    camera_x -= 20
            elif event.key == SDLK_UP:  # 왼쪽 화살표 키로 카메라를 왼쪽으로 이동
                camera_y += 20
            elif event.key == SDLK_DOWN:  # 왼쪽 화살표 키로 카메라를 왼쪽으로 이동
                camera_y -= 20

        delay(0.01)  # 프레임 조절


if __name__ == '__main__':
    main()
