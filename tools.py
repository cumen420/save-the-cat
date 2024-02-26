import os
import pygame
import sys
import random
import datetime

# константы
w = 'up'
a = 'left'
s = 'down'
d = 'right'


# класс статичного спрайта
class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, group=None):
        self.x, self.y = x, y
        super().__init__()
        self.image = image
        self.speed = 2
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height()).move(x, y)
        if group:
            group.add(self)


# функция загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    if not os.path.isfile(fullname):
        print("Не вышло(")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# функция выбора случайного изображения проджектайла
def image_choice():
    image = 'atoms/' + str(random.choice([1, 2, 3, 4, 5])) + '.png'
    return load_image(image)


# конечный экран
class GameOverScreen:
    # создание элементов
    def __init__(self, display, score):
        self.did_save = False
        self.score = score
        self.display = display
        self.font = pygame.font.Font('assets/font/joystix monospace.otf', 40)
        self.game_is_over = False
        self.button = StaticSprite(pygame.transform.scale(load_image('enbutton.png'), (400, 300)), 300, 150)
        self.group = pygame.sprite.Group()
        self.group.add(self.button)

    # отображение элементов на окно
    def __call__(self, *args, **kwargs):
        self.text = f' GAME OVER! YOUR SCORE: {self.score}!'
        self.printing = self.font.render(self.text, True, (255, 255, 255))
        self.display.fill('black')
        self.display.blit(self.printing, (1000 // 2 - self.printing.get_width() // 2, 10))
        self.group.draw(self.display)

        # обновление/отрисовка
        pygame.display.flip()

    # сохранение информации об игре в файл
    def try_save(self):
        if not self.did_save:
            save = open('user data.txt', 'a', encoding='UTF-8')
            time = datetime.datetime.now()
            print(f'Run:{time.day}.{time.month}.{time.day} {time.hour}:{time.minute}:{time.second}; '
                f'Score: {self.score}', file=save)
            save.close()
        else:
            return


# начальный экран
class StartingScreen:
    # создание элементов
    def __init__(self, display):
        self.show = True
        self.display = display
        self.text = f'Save the cat!'
        self.font = pygame.font.Font('assets/font/joystix monospace.otf', 70)
        self.start = StaticSprite(pygame.transform.scale(load_image('button.png'), (400, 200)), 300, 250)
        self.group = pygame.sprite.Group()
        self.group.add(self.start)

    # отрисовка
    def __call__(self, *args, **kwargs):
        self.printing = self.font.render(self.text, True, (255, 255, 255))
        self.display.fill('black')
        self.display.blit(self.printing, (1000 // 2 - self.printing.get_width() // 2, 100))
        self.group.draw(self.display)

    # начало игры снова
    def start_game(self, pos):
        if 300 < pos[0] < 700 and 250 < pos[1] < 450:
            print("success")
            self.show = False
            return True
        else:
            return False
