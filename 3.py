from pygame import *
from random import randint

class Object(sprite.Sprite):
    def __init__(self, player_image: str, player_x: float, player_y: float, player_speed: float):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (64, 64))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Object):
    def move(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 0:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < WIDTH - 64:
            self.rect.x += self.speed

class Enemy(Object):
    def update(self, barrier_x, barrier_y, enemy_speed):
        # if barrier_x - 64 <= self.rect.x <= barrier_x+64:
        #     if self.rect.x <= WIDTH / 2:
        #         self.speed = enemy_speed
        #     if self.rect.x > WIDTH / 2:
        #         self.speed = -enemy_speed

            #self.speed = enemy_speed
        # if barrier_x <= self.rect.x <= barrier_x + 32:
        #     self.speed = -enemy_speed
        # elif barrier_x + 32 < self.rect.x <= barrier_x + 64:
        #     self.speed = enemy_speed

        # if self.rect.x <= barrier_x <= self.rect.x + 32:
        #     self.speed = -enemy_speed
        # elif self.rect.x + 32 < barrier_x <= self.rect.x + 64:
        #     self.speed = enemy_speed
        # elif barrier_x <= self.rect.x <= barrier_x + 32:
        #     self.speed = -enemy_speed
        # elif barrier_x + 32 < self.rect.x <= barrier_x + 64:
        #     self.speed = enemy_speed
        crash = randint(1, 10)
        if crash != 10:
            t1 = 16 + self.rect.x
            t2 = 48+ self.rect.x
            a1 = barrier_x <= self.rect.x <= barrier_x + 64
            a2 = barrier_x <= t1 <= barrier_x + 64
            a3 = barrier_x <= t2 <= barrier_x + 64
            a4 = barrier_x <= self.rect.x + 64 <= barrier_x + 64
            if a1 and a2 and a3 and a4:
                self.speed = enemy_speed
            elif (a1 and a2) or a1:
                self.speed = enemy_speed
            elif (a3 and a4) or a4:
                self.speed = -enemy_speed
        


        else:
            self.speed = 0
    def move(self):
        self.rect.x += self.speed

class Barrier(Object):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH - 64) # Случайная X позиция
            self.rect.y = -32 # За пределами экрана
        self.reset()
#Константы
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HEIGHT = 512
WIDTH = 512

game = True
finish = False

window = display.set_mode((WIDTH, HEIGHT))
window.fill(WHITE)
background = transform.scale(image.load("road.png"), (WIDTH, HEIGHT))
clock = time.Clock()



player = Player('car.png', 0, 448, 5)
enemy = Enemy('car.png', 256, 448, 5)
barrier_list = list()
num_barrier = 1  # Количество метеоритов
for i in range(num_barrier):
    x = randint(0, WIDTH - 32) # Рандом по X
    # x = 256
    y = randint(-100, -50) # Начальная позиция над экраном
    barrier = Barrier("car.png", x, y, 30) # Скорость 2
    barrier_list.append(barrier)


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish:
        window.blit(background, (0, 0))
        player.reset()

        enemy.reset()
        player.move()
        for barrier in barrier_list:
            barrier.update()
            enemy.update(barrier.rect.x, barrier.rect.y, 5)
        enemy.move()
        display.update()
        clock.tick(FPS)