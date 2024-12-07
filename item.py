#item.py
from pico2d import load_image, draw_rectangle

import game_framework
import game_world
from monster import Monster


class Item:
    """아이템의 공통 클래스"""
    def __init__(self, x, y, width, height, image_path, item_id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = load_image(image_path)
        self.picked_up = False
        self.id = item_id  # 아이템 고유 ID 추가

    def update(self):
        """소녀와 충돌 체크 후 아이템을 들게 설정"""
        girl = game_world.get_girl()  # game_world에서 소녀 객체 가져오기
        if not self.picked_up and self.is_colliding(girl):
            self.picked_up = True
            girl.pick_up_item(self)
            game_world.mark_item_picked(self.id)  # 아이템을 습득된 상태로 기록

    def draw(self):
        """아이템을 화면에 그리기 (습득되지 않은 경우)"""
        if not self.picked_up:
            self.image.draw(self.x, self.y, self.width, self.height)
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        """아이템의 히트박스 반환"""
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top

    def is_colliding(self, obj):
        """소녀와 아이템의 충돌 여부 확인"""
        item_left, item_bottom, item_right, item_top = self.get_bb()
        obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()

        if item_right < obj_left or item_left > obj_right:
            return False
        if item_top < obj_bottom or item_bottom > obj_top:
            return False
        return True


class Key:
    """키 아이템 클래스"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.image = load_image('key.png')
        self.picked_up = False
        self.id = 0  # 고유 ID 추가

    def update(self):
        """키 아이템 업데이트 (소녀와의 충돌 확인)"""
        girl = game_world.get_girl()
        if not self.picked_up and self.is_colliding(girl):
            self.picked_up = True
            girl.pick_up_item(self)

    def draw(self):
        """키를 화면에 그리기"""
        if not self.picked_up:
            self.image.draw(self.x, self.y, self.width, self.height)

    def draw_at(self, x, y):
        """소녀가 들고 있을 때의 키 그리기"""
        self.image.draw(x, y, self.width, self.height)

    def get_bb(self):
        """히트박스 반환"""
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top

    def is_colliding(self, obj):
        """충돌 여부 확인"""
        item_left, item_bottom, item_right, item_top = self.get_bb()
        obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()

        if item_right < obj_left or item_left > obj_right:
            return False
        if item_top < obj_bottom or item_bottom > obj_top:
            return False
        return True

class Key2:
    """키 아이템 클래스"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.image = load_image('key2.png')
        self.picked_up = False

    def update(self):
        """키 아이템 업데이트 (소녀와의 충돌 확인)"""
        girl = game_world.get_girl()
        if not self.picked_up and self.is_colliding(girl):
            self.picked_up = True
            girl.pick_up_item(self)

    def draw(self):
        """키를 화면에 그리기"""
        if not self.picked_up:
            self.image.draw(self.x, self.y, self.width, self.height)

    def draw_at(self, x, y):
        """소녀가 들고 있을 때의 키 그리기"""
        self.image.draw(x, y, self.width, self.height)

    def get_bb(self):
        """히트박스 반환"""
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top

    def is_colliding(self, obj):
        """충돌 여부 확인"""
        item_left, item_bottom, item_right, item_top = self.get_bb()
        obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()

        if item_right < obj_left or item_left > obj_right:
            return False
        if item_top < obj_bottom or item_bottom > obj_top:
            return False
        return True

class Potion:
    """포션 아이템 클래스"""


    def __init__(self, x, y, potion_id):
        self.x = x
        self.y = y
        self.width = 30  # 포션 너비
        self.height = 50  # 포션 높이
        self.image = load_image('potion.png')
        self.picked_up = False
        self.throwing = False  # 포션이 던져지고 있는 상태
        self.speed = 1000  # 포션 이동 속도 (픽셀/초)
        self.id = potion_id  # 고유 ID 설정
        self.direction = 0  # 발사 방향 (1: 오른쪽, -1: 왼쪽)

    def update(self):
        if self.throwing:  # 던져진 상태에서만 이동
            self.x += self.direction * self.speed * game_framework.frame_time

            # 화면 밖으로 나가면 포션을 사용된 상태로 기록하고 제거
            if self.x < 0 or self.x > 1600:  # 화면 크기 가정: 1600x800
                self.throwing = False
                game_world.mark_item_used(self.id)  # 포션 ID를 사용된 것으로 기록
                game_world.remove_object(self)
                return

            # 몬스터와 충돌 체크
            for obj in game_world.objects_at(1):  # 2번 레이어에 몬스터가 있다고 가정
                if self.is_colliding(obj):
                    if isinstance(obj, Monster):  # 충돌한 객체가 몬스터인지 확인
                        print(f"Potion collided with Monster {obj.monster_id}!")
                        obj.die()  # 몬스터 사망 처리
                        game_world.mark_item_used(self.id)  # 포션 ID를 사용된 것으로 기록
                        game_world.remove_object(self)  # 포션 제거
                        return
                    else:
                        print(f"Potion collided with a non-monster object: {obj.__class__.__name__}")
        elif not self.picked_up:  # 포션이 던져진 상태가 아니고 습득되지 않은 경우
            girl = game_world.get_girl()
            if girl and self.is_colliding(girl):
                self.picked_up = True
                girl.pick_up_item(self)  # 소녀가 포션을 들도록 설정

    def fire(self, x, y, direction):
        """포션 발사"""
        self.x = x
        self.y = y
        self.direction = direction
        self.throwing = True
        game_world.add_object(self, 1)  # 포션을 던질 때 game_world에 다시 추가
        print(f"Potion fired at ({self.x}, {self.y}) in direction {direction}")

    def draw(self):
        """포션을 화면에 그리기"""

        if self.throwing or not self.picked_up:
            self.image.draw(self.x, self.y, self.width, self.height)
            print(f"Drawing Potion at ({self.x}, {self.y})")  # 디버깅 출력

    def draw_at(self, x, y):
        """소녀가 포션을 들고 있을 때 특정 위치에 그리기"""
        self.image.draw(x, y, self.width, self.height)

    def get_bb(self):
        """포션의 히트박스 반환"""
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top

    def is_colliding(self, obj):
        """소녀와의 충돌 여부 확인"""
        left, bottom, right, top = self.get_bb()
        obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()
        return not (right < obj_left or left > obj_right or top < obj_bottom or bottom > obj_top)