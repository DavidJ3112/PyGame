import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(parent_dir)

import random

from general_scripts.ANSI import ANSI

class PvE:
    def __init__(self):
        pass

    def Attack(self): PvE.Do_Action(self, "Attack")
    def Guard(self): PvE.Do_Action(self, "Guard")
    def Flee(self): PvE.Do_Action(self, "Flee")
    def Item(self): PvE.Do_Action(self, "Item")
    def Cast(self, spell_key, spell_data): PvE.Do_Action(self, "Spell", (spell_key, spell_data))
    

    def Do_Action(self, mode, spell_data = None):
        Player_Attack_Data, mode_player, cast_data = PvE.Player(self, mode, spell_data)
        Enemy_Attack_Data, mode_enemy = PvE.Enemy(self)
        PvE.Attack_Cycle(self, Player_Attack_Data, Enemy_Attack_Data, mode_player, mode_enemy, cast_data)

    def Player_Stats(self):
        Player_Attack_Data = {
            "HP": self.player_stats_base["hp"],
            "MAX_HP": self.player_stats_base["max_hp"],
            "MP": self.player_stats_base["mp"],
            "MAX_MP": self.player_stats_base["max_mp"],
            "LVL": self.player_stats_base["lvl"],
            "EXP": self.player_stats_base["xp"],
            "EXP_REQ": self.player_stats_base["xp_req"],
            "STR": self.player_stats["str"],
            "INT": self.player_stats["int"],
            "DEX": self.player_stats["dex"],
            "RES": self.player_stats["res"],
            "DEF": self.player_stats["def"],
            "ATK": self.player_stats["atk"],
            "CRIT": self.player_stats["crit"],
            "SPD": self.player_stats["spd"],
            "EVA": self.player_stats["eva"],
        }

        return Player_Attack_Data
    
    def Enemy_Stats(self):
        Enemy_Attack_Data = {
            "HP": self.enemy["hp"],
            "MAX_HP": self.enemy["max_hp"],
            "MP": self.enemy["mp"],
            "DEF": self.enemy["defense"],
            "ATK": self.enemy["attack"],
            "CRIT": self.enemy["crit"],
            "SPD": self.enemy["speed"],
            "EVA": self.enemy["eva"],
            "DROP": {"XP": self.enemy["exp_drop"], "GOLD": self.enemy["gold_drop"]},
            "Type": self.enemy["attack_type"],
            "RES": self.enemy["resistance"],
        }

        if self.enemy["boss"]:
            mode = random.randint(1, 4)
        else:
            mode = random.randint(1, 3)

        return Enemy_Attack_Data, mode

    def Player(self, mode, spell_data):
        if self.debug:
            print(f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}")
            for key, value in self.player_stats.items():
                print(f"{ANSI.YELLOW}{key}: {value}{ANSI.RESET}")
            print(f"{ANSI.wrap(mode, ANSI.BOLD, ANSI.YELLOW)}")

            if spell_data:
                print(f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}")
                print(f"{ANSI.wrap(str(spell_data), ANSI.BOLD, ANSI.YELLOW)}")

        if mode == "Attack":
            Player_Attack_Data = PvE.Player_Stats(self)
            cast_data = spell_data

        elif mode == "Guard":
            Player_Attack_Data = PvE.Player_Stats(self)
            cast_data = spell_data

        elif mode == "Flee":
            Player_Attack_Data = PvE.Player_Stats(self)
            cast_data = spell_data

        elif mode == "Items":
            Player_Attack_Data = PvE.Player_Stats(self)
            cast_data = spell_data

        elif mode == "Spell":
            Player_Attack_Data = PvE.Player_Stats(self)
            cast_data = spell_data

        return Player_Attack_Data, mode, cast_data

    def Enemy(self):
        if self.debug:
            print(self.sep)
            for key, value in self.enemy.items():
                print(f"{ANSI.YELLOW}{key}: {value}{ANSI.RESET}")
            print(self.sep)

        Enemy_Attack_Data, mode = PvE.Enemy_Stats(self)

        if mode == 1: mode = "Attack"
        elif mode == 2: mode = "Defend"
        elif mode == 3: mode = "Magic/ Attack"
        elif mode == 4: mode = "Heal"

        return Enemy_Attack_Data, mode

    def Attack_Cycle(self, Player_Attack_Data,  Enemy_Attack_Data, mode_player = "Attack",mode_enemy = "Attack",  cast_data = None):
        if cast_data:
            spell_key, spell_data = cast_data
        
        P = Player_Attack_Data
        E = Enemy_Attack_Data

        ## Debug prints
        if self.debug:
            print(f"{ANSI.CYAN}{ANSI.BOLD} Player: {Player_Attack_Data} {ANSI.NEW_LINE} Enemy:{Enemy_Attack_Data}{ANSI.RESET}")
            print(f"{ANSI.CYAN}{ANSI.BOLD} Spell: {cast_data}{ANSI.RESET}")

            print(self.sep)
            print(ANSI.wrap(f"Player: {mode_player}", ANSI.YELLOW, ANSI.BOLD))
            print(ANSI.wrap(f"Enemy: {mode_enemy}", ANSI.YELLOW, ANSI.BOLD))

            print(self.sep)

#!% Player Attack Logic ────────────────────────────────────────────────────────────────────────
        #!^ Damage
        P_damage = int(P["ATK"] * (1 + P["STR"] / 100))

        #!^ Spell Damage
        spell_damage = 0
        if cast_data:
            spell_damage = int(spell_data["enemy_dmg"] * (P["INT"] * 0.1))

        #!^ Crit
        is_crit = random.uniform(0, 100) < P["CRIT"]
        crit_multiplier = 1.5 + (P["DEX"] / 100)  # DEX=11 → ×1.61
        P_damage = int(P_damage * crit_multiplier) if is_crit else P_damage

        #% Debug prints
        if self.debug:
            print(ANSI.wrap(f"[P ATK] dmg={P_damage} spell={spell_damage} crit={is_crit} ×{crit_multiplier:.2f}", ANSI.YELLOW, ANSI.BOLD))

#!% Enemy Attack Logic ─────────────────────────────────────────────────────────────────────────
        #!^ Damage
        E_damage = int(E["ATK"] * (1 + E["STR"] / 100)) if "STR" in E else int(E["ATK"])

        #!^ Crit
        is_crit_e = random.uniform(0, 100) < float(E["CRIT"])
        crit_multiplier_e = 1.5 + (float(E["SPD"]) / 100)
        E_damage = int(E_damage * crit_multiplier_e) if is_crit_e else E_damage

        #% Debug prints
        if self.debug:
            print(ANSI.wrap(f"[E ATK] dmg={E_damage} crit={is_crit_e} ×{crit_multiplier_e:.2f}", ANSI.YELLOW, ANSI.BOLD))

#!% Player Def / EVA ───────────────────────────────────────────────────────────────────────────
        #!^ DEF
        E_damage = int(E_damage * (1 - E["DEF"] / (E["DEF"] + 50)))

        #!^ EVA
        hit = random.uniform(0, 100) > float(E["EVA"]) - (P["SPD"] - E["SPD"])
        E_damage = E_damage if hit else 0

        #% Debug prints
        if self.debug:
            print(ANSI.wrap(f"[P DEF] e_dmg={E_damage} hit={hit}", ANSI.YELLOW, ANSI.BOLD))

#!% Enemy Def / EVA ────────────────────────────────────────────────────────────────────────────
        #!^ DEF
        P_damage = int(P_damage * (1 - P["DEF"] / (P["DEF"] + 50)))
        spell_damage = int(spell_damage * (1 - P["DEF"] / (P["DEF"] + 50))) if cast_data else 0

        #!^ EVA
        hit_e = random.uniform(0, 100) > float(P["EVA"]) - (E["SPD"] - P["SPD"])
        P_damage = P_damage if hit_e else 0
        spell_damage = spell_damage if hit_e else 0

        #% Debug prints
        if self.debug:
            print(ANSI.wrap(f"[E DEF] p_dmg={P_damage} spell={spell_damage} hit={hit_e}", ANSI.YELLOW, ANSI.BOLD))
            print(self.sep)