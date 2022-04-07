import sys

import pygame

import button
import platform
import enemy
import parameters
import player as hero
import cam

first_lvl = [
    "--------------------------------------------",
    "-                                          -",
    "-                                          -",
    "-                          ----   e  x     -",
    "-             --              -------      -",
    "-                                          -",
    "-x   e x x  e  x                           -",
    "- -----   -----                            -",
    "-                    ---                   -",
    "-                                          -",
    "-----   --------                    ---    -",
    "-                                          -",
    "-                             ---          -",
    "----------------                           -",
    "-                                  x      e-",
    "-               x    e -------      --------",
    "-                -------------      --------",
    "-                             ---          -",
    "-x      e                     x           x-",
    "--------------------------------------------"]


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


def game(player):
    running = True
    while running:
        pygame.display.set_caption("Time_Killer")
        clock.tick(parameters.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(player)

        # Обновление
        parameters.all_sprites.update()

        # Отрисовка
        screen.fill(parameters.BLACK)

        camera.update(player)  # центризируем камеру относительно персонажа
        for s in parameters.all_sprites:
            screen.blit(s.image, camera.apply(s))
        pygame.display.flip()


def pause(player):
    paused = True
    while paused:
        pygame.display.set_caption("Paused")
        screen.fill(parameters.BLACK)
        screen.blit(pause_name, (350, 300))

        if pause_btn.draw(screen):
            paused = False
        elif exit_btn.draw(screen):
            parameters.reload = True
            paused = False
            for s in parameters.all_sprites:
                s.kill()
            for e in enemy.enemies:
                e.kill()
            player.kill()
            main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.flip()


def main_menu():

    running = True
    while running:
        pygame.display.set_caption("Main Menu")
        screen.fill(parameters.BLACK)
        screen.blit(name, (290, 300))
        if start_btn.draw(screen):
            running = False
            draw_lvl(first_lvl)
            player = hero.Player()
            parameters.all_sprites.add(player)
            game(player)
        elif exit_btn.draw(screen):
            running = False
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.flip()


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + parameters.WIDTH / 2, -t + parameters.HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - parameters.WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - parameters.HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


# Создаем игру и окно
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((parameters.WIDTH, parameters.HEIGHT))
clock = pygame.time.Clock()

total_level_width = len(first_lvl[0]) * platform.PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
total_level_height = len(first_lvl) * platform.PLATFORM_HEIGHT  # высоту

camera = cam.Camera(camera_configure, total_level_width, total_level_height)

start_img = pygame.image.load("m_Start-Button.png").convert_alpha()
start_btn = button.Button(x=200, y=400, image=start_img)

exit_img = pygame.image.load("m_Exit-Button.png").convert_alpha()
exit_btn = button.Button(x=420, y=410, image=exit_img)

pause_img = pygame.image.load("m_Pause-Button.png").convert_alpha()
pause_btn = button.Button(x=200, y=410, image=pause_img)

font = pygame.font.SysFont('serif', 48)
name = font.render("Time_Killer", True, parameters.RED)
pause_name = font.render("Pause", True, parameters.RED)

main_menu()
