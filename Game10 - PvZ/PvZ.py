import pygame_gui
import os, sys
import pygame
import json
import time
from typing import (
    Any,
    Optional,
    Union,
    Callable,
    Iterable,
    Generator,
    TypeVar,
    Protocol,
    Literal,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from general_scripts.Save_Load import SaveLoad
from general_scripts.Helpers import console
from general_scripts.ANSI import ANSI

class GameLevel():
    def __init__(self, screen, current_level=0) -> None:
        self.current_level = current_level
        self.Clock = pygame.time.Clock()
        self.FPS = 24
        self.BGC = (25, 25, 25)
        self.screen = screen

        self.running = True

        self.sun_count: int = 50
        self.wave_progress: float = 0
        self.zombie_count: int = 0
        self.zombie_pos: int = 0
        self.current_lawn: str = "roof"
        self.planting: bool = True
        self.planting_location: tuple[int, int] = (-1, -1)

        self.lawn_size: dict[str, tuple[int, int]] = {
            "normal": (5, 9),
            "night": (5, 9),
            "pool": (6, 9),
            "fog": (6, 9),
            "roof": (5, 9)
        }

        self.lawn_properties: dict[str, dict] = {
            "normal": {"night": False, "watered_rows": (), "tilted_cols": (), "tile_skin": "grass"},
            "night": {"night": True, "watered_rows": (), "tilted_cols": (), "tile_skin": "grass"},
            "pool": {"night": False, "watered_rows": (2, 3), "tilted_cols": (), "tile_skin": "grass"},
            "fog": {"night": True, "watered_rows": (2, 3), "tilted_cols": (), "tile_skin": "grass"},
            "roof": {"night": False, "watered_rows": (), "tilted_cols": (1, 2), "tile_skin": "roof"},
        }

        self.game_lawn: dict = {}

        self.active_seeds: dict[str, Optional[int]] = {
            "seedslot0": None,
            "seedslot1": None,
            "seedslot2": None,
            "seedslot3": None,
            "seedslot4": None,
            "seedslot5": None,
            "seedslot6": None,
            "seedslot7": None,
            "seedslot8": None,
            "seedslot9": None,
        }

        self.rows, self.cols = self.lawn_size[self.current_lawn]

        self.margin_x = 60
        self.margin_y = 80
        avail_w = self.screen.get_width() - self.margin_x * 2
        avail_h = self.screen.get_height() - self.margin_y * 2
        tile_w = avail_w // self.cols
        tile_h = avail_h // self.rows
        self.cell_size = (min(tile_w, tile_h), min(tile_w, tile_h))
        grid_w = self.cols * self.cell_size[0]
        grid_h = self.rows * self.cell_size[1]
        self.lawn_offset = (
            (self.screen.get_width() - grid_w) // 2,
            (self.screen.get_height() - grid_h) // 2 + 20
        )

        self.ConstructBoard()
    
    def ConstructBoard(self):
        lawn = []

        rows, cols = self.lawn_size[self.current_lawn]

        night = self.lawn_properties[self.current_lawn]["night"]
        watered_rows = self.lawn_properties[self.current_lawn]["watered_rows"]
        tilted_cols = self.lawn_properties[self.current_lawn]["tilted_cols"]
        tile_skin = self.lawn_properties[self.current_lawn]["tile_skin"]

        for r in range(rows):
            row = []
            for c in range(cols):
                if r in watered_rows:
                    if c in tilted_cols:
                        row.append(((c, r), "water", "tilted", "empty"))
                    else:
                        row.append(((c, r), "water", "", "empty"))
                else:
                    if c in tilted_cols:
                        row.append(((c, r), tile_skin, "tilted", "empty"))
                    else:
                        row.append(((c, r), tile_skin, "", "empty"))
                    
            
            
            lawn.append(row)
        
        self.game_lawn = {"Game_Grid": lawn, "night": night}
    
    def clamp(self, v):
        return max(0, min(255, v))

    def draw_lawn(self):
        grid = self.game_lawn["Game_Grid"]
        night = self.game_lawn["night"]

        for row in grid:
            for cell in row:
                (c, r), tile, *_ = cell

                x = self.lawn_offset[0] + c * self.cell_size[0]
                y = self.lawn_offset[1] + r * self.cell_size[1]

                base_color = None

                if tile == "grass":
                    base_color = (60, 180, 75)
                elif tile == "water":
                    base_color = (50, 120, 200)
                elif tile == "roof":
                    base_color = (164, 74, 74)
                else:
                    base_color = (120, 120, 120)

                
                #!^ variation construction
                if (c + r) % 2 == 0:
                    color = base_color
                else:
                    color = tuple(self.clamp(v - 10) for v in base_color)

                #!^ night mode
                if night:
                    color = tuple(self.clamp(v - 50) for v in color)
                
                if c == self.planting_location[0] or r == self.planting_location[1]:
                    color = tuple(self.clamp(v + 25) for v in color)

                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        x,
                        y,
                        self.cell_size[0],
                        self.cell_size[1]
                    )
                )
    

    def draw_zombies(self):
        pass

    def draw_plants(self):
        pass
        

    def loop(self, current_level):
        self.current_level: int = current_level


        while self.running:
            dt = self.Clock.tick(self.FPS)
            self.screen.fill(self.BGC)
            result = self.check_events()

            if result:
                return result

            self.draw_lawn()
            self.draw_plants()
            self.draw_zombies()


            pygame.display.flip()

    def check_events(self) -> str:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit_game"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.K_LCTRL:
                    return "exit_game"
                
                if event.key == pygame.K_ESCAPE:
                    return "exit_level"
                
                if event.key == pygame.K_p:
                    self.planting = not self.planting
            if self.planting:
                mx, my = pygame.mouse.get_pos()

                grid_x = (mx - self.lawn_offset[0]) // self.cell_size[0]
                grid_y = (my - self.lawn_offset[1]) // self.cell_size[1]

                if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
                    self.planting_location = (grid_x, grid_y)
                else:
                    self.planting_location = (-1, -1)

        return ""

class GameMenu():
    def __init__(self) -> None:
        SCREEN_RATIO = (640, 640)
        self.screen = pygame.display.set_mode(SCREEN_RATIO)
        pygame.display.set_caption("PvZ But Sceer")

        self.running = True
        self.running_level = False

        self.unlocked_seeds: int = 1
        self.current_level: int = 0
        self.coint_count: int = 0
        self.BGC: tuple = (25,25,25)
        self.Clock = pygame.time.Clock()
        self.FPS: int = 24

        self.statistics: dict[str, float]  = {

        }
        self.upgrades: dict[str, float]  = {

        }

        self.RunLevel = GameLevel(self.screen)

    def loop(self):
        while self.running:
            dt = self.Clock.tick(self.FPS)
            self.screen.fill(self.BGC)

            if self.running_level:
                result = self.RunLevel.loop(self.current_level)
            else:
                result = self.check_events()
            
            if result == "exit_game":
                self.running = False
            
            elif result == "exit_level":
                self.running_level = False
                continue

            pygame.display.flip()

        pygame.quit()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit_game"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.K_LCTRL:
                    return "exit_game"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.running_level = not self.running_level


class StartGame():
    def __init__(self) -> None:
        self.menu = GameMenu()


    def LoadSave(self):
        self.menu.loop()
        key = SaveLoad.generate_key_from_string("PvZ_Skeered")
        config = SaveLoad.get_save_path(name="config", folder_type="Configs")
        save = SaveLoad.get_save_path(name="save", folder_type="Saves")
        statistics = SaveLoad.get_save_path(name="statistics", folder_type="Statistics")
        self.config = SaveLoad.load(config)
        self.save = SaveLoad.load(save, key=key, encrypted=True, log=True)
        self.statistics = SaveLoad.load(statistics, key=key, encrypted=True, log=True)


def main():
    start = StartGame()
    start.LoadSave()


if __name__ == "__main__":
    main()