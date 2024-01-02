import pygame
import sys

pygame.init()
all_sprites = pygame.sprite.Group()
info = pygame.display.Info()
size = width, height = 0.8 * info.current_w, 0.8 * info.current_h
screen = pygame.display.set_mode(size)
pygame.display.set_caption("KINGDOM: A CHILDHOOD DREAM BUT IT IS REALISTIC")
clock = pygame.time.Clock()


class Character(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        first_pos = pygame.image.load('pictures/1pos.tiff')
        self.image = pygame.transform.scale(
            first_pos, (first_pos.get_width() * 4,
                        first_pos.get_height() * 4))
        self.frames_for_right = [pygame.image.load('pictures/go_right6.tiff'),
                                 pygame.image.load('pictures/go_right1.tiff'),
                                 pygame.image.load('pictures/go_right6.tiff'),
                                 pygame.image.load('pictures/go_right4.tiff')]
        self.cur_frame = 0
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_right)
        image = self.frames_for_right[self.cur_frame]
        self.image = pygame.transform.scale(
            image, (image.get_width() * 4,
                    image.get_height() * 4))

    def move(self, where):
        if where == 'up':
            if self.pos_y > 35:
                self.pos_y -= speed
        if where == 'down':
            if self.pos_y < height - self.image.get_height() - 16:
                self.pos_y += speed
        if where == 'left':
            if self.pos_x > 16:
                self.pos_x -= speed
        if where == 'right':
            if self.pos_x < width - self.image.get_width() - 16:
                self.pos_x += speed
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_for_right)
                image = self.frames_for_right[self.cur_frame]
                clock.tick(10)
                self.image = pygame.transform.scale(
                    image, (image.get_width() * 4,
                            image.get_height() * 4))
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["KINGDOM: A CHILDHOOD DREAM BUT IT IS REALISTIC",
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
image = pygame.image.load('pictures/background.png')
background = pygame.transform.scale(image, (width, height))
fullscreen_mode = False
speed = 5
to_right, to_left, to_up, to_down = False, False, False, False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                to_left = True
            if event.key == pygame.K_d:
                to_right = True
            if event.key == pygame.K_s:
                to_down = True
            if event.key == pygame.K_w:
                to_up = True
            if event.key == pygame.K_f:
                fullscreen_mode = not fullscreen_mode
                if fullscreen_mode:
                    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(size)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                to_left = False
            if event.key == pygame.K_d:
                to_right = False
            if event.key == pygame.K_s:
                to_down = False
            if event.key == pygame.K_w:
                to_up = False
    if to_right:
        chel.move('right')
    if to_left:
        chel.move('left')
    if to_down:
        chel.move('down')
    if to_up:
        chel.move('up')
    screen.fill((255, 255, 255))
    pygame.time.delay(20)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.update()
