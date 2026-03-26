import pygame

from settings import BUTTON_HEIGHT, BUTTON_WIDTH


class Button(pygame.sprite.Sprite):
    instances = pygame.sprite.Group()

    def __init__(self, callback, image_path, top, left):
        super().__init__()
        self.callback = callback
        self.load_image(image_path)
        self.set_position(top, left)
        Button.instances.add(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def load_image(self, image_path):
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (BUTTON_WIDTH, BUTTON_HEIGHT))

    def set_position(self, top, left):
        self.rect = self.image.get_rect()
        self.rect.topleft = left, top

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
