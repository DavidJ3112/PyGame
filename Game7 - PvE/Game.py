import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI
import scripts.PvE as PvE
import scripts.Ui as pve_ui
import scripts.spell as Spell
import scripts.Enemies as Enemies
import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.pve = PvE.PvE()
        self.running = True

        self.SCREEN_RATIOS = (640, 640)
        self.BGCOLOR = (25, 25, 25)

        self.SCREEN = pygame.display.set_mode(self.SCREEN_RATIOS)

        self.FPS = 24
        self.Clock = pygame.time.Clock()

        self.ui = pve_ui.PvEUI(self.SCREEN)

        self.spells = Spell.all_spells()

        self.player_stats = {
            "lvl": 5,
            "hp": 80,
            "max_hp": 100,
            "mp": 30,
            "max_mp": 50
        }
        
        self.enemy = Enemies.generate_enemy(self.player_stats["lvl"])

    def loop(self):
        while self.running:
            self.Clock.tick(self.FPS)

            buttons = self.ui.draw(self.player_stats, self.enemy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.enemy = Enemies.generate_enemy(self.player_stats["lvl"])

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    for name, rect in buttons:
                        if rect.collidepoint(mx, my):
                            print("Action clicked:", name)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.loop()