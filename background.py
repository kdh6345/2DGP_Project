#background.py
from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('start room1.png')


    def update(self):
        pass

    def draw(self):
        self.image.draw(575.5, 300)


class Fence:
    def __init__(self):
        self.image=load_image('fence.png')
    def update(self):
        pass
    def draw(self):
        self.image.draw(185,110,210,170)

