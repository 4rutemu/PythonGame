import pygame
from pygame import sprite
from random import randint

WIDTH = 800
HEIGHT = 600
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30
PLATFORM_COLOUR = WHITE

platforms = []  # Массив платформ
enemys = []
FIRST_LVL = [
    "                            ",
    "                            ",
    "                            ",
    "                            ",
    "             --             ",
    "          e                  ",
    "  e                         ",
    "-----   -----               ",
    "                    ---     ",
    "                            ",
    "----   --------            ",
    "                            ",
    "                            ",
    "---------------             ",
    "                            ",
    "                    e ------",
    "    e           ------------",
    "                            ",
    "                            ",
    "----------------------------"]


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.width = width
        self.height = height


# В будущем будет отдельный файл для уровней

def draw_lvl(LVL):

    for y, row in enumerate(LVL):  # вся строка
        for x, col in enumerate(row):  # каждый символ
			
            if col == ' ': #поскольку пустота самая частая лучше сразу её отбросить и не гонять лишний раз кучу условий
                continue
            
            elif col == "-":
                createdObject = Platforms(x*PLATFORM_WIDTH, y*PLATFORM_HEIGHT)
                platforms.append(createdObject)

            elif col == "e":
                createdObject = Enemy(x*PLATFORM_WIDTH, y*PLATFORM_HEIGHT)
                enemys.append(createdObject)
                
            all_sprites.add(createdObject)

            

class Platforms(GameObject): #как видно класс не имеет смысла и на данном этапе имеет смысл сразу создавать GameObject без посредников 
    def __init__(self, x, y): #но возможно в будущем это будет иметь смысл так что пока оставим
        super().__init__(x = x, y = y, width = PLATFORM_WIDTH, height = PLATFORM_HEIGHT, color = WHITE)



# Надо бы перенести в отдельный файл Игрока и Game_Object
GRAVITY = 0.35
J_POWER = 10
MOVE_SPEED = 7
ATTACK_TIME = 200
ATTACK_WIDTH = 10
ATTACK_HEIGHT = 30


class AttackSprite(GameObject):
    def __init__(self, owner):
        
        self.owner = owner

            
        super().__init__(x = -50, y = 0, width = ATTACK_WIDTH, height = ATTACK_HEIGHT, color = RED)
        self.creation_time = pygame.time.get_ticks()


    def update(self):
        
        if (pygame.time.get_ticks() - self.creation_time) > ATTACK_TIME:
            player.is_attacking = False
            self.kill()
            if self.owner != 'player':
                enemys[self.owner].attacked = False
            return
        
        if self.owner == 'player': 
			
            self.rect.y = player.rect.y
            if player.dx>0:
                self.rect.x = player.rect.x + player.width
            else:
                self.rect.x = player.rect.x - ATTACK_WIDTH
                
                
            for enemy in enemys:
                if sprite.collide_rect(enemy, self):
                    enemy.hp -= 1

        else: 

            if player.rect.x >= enemys[self.owner].rect.x:	        
                self.rect.x = enemys[self.owner].rect.x + enemys[self.owner].rect.width
            elif player.rect.x <= enemys[self.owner].rect.x:	        
                self.rect.x = enemys[self.owner].rect.x - ATTACK_WIDTH
            self.rect.y = enemys[self.owner].rect.y
               
            if sprite.collide_rect(player, self):
                player.hp -= 1
				
class Player(GameObject):
    def __init__(self):
        super().__init__(x = WIDTH / 2 + 15, y = HEIGHT / 2 + 15, width = 30, height = 30, color = GREEN)
        
        self.dy, self.dx = 0, 0
        self.onGround = True
        self.enemyKilled = 0
        self.is_attacking = False
        self.hp = 100
    def get_input(self, platforms, enemys):
        keys = pygame.key.get_pressed()

        self.dx = (keys[pygame.K_d] - keys[pygame.K_a]) * MOVE_SPEED
        
        if self.onGround:
            self.dy = -J_POWER * keys[pygame.K_w]
        else:
            self.dy += GRAVITY

        if keys[pygame.K_SPACE] and not self.is_attacking:
            attack = AttackSprite(owner='player')
            all_sprites.add(attack)
            self.is_attacking = True

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.dy
        self.collide(0, self.dy, platforms, enemys)

        self.rect.x += self.dx
        self.collide(self.dx, 0, platforms, enemys)

    def collide(self,dx, dy, platforms, enemys):
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

        for e in enemys: # Коллизия с противником
            if sprite.collide_rect(self, e):
                if dx > 0:
                    self.rect.right = e.rect.left
                if dx < 0:
                    self.rect.left = e.rect.right
                if dy > 0:
                    self.rect.bottom = e.rect.top
                    self.onGround = True
                    self.yvel = 0

    def update(self):
        self.get_input(platforms, enemys)
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH    
        if player.hp == 0:
            print('death')
            player.hp = -1 
            player.kill()



#TODO: Сделать врагам физику, коллизии, получение урона от атак
class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x = x, y = y, width = 30, height = 30, color = YELLOW)
        self.onGround = False

        #Так как враг будет перемещаться к игроку + для колизии
        self.xvel = 0
        self.yvel = 0
        self.id = len(enemys)
        self.hp = 10
        self.attacked = False# не атакует
    def enemy_collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # Проверяем на пересечение противника с платформой

                if xvel > 0:  # Если противник движется вправо, то запрещаем
                    self.rect.right = p.rect.left

                if xvel < 0:  # Если противник движется в лево, то запрещаем
                    self.rect.left = p.rect.right

                if yvel > 0:  # Если противник падает вниз под гравитацией,
                    self.rect.bottom = p.rect.top  # то не падает вниз, как только сопрекасается с верхушкой платформы
                    self.onGround = True  # и становится на ноги твёрдо
                    self.yvel = 0  # Убираем энергию падения

                if yvel < 0:  # Если противник движется вверх, то запрещаем ему двигаться туда
                    self.rect.top = p.rect.bottom
                    self.yvel = 0  # Убираем энергию прыжка

    def moving(self, platfroms): # Функция с перемещением противника
        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        
        self.rect.y += self.yvel
        self.enemy_collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.enemy_collide(self.xvel, 0, platforms)
    def update(self):
        self.moving(platforms)
        
        if self.hp <= 0:
            self.rect.x = -50
            self.kill()
            
        if self.rect.y == player.rect.y and ((abs(self.rect.x - player.rect.x+player.rect.width) < ATTACK_WIDTH) or (abs(self.rect.x - player.rect.x-player.rect.width) < ATTACK_WIDTH)) :
            if not self.attacked and randint(1,5) == 3: #немного глупости что бы не был непобедимым
                
                attack = AttackSprite(self.id)
                all_sprites.add(attack)
                self.attacked = True
        else:
            self.attacked = False
            


# Создаем игру и окно
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("platformer")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()

draw_lvl(FIRST_LVL)
all_sprites.add(player)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    pygame.display.set_caption('FPS: ' + str(round(clock.get_fps())) + 
                     '          PLAYER_HP: ' + str(player.hp))
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Обновление
    all_sprites.update()

    # Отрисовка
    screen.fill(BLACK)

    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
