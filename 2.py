from pygame import *
from random import *

class Object(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, x, y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (64, 64))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Object):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIDTH - 64:
            self.rect.x += self.speed

class Barrier(Object):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH - 64) # Случайная X позиция
            self.rect.y = -32 # За пределами экрана
        self.reset()

player = Player("car.png", 0, 448, 10)
WIDTH = 512
HEIGHT= 512
FPS = 60
clock = time.Clock()
window = display.set_mode((WIDTH, HEIGHT))
background = transform.scale(image.load("road.png"), (WIDTH, HEIGHT))
game = True

barrier_list = list()
num_barrier = 2  # Количество метеоритов
for i in range(num_barrier):
    x = randint(0, WIDTH - 32) # Рандом по X
    y = randint(-100, -50) # Начальная позиция над экраном
    barrier = Barrier("car.png", x, y, 2) # Скорость 2
    barrier_list.append(barrier)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))
    player.reset()
    player.move()

    for barrier in barrier_list:
        barrier.update()

    display.update()
    clock.tick(FPS)