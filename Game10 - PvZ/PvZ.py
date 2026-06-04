from init import *

from scripts import *

class GameLevel:
    def __init__(self, screen, config, save_data, statistics) -> None:
        self.config = config
        self.save_data = save_data
        self.statistics = statistics

        DEBUG.debug_level = "NONE"

        #!^ Temp Data Setup prevent pylance Crying
        self.lawn_offset, self.cell_size = {}, {}
        self.rows, self.cols = (None,None)
        self.selector_rects = {}
        self.board_rects = {}
        self.planting_seed = None

        self.current_level = 1
        self.Clock = pygame.time.Clock()
        self.FPS: int = 24
        self.BGC: tuple[int, int, int] = (25, 25, 25)
        self.screen = screen

        self.running = True
        self.Running_Level = False

        self.sun_count: int = 50
        self.wave_progress: float = 0
        self.zombie_count: int = 0
        self.zombie_pos: int = 0
        self.current_lawn: str = "normal"
        self.planting: bool = False
        self.planting_location: tuple[int, int] = (-1, -1)
        self.seed_rects: dict[str, pygame.Rect] = {}

        self.seedbar_scale = 1.0
        self.seedbar_scale_target = 1.0

        self.lawn_size, self.lawn_properties = Configs.Get_LawnConfigs()
        make_slots = lambda: {f"seedslot{i}": None for i in range(1, 11)}
        self.active_seeds = make_slots()

        self.game_lawn: dict = {}

        self.unlocked_slots = self.save_data["unlocked_slots"]

        self.SPRITES = {
            'Plants': UTILS.load_images_dict('Plants'),
            'Zombies': UTILS.load_images_dict('Zombies'),
            'Projectiles': UTILS.load_images_dict('Projectiles'),
        }
        

    def loop(self, current_level):
        self.current_level: int = current_level
        Constructions.ConstructBoard(self)

        while self.running:
            dt = self.Clock.tick(self.FPS)
            self.screen.fill(self.BGC)
            result = self.check_events()

            if result:
                return result
            
            self.seedbar_scale += (self.seedbar_scale_target - self.seedbar_scale) * 0.12

            ## Level Draw
            if self.Running_Level:
                Draw.draw_lawn(self)
                Draw.draw_plants(self)
                Draw.draw_zombies(self)
                self.seedbar_scale_target = 1.2
            else:
                Draw.draw_seed_selector(self)
                self.seedbar_scale_target = 1.0

            ## Planting Draw
            if self.planting:
                Draw.draw_planting(self, self.planting_seed)
            
            ## HUD Draw
            Draw.draw_SeedBar(self)

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

                if event.key == pygame.K_F1:
                    self.Running_Level = not self.Running_Level

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                if self.planting:
                    for (x, y), rect in self.board_rects.items():
                        if rect.collidepoint(mx ,my):
                            Lawn_cell = self.game_lawn["Game_Grid"][y][x]
                            Lawn_cell[3] = self.planting_seed

                            DEBUG.sendmsg("LOW", Lawn_cell)
                            

                for slot, rect in self.seed_rects.items():
                    if rect.collidepoint(mx, my):
                        if self.Running_Level == False:
                            values = list(self.active_seeds.values())
                            index = int(slot.replace("seedslot", "")) - 1
                            values.pop(index)
                            values.append(None)
                            for i in range(10):
                                self.active_seeds[f"seedslot{i+1}"] = values[i]

                        else:
                            self.planting = True
                            self.planting_seed = self.active_seeds[slot]
                
                if not self.Running_Level:
                    for name, rect in self.selector_rects.items():
                        if rect.collidepoint(mx, my):
                            if name in self.active_seeds.values():
                                break
                            for slot, seed in self.active_seeds.items():
                                if self.active_seeds[slot] is None and self.unlocked_slots.get(slot, False):
                                    self.active_seeds[slot] = name
                                    break
                            break


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
    def __init__(self) -> None:
        pygame.init()
        SCREEN_RATIO = (640, 640)
        self.screen = pygame.display.set_mode(SCREEN_RATIO)
        pygame.display.set_caption("PvZ But Sceer")

        self.running = True
        self.running_level = False

        self.BGC: tuple = (25, 25, 25)
        self.Clock = pygame.time.Clock()
        self.FPS: int = 24

        self.config = {}
        self.save_data = {}
        self.statistics = {}

        self.Seeds = SeedArcive.get_all()

        loader = Load_Data()
        loader.LoadData(self)

        self.RunLevel = GameLevel(self.screen, self.config, self.save_data, self.statistics)

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

        saver = Save_Data
        saver.Save_Data(self.config, self.save_data, self.statistics)

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
        self.menu = GameMenu()

    def LoadSave(self):
        self.menu.loop()


def main():
    start = StartGame()
    start.LoadSave()


if __name__ == "__main__":
    main()
