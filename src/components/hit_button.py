import os

from components.button import Button


class HitButton(Button):
    def __init__(self, callback):
        image_path = os.path.join("assets", "buttons", "hit.bmp")
        super().__init__(callback, image_path)
