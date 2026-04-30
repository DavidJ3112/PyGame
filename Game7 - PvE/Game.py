import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI
import scripts.PvE as PvE
import scripts.Ui as pve_ui
import scripts.spells as Spell
import scripts.Enemies as Enemies
import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.pve = PvE.PvE()
        self.mode = "Normal"
        self.running = True
        self.debug = True

        self.SCREEN_RATIOS = (640, 640)
        self.BGCOLOR = (25, 25, 25)

        self.SCREEN = pygame.display.set_mode(self.SCREEN_RATIOS)

        self.FPS = 24
        self.Clock = pygame.time.Clock()

        self.ui = pve_ui.PvEUI(self.SCREEN)

        self.spells = Spell.all_spells()

        self.player_stats = {
            "lvl": 5,

            #!^ Health & mana
            "hp": 80,
            "max_hp": 100,
            "mp": 30,
            "max_mp": 50,

            #!^ Core attributes
            "str": 12,   ## Strength (physical damage)
            "int": 10,   ## Intelligence (magic power)
            "dex": 11,   ## Dexterity (speed / accuracy)
            "def": 9,    ## Defense (damage reduction)
            "res": 8,    ## Resistance (magic defense)

            #!^ Secondary stats
            "atk": 15,   ## Attack power
            "crit": 5,   ## Critical chance (%)
            "spd": 10,   ## Turn speed / initiative
            "eva": 7,    ## Dodge / Evasion chance

            #!^ Progression
            "xp": 120,
            "xp_to_next": 200,

            #!^ Misc
            "gold": 50,
            "luck": 3
        }
        
        self.enemy = Enemies.generate_enemy(self.player_stats["lvl"])

    def loop(self):
        while self.running:
            self.Clock.tick(self.FPS)

            buttons = self.ui.draw(self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c and pygame.key.get_mods() & pygame.K_RCTRL:
                        self.running = False

                    if event.key == pygame.K_F1:
                        self.enemy = Enemies.generate_enemy(self.player_stats["lvl"])

                    if event.key == pygame.K_F2:
                        self.mode = "Normal"
                    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for name, rect, mode, spell_index in buttons:
                        if rect.collidepoint(mx, my):

#note ──────────────────   Debug Text  ──────────────────────────────────────────────────────────
                            if self.debug:
                                print(f"{ANSI.RED}{buttons}{ANSI.RESET}")

                            print(f"{ANSI.BRIGHT_GREEN}     Action clicked: {name}{ANSI.RESET}")
                            if self.debug:
                                print(f"{ANSI.CYAN}     Action Clicked: {name}, rect: {rect}, Mode: {mode}, Current mode:{self.mode}{ANSI.RESET}")
                            print(f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}")

#note ──────────────────    Main Detection  ─────────────────────────────────────────────────────
                            if mode == "main":
                                if name == "Attack":
                                    PvE.PvE.Attack(self, self.player_stats, self.enemy)
                                elif name == "Magic":
                                    self.mode = "Spells"
                                elif name == "Guard":
                                    PvE.PvE.Guard(self, self.player_stats, self.enemy)
                                elif name == "Item":
                                    print("Item")
                                    self.mode = "Inventory"
                                elif name == "Flee":
                                    PvE.PvE.Flee(self, self.player_stats, self.enemy)

#note ──────────────────    Magic Detection ─────────────────────────────────────────────────────
                            elif mode == "magic":
                                cast = list(self.spells.items())
                                spell_key, spell_data = cast[spell_index]
                                PvE.PvE.Cast(self, self.player_stats, self.enemy, spell_key, spell_data)
                                self.mode = "Normal"

#note ──────────────────    Page Detection ──────────────────────────────────────────────────────
                            else:
                                if name == "Next":
                                    max_page = max(0, (len(self.ui.spell_list) - 1) // self.ui.spells_per_page)
                                    self.ui.spell_page = min(max_page, self.ui.spell_page + 1)
                                    break
                                elif name == "Prev":
                                    self.ui.spell_page = max(0, self.ui.spell_page - 1)
                                    break
                                elif name == "Back":
                                    self.mode = "Normal"
                                    break

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.loop()