import os

import pygame

from settings import CARD_HEIGHT, CARD_WIDTH, WINDOW_HEIGHT


class Card(pygame.sprite.Sprite):
    instances = pygame.sprite.Group()

    def __init__(self, rank, suit, cards, player, isFlipped):
        super().__init__()
        self.rank = rank
        self.suit = suit
        self.cards = cards
        self.player = player
        self.isFlipped = isFlipped
        Card.instances.add(self)

        if self.isFlipped:
            self.load_image()
        else:
            self.load_white_background()

        self.set_position()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def load_image(self):
        image_path = os.path.join("assets", "cards", f"{self.rank}{self.suit}.bmp")
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

    def load_white_background(self):
        self.image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.image.fill((255, 255, 255))

    def show(self):
        self.load_image()
