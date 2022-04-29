import pygame

import game_object


PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30
PLATFORM_COLOUR = (255, 255, 255)

stoppers = []
platforms = []


class Platform(game_object.GameObject):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT, colour=PLATFORM_COLOUR)
        self.image = pygame.image.load("Platforms images/center.png").convert_alpha()
