#game_world.py
from girl import Girl
from monster import Monster

objects = [[] for _ in range(4)]
girl = None  # 소녀 객체를 전역으로 관리
monsters = {}  # 방별로 몬스터를 저장하는 딕셔너리
monster_positions = {}  # 방별 몬스터 위치 저장

current_mode = None  # 현재 게임 모드(방) 저장

def add_object(o, depth=0):

    global girl
    if isinstance(o, Girl):  # Girl 객체라면 저장
        girl = o
    objects[depth].append(o)

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

def get_girl():
    """소녀 객체를 반환"""
    global girl
    return girl

def set_girl(new_girl):
    global girl
    girl=new_girl

def update():
    for layer in objects:
        for o in layer:
            o.update()

def render():
    for layer in objects:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')

def collide(a, b):
    # a와 b의 히트박스 비교
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b or right_a < left_b:
        return False
    if bottom_a > top_b or top_a < bottom_b:
        return False

    return True

def objects_at(layer):
    return objects[layer]


def clear():
    global objects

    objects = [[] for _ in range(4)]

def clear_except(except_object):
    global objects
    for layer in objects:
        layer[:] = [o for o in layer if o == except_object]
