import sys, os

parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
sys.path.append(parent_dir)

from init import *
from .DataBases.Seeds import SeedArcive


class Draw:
    @staticmethod
    def clamp(v):
        return max(0, min(255, v))

    @staticmethod
    def draw_lawn(game):
        grid = game.game_lawn["Game_Grid"]
        night = game.game_lawn["night"]

        for row in grid:
            for cell in row:
                (c, r), tile, *_ = cell

                x = game.lawn_offset[0] + c * game.cell_size[0]
                y = game.lawn_offset[1] + r * game.cell_size[1]

                game.board_rects[(c, r)] = pygame.Rect(
                    x, y, game.cell_size[0], game.cell_size[1]
                )

                base_color = None

                TILE_COLORS = {
                    "grass": (60, 180, 75),
                    "water": (50, 120, 200),
                    "roof": (164, 74, 74),
                    "glitched": (157, 0, 255),
                    "empty": (120, 120, 120),
                }

                base_color = TILE_COLORS.get(tile, (120, 120, 120))

                #!^ variation construction
                if (c + r) % 2 == 0:
                    color = base_color
                else:
                    color = tuple(Draw.clamp(v - 10) for v in base_color)
                    if tile == "glitched":
                        color = (0, 0, 0)

                #!^ night mode
                if night:
                    color = tuple(Draw.clamp(v - 50) for v in color)

                if c == game.planting_location[0] or r == game.planting_location[1]:
                    color = tuple(Draw.clamp(v + 25) for v in color)

                pygame.draw.rect(
                    game.screen,
                    color,
                    pygame.Rect(x, y, game.cell_size[0], game.cell_size[1]),
                )

    @staticmethod
    def draw_SeedBar(game):
        bar_x, bar_y = 10, 10
        slot_w, slot_h = 50, 60
        padding = 5
        sun_box_w = 60

        if isinstance(game.unlocked_slots, dict):
            slots_count = sum(1 for value in game.unlocked_slots.values() if value)
        else:
            try:
                slots_count = int(game.unlocked_slots)
            except (TypeError, ValueError):
                slots_count = 6

        total_width = sun_box_w + padding + (slots_count * (slot_w + padding)) + padding
        total_height = slot_h + (padding * 2)

        pygame.draw.rect(
            game.screen,
            (50, 40, 30),
            (bar_x, bar_y, total_width, total_height),
            border_radius=5,
        )
        pygame.draw.rect(
            game.screen,
            (100, 80, 60),
            (bar_x, bar_y, total_width, total_height),
            width=2,
            border_radius=5,
        )

        sun_box_x = bar_x + padding
        sun_box_y = bar_y + padding
        pygame.draw.rect(
            game.screen,
            (220, 200, 150),
            (sun_box_x, sun_box_y, sun_box_w, slot_h),
            border_radius=3,
        )

        font = pygame.font.SysFont("Arial", 16, bold=True)
        sun_text = font.render(str(game.sun_count), True, (0, 0, 0))
        text_rect = sun_text.get_rect(
            center=(sun_box_x + sun_box_w // 2, sun_box_y + slot_h // 2)
        )
        game.screen.blit(sun_text, text_rect)

        start_slots_x = sun_box_x + sun_box_w + padding
        slots_keys = [f"seedslot{i}" for i in range(1, slots_count + 1)]

        game.seed_rects.clear()

        for i, key in enumerate(slots_keys):
            slot_x = start_slots_x + i * (slot_w + padding)
            slot_y = bar_y + padding

            plant_id = game.active_seeds.get(key)
            if plant_id is not None:
                slot_color = (139, 115, 85)
            else:
                slot_color = (80, 80, 80)

            if getattr(game, "selected_seed_slot", None) == key:
                slot_color = (255, 215, 0)

            pygame.draw.rect(
                game.screen,
                slot_color,
                (slot_x, slot_y, slot_w, slot_h),
                border_radius=3,
            )
            pygame.draw.rect(
                game.screen,
                (30, 30, 30),
                (slot_x, slot_y, slot_w, slot_h),
                width=1,
                border_radius=3,
            )

            if plant_id is not None:
                plant_text = font.render(f"{plant_id}", True, (255, 255, 255))
                p_rect = plant_text.get_rect(
                    center=(slot_x + slot_w // 2, slot_y + slot_h // 2)
                )
                game.screen.blit(plant_text, p_rect)
            else:
                empty_text = font.render("-", True, (120, 120, 120))
                e_rect = empty_text.get_rect(
                    center=(slot_x + slot_w // 2, slot_y + slot_h // 2)
                )
                game.screen.blit(empty_text, e_rect)

            game.seed_rects[key] = pygame.Rect(slot_x, slot_y, slot_w, slot_h)

    @staticmethod
    def draw_seed_selector(game):
        panel_x, panel_y = 40, 100
        cols = 8
        card_w, card_h = 55, 70
        padding = 6

        seeds_dict = SeedArcive.get_all()
        total_seeds = len(seeds_dict)
        rows = (total_seeds + cols - 1) // cols

        panel_w = (cols * (card_w + padding)) + padding
        panel_h = (rows * (card_h + padding)) + padding + 30

        if not hasattr(game, "selector_rects"):
            game.selector_rects = {}
        game.selector_rects.clear()

        pygame.draw.rect(
            game.screen,
            (35, 25, 20),
            (panel_x, panel_y, panel_w, panel_h),
            border_radius=8,
        )
        pygame.draw.rect(
            game.screen,
            (75, 55, 40),
            (panel_x, panel_y, panel_w, panel_h),
            width=3,
            border_radius=8,
        )

        title_font = pygame.font.SysFont("Arial", 14, bold=True)
        title_text = title_font.render("CHOOSE YOUR CARDS", True, (210, 180, 140))
        game.screen.blit(title_text, (panel_x + padding + 2, panel_y + 8))

        font_name = pygame.font.SysFont("Arial", 9, bold=True)
        font_cost = pygame.font.SysFont("Arial", 11, bold=True)

        start_grid_y = panel_y + 30

        for i, (name, data) in enumerate(seeds_dict.items()):
            c = i % cols
            r = i // cols

            cx = panel_x + padding + c * (card_w + padding)
            cy = start_grid_y + r * (card_h + padding)

            is_chosen = name in game.active_seeds.values()
            is_upgrade = data["is_upgrade"]

            if is_chosen:
                bg_color = (40, 40, 40)
                text_color = (100, 100, 100)
                cost_color = (70, 70, 70)
            elif is_upgrade:
                bg_color = (90, 0, 130)
                text_color = (255, 255, 255)
                cost_color = (0, 0, 0)
            elif name == "Imitater":
                bg_color = (150, 150, 150)
                text_color = (255, 255, 255)
                cost_color = (0, 0, 0)
            else:
                bg_color = (139, 115, 85)
                text_color = (255, 255, 255)
                cost_color = (0, 0, 0)

            card_rect = pygame.Rect(cx, cy, card_w, card_h)
            pygame.draw.rect(game.screen, bg_color, card_rect, border_radius=4)
            pygame.draw.rect(
                game.screen, (20, 20, 20), card_rect, width=1, border_radius=4
            )

            game.selector_rects[name] = card_rect

            display_name = name
            if len(display_name) > 9:
                display_name = display_name[:8] + "."

            name_surface = font_name.render(display_name, True, text_color)
            name_rect = name_surface.get_rect(center=(cx + card_w // 2, cy + 18))
            game.screen.blit(name_surface, name_rect)

            cost_h = 16
            cost_strip_y = (cy + card_h) - cost_h - 2
            pygame.draw.rect(
                game.screen,
                (240, 230, 180) if not is_chosen else (60, 60, 60),
                (cx + 2, cost_strip_y, card_w - 4, cost_h),
                border_radius=2,
            )

            cost_surface = font_cost.render(str(data["cost"]), True, cost_color)
            cost_rect = cost_surface.get_rect(
                center=((cx + card_w // 2), cost_strip_y + (cost_h // 2))
            )
            game.screen.blit(cost_surface, cost_rect)

    @staticmethod
    def draw_zombies(game):
        pass

    @staticmethod
    def draw_plants(game):
        pass

    @staticmethod
    def draw_planting(game, selected_seed):
        mx, my = pygame.mouse.get_pos()
