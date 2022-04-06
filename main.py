import pygame
import keyboard
import random
from pygame import sprite

WIDTH = 800
HEIGHT = 600
FPS = 45

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

GRAVITY = 0.35
J_POWER = 10
MOVE_SPEED = 7

ATTACK_TIME = 200
ATTACK_WIDTH = 10
ATTACK_HEIGHT = 30

platforms = []  # Массив платформ
enemys = []
stoppers = []
first_lvl = [
    "                             ",
    "                             ",
    "                             ",
    "                             ",
    "             --              ",
    "                             ",
    "x   e x x  e  x              ",
    " -----   -----               ",
    "                    ---      ",
    "                             ",
    "----   --------              ",
    "                             ",
    "                             ",
    "---------------              ",
    "                             ",
    "               x    e -------",
    "                -------------",
    "                             ",
    "x      e                     x",
    "---------------------------- "]


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

def draw_lvl(LVL):
    x = y = 0
    for row in LVL:
        for col in row:
            if col == "":  # Пропускаем пустые символы, чтобы не тратить лишнее время
                continue
            elif col == "-":
                pf = Platforms(x, y)
                all_sprites.add(pf)
                platforms.append(pf)
            elif col == "x":
                stop = Platforms(x, y)
                stoppers.append(stop)

            elif col == "e":
                enemy = Enemy(x, y)
                all_sprites.add(enemy)
                enemys.append(enemy)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля


class Platforms(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT, WHITE)


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
        if looking_down:  # Для удара снизу
            pass

    def update(self):
        if (pygame.time.get_ticks() - self.creation_time) > ATTACK_TIME:
            self.kill()
            player.is_attacking = False


class Player(GameObject):
    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT / 2, 30, 30, GREEN)

        self.dy = 0
        self.dx = 0
        self.onGround = True
        self.looking_right = True
        self.looking_down = False
        self.is_attacking = False

    def get_input(self, platforms, enemys):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.onGround:
                self.dy = -J_POWER
        if keys[pygame.K_d]:
            self.dx = MOVE_SPEED
            self.looking_right = True
        if keys[pygame.K_a]:
            self.dx = -MOVE_SPEED
            self.looking_right = False
        if keys[pygame.K_s]:
            self.looking_down = True
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            self.dx = 0
        if not self.onGround:
            self.dy += GRAVITY
        if keys[pygame.K_SPACE] and not self.is_attacking:
            attack = AttackSprite(self.looking_right, self.looking_down)
            all_sprites.add(attack)
            self.is_attacking = True

        self.onGround = False  # Неизвестно, когда он на земле
        self.rect.y += self.dy
        self.collide(0, self.dy, platforms, enemys)

        self.rect.x += self.dx
        self.collide(self.dx, 0, platforms, enemys)

    def collide(self, dx, dy, platforms, enemys):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if dx > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if dx < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if dy > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.dy = 0  # и энергия падения пропадает

                if dy < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.dy = 0  # и энергия прыжка пропадает

        for e in enemys:  # Коллизия с противником
            if sprite.collide_rect(self, e):
                if dx > 0:
                    self.rect.right = e.rect.left
                if dx < 0:
                    self.rect.left = e.rect.right
                if dy > 0:
                    self.rect.bottom = e.rect.top
                    self.onGround = True
                    self.dy = 0

    def update(self):
        self.get_input(platforms, enemys)
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH


# TODO: получение урона от атак
class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, YELLOW)
        self.dx = 0
        # Так как враг будет перемещаться к игроку + для колизии
        if random.random() != 0:
            self.dx = 2
        else:
            self.dx = -2

    def enemy_collide(self, dx, platforms, stoppers):
        for p in platforms:
            if sprite.collide_rect(self, p):  # Проверяем на пересечение противника с платформой
                if dx > 0:  # Если противник движется вправо, то запрещаем
                    self.rect.right = p.rect.left
                    self.dx = -2
                if dx < 0:  # Если противник движется в лево, то запрещаем
                    self.rect.left = p.rect.right
                    self.dx = 2

        for s in stoppers:
            if sprite.collide_rect(self, s):
                if dx > 0:  # Если противник движется вправо, то запрещаем
                    self.rect.right = s.rect.left
                    self.dx = -2
                if dx < 0:  # Если противник движется в лево, то запрещаем
                    self.rect.left = s.rect.right
                    self.dx = 2

    def moving(self, plarforms, stoppers):  # Функция с перемещением противника
        self.rect.x += self.dx
        self.enemy_collide(self.dx, platforms, stoppers)

    def update(self):
        self.moving(platforms, stoppers)


# Создаем игру и окно
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time_Killer")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()

draw_lvl(first_lvl)
all_sprites.add(player)


def game():
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Обновление
        all_sprites.update()

        # Отрисовка
        screen.fill(BLACK)

        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
game()
