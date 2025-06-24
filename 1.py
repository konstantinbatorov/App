import pygame
from pygame import *
from random import *

# Инициализация pygame
pygame.init()

# Размеры окна
WIDTH = 512
HEIGHT = 512
FPS = 60

# Создание окна
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Meteor Game")

# Загрузка фонового изображения
background = transform.scale(image.load("road.png"), (WIDTH, HEIGHT))

# Создание класса Object
class Object(sprite.Sprite):
    def __init__(self, player_image, x, y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (64, 64))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс Player
class Player(Object):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIDTH - 64:
            self.rect.x += self.speed

# Класс Barrier (препятствие), пока что пустой, можно расширить
class Barrier(Object):
    pass

# Класс Meteor
class Meteor(Object):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed)
        self.speed_y = speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH - 64)
            self.rect.y = randint(-200, -50)

# Создаем игрока
player = Player("car.png", WIDTH // 2, 448, 5)

# Функция для создания метеоров, избегая перекрытия
def create_meteors(num_meteors):
    meteors = []
    for _ in range(num_meteors):
        while True:
            x = randint(0, WIDTH - 64)
            y = randint(-200, -50)
            new_meteor = Meteor("pocr.png", x, y, 2)
            # Проверка перекрытия
            overlap = False
            for m in meteors:
                if m.rect.colliderect(new_meteor.rect):
                    overlap = True
                    break
            if not overlap:
                meteors.append(new_meteor)
                break
    return meteors

# Создаем метеоры
meteor_list = create_meteors(5)

clock = time.Clock()

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
        meteor.reset()

    # Проверка столкновений между метеорами
    for i in range(len(meteor_list)):
        for j in range(i + 1, len(meteor_list)):
            # Проверка, что оба метеора существуют
            if meteor_list[i] is not None and meteor_list[j] is not None:
                if sprite.collide_rect(meteor_list[i], meteor_list[j]):
                    # Удаляем столкнувшиеся метеоры
                    meteor_list[i] = None
                    meteor_list[j] = None

    # Удаляем None из списка
    meteor_list = [m for m in meteor_list if m is not None]

    # Если осталось менее 5 метеоров, создаем новых
    while len(meteor_list) < 5:
        new_meteor = Meteor("pocr.png", randint(0, WIDTH - 64), randint(-200, -50), 2)
        # Проверка перекрытия с существующими
        overlap = False
        for m in meteor_list:
            if m.rect.colliderect(new_meteor.rect):
                overlap = True
                break
        if not overlap:
            meteor_list.append(new_meteor)

    display.update()
    clock.tick(FPS)

pygame.quit()
