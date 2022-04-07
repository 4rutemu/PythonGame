import sys

import pygame

import button
import platform
import enemy
import parameters
import player

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


def draw_lvl(lvl):
    x = y = 0
    for row in lvl:
        for col in row:
            if col == "":  # Пропускаем пустые символы, чтобы не тратить лишнее время
                continue
            elif col == "-":
                pf = platform.Platform(x, y)
                parameters.all_sprites.add(pf)
                platform.platforms.append(pf)
            elif col == "x":
                stop = platform.Platform(x, y)
                platform.stoppers.append(stop)

            elif col == "e":
                enemyForList = enemy.Enemy(x, y)
                parameters.all_sprites.add(enemyForList)
                enemy.enemies.append(enemyForList)

            x += platform.PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += platform.PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля


def game():
    running = True
    while running:
        pygame.display.set_caption("Time_Killer")
        clock.tick(parameters.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Обновление
        parameters.all_sprites.update()

        # Отрисовка
        screen.fill(parameters.BLACK)
        parameters.all_sprites.draw(screen)
        pygame.display.flip()


def main_menu():
    running = True
    while running:
        pygame.display.set_caption("Main Menu")
        screen.fill(parameters.BLACK)
        screen.blit(name, (290, 300))

        if start_btn.draw(screen):
            game()
        elif exit_btn.draw(screen):
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


# Создаем игру и окно
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((parameters.WIDTH, parameters.HEIGHT))
clock = pygame.time.Clock()

player = player.Player()

draw_lvl(first_lvl)
parameters.all_sprites.add(player)

start_img = pygame.image.load("m_Start-Button.png").convert_alpha()
start_btn = button.Button(x=200, y=400, image=start_img)

exit_img = pygame.image.load("m_Exit-Button.png").convert_alpha()
exit_btn = button.Button(x=420, y=410, image=exit_img)

font = pygame.font.SysFont('serif', 48)
name = font.render("Time_Killer", True, parameters.RED)

main_menu()
