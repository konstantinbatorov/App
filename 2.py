from pygame import *

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

player = Player("car.png", 0, 448, 10)
WIDTH = 512
HEIGHT= 512
FPS = 60
clock = time.Clock()
window = display.set_mode((WIDTH, HEIGHT))
background = transform.scale(image.load("road.png"), (WIDTH, HEIGHT))
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))
    player.reset()
    player.move()

    display.update()
    clock.tick(FPS)