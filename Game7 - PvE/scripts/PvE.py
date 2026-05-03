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

#!# DO ACTION ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Do_Action(self, mode, spell_data = None):
        Player_Attack_Data, mode_player, P_cast_data = PvE.Player(self, mode, spell_data)
        Enemy_Attack_Data, mode_enemy, E_cast_data = PvE.Enemy(self)
        PvE.Attack_Cycle(self, Player_Attack_Data, Enemy_Attack_Data, mode_player, mode_enemy, P_cast_data, E_cast_data)

#!# Player Stats ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
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

#!# Enemy Stats ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Enemy_Stats(self):
        Enemy_Attack_Data = {
            "HP": self.enemy["hp"],
            "MAX_HP": self.enemy["max_hp"],
            "MP": self.enemy["mp"],
            "MAX_MP": self.enemy["max_mp"],
            "LVL": self.enemy["lvl"],
            "DEF": self.enemy["defense"],
            "ATK": self.enemy["attack"],
            "CRIT": self.enemy["crit"],
            "SPD": self.enemy["speed"],
            "EVA": self.enemy["eva"],
            "DROP": {"XP": self.enemy["exp_drop"], "GOLD": self.enemy["gold_drop"]},
            "Type": self.enemy["attack_type"],
            "RES": self.enemy["resistance"],
        }
        
        if Enemy_Attack_Data["Type"] == "Magician":
            mode = random.choices([1, 2, 3], weights=[0.5, 3, 5])[0]
        else:
            mode = random.choices([1, 2, 3], weights=[5, 3, 0.5])[0]

        return Enemy_Attack_Data, mode

#!# PLAYER ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Player(self, mode, spell_data):
        if self.debug:
            print(f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}")
            for key, value in self.player_stats.items():
                print(f"{ANSI.YELLOW}{key}: {value}{ANSI.RESET}")

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

#!# Enemy ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Enemy(self):
        if self.debug:
            print(self.sep)
            for key, value in self.enemy.items():
                print(f"{ANSI.YELLOW}{key}: {value}{ANSI.RESET}")
            print(self.sep)

        Enemy_Attack_Data, mode = PvE.Enemy_Stats(self)
        spell_key, spell = None, None
        cast = None

#!! NEEDS REWORK ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        if mode == 1: mode = "Attack"
        elif mode == 2: mode = "Defend"
        elif mode == 3: 
            spell_list = list(self.spells_damage.items())

            if self.debug or self.log:
                print(self.sep)

            for _ in range(10):
                idx = random.randint(0, len(spell_list) - 1)
                spell_key, spell = spell_list[idx]

                if self.debug or self.log:
                    print(f"{ANSI.rgb(255,128,0)}{ANSI.BOLD} The Individual know as {self.enemy["name"]} is atempting to cast: {spell["name"]}{ANSI.CURSOR_SAVE}{ANSI.RESET}")

                if Enemy_Attack_Data["MP"] > 0:
                    if Enemy_Attack_Data["MP"] > spell["mp_cost"] and Enemy_Attack_Data["HP"] > spell["self_damage"]:
                        if spell["scaling_type"] == "mana_to_damage":
                            if Enemy_Attack_Data["MP"] >= 25: mode = "Spell" 
                            else:
                                print(f"{ANSI.CURSOR_RESTORE}{ANSI.RED}{ANSI.BOLD} Faild Mp-Dmg {ANSI.RESET}")
                                mode = "Attack"
                                continue
                        else: mode = "Spell"
                        if self.debug or self.log:
                            print(f"{ANSI.CURSOR_RESTORE}{ANSI.BRIGHT_GREEN}{ANSI.BOLD} Success {ANSI.RESET}")
                        break
                    else:
                        if self.debug or self.log:
                            print(f"{ANSI.CURSOR_RESTORE}{ANSI.RED}{ANSI.BOLD} Faild {ANSI.RESET}")
                        mode = "Attack"
                        continue
                else: continue
            if mode == "Spell": cast = (spell_key, self.spells_damage[spell_key])

        return Enemy_Attack_Data, mode, cast

#!# APPLY MODE ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def apply_mode(stats, mode, SCALES):
        for k, v in SCALES.get(mode, {}).items():
            stats[k] = round(stats[k] * v)

#!# ATTACK CYCLE ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Attack_Cycle(self, Player_Attack_Data,  Enemy_Attack_Data, mode_player = "Attack",mode_enemy = "Attack",  P_cast_data = None, E_cast_data = None):
        P_spell_key, P_spell_data = None, {"name": "No Cast Has Happend"}
        E_spell_key, E_spell_data = None, {"name": "No Cast Has Happend"}
        if P_cast_data: P_spell_key, P_spell_data = P_cast_data
        if E_cast_data: E_spell_key, E_spell_data = E_cast_data

        SCALES = {
            "Attack": {"ATK": 1.0, "DEF": 1.0},
            "Guard":  {"ATK": 0.3, "DEF": 5.0},
            "Spell":  {"ATK": 0.0, "DEF": 1.0},
            "Flee":   {"ATK": 0.0, "DEF": 0.3},
        }
        
        P = Player_Attack_Data.copy()
        E = Enemy_Attack_Data.copy()

        ## Debug prints
        if self.debug:
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.player_stats["name"]} Data: {ANSI.RED}HP:{self.player_stats_base["hp"]}/{self.player_stats_base["max_hp"]}{ANSI.BLUE} MP:{P["MP"]}/{P["MAX_MP"]} {ANSI.GREEN}LVL:{P["LVL"]}{ANSI.NEW_LINE}{ANSI.BRIGHT_YELLOW}{Player_Attack_Data}{ANSI.RESET}{ANSI.NEW_LINE}")
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.enemy["name"]} Data: {ANSI.RED}HP:{self.enemy["hp"]}/{self.enemy["max_hp"]}{ANSI.BLUE} MP:{E["MP"]}/{E["MAX_MP"]} {ANSI.GREEN}LVL:{E["LVL"]}{ANSI.NEW_LINE}{ANSI.BRIGHT_YELLOW}{Enemy_Attack_Data}{ANSI.RESET}{ANSI.NEW_LINE}")
            print(f"{ANSI.BRIGHT_MAGENTA}{ANSI.BOLD} {self.player_stats["name"]} Spell: {P_spell_data["name"]}{ANSI.YELLOW}{ANSI.NEW_LINE}{ANSI.BRIGHT_YELLOW}Data: {P_cast_data}{ANSI.RESET}{ANSI.NEW_LINE}")
            print(f"{ANSI.BRIGHT_MAGENTA}{ANSI.BOLD} {self.enemy["name"]} Spell: {E_spell_data["name"]}{ANSI.YELLOW}{ANSI.NEW_LINE}{ANSI.BRIGHT_YELLOW}Data: {E_cast_data}{ANSI.RESET}{ANSI.NEW_LINE}")

        if self.debug or self.log:
            print(self.sep)
            print(ANSI.wrap(f"{self.player_stats["name"]}: {mode_player}", ANSI.YELLOW, ANSI.BOLD))
            print(ANSI.wrap(f"{self.enemy["name"]}: {mode_enemy}", ANSI.YELLOW, ANSI.BOLD))
        
        if self.debug: print(self.sep)

#!% Action Scaler ──────────────────────────────────────────────────────────────────────────────
        PvE.apply_mode(P, mode_player, SCALES)
        PvE.apply_mode(E, mode_enemy, SCALES)

#!% Player Attack Logic ────────────────────────────────────────────────────────────────────────
        #!^ Damage
        P_damage = int(P["ATK"] * (1 + P["STR"] / 100))

        #!^ Spell Damage
        P_spell_damage = 0
        if P_cast_data:
            P_spell_damage = int(P_spell_data["enemy_dmg"] * (P["INT"] * 0.1))

        #!^ Crit
        is_crit = random.uniform(0, 100) < P["CRIT"]
        crit_multiplier = 1.5 + (P["DEX"] / 100)  # DEX=11 → ×1.61
        P_damage = int(P_damage * crit_multiplier) if is_crit else P_damage

        #% Debug prints
        if self.debug:
            print(ANSI.wrap(f"[P ATK] dmg={P_damage} spell={P_spell_damage} crit={is_crit} ×{crit_multiplier:.2f}", ANSI.YELLOW, ANSI.BOLD))

#!% Enemy Attack Logic ─────────────────────────────────────────────────────────────────────────
        #!^ Damage
        E_damage = int(E["ATK"] * (1 + E["STR"] / 100)) if "STR" in E else int(E["ATK"])

        #!^ Spell Damage
        E_spell_damage = 0
        if E_cast_data:
            E_spell_damage = int(round(E_spell_data["enemy_dmg"] * max(1, ((E["MAX_MP"] / 5) * 0.1))))

        #!^ Crit
        is_crit_e = random.uniform(0, 100) < float(E["CRIT"])
        crit_multiplier_e = 1.5 + (float(E["SPD"]) / 100)
        E_damage = int(E_damage * crit_multiplier_e) if is_crit_e else E_damage

        #% Debug prints
        if self.debug:
            print(ANSI.wrap(f"[E ATK] dmg={E_damage} spell={E_spell_damage} crit={is_crit_e} ×{crit_multiplier_e:.2f}", ANSI.YELLOW, ANSI.BOLD))

#!% Player Def / EVA ───────────────────────────────────────────────────────────────────────────
        #!^ DEF
        E_damage = int(E_damage * (1 - P["DEF"] / (P["DEF"] + 50)))
        
        if not E_spell_data: E_spell_damage = 0
        
        #!^ EVA
        hit = random.uniform(0, 100) > float(P["EVA"]) - (E["SPD"] - P["SPD"])
        E_damage = E_damage if hit else 0
        E_spell_damage = E_spell_damage if hit else E_spell_damage * .8

        #% Debug prints
        if self.debug:
            print(ANSI.wrap(f"[P DEF] e_dmg={E_damage} spell={E_spell_damage} hit={hit}", ANSI.YELLOW, ANSI.BOLD))

#!% Enemy Def / EVA ────────────────────────────────────────────────────────────────────────────
        #!^ DEF
        P_damage = int(P_damage * (1 - E["DEF"] / (E["DEF"] + 50)))

        if not P_spell_data: P_spell_damage = 0

        #!^ EVA
        hit_e = random.uniform(0, 100) > float(E["EVA"]) - (P["SPD"] - E["SPD"])
        P_damage = P_damage if hit_e else 0
        P_spell_damage = P_spell_damage if hit_e else P_spell_damage * .8

        #% Debug prints
        if self.debug:
            print(ANSI.wrap(f"[E DEF] p_dmg={P_damage} spell={P_spell_damage} hit={hit_e}", ANSI.YELLOW, ANSI.BOLD))
            print(self.sep)
#!% Damage cheats etc:
        if self.inf_dmg:
            P_damage = 32_767
            if P_cast_data: P_spell_damage = 32_767


#!% Actual Attack Caluclation ──────────────────────────────────────────────────────────────────
        for element, value in Enemy_Attack_Data["RES"].items():
            if self.debug:
                print(f"{ANSI.BLACK}{element = } {value = }{ANSI.RESET}")

            if E_cast_data:
                if element == E_spell_data["damage_type"]:
                    print(ANSI.wrap("Enemy: " + str(E_spell_damage), ANSI.BOLD, ANSI.BLUE))
                    E_spell_damage = round(E_spell_damage * (1 + value))
                    print(ANSI.wrap("Enemy: " + str(E_spell_damage), ANSI.BOLD, ANSI.RED))
            
            if P_cast_data:
                if element == P_spell_data["damage_type"]:
                    print(ANSI.wrap("Player: " + str(P_spell_damage), ANSI.BOLD, ANSI.BLUE))
                    P_spell_damage = round(P_spell_damage * (1 - value))
                    print(ANSI.wrap("Player: " + str(P_spell_damage), ANSI.BOLD, ANSI.RED))

        #!^ Player AtK
        if P_spell_damage > 0:
            self.enemy["hp"] -= P_spell_damage
            self.player_stats_base["mp"] -= P_spell_data["mp_cost"]
        if P_damage > 0:
            self.enemy["hp"] -= P_damage


        #!^ Enemy AtK
        if E_spell_damage > 0:
            self.player_stats_base["hp"] -= E_spell_damage
            self.enemy["mp"] -= E_spell_data["mp_cost"]
        if E_damage > 0:
            self.player_stats_base["hp"] -= E_damage
            
        #!^ MP Regen
        if self.player_stats_base["max_mp"] > 0:
            self.player_stats_base["mp"] += round(max(self.player_stats_base["max_mp"] / 15, (self.player_stats_base["max_mp"] / 10) * (1 - (self.player_stats_base["mp"] / self.player_stats_base["max_mp"]))))
            
            if self.player_stats_base["mp"] > self.player_stats_base["max_mp"]: 
                self.player_stats_base["mp"] = self.player_stats_base["max_mp"]
        
        if self.enemy["max_mp"] > 0:
            self.enemy["mp"] += round(max(self.enemy["max_mp"] / 15, (self.enemy["max_mp"] / 10) * (1 - (self.enemy["mp"] / self.enemy["max_mp"]))))
            
            if self.enemy["mp"] > self.enemy["max_mp"]: 
                self.enemy["mp"] = self.enemy["max_mp"]

        if self.log or self.debug:
            print(self.sep)
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.player_stats["name"]} Data: {ANSI.RED}HP:{self.player_stats_base["hp"]}/{self.player_stats_base["max_hp"]}{ANSI.BLUE} MP:{P["MP"]}/{P["MAX_MP"]} {ANSI.GREEN}LVL:{P["LVL"]}{ANSI.RESET}")
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.enemy["name"]} Data: {ANSI.RED}HP:{self.enemy["hp"]}/{self.enemy["max_hp"]}{ANSI.BLUE} MP:{E["MP"]}/{E["MAX_MP"]} {ANSI.GREEN}LVL:{E["LVL"]}{ANSI.RESET}")

            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.player_stats["name"]} Spell: {ANSI.YELLOW}{P_spell_data["name"]}{ANSI.RESET}")
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.enemy["name"]} Spell: {ANSI.YELLOW}{E_spell_data["name"]}{ANSI.RESET}")

        #!^ death
        if self.player_stats_base["hp"] <= 0:
            if self.god_p:
                print(self.sep)
                print(f"{ANSI.YELLOW}{ANSI.BOLD} The Individual know as {self.player_stats_base["name"]} has Died {ANSI.RESET}{ANSI.CURSOR_SAVE}")
                self.player_stats_base["hp"] = self.player_stats_base["max_hp"]
                self.player_stats_base["mp"] = self.player_stats_base["max_mp"]
                print(f"{ANSI.CURSOR_RESTORE}{ANSI.MAGENTA}{ANSI.BOLD} Reincarnation Compleate{ANSI.RESET}")
            else:
                print("death")

        if self.enemy["hp"] <= 0:
            if self.god_e:
                print(self.sep)
                print(f"{ANSI.YELLOW}{ANSI.BOLD} The Individual know as {self.enemy["name"]} has Died {ANSI.RESET}{ANSI.CURSOR_SAVE}")
                self.enemy["hp"] = self.enemy["max_hp"]
                self.enemy["mp"] = self.enemy["max_mp"]
                print(f"{ANSI.CURSOR_RESTORE}{ANSI.MAGENTA}{ANSI.BOLD} Reincarnation Compleate{ANSI.RESET}")
            else:
                xp_d, gold_d = E["DROP"].values()
                self.player_stats_base["gold"] += gold_d
                
                self.player_stats_base["xp"] += xp_d
                if self.player_stats_base["xp"] >= self.player_stats_base["xp_req"]:
                    self.player_stats_base["xp"] = self.player_stats_base["xp"] - self.player_stats_base["xp_req"]
                    
                    self.player_stats_base["lvl"] += 1
                    self.player_stats_base["xp_req"] = round(self.player_stats_base["xp_req"] * 1.1)
                
                self.shop = True
                self.Enemy_Generation_Logic()
            
