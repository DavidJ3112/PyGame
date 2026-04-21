# game reset
# start screen turn indicator

# Basic Setup
import os
import pygame

pygame.init()
screen = pygame.display.set_mode((672, 672))
clock = pygame.time.Clock()
running = True


# Sprite Library
sprite_path = os.path.join(os.path.dirname(__file__), 'sprites')

map_sprite = pygame.image.load(os.path.join(sprite_path, 'map.png')).convert_alpha()
x_sprite = pygame.image.load(os.path.join(sprite_path, 'sprite-x.png')).convert_alpha()
o_sprite = pygame.image.load(os.path.join(sprite_path, 'sprite-o.png')).convert_alpha()


turn_cycle = 'x'
move = False

# Map Data
map_cell_size = 224
game_cell_size = 224


# Game field Table construction
game_field = [
    [{'state': 0} for _ in range(3)]
    for _ in range(3)
]

winning_lines = [
    # Rows
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],

    # Columns
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],

    # Diagonals
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]


# Draw's the board
def draw_board():
    for row in range(3):
        for col in range(3):
            x = col * map_cell_size
            y = row * map_cell_size
            screen.blit(map_sprite, (x, y))


# Draw's the pieces
def draw_pieces():
    for row in range(3):
        for col in range(3):
            x = 16 + col * game_cell_size
            y = 16 + row * game_cell_size

            state = game_field[row][col]['state']

            if state == 1:
                screen.blit(x_sprite, (x, y))
            elif state == -1:
                screen.blit(o_sprite, (x, y))

# Checks the win
def check_win():
    for line in winning_lines:
        values = [game_field[r][c]['state'] for r, c in line]
        if values == [1, 1, 1]:
            return 'x'
        elif values == [-1, -1, -1]:
            return 'o'

while running:

# Screen construction
    screen.fill((255,255,255))
    draw_board()
    draw_pieces()

# Runs win check
    winning = check_win()
    if winning:
        print(f'{winning} Wins')
        # running = False


# User Key Activational
    keys = pygame.key.get_pressed()


# keypad control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            c = mouse_x // map_cell_size
            r = mouse_y // map_cell_size

            move = True
            print(f'click C: {c} R: {r}')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_KP0:
                for row in game_field:
                    print(' | '.join(str(cell['state']) for cell in row))
                print()

            else:
                continue

    if move:
        if game_field[r][c]['state'] == 0:
            if turn_cycle == 'x':
                game_field[r][c]['state'] = 1
                turn_cycle = 'o'
                move = False
                draw_pieces()

            elif turn_cycle == 'o':
                game_field[r][c]['state'] = -1
                turn_cycle = 'x'
                move = False
                draw_pieces()

    pygame.display.flip()
    delta_time = max(0.001, min(0.1, clock.tick(24) / 1000))

pygame.quit