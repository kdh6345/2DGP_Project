#game_world.py
from girl import Girl
from monster import Monster
from item import Potion
from pico2d import *

objects = [[] for _ in range(4)]
girl = None  # 소녀 객체를 전역으로 관리
monsters = {}  # 방별로 몬스터를 저장하는 딕셔너리
monster_positions = {}  # 방별 몬스터 위치 저장
items = []  # 현재 들고 있는 아이템 관리
dead_monsters = {}  # 죽은 몬스터 ID 저장
used_items = {}  # {item_id: True/False} 형태로 사용 상태 관리
picked_items = {}  # {item_id: True/False} 형태로 픽업 상태 관리
obstacles = []  # 장애물 객체를 저장하는 리스트

girl_safe = False  # 소녀의 안전 상태
potion_state = None  # 소녀가 들고 있는 포션 상태 저장
current_mode = None  # 현재 게임 모드(방) 저장
girl_holding_item = None  # 소녀가 들고 있는 아이템
slot_image = None
heart_image = None
cantgo = False  # 전역 변수로 선언
hall3open = False  # Hall3의 열림 상태를 관리하는 전역 변수
kitchen2open=False

def set_cantgo(state):
    """cantgo 상태를 설정"""
    global cantgo
    cantgo = state

def is_cantgo():
    """cantgo 상태를 반환"""
    global cantgo
    return cantgo

def set_girl_safe(safe):
    """소녀의 안전 상태를 설정"""
    global girl_safe
    girl_safe = safe

def is_girl_safe():
    """소녀가 안전한지 반환"""
    return girl_safe

# 슬롯 상태 초기화 (False는 비어있음, True는 하트가 채워짐)
slots = [False, False, False]

# 슬롯 위치 초기화 (화면 하단에 3개 배치)
slot_positions = [(300, 50), (360, 50), (420, 50)]

def init_slot_images():
    """슬롯 및 하트 이미지를 초기화"""
    global slot_image, heart_image
    try:
        slot_image = load_image('slot.png')  # 슬롯 이미지 로드
        heart_image = load_image('heart.png')  # 하트 이미지 로드
    except:
        print("Error: Failed to load slot.png or heart.png")
        slot_image = None
        heart_image = None

def collect_heart():
    """하트를 수집하여 빈 슬롯에 추가"""
    for i in range(len(slots)):
        if not slots[i]:  # 비어있는 슬롯을 찾으면
            slots[i] = True
            return True
    return False  # 슬롯이 모두 차 있으면 아무 일도 하지 않음

def is_slot_filled(index):
    """슬롯이 채워져 있는지 확인"""
    if 0 <= index < len(slots):
        return slots[index]
    return False
def are_all_slots_filled():
    """슬롯이 모두 채워졌는지 확인"""
    return all(slots)  # 모든 슬롯이 True인지 확인

def reset_slots():
    """슬롯 초기화"""
    global slots
    slots = [False, False, False]

def add_obstacle(obstacle):
    """장애물을 추가"""
    obstacles.append(obstacle)

def get_obstacles():
    """현재 등록된 모든 장애물을 반환"""
    return obstacles

def is_point_in_obstacle(x, y):
    """주어진 좌표가 장애물 내부에 있는지 확인"""
    for obstacle in obstacles:
        if hasattr(obstacle, 'get_bb'):
            left, bottom, right, top = obstacle.get_bb()
            if left <= x <= right and bottom <= y <= top:
                return True
    return False
def draw_slots():
    """슬롯과 하트를 화면에 그리기"""
    global slot_image, heart_image

    if slot_image is None or heart_image is None:
        init_slot_images()  # 이미지 초기화

    if slot_image is None or heart_image is None:
        print("Error: Slot or heart image is not loaded.")
        return

    for i, position in enumerate(slot_positions):
        x, y = position
        slot_image.draw(x, y, 50, 50)  # 슬롯 그리기
        if is_slot_filled(i):  # 슬롯에 하트가 있으면
            heart_image.draw(x, y, 50, 50)  # 하트 그리기

def set_hall3open(state):
    """Hall3로 이동 가능 여부를 설정"""
    global hall3open
    hall3open = state

def is_hall3open():
    """Hall3로 이동 가능 여부를 반환"""
    global hall3open
    return hall3open

def set_kitchen2open(state):
    """Hall3로 이동 가능 여부를 설정"""
    global kitchen2open
    kitchen2open = state

def is_kitchen2open():
    """Hall3로 이동 가능 여부를 반환"""
    global kitchen2open
    return kitchen2open


def set_cantgo(state):
    """cantgo 상태를 설정"""
    global cantgo
    cantgo = state

def is_cantgo():
    """cantgo 상태를 반환"""
    return cantgo

def set_cantgo_start_time(start_time):
    """cantgo 메시지 시작 시간을 설정"""
    global cantgo_start_time
    cantgo_start_time = start_time

def get_cantgo_start_time():
    """cantgo 메시지 시작 시간을 반환"""
    return cantgo_start_time

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
        #print(f"[DEBUG] Loading holding item: {girl_holding_item.__class__.__name__}")
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
    used_items[item_id] = True

def is_item_used(item_id):
    """아이템이 사용된 상태인지 확인"""
    return used_items.get(item_id, False)  # 기본값 False

def mark_item_picked(item_id):
    """아이템을 픽업된 상태로 기록"""
    picked_items[item_id] = True

def is_item_picked(item_id):
    """아이템이 픽업된 상태인지 확인"""
    return picked_items.get(item_id, False)  # 기본값 False

# 상태 초기화 함수 (테스트 또는 초기화 필요 시)
def reset_item_states():
    """아이템 상태를 초기화"""
    used_items.clear()
    picked_items.clear()

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

def mark_monster_dead(room_name, monster_id):
    """특정 방의 몬스터를 죽은 상태로 기록"""
    if room_name not in dead_monsters:
        dead_monsters[room_name] = set()
    dead_monsters[room_name].add(monster_id)
    print(f"[DEBUG] Marking monster {monster_id} in room '{room_name}' as dead.")

def is_monster_dead(room_name, monster_id):
    """특정 방의 몬스터가 죽었는지 확인"""
    return room_name in dead_monsters and monster_id in dead_monsters[room_name]

def mark_item_used(item_id):
    """아이템을 사용된 상태로 기록"""
    used_items[item_id] = True  # `add` 대신 `dict` 방식으로 기록

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
        print(f"[DEBUG] Saved monster state for room '{room_name}': {monster_positions[room_name]}")

def load_monster_state(room_name):
    """특정 방의 몬스터 상태 복원"""
    return monster_positions.get(room_name)

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
            pass
           #print("Girl collided with a stair")  # 디버깅 로그 추가
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
