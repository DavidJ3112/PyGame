import sys, os

parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
sys.path.append(parent_dir)

from init import *
from .Debug import DEBUG
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
        s = getattr(game, "seedbar_scale", 1.0)

        card_w      = int(45 * s)
        card_h      = int(58 * s)
        padding     = int(4  * s)
        sun_box_w   = int(45 * s)
        cost_h      = int(14 * s)
        header_h    = int(22 * s)
        title_size  = max(8, int(11 * s))
        name_size   = max(7, int(8  * s))
        cost_size   = max(8, int(10 * s))

        bar_x, bar_y = 10, 10

        if isinstance(game.unlocked_slots, dict):
            slots_count = sum(1 for value in game.unlocked_slots.values() if value)
        else:
            try:
                slots_count = int(game.unlocked_slots)
            except (TypeError, ValueError):
                slots_count = 6

        panel_w = padding + sun_box_w + padding + (slots_count * (card_w + padding))
        panel_h = card_h + (padding * 2) + header_h

        pygame.draw.rect(
            game.screen,
            (35, 25, 20),
            (bar_x, bar_y, panel_w, panel_h),
            border_radius=8,
        )
        pygame.draw.rect(
            game.screen,
            (75, 55, 40),
            (bar_x, bar_y, panel_w, panel_h),
            width=3,
            border_radius=8,
        )

        title_font = pygame.font.SysFont("Arial", title_size, bold=True)
        title_text = title_font.render("SEED BAR", True, (210, 180, 140))
        game.screen.blit(title_text, (bar_x + padding + 2, bar_y + max(4, int(6 * s))))

        start_y    = bar_y + header_h
        font_name  = pygame.font.SysFont("Arial", name_size, bold=True)
        font_cost  = pygame.font.SysFont("Arial", cost_size, bold=True)

        # ── Sun card ──────────────────────────────────────────────────────────
        sun_x = bar_x + padding
        sun_y = start_y

        sun_card = pygame.Rect(sun_x, sun_y, sun_box_w, card_h)
        pygame.draw.rect(game.screen, (139, 115, 85), sun_card, border_radius=4)
        pygame.draw.rect(game.screen, (20, 20, 20), sun_card, width=1, border_radius=4)

        img_area_h = card_h - cost_h - 4
        img_cx = sun_x + sun_box_w // 2
        img_cy = sun_y + img_area_h // 2

        sun_img = game.SPRITES.get("Sun") or game.SPRITES.get("sun")
        if sun_img:
            max_size = max(4, img_area_h - 6)
            scaled = pygame.transform.smoothscale(sun_img, (max_size, max_size))
            game.screen.blit(scaled, scaled.get_rect(center=(img_cx, img_cy)))
        else:
            r = max(3, img_area_h // 2 - 4)
            pygame.draw.circle(game.screen, (255, 220, 50), (img_cx, img_cy), r)
            pygame.draw.circle(game.screen, (230, 180, 0), (img_cx, img_cy), r, width=1)

        cost_strip_y = (sun_y + card_h) - cost_h - 2
        pygame.draw.rect(
            game.screen,
            (240, 230, 180),
            (sun_x + 2, cost_strip_y, sun_box_w - 4, cost_h),
            border_radius=2,
        )
        sun_count_surface = font_cost.render(str(game.sun_count), True, (0, 0, 0))
        game.screen.blit(
            sun_count_surface,
            sun_count_surface.get_rect(center=(sun_x + sun_box_w // 2, cost_strip_y + cost_h // 2))
        )

        # ── Seed slot cards ───────────────────────────────────────────────────
        slots_start_x = sun_x + sun_box_w + padding
        slots_keys = [f"seedslot{i}" for i in range(1, slots_count + 1)]
        game.seed_rects.clear()

        for i, key in enumerate(slots_keys):
            cx = slots_start_x + i * (card_w + padding)
            cy = start_y

            plant_id  = game.active_seeds.get(key)
            is_selected = getattr(game, "selected_seed_slot", None) == key

            if is_selected:
                bg_color         = (40, 40, 40)
                text_color       = (100, 100, 100)
                cost_color       = (70, 70, 70)
                cost_strip_color = (60, 60, 60)
            elif plant_id is not None:
                bg_color         = (139, 115, 85)
                text_color       = (255, 255, 255)
                cost_color       = (0, 0, 0)
                cost_strip_color = (240, 230, 180)
            else:
                bg_color         = (35, 25, 20)
                text_color       = (100, 100, 100)
                cost_color       = (70, 70, 70)
                cost_strip_color = (60, 60, 60)

            card_rect = pygame.Rect(cx, cy, card_w, card_h)
            pygame.draw.rect(game.screen, bg_color, card_rect, border_radius=4)
            pygame.draw.rect(game.screen, (20, 20, 20), card_rect, width=1, border_radius=4)
            game.seed_rects[key] = card_rect

            img_area_h = card_h - cost_h - 4
            p_cx = cx + card_w // 2
            p_cy = cy + img_area_h // 2

            if plant_id is not None:
                plant_sprites = game.SPRITES.get("Plants")
                plant_img = isinstance(plant_sprites, dict) and plant_sprites.get(str(plant_id))
                if plant_img:
                    max_size = max(4, min(card_w - 6, img_area_h - 4))
                    scaled = pygame.transform.smoothscale(plant_img, (max_size, max_size))
                    game.screen.blit(scaled, scaled.get_rect(center=(p_cx, p_cy)))
                else:
                    display_name = str(plant_id)
                    if len(display_name) > 8:
                        display_name = display_name[:7] + "."
                    surf = font_name.render(display_name, True, text_color)
                    game.screen.blit(surf, surf.get_rect(center=(p_cx, p_cy)))
            else:
                surf = font_name.render("-", True, text_color)
                game.screen.blit(surf, surf.get_rect(center=(p_cx, p_cy)))

            cost_strip_y = (cy + card_h) - cost_h - 2
            pygame.draw.rect(
                game.screen,
                cost_strip_color,
                (cx + 2, cost_strip_y, card_w - 4, cost_h),
                border_radius=2,
            )

            cost_val = "-"
            if plant_id is not None:
                plant_data = SeedArcive.get_all().get(str(plant_id), {})
                cost_val   = str(plant_data.get("cost", "?"))

            cost_surf = font_cost.render(cost_val, True, cost_color)
            game.screen.blit(
                cost_surf,
                cost_surf.get_rect(center=(cx + card_w // 2, cost_strip_y + cost_h // 2))
            )

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
    def draw_projectiles(game):
        pass

    @staticmethod
    def draw_plants(game):
        for row in game.game_lawn["Game_Grid"]:
            for data in row:
                DEBUG.sendmsg("HIGH", f"Plant: {data[3]}, Pos: {data[0]}")

                x = data[0][0] * game.cell_size[0] + game.lawn_offset[0] +30
                y = data[0][1] * game.cell_size[1] + game.lawn_offset[1] +30

                font = pygame.font.SysFont("Arial", 12, bold=True)
                plant_sprites = game.SPRITES.get("Plants")

                if data[3] == "empty":
                    continue
                
                if isinstance(plant_sprites, dict) and data[3] in plant_sprites:
                    img = plant_sprites[data[3]]
                    img_rect = img.get_rect(topleft=(x, y))
                    game.screen.blit(img, img_rect)
                    
                else:
                    pygame.draw.circle(game.screen, (46, 204, 113), (x, y), 22)
                    pygame.draw.circle(game.screen, (255, 255, 255), (x, y), 22, width=2)
                    
                    text_surface = font.render(f"{data[3]}", True, (255, 255, 255))
                    text_rect = text_surface.get_rect(topleft=(x, y - 35))
                    
                    shadow_surface = font.render(f"{data[3]}", True, (0, 0, 0))
                    shadow_rect = shadow_surface.get_rect(topleft=(x + 1, y - 34))
                    
                    game.screen.blit(shadow_surface, shadow_rect)
                    game.screen.blit(text_surface, text_rect)

    @staticmethod
    def draw_planting(game, selected_seed):
        """Draws the selected seed tracking the mouse position."""
        if not selected_seed:
            return

        mx, my = pygame.mouse.get_pos()
        font = pygame.font.SysFont("Arial", 12, bold=True)

        plant_sprites = game.SPRITES.get("Plants")

        if isinstance(plant_sprites, dict) and selected_seed in plant_sprites:
            img = plant_sprites[selected_seed]
            img_rect = img.get_rect(center=(mx, my))
            game.screen.blit(img, img_rect)
            
        else:
            pygame.draw.circle(game.screen, (46, 204, 113), (mx, my), 22)
            pygame.draw.circle(game.screen, (255, 255, 255), (mx, my), 22, width=2)
            
            text_surface = font.render(f"Planting: {selected_seed}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(mx, my - 35))
            
            shadow_surface = font.render(f"Planting: {selected_seed}", True, (0, 0, 0))
            shadow_rect = shadow_surface.get_rect(center=(mx + 1, my - 34))
            
            game.screen.blit(shadow_surface, shadow_rect)
            game.screen.blit(text_surface, text_rect)

        if game.planting_location != (-1, -1):
            target_rect = game.board_rects.get(game.planting_location)
            if target_rect:
                pygame.draw.rect(game.screen, (255, 255, 255), target_rect, width=2)
