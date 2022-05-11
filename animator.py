import pygame


def animation(sprite, animation_list, length):
    if animation_list[0] >= length:
        animation_list[0] = 1
    sprite.image = animation_list[animation_list[0]]
    animation_list[0] += 1
