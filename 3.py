from pygame import *

class Object(sprite.Sprite):
    def __init__(self, player_image: str, player_x: float, player_y: float, player_speed: float):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
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
    def move(self, barrier_x, barrier_y, enemy_speed):
        if barrier_x <= self.x <= barrier_x+64:
            if self.x <= WIDTH / 2:
                self.speed = enemy_speed
            if self.x > WIDTH / 2:
                self.speed = -enemy_speed
        else:
            self.speed = 0
    
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


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.move()
        if sprite.collide_rect()
        display.update()
        clock.tick(FPS)