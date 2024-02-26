import pygame
from tools import load_image, image_choice, \
    GameOverScreen, StaticSprite, StartingScreen
import random

# константы
w = 'up'
a = 'left'
s = 'down'
d = 'right'


# класс спрайта гг
class Char(pygame.sprite.Sprite):
    # создание элементов
    def __init__(self, sheet1, sheet2, columns, rows, x, y):
        super().__init__()
        self.speed = 6
        self.frames = []
        self.columns = columns
        self.rows = rows
        self.sheets = [sheet1, sheet2]
        self.cur_sheet = self.sheets[0]
        self.cut(self.cur_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    # метод движения
    def move(self, direction):
        if direction == d:
            self.cur_sheet = self.sheets[0]
            self.rect.x += self.speed

        elif direction == a:
            self.rect.x -= self.speed

        elif direction == s:

            self.rect.y += self.speed

        elif direction == w:
            self.cur_sheet = self.sheets[1]
            self.rect.y -= self.speed

        self.check_bounds(direction)

    # метод проверки столкновений со столом и стенами
    def check_bounds(self, direction):
        # края окна
        if self.rect.x > 811:
            self.rect.x = 809
        if self.rect.x < 119:
            self.rect.x = 120

        if self.rect.y > 435:
            self.rect.y = 432
        if self.rect.y < 83:
            self.rect.y = 83

        # стол
        if 360 < self.rect.x < 566 and 176 < self.rect.y < 300:
            if direction == w:
                self.rect.y += self.speed
            elif direction == a:
                self.rect.x += self.speed
            elif direction == s:
                self.rect.y -= self.speed
            else:
                self.rect.x -= self.speed

    # метод нарезки для анимаций
    def cut(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # метод обновления спрайта
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# класс анимированного спрайта
class AnimatedSprite(pygame.sprite.Sprite):
    # метод создания
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(decor_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    # метод нарезки для анимации
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # метод обновления спрайта
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# класс проджектайлов
class AlphaParticle(pygame.sprite.Sprite):
    # метод создания спрайта проджектайла
    def __init__(self, ):
        super().__init__()
        self.image = image_choice()
        self.speed = random.choice([2, 3, 4])
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-30, 1030])
        self.rect.y = random.choice(range(570))

    # метод обновления спрайта
    def update(self):
        if self.rect.x > 500:
            x = -self.speed
        else:
            x = self.speed

        if self.rect.y > 300:
            y = -self.speed // 2
        else:
            y = self.speed // 2

        self.rect = self.rect.move(x, y)
        self.check_collision()

    # метод проверки столкновения с гг
    def check_collision(self):
        if pygame.sprite.collide_rect(self, galle):
            self.kill()
            collision_sprites.add(AlphaParticle())
            kitty_dies.score += 1
            if kitty_dies.score in [5, 15, 30, 50]:
                collision_sprites.add(AlphaParticle())

        # окончание игры
        if self.do_game_over():
            kitty_dies.game_is_over = True

    # метод проверки окончания игры
    def do_game_over(self):
        if 450 < self.rect.x < 540:
            if 280 < self.rect.y < 360:
                print(1111)
                return True


if __name__ == '__main__':
    # задание окна
    pygame.init()
    pygame.mouse.set_visible(False)
    size = width, height = 1000, 600
    screen = pygame.display
    screen.set_caption('Save the Cat')
    screen = screen.set_mode(size)
    running = True
    gameclock = pygame.time.Clock()

    # задание групп
    collision_sprites = pygame.sprite.Group()
    decor_sprites = pygame.sprite.Group()
    decor_sprites_moving = pygame.sprite.Group()
    screen_bcg = pygame.sprite.Group()
    galle_group = pygame.sprite.Group()

    # спрайт главного героя, создания окон конечного и начального экранов
    galle = Char(load_image("galwalk.png"), load_image("galback.png"), 4, 1, 720, 300)
    kitty_dies = GameOverScreen(screen, 0)
    the_beginning = StartingScreen(screen)

    # создание всех спрайтов
    vent = AnimatedSprite(load_image("vent_animation_fin.png"), 7, 1, 720, 70)
    bcg = StaticSprite(load_image('bcg.png'), 0, 0)
    table = StaticSprite(load_image('table.png'), 420, 280)
    notes = StaticSprite(pygame.transform.scale(load_image('notes.png'), (140, 60)), 180, 80)
    cat = StaticSprite(pygame.transform.scale(load_image('box.png'), (70, 50)), 470, 280)
    screen_bcg.add(bcg)
    decor_sprites.add(table, notes, cat)
    decor_sprites_moving.add(vent)
    collision_sprites.add(AlphaParticle())
    galle_group.add(galle)

    # игровой цикл
    while running:
        # проверка надобности выведения стартового окна
        if the_beginning.show:
            the_beginning()

            mp = pygame.mouse.get_pos()
            pygame.draw.circle(screen, 'white', mp, 4.5)
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    kitty_dies.try_save()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        kitty_dies.try_save()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    the_beginning.start_game(pygame.mouse.get_pos())

        # проверка, не закончилась ли игра
        elif not kitty_dies.game_is_over:
            catches = []

            keys = pygame.key.get_pressed()

            # реализация движения
            if keys[pygame.K_w]:
                galle.move(w)
                galle.update()
                gameclock.tick()
                pygame.display.flip()

            if keys[pygame.K_a]:
                galle.move(a)
                galle.update()
                gameclock.tick()
                pygame.display.flip()

            if keys[pygame.K_s]:
                galle.move(s)
                galle.update()
                gameclock.tick()
                pygame.display.flip()

            if keys[pygame.K_d]:
                galle.move(d)
                galle.update()
                gameclock.tick()
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    kitty_dies.try_save()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        kitty_dies.try_save()

            gameclock.tick(25)
            collision_sprites.update()
            decor_sprites_moving.update()
            galle_group.update()
            screen.fill((40, 20, 30))
            screen_bcg.draw(screen)
            decor_sprites_moving.draw(screen)
            decor_sprites.draw(screen)
            collision_sprites.draw(screen)
            galle_group.draw(screen)
            pygame.display.flip()

        # проверка показа конечного экрана
        else:
            kitty_dies()
            cursor_pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, 'white', cursor_pos, 3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    kitty_dies.try_save()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        kitty_dies.try_save()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.circle(screen, 'white', cursor_pos, 6)
                    if pygame.mouse.get_pos()[0] in range(300, 700) and pygame.mouse.get_pos()[1] in range(150, 450):
                        kitty_dies.game_is_over = False
                        kitty_dies.try_save()
                        print(1234)
                        for sprite in collision_sprites:
                            sprite.kill()
                            collision_sprites.empty()
                        galle.kill()
                        galle = Char(load_image("galback.png"), load_image("galwalk.png"), 4, 1, 720, 300)
                        galle_group.add(galle)
                        collision_sprites.add(AlphaParticle())

            pygame.display.flip()
            gameclock.tick(40)

    # выход из игры
    pygame.quit()
