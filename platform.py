import game_object


PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30
PLATFORM_COLOUR = (255, 255, 255)

stoppers = []
platforms = []


class Platform(game_object.GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOUR)
