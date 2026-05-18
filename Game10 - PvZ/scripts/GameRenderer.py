import sys, os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(parent_dir)

from init import *


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
                    color = tuple(Draw.clamp(v - 10) for v in base_color)
                    if tile == "glitched":
                        color = (0,0,0)

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
        
        pygame.draw.rect(game.screen, (50, 40, 30), (bar_x, bar_y, total_width, total_height), border_radius=5)
        pygame.draw.rect(game.screen, (100, 80, 60), (bar_x, bar_y, total_width, total_height), width=2, border_radius=5)

        sun_box_x = bar_x + padding
        sun_box_y = bar_y + padding
        pygame.draw.rect(game.screen, (220, 200, 150), (sun_box_x, sun_box_y, sun_box_w, slot_h), border_radius=3)
        
        font = pygame.font.SysFont("Arial", 16, bold=True)
        sun_text = font.render(str(game.sun_count), True, (0, 0, 0))
        text_rect = sun_text.get_rect(center=(sun_box_x + sun_box_w // 2, sun_box_y + slot_h // 2))
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
                
            pygame.draw.rect(game.screen, slot_color, (slot_x, slot_y, slot_w, slot_h), border_radius=3)
            pygame.draw.rect(game.screen, (30, 30, 30), (slot_x, slot_y, slot_w, slot_h), width=1, border_radius=3)
            
            if plant_id is not None:
                plant_text = font.render(f"P{plant_id}", True, (255, 255, 255))
                p_rect = plant_text.get_rect(center=(slot_x + slot_w // 2, slot_y + slot_h // 2))
                game.screen.blit(plant_text, p_rect)
            else:
                empty_text = font.render("-", True, (120, 120, 120))
                e_rect = empty_text.get_rect(center=(slot_x + slot_w // 2, slot_y + slot_h // 2))
                game.screen.blit(empty_text, e_rect)
                
            game.seed_rects[key] = pygame.Rect(slot_x, slot_y, slot_w, slot_h)

    @staticmethod
    def draw_zombies(game):
        pass

    @staticmethod
    def draw_plants(game):
        pass