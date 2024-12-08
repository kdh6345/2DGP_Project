#girl.py
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_RETURN, SDLK_LEFT, SDLK_RIGHT, SDLK_c, \
    draw_rectangle, load_wav, load_music

import gameover_mode
from item import Key,Potion
from state_machine import *
import game_world
import game_framework

can_run = True  # 달리기 상태 해금 여부

class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def get_bb(self):
        return self.x1, self.y1, self.x2, self.y2

    def draw(self):
        #draw_rectangle(self.x1, self.y1, self.x2, self.y2)
        pass

    def update(self):
        """
        게임 월드에서 호출되는 빈 업데이트 메서드
        """
        pass


def setup_walls(wall_data, girl):
    for data in wall_data:
        x1, y1, x2, y2 = data
        wall = Wall(x1, y1, x2, y2)
        girl.add_wall(wall)



class UseItem:
    """아이템을 사용하는 상태"""
    @staticmethod
    def enter(girl, e):
        if girl.holding_item:  # 아이템을 들고 있는 경우
            girl.use_item_callback(girl.holding_item)  # 아이템 사용 콜백 호출
            girl.holding_item = None  # 아이템 초기화
        if isinstance(girl.holding_item, Potion):  # 포션 사용
            girl.holding_item.fire(girl.x, girl.y, girl.face_dir)
            game_world.clear_potion_state()  # 포션 상태 초기화
            girl.holding_item = None  # 포션 사용 후 초기화


        else:
            # 들고 있는 아이템이 없는 경우
            print("No item to use.")

        # 상태 전환 이벤트 추가
        girl.state_machine.add_event(('TIME_OUT', None))

    @staticmethod
    def exit(girl, e):
        pass

    @staticmethod
    def do(girl):
        pass

    @staticmethod
    def draw(girl):
        frame_width = 1354 // 3  # Idle 스프라이트 한 프레임의 너비
        frame_height = 500  # Idle 스프라이트 높이

        if girl.face_dir == 1:
            girl.idle_image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                      girl.x, girl.y, girl.width, girl.height)
        else:
            girl.idle_image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                                0, 'h', girl.x, girl.y, girl.width, girl.height)

class Idle:
    @staticmethod
    def enter(girl, e):
        girl.current_state_name = 'Idle'
        if start_event(e):
            girl.action = 3
        elif right_down(e) or left_up(e):
            girl.action = 2
        elif left_down(e) or right_up(e):
            girl.action = 3

        girl.frame = 0
        girl.wait_time = get_time()
        #girl.stop_walk_sound()

    @staticmethod
    def exit(girl, e):
        pass

    @staticmethod
    def do(girl):
        frame_speed = 0.1  # Idle 상태에서 프레임 변경 주기 (초)
        girl.frame_time_accumulator += game_framework.frame_time

        if girl.frame_time_accumulator >= frame_speed:
            girl.frame = (girl.frame + 1) % 3  # Idle 상태에서 3개의 프레임 반복
            girl.frame_time_accumulator = 0  # 누적 시간 초기화

    @staticmethod
    def draw(girl):
        frame_width = 1354 // 3  # Idle 스프라이트 한 프레임의 너비
        frame_height = 500  # Idle 스프라이트 높이

        if girl.face_dir == 1:  # 오른쪽을 바라보는 경우
            girl.idle_image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                      girl.x, girl.y, girl.width, girl.height)
        else:  # 왼쪽을 바라보는 경우
            girl.idle_image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                                0, 'h', girl.x, girl.y, girl.width, girl.height)


class Walk:
    @staticmethod
    def enter(girl, e):
        girl.current_state_name = 'Walk'
        if right_down(e):  # 오른쪽 이동
            girl.dir_x, girl.face_dir = 1, 1
        elif left_down(e):  # 왼쪽 이동
            girl.dir_x, girl.face_dir = -1, -1

        girl.frame_time_accumulator = 0  # Walk 상태에서 프레임 시간 초기화

        # 걷기 사운드 재생
        #girl.play_walk_sound()

    @staticmethod
    def exit(girl, e):
        girl.dir_x = 0  # 이동 멈춤
        girl.dir_y = 0  # 이동 멈춤
        #girl.stop_walk_sound()  # 걷기 사운드 멈춤

    @staticmethod
    def do(girl):
        # Walk 상태에서 프레임 변경 속도
        frame_speed = 0.1
        girl.frame_time_accumulator += game_framework.frame_time

        if girl.frame_time_accumulator >= frame_speed:
            girl.frame = (girl.frame + 1) % 6  # Walk 상태에서 6개의 프레임 반복
            girl.frame_time_accumulator = 0

        # 이동 처리
        girl.x += girl.dir_x * 1.0  # X축 이동

    @staticmethod
    def draw(girl):
        frame_width = 717  # 각 프레임의 너비
        frame_height = 800  # 이미지 높이

        if girl.face_dir == 1:
            girl.image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                 girl.x, girl.y, girl.width, girl.height)
        else:
            girl.image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                           0, 'h', girl.x, girl.y, girl.width, girl.height)

class Climb:
    @staticmethod
    def enter(girl, e):
        girl.current_state_name = 'Climb'
        if up_down(e):  # 위로 이동
            girl.dir_y = 1
        elif down_down(e):  # 아래로 이동
            girl.dir_y = -1

        girl.dir_x = 0  # Climb 상태에서는 X축 이동 불가
        girl.frame_time_accumulator = 0  # Climb 상태에서 프레임 시간 초기화
        #girl.play_walk_sound()

    @staticmethod
    def exit(girl, e):
        girl.dir_y = 0  # Y축 이동 멈춤

    @staticmethod
    def do(girl):
        # Climb 상태에서 프레임 변경 속도
        frame_speed = 0.1
        girl.frame_time_accumulator += game_framework.frame_time

        if girl.frame_time_accumulator >= frame_speed:
            girl.frame = (girl.frame + 1) % 6  # Climb 상태에서 3개의 프레임 반복
            girl.frame_time_accumulator = 0

        # 이동 처리
        girl.y += girl.dir_y * 1  # Y축 이동

    @staticmethod
    def draw(girl):
        frame_width = 717  # Climb 상태 프레임 너비
        frame_height = 800  # Climb 상태 프레임 높이
        girl.image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                             girl.x, girl.y, girl.width, girl.height)

class Hide:
    @staticmethod
    def enter(girl, e):
        girl.current_state_name = 'Hide'
        # 숨는 상태 진입 시, 초기화 작업
        girl.frame = 0
        girl.dir_x = 0
        girl.dir_y = 0
        girl.action = 4  # 숨는 상태의 동작 번호 (예)

    @staticmethod
    def exit(girl, e):
        # 숨는 상태에서 나올 때의 작업
        pass

    @staticmethod
    def do(girl):
        # 숨는 상태에서는 프레임 고정 또는 반복
        frame_speed = 0.1
        girl.frame_time_accumulator += game_framework.frame_time

        if girl.frame_time_accumulator >= frame_speed:
            girl.frame = (girl.frame + 1) % 6  # 숨는 상태에서 3개의 프레임 반복
            girl.frame_time_accumulator = 0

    @staticmethod
    def draw(girl):
        # 숨는 상태의 이미지 그리기
        frame_width = 452  # `character_down.png`의 각 프레임 너비
        frame_height = 500  # `character_down.png`의 높이
        if girl.face_dir == 1:  # 오른쪽을 바라보는 경우
            girl.hide_image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                      girl.x, girl.y, girl.width, girl.height)
        else:  # 왼쪽을 바라보는 경우
            girl.hide_image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                                0, 'h', girl.x, girl.y, girl.width, girl.height)

class Run:
    @staticmethod
    def enter(girl, e):
        girl.current_state_name='Run'
        print("Entered Run state")
        girl.frame_time_accumulator = 0
        girl.run_duration = 3.0  # 3초 동안 유지
        girl.speed = 3.0  # 빠른 속도
        girl.dir_x = girl.face_dir  # 바라보는 방향으로 이동
        #girl.play_walk_sound()

    @staticmethod
    def exit(girl, e):
        girl.dir_x = 0
        girl.speed = 0
        print("Exited Run state")

    @staticmethod
    def do(girl):
        global can_run
        girl.run_duration -= game_framework.frame_time
        if girl.run_duration <= 0:
            girl.state_machine.add_event(('TIME_OUT', None))

        girl.x += girl.dir_x * girl.speed
        #print(f"Running... New position: {girl.x}")

        frame_speed = 0.05
        girl.frame_time_accumulator += game_framework.frame_time
        if girl.frame_time_accumulator >= frame_speed:
            girl.frame = (girl.frame + 1) % 6
            girl.frame_time_accumulator = 0

    @staticmethod
    def draw(girl):
        frame_width = 717
        frame_height = 800
        if girl.face_dir == 1:
            girl.image.clip_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                 girl.x, girl.y, girl.width, girl.height)
        else:
            girl.image.clip_composite_draw(int(girl.frame) * frame_width, 0, frame_width, frame_height,
                                           0, 'h', girl.x, girl.y, girl.width, girl.height)




class Girl:
    def __init__(self):
        self.x, self.y = 400, 200  # 초기 위치
        self.face_dir = 1
        self.dir_x, self.dir_y = 0, 0
        self.action = 3
        self.frame = 0
        self.frame_time_accumulator = 0
        self.image = load_image('character_walk.png')
        self.idle_image = load_image('character_idle.png')
        self.hide_image = load_image('character_down.png')  # 숨는 상태 이미지
        self.key_image = load_image('key.png')  # 키 이미지 추가
        self.width = 120
        self.height = 120
        self.boundaries = []  # 여러 바운더리를 저장하는 리스트
        self.current_state_name = 'Idle'  # 현재 상태 이름을 추적하는 변수 추가
        self.walls = []  # 충돌 가능한 벽 리스트
        #self.walk_sound = load_music('girl_walk.mp3')  # 사운드 파일 로드
        #self.run_sound=load_music('girl_run.mp3')

        #self.walk_sound.set_volume(50)  # 볼륨 설정 (0~100)
        #self.run_sound.set_volume(70)  # 볼륨 설정 (0~100)
        #self.is_walking_sound_playing = False  # 걷기 사운드 상태 확인


        self.state_machine = StateMachine(self)
        self.y_min, self.y_max = None, None
        self.x_min, self.x_max = None, None  # x 좌표 제한 변수
        self.is_space_pressed = False  # 스페이스바 입력 상태

        global can_run

        self.state_machine = StateMachine(self)
        self.holding_item = None

        # 상태 머신 초기화
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {
                right_down: Walk,  # 오른쪽 키를 누르면 Walk 상태로 전환
                left_down: Walk,  # 왼쪽 키를 누르면 Walk 상태로 전환
                space_down: Run if can_run else Walk,  # 달리기 가능하면 Run 상태로, 아니면 Walk
                up_down: Climb,  # 위 키를 누르면 Climb 상태로 전환
                down_down: Climb,  # 아래 키를 누르면 Climb 상태로 전환
                enter_down: Hide,  # 숨기 상태로 전환
                c_down: UseItem,  # UseItem 상태로 전환
            },
            Walk: {
                right_down: Walk,  # 오른쪽 키를 누른 상태 유지
                left_down: Walk,  # 왼쪽 키를 누른 상태 유지
                space_down: Run if can_run else Walk,  # 달리기 가능하면 Run 상태로
                right_up: Idle,  # 오른쪽 키를 떼면 Idle 상태로
                left_up: Idle,  # 왼쪽 키를 떼면 Idle 상태로
                up_down: Climb,  # 위 키를 누르면 Climb 상태로 전환
                down_down: Climb,  # 아래 키를 누르면 Climb 상태로 전환
                enter_down: Hide,  # 숨기 상태로 전환
                c_down: UseItem,  # UseItem 상태로 전환
            },
            Run: {
                time_out: Idle,  # 3초가 지나면 Idle 상태로 전환
                right_up: Idle,  # 오른쪽 키를 떼면 Idle 상태로 전환
                left_up: Idle,  # 왼쪽 키를 떼면 Idle 상태로 전환
            },
            Climb: {
                up_up: Idle,  # 위 키를 떼면 Idle 상태로 전환
                down_up: Idle,  # 아래 키를 떼면 Idle 상태로 전환
            },
            Hide: {
                up_down: Climb,  # 위 키를 누르면 Climb 상태로 전환
                down_down: Climb,  # 아래 키를 누르면 Climb 상태로 전환
                enter_up: Idle,  # 숨기에서 Idle 상태로 전환
                c_down: UseItem,  # UseItem 상태로 전환
            },
            UseItem: {
                time_out: Idle,  # UseItem 상태에서 일정 시간이 지나면 Idle 상태로 전환
            },
        })

    def add_wall(self, wall):
        """
        소녀가 충돌할 벽을 추가합니다.
        :param wall: Wall 객체
        """
        self.walls.append(wall)

    def is_in_obstacle(self):
        """소녀가 장애물 안에 있는지 판단"""
        girl_bb = self.get_bb()
        for obstacle in game_world.get_obstacles():  # game_world에서 장애물 가져오기
            if hasattr(obstacle, 'get_bb'):
                obstacle_bb = obstacle.get_bb()
                if self.bb_overlap(girl_bb, obstacle_bb):
                    return True
        return False

    @staticmethod
    def bb_overlap(bb1, bb2):
        """히트박스 겹침 여부 확인"""
        left1, bottom1, right1, top1 = bb1
        left2, bottom2, right2, top2 = bb2

        if left1 > right2 or right1 < left2:
            return False
        if bottom1 > top2 or top1 < bottom2:
            return False
        return True

    def is_in_state(self, state_name):
        """소녀가 특정 상태에 있는지 확인"""
        return self.state_machine.cur_state.__class__.__name__ == state_name

    def set_y_bounds(self, y_min, y_max):
        """y 좌표의 최소값과 최대값 설정"""
        self.y_min = y_min
        self.y_max = y_max

    def set_x_bounds(self, x_min, x_max):
        """x 좌표의 최소값과 최대값 설정"""
        self.x_min = x_min
        self.x_max = x_max

    def add_boundary(self, x1, y1, x2, y2):
        """새로운 바운더리를 추가"""
        self.boundaries.append((x1, y1, x2, y2))
        print(f"Added boundary: ({x1}, {y1}, {x2}, {y2})")

    def boundary(self, x1, y1, x2, y2):
        """소녀가 움직일 수 있는 영역 설정"""
        self.x_min = x1
        self.y_min = y1
        self.x_max = x2
        self.y_max = y2
        print(f"Boundary set to: ({x1}, {y1}, {x2}, {y2})")


    def update(self):
        self.state_machine.update()
        # 벽과의 충돌 검사 및 위치 제한
        for wall in self.walls:
            wx1, wy1, wx2, wy2 = wall.get_bb()

            # x축 충돌 처리
            if self.x - self.width // 2 < wx2 and self.x + self.width // 2 > wx1:
                if self.y - self.height // 2 < wy2 and self.y + self.height // 2 > wy1:
                    # 왼쪽 벽 충돌
                    if self.x < wx1:
                        self.x = wx1 - self.width // 2
                    # 오른쪽 벽 충돌
                    elif self.x > wx2:
                        self.x = wx2 + self.width // 2

            # y축 충돌 처리
            if self.y - self.height // 2 < wy2 and self.y + self.height // 2 > wy1:
                if self.x - self.width // 2 < wx2 and self.x + self.width // 2 > wx1:
                    # 아래쪽 벽 충돌
                    if self.y < wy1:
                        self.y = wy1 - self.height // 2
                    # 위쪽 벽 충돌
                    elif self.y > wy2:
                        self.y = wy2 + self.height // 2


        if self.current_state_name == 'Hide':
            if self.is_in_obstacle():
                game_world.set_girl_safe(True)
                print("[DEBUG] Girl is hiding inside an obstacle. Safe!")
            else:
                game_world.set_girl_safe(False)
                print("[DEBUG] Girl is hiding, but not inside an obstacle. Not safe.")
        else:
            game_world.set_girl_safe(False)

        if self.holding_item:
            self.holding_item.x = self.x + (30 if self.face_dir == 1 else -30)
            self.holding_item.y = self.y
            pass


    def is_in_boundary(self):
        """소녀가 현재 어느 바운더리 안에 있는지 확인"""
        for boundary in self.boundaries:
            x1, y1, x2, y2 = boundary
            if x1 <= self.x <= x2 and y1 <= self.y <= y2:
                return True
        return False
    def handle_event(self, event, stairs):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            self.state_machine.add_event(('SPACE_DOWN', None))  # 스페이스바 이벤트 추가

        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        #draw_rectangle(*self.get_bb())  # 소녀의 히트박스를 화면에 표시
        self.state_machine.draw()
        # 바운더리 표시
        # 디버깅용으로 모든 벽을 표시합니다.
        #for wall in self.walls:
            #wall.draw()

        if self.holding_item:  # 아이템을 들고 있을 때
            offset_x = 30 if self.face_dir == 1 else -30
            self.holding_item.draw_at(self.x + offset_x, self.y)

    def pick_up_item(self, item):
        """소녀가 아이템을 들게 설정"""
        self.holding_item = item
        game_world.save_girl_holding_item(item)  # game_world에 상태 저장
        print(f"Picked up {item.__class__.__name__}")

    def use_item_callback(self, item):
        """아이템을 사용할 때의 동작"""
        if isinstance(item, Key):  # 키를 사용했을 경우
            print(f"Using Key with ID: {item.id}")
            self.holding_item = None
            game_world.mark_item_used(item.id)  # 키 사용 상태 기록
            game_world.remove_item(item)  # `game_world`에서도 제거
            game_world.save_girl_holding_item(None)  # 소녀의 들고 있는 아이템 초기화
            import rooftop_mode
            rooftop_mode.open_jail = True

        elif isinstance(item, Potion):  # 포션 사용
            print("Using Potion!")
            direction = 1 if self.face_dir == 1 else -1
            item.fire(self.x + (50 * direction), self.y, direction)  # 소녀의 앞에서 발사
            game_world.mark_item_used(item.id)  # 포션 사용 상태 기록
            game_world.mark_item_picked(item.id)  # 포션 픽업 상태 기록
            self.holding_item = None  # 포션 사용 후 손에서 제거
        else:
            print("Cannot use this item.")

    def set_holding_item(self, item):
        """들고 있는 아이템 설정"""
        self.holding_item = item

    def get_holding_item(self):
        """들고 있는 아이템 반환"""
        return self.holding_item

    def get_bb(self):
        """소녀의 히트박스 반환"""
        # 실제 스프라이트 크기에 맞게 히트박스 조정
        left = self.x - 30  # 히트박스 크기 조정
        bottom = self.y - 50
        right = self.x + 30
        top = self.y + 50


        return left, bottom, right, top

    def die(self):
        """소녀 사망 처리"""
        print("The girl has died!")
        import died_mode  # 새로운 사망 모드
        game_framework.change_mode(died_mode)

