import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(parent_dir)

import random

from general_scripts.ANSI import ANSI


class PvE:
    def __init__(self, game):
        self.game = game

    def Attack(self): self.Do_Action("Attack")
    def Guard(self): self.Do_Action("Guard")
    def Flee(self): self.Do_Action("Flee")
    def Item(self): self.Do_Action("Item")
    def Cast(self, spell_key, spell_data): self.Do_Action("Spell", (spell_key, spell_data))

#!# DO ACTION ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Do_Action(self, mode, spell_data=None):
        Player_Attack_Data, mode_player, P_cast_data = self.Player(mode, spell_data)
        Enemy_Attack_Data, mode_enemy, E_cast_data = self.Enemy()
        self.Attack_Cycle(
            Player_Attack_Data,
            Enemy_Attack_Data,
            mode_player,
            str(mode_enemy),
            P_cast_data,
            E_cast_data
        )

#!# Player Stats ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Player_Stats(self):
        Player_Attack_Data = {
            "HP": self.game.player_stats_base["hp"],
            "MAX_HP": self.game.player_stats_base["max_hp"],
            "MP": self.game.player_stats_base["mp"],
            "MAX_MP": self.game.player_stats_base["max_mp"],
            "LVL": self.game.player_stats_base["lvl"],
            "EXP": self.game.player_stats_base["xp"],
            "EXP_REQ": self.game.player_stats_base["xp_req"],
            "STR": self.game.player_stats["str"],
            "INT": self.game.player_stats["int"],
            "DEX": self.game.player_stats["dex"],
            "RES": self.game.player_stats["res"],
            "DEF": self.game.player_stats["def"],
            "ATK": self.game.player_stats["atk"],
            "CRIT": self.game.player_stats["crit"],
            "SPD": self.game.player_stats["spd"],
            "EVA": self.game.player_stats["eva"],
        }
        return Player_Attack_Data

#!# Enemy Stats ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Enemy_Stats(self):
        Enemy_Attack_Data = {
            "HP": self.game.enemy["hp"],
            "MAX_HP": self.game.enemy["max_hp"],
            "MP": self.game.enemy["mp"],
            "MAX_MP": self.game.enemy["max_mp"],
            "LVL": self.game.enemy["lvl"],
            "DEF": self.game.enemy["defense"],
            "ATK": self.game.enemy["attack"],
            "CRIT": self.game.enemy["crit"],
            "SPD": self.game.enemy["speed"],
            "EVA": self.game.enemy["eva"],
            "DROP": {"XP": self.game.enemy["exp_drop"], "GOLD": self.game.enemy["gold_drop"]},
            "Type": self.game.enemy["attack_type"],
            "RES": self.game.enemy["resistance"],
        }

        if Enemy_Attack_Data["Type"] == "Magician":
            mode = random.choices([1, 2, 3], weights=[0.5, 3, 5])[0]
        else:
            mode = random.choices([1, 2, 3], weights=[5, 3, 0.5])[0]

        return Enemy_Attack_Data, mode

#!# PLAYER ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Player(self, mode, spell_data):
        if self.game.debug:
            print(f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}")
            for key, value in self.game.player_stats.items():
                print(f"{ANSI.YELLOW}{key}: {value}{ANSI.RESET}")

        Player_Attack_Data = self.Player_Stats()
        cast_data = spell_data

        return Player_Attack_Data, mode, cast_data

#!# Enemy ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Enemy(self):
        if self.game.debug:
            print(self.game.sep)
            for key, value in self.game.enemy.items():
                print(f"{ANSI.YELLOW}{key}: {value}{ANSI.RESET}")
            print(self.game.sep)

        Enemy_Attack_Data, mode = self.Enemy_Stats()
        spell_key, spell = None, None
        cast = None

#!! NEEDS REWORK ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        if mode == 1:
            mode = "Attack"
        elif mode == 2:
            mode = "Defend"
        elif mode == 3:
            spell_list = list(self.game.spells_damage.items())

            if self.game.debug or self.game.log:
                print(self.game.sep)

            for _ in range(10):
                idx = random.randint(0, len(spell_list) - 1)
                spell_key, spell = spell_list[idx]

                if self.game.debug or self.game.log:
                    print(f"{ANSI.rgb(255,128,0)}{ANSI.BOLD} The Individual know as {self.game.enemy['name']} is atempting to cast: {spell['name']}{ANSI.CURSOR_SAVE}{ANSI.RESET}")

                if Enemy_Attack_Data["MP"] > 0:
                    if Enemy_Attack_Data["MP"] > spell["mp_cost"] and Enemy_Attack_Data["HP"] > spell["self_damage"]:
                        if spell["scaling_type"] == "mana_to_damage":
                            if Enemy_Attack_Data["MP"] >= 25:
                                mode = "Spell"
                            else:
                                print(f"{ANSI.CURSOR_RESTORE}{ANSI.RED}{ANSI.BOLD} Faild Mp-Dmg {ANSI.RESET}")
                                mode = "Attack"
                                continue
                        else:
                            mode = "Spell"
                        if self.game.debug or self.game.log:
                            print(f"{ANSI.CURSOR_RESTORE}{ANSI.BRIGHT_GREEN}{ANSI.BOLD} Success {ANSI.RESET}")
                        break
                    else:
                        if self.game.debug or self.game.log:
                            print(f"{ANSI.CURSOR_RESTORE}{ANSI.RED}{ANSI.BOLD} Faild {ANSI.RESET}")
                        mode = "Attack"
                        continue
                else:
                    continue

            if mode == "Spell":
                cast = (spell_key, self.game.spells_damage[spell_key])

        return Enemy_Attack_Data, mode, cast

#!# APPLY MODE ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def apply_mode(self, stats, mode, SCALES):
        for k, v in SCALES.get(mode, {}).items():
            stats[k] = round(stats[k] * v)

#!# ATTACK CYCLE ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    def Attack_Cycle(self, Player_Attack_Data, Enemy_Attack_Data, mode_player="Attack", mode_enemy="Attack", P_cast_data=None, E_cast_data=None):
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
        if self.game.debug:
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.game.player_stats['name']} Data: {ANSI.RED}HP:{self.game.player_stats_base['hp']}/{self.game.player_stats_base['max_hp']}{ANSI.BLUE} MP:{P['MP']}/{P['MAX_MP']} {ANSI.GREEN}LVL:{P['LVL']}{ANSI.NEW_LINE}{ANSI.BRIGHT_YELLOW}{Player_Attack_Data}{ANSI.RESET}{ANSI.NEW_LINE}")
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.game.enemy['name']} Data: {ANSI.RED}HP:{self.game.enemy['hp']}/{self.game.enemy['max_hp']}{ANSI.BLUE} MP:{E['MP']}/{E['MAX_MP']} {ANSI.GREEN}LVL:{E['LVL']}{ANSI.NEW_LINE}{ANSI.BRIGHT_YELLOW}{Enemy_Attack_Data}{ANSI.RESET}{ANSI.NEW_LINE}")
            print(f"{ANSI.BRIGHT_MAGENTA}{ANSI.BOLD} {self.game.player_stats['name']} Spell: {P_spell_data['name']}{ANSI.YELLOW}{ANSI.NEW_LINE}{ANSI.BRIGHT_YELLOW}Data: {P_cast_data}{ANSI.RESET}{ANSI.NEW_LINE}")
            print(f"{ANSI.BRIGHT_MAGENTA}{ANSI.BOLD} {self.game.enemy['name']} Spell: {E_spell_data['name']}{ANSI.YELLOW}{ANSI.NEW_LINE}{ANSI.BRIGHT_YELLOW}Data: {E_cast_data}{ANSI.RESET}{ANSI.NEW_LINE}")

        if self.game.debug or self.game.log:
            print(self.game.sep)
            print(ANSI.wrap(f"{self.game.player_stats['name']}: {mode_player}", ANSI.YELLOW, ANSI.BOLD))
            print(ANSI.wrap(f"{self.game.enemy['name']}: {mode_enemy}", ANSI.YELLOW, ANSI.BOLD))

        if self.game.debug: print(self.game.sep)

#!% Action Scaler ──────────────────────────────────────────────────────────────────────────────
        self.apply_mode(P, mode_player, SCALES)
        self.apply_mode(E, mode_enemy, SCALES)

#!% Player Attack Logic ────────────────────────────────────────────────────────────────────────
        #!^ Damage
        P_damage = int(P["ATK"] * (1 + P["STR"] / 100))

        #!^ Spell Damage
        P_spell_damage = 0
        if P_cast_data:
            P_spell_damage = int(P_spell_data["enemy_dmg"] * (P["INT"] * 0.1))

        #!^ Crit
        is_crit = random.uniform(0, 100) < P["CRIT"]
        crit_multiplier = 1.5 + (P["DEX"] / 100)
        P_damage = int(P_damage * crit_multiplier) if is_crit else P_damage

        if self.game.debug:
            print(ANSI.wrap(f"[P ATK] dmg={P_damage} spell={P_spell_damage} crit={is_crit} ×{crit_multiplier:.2f}", ANSI.YELLOW, ANSI.BOLD))

#!% Enemy Attack Logic ─────────────────────────────────────────────────────────────────────────
        #!^ Damage
        E_damage = int(E["ATK"] * (1 + E["STR"] / 100)) if "STR" in E else int(E["ATK"])

        #!^ Spell Damage
        E_spell_damage = 0
        if E_cast_data:
            E_spell_damage = int(round(float(E_spell_data["enemy_dmg"]) * float(max(1, ((E["MAX_MP"] / 5) * 0.1)))))

        #!^ Crit
        is_crit_e = random.uniform(0, 100) < float(E["CRIT"])
        crit_multiplier_e = 1.5 + (float(E["SPD"]) / 100)
        E_damage = int(E_damage * crit_multiplier_e) if is_crit_e else E_damage

        if self.game.debug:
            print(ANSI.wrap(f"[E ATK] dmg={E_damage} spell={E_spell_damage} crit={is_crit_e} ×{crit_multiplier_e:.2f}", ANSI.YELLOW, ANSI.BOLD))

#!% Player Def / EVA ───────────────────────────────────────────────────────────────────────────
        #!^ DEF
        E_damage = int(E_damage * (1 - P["DEF"] / (P["DEF"] + 50)))

        if not E_spell_data: E_spell_damage = 0

        #!^ EVA
        hit = random.uniform(0, 100) > float(P["EVA"]) - (E["SPD"] - P["SPD"])
        E_damage = E_damage if hit else 0
        E_spell_damage = E_spell_damage if hit else E_spell_damage * .8

        if self.game.debug:
            print(ANSI.wrap(f"[P DEF] e_dmg={E_damage} spell={E_spell_damage} hit={hit}", ANSI.YELLOW, ANSI.BOLD))

#!% Enemy Def / EVA ────────────────────────────────────────────────────────────────────────────
        #!^ DEF
        P_damage = int(P_damage * (1 - E["DEF"] / (E["DEF"] + 50)))

        if not P_spell_data: P_spell_damage = 0

        #!^ EVA
        hit_e = random.uniform(0, 100) > float(E["EVA"]) - (P["SPD"] - E["SPD"])
        P_damage = P_damage if hit_e else 0
        P_spell_damage = P_spell_damage if hit_e else P_spell_damage * .8

        if self.game.debug:
            print(ANSI.wrap(f"[E DEF] p_dmg={P_damage} spell={P_spell_damage} hit={hit_e}", ANSI.YELLOW, ANSI.BOLD))
            print(self.game.sep)

#!% Damage cheats etc:
        if self.game.inf_dmg:
            P_damage = 32_767
            if P_cast_data: P_spell_damage = 32_767

#!% Actual Attack Caluclation ──────────────────────────────────────────────────────────────────
        for element, value in Enemy_Attack_Data["RES"].items():
            if self.game.debug:
                print(f"{ANSI.BLACK}{element = } {value = }{ANSI.RESET}")

            if E_cast_data:
                if element == E_spell_data["damage_type"]:
                    if self.game.debug: print(ANSI.wrap("Enemy: " + str(E_spell_damage), ANSI.BOLD, ANSI.BLUE))
                    E_spell_damage = round(E_spell_damage * (1 + value))
                    if self.game.debug: print(ANSI.wrap("Enemy: " + str(E_spell_damage), ANSI.BOLD, ANSI.RED))

            if P_cast_data:
                if element == P_spell_data["damage_type"]:
                    if self.game.debug: print(ANSI.wrap("Player: " + str(P_spell_damage), ANSI.BOLD, ANSI.BLUE))
                    P_spell_damage = round(P_spell_damage * (1 - value))
                    if self.game.debug: print(ANSI.wrap("Player: " + str(P_spell_damage), ANSI.BOLD, ANSI.RED))

        #!^ Player AtK
        if P_spell_damage > 0:
            self.game.enemy["hp"] -= P_spell_damage
            self.game.player_stats_base["mp"] -= P_spell_data["mp_cost"]
        if P_damage > 0:
            self.game.enemy["hp"] -= P_damage

        #!^ Enemy AtK
        if E_spell_damage > 0:
            self.game.player_stats_base["hp"] -= E_spell_damage
            self.game.enemy["mp"] -= E_spell_data["mp_cost"]
        if E_damage > 0:
            self.game.player_stats_base["hp"] -= E_damage

        #!^ MP Regen
        if self.game.player_stats_base["max_mp"] > 0:
            self.game.player_stats_base["mp"] += round(max(
                self.game.player_stats_base["max_mp"] / 15,
                (self.game.player_stats_base["max_mp"] / 10) * (1 - (self.game.player_stats_base["mp"] / self.game.player_stats_base["max_mp"]))
            ))
            if self.game.player_stats_base["mp"] > self.game.player_stats_base["max_mp"]:
                self.game.player_stats_base["mp"] = self.game.player_stats_base["max_mp"]

        if self.game.enemy["max_mp"] > 0:
            self.game.enemy["mp"] += round(max(
                self.game.enemy["max_mp"] / 15,
                (self.game.enemy["max_mp"] / 10) * (1 - (self.game.enemy["mp"] / self.game.enemy["max_mp"]))
            ))
            if self.game.enemy["mp"] > self.game.enemy["max_mp"]:
                self.game.enemy["mp"] = self.game.enemy["max_mp"]

        if self.game.log or self.game.debug:
            print(self.game.sep)
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.game.player_stats['name']} Data: {ANSI.RED}HP:{self.game.player_stats_base['hp']}/{self.game.player_stats_base['max_hp']}{ANSI.BLUE} MP:{P['MP']}/{P['MAX_MP']} {ANSI.GREEN}LVL:{P['LVL']}{ANSI.RESET}")
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.game.enemy['name']} Data: {ANSI.RED}HP:{self.game.enemy['hp']}/{self.game.enemy['max_hp']}{ANSI.BLUE} MP:{E['MP']}/{E['MAX_MP']} {ANSI.GREEN}LVL:{E['LVL']}{ANSI.RESET}")
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.game.player_stats['name']} Spell: {ANSI.YELLOW}{P_spell_data['name']}{ANSI.RESET}")
            print(f"{ANSI.CYAN}{ANSI.BOLD} {self.game.enemy['name']} Spell: {ANSI.YELLOW}{E_spell_data['name']}{ANSI.RESET}")

        #!^ death
        if self.game.player_stats_base["hp"] <= 0:
            if self.game.god_p:
                print(self.game.sep)
                print(f"{ANSI.YELLOW}{ANSI.BOLD} The Individual know as {self.game.player_stats_base['name']} has Died {ANSI.RESET}{ANSI.CURSOR_SAVE}")
                self.game.player_stats_base["hp"] = self.game.player_stats_base["max_hp"]
                self.game.player_stats_base["mp"] = self.game.player_stats_base["max_mp"]
                print(f"{ANSI.CURSOR_RESTORE}{ANSI.MAGENTA}{ANSI.BOLD} Reincarnation Compleate{ANSI.RESET}")
            else:
                print("death")

        if self.game.enemy["hp"] <= 0:
            xp_d, gold_d = E["DROP"].values()
            self.game.player_stats_base["gold"] += gold_d
            self.game.player_stats_base["xp"] += xp_d
            
            self.game.player_stats["gold"] += gold_d
            self.game.player_stats["xp"] += xp_d

            if self.game.god_e:
                print(self.game.sep)
                print(f"{ANSI.YELLOW}{ANSI.BOLD} The Individual know as {self.game.enemy['name']} has Died {ANSI.RESET}{ANSI.CURSOR_SAVE}")
                self.game.enemy["hp"] = self.game.enemy["max_hp"]
                self.game.enemy["mp"] = self.game.enemy["max_mp"]
                print(f"{ANSI.CURSOR_RESTORE}{ANSI.MAGENTA}{ANSI.BOLD} Reincarnation Compleate{ANSI.RESET}")
            else:
                self.game.shop = True
                self.game.Enemy_Generation_Logic()


#Todo Shop