import pygame
import os

pygame.init()

base_path = os.path.dirname(__file__)
image_path = os.path.join(base_path, 'Sprites', '1.jpg')

# creates screen with the set size
screen = pygame.display.set_mode((640, 640))

#auto scalingscreen
# screen = pygame.display.set_mode((320, 320), pygame.SCALED)

# loads image plus converts it
random_image = pygame.image.load(image_path).convert()

# With Alpha layer you can convert like this to keep the alpha
# random_image = pygame.image.load(image_path).convert_alpha()

# Scale image
random_image = pygame.transform.scale(random_image,(random_image.get_width() / 3, random_image.get_height() / 3))

#creates image cluster
cluster = pygame.Surface((64,64), pygame.SRCALPHA)
cluster.blit(random_image, (0, 0))
cluster.blit(random_image, (20, 0))
cluster.blit(random_image, (10, 10))


# removes black
random_image.set_colorkey((0,0,0))

# creates the update clock
clock = pygame.time.Clock()

# starting cords
x = 30
y = 0

alpha = 0

delta_time = 0.1

running = True
while running:

    screen.fill((255,255,255))
    
    # it draws the image onto the screen (screen.blit(cluster, (x, y)))
    screen.blit(random_image, (x , y))

    # tranceparancy changer
    random_image.set_alpha(max(0, 255 - x))

    # moves image +1 x
    x += 50 * delta_time

    # Exit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # render the screen
    pygame.display.flip()

    # Limits the game clock
    # Delta time ensures movement stays consistent regardless of frame rate (lag)
    delta_time = clock.tick(24) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

# closes the game
pygame.quit()