import platform

from pygame import sprite

import game_object
import pygame
import settings
import enemy

GRAVITY = 0.35
J_POWER = 10
MOVE_SPEED = 7
ATTACK_TIME = 200
ATTACK_WIDTH = 10
ATTACK_HEIGHT = 30


class Player(game_object.GameObject):
    def __init__(self):
        super().__init__(settings.WIDTH / 2, settings.HEIGHT / 2, 30, 30, settings.GREEN)

        self.dy = 0
        self.dx = 0
        self.onGround = True
        self.looking_right = True
        self.looking_down = False
        self.is_attacking = False

    def get_input(self, pf, enemies):
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
            attack = AttackSprite(self.looking_right, self.looking_down, player=self)
            settings.all_sprites.add(attack)
            self.is_attacking = True

        self.onGround = False  # Неизвестно, когда он на земле
        self.rect.y += self.dy
        self.collide(0, self.dy, pf, enemies)

        self.rect.x += self.dx
        self.collide(self.dx, 0, pf, enemies)

    def collide(self, dx, dy, platforms, enemies):
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

        for e in enemies:  # Коллизия с противником
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
        self.get_input(platform.platforms, enemy.enemies)
        if self.rect.left > settings.WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = settings.WIDTH


class AttackSprite(game_object.GameObject):
    def __init__(self, looking_right, looking_down, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = pygame.Surface((ATTACK_WIDTH, ATTACK_HEIGHT))
        self.image.fill(settings.RED)
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
            self.player.is_attacking = False
