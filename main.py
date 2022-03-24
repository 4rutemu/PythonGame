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

PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30
PLATFORM_COLOUR = WHITE

# Создаём уровень. По-хорошему, надо перенести в отдельный файлик с уровнями
platforms = []  # Массив платформ
FIRST_LVL = [
    "                            ",
    "                            ",
    "                            ",
    "                            ",
    "             --             ",
    "                            ",
    "                            ",
    "-----   -----               ",
    "                    ---     ",
    "                            ",
    "----   --------            ",
    "                            ",
    "                            ",
    "---------------             ",
    "                            ",
    "                      ------",
    "                ------------",
    "                            ",
    "                            ",
    "----------------------------"]


class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


# Создадим двухмерный массив для первого уровня
# В будущем будет отдельный файл для уровней


def draw_lvl(LVL):
    x = y = 0  # координаты
    for row in LVL:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platforms(x, y)
                all_sprites.add(pf)
                platforms.append(pf)
                # Заносим платформу в массив для последующей проверки пересечений

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля


class Platforms(GameObject):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(WHITE)
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


# Надо бы перенести в отдельный файл Игрока и Game_Object


GRAVITY = 0.35
J_POWER = 10


class Player(GameObject):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.yvel = 0
        self.onGround = False

    def update(self):
        self.rect.y += self.yvel
        self.onGround = False

        if keyboard.is_pressed("d"):
            self.rect.x += 10

        if keyboard.is_pressed("a"):
            self.rect.x -= 10

        if keyboard.is_pressed("w"):
            self.onGround = True
            if self.onGround:
                self.yvel = -J_POWER

        if keyboard.is_pressed("s"):
            self.onGround = False

        if not self.onGround:
            self.yvel += GRAVITY

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

draw_lvl(FIRST_LVL)
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

    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
