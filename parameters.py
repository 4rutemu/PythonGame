import pygame

pygame.mixer.init()
player_attack_sound = pygame.mixer.Sound("Sounds/player_attack_sound.wav")
# death_sound = pygame.mixer.Sound("Sounds/death_sound.wav")
npc_damage = pygame.mixer.Sound("Sounds/get_damage_npc.wav")
select_sound = pygame.mixer.Sound("Sounds/select_sound.wav")
game_over_sound = pygame.mixer.Sound("Sounds/game_over.wav")

title = pygame.mixer.Sound("music/title.wav")
moon_forest = pygame.mixer.Sound("music/moon-forest.wav")

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

based_hp = 30
based_move_speed = 4
GRAVITY = 0.35
based_j_power = 10
ATTACK_TIME = 300
ATTACK_WIDTH = 10
ATTACK_HEIGHT = 30
based_attack_power = 1

default_lvl = 1
level_status = False

all_sprites = pygame.sprite.Group()

