from pygame import *
from random import *

class Object(sprite.Sprite):
    def __init__(self, image_path, x, y, speed, size=(64, 64)):
        super().__init__()
        self.image = transform.scale(image.load(image_path), size)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс Player с более приятными размерами
class Player(Object):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed, size=(40, 80))
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 104:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIDTH - self.rect.width - 104:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

# Класс Enemy (самолет)
class Enemy(Object):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed, size=(40, 80))
    def update(self, barrier_x, barrier_y, enemy_speed):
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

# Класс Barrier (покрышки)
class Barrier(Object):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed, size=(64, 64))
        self.speed_y = speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH - 64)
            self.rect.y = randint(-200, -50)



def create_barriers(num_bars):
    barriers = []
    for _ in range(num_bars):
        while True:
            x = randint(0, WIDTH - 64)
            y = randint(-200, -50)
            # Вероятность выбрать текстуру conus.png
            if random() < 0.3:  # 30% шанс
                image_path = "conus.png"
            else:
                image_path = "pocr.png"
            new_barrier = Barrier(image_path, x, y, 3)
            # Проверка перекрытия с существующими препятствиями
            overlap = False
            for b in barriers:
                if b.rect.colliderect(new_barrier.rect):
                    overlap = True
                    break
            # Проверка перекрытия с игроком
            if new_barrier.rect.colliderect(player.rect):
                overlap = True
            # Если нет пересечений, добавляем
            if not overlap:
                barriers.append(new_barrier)
                break
    return barriers



#Константы
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HEIGHT = 512
WIDTH = 512

game = True

window = display.set_mode((WIDTH, HEIGHT))
road_image = image.load("road.png")
background1 = transform.scale(road_image, (WIDTH, HEIGHT))
background2 = transform.scale(road_image, (WIDTH, HEIGHT))
bg1_y = 0
bg2_y = -HEIGHT
clock = time.Clock()


# Создаем игрока
player = Player("car.png", WIDTH // 2, 400, 3)

# Создаем бота
enemy = Enemy("Bot.png", WIDTH // 2 - 64, 400, 3)

barrier_list = create_barriers(3)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    # Обновляем позицию фона (движение дороги)
    bg1_y += 3
    bg2_y += 3
    if bg1_y >= HEIGHT:
        bg1_y = -HEIGHT
    if bg2_y >= HEIGHT:
        bg2_y = -HEIGHT

    # Отрисовка фона
    window.blit(background1, (0, bg1_y))
    window.blit(background2, (0, bg2_y))
    
    # Обработка игрока
    player.reset()
    player.move()
    
    enemy.reset()
    # Обновление и отрисовка препятствий
    for barrier in barrier_list:
        barrier.update()
        barrier.reset()

    # Проверка столкновений между препятствиями
    for i in range(len(barrier_list)):
        for j in range(i + 1, len(barrier_list)):
            if barrier_list[i] is not None and barrier_list[j] is not None:
                if sprite.collide_rect(barrier_list[i], barrier_list[j]):
                    barrier_list[i] = None
                    barrier_list[j] = None

    # Удаляем None из списка
    barrier_list = [b for b in barrier_list if b is not None]

    # Проверка столкновения игрока с препятствиями
    for b in barrier_list:
        if sprite.collide_rect(player, b):
            window.fill(BLACK)

        enemy.update(b.rect.x, b.rect.y, 5)
    enemy.move()
    # Создаем новых препятствий, чтобы их было всегда 5, избегая пересечений
    while len(barrier_list) < 3:
        x = randint(0, WIDTH - 64)
        y = randint(-200, -50)
        # Вероятность выбрать текстуру conus.png
        if random() < 0.3:
            image_path = "conus.png"
        else:
            image_path = "pocr.png"
        new_barrier = Barrier(image_path, x, y, 3)
        # Проверка перекрытия с уже существующими препятствиями и с игроком
        overlap = False
        for b in barrier_list:
            if b.rect.colliderect(new_barrier.rect):
                overlap = True
                break
        if new_barrier.rect.colliderect(player.rect):
            overlap = True
        if not overlap:
            barrier_list.append(new_barrier)    
    display.update()
    clock.tick(FPS)