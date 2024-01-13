import pygame
import sys
import random
import sqlite3

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
image = pygame.image.load('pictures/background.png')
background = pygame.transform.scale(image, (info.current_w, info.current_h))
to_right1, to_left1, to_up1, to_down1 = False, False, False, False
score = 0


def game(fullscreen_mode, screen):
    global to_right1, to_left1, to_up1, to_down1
    stamina_cd = 0
    fight_cd = 0
    fight = False
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
                    if chel.stamina >= 20 and pygame.time.get_ticks() - fight_cd > 3000:
                        if event.key == pygame.K_LEFT:
                            Attack(chel.pos_x - 10, chel.pos_y + 20, 'left')
                        if event.key == pygame.K_RIGHT:
                            Attack(chel.pos_x + 10, chel.pos_y + 20, 'right')
                        if event.key == pygame.K_DOWN:
                            Attack(chel.pos_x + 10, chel.pos_y + 10, 'down')
                        if event.key == pygame.K_UP:
                            Attack(chel.pos_x + 10, chel.pos_y - 10, 'up')
                    if event.key == pygame.K_e and 630 < chel.pos_x <= 760 and 0 < chel.pos_y <= 100 and not enemies:
                        level_build()
                        fight_cd = pygame.time.get_ticks()
                        fight = True
                        chel.pos_y += 800 - chel.pos_y
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
            pygame.draw.rect(screen, pygame.color.Color('red'), (18, 18, chel.HP * 4, 20))
            pygame.draw.rect(screen, pygame.color.Color('blue'), (18, 40, chel.stamina * 2, 20))
            if pygame.time.get_ticks() - fight_cd > 3000:
                fight = False
                if enemies:
                    for enem in enemies:
                        enem.move()
                        if chel.rect.colliderect(enem.rect):
                            enem.player_hit()
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
            if chel not in all_sprites:
                return
            if pygame.time.get_ticks() - stamina_cd >= 1000 and chel.stamina < 200:
                chel.stamina += 20
                stamina_cd = pygame.time.get_ticks()
            chel.move()
            all_sprites.update()
            all_sprites.draw(screen)
            font = pygame.font.Font(None, 50)
            text = font.render(str(score), True, (255, 255, 255))
            text_w, text_h = text.get_width(), text.get_height()
            screen.blit(text, (info.current_w - text_w - 10, 18))
            pygame.draw.rect(screen, (255, 255, 255), (info.current_w - text_w - 20, 18,
                                                       text_w + 20, text_h), 1)
            middle_text = font.render('0', True, (255, 255, 255))
            if not enemies and 630 < chel.pos_x <= 760 and 0 < chel.pos_y <= 100:
                middle_text = font.render('Нажмите E, чтобы перейти в следующую комнату', True, (255, 255, 255))
            if pygame.time.get_ticks() - fight_cd <= 3000:
                middle_text = font.render('1', True, (255, 255, 255))
            if pygame.time.get_ticks() - fight_cd <= 2000:
                middle_text = font.render('2', True, (255, 255, 255))
            if pygame.time.get_ticks() - fight_cd <= 1000:
                middle_text = font.render('3', True, (255, 255, 255))
            if fight or (not enemies and 630 < chel.pos_x <= 760 and 0 < chel.pos_y <= 100):
                middle_text_w, middle_text_h = middle_text.get_width(), middle_text.get_height()
                pygame.draw.rect(screen, (0, 0, 0), (info.current_w // 2 - middle_text_w // 2 - 20,
                                                     info.current_h // 2 - middle_text_h // 2 - 20,
                                                     middle_text_w + 40, middle_text_h + 40))
                screen.blit(middle_text, (info.current_w // 2 - middle_text_w // 2,
                                          info.current_h // 2 - middle_text_h // 2))
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
        self.stamina = 200
        self.last_hit = 0

    def move(self):
        if to_up1:
            if self.pos_y > 35:
                if to_left1 or to_right1:
                    self.pos_y -= self.speed // 2
                else:
                    self.pos_y -= self.speed
        if to_down1:
            if self.pos_y < height / 0.8 - self.image.get_height() - 15:
                if to_left1 or to_right1:
                    self.pos_y += self.speed // 2
                else:
                    self.pos_y += self.speed
        if to_left1:
            if self.pos_x > 15:
                if to_down1 or to_up1:
                    self.pos_x -= self.speed // 2
                else:
                    self.pos_x -= self.speed
        if to_right1:
            if self.pos_x < width / 0.8 - self.image.get_width() - 15:
                if to_down1 or to_up1:
                    self.pos_x += self.speed // 2
                else:
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
        chel.stamina -= 20

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
        self.speed = 3
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.HP = 200
        self.damage = 20
        self.last_hit = 0

    def move(self):
        if chel.pos_y < self.pos_y:
            if self.pos_y > 35:
                self.pos_y -= self.speed
        if chel.pos_y >= self.pos_y:
            if self.pos_y < height / 0.8 - self.image.get_height() - 15:
                self.pos_y += self.speed
        if chel.pos_x < self.pos_x:
            if self.pos_x > 15:
                self.pos_x -= self.speed
        if chel.pos_x >= self.pos_x:
            if self.pos_x < width / 0.8 - self.image.get_width() - 15:
                self.pos_x += self.speed
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def update(self):
        if chel.pos_x < self.pos_x:
            self.cur_frame3 = (self.cur_frame3 + 1) % len(self.frames_for_left)
            self.image = self.frames_for_left[self.cur_frame3]
            self.right = False
        if chel.pos_x > self.pos_x:
            self.cur_frame4 = (self.cur_frame4 + 1) % len(self.frames_for_right)
            self.image = self.frames_for_right[self.cur_frame4]
            self.right = True
        if chel.pos_y + 3 < self.pos_y:
            self.cur_frame1 = (self.cur_frame1 + 1) % len(self.frames_for_up)
            self.image = self.frames_for_up[self.cur_frame1]
        if chel.pos_y - 3 > self.pos_y:
            if self.right:
                self.cur_frame2 = (self.cur_frame2 + 1) % len(self.frames_for_right)
                self.image = self.frames_for_right[self.cur_frame2]
            else:
                self.cur_frame2 = (self.cur_frame2 + 1) % len(self.frames_for_left)
                self.image = self.frames_for_left[self.cur_frame2]
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() * 4,
                         self.image.get_height() * 4))

    def hit(self, damage):
        global score
        self.HP -= damage
        if chel.pos_y < self.pos_y:
            self.pos_y += 12
        if chel.pos_y > self.pos_y:
            self.pos_y -= 12
        if chel.pos_x < self.pos_x:
            self.pos_x += 12
        if chel.pos_x > self.pos_x:
            self.pos_x -= 12
        if self.HP <= 0:
            enemies.remove(self)
            all_sprites.remove(self)
            score += 10

    def player_hit(self):
        if pygame.time.get_ticks() - self.last_hit >= 2000:
            chel.HP -= self.damage
            self.last_hit = pygame.time.get_ticks()
            if chel.HP <= 0:
                all_sprites.remove(chel)


def terminate():
    pygame.quit()
    sys.exit()


def start_end_screen(screen, end):
    global fullscreen_mode
    statistics = False
    text = ["KINGDOM: A CHILDHOOD DREAM BUT IT IS MORE REALISTIC",
            "", "НАЧАТЬ", "", "СТАТИСТИКА"]
    image = pygame.image.load('pictures/second.tiff')
    if end:
        text = ["KINGDOM: A CHILDHOOD DREAM BUT IT IS MORE REALISTIC",
                "", f"ВЫ НАБРАЛИ {score}", "НАЖМИТЕ Q", "ЧТОБЫ ВЕРНУТЬСЯ"]
        image = pygame.image.load('pictures/game_over.tiff')
    fon = pygame.transform.scale(image, size)
    if fullscreen_mode:
        fon = pygame.transform.scale(image, (info.current_w, info.current_h))
    screen.blit(fon, (0, 0))
    text_tool(text)
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
                    text_tool(text)
                else:
                    screen = pygame.display.set_mode(size)
                    fon = pygame.transform.scale(image, size)
                    screen.blit(fon, (0, 0))
                    text_tool(text)
            elif end and event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                all_sprites.empty()
                enemies.empty()
                attacks.empty()
                restart()
            elif not end and event.type == pygame.MOUSEBUTTONDOWN:
                if not statistics and 5 < event.pos[0] <= 95 and 115 < event.pos[1] <= 145:
                    return
                if 5 < event.pos[0] <= 148 and 175 < event.pos[1] <= 205:
                    statistics = True
                if statistics and 5 < event.pos[0] <= 88 and 55 < event.pos[1] <= 85:
                    statistics = False
        if statistics:
            screen.blit(fon, (0, 0))
            image = pygame.image.load('pictures/statistics.tiff')
            fon = pygame.transform.scale(image, size)
            if fullscreen_mode:
                fon = pygame.transform.scale(image, (info.current_w, info.current_h))
            screen.blit(fon, (0, 0))
            text = ["НАЗАД"]
            text_tool(text)
        elif not end:
            screen.blit(fon, (0, 0))
            image = pygame.image.load('pictures/second.tiff')
            fon = pygame.transform.scale(image, size)
            if fullscreen_mode:
                fon = pygame.transform.scale(image, (info.current_w, info.current_h))
            screen.blit(fon, (0, 0))
            text = ["KINGDOM: A CHILDHOOD DREAM BUT IT IS MORE REALISTIC",
                    "", "НАЧАТЬ", "", "СТАТИСТИКА"]
            text_tool(text)
        pygame.display.flip()
        clock.tick(60)


def text_tool(text):
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for num, line in enumerate(text):
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        if line not in ['', 'KINGDOM: A CHILDHOOD DREAM BUT IT IS MORE REALISTIC']:
            pygame.draw.rect(screen, pygame.color.Color('black'), (intro_rect.x - 5, intro_rect.top - 5,
                                                                   intro_rect.width + 10, intro_rect.height + 10), 1)
        screen.blit(string_rendered, intro_rect)


def level_build():
    for number in range(random.randint(1, 5)):
        Enemy(random.randint(16, info.current_w - 34), random.randint(36, info.current_h - 54))


def restart():
    global chel, to_right1, to_left1, to_up1, to_down1
    to_right1, to_left1, to_up1, to_down1 = False, False, False, False
    start_end_screen(screen, False)
    chel = Character(150, 200)
    game(fullscreen_mode, screen)
    start_end_screen(screen, True)


start_end_screen(screen, False)
chel = Character(150, 200)
game(fullscreen_mode, screen)
start_end_screen(screen, True)
