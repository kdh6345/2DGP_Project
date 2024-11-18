from pico2d import draw_rectangle, load_image

class Key:
    def __init__(self, x, y):
        self.x = x  # 키의 위치
        self.y = y
        self.width = 50  # 키의 너비
        self.height = 50  # 키의 높이
        self.image = load_image('key.png')  # 키 이미지 파일

    def update(self):
        """필요 시 아이템 업데이트 로직 추가"""
        pass

    def draw(self):
        """키를 화면에 그리기"""
        self.image.draw(self.x, self.y, self.width, self.height)
        # 히트박스 시각화 (디버깅용)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        """키의 히트박스 반환"""
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        return left, bottom, right, top

    def is_colliding(self, obj):
        """키와 소녀 또는 다른 객체가 충돌했는지 확인"""
        key_left, key_bottom, key_right, key_top = self.get_bb()
        obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()

        if key_right < obj_left or key_left > obj_right:
            return False
        if key_top < obj_bottom or key_bottom > obj_top:
            return False
        return True

    def on_pickup(self, inventory):
        """키가 획득되었을 때 실행될 로직"""
        if 'key' not in inventory:
            inventory.append('key')  # 키를 인벤토리에 추가
            return True
        return False
