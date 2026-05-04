import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI

import pygame

class PvEUI:
    def __init__(self, screen):
        self.screen = screen

        self.actions = ["Attack", "Magic", "Guard", "Item", "Flee"]
        self.buttons = []
        self.spell_list = []

        self.spell_page = 0
        self.spells_per_page = 4
        self.printed = False

        #!^ Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (40, 40, 40)
        self.DARK = (25, 25, 25)
        self.RED = (200, 60, 60)
        self.BLUE = (60, 120, 220)
        self.YELLOW = (255, 234, 0)

        #!^ Fonts (correct + safe)
        self.FONT = pygame.font.SysFont("arial", 18)
        self.BIG = pygame.font.SysFont("arial", 24)

        self.spell_bg = {
            "": {
                "text": "#1F2937",
                "bg": "#E5E7EB"
            },
            "arcane": {
                "text": "#E9D5FF",
                "bg": "#0021A8"
            },
            "blood": {
                "text": "#FEE2E2",
                "bg": "#991B1B"
            },
            "dark": {
                "text": "#D1D5DB",
                "bg": "#111827"
            },
            "earth": {
                "text": "#ECFDF5",
                "bg": "#365314"
            },
            "electric": {
                "text": "#1F2937",
                "bg": "#FACC15"
            },
            "fire": {
                "text": "#FFF7ED",
                "bg": "#C2410C"
            },
            "holy": {
                "text": "#78350F",
                "bg": "#FEF9C3"
            },
            "ice": {
                "text": "#0C4A6E",
                "bg": "#BAE6FD"
            },
            "physical": {
                "text": "#111827",
                "bg": "#9CA3AF"
            },
            "poison": {
                "text": "#F3E8FF",
                "bg": "#005100"
            },
            "wind": {
                "text": "#064E3B",
                "bg": "#A7F3D0"
            }
        }

        self.categories = {
            "Rage": {
                "border": "#DC2626"
            },
            "Spell": {
                "border": "#7C3AED"
            },
            "Technique": {
                "border": "#2563EB"
            }
        }

    #note ---------------- TEXT HELPER ----------------
    def draw_text(self, text, x, y, font, color=None, clip_rect=None):
        if color is None:
            color = self.WHITE

        surf = font.render(text, True, color)

        if clip_rect:
            old_clip = self.screen.get_clip()
            self.screen.set_clip(clip_rect)

        self.screen.blit(surf, (x, y))

        if clip_rect:
            self.screen.set_clip(old_clip)

    def fit_text_ellipsis(self, text, font, max_width):
        if font.size(text)[0] <= max_width:
            return text

        ellipsis = "..."
        while len(text) > 0:
            text = text[:-1]
            if font.size(text + ellipsis)[0] <= max_width:
                return text + ellipsis

        return ellipsis

    #note ---------------- MAIN DRAW ----------------
    def draw(self, game, shop = False):
        
        if shop:
            self.screen.fill(self.DARK)
            
            self._draw_shop(game.player_stats)
            
            return self.buttons
        else:
            self.screen.fill(self.DARK)

            self._draw_enemy(game.enemy)
            self._draw_player(game.player_stats)
            self._draw_actions(game, game.mode, game.spells_damage)

            return self.buttons

#!^ Shop:
    def _draw_shop(self, player):
        self.buttons = []

        # background bar (same style as actions)
        pygame.draw.rect(self.screen, self.BLACK, (10, 520, 620, 110))

        # shop title
        self.draw_text("SHOP", 20, 525, self.BIG)

        btn_w, btn_h = 180, 60
        spacing = 15
        start_x = 20
        y = 555

        # example shop items (replace with your real shop data)
        shop_items = [
            {"name": "Sword", "price": 100},
            {"name": "Shield", "price": 75},
            {"name": "Potion", "price": 25},
        ]

        # Leave shop button
        leave_rect = pygame.Rect(500, 20, 120, 60)

        pygame.draw.rect(self.screen, self.RED, leave_rect)
        pygame.draw.rect(self.screen, self.WHITE, leave_rect, 2)

        self.draw_text("LEAVE", leave_rect.x + 25, leave_rect.y + 18, self.FONT)

        self.buttons.append(("leave_shop", leave_rect, "shop", -1))

        for i, item in enumerate(shop_items):
            x = start_x + i * (btn_w + spacing)
            rect = pygame.Rect(x, y, btn_w, btn_h)

            # affordability check (because players are broke 90% of the time)
            affordable = player["gold"] >= item["price"]

            bg = self.GRAY if affordable else (60, 60, 60)
            border = self.BLUE if affordable else self.RED

            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, border, rect, 2)

            name_text = self.fit_text_ellipsis(item["name"], self.FONT, rect.width - 10)
            self.draw_text(name_text, x + 10, y + 10, self.FONT)

            self.draw_text(
                f"{item['price']}g",
                x + 10,
                y + 32,
                self.FONT,
                self.YELLOW if hasattr(self, "YELLOW") else self.WHITE
            )

            self.buttons.append((item["name"], rect, "shop", i))
        

    #note ---------------- ENEMY ----------------
    def _draw_enemy(self, enemy):
        pygame.draw.rect(self.screen, self.GRAY, (10, 10, 260, 120))

        self.draw_text(
            f"{enemy['name']} (Lv {enemy['lvl']})",
            20, 20, self.BIG
        )

        self.draw_text(
            f"HP: {enemy['hp']} / {enemy['max_hp']}",
            20, 60, self.FONT
        )

        ratio = enemy["hp"] / enemy["max_hp"]

        pygame.draw.rect(self.screen, self.RED, (20, 90, 200 * ratio, 10))
        pygame.draw.rect(self.screen, self.WHITE, (20, 90, 200, 10), 1)

    #note ---------------- PLAYER ----------------
    def _draw_player(self, player):
        pygame.draw.rect(self.screen, self.GRAY, (400, 10, 230, 120))

        self.draw_text(
            f"{player['name']} Lv {player['lvl']}",
            410, 20, self.BIG
        )

        self.draw_text(
            f"HP: {player['hp']} / {player['max_hp']}",
            410, 60, self.FONT
        )

        self.draw_text(
            f"MP: {player['mp']} / {player['max_mp']}",
            410, 90, self.FONT
        )

        hp_r = player["hp"] / player["max_hp"]
        mp_r = player["mp"] / player["max_mp"]

        pygame.draw.rect(self.screen, self.RED, (410, 80, 180 * hp_r, 6))
        pygame.draw.rect(self.screen, self.BLUE, (410, 105, 180 * mp_r, 6))

        pygame.draw.rect(self.screen, self.WHITE, (410, 80, 180, 6), 1)
        pygame.draw.rect(self.screen, self.WHITE, (410, 105, 180, 6), 1)

    #note ---------------- ACTIONS ----------------
    def _draw_actions(self, game, mode, spells):
        self.buttons = []

        btn_w, btn_h = 110, 60
        spacing = 10
        start_x = 20
        y = 545
        nav_w, nav_h = 70, 25
        nav_y = 500
        center_x = 10 + 620 // 2

        if mode == "Normal":
            pygame.draw.rect(self.screen, self.BLACK, (10, 520, 620, 110))
            for i, action in enumerate(self.actions):
                x = start_x + i * (btn_w + spacing)
                rect = pygame.Rect(x, y, btn_w, btn_h)

                pygame.draw.rect(self.screen, self.GRAY, rect)
                pygame.draw.rect(self.screen, self.WHITE, rect, 2)

                self.draw_text(action, x + 20, y + 18, self.FONT)

                self.buttons.append((action, rect, "main","-1"))
        
        elif mode == "Spells":
            pygame.draw.rect(self.screen, self.BLACK, (10, 520, 620, 110))
            WIDTH_MULT = 1.29

            prev_rect = pygame.Rect(center_x - 120, nav_y, nav_w, nav_h)
            back_rect = pygame.Rect(center_x - 35, nav_y, nav_w, nav_h)
            next_rect = pygame.Rect(center_x + 50, nav_y, nav_w, nav_h)

            for label, rect in [
                ("Prev", prev_rect),
                ("Back", back_rect),
                ("Next", next_rect)
            ]:
                pygame.draw.rect(self.screen, self.GRAY, rect)
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)
                self.draw_text(label, rect.x + 10, rect.y + 3, self.FONT)
                self.buttons.append((label, rect, "nav","-1"))


            if not self.printed:
                for _, spell in spells.items():
                    self.spell_list.append((spell['name'],spell['type'],spell['damage_type']))
                    
                if game.debug:
                    print (f"{ANSI.YELLOW}{self.spell_list}{ANSI.RESET}")
                self.printed = True
            
            start = self.spell_page *self.spells_per_page
            end = start + self.spells_per_page

            for i, spell_data in enumerate(self.spell_list[start:end]):
                spell, type, damage_type = spell_data
                
                BORDER = self.categories[type]["border"]
                TILE = self.spell_bg[damage_type]["bg"]
                TEXT_COLOR = self.spell_bg[damage_type]["text"]
                
                x = start_x + i * (btn_w * WIDTH_MULT + spacing)
                rect = pygame.Rect(x, y, btn_w * WIDTH_MULT, btn_h)

                pygame.draw.rect(self.screen, TILE, rect)
                pygame.draw.rect(self.screen, BORDER, rect, 2)
                
                max_text_width = rect.width - 20  # padding inside tile

                display_text = self.fit_text_ellipsis(spell, self.FONT, max_text_width)
                
                self.draw_text(display_text, x + 10, y + 18, self.FONT, TEXT_COLOR, clip_rect=rect)
                
                self.buttons.append((spell, rect, "magic",start + i))
                
                

        elif mode == "Inventory":
            return

        else: return