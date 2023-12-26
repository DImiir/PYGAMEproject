import pygame

# class Character(pygame.sprite.Sprite):
#   def __init__(self):
#       super().__init__()
#       self.first_pos = pygame.image.load(image)
#       self.first_pos = pygame.transform.scale(
#           self.first_pos, (self.first_pos.get_width() * 4,
#                            self.first_pos.get_height() * 4))
#       self.rect = self.first_pos.get_rect()
#       self.rect.center = (x, y)


width, height = 1000, 700
x, y = 100, 100
chel = pygame.image.load('pictures/1pos.tiff')
chel = pygame.transform.scale(
    chel, (chel.get_width() * 4,
           chel.get_height() * 4))
# all_sprites = pygame.sprite.Group()
# list_of_pictures = ['1pos', 'go_right1', 'go_right2', 'go_right3']
# for _ in range(len(list_of_pictures)):
#   image = f'pictures/{list_of_pictures[_]}.tiff'
#   character = Character()
#   all_sprites.add(character)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("KINGDOM")
speed = 5
running = True
to_right, to_left, to_up, to_down = False, False, False, False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                to_left = True
            if event.key == pygame.K_d:
                to_right = True
            if event.key == pygame.K_s:
                to_down = True
            if event.key == pygame.K_w:
                to_up = True
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
        x += speed
    if to_left:
        x -= speed
    if to_down:
        y += speed
    if to_up:
        y -= speed
    screen.fill((255, 255, 255))
    pygame.time.delay(20)
    screen.blit(chel, (x, y))
    pygame.display.update()
pygame.quit()
