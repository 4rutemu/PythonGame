import platform

from pygame import sprite

import game_object
import pygame
import parameters
import enemy
import AttackSprite


class Player(game_object.GameObject):
    def __init__(self):
        super().__init__(x=parameters.WIDTH / 2, y=parameters.HEIGHT / 2, width=20,
                         height=30, colour=parameters.GREEN)

        self.kill_score = 0
        self.hp = parameters.based_hp
        self.j_power = parameters.based_j_power
        self.move_speed = parameters.based_move_speed
        self.attack_power = parameters.based_attack_power
        self.dy = 0
        self.dx = 0
        self.onGround = True
        self.looking_right = True
        self.is_attacking = False

    def get_input(self, pf, enemies):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.onGround:
                self.dy = -self.j_power
        if keys[pygame.K_d]:
            self.dx = self.move_speed
            self.looking_right = True
        if keys[pygame.K_a]:
            self.dx = -self.move_speed
            self.looking_right = False
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            self.dx = 0
        if not self.onGround:
            self.dy += parameters.GRAVITY
        if keys[pygame.K_SPACE] and not self.is_attacking:
            parameters.player_attack_sound.play(maxtime=1000)
            attack = AttackSprite.AttackSprite(owner='player', player=self)
            parameters.all_sprites.add(attack)
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
        self.get_input(pf=platform.platforms, enemies=enemy.enemies)


