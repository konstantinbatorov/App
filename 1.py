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

# Создание класса Object с возможностью задавать размер
class Object(sprite.Sprite):
    def __init__(self, image_path, x, y, speed, size=(64, 64)):
        super().__init__()
        # Масштабируем изображение по заданным размерам
        self.image = transform.scale(image.load(image_path), size)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс Player с размером 32x64
class Player(Object):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed, size=(32, 70))
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 20:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIDTH - self.rect.width - 20:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

# Класс Barrier (заменяет Meteor), размер 64x64
class Barrier(Object):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed, size=(64, 64))
        self.speed_y = speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH - 64)
            self.rect.y = randint(-200, -50)

# Создаем игрока
player = Player("car.png", WIDTH // 2, 448, 3)

# Функция для создания барьеров (ранее метеоров), избегая перекрытия
def create_barriers(num_bars):
    barriers = []
    for _ in range(num_bars):
        while True:
            x = randint(0, WIDTH - 64)
            y = randint(-200, -50)
            new_barrier = Barrier("pocr.png", x, y, 2)
            # Проверка перекрытия
            overlap = False
            for b in barriers:
                if b.rect.colliderect(new_barrier.rect):
                    overlap = True
                    break
            if not overlap:
                barriers.append(new_barrier)
                break
    return barriers

# Создаем барьеры
barrier_list = create_barriers(5)

clock = time.Clock()

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))
    player.reset()
    player.move()

    # Обновление и отрисовка барьеров
    for barrier in barrier_list:
        barrier.update()
        barrier.reset()

    # Проверка столкновений между барьерами
    for i in range(len(barrier_list)):
        for j in range(i + 1, len(barrier_list)):
            if barrier_list[i] is not None and barrier_list[j] is not None:
                if sprite.collide_rect(barrier_list[i], barrier_list[j]):
                    # Удаляем столкнувшиеся барьеры
                    barrier_list[i] = None
                    barrier_list[j] = None

    # Удаляем None из списка
    barrier_list = [b for b in barrier_list if b is not None]

    # Если осталось менее 5 барьеров, создаем новых
    while len(barrier_list) < 5:
        new_barrier = Barrier("pocr.png", randint(0, WIDTH - 64), randint(-200, -50), 2)
        # Проверка перекрытия с существующими
        overlap = False
        for b in barrier_list:
            if b.rect.colliderect(new_barrier.rect):
                overlap = True
                break
        if not overlap:
            barrier_list.append(new_barrier)

    display.update()
    clock.tick(FPS)

pygame.quit()
