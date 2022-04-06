import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, colour):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
