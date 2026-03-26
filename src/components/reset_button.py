import os

from components.button import Button
from settings import BUTTON_HEIGHT, BUTTON_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH


class ResetButton(Button):
    def __init__(self, callback):
        image_path = os.path.join("assets", "buttons", "reset_button.bmp")
        left = WINDOW_WIDTH - BUTTON_WIDTH * 3 - 30
        top = WINDOW_HEIGHT - BUTTON_HEIGHT - 10
        super().__init__(callback, image_path, top, left)
