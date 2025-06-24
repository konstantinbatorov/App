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
        self.rect.x = x
        self.rect.y = y
        self.speed_y = speed # Скорость падения по Y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH - self.rect.width) # Случайная X позиция
            self.rect.y = randint(-200, -50)  # Случайная Y позиция, чтобы не сразу появлялись
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
def create_meteors(num_meteors):
    """Создает метеориты, избегая перекрытия."""
    meteors = []
    occupied_positions = set()  # Множество для отслеживания занятых позиций

    for _ in range(num_meteors):
        while True:
            x = randint(0, WIDTH - 32)
            y = randint(-200, -50)
            position = (x, y)  # Создаем кортеж для хранения позиции

            # Проверяем, занята ли эта позиция другим метеоритом
            is_overlapping = False
            for existing_x, existing_y in occupied_positions:
                distance = ((x - existing_x)**2 + (y - existing_y)**2)**0.5
                if distance < 40:  # Регулируйте расстояние, чтобы избежать перекрытия
                    is_overlapping = True
                    break

            if not is_overlapping:
                break

        meteor = Meteor("car.png", x, y, 2)
        meteors.append(meteor)
        occupied_positions.add(position) # Добавляем новую позицию в множество

    return meteors

game = True
meteor_list = create_meteors(5)  # Создаем метеориты один раз в начале
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
