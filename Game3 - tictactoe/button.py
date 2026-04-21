import pygame
pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Button Example")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)

# Button setup
button_rect = pygame.Rect(200, 150, 200, 60)
font = pygame.font.SysFont(None, 40)

running = True
while running:
    screen.fill(WHITE)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # Change color on hover
    if button_rect.collidepoint(mouse_pos):
        color = LIGHT_BLUE

        # Click detection
        if mouse_pressed[0]:  # Left mouse button
            print("Button clicked")
    else:
        color = BLUE

    # Draw button
    pygame.draw.rect(screen, color, button_rect)

    # Draw text
    text = font.render("Click Me", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()