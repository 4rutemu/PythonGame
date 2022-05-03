import sys

import pygame

import button
import platform
import enemy
import parameters
import player
import player as hero
import cam

first_lvl = [
    "++++++++++++++++++++++++++++++++++++++++++++",
    "+                                          +",
    "+                                          +",
    "+                         ----   e  x      +",
    "+             --              -------      +",
    "+                                          +",
    "+x   e x x  e  x                           +",
    "+ -----   -----                            +",
    "+                    ---                   +",
    "+                                          +",
    "+----   --------                    ---    +",
    "+                                          +",
    "+                             ---          +",
    "+---------------                           +",
    "+                                  x      e+",
    "+               x    e -------      -------+",
    "+                ------+++++++      ++++++++",
    "+                             ---          +",
    "+x      e                     x            +",
    "+-------------------------------------------"]
second_lvl = [
    "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",
    "+                                                                          +",
    "+                                                                          +",
    "+                                                                          +",
    "+       -                                             xe       xxe   x     +",
    "+      -+         -                                    --------  ----      +",
    "+     -++ e      -                x e     x                                +",
    "+       +--------+                 -------                                 +",
    "+                                                                          +",
    "+                                                    x     e       x       +",
    "+                     ---                             -------------        +",
    "+                                                     +           +---     +",
    "+                                                     +      x   e+    x  e+",
    "+                                    ------           +       ----+     ---+",
    "+        --------                         +----                   +        +",
    "+        +       -                  xe           x   x   e   e    +---     +",
    "+e       +                           ------------     ------------+        +",
    "+--------+------                  ---           +     +                    +",
    "+                              ---+             +     +               ---  +",
    "+e                  x       ---+                +     +                    +",
    "+-------------------  ------+                                              +",
    "+                                                               -----      +",
    "+                                    ------                                +",
    "+                                                                          +",
    "+                x    e   -----                - e      -                  +",
    "+     e            -------e                     --------                   +",
    "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"]


def draw_lvl(lvl, player):
    x = y = 0
    for row in lvl:
        for col in row:
            if col == "":  # Пропускаем пустые символы, чтобы не тратить лишнее время
                continue
            elif col == "-":
                pf = platform.Platform(x=x, y=y)
                parameters.all_sprites.add(pf)
                platform.platforms.append(pf)
            elif col == "x":
                stop = platform.Platform(x=x, y=y)
                platform.stoppers.append(stop)

            elif col == "+":
                pf = platform.Platform(x=x, y=y)
                pf.image = pygame.image.load('Platforms images/edges.png').convert_alpha()
                parameters.all_sprites.add(pf)
                platform.platforms.append(pf)

            elif col == "e":
                enemyForList = enemy.Enemy(x=x, y=y, player=player)
                parameters.all_sprites.add(enemyForList)
                enemy.enemies.append(enemyForList)

            x += platform.PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += platform.PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля


def game():
    running = True
    player = hero.Player()
    if parameters.default_lvl == 1:
        parameters.moon_forest.play(100)
        draw_lvl(lvl=first_lvl, player=player)
        total_level_width = len(first_lvl[0]) * platform.PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
        total_level_height = len(first_lvl) * platform.PLATFORM_HEIGHT  # высоту
        camera = cam.Camera(camera_configure, total_level_width, total_level_height)
    else:
        draw_lvl(lvl=second_lvl, player=player)
        total_level_width = len(second_lvl[0]) * platform.PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
        total_level_height = len(second_lvl) * platform.PLATFORM_HEIGHT  # высоту
        camera = cam.Camera(camera_configure, total_level_width, total_level_height)
        parameters.level_status = True
    parameters.all_sprites.add(player)
    while running:
        pygame.display.set_caption("Time_Killer " + "Killed: " + str(player.kill_score) + " HP: " + str(player.hp))
        clock.tick(parameters.FPS)
        if player.kill_score == len(enemy.enemies):
            if parameters.level_status:
                parameters.game_over_sound.play()
                running = False
                parameters.default_lvl = 1
                parameters.level_status = False
                delliting()
                parameters.all_sprites.empty()
                main_menu()

            parameters.default_lvl = 2
            parameters.based_j_power += 1
            parameters.based_attack_power += 3
            parameters.based_hp += 10
            parameters.based_move_speed = player.move_speed
            delliting()
            parameters.all_sprites.empty()
            pygame.display.flip()
            running = False
            game()

        if player.hp <= 0:
            parameters.game_over_sound.play()
            running = False
            delliting()
            parameters.all_sprites.empty()
            main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_c:
                    characteristics(speed=player.move_speed, hp=player.hp,
                                    jump_power=player.j_power, damage=player.attack_power)

        # Обновление
        parameters.all_sprites.update()

        # Отрисовка
        if parameters.default_lvl == 1:
            screen.blit(background, (0, 0))
        elif parameters.default_lvl == 2:
            screen.blit(second_background, (0, 0))

        camera.update(player)  # центрируем камеру относительно персонажа
        for s in parameters.all_sprites:
            screen.blit(s.image, camera.apply(s))
        pygame.display.flip()


def delliting():  # Функция для удаления
    for s in parameters.all_sprites:
        s.rect.x = -600000
        s.kill()
    platform.platforms.clear()
    platform.stoppers.clear()
    enemy.enemies.clear()


def pause():
    paused = True
    while paused:
        pygame.display.set_caption("Paused")
        screen.blit(main_background, (0, 0))
        screen.blit(pause_name, (350, 150))
        screen.blit(restart_name, (350, 100))

        if pause_btn.draw(screen):
            parameters.select_sound.play()
            paused = False
        elif exit_btn.draw(screen):
            parameters.moon_forest.stop()
            parameters.select_sound.play()
            paused = False
            delliting()
            parameters.all_sprites.empty()
            main_menu()
        elif pygame.key.get_pressed()[pygame.K_r]:
            paused = False
            parameters.moon_forest.stop()
            delliting()
            parameters.all_sprites.empty()
            game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.flip()


def characteristics(speed, hp, jump_power, damage):
    running = True
    speed_stat = font1.render("Current Speed: " + str(speed), True, parameters.WHITE)
    hp_stat = font1.render("Current HP: " + str(hp), True, parameters.WHITE)
    damage_stat = font1.render("Current Damage: " + str(damage), True, parameters.WHITE)
    jump_stat = font1.render("Current Jump: " + str(jump_power), True, parameters.WHITE)
    exit_name = font1.render("C for exit", True, parameters.RED)
    while running:
        pygame.display.set_caption("Characteristics")
        screen.blit(main_background, (0, 0))
        screen.blit(exit_name, (350, 10))
        screen.blit(hp_stat, (330, 200))
        screen.blit(speed_stat, (330, 240))
        screen.blit(damage_stat, (330, 280))
        screen.blit(jump_stat, (330, 320))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    running = False

        pygame.display.flip()


def select():
    running = True
    while running:
        pygame.display.set_caption("Select Level")
        screen.blit(main_background, (0, 0))
        if start_btn.draw(screen):
            parameters.select_sound.play()
            parameters.default_lvl = 1
            running = False
            game()
            parameters.all_sprites.empty()
        elif exit_btn.draw(screen):
            parameters.select_sound.play()
            parameters.default_lvl = 2
            running = False
            game()
            parameters.all_sprites.empty()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.flip()


def main_menu():
    running = True
    parameters.title.play(loops=100)
    while running:

        pygame.display.set_caption("Main Menu")
        screen.blit(main_background, (0, 0))
        screen.blit(name, (290, 200))
        if start_btn.draw(screen):
            parameters.title.stop()
            parameters.select_sound.play()
            running = False
            game()
            parameters.all_sprites.empty()
        elif exit_btn.draw(screen):
            parameters.title.stop()
            parameters.select_sound.play()
            running = False
            pygame.quit()
            quit()
        elif first_btn.draw(screen):
            parameters.title.stop()
            parameters.select_sound.play()
            running = False
            select()

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

background = pygame.image.load('Backgrounds/background.png').convert_alpha()
background = pygame.transform.scale(background, (parameters.WIDTH, parameters.HEIGHT))

main_background = pygame.image.load('Backgrounds/main_background.png').convert_alpha()
main_background = pygame.transform.scale(main_background, (parameters.WIDTH, parameters.HEIGHT))

second_background = pygame.image.load('Backgrounds/second_background.png').convert_alpha()
second_background = pygame.transform.scale(second_background, (parameters.WIDTH, parameters.HEIGHT))

start_img = pygame.image.load("Buttons_Pictures/m_Start-Button.png").convert_alpha()
start_btn = button.Button(x=300, y=250, image=start_img)

exit_img = pygame.image.load("Buttons_Pictures/m_Exit-Button.png").convert_alpha()
exit_btn = button.Button(x=328, y=350, image=exit_img)

pause_img = pygame.image.load("Buttons_Pictures/m_Pause-Button.png").convert_alpha()
pause_btn = button.Button(x=300, y=250, image=pause_img)

first_img = pygame.image.load("Buttons_Pictures/frist.png").convert_alpha()
first_btn = button.Button(x=300, y=450, image=first_img)

font = pygame.font.SysFont('serif', 48)
font1 = pygame.font.SysFont('serif', 24)
name = font.render("Time_Killer", True, parameters.RED)
pause_name = font.render("Pause", True, parameters.RED)
restart_name = font1.render("R for restart", True, parameters.RED)

main_menu()
