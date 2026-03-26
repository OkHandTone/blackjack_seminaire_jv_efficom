import os

from src.components.button import Button
from src.settings import BUTTON_HEIGHT, BUTTON_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH


class StandButton(Button):
    def __init__(self, callback):
        image_path = os.path.join("assets", "buttons", "stand.bmp")
        left = WINDOW_WIDTH - BUTTON_WIDTH * 2 - 20
        top = WINDOW_HEIGHT - BUTTON_HEIGHT - 10
        super().__init__(callback, image_path, top, left)
