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
YELLOW = (255, 255, 0)

PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30
PLATFORM_COLOUR = WHITE

platforms = []  # Массив платформ
enemys = []
FIRST_LVL = [
    "                            ",
    "                            ",
    "                            ",
    "                            ",
    "             --             ",
    "          e                  ",
    "  e                         ",
    "-----   -----               ",
    "                    ---     ",
    "                            ",
    "----   --------            ",
    "                            ",
    "                            ",
    "---------------             ",
    "                            ",
    "                    e ------",
    "    e           ------------",
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

            if col == "e":
                enemy = Enemy(x, y)
                all_sprites.add(enemy)
                enemys.append(enemy)

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
    def __init__(self, looking_right, looking_down):
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
        if looking_down: #Для удара снизу
            pass

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
        self.looking_down = False
        self.is_attacking = False

    def get_input(self, platforms, enemys):
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
        if keys[pygame.K_s]:
            self.looking_down = True
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY
        if keys[pygame.K_SPACE] and not self.is_attacking:
            attack = AttackSprite(self.looking_right, self.looking_down)
            all_sprites.add(attack)
            self.is_attacking = True

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, enemys)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, enemys)

    def collide(self, xvel, yvel, platforms, enemys):
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

        for e in enemys: # Коллизия с противником
            if sprite.collide_rect(self, e):
                if xvel > 0:
                    self.rect.right = e.rect.left
                if xvel < 0:
                    self.rect.left = e.rect.right
                if yvel > 0:
                    self.rect.bottom = e.rect.top
                    self.onGround = True
                    self.yvel = 0

    def update(self):
        self.get_input(platforms, enemys)
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH


#TODO: Сделать врагам физику, коллизии, получение урона от атак
class Enemy(GameObject):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.onGround = False
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = pygame.Rect(x, y, 30, 30)
        #Так как враг будет перемещаться к игроку + для колизии
        self.xvel = 0
        self.yvel = 0

    def enemy_collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # Проверяем на пересечение противника с платформой

                if xvel > 0:  # Если противник движется вправо, то запрещаем
                    self.rect.right = p.rect.left

                if xvel < 0:  # Если противник движется в лево, то запрещаем
                    self.rect.left = p.rect.right

                if yvel > 0:  # Если противник падает вниз под гравитацией,
                    self.rect.bottom = p.rect.top  # то не падает вниз, как только сопрекасается с верхушкой платформы
                    self.onGround = True  # и становится на ноги твёрдо
                    self.yvel = 0  # Убираем энергию падения

                if yvel < 0:  # Если противник движется вверх, то запрещаем ему двигаться туда
                    self.rect.top = p.rect.bottom
                    self.yvel = 0  # Убираем энергию прыжка

    def moving(self, platfroms): # Функция с перемещением противника
        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.enemy_collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.enemy_collide(self.xvel, 0, platforms)
    def update(self):
        self.moving(platforms)


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
