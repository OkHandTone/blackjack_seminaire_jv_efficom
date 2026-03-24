import os

import pygame

from settings import CARD_RATIO, WINDOW_HEIGHT


class Card(pygame.sprite.Sprite):
    instances = pygame.sprite.Group()

    def __init__(self, rank, suit, cards, player):
        super().__init__()
        Card.instances.add(self)

        image_path = os.path.join("assets", "cards", f"{rank}{suit}.bmp")
        image = pygame.image.load(image_path)
        width, height = image.get_size()
        self.image = pygame.transform.scale(image, (width * CARD_RATIO // height, CARD_RATIO))

        if player == 1:
            top = 10
        else:
            top = WINDOW_HEIGHT - self.image.get_height() - 10
        left = 10 + ((self.image.get_width() + 10) * cards)
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(left), top)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
