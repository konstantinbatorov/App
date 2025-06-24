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
    pass #тут код препятствия

class Meteor(Object):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed)
        self.image = transform.scale(image.load(image_path), (32, 32)) # Например, уменьшим метеориты
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = speed # Скорость падения по Y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH - self.rect.width) # Случайная X позиция
            self.rect.y = -32 # За пределами экрана
        self.reset()


player = Player("car.png", 0, 448, 10)
WIDTH = 512
HEIGHT= 512
FPS = 60
clock = time.Clock()
window = display.set_mode((WIDTH, HEIGHT))
background = transform.scale(image.load("road.png"), (WIDTH, HEIGHT))

# Инициализация метеора
meteor_list = []
num_meteors = 5  # Количество метеоритов
for i in range(num_meteors):
    x = randint(0, WIDTH - 32) # Рандом по X
    y = randint(-100, -50) # Начальная позиция над экраном
    meteor = Meteor("car.png", x, y, 2) # Скорость 2
    meteor_list.append(meteor)

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))
    player.reset()
    player.move()

    # Обновление и отрисовка метеоров
    for meteor in meteor_list:
        meteor.update()

    display.update()
    clock.tick(FPS)
