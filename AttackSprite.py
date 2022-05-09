import random

import pygame
from pygame import sprite

import game_object
import parameters
import enemy as e


class AttackSprite(game_object.GameObject):
    def __init__(self, owner, player):

        self.owner = owner
        self.player = player
        super().__init__(x=-50, y=0, width=parameters.ATTACK_WIDTH, height=parameters.ATTACK_HEIGHT,
                         colour=parameters.RED)
        self.creation_time = pygame.time.get_ticks()


    def update(self):

        if (pygame.time.get_ticks() - self.creation_time) > parameters.ATTACK_TIME:
            self.player.is_attacking = False
            self.kill()
            if self.owner != 'player':
                e.enemies[self.owner].attacked = False
            return

        if self.owner == 'player':
            if self.player.looking_right:
                self.rect.left = self.player.rect.right
                self.rect.top = self.player.rect.top
                self.image = parameters.right_attack_image
            else:
                self.rect.right = self.player.rect.left
                self.rect.top = self.player.rect.top
                self.image = parameters.left_attack_image
            if self.player.is_attacking:
                for enemy in e.enemies:
                    if sprite.collide_rect(enemy, self):
                        enemy.hp -= self.player.attack_power
                        self.player.is_attacking = False

        else:
            if self.player.rect.x >= e.enemies[self.owner].rect.x:
                self.rect.x = e.enemies[self.owner].rect.x + e.enemies[self.owner].rect.width
            elif self.player.rect.x <= e.enemies[self.owner].rect.x:
                self.rect.x = e.enemies[self.owner].rect.x - parameters.ATTACK_WIDTH
            self.rect.y = e.enemies[self.owner].rect.y

            if e.enemies[self.owner].is_attacking:
                if sprite.collide_rect(self.player, self):
                    self.player.hp -= random.randint(0, 3)
                    e.enemies[self.owner].is_attacking = False
