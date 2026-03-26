import pygame

from components.button import Button
from settings import GAME_BACKGROUND, WINDOW_WIDTH


class AceToggle(Button):
    def __init__(self, on_change):
        self.ace_value = 11
        self.on_change = on_change
        pygame.sprite.Sprite.__init__(self)
        self._build_image()
        self.set_position(top=10, left=WINDOW_WIDTH - 220)
        self.callback = self._toggle
        Button.instances.add(self)

    def _toggle(self):
        self.ace_value = 1 if self.ace_value == 11 else 11
        self._build_image()
        self.on_change(self.ace_value)

    def _build_image(self):
        width, height = 210, 40
        surface = pygame.Surface((width, height))
        surface.fill(GAME_BACKGROUND)

        font = pygame.font.SysFont("Arial", 16, bold=True)

        # label gauche "1"
        col_1 = (255, 255, 255) if self.ace_value == 1 else (150, 150, 150)
        # label droit "11"
        col_11 = (255, 255, 255) if self.ace_value == 11 else (150, 150, 150)

        label = font.render("As :", True, (255, 255, 255))
        text_1 = font.render("1", True, col_1)
        text_11 = font.render("11", True, col_11)

        # dessin du track du switch
        track_x, track_y = 90, 10
        track_w, track_h = 60, 20
        pygame.draw.rect(
            surface,
            (80, 80, 80),
            (track_x, track_y, track_w, track_h),
            border_radius=10,
        )

        # dessin du curseur
        if self.ace_value == 1:
            knob_x = track_x + 4
        else:
            knob_x = track_x + track_w - 24

        pygame.draw.circle(surface, (255, 255, 255), (knob_x + 10, track_y + 10), 10)

        surface.blit(label, (5, 10))
        surface.blit(text_1, (72, 10))
        surface.blit(text_11, (155, 10))

        self.image = surface
