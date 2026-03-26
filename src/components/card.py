import os

import pygame

from settings import CARD_HEIGHT, CARD_WIDTH, WINDOW_HEIGHT


class Card(pygame.sprite.Sprite):
    instances = pygame.sprite.Group()

    def __init__(self, rank, suit, cards, player, isFlipped):
        super().__init__()
        self.player = player
        self.cards = cards
        self.image_path = f"{rank}{suit}.bmp"
        Card.instances.add(self)

        if isFlipped:
            self.load_image(self.image_path)
        else:
            self.load_image("back.bmp")

        self.set_position()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def load_image(self, filename):
        image_path = os.path.join("assets", "cards", filename)
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))

    def set_position(self):
        if self.player == 1:
            top = 10
        else:
            top = WINDOW_HEIGHT - CARD_HEIGHT - 10
        left = 10 + ((CARD_WIDTH + 10) * self.cards)
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(left), top)

    def show(self):
        self.load_image(self.image_path)
