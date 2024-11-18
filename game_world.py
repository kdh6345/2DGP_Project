#game_world.py
from girl import Girl

objects = [[] for _ in range(4)]
girl = None  # 소녀 객체를 전역으로 관리

def add_object(o, depth=0):
    global girl
    if isinstance(o, Girl):  # Girl 객체라면 저장
        girl = o
    objects[depth].append(o)

def get_girl():
    """소녀 객체를 반환"""
    return girl

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
