#game_world.py
from girl import Girl
from monster import Monster
from item import Potion

objects = [[] for _ in range(4)]
girl = None  # 소녀 객체를 전역으로 관리
monsters = {}  # 방별로 몬스터를 저장하는 딕셔너리
monster_positions = {}  # 방별 몬스터 위치 저장
items = []  # 현재 들고 있는 아이템 관리
dead_monsters = set()  # 죽은 몬스터 ID 저장
used_items = set()     # 사용된 아이템 ID 저장
picked_items=set()
potion_state = None  # 소녀가 들고 있는 포션 상태 저장
current_mode = None  # 현재 게임 모드(방) 저장
girl_holding_item = None  # 소녀가 들고 있는 아이템

def save_girl_holding_item(item):
    """소녀가 들고 있는 아이템 상태를 저장"""
    global girl_holding_item
    girl_holding_item = item

def load_girl_holding_item():
    """소녀가 들고 있는 아이템 상태를 반환"""
    global girl_holding_item
    if girl_holding_item:
        # 아이템이 사용된 상태인지 확인
        if isinstance(girl_holding_item, Potion) and is_item_used(girl_holding_item.id):
            print("[DEBUG] Used potion detected, not restoring.")
            return None  # 사용된 포션은 복원하지 않음
        print(f"[DEBUG] Loading holding item: {girl_holding_item.__class__.__name__}")
    else:
        print("[DEBUG] No holding item found.")
    return girl_holding_item


def add_object(o, depth=0):
    if o is None:  # 객체가 None인 경우 추가하지 않음
        return

    global girl
    if isinstance(o, Girl):  # Girl 객체라면 저장
        girl = o
    objects[depth].append(o)

def add_item(item):
    """아이템을 게임 월드에 추가"""
    if item not in items:
        items.append(item)
def remove_item(item):
    """아이템을 게임 월드에서 제거"""
    if item in items:
        items.remove(item)

def mark_item_used(item_id):
    """아이템을 사용된 상태로 기록"""
    used_items.add(item_id)

def is_item_used(item_id):
    """아이템이 사용된 상태인지 확인"""
    return item_id in used_items

def get_items():
    """현재 들고 있는 아이템 리스트 반환"""
    return items
def clear_items():
    """아이템 리스트 초기화"""
    global items
    items.clear()
def set_monster_for_room(room_name, monster):
    """특정 방에 몬스터를 설정"""
    monsters[room_name] = monster

def get_monster_for_room(room_name):
    """특정 방에 설정된 몬스터를 반환"""
    return monsters.get(room_name)

def remove_monster_for_room(room_name):
    """특정 방에서 몬스터를 제거"""
    if room_name in monsters:
        del monsters[room_name]
def set_monster_position_for_room(room_name, position):
    """특정 방의 몬스터 위치를 저장"""

    monster_positions[room_name] = position

def get_monster_position_for_room(room_name):
    """특정 방의 몬스터 위치를 반환"""
    return monster_positions.get(room_name, None)

def set_current_mode(mode_name):
    global current_mode
    current_mode = mode_name

def mark_monster_dead(monster_id):
    """몬스터를 죽은 상태로 기록"""
    dead_monsters.add(monster_id)

def is_monster_dead(monster_id):
    """몬스터가 죽었는지 확인"""
    return monster_id in dead_monsters

def mark_item_used(item_id):
    """아이템을 사용된 상태로 기록"""
    used_items.add(item_id)

def is_item_used(item_id):
    """아이템이 사용된 상태인지 확인"""
    return item_id in used_items

def save_potion_state(potion):
    """소녀가 들고 있는 포션 상태를 저장"""
    global potion_state
    potion_state = potion

def load_potion_state():
    """소녀가 들고 있는 포션 상태를 반환"""
    return potion_state

def clear_potion_state():
    """포션 상태 초기화"""
    global potion_state
    potion_state = None

def get_girl():
    """소녀 객체를 반환"""
    global girl
    return girl
def save_girl_state():
    """소녀의 상태를 저장"""
    global girl
    if girl:
        return {'x': girl.x, 'y': girl.y, 'holding_item': girl.holding_item}
    return None

def load_girl_state(state):
    """저장된 소녀의 상태를 복원"""
    global girl
    if girl and state:
        girl.x, girl.y = state['x'], state['y']
        girl.holding_item = state['holding_item']

def save_monster_state(room_name, monster):
    """특정 방의 몬스터 상태 저장"""
    if monster:
        monster_positions[room_name] = (monster.x, monster.y, monster.is_dying)

def set_girl(new_girl):
    global girl
    girl=new_girl

def update():
    for layer in objects:
        for o in layer:
            if o:
                o.update()
        # 계단 충돌 처리는 소녀와만 수행

    for stair in objects_at(2):  # 계단은 2번 레이어에 있음
        girl = get_girl()
        if collide(girl, stair):
            print("Girl collided with a stair")  # 디버깅 로그 추가
            # 필요한 계단 이동 처리 (예: 소녀의 위치 수정)


def render():
    for layer in objects:
        for o in layer:
            if o:  # 객체가 None인지 확인
                o.draw()

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')

def collide(a, b):
    """a와 b의 히트박스 비교"""
    # 계단과의 충돌 처리는 소녀와의 충돌만 검사
    from girl import Girl
    if isinstance(a, Girl) or isinstance(b, Girl):  # a 또는 b 중 하나가 소녀일 때만
        left_a, bottom_a, right_a, top_a = a.get_bb()
        left_b, bottom_b, right_b, top_b = b.get_bb()

        if left_a > right_b or right_a < left_b:
            return False
        if bottom_a > top_b or top_a < bottom_b:
            return False

        return True

    return False  # 소녀가 아닌 경우 항상 False

def objects_at(layer):
    return objects[layer]


def clear():
    global objects

    objects = [[] for _ in range(4)]

def clear_except(except_object):
    global objects
    for layer in objects:
        layer[:] = [o for o in layer if o == except_object]
