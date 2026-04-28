import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI
import pygame
import random
pygame.font.init()


class GameOfLife:
    def __init__(self):
        self.debug = {'enabled': True, 'log_level': 'none'}

        self.grid_size = (16, 16)

        self.game_field = [
            [{'alive': False} for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])
        ]

        self.cells_required_to_birth = (3,)
        self.cells_required_to_survive = (2,3)
        self.cells_required_to_die = (0,1,4,5,6,7,8)
        self.running = True

        self.screen_ratios = (640, 640)
        self.screen = pygame.display.set_mode(self.screen_ratios)
        pygame.display.set_caption("Game of Life")
        self.BGCOLOR = (50, 50, 50)

        self.font = pygame.font.SysFont('arial', 20)

        self.cell_size = self.screen_ratios[0] // len(self.game_field)
        self.fps = 24
        self.clock = pygame.time.Clock()

        self.randomize_field(0.2)

        self.prev_grid_x = -1
        self.prev_grid_y = -1

    def randomize_field(self, alive_probability):
        width, height = self.grid_size
        cells_to_live = []

        if alive_probability >= 1.0:
            cells_to_live = [
                (x, y)
                for x in range(width)
                for y in range(height)
            ]
        else:
            total = int(width * height * alive_probability)
            cells_to_live = set()

            while len(cells_to_live) < total:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                cells_to_live.add((x, y))

        for x in range(width):
            for y in range(height):
                self.game_field[x][y]['alive'] = False

        for x, y in cells_to_live:
            self.game_field[x][y]['alive'] = True


    def display(self):
        for x, row in enumerate(self.game_field):
            for y, cell in enumerate(row):
                color = (255, 255, 255) if cell['alive'] else (0, 0, 0)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                )
    
    def count_alive_neighbors(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1),  (1, 0),  (1, 1)]
        count = 0

        for dx, dy in directions:
            check_x, check_y = x + dx, y + dy
            if 0 <= check_x < len(self.game_field) and 0 <= check_y < len(self.game_field[0]):
                if self.game_field[check_x][check_y]['alive']:
                    count += 1
        return count

    def update(self):
        new_field = [[cell.copy() for cell in row] for row in self.game_field]

        for x in range(len(self.game_field)):
            for y in range(len(self.game_field[0])):
                alive_neighbors = self.count_alive_neighbors(x, y)

                if self.game_field[x][y]['alive']:
                    new_field[x][y]['alive'] = (
                        alive_neighbors in self.cells_required_to_survive
                    )
                else:
                    new_field[x][y]['alive'] = (
                        alive_neighbors in self.cells_required_to_birth
                    )

        self.game_field = new_field

    def render(self):
        self.screen.fill(self.BGCOLOR)
        self.display()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  #note Left click
                    self.prev_grid_x, self.prev_grid_y = -1, -1

            if mouse_buttons := pygame.mouse.get_pressed():
                if mouse_buttons[2]: #note Right click
                    self.game_field = [
                        [{'alive': False} for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])
                    ]

                if mouse_buttons[0]:  #note Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    grid_x = mouse_y // self.cell_size
                    grid_y = mouse_x // self.cell_size

                    if (grid_x, grid_y) == (self.prev_grid_x, self.prev_grid_y):
                        self.debug_log("info", f"{ANSI.BRIGHT_YELLOW}Already toggled cell: {grid_x, grid_y}{ANSI.RESET}")
                        return

                    self.prev_grid_x, self.prev_grid_y = grid_x, grid_y

                    self.debug_log("info", f"{ANSI.BRIGHT_GREEN}Clicked on cell: {grid_x, grid_y}{ANSI.RESET}")

                    if 0 <= grid_x < self.grid_size[0] and 0 <= grid_y < self.grid_size[1]:
                        self.game_field[grid_x][grid_y]['alive'] = not self.game_field[grid_x][grid_y]['alive']

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.randomize_field(0.2)

                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.running = False

                if event.key == pygame.K_UP:
                    self.update_interval = max(0.05, self.update_interval - 0.05)
                if event.key == pygame.K_DOWN:
                    self.update_interval = min(10, self.update_interval + 0.05)
                if event.key == pygame.K_SPACE and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self.update()
                if event.key == pygame.K_SPACE and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if self.update_interval <= 10:
                        self.update_interval = 100
                    else:
                        self.update_interval = 1
            
            self.debug_log("all", f"{ANSI.BRIGHT_MAGENTA}Handled event: {event}{ANSI.RESET}")
    
        self.debug_log("all", f"{ANSI.BRIGHT_CYAN}Current update interval: {self.update_interval:.2f}s{ANSI.RESET}")

    def loop(self):
        self.update_interval = 100
        accumulator = 0.0

        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            accumulator += dt

            self.handle_events()
            
            if self.update_interval <= 10:
                while accumulator >= self.update_interval:
                    self.update()
                    accumulator -= self.update_interval

            self.render()
            font_text = self.font.render(f"Update Interval: {self.update_interval:.2f}s", True, (0, 255, 255))
            self.screen.blit(font_text, (10, 10))
            pygame.display.flip()

    def debug_log(self, level, msg):
        if not self.debug["enabled"]:
            return
        if self.debug["log_level"] in ("all", level):
            print(msg)

if __name__ == "__main__":
    game = GameOfLife()
    game.loop()