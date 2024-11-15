# game_framework.py
from pico2d import *

running = True
current_state = None

def run(start_state):
    global current_state, running
    current_state = start_state
    current_state.init()

    while running:
        handle_events()
        current_state.update()
        current_state.draw()
        delay(0.03)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
