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


class GameLevel:
    def __init__(self, screen, config, save_data, statistics) -> None:
        self.config = config
        self.save_data = save_data
        self.statistics = statistics

        self.current_level = 1
        self.Clock = pygame.time.Clock()
        self.FPS: int = 24
        self.BGC: tuple[int, int, int] = (25, 25, 25)
        self.screen = screen

        self.running = True

        self.sun_count: int = 50
        self.wave_progress: float = 0
        self.zombie_count: int = 0
        self.zombie_pos: int = 0
        self.current_lawn: str = "normal"
        self.planting: bool = True
        self.planting_location: tuple[int, int] = (-1, -1)

        self.lawn_size: dict[str, tuple[int, int]] = {
            "glitched": (5,9),
            "normal": (5, 9),
            "night": (5, 9),
            "pool": (6, 9),
            "fog": (6, 9),
            "roof": (5, 9),
        }

        self.lawn_properties: dict[str, dict] = {
            "glitched": {
                "night": False,
                "watered_rows": (3,),
                "watered_cols": (0,),
                "watered_tiles": ((3, 4), (5, 1)),
                "tilted_rows": (0,),
                "tilted_cols": (),
                "tilted_tiles": ((3, 4), ),
                "tile_skin": "glitched",
            },
            "normal": {
                "night": False,
                "watered_rows": (),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (),
                "tilted_tiles": (),
                "tile_skin": "grass",
            },
            "night": {
                "night": True,
                "watered_rows": (),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (),
                "tilted_tiles": (),
                "tile_skin": "grass",
            },
            "pool": {
                "night": False,
                "watered_rows": (2, 3),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (),
                "tilted_tiles": (),
                "tile_skin": "grass",
            },
            "fog": {
                "night": True,
                "watered_rows": (2, 3),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (),
                "tilted_tiles": (),
                "tile_skin": "grass",
            },
            "roof": {
                "night": False,
                "watered_rows": (),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (0, 1),
                "tilted_tiles": (),
                "tile_skin": "roof",
            },
        }

        self.game_lawn: dict = {}

        self.unlocked_slots = self.save_data["unlocked_slots"]

        self.active_seeds: dict[str, Optional[int]] = {
            "seedslot1": None,
            "seedslot2": None,
            "seedslot3": None,
            "seedslot4": None,
            "seedslot5": None,
            "seedslot6": None,
            "seedslot7": None,
            "seedslot8": None,
            "seedslot9": None,
            "seedslot10": None,
        }

    def ConstructBoard(self):
        if 1 <= self.current_level <= 10:
            self.current_lawn = "normal"
        elif 11 <= self.current_level <= 20:
            self.current_lawn = "night"
        elif 21 <= self.current_level <= 30:
            self.current_lawn = "pool"
        elif 31 <= self.current_level <= 40:
            self.current_lawn = "fog"
        elif 41 <= self.current_level <= 50:
            self.current_lawn = "roof"
        else:
            self.current_lawn = "glitched"
 
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
            (self.screen.get_height() - grid_h) // 2 + 20,
        )

        lawn = []

        rows, cols = self.lawn_size[self.current_lawn]
        props = self.lawn_properties[self.current_lawn]

        night        = props["night"]
        watered_rows = props["watered_rows"]
        watered_cols = props["watered_cols"]
        watered_tiles = props["watered_tiles"]
        tilted_rows  = props["tilted_rows"]
        tilted_cols  = props["tilted_cols"]
        tilted_tiles = props["tilted_tiles"]
        tile_skin    = props["tile_skin"]



        for r in range(rows):
            row = []
            for c in range(cols):
                is_watered = r in watered_rows or c in watered_cols or (c, r) in watered_tiles
                is_tilted  = r in tilted_rows  or c in tilted_cols  or (c, r) in tilted_tiles

                if is_watered:
                    row.append(((c, r), "water", "tilted" if is_tilted else "", "empty"))
                else:
                    row.append(((c, r), tile_skin, "tilted" if is_tilted else "", "empty"))

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

                if tile == "glitched":
                    base_color = (157, 0, 255)
                elif tile == "grass":
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
                    if tile == "glitched":
                        color = (0,0,0)

                #!^ night mode
                if night:
                    color = tuple(self.clamp(v - 50) for v in color)

                if c == self.planting_location[0] or r == self.planting_location[1]:
                    color = tuple(self.clamp(v + 25) for v in color)

                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(x, y, self.cell_size[0], self.cell_size[1]),
                )

    def draw_zombies(self):
        pass

    def draw_plants(self):
        pass

    def loop(self, current_level):
        self.current_level: int = current_level
        self.ConstructBoard()

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


class GameMenu:
    def __init__(self, config, save, statistics) -> None:
        SCREEN_RATIO = (640, 640)
        self.screen = pygame.display.set_mode(SCREEN_RATIO)
        pygame.display.set_caption("PvZ But Sceer")

        self.running = True
        self.running_level = False

        self.BGC: tuple = (25, 25, 25)
        self.Clock = pygame.time.Clock()
        self.FPS: int = 24

        if statistics:
            self.statistics = statistics
        else:
            self.statistics: dict[str, float] = {}

        if save:
            self.save_data = save
        else:
            self.save_data = {
                "unlocked_seeds": 0,
                "current_level": 0,
                "coin_count": 0,
                "shop": {
                    ## --- EXTRA SEED SLOTS ---
                    "seed_slot_7": {"unlocked": False, "price": 750, "enabled": True, "req": None},
                    "seed_slot_8": {"unlocked": False, "price": 5000, "enabled": False, "req": "seed_slot_7"},
                    "seed_slot_9": {"unlocked": False, "price": 20000, "enabled": False, "req": "seed_slot_8"},
                    "seed_slot_10": {"unlocked": False, "price": 80000, "enabled": False, "req": "seed_slot_9"},

                    ## --- EXTRA DEFENSES ---
                    "pool_cleaner": {"unlocked": False, "price": 1000, "enabled": True, "req": "level_3_1"},
                    "garden_rake": {"unlocked": False, "price": 200, "enabled": True, "req": None, "uses": 3},
                    "roof_cleaner": {"unlocked": False, "price": 3000, "enabled": True, "req": "level_5_1"},

                    ## --- UPGRADES ---
                    #!$ Available after Level 3-4
                    "gatling_pea": {"unlocked": False, "price": 5000, "enabled": False, "req": "level_3_4"},
                    "twin_sunflower": {"unlocked": False, "price": 5000, "enabled": False, "req": "level_3_4"},
                    
                    #!$ Available after Level 4-4
                    "gloom_shroom": {"unlocked": False, "price": 7500, "enabled": False, "req": "level_4_4"},
                    "cattail": {"unlocked": False, "price": 10000, "enabled": False, "req": "level_4_4"},
                    
                    #!$ Available after Level 5-1
                    "spikerock": {"unlocked": False, "price": 7500, "enabled": False, "req": "level_5_1"},
                    "gold_magnet": {"unlocked": False, "price": 3000, "enabled": False, "req": "level_5_1"},
                    
                    #!$ Available after Level 5-10
                    "winter_melon": {"unlocked": False, "price": 10000, "enabled": False, "req": "level_5_10"},
                    "cob_cannon": {"unlocked": False, "price": 20000, "enabled": False, "req": "level_5_10"},
                },
                "unlocked_slots": {
                    f"seedslot{i}": (True if i <= 6 else False) for i in range(1, 11)
                },
            }

        if config:
            self.config = config
        else:
            self.config = {}

        self.RunLevel = GameLevel(
            self.screen, self.config, self.save_data, self.statistics
        )

    def loop(self):
        while self.running:
            dt = self.Clock.tick(self.FPS)
            self.screen.fill(self.BGC)

            if self.running_level:
                result = self.RunLevel.loop(self.save_data["current_level"])
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


class StartGame:
    def __init__(self) -> None:
        key = SaveLoad.generate_key_from_string("PvZ_Skeered")
        config_path = SaveLoad.get_save_path(name="config", folder_type="Configs")
        save_path = SaveLoad.get_save_path(name="save", folder_type="Saves")
        statistics_path = SaveLoad.get_save_path(name="statistics", folder_type="Saves")
        self.config = SaveLoad.load(config_path)
        self.save = SaveLoad.load(save_path, key=key, encrypted=True, log=True)
        self.statistics = SaveLoad.load(
            statistics_path, key=key, encrypted=True, log=True
        )

        self.menu = GameMenu(self.config, self.save, self.statistics)

    def LoadSave(self):
        self.menu.loop()


def main():
    start = StartGame()
    start.LoadSave()


if __name__ == "__main__":
    main()
