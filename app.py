from pygame import *

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


#Константы
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HEIGHT = 512
WIDTH = 512

game = True

window = display.set_mode((WIDTH, HEIGHT))
window.fill(WHITE)
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(FPS)