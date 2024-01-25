import pygame
import sys
import random
import sqlite3

pygame.init()
pygame.display.set_icon(pygame.image.load('pictures/icon.png'))
all_sprites = pygame.sprite.Group()
attacks = pygame.sprite.Group()
enemies = pygame.sprite.Group()
potions = pygame.sprite.Group()
info = pygame.display.Info()
size = width, height = 0.8 * info.current_w, 0.8 * info.current_h
screen = pygame.display.set_mode(size)
pygame.display.set_caption("KINGDOM: A CHILDHOOD DREAM BUT MORE REALISTIC")
clock = pygame.time.Clock()
fullscreen_mode = False
image = pygame.image.load('pictures/background.png')
background = pygame.transform.scale(image, (info.current_w, info.current_h))
to_right1, to_left1, to_up1, to_down1 = False, False, False, False
score = 0
nickname = ''
lvl = 0
speed_gain, strength_gain, health_gain = 0, 0, 0
minimum, maximum = 1, 6
sound1 = pygame.mixer.Sound('sounds/punch flesh 1.wav')
sound2 = pygame.mixer.Sound('sounds/umbrella hit 18.wav')
sound3 = pygame.mixer.Sound('sounds/05_door_open_1.mp3')
sound4 = pygame.mixer.Sound('sounds/06_door_close_1.mp3')


def game(fullscreen_mode, screen):
    global to_right1, to_left1, to_up1, to_down1, lvl
    stamina_cd = 0
    fight_cd = 0
    fight = False
    pygame.mixer.music.load('sounds/Goblins_Dance_(Battle).wav')
    pygame.mixer.music.play(-1)
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
                    if chel.rect.colliderect(door.rect) and not enemies:
                        if event.key == pygame.K_e:
                            pygame.mixer.Sound.play(sound3)
                            level_build()
                            fight_cd = pygame.time.get_ticks()
                            fight = True
                            chel.pos_y += 790 - chel.pos_y
                            door.pos_x = random.randint(400, 1300)
                            lvl += 1
                            pygame.mixer.Sound.play(sound4)
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
                                pygame.mixer.Sound.play(sound2)
                                enem.hit(atk.damage)
                                attacks.remove(atk)
                                all_sprites.remove(atk)
            if chel not in all_sprites:
                pygame.mixer.music.stop()
                return
            if pygame.time.get_ticks() - stamina_cd >= 1000 and chel.stamina < 200:
                chel.stamina += 20
                stamina_cd = pygame.time.get_ticks()
            if potions:
                for potion in potions:
                    if chel.rect.colliderect(potion.rect):
                        chel.HP += potion.HP_up
                        all_sprites.remove(potion)
                        potions.remove(potion)
            chel.move()
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.draw.rect(screen, pygame.color.Color('red'), (18, 18, chel.HP * 4, 20))
            pygame.draw.rect(screen, pygame.color.Color('blue'), (18, 40, chel.stamina * 2, 20))
            font = pygame.font.Font(None, 50)
            text = font.render(str(score), True, (255, 255, 255))
            text_w, text_h = text.get_width(), text.get_height()
            screen.blit(text, (info.current_w - text_w - 10, 18))
            pygame.draw.rect(screen, (255, 255, 255), (info.current_w - text_w - 20, 18, text_w + 20, text_h), 1)
            middle_text = font.render('0', True, (255, 255, 255))
            if not enemies and chel.rect.colliderect(door.rect):
                middle_text = font.render('Нажмите E, чтобы перейти в следующую комнату', True, (255, 255, 255))
            if pygame.time.get_ticks() - fight_cd <= 3000:
                middle_text = font.render('1', True, (255, 255, 255))
            if pygame.time.get_ticks() - fight_cd <= 2000:
                middle_text = font.render('2', True, (255, 255, 255))
            if pygame.time.get_ticks() - fight_cd <= 1000:
                middle_text = font.render('3', True, (255, 255, 255))
            if fight or (not enemies and chel.rect.colliderect(door.rect)):
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
            if self.pos_y > 50:
                if to_left1 or to_right1:
                    self.pos_y -= self.speed // 2
                else:
                    self.pos_y -= self.speed
        if to_down1:
            if self.pos_y < height / 0.8 - self.image.get_height() - 20:
                if to_left1 or to_right1:
                    self.pos_y += self.speed // 2
                else:
                    self.pos_y += self.speed
        if to_left1:
            if self.pos_x > 20:
                if to_down1 or to_up1:
                    self.pos_x -= self.speed // 2
                else:
                    self.pos_x -= self.speed
        if to_right1:
            if self.pos_x < width / 0.8 - self.image.get_width() - 20:
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
                self.image = pygame.transform.scale(self.first_pos, (self.first_pos.get_width() * 4,
                                                                     self.first_pos.get_height() * 4))
            else:
                self.image = pygame.transform.scale(self.first_pos, (self.first_pos.get_width() * 4,
                                                                     self.first_pos.get_height() * 4))
                self.image = pygame.transform.flip(self.image, True, False)
        elif to_up1:
            self.cur_frame1 = (self.cur_frame1 + 1) % len(self.frames_for_up)
            image = self.frames_for_up[self.cur_frame1]
            self.image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
            self.up = True
        elif to_down1:
            if self.right:
                self.cur_frame2 = (self.cur_frame2 + 1) % len(self.frames_for_right)
                image = self.frames_for_right[self.cur_frame2]
                self.image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
            else:
                self.cur_frame2 = (self.cur_frame2 + 1) % len(self.frames_for_left)
                image = self.frames_for_left[self.cur_frame2]
                self.image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
            self.up = False
        elif to_left1:
            self.cur_frame3 = (self.cur_frame3 + 1) % len(self.frames_for_left)
            image = self.frames_for_left[self.cur_frame3]
            self.image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
            self.right = False
            self.up = False
        elif to_right1:
            self.cur_frame4 = (self.cur_frame4 + 1) % len(self.frames_for_right)
            image = self.frames_for_right[self.cur_frame4]
            self.image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
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
        self.image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))


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
            if random.randint(1, 10) == 1:
                potion = Potion(self.pos_x + random.randint(5, 10), self.pos_y + random.randint(10, 15))

    def player_hit(self):
        if pygame.time.get_ticks() - self.last_hit >= 2000:
            pygame.mixer.Sound.play(sound1)
            chel.HP -= self.damage
            self.last_hit = pygame.time.get_ticks()
            if chel.HP <= 0:
                all_sprites.remove(chel)


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.pos_x = x
        self.pos_y = y
        self.image = pygame.image.load('pictures/door.png')
        self.image = pygame.transform.scale(self.image, ((info.current_w / 89) * 9, 0.125 * info.current_h))
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        self.image = pygame.transform.scale(self.image, ((info.current_w / 89) * 9, 0.125 * info.current_h))
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


def terminate():
    pygame.quit()
    sys.exit()


def start_end_screen(screen, end):
    global fullscreen_mode
    statistics = False
    image = pygame.image.load('pictures/second.tiff')
    text = [""]
    fon = pygame.transform.scale(image, size)
    while True:
        screen.blit(fon, (0, 0))
        if end:
            text = ["KINGDOM: A CHILDHOOD DREAM BUT MORE REALISTIC", "", f"ВЫ НАБРАЛИ {score}", "", "ВЕРНУТЬСЯ"]
            image = pygame.image.load('pictures/game_over.tiff')
        elif statistics:
            image = pygame.image.load('pictures/statistics.tiff')
            text = ["НАЗАД"]
            con = sqlite3.connect("database")
            cur = con.cursor()
            table = cur.execute("SELECT * FROM score").fetchall()[-15:]
            font = pygame.font.Font('GloriaHallelujah-Regular.ttf', 30)
            y_string = 0
            x_string = 2 * (width / 19)
            if fullscreen_mode:
                x_string = 2 * (info.current_w / 19)
            for i in table:
                y_string += 50
                string = [str(j) for j in i]
                string = font.render('  '.join(string), True, 'black')
                screen.blit(string, (x_string, y_string))
            con.commit()
            con.close()
        elif not end:
            screen.blit(fon, (0, 0))
            image = pygame.image.load('pictures/second.tiff')
            text = ["KINGDOM: A CHILDHOOD DREAM BUT MORE REALISTIC", "", "НАЧАТЬ", "", "СТАТИСТИКА"]
        fon = pygame.transform.scale(image, size)
        if fullscreen_mode:
            fon = pygame.transform.scale(image, (info.current_w, info.current_h))
        text_tool(text)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                fullscreen_mode = not fullscreen_mode
                if fullscreen_mode:
                    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not statistics and not end and 5 < event.pos[0] <= 95 and 115 < event.pos[1] <= 145:
                    login(screen)
                    return
                if not end and 5 < event.pos[0] <= 148 and 175 < event.pos[1] <= 205:
                    statistics = True
                if statistics and 5 < event.pos[0] <= 88 and 55 < event.pos[1] <= 85:
                    statistics = False
                if end and 5 < event.pos[0] <= 148 and 175 < event.pos[1] <= 205:
                    all_sprites.empty()
                    enemies.empty()
                    attacks.empty()
                    con = sqlite3.connect("database")
                    cur = con.cursor()
                    cur.execute("INSERT INTO score (nickname, score_number, lvl) VALUES (?, ?, ?)",
                                (nickname, f'{score} points', f'{lvl} level'))
                    con.commit()
                    con.close()
                    restart()


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
        if line not in ['', 'KINGDOM: A CHILDHOOD DREAM BUT MORE REALISTIC']:
            pygame.draw.rect(screen, pygame.color.Color('black'), (intro_rect.x - 5, intro_rect.top - 5,
                                                                   intro_rect.width + 10, intro_rect.height + 10), 1)
        screen.blit(string_rendered, intro_rect)


def level_build():
    global minimum, maximum
    if lvl in [5, 10, 15, 20]:
        minimum += 1
        maximum += 1
    for number in range(random.randint(minimum, maximum)):
        Enemy(random.randint(50, info.current_w - 100), random.randint(50, info.current_h - 100))
    level_up()
    potions.empty()


def restart():
    global chel, to_right1, to_left1, to_up1, to_down1, door, score
    to_right1, to_left1, to_up1, to_down1 = False, False, False, False
    score = 0
    start_end_screen(screen, False)
    door = Door(random.randint(200, 1240), 0)
    chel = Character(300, 300)
    game(fullscreen_mode, screen)
    start_end_screen(screen, True)


def login(screen):
    global fullscreen_mode, nickname
    name = ''
    font = pygame.font.Font(None, 50)
    NAME = font.render(name, True, 'white')
    text = font.render("Как твоё имя ?", True, 'white')
    enter_text = font.render("Нажмите ENTER, чтобы продолжить", True, 'white')
    width = 0.8 * info.current_w // 2
    height = 0.8 * info.current_h // 2
    if fullscreen_mode:
        width = info.current_w // 2
        height = info.current_h // 2
    x = width - 150
    y = height - 50
    text_x1 = width - text.get_width() // 2
    text_y1 = height - text.get_height() - 100
    enter_text_x = width - enter_text.get_width() // 2
    enter_text_y = height - enter_text.get_height() + 100
    input_on = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x < event.pos[0] <= 300 + x and y < event.pos[1] <= 50 + y:
                    input_on = True
                else:
                    input_on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    nickname = name
                    return
                if input_on:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_SPACE:
                        pass
                    else:
                        letter1 = event.unicode
                        letter2 = font.render(letter1, True, 'white')
                        if NAME.get_width() + letter2.get_width() <= 280:
                            name += letter1
                    NAME = font.render(name, True, 'white')
                else:
                    if event.key == pygame.K_f:
                        fullscreen_mode = not fullscreen_mode
                        if fullscreen_mode:
                            screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                            width = info.current_w // 2
                            height = info.current_h // 2
                        else:
                            screen = pygame.display.set_mode(size)
                            width = 0.8 * info.current_w // 2
                            height = 0.8 * info.current_h // 2
                        x = width - 150
                        y = height - 50
                        text_x1 = width - text.get_width() // 2
                        text_y1 = height - text.get_height() - 100
                        enter_text_x = width - enter_text.get_width() // 2
                        enter_text_y = height - enter_text.get_height() + 100
        pygame.draw.rect(screen, 'white', (x, y, 300, 50), 1)
        screen.blit(NAME, (x + 10, y + 10, 300, 50))
        screen.blit(text, (text_x1, text_y1))
        screen.blit(enter_text, (enter_text_x, enter_text_y))
        pygame.display.flip()
        screen.fill('black')


def level_up():
    global health_gain, strength_gain, speed_gain
    if lvl in [2, 3, 4, 5]:
        health_gain += 20
    if lvl in [6, 7, 8, 9]:
        strength_gain += 2
    if lvl in [10, 12]:
        speed_gain += 1
    for enem in enemies:
        enem.HP += health_gain
        enem.damage += strength_gain
        enem.speed += speed_gain


class Potion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, potions)
        image = pygame.image.load('pictures/potion.tiff')
        self.image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.HP_up = random.randint(10, 40)


start_end_screen(screen, False)
door = Door(random.randint(200, 1240), 0)
chel = Character(300, 300)
game(fullscreen_mode, screen)
start_end_screen(screen, True)
