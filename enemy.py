import random

from pygame import sprite

import game_object
import platform

enemies = []


# TODO: получение урона от атак
class Enemy(game_object.GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, (255, 255, 0))
        self.dx = 0
        # Так как враг будет перемещаться к игроку + для колизии
        if random.random() != 0:
            self.dx = 2
        else:
            self.dx = -2

    def enemy_collide(self, dx, pf, stop_list):
        for p in pf:
            if sprite.collide_rect(self, p):  # Проверяем на пересечение противника с платформой
                if dx > 0:  # Если противник движется вправо, то запрещаем
                    self.rect.right = p.rect.left
                    self.dx = -2
                if dx < 0:  # Если противник движется в лево, то запрещаем
                    self.rect.left = p.rect.right
                    self.dx = 2

        for s in stop_list:
            if sprite.collide_rect(self, s):
                if dx > 0:  # Если противник движется вправо, то запрещаем
                    self.rect.right = s.rect.left
                    self.dx = -2
                if dx < 0:  # Если противник движется в лево, то запрещаем
                    self.rect.left = s.rect.right
                    self.dx = 2

    def moving(self, pf, stop_list):  # Функция с перемещением противника
        self.rect.x += self.dx
        self.enemy_collide(self.dx, pf, stop_list)

    def update(self):
        self.moving(platform.platforms, platform.stoppers)
