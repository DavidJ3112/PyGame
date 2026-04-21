import pygame
import os

pygame.init()
screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()

sprite1 = os.path.join(os.path.dirname(__file__), 'Sprites', '1.jpeg')
sprite1 = pygame.image.load(sprite1)

sprite1 = pygame.transform.scale(sprite1,(sprite1.get_width() / 3, sprite1.get_height() / 3))

x = 0
y = 0

speed = 5

delta_time = 0.1

running = True
while running:
    screen.fill((255,255,255))
    screen.blit(sprite1, (x, y))
    pygame.display.flip()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_SPACE]:
        x = 0
        y = 0

    if keys[pygame.K_ESCAPE]:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta_time = max(0.001, min(0.1, clock.tick(24) / 1000))

pygame.quit