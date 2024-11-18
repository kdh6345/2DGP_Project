from pico2d import load_image, draw_rectangle
import game_world

class Item:
    """아이템의 공통 클래스"""
    def __init__(self, x, y, width, height, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = load_image(image_path)
        self.picked_up = False

    def update(self):
        """소녀와 충돌 체크 후 아이템을 들게 설정"""
        girl = game_world.get_girl()  # game_world에서 소녀 객체 가져오기
        if not self.picked_up and self.is_colliding(girl):
            self.picked_up = True
            girl.pick_up_item(self)

    def draw(self):
        """아이템을 화면에 그리기 (습득되지 않은 경우)"""
        if not self.picked_up:
            self.image.draw(self.x, self.y, self.width, self.height)
            draw_rectangle(*self.get_bb())

    def draw_at(self, x, y):
        """소녀가 들고 있을 때의 위치에 아이템을 그리기"""
        self.image.draw(x, y, self.width, self.height)

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