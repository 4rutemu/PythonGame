import pygame
import keyboard
import random

from pygame import sprite

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
MOVE_SPEED = 7
ATTACK_TIME = 200
ATTACK_WIDTH = 10
ATTACK_HEIGHT = 30


class AttackSprite(GameObject):
    def __init__(self, looking_right):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ATTACK_WIDTH, ATTACK_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        if looking_right:
            self.rect.left = player.rect.right
            self.rect.top = player.rect.top
            self.creation_time = pygame.time.get_ticks()
        if not looking_right:
            self.rect.right = player.rect.left
            self.rect.top = player.rect.top
            self.creation_time = pygame.time.get_ticks()

    def update(self):
        if (pygame.time.get_ticks() - self.creation_time) > ATTACK_TIME:
            self.kill()
            player.is_attacking = False


class Player(GameObject):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.yvel = 0
        self.xvel = 0
        self.onGround = True
        self.looking_right = True
        self.is_attacking = False

    def get_input(self, platforms):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.onGround:
                self.yvel = -J_POWER
        if keys[pygame.K_d]:
            self.xvel = MOVE_SPEED
            self.looking_right = True
        if keys[pygame.K_a]:
            self.xvel = -MOVE_SPEED
            self.looking_right = False
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY
        if keys[pygame.K_SPACE] and not self.is_attacking:
            attack = AttackSprite(self.looking_right)
            all_sprites.add(attack)
            self.is_attacking = True

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

    def update(self):
        self.get_input(platforms)
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
