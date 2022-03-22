import pygame
import keyboard
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Задаём параметры платформ, по которым будет ходить персонаж
PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30
PLATFORM_COLOUR = WHITE

#Создаём уровень. По-хорошему, надо перенести в отдельный файлик с уровнями
FIRST_LVL = [
    "                            ",
    "                            ",
    "                            ",
    "                            ",
    "             --             ",
    "                            ",
    "                            ",
    "        -----               ",
    "                    ---     ",
    "                            ",
    "               ----         ",
    "       -----                ",
    "                            ",
    "    -----------             ",
    "                            ",
    "                   ---      ",
    "                ------      ",
    "                            ",
    "                            ",
    "----------------------------"]

class Game_Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

# Создадим двухмерный массив для первого уровня
# В будущем будет отдельный файл для уровней
class Platforms(Game_Object):
    def draw_lvl(self, LVL, WIDTH, HEIGHT, COLOUR):
        x = y = 0  # координаты
        for row in LVL:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    # создаем блок, заливаем его цветом и рисеум его
                    pf = pygame.Surface((WIDTH, HEIGHT))
                    pf.fill(COLOUR)
                    screen.blit(pf, (x, y))

                x += WIDTH  # блоки платформы ставятся на ширине блоков
            y += HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

# Надо бы перенести в отдельный файл Игрока и Game_Object
class Player(Game_Object):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):

        if keyboard.is_pressed("d"):
            self.rect.x += 10
        if keyboard.is_pressed("a"):
            self.rect.x -= 10

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH


# Создаем игру и окно
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("platformer")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
platform = Platforms()
all_sprites.add(player)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Обновление
    all_sprites.update()

    # Отрисовка
    screen.fill(BLACK)
    platform.draw_lvl(FIRST_LVL, PLATFORM_WIDTH, PLATFORM_HEIGHT, WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
