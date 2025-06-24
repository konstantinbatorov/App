from pygame import *

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