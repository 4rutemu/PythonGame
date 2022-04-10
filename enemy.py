import random

from pygame import sprite

import game_object
import parameters
import platform

enemies = []
speed_list = [-7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7]


# TODO: получение урона от атак
class Enemy(game_object.GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 30, (255, 255, 0))
        self.dx = speed_list[random.randint(0, 13)]
        # Так как враг будет перемещаться к игроку + для колизии

        self.hp = 10

    def enemy_collide(self, dx, pf, stop_list):
        for p in pf:
            if sprite.collide_rect(self, p):  # Проверяем на пересечение противника с платформой
                if dx > 0:  # Если противник движется вправо, то запрещаем
                    self.rect.right = p.rect.left
                    self.dx *= -1
                if dx < 0:  # Если противник движется в лево, то запрещаем
                    self.rect.left = p.rect.right
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
        self.enemy_collide(self.dx, pf, stop_list)

    def update(self):
        self.moving(platform.platforms, platform.stoppers)

        if self.hp <= 0:
            parameters.death_sound.play()
            self.rect.x = -600000
            self.kill()
