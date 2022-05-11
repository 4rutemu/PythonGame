import random

import pygame
from pygame import sprite

import game_object
import parameters
import platform
from AttackSprite import AttackSprite
import animator

enemies = []
speed_list = [-7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7]
enemy_hp = [5, 10, 15, 20, 25]


class Enemy(game_object.GameObject):
    def __init__(self, x, y, player):
        self.hp = enemy_hp[random.randint(0, 4)]
        if self.hp == 5 or self.hp == 10:
            self.colour = parameters.YELLOW
        elif self.hp == 20 or self.hp == 25:
            self.colour = parameters.RED
        else:
            self.colour = parameters.BLUE
        super().__init__(x=x, y=y, width=20, height=30, colour=self.colour)
        self.player = player
        self.dx = speed_list[random.randint(0, 8)]
        # Так как враг будет перемещаться к игроку + для колизии
        self.attacked = False
        self.is_attacking = False

        self.id = len(enemies)

        self.run_images = [1, pygame.image.load("AnimationImages/Skeleton/walk_1.png").convert_alpha(),
                           pygame.image.load("AnimationImages/Skeleton/walk_2.png").convert_alpha(),
                           pygame.image.load("AnimationImages/Skeleton/walk_3.png").convert_alpha(),
                           pygame.image.load("AnimationImages/Skeleton/walk_4.png").convert_alpha(),
                           pygame.image.load("AnimationImages/Skeleton/walk_5.png").convert_alpha(),
                           pygame.image.load("AnimationImages/Skeleton/walk_6.png").convert_alpha()]

        self.left_run_images = [1, pygame.image.load("AnimationImages/Skeleton/walk_1-left.png").convert_alpha(),
                                pygame.image.load("AnimationImages/Skeleton/walk_2-left.png").convert_alpha(),
                                pygame.image.load("AnimationImages/Skeleton/walk_3-left.png").convert_alpha(),
                                pygame.image.load("AnimationImages/Skeleton/walk_4-left.png").convert_alpha(),
                                pygame.image.load("AnimationImages/Skeleton/walk_5-left.png").convert_alpha(),
                                pygame.image.load("AnimationImages/Skeleton/walk_6-left.png").convert_alpha()]

        self.attack_image = pygame.image.load("AnimationImages/Skeleton/attack1_4.png").convert_alpha()
        self.left_attack_image = pygame.image.load("AnimationImages/Skeleton/attack1_4-left.png").convert_alpha()

    def enemy_collide(self, dx, pf, stop_list):
        for p in pf:
            if sprite.collide_rect(self, p):  # Проверяем на пересечение противника с платформой
                if dx > 0:  # Если противник движется вправо, то запрещаем
                    self.rect.right = p.rect.left
                    self.dx *= -1
                if dx < 0:  # Если противник движется в лево, то запрещаем
                    self.rect.left = p.rect.right
                    self.dx *= -1
        if sprite.collide_rect(self, self.player):
            if self.dx > 0:
                self.rect.right = self.player.rect.left
                self.dx *= -1
            elif self.dx < 0:
                self.rect.left = self.player.rect.right
                self.dx *= -1
        for s in stop_list:
            if sprite.collide_rect(self, s):
                if dx > 0:  # Если противник движется вправо, то запрещаем
                    self.rect.right = s.rect.left
                    self.dx *= -1
                if dx < 0:  # Если противник движется в лево, то запрещаем
                    self.rect.left = s.rect.right
                    self.dx *= -1

    def moving(self, pf, stop_list):  # Функция с перемещением противника
        self.rect.x += self.dx
        if self.dx > 0:
            animator.animation(self, self.run_images, len(self.run_images))
        else:
            animator.animation(self, self.left_run_images, len(self.left_run_images))
        self.enemy_collide(dx=self.dx, pf=pf, stop_list=stop_list)

    def update(self):
        self.moving(pf=platform.platforms, stop_list=platform.stoppers)

        if (self.player.rect.y + 3 >= self.rect.y >= self.player.rect.y - 3) and (
                (abs(self.rect.x - self.player.rect.x + self.player.rect.width) < parameters.ATTACK_WIDTH) or (
                abs(self.rect.x - self.player.rect.x - self.player.rect.width) < parameters.ATTACK_WIDTH)):
            if not self.attacked and random.randint(0, 4) == 3:  # немного глупости чтобы не был непобедимым

                if self.dx > 0:
                    self.image = self.attack_image
                else:
                    self.image = self.left_attack_image
                attack = AttackSprite(owner=self.id, player=self.player)
                parameters.all_sprites.add(attack)
                self.attacked = True
                self.is_attacking = True
        else:
            self.is_attacking = False
            self.attacked = False
        if self.hp <= 0:
            parameters.npc_damage.play()
            self.rect.x = -600000
            self.player.kill_score += 1
            self.player.move_speed += 0.5  # Для большей динамичности будет увеличиваться скорость передвижения после
            # убийства противника
            self.kill()

