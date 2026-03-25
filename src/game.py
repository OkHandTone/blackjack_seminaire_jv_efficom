import pygame

from components.card import Card
from components.hit_button import HitButton
from settings import DISPLAY_CAPTION, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(DISPLAY_CAPTION)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                HitButton.instances.update(event)
            self.render()

            self.clock.tick(60)
        pygame.quit()

    def render(self):
        self.screen.fill((0, 0, 0))
        Card.instances.draw(self.screen)
        HitButton.instances.draw(self.screen)
        pygame.display.flip()
