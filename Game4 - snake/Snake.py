import pygame
import os
import random
import time

pygame.init()
pygame.font.init()

sprite_path = os.path.join(os.path.dirname(__file__), 'sprites')
my_font = pygame.font.SysFont('arial', 30)

snake_sprite = pygame.image.load(os.path.join(sprite_path, 'snake-sprite.png'))
snake_tail_sprite = pygame.image.load(os.path.join(sprite_path, 'snake-tail-sprite.png'))
apple_sprite = pygame.image.load(os.path.join(sprite_path, 'apple.png'))

screen_ratio = 640, 640
bg = (25, 25, 25)

clock = pygame.time.Clock()
fps = 24

start_button_state, option_button_state, quit_button_state = 0,0,0
mouse_pos = (0,0)

screen = pygame.display.set_mode(screen_ratio)

CORNER_SPRITE_X = 5

settings = {
    'wall_clip': False,
    'god_mode9': False,
    'apple_count': 1
}

def reset():
    global grow, grow_flag, defeat
    global move_timer, move_delay, starting_length, length, tile
    global game_boarder_size, rotate_angle, move_dir
    global si, sih, sit, snake, game_size, apples, settings

    grow = False
    grow_flag = False
    defeat = False

    move_timer = 0
    move_delay = 200

    starting_length = 4
    length = starting_length
    tile = 32

    game_boarder_size = tile * 1

    rotate_angle = 0
    move_delay = 200
    move_dir = 'right'

    si = 0
    sih = 0
    sit = 0

    snake = [(320 - i * tile, 320) for i in range(length)]

    game_size = {
        'X_H' : screen_ratio[0] - game_boarder_size * 2,
        'X_L' : game_boarder_size,
        'Y_H' : screen_ratio[1] - game_boarder_size * 2,
        'Y_L' : game_boarder_size
    }

    apples = []

reset()

def menu():
    global start_rect, options_rect, quit_rect

    start_button = menu_button_sprite.get_sprite(320 * start_button_state, 64, 320, 64)
    start_rect = start_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
    screen.blit(start_button, start_rect)

    options_button = menu_button_sprite.get_sprite(320 * option_button_state, 64 * 2, 320, 64)
    options_rect = options_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2.25))
    screen.blit(options_button, options_rect)

    quit_button = menu_button_sprite.get_sprite(320 * quit_button_state, 64 * 3, 320, 64)
    quit_rect = quit_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 1.25))
    screen.blit(quit_button, quit_rect)

class spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

def apple_spawn():
    global apples, apple_x, apple_y

    while True:
        apple_x = random.randint(grid_x_min, grid_x_max) * tile
        apple_y = random.randint(grid_y_min, grid_y_max) * tile

        if (apple_x, apple_y) not in apples and (apple_x, apple_y) not in snake:
            apples.insert(0, (apple_x, apple_y))
            break



def move(grow=False):
    global rotate_angle, snake, grow_flag, length, defeat, sih
    grow_flag = False

    head_x, head_y = snake[0]

    if move_dir == 'up':
        head_y -= tile
        rotate_angle = 90
    elif move_dir == 'down':
        head_y += tile
        rotate_angle = 270
    elif move_dir == 'left':
        head_x -= tile
        rotate_angle = 180
    elif move_dir == 'right':
        head_x += tile
        rotate_angle = 0

    if settings['wall_clip'] or settings['god_mode9']:
        if head_x < game_size['X_L']:
            head_x = game_size['X_H']
        if head_x > game_size['X_H']:
            head_x = game_size['X_L']

        if head_y < game_size['Y_L']:
            head_y = game_size['Y_H']
        if head_y > game_size['Y_H']:
            head_y = game_size['Y_L']

    else:
        if head_x < game_size['X_L']:
            defeat = True
        if head_x > game_size['X_H']:
            defeat = True

        if head_y < game_size['Y_L']:
            defeat = True
        if head_y > game_size['Y_H']:
            defeat = True

    if not settings['god_mode9']:
        if (head_x, head_y) in snake[:-1]:
            snake.insert(0, (head_x, head_y))
            defeat = True
        else:
            snake.insert(0, (head_x, head_y))
    else:
        snake.insert(0, (head_x, head_y))

    if (head_x, head_y) in apples:
        grow = True
        apples.remove((head_x, head_y))

    if not grow:
        snake.pop()
        grow = False
    elif grow:
        length += 1

def get_angle(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    if dx > 0:
        return 180
    elif dx < 0:
        return 0
    elif dy > 0:
        return 90
    else:
        return 270

def blit_rotated(surface, sprite, pos, angle):
    rotated = pygame.transform.rotate(sprite, angle)
    offset_x = (rotated.get_width() - sprite.get_width()) // 2
    offset_y = (rotated.get_height() - sprite.get_height()) // 2
    surface.blit(rotated, (pos[0] - offset_x, pos[1] - offset_y))

def get_segment_type(prev_pos, curr_pos, next_pos):
    dx_in = curr_pos[0] - prev_pos[0]
    dy_in = curr_pos[1] - prev_pos[1]
    
    dx_out = next_pos[0] - curr_pos[0]
    dy_out = next_pos[1] - curr_pos[1]

    def norm(v): return 0 if v == 0 else (1 if v > 0 else -1)
    key = (norm(dx_in), norm(dy_in), norm(dx_out), norm(dy_out))

    if dx_in == dx_out and dy_in == dy_out:
        return ('straight', get_angle(prev_pos, curr_pos))

    corner_angles = {
    #Counter Clock wise
        ( 0,  1, -1,  0): 90, # right - up
        ( 1,  0,  0,  1): 180, # up - left
        ( 0, -1,  1,  0): 270, # left - down
        (-1,  0,  0, -1): 0, # down - right
    #Clock wise
        ( 0, -1, -1,  0): 180, # right - down
        ( 1,  0,  0, -1): 90, # down - left
        ( 0,  1,  1,  0): 0, # left - up
        (-1,  0,  0,  1): 270, # up - right
    }

    angle = corner_angles.get(key, 0)

    return ('corner', angle)

snake_head_sprite = spritesheet(os.path.join(sprite_path, 'snake-sprite.png'))
snake_tail_sprite = spritesheet(os.path.join(sprite_path, 'snake-tail-sprite.png'))

menu_button_sprite = spritesheet(os.path.join(sprite_path, 'buttons.png'))

run = True
running_game = False
while run:
    grid_x_min = game_size['X_L'] // tile
    grid_x_max = game_size['X_H'] // tile
    grid_y_min = game_size['Y_L'] // tile
    grid_y_max = game_size['Y_H'] // tile

    screen.fill(bg)

    if running_game:
        dt = clock.tick(fps)

        text_surface = my_font.render(f'score: {length - starting_length}', False, (255, 255, 255))
        screen.blit(text_surface, (0,0))

        if not settings['apple_count'] <= len(apples):
            apple_spawn()

        for apple in apples:
            screen.blit(apple_sprite,(apple))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_game = False

                elif event.key == pygame.K_UP:
                    if not move_dir == 'down':
                        move_dir = 'up'
                elif event.key == pygame.K_DOWN:
                    if not move_dir == 'up':
                        move_dir = 'down'
                if event.key == pygame.K_LEFT:
                    if not move_dir == 'right':
                        move_dir = 'left'
                elif event.key == pygame.K_RIGHT:
                    if not move_dir == 'left':
                        move_dir = 'right'

                elif event.key == pygame.K_0:
                    grow_flag = True

                elif event.key == pygame.K_1:
                    if settings['wall_clip']:
                        settings['wall_clip'] = False
                        print(f'Wall Clip {settings['wall_clip']}')
                    else:
                        settings['wall_clip'] = True
                        print(f'Wall Clip {settings['wall_clip']}')

                elif event.key == pygame.K_2:
                    if settings['god_mode9']:
                        settings['god_mode9'] = False
                        print(f'God Mode {settings['god_mode9']}')
                    else:
                        settings['god_mode9'] = True
                        print(f'God Mode {settings['god_mode9']}')

        for i, pos in enumerate(snake):
            if i == 0:
                snake_head = snake_head_sprite.get_sprite(32 * sih, 0, 32, 32)
                blit_rotated(screen, snake_head, pos, rotate_angle)
        
            elif i == length - 1:
                sit = (si % 3) + 6
                snake_tail = snake_tail_sprite.get_sprite(32 * sit, 0, 32, 32)
                angle = get_angle(snake[i - 1], snake[i])
                blit_rotated(screen, snake_tail, pos, angle + 180)
        
            else:
                seg_type, angle = get_segment_type(snake[i - 1], snake[i], snake[i + 1])
                if seg_type == 'corner':
                    corner_sprite = snake_tail_sprite.get_sprite(32 * CORNER_SPRITE_X, 0, 32, 32)
                    blit_rotated(screen, corner_sprite, pos, angle)
                else:
                    sit = (i + si) % 5
                    snake_tail = snake_tail_sprite.get_sprite(32 * sit, 0, 32, 32)
                    blit_rotated(screen, snake_tail, pos, angle)

        move_timer += dt

        if move_timer >= move_delay:
            si += 1
            sih = (sih+1)%7
            move(grow_flag)
            move_timer = 0

    else:
        reset()
        menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running_game = True
                if event.key == pygame.K_ESCAPE:
                    running_game = True
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

        if start_rect.collidepoint(mouse_pos):
            start_button_state = 1
            mouse_pos = (0,0)
            running_game = True
            time.sleep(0.5)
            start_button_state = 0

        elif options_rect.collidepoint(mouse_pos):
            print('options')
            option_button_state = 1
            mouse_pos = (0,0)
            time.sleep(0.5)
            option_button_state = 0

        elif quit_rect.collidepoint(mouse_pos):
            quit_button_state = 1
            mouse_pos = (0,0)
            run = False
            time.sleep(0.5)
            quit_button_state = 0
    
    if defeat:
        running_game = False
    pygame.display.flip()

pygame.QUIT
