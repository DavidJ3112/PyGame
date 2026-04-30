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

        #!^ Fonts (correct + safe)
        self.FONT = pygame.font.SysFont("arial", 18)
        self.BIG = pygame.font.SysFont("arial", 24)

    #note ---------------- TEXT HELPER ----------------
    def draw_text(self, text, x, y, font, color=None):
        if color is None:
            color = self.WHITE
        surf = font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    #note ---------------- MAIN DRAW ----------------
    def draw(self, game):
        self.screen.fill(self.DARK)

        self._draw_enemy(game.enemy)
        self._draw_player(game.player_stats)
        self._draw_actions(game, game.mode, game.spells)

        return self.buttons

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
                    self.spell_list.append(spell['name'])
                if game.debug:
                    print (f"{ANSI.YELLOW}{self.spell_list}{ANSI.RESET}")
                self.printed = True
            
            start = self.spell_page *self.spells_per_page
            end = start + self.spells_per_page

            for i, spell in enumerate(self.spell_list[start:end]):
                x = start_x + i * (btn_w * WIDTH_MULT + spacing)
                rect = pygame.Rect(x, y, btn_w * WIDTH_MULT, btn_h)
                
                pygame.draw.rect(self.screen, self.GRAY, rect)
                pygame.draw.rect(self.screen, self.WHITE, rect, 2)
                
                self.draw_text(spell, x + 20, y + 18, self.FONT)
                
                self.buttons.append((spell, rect, "magic",start + i))
                

        elif mode == "Inventory":
            return

        else: return