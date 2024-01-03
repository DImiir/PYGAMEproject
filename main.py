import pygame
import sys

pygame.init()
all_sprites = pygame.sprite.Group()
info = pygame.display.Info()
size = width, height = 0.8 * info.current_w, 0.8 * info.current_h
screen = pygame.display.set_mode(size)
pygame.display.set_caption("KINGDOM: A CHILDHOOD DREAM BUT IT IS MORE REALISTIC")
clock = pygame.time.Clock()


class Character(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        first_pos = pygame.image.load('pictures/character/1pos.tiff')
        self.image = pygame.transform.scale(
            first_pos, (first_pos.get_width() * 4,
                        first_pos.get_height() * 4))
        self.frames_for_right = [pygame.image.load('pictures/character/go_right2.tiff'),
                                 pygame.image.load('pictures/character/go_right1.tiff'),
                                 pygame.image.load('pictures/character/go_right2.tiff'),
                                 pygame.image.load('pictures/character/go_right3.tiff')]
        self.frames_for_left = [pygame.transform.flip(im, True, False) for im in self.frames_for_right]
        self.frames_for_up = [pygame.image.load('pictures/character/go_back1.tiff'),
                              pygame.image.load('pictures/character/go_back2.tiff'),
                              pygame.image.load('pictures/character/go_back3.tiff')]
        self.right = True
        self.cur_frame = 0
        self.speed = 10
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def move(self, where):
        if where == 'up':
            if self.pos_y > 35:
                self.pos_y -= self.speed
        if where == 'down':
            if self.pos_y < height - self.image.get_height() - 16:
                self.pos_y += self.speed
        if where == 'left':
            if self.pos_x > 16:
                self.pos_x -= self.speed
        if where == 'right':
            if self.pos_x < width - self.image.get_width() - 16:
                self.pos_x += self.speed
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def update(self):
        if to_up1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_up)
            image = self.frames_for_up[self.cur_frame]
            pygame.time.delay(10)
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
        elif to_down1:
            if self.right:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_right)
                image = self.frames_for_right[self.cur_frame]
                pygame.time.delay(10)
                self.image = pygame.transform.scale(
                    image, (image.get_width() * 4,
                            image.get_height() * 4))
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_left)
                image = self.frames_for_left[self.cur_frame]
                pygame.time.delay(10)
                self.image = pygame.transform.scale(
                    image, (image.get_width() * 4,
                            image.get_height() * 4))
        elif to_left1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_left)
            image = self.frames_for_left[self.cur_frame]
            pygame.time.delay(10)
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
            self.right = False
        elif to_right1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_right)
            image = self.frames_for_right[self.cur_frame]
            pygame.time.delay(10)
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
            self.right = True


class Attack(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, movement):
        super().__init__(all_sprites)
        first_pos = pygame.image.load('pictures/gold_attack/gold1.tiff')
        self.image = pygame.transform.scale(
            first_pos, (first_pos.get_width() * 4,
                        first_pos.get_height() * 4))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.cur_frame = 0
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

    def move(self):
        if self.movement == 'up':
            if self.pos_y > 20:
                self.pos_y -= self.speed
        if self.movement == 'down':
            if self.pos_y < height - self.image.get_height() - 20:
                self.pos_y += self.speed
        if self.movement == 'left':
            if self.pos_x > 20:
                self.pos_x -= self.speed
        if self.movement == 'right':
            if self.pos_x < width - self.image.get_width() - 20:
                self.pos_x += self.speed
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def update(self):
        if self.movement == 'up':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_up)
            image = self.frames_for_up[self.cur_frame]
            pygame.time.delay(10)
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
        elif self.movement == 'down':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_down)
            image = self.frames_for_right[self.cur_frame]
            pygame.time.delay(10)
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
        elif self.movement == 'left':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_left)
            image = self.frames_for_left[self.cur_frame]
            pygame.time.delay(10)
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))
        elif self.movement == 'right':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_right)
            image = self.frames_for_right[self.cur_frame]
            pygame.time.delay(10)
            self.image = pygame.transform.scale(
                image, (image.get_width() * 4,
                        image.get_height() * 4))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["KINGDOM: A CHILDHOOD DREAM BUT IT IS MORE REALISTIC",
                  "",
                  "НАЖМИТЕ ЧТО-НИБУДЬ",
                  "ЧТОБЫ НАЧАТЬ"]
    image = pygame.image.load('pictures/second.tiff')
    fon = pygame.transform.scale(image, (image.get_width(), image.get_height()))
    screen.blit(fon, (0, 0))
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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)


start_screen()
chel = Character(100, 100)
attacks = []
image = pygame.image.load('pictures/background.png')
background = pygame.transform.scale(image, (width, height))
fullscreen_mode = False
to_right1, to_left1, to_up1, to_down1 = False, False, False, False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
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
                attack = Attack(chel.pos_x - 10, chel.pos_y, 'left')
                attacks.append(attack)
            if event.key == pygame.K_RIGHT:
                attack = Attack(chel.pos_x + 10, chel.pos_y, 'right')
                attacks.append(attack)
            if event.key == pygame.K_DOWN:
                attack = Attack(chel.pos_x, chel.pos_y + 10, 'down')
                attacks.append(attack)
            if event.key == pygame.K_UP:
                attack = Attack(chel.pos_x, chel.pos_y - 10, 'up')
                attacks.append(attack)
            if event.key == pygame.K_f:
                fullscreen_mode = not fullscreen_mode
                if fullscreen_mode:
                    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(size)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                to_left1 = False
            if event.key == pygame.K_d:
                to_right1 = False
            if event.key == pygame.K_s:
                to_down1 = False
            if event.key == pygame.K_w:
                to_up1 = False
    if to_right1:
        chel.move('right')
    if to_left1:
        chel.move('left')
    if to_down1:
        chel.move('down')
    if to_up1:
        chel.move('up')
    if attacks:
        for num, atk in enumerate(attacks):
            atk.move()
            if atk.pos_x <= 20:
                attacks.pop(num)
            if atk.pos_x >= width - atk.image.get_width() - 20:
                attacks.pop(num)
            if atk.pos_y <= 40:
                attacks.pop(num)
            if atk.pos_y >= height - atk.image.get_height() - 20:
                attacks.pop(num)
    screen.fill((255, 255, 255))
    pygame.time.delay(20)
    screen.blit(background, (0, 0))
    chel.update()
    all_sprites.draw(screen)
    pygame.display.update()
