import pygame

class PvEUI:
    def __init__(self, screen):
        self.screen = screen

        self.actions = ["Attack", "Magic", "Guard", "Item", "Flee"]
        self.buttons = []

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (40, 40, 40)
        self.DARK = (25, 25, 25)
        self.RED = (200, 60, 60)
        self.BLUE = (60, 120, 220)

        # Fonts (correct + safe)
        self.FONT = pygame.font.SysFont("arial", 18)
        self.BIG = pygame.font.SysFont("arial", 24)

    #note ---------------- TEXT HELPER ----------------
    def draw_text(self, text, x, y, font, color=None):
        if color is None:
            color = self.WHITE
        surf = font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    #note ---------------- MAIN DRAW ----------------
    def draw(self, player, enemy):
        self.screen.fill(self.DARK)

        self._draw_enemy(enemy)
        self._draw_player(player)
        self._draw_actions()

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

        pygame.draw.rect(self.screen, self.RED, (20, 90, 180 * ratio, 10))
        pygame.draw.rect(self.screen, self.WHITE, (20, 90, 180, 10), 1)

    #note ---------------- PLAYER ----------------
    def _draw_player(self, player):
        pygame.draw.rect(self.screen, self.GRAY, (400, 10, 230, 120))

        self.draw_text(
            f"Player Lv {player['lvl']}",
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
    def _draw_actions(self):
        pygame.draw.rect(self.screen, self.BLACK, (10, 520, 620, 110))

        self.buttons = []

        btn_w, btn_h = 110, 60
        spacing = 10
        start_x = 20
        y = 545

        for i, action in enumerate(self.actions):
            x = start_x + i * (btn_w + spacing)
            rect = pygame.Rect(x, y, btn_w, btn_h)

            pygame.draw.rect(self.screen, self.GRAY, rect)
            pygame.draw.rect(self.screen, self.WHITE, rect, 2)

            self.draw_text(action, x + 20, y + 18, self.FONT)

            self.buttons.append((action, rect))