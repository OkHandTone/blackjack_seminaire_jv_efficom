import pygame

from card import Card
from settings import DISPLAY_CAPTION


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(DISPLAY_CAPTION)

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        Card(0, 0, 10, "10.bmp")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0, 0, 0))
            Card.instances.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
