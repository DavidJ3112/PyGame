import random

SOFT_CAP_LEVEL = 60
LATE_GAME_DIVISOR = 4


enemy_pool = {
    "goblin": {
        "name": "Goblin",
        "base_lvl": 1,
        "base_hp": 40,
        "max_hp": 40,
        "mp": 5,
        "max_mp": 5,
        "attack": 6,
        "defense": 2,
        "speed": 8,
        "crit": 2,
        "eva": 5,
        "exp_drop": 10,
        "gold_drop": 5,
        "rarity": "common",
        "resistance": {"fire": 0.0, "ice": 0.0, "dark": 0.0, "holy": 0.0, "physical": 0.0},
        "attack_type": "Melee",
        "boss": False
    },

    "wolf": {
        "name": "Wolf",
        "base_lvl": 2,
        "base_hp": 50,
        "max_hp": 50,
        "mp": 0,
        "max_mp": 0,
        "attack": 8,
        "defense": 3,
        "speed": 12,
        "crit": 6,
        "eva": 10,
        "exp_drop": 14,
        "gold_drop": 6,
        "rarity": "common",
        "resistance": {"fire": -0.1, "ice": 0.1, "dark": 0.0, "holy": 0.0, "physical": 0.0},
        "attack_type": "Melee",
        "boss": False
    },

    "orc": {
        "name": "Orc",
        "base_lvl": 3,
        "base_hp": 80,
        "max_hp": 80,
        "mp": 0,
        "max_mp": 0,
        "attack": 12,
        "defense": 6,
        "speed": 6,
        "crit": 3,
        "eva": 3,
        "exp_drop": 25,
        "gold_drop": 12,
        "rarity": "uncommon",
        "resistance": {"fire": 0.1, "ice": 0.0, "dark": 0.0, "holy": 0.0, "physical": 0.0},
        "attack_type": "Melee",
        "boss": False
    },

    "skeleton": {
        "name": "Skeleton",
        "base_lvl": 2,
        "base_hp": 45,
        "max_hp": 45,
        "mp": 0,
        "max_mp": 0,
        "attack": 9,
        "defense": 4,
        "speed": 7,
        "crit": 4,
        "eva": 4,
        "exp_drop": 16,
        "gold_drop": 8,
        "rarity": "common",
        "resistance": {"fire": 0.2, "ice": -0.2, "dark": 0.2, "holy": -0.3, "physical": 0.1},
        "attack_type": "Melee",
        "boss": False
    },

    "slime": {
        "name": "Slime",
        "base_lvl": 1,
        "base_hp": 35,
        "max_hp": 35,
        "mp": 10,
        "max_mp": 10,
        "attack": 5,
        "defense": 1,
        "speed": 4,
        "crit": 1,
        "eva": 2,
        "exp_drop": 8,
        "gold_drop": 3,
        "rarity": "common",
        "resistance": {"fire": 0.3, "ice": -0.1, "dark": 0.0, "holy": 0.0, "physical": -0.1},
        "attack_type": "Magician",
        "boss": False
    },

    "bandit": {
        "name": "Bandit",
        "base_lvl": 3,
        "base_hp": 60,
        "max_hp": 60,
        "mp": 5,
        "max_mp": 5,
        "attack": 11,
        "defense": 5,
        "speed": 10,
        "crit": 7,
        "eva": 8,
        "exp_drop": 22,
        "gold_drop": 20,
        "rarity": "uncommon",
        "resistance": {"fire": 0.0, "ice": 0.0, "dark": 0.0, "holy": 0.0, "physical": 0.0},
        "attack_type": "Melee",
        "boss": False
    },

    "troll": {
        "name": "Troll",
        "base_lvl": 5,
        "base_hp": 120,
        "max_hp": 120,
        "mp": 0,
        "max_mp": 0,
        "attack": 18,
        "defense": 10,
        "speed": 3,
        "crit": 2,
        "eva": 1,
        "exp_drop": 40,
        "gold_drop": 18,
        "rarity": "rare",
        "resistance": {"fire": -0.2, "ice": 0.1, "dark": 0.0, "holy": 0.0, "physical": 0.2},
        "attack_type": "Melee",
        "boss": False
    },

    "bat": {
        "name": "Bat",
        "base_lvl": 1,
        "base_hp": 25,
        "max_hp": 25,
        "mp": 0,
        "max_mp": 0,
        "attack": 4,
        "defense": 1,
        "speed": 14,
        "crit": 5,
        "eva": 15,
        "exp_drop": 6,
        "gold_drop": 2,
        "rarity": "common",
        "resistance": {"fire": 0.0, "ice": 0.0, "dark": 0.1, "holy": -0.1, "physical": 0.0},
        "attack_type": "Melee",
        "boss": False
    },

    "spider": {
        "name": "Spider",
        "base_lvl": 2,
        "base_hp": 40,
        "max_hp": 40,
        "mp": 0,
        "max_mp": 0,
        "attack": 7,
        "defense": 2,
        "speed": 11,
        "crit": 6,
        "eva": 9,
        "exp_drop": 12,
        "gold_drop": 5,
        "rarity": "common",
        "resistance": {"fire": -0.1, "ice": 0.0, "dark": 0.0, "holy": 0.0, "physical": 0.0},
        "attack_type": "Melee",
        "boss": False
    },

    "dark_mage": {
        "name": "Dark Mage",
        "base_lvl": 6,
        "base_hp": 70,
        "max_hp": 70,
        "mp": 40,
        "max_mp": 40,
        "attack": 20,
        "defense": 6,
        "speed": 7,
        "crit": 10,
        "eva": 5,
        "exp_drop": 55,
        "gold_drop": 30,
        "rarity": "rare",
        "resistance": {"fire": 0.1, "ice": 0.0, "dark": 0.5, "holy": -0.2, "physical": 0.0},
        "attack_type": "Magician",
        "boss": False
    },

    "golem": {
        "name": "Golem",
        "base_lvl": 7,
        "base_hp": 160,
        "max_hp": 160,
        "mp": 0,
        "max_mp": 0,
        "attack": 22,
        "defense": 18,
        "speed": 2,
        "crit": 1,
        "eva": 0,
        "exp_drop": 70,
        "gold_drop": 40,
        "rarity": "rare",
        "resistance": {"fire": -0.3, "ice": 0.2, "dark": 0.0, "holy": 0.0, "physical": 0.3},
        "attack_type": "Melee",
        "boss": False
    },

    "necromancer": {
        "name": "Necromancer",
        "base_lvl": 8,
        "base_hp": 90,
        "max_hp": 90,
        "mp": 60,
        "max_mp": 60,
        "attack": 25,
        "defense": 8,
        "speed": 6,
        "crit": 12,
        "eva": 4,
        "exp_drop": 90,
        "gold_drop": 60,
        "rarity": "epic",
        "resistance": {"fire": 0.0, "ice": 0.0, "dark": 0.6, "holy": -0.4, "physical": 0.0},
        "attack_type": "Magician",
        "boss": True
    },

    "wyvern": {
        "name": "Wyvern",
        "base_lvl": 9,
        "base_hp": 140,
        "max_hp": 140,
        "mp": 20,
        "max_mp": 20,
        "attack": 28,
        "defense": 10,
        "speed": 16,
        "crit": 9,
        "eva": 12,
        "exp_drop": 110,
        "gold_drop": 80,
        "rarity": "epic",
        "resistance": {"fire": 0.2, "ice": -0.2, "dark": 0.0, "holy": 0.0, "physical": 0.1},
        "attack_type": "Melee",
        "boss": True
    },

    "demon_hound": {
        "name": "Demon Hound",
        "base_lvl": 6,
        "base_hp": 100,
        "max_hp": 100,
        "mp": 10,
        "max_mp": 10,
        "attack": 24,
        "defense": 7,
        "speed": 15,
        "crit": 8,
        "eva": 11,
        "exp_drop": 75,
        "gold_drop": 35,
        "rarity": "rare",
        "resistance": {"fire": 0.3, "ice": 0.0, "dark": 0.2, "holy": -0.3, "physical": 0.0},
        "attack_type": "Melee",
        "boss": False
    },

    "ancient_guardian": {
        "name": "Ancient Guardian",
        "base_lvl": 10,
        "base_hp": 220,
        "max_hp": 220,
        "mp": 30,
        "max_mp": 30,
        "attack": 35,
        "defense": 25,
        "speed": 4,
        "crit": 5,
        "eva": 2,
        "exp_drop": 150,
        "gold_drop": 120,
        "rarity": "legendary",
        "resistance": {"fire": 0.0, "ice": 0.0, "dark": 0.2, "holy": 0.2, "physical": 0.4},
        "attack_type": "Melee",
        "boss": True
    }
}

def _scale_player_level(player_lvl: int) -> int:
    if player_lvl <= SOFT_CAP_LEVEL:
        return player_lvl
    return SOFT_CAP_LEVEL + (player_lvl - SOFT_CAP_LEVEL) // LATE_GAME_DIVISOR


def generate_enemy(player_lvl: int):
    scaled_player = _scale_player_level(player_lvl)

    while True:
        enemy_key = random.choice(list(enemy_pool.keys()))
        base = enemy_pool[enemy_key]

        #!^ boss protection: prevent low level players from getting destroyed instantly
        if base.get("boss", False) and player_lvl < 5:
            continue

        enemy_lvl = base["base_lvl"] + scaled_player
        lvl_variation = random.randint(-1, 2)
        lvl = max(1, enemy_lvl + lvl_variation)

        hp = base["base_hp"] + (lvl * 8)
        hp = round(hp / 5) * 5


        return {
            "id": enemy_key,
            "name": base["name"],
            "lvl": lvl,
            "hp": hp,
            "max_hp": hp,
            "attack": base["attack"],
            "defense": base["defense"],
            "speed": base["speed"],
            "exp_drop": base["exp_drop"],
            "rarity": base["rarity"],
            "resistance": base["resistance"],
            "attack_type": base["attack_type"],
            "boss": base.get("boss", False)
        }
