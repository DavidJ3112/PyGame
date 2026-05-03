import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI
import scripts.PvE as PvE
import scripts.Ui as pve_ui
from general_scripts.RPG.Spells import all_spells
import scripts.Enemies as Enemies
import pygame
import socket

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.HOSTNAME = socket.gethostname()

        self.pve = PvE.PvE()
        self.mode = "Normal"
        self.shop = False
        self.running = True
        self.log = True
        self.debug = True
        self.sep = f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}"
        
        self.god_p = True
        self.god_e = True
        self.inf_dmg = True

        self.SCREEN_RATIOS = (640, 640)
        self.BGCOLOR = (25, 25, 25)

        self.SCREEN = pygame.display.set_mode(self.SCREEN_RATIOS)

        self.FPS = 24
        self.Clock = pygame.time.Clock()

        self.ui = pve_ui.PvEUI(self.SCREEN)

        self.spells_damage = all_spells(False, False)
        self.spells_buffs = all_spells(True, False)
        self.spells_healing = all_spells(False, True)

        self.player_stats_base = {
            "name": "Rose",
            "lvl": 5,

            #!^ Health & mana
            "hp": 250,
            "max_hp": 250,
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
            "xp_req": 200,

            #!^ Misc
            "gold": 50,
            "luck": 3
        }
        self.player_stats = self.player_stats_base
        
        self.dificulty : float = 1.0
        self.no_boss_sinds : int = 0

        self.Enemy_Generation_Logic()

    def Enemy_Generation_Logic(self):
        self.player_stats = self.player_stats_base
        self.enemy = Enemies.generate_enemy(self, self.player_stats["lvl"])


    def loop(self):
        while self.running:
            if self.debug: self.log = False

            self.Clock.tick(self.FPS)

            buttons = self.ui.draw(self, self.shop)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c and pygame.key.get_mods() & pygame.K_RCTRL:
                        self.running = False

                    if event.key == pygame.K_F1:
                        if self.debug: self.Enemy_Generation_Logic()
                    
                    if event.key == pygame.K_F2:
                        if self.debug: 
                            self.god_p = not self.god_p
                            print(ANSI.wrap("God Mode of player: " + str(self.god_p), ANSI.GREEN))
                        
                    if event.key == pygame.K_F3:
                        if self.debug: 
                            self.god_e = not self.god_e
                            print(ANSI.wrap("God Mode of enemy: " + str(self.god_e), ANSI.GREEN))
                        
                    if event.key == pygame.K_F4:
                        if self.debug: 
                            self.inf_dmg = not self.inf_dmg
                            print(ANSI.wrap("Infinity Dmg: " + str(self.inf_dmg), ANSI.GREEN))
                        
                    if event.key == pygame.K_F5:
                        if self.HOSTNAME == "Desktop-David" or self.HOSTNAME == "Loptop-David":
                            self.debug = not self.debug
                            self.log = not self.log
                            print(ANSI.wrap("Debugging: " + str(self.debug), ANSI.GREEN))
                            print(ANSI.wrap("loggin: " + str(self.log), ANSI.GREEN))

                    if event.key == pygame.K_F6:
                        self.log = not self.log
                        print(ANSI.wrap("loggin: " + str(self.log), ANSI.GREEN))
                    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for name, rect, mode, spell_index in buttons:
                        if rect.collidepoint(mx, my):

#!^ ──────────────────   Debug Text  ──────────────────────────────────────────────────────────
                            if self.debug:
                                print(self.sep)
                                print(f"{ANSI.YELLOW}     Action Clicked: {name}, rect: {rect}, Mode: {mode}, Current mode:{self.mode}{ANSI.RESET}")

#!^ ──────────────────    Main Detection  ─────────────────────────────────────────────────────
                            if mode == "main":
                                if name == "Attack":
                                    PvE.PvE.Attack(self)
                                elif name == "Magic":
                                    self.mode = "Spells"
                                elif name == "Guard":
                                    PvE.PvE.Guard(self)
                                elif name == "Item":
                                    print("Item")
                                    self.mode = "Inventory"
                                elif name == "Flee":
                                    PvE.PvE.Flee(self)

#!^ ──────────────────    Spell Detection ─────────────────────────────────────────────────────
                            elif mode == "magic":
                                cast = list(self.spells_damage.items())
                                spell_key, spell_data = cast[spell_index]
                                
                                print(f"{ANSI.rgb(255,128,0)}{ANSI.BOLD} The Individual know as {self.player_stats_base["name"]} is atempting to cast: {spell_data["name"]}{ANSI.CURSOR_SAVE}{ANSI.RESET}")

                                if spell_data["mp_cost"] <= self.player_stats_base["mp"]:
                                    print(f"{ANSI.CURSOR_RESTORE}{ANSI.BRIGHT_GREEN}{ANSI.BOLD} Success {ANSI.RESET}")
                                    PvE.PvE.Cast(self, spell_key, spell_data)
                                else: print(f"{ANSI.CURSOR_RESTORE}{ANSI.RED}{ANSI.BOLD} Failed: Mana Def {ANSI.RESET}")

                                self.mode = "Normal"

#!^ ──────────────────    Page Detection ──────────────────────────────────────────────────────
                            elif mode == "nav":
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

                            elif mode == "shop":
                                if name == "leave_shop":
                                    self.shop = False
                            
                            
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.loop()