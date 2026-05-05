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
import copy


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.HOSTNAME = socket.gethostname()

        self.mode = "Normal"
        self.shop = False
        self.running = True
        self.log = False
        self.debug = False
        self.level_up = True
        self.sep = f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}"

        self.god_p = False
        self.god_e = False
        self.inf_dmg = False

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
            "lvl": 1,

            #!^ Health & mana
            "hp": 500,
            "max_hp": 500,
            "mp": 50,
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
            "xp": 0,
            "xp_req": 100,

            #!^ Misc
            "gold": 50,
            "luck": 3
        }

        self.SCALING = {
            "hp": 50,
            "max_hp": 50,
            "mp": 5,
            "max_mp": 5,
            "str": 2,
            "int": 2,
            "dex": 2,
            "def": 2,
            "res": 2,
            "atk": 3,
            "spd": 1,
            "eva": 1,
        }

        self.player_stats = copy.deepcopy(self.player_stats_base)

        self.dificulty: float = 1.0
        self.no_boss_sinds: int = 0

        self.Enemy_Generation_Logic()

        self.pve = PvE.PvE(self)

    def Enemy_Generation_Logic(self):
        self.enemy = Enemies.generate_enemy(self, self.player_stats["lvl"])

    def state_scaling(self, base, lvl, per_level):
        return base + (lvl - 1) * per_level

    def scale_stats(self, base_stats, lvl):
        scaled = {}
        for stat, base in base_stats.items():
            if stat in self.SCALING:
                scaled[stat] = self.state_scaling(base, lvl, self.SCALING[stat])
            else:
                scaled[stat] = base
        return scaled

    def loop(self):
        while self.running:
            if self.debug: self.log = False

            self.Clock.tick(self.FPS)

            buttons = self.ui.draw(self, self.shop)

            if self.player_stats_base["xp"] >= self.player_stats_base["xp_req"]:
                self.player_stats_base["xp"] = self.player_stats_base["xp"] - self.player_stats_base["xp_req"]
                self.player_stats_base["lvl"] += 1

                self.player_stats_base["xp_req"] = round(self.player_stats_base["xp_req"] * 1.25)

                base_lvl = self.player_stats_base["lvl"]
                self.player_stats = self.scale_stats(self.player_stats_base, base_lvl)

                self.player_stats["hp"] = self.player_stats["max_hp"]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c and pygame.key.get_mods() & pygame.K_RCTRL:
                        self.running = False

                    if event.key == pygame.K_F1:
                        if self.debug: self.Enemy_Generation_Logic()
                        else:
                            self.log = not self.log
                            print(ANSI.wrap("loggin: " + str(self.log), ANSI.GREEN))

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
                                    self.pve.Attack()
                                elif name == "Magic":
                                    self.mode = "Spells"
                                elif name == "Guard":
                                    self.pve.Guard()
                                elif name == "Item":
                                    print("Item")
                                    self.mode = "Inventory"
                                elif name == "Flee":
                                    self.pve.Flee()

#!^ ──────────────────    Spell Detection ─────────────────────────────────────────────────────
                            elif mode == "magic":
                                cast = list(self.spells_damage.items())
                                spell_key, spell_data = cast[spell_index]

                                if self.debug: print(f"{ANSI.rgb(255,128,0)}{ANSI.BOLD} The Individual know as {self.player_stats_base['name']} is atempting to cast: {spell_data['name']}{ANSI.CURSOR_SAVE}{ANSI.RESET}")

                                if spell_data["mp_cost"] <= self.player_stats_base["mp"]:
                                    if self.debug: print(f"{ANSI.CURSOR_RESTORE}{ANSI.BRIGHT_GREEN}{ANSI.BOLD} Success {ANSI.RESET}")
                                    self.pve.Cast(spell_key, spell_data)
                                else:
                                    if self.debug: print(f"{ANSI.CURSOR_RESTORE}{ANSI.RED}{ANSI.BOLD} Failed: Mana Def {ANSI.RESET}")

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