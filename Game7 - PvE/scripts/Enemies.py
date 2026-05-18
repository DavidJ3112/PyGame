import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI
from general_scripts.RPG.Enemy_Pool import EnemyDataBase

import random

SOFT_CAP_LEVEL = 60
LATE_GAME_DIVISOR = 4

enemy_pool = EnemyDataBase.all_enemy()

def _scale_player_level(player_lvl: int) -> int:
    if player_lvl <= SOFT_CAP_LEVEL:
        return player_lvl
    return SOFT_CAP_LEVEL + (player_lvl - SOFT_CAP_LEVEL) // LATE_GAME_DIVISOR

def round_0(x):
    return int(round(x, 0))

def round_3(x):
    return str(round(x, 3))

def generate_enemy(self, player_lvl: int):
    scaled_player = _scale_player_level(player_lvl)

    if self.debug or self.log:
        print(self.sep)

    for _ in range(20):  #!^ prevent infinite loop
        enemy_key = random.choice(list(enemy_pool.keys()))
        base = enemy_pool[enemy_key]
        #!^ boss protection
        is_boss = base.get("boss", False)

        if self.debug or self.log:
            print(f"{ANSI.rgb(255, 128, 0)}{ANSI.BOLD} Trying Enemy: {ANSI.rgb(0, 255, 255)}{enemy_key}{ANSI.rgb(255, 128, 0)} Boss: {ANSI.rgb(0, 255, 0) if is_boss else ANSI.rgb(255, 0, 0)}{is_boss}{ANSI.RESET}{ANSI.CURSOR_SAVE}")


        hp0 = base.get("base_hp", 100)
        atk0 = base.get("attack", 0)
        def0 = base.get("defense", 0)
        spd0 = base.get("speed", 0)
        mp0 = base.get("mp", 0)
        crit0 = base.get("crit", 0)
        eva0 = base.get("eva", 0)
        exp0 = base.get("exp_drop", 0)
        gold0 = base.get("gold_drop", 0)

        if is_boss:
            if player_lvl < 15:
                if self.debug or self.log:
                    print(f"{ANSI.CURSOR_RESTORE}{ANSI.wrap("   Faild, (Level Req)", ANSI.rgb(255, 0, 0), ANSI.BOLD)}")
                continue

            if random.randint(1, 100) < 30:
                if self.debug or self.log:
                    print(f"{ANSI.CURSOR_RESTORE}{ANSI.wrap("   Faild, (Chance)", ANSI.rgb(255, 0, 0), ANSI.BOLD)}")
                continue

            if self.no_boss_sinds < 10:
                if self.debug or self.log:
                    print(f"{ANSI.CURSOR_RESTORE}{ANSI.wrap("   Faild, (Boss Cooldown)", ANSI.rgb(255, 0, 0), ANSI.BOLD)}")
                continue

        if is_boss:
            self.no_boss_sinds = 0
        else:
            self.no_boss_sinds += 1


        enemy_lvl = base["base_lvl"] + scaled_player
        lvl_variation = random.randint(-1, 2)
        lvl = max(1, enemy_lvl + lvl_variation)

        #!^ --- Scaling ---
        multiplier = self.dificulty

        if base.get("boss", False):
            multiplier = self.dificulty * 1.8

        multiplier = multiplier + lvl / 5

        hp = round_0(round((hp0 * multiplier) / 5) * 5)
        attack = round_0(atk0 * multiplier)
        defense = round_0(def0 * multiplier)
        speed = round_0(spd0 * multiplier)

        mp = round_0(mp0 * multiplier)
        max_mp = mp

        crit = round_3(crit0 * multiplier)
        eva = round_3(eva0 * multiplier)

        exp_drop = round_0(exp0 * multiplier)
        gold_drop = round_0(gold0 * multiplier)

        if self.debug or self.log:
            print(f"{ANSI.CURSOR_RESTORE}{ANSI.wrap('   Success', ANSI.rgb(0, 255, 0), ANSI.BOLD)}")

        return {
            "id": enemy_key,
            "name": base["name"],
            "lvl": lvl,
            "hp": hp,
            "max_hp": hp,
            "mp": mp,
            "max_mp": max_mp,
            "attack": attack,
            "defense": defense,
            "speed": speed,
            "crit": crit,
            "eva": eva,
            "exp_drop": exp_drop,
            "gold_drop": gold_drop,
            "rarity": base["rarity"],
            "resistance": base["resistance"].copy(),
            "attack_type": base["attack_type"],
            "boss": base.get("boss", False)
        }

    raise ValueError("No valid enemy found")
