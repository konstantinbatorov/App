# Тестовое пространство

from pygame import *

#
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = width  
        self.height = height
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#
class Player(GameSprite):
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < (window_height - self.height):
            self.rect.y += self.speed
    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < (window_height - self.height):
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height, speed_x, speed_y):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self, racket1, racket2):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y >= window_height - self.height or self.rect.y <= 0:
            self.speed_y *= -1
        if sprite.collide_rect(racket1, self) or sprite.collide_rect(racket2, self):
            ball.speed_x *= - 1
        

#Constants
racket_image = 'racket.png'
ball_image = 'ball.png'
window_width = 700
window_height = 500
window_color = (255, 255, 255)
clock = time.Clock()
FPS = 60
RED = (128, 0, 0)

#Window
window = display.set_mode((window_width, window_height))
window.fill(window_color)

font.init()
font1 = font.SysFont('Arial', 35)
lose1 = font1.render('The left racket has lost!', True, RED)
lose2 = font1.render('The right racket has lost!', True, RED)
#Markers
game = True
finish = False

#Sprites

left_racket = Player(racket_image, 20, 150, 5, 25, 150)
right_racket = Player(racket_image, 655, 150, 5, 25, 150)
ball = Ball(ball_image, 200, 200, 4, 50, 50, 3, 3)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.fill(window_color)
        left_racket.update_left()
        right_racket.update_right()
        ball.update(left_racket, right_racket)
        left_racket.reset()
        right_racket.reset()
        ball.reset()
        if ball.rect.x <= 0:
            finish = True
            window.blit(lose1, (200, 200))
        if ball.rect.x >= window_width - ball.width:
            finish = True
            window.blit(lose2, (200, 200))
    display.update()
    clock.tick(FPS)
            