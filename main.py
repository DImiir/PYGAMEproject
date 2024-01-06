import pygame
import sys
import random

pygame.init()
all_sprites = pygame.sprite.Group()
attacks = pygame.sprite.Group()
enemies = pygame.sprite.Group()
info = pygame.display.Info()
size = width, height = 0.8 * info.current_w, 0.8 * info.current_h
screen = pygame.display.set_mode(size)
pygame.display.set_caption("KINGDOM: A CHILDHOOD DREAM BUT IT IS MORE REALISTIC")
clock = pygame.time.Clock()
fullscreen_mode = False


class Character(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.first_pos = pygame.image.load('pictures/character/1pos.tiff')
        self.image = pygame.transform.scale(self.first_pos, (self.first_pos.get_width() * 4,
                                                             self.first_pos.get_height() * 4))
        self.frames_for_right = [pygame.image.load('pictures/character/go_right1.tiff'),
                                 pygame.image.load('pictures/character/go_right1.tiff'),
                                 pygame.image.load('pictures/character/go_right2.tiff'),
                                 pygame.image.load('pictures/character/go_right2.tiff'),
                                 pygame.image.load('pictures/character/go_right3.tiff'),
                                 pygame.image.load('pictures/character/go_right3.tiff')]
        self.frames_for_left = [pygame.transform.flip(im, True, False) for im in self.frames_for_right]
        self.frames_for_up = [pygame.image.load('pictures/character/go_back1.tiff'),
                              pygame.image.load('pictures/character/go_back1.tiff'),
                              pygame.image.load('pictures/character/go_back2.tiff'),
                              pygame.image.load('pictures/character/go_back2.tiff'),
                              pygame.image.load('pictures/character/go_back3.tiff'),
                              pygame.image.load('pictures/character/go_back3.tiff')]
        self.right, self.up = True, False
        self.cur_frame1, self.cur_frame2, self.cur_frame3, self.cur_frame4 = 0, 0, 0, 0
        self.speed = 10
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.HP = 100
        self.last_hit = 0

    def move(self):
        if to_up1:
            if self.pos_y > 35:
                self.pos_y -= self.speed
        if to_down1:
            if self.pos_y < height / 0.8 - self.image.get_height() - 15:
                self.pos_y += self.speed
        if to_left1:
            if self.pos_x > 15:
                self.pos_x -= self.speed
        if to_right1:
            if self.pos_x < width / 0.8 - self.image.get_width() - 15:
                self.pos_x += self.speed
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def update(self):
        if not any([to_up1, to_down1, to_left1, to_right1]):
            if self.up:
                self.image = pygame.transform.scale(
                    self.frames_for_up[0], (self.frames_for_up[0].get_width() * 4,
                                            self.frames_for_up[0].get_height() * 4))
            elif self.right:
                self.image = pygame.transform.scale(
                    self.first_pos, (self.first_pos.get_width() * 4,
                                     self.first_pos.get_height() * 4))
            else:
                self.image = pygame.transform.scale(
                    self.first_pos, (self.first_pos.get_width() * 4,
                                     self.first_pos.get_height() * 4))
                self.image = pygame.transform.flip(self.image, True, False)
        elif to_up1:
            self.cur_frame1 = (self.cur_frame1 + 1) % len(self.frames_for_up)
            image = self.frames_for_up[self.cur_frame1]
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
            self.up = True
        elif to_down1:
            if self.right:
                self.cur_frame2 = (self.cur_frame2 + 1) % len(self.frames_for_right)
                image = self.frames_for_right[self.cur_frame2]
                self.image = pygame.transform.scale(
                    image, (image.get_width() * 4,
                            image.get_height() * 4))
            else:
                self.cur_frame2 = (self.cur_frame2 + 1) % len(self.frames_for_left)
                image = self.frames_for_left[self.cur_frame2]
                self.image = pygame.transform.scale(
                    image, (image.get_width() * 4,
                            image.get_height() * 4))
            self.up = False
        elif to_left1:
            self.cur_frame3 = (self.cur_frame3 + 1) % len(self.frames_for_left)
            image = self.frames_for_left[self.cur_frame3]
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
            self.right = False
            self.up = False
        elif to_right1:
            self.cur_frame4 = (self.cur_frame4 + 1) % len(self.frames_for_right)
            image = self.frames_for_right[self.cur_frame4]
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
            self.right = True
            self.up = False

    def hit(self, damage):
        if pygame.time.get_ticks() - self.last_hit >= 2000:
            self.HP -= damage
            self.last_hit = pygame.time.get_ticks()
            if self.HP <= 0:
                all_sprites.remove(self)


class Attack(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, movement):
        super().__init__(all_sprites, attacks)
        first_pos = pygame.image.load('pictures/gold_attack/gold1.tiff')
        self.image = pygame.transform.scale(first_pos, (first_pos.get_width() * 4, first_pos.get_height() * 4))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.cur_frame = 0
        self.frames = [pygame.transform.rotate(first_pos, 90), pygame.transform.rotate(first_pos, 180),
                       pygame.transform.rotate(first_pos, 270), pygame.transform.rotate(first_pos, 360)]
        self.frames_for_right = [pygame.image.load('pictures/gold_attack/gold1.tiff'),
                                 pygame.image.load('pictures/gold_attack/gold2.tiff'),
                                 pygame.image.load('pictures/gold_attack/gold3.tiff'),
                                 pygame.image.load('pictures/gold_attack/gold2.tiff')]
        self.frames_for_left = [pygame.transform.flip(im, True, False) for im in self.frames_for_right]
        self.frames_for_up = [pygame.transform.flip(im, False, True) for im in self.frames_for_right]
        self.frames_for_down = [pygame.transform.flip(im, True, True) for im in self.frames_for_right]
        self.speed = 20
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.movement = movement
        self.damage = 25

    def move(self):
        if self.movement == 'up':
            self.pos_y -= self.speed
        if self.movement == 'down':
            self.pos_y += self.speed
        if self.movement == 'left':
            self.pos_x -= self.speed
        if self.movement == 'right':
            self.pos_x += self.speed
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(
            image, (image.get_width() * 4,
                    image.get_height() * 4))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, enemies)
        self.first_pos = pygame.image.load('pictures/enemy/1pos.tiff')
        self.image = pygame.transform.scale(self.first_pos, (self.first_pos.get_width() * 4,
                                                             self.first_pos.get_height() * 4))
        self.frames_for_right = [pygame.image.load('pictures/enemy/go_right1.tiff'),
                                 pygame.image.load('pictures/enemy/go_right1.tiff'),
                                 pygame.image.load('pictures/enemy/go_right2.tiff'),
                                 pygame.image.load('pictures/enemy/go_right2.tiff'),
                                 pygame.image.load('pictures/enemy/go_right3.tiff'),
                                 pygame.image.load('pictures/enemy/go_right3.tiff')]
        self.frames_for_left = [pygame.transform.flip(im, True, False) for im in self.frames_for_right]
        self.frames_for_up = [pygame.image.load('pictures/enemy/go_back1.tiff'),
                              pygame.image.load('pictures/enemy/go_back1.tiff'),
                              pygame.image.load('pictures/enemy/go_back2.tiff'),
                              pygame.image.load('pictures/enemy/go_back2.tiff'),
                              pygame.image.load('pictures/enemy/go_back3.tiff'),
                              pygame.image.load('pictures/enemy/go_back3.tiff')]
        self.right = True
        self.cur_frame1, self.cur_frame2, self.cur_frame3, self.cur_frame4 = 0, 0, 0, 0
        self.speed = 5
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.HP = 200
        self.damage = 20

    def move(self):
        if chel.pos_y < self.pos_y:
            if self.pos_y > 35:
                self.pos_y -= self.speed
        if chel.pos_y > self.pos_y:
            if self.pos_y < height / 0.8 - self.image.get_height() - 15:
                self.pos_y += self.speed
        if chel.pos_x < self.pos_x:
            if self.pos_x > 15:
                self.pos_x -= self.speed
        if chel.pos_x > self.pos_x:
            if self.pos_x < width / 0.8 - self.image.get_width() - 15:
                self.pos_x += self.speed
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def update(self):
        if chel.pos_y < self.pos_y:
            self.cur_frame1 = (self.cur_frame1 + 1) % len(self.frames_for_up)
            image = self.frames_for_up[self.cur_frame1]
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
        elif chel.pos_y > self.pos_y:
            if self.right:
                self.cur_frame2 = (self.cur_frame2 + 1) % len(self.frames_for_right)
                image = self.frames_for_right[self.cur_frame2]
                self.image = pygame.transform.scale(
                    image, (image.get_width() * 4,
                            image.get_height() * 4))
            else:
                self.cur_frame2 = (self.cur_frame2 + 1) % len(self.frames_for_left)
                image = self.frames_for_left[self.cur_frame2]
                self.image = pygame.transform.scale(
                    image, (image.get_width() * 4,
                            image.get_height() * 4))
        elif chel.pos_x < self.pos_x:
            self.cur_frame3 = (self.cur_frame3 + 1) % len(self.frames_for_left)
            image = self.frames_for_left[self.cur_frame3]
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
            self.right = False
        elif chel.pos_x > self.pos_x:
            self.cur_frame4 = (self.cur_frame4 + 1) % len(self.frames_for_right)
            image = self.frames_for_right[self.cur_frame4]
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
            self.right = True

    def hit(self, damage):
        self.HP -= damage
        if self.HP <= 0:
            enemies.remove(enem)
            all_sprites.remove(enem)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    global fullscreen_mode
    image = pygame.image.load('pictures/second.tiff')
    fon = pygame.transform.scale(image, size)
    screen.blit(fon, (0, 0))
    start_screen_tool()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                fullscreen_mode = not fullscreen_mode
                if fullscreen_mode:
                    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                    fon = pygame.transform.scale(image, (info.current_w, info.current_h))
                    screen.blit(fon, (0, 0))
                    start_screen_tool()
                else:
                    screen = pygame.display.set_mode(size)
                    fon = pygame.transform.scale(image, size)
                    screen.blit(fon, (0, 0))
                    start_screen_tool()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)


def start_screen_tool():
    intro_text = ["KINGDOM: A CHILDHOOD DREAM BUT IT IS MORE REALISTIC",
                  "",
                  "НАЖМИТЕ ЧТО-НИБУДЬ",
                  "ЧТОБЫ НАЧАТЬ"]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def game_over(screen):
    global fullscreen_mode
    image = pygame.image.load('pictures/game_over.tiff')
    fon = pygame.transform.scale(image, size)
    if fullscreen_mode:
        fon = pygame.transform.scale(image, (info.current_w, info.current_h))
    screen.blit(fon, (0, 0))
    start_screen_tool()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                fullscreen_mode = not fullscreen_mode
                if fullscreen_mode:
                    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                    fon = pygame.transform.scale(image, (info.current_w, info.current_h))
                    screen.blit(fon, (0, 0))
                    start_screen_tool()
                else:
                    screen = pygame.display.set_mode(size)
                    fon = pygame.transform.scale(image, size)
                    screen.blit(fon, (0, 0))
                    start_screen_tool()
        pygame.display.flip()
        clock.tick(60)


start_screen(screen)
chel = Character(100, 100)
image = pygame.image.load('pictures/background.png')
background = pygame.transform.scale(image, (info.current_w, info.current_h))
to_right1, to_left1, to_up1, to_down1 = False, False, False, False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            fullscreen_mode = not fullscreen_mode
            if fullscreen_mode:
                screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode(size)
        if fullscreen_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    to_left1 = True
                if event.key == pygame.K_d:
                    to_right1 = True
                if event.key == pygame.K_s:
                    to_down1 = True
                if event.key == pygame.K_w:
                    to_up1 = True
                if event.key == pygame.K_LEFT:
                    Attack(chel.pos_x - 10, chel.pos_y + 20, 'left')
                if event.key == pygame.K_RIGHT:
                    Attack(chel.pos_x + 10, chel.pos_y + 20, 'right')
                if event.key == pygame.K_DOWN:
                    Attack(chel.pos_x + 10, chel.pos_y + 10, 'down')
                if event.key == pygame.K_UP:
                    Attack(chel.pos_x + 10, chel.pos_y - 10, 'up')
                if event.key == pygame.K_q:
                    Enemy(random.randint(500, 700), random.randint(500, 700))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    to_left1 = False
                    chel.cur_frame3 = 0
                if event.key == pygame.K_d:
                    to_right1 = False
                    chel.cur_frame4 = 0
                if event.key == pygame.K_s:
                    to_down1 = False
                    chel.cur_frame2 = 0
                if event.key == pygame.K_w:
                    chel.cur_frame1 = 0
                    to_up1 = False
    if fullscreen_mode:
        screen.fill((0, 0, 0))
        clock.tick(30)
        screen.blit(background, (0, 0))
        if enemies:
            for enem in enemies:
                enem.move()
        if attacks:
            for atk in attacks:
                atk.move()
                if (atk.pos_x <= 10 or atk.pos_x >= width / 0.8 - atk.image.get_width() - 10
                        or atk.pos_y <= 40 or atk.pos_y >= height / 0.8 - atk.image.get_height() - 10):
                    attacks.remove(atk)
                    all_sprites.remove(atk)
                if enemies:
                    for enem in enemies:
                        if atk.rect.colliderect(enem.rect):
                            enem.hit(atk.damage)
                            attacks.remove(atk)
                            all_sprites.remove(atk)
        if enemies:
            for enem in enemies:
                if chel.rect.colliderect(enem.rect):
                    chel.hit(enem.damage)
        if chel not in all_sprites:
            game_over(screen)
        chel.move()
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
    else:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text1 = font.render("Нажмите F чтобы войти в полноэкранный режим", True, (255, 255, 255))
        text2 = font.render("(без этого никак)", True, (255, 255, 255))
        text_x1 = width // 2 - text1.get_width() // 2
        text_y1 = height // 2 - text1.get_height()
        text_x2 = width // 2 - text2.get_width() // 2
        text_y2 = height // 2 + text2.get_height()
        screen.blit(text1, (text_x1, text_y1))
        screen.blit(text2, (text_x2, text_y2))
        pygame.display.flip()
