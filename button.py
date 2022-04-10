import pygame


class Button:
    def __init__(self, x, y, image):
        self.clicked = False
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        action = False
        # Узнаём позицию курсора
        pos = pygame.mouse.get_pos()

        # Находим курсор на кнопке и обработка кликов
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
