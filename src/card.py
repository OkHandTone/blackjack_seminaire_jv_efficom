import os

import pygame

from settings import CARD_RATIO


class Card(pygame.sprite.Sprite):
    instances = pygame.sprite.Group()

    def __init__(self, x, y, value, filename):
        super().__init__()
        image_path = os.path.join("assets", "cards", filename)
        image = pygame.image.load(image_path)
        width, height = image.get_size()

        Card.instances.add(self)
        self.value = value
        self.image = pygame.transform.scale(image, (width * CARD_RATIO // height, CARD_RATIO))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
