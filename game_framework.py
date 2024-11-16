import time

running = True
stack = []
frame_time = 0.0  # 프레임 간 경과 시간

def change_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.enter()

def push_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(mode)
    mode.enter()

def pop_mode():
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    if len(stack) > 0:
        stack[-1].resume()

def quit():
    global running
    running = False

def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]
    start_mode.enter()

    current_time = time.time()  # 현재 시간을 기록

    while running:
        # frame_time 계산
        new_time = time.time()
        frame_time = new_time - current_time
        current_time = new_time

        # 현재 모드 실행
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while len(stack) > 0:
        stack[-1].finish()
        stack.pop()
