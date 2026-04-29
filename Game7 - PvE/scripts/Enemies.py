# enemies.py
# Enemy catalog + generation logic
# Includes scaling limiter and boss protection system

import random

SOFT_CAP_LEVEL = 60
LATE_GAME_DIVISOR = 4


enemy_pool = {
    "goblin": {
        #note Hidden Stats
        #note Weakness: None Resistance: fire/ice Rarity: common
        #note attack type: Melee
        "name": "Goblin",
        "base_lvl": 1,
        "base_hp": 40,
        "attack": 6,
        "defense": 2,
        "speed": 8,
        "exp_drop": 10,
        "rarity": "common",
        "resistance": {"fire": 0.0, "ice": 0.0},
        "attack_type": "Melee",
        "boss": False
    },

    "wolf": {
        #note Hidden Stats
        #note Weakness: fire Resistance: ice Rarity: common
        #note attack type: Melee
        "name": "Wolf",
        "base_lvl": 2,
        "base_hp": 50,
        "attack": 8,
        "defense": 3,
        "speed": 12,
        "exp_drop": 14,
        "rarity": "common",
        "resistance": {"fire": -0.1, "ice": 0.1},
        "attack_type": "Melee",
        "boss": False
    },

    "orc": {
        #note Hidden Stats
        #note Weakness: None Resistance: fire Rarity: uncommon
        #note attack type: Melee
        "name": "Orc",
        "base_lvl": 3,
        "base_hp": 80,
        "attack": 12,
        "defense": 6,
        "speed": 6,
        "exp_drop": 25,
        "rarity": "uncommon",
        "resistance": {"fire": 0.1, "ice": 0.0},
        "attack_type": "Melee",
        "boss": False
    },

    "skeleton": {
        #note Hidden Stats
        #note Weakness: ice Resistance: fire Rarity: common
        #note attack type: Melee
        "name": "Skeleton",
        "base_lvl": 2,
        "base_hp": 45,
        "attack": 9,
        "defense": 4,
        "speed": 7,
        "exp_drop": 16,
        "rarity": "common",
        "resistance": {"fire": 0.2, "ice": -0.2},
        "attack_type": "Melee",
        "boss": False
    },

    "slime": {
        #note Hidden Stats
        #note Weakness: ice Resistance: fire Rarity: common
        #note attack type: Magician
        "name": "Slime",
        "base_lvl": 1,
        "base_hp": 35,
        "attack": 5,
        "defense": 1,
        "speed": 4,
        "exp_drop": 8,
        "rarity": "common",
        "resistance": {"fire": 0.3, "ice": -0.1},
        "attack_type": "Magician",
        "boss": False
    },

    "bandit": {
        #note Hidden Stats
        #note Weakness: None Resistance: none Rarity: uncommon
        #note attack type: Melee
        "name": "Bandit",
        "base_lvl": 3,
        "base_hp": 60,
        "attack": 11,
        "defense": 5,
        "speed": 10,
        "exp_drop": 22,
        "rarity": "uncommon",
        "resistance": {},
        "attack_type": "Melee",
        "boss": False
    },

    "troll": {
        #note Hidden Stats
        #note Weakness: fire Resistance: none Rarity: rare
        #note attack type: Melee
        "name": "Troll",
        "base_lvl": 5,
        "base_hp": 120,
        "attack": 18,
        "defense": 10,
        "speed": 3,
        "exp_drop": 40,
        "rarity": "rare",
        "resistance": {"fire": -0.2},
        "attack_type": "Melee",
        "boss": False
    },

    "bat": {
        #note Hidden Stats
        #note Weakness: None Resistance: none Rarity: common
        #note attack type: Melee
        "name": "Bat",
        "base_lvl": 1,
        "base_hp": 25,
        "attack": 4,
        "defense": 1,
        "speed": 14,
        "exp_drop": 6,
        "rarity": "common",
        "resistance": {},
        "attack_type": "Melee",
        "boss": False
    },

    "spider": {
        #note Hidden Stats
        #note Weakness: fire Resistance: none Rarity: common
        #note attack type: Melee
        "name": "Spider",
        "base_lvl": 2,
        "base_hp": 40,
        "attack": 7,
        "defense": 2,
        "speed": 11,
        "exp_drop": 12,
        "rarity": "common",
        "resistance": {"fire": -0.1},
        "attack_type": "Melee",
        "boss": False
    },

    "dark_mage": {
        #note Hidden Stats
        #note Weakness: None Resistance: dark/fire Rarity: rare
        #note attack type: Magician
        "name": "Dark Mage",
        "base_lvl": 6,
        "base_hp": 70,
        "attack": 20,
        "defense": 6,
        "speed": 7,
        "exp_drop": 55,
        "rarity": "rare",
        "resistance": {"dark": 0.5, "fire": 0.1},
        "attack_type": "Magician",
        "boss": False
    },

    "golem": {
        #note Hidden Stats
        #note Weakness: fire Resistance: physical Rarity: rare
        #note attack type: Melee
        "name": "Golem",
        "base_lvl": 7,
        "base_hp": 160,
        "attack": 22,
        "defense": 18,
        "speed": 2,
        "exp_drop": 70,
        "rarity": "rare",
        "resistance": {"physical": 0.3, "fire": -0.3},
        "attack_type": "Melee",
        "boss": False
    },

    "necromancer": {
        #note Hidden Stats
        #note Weakness: None Resistance: dark Rarity: epic
        #note attack type: Magician
        "name": "Necromancer",
        "base_lvl": 8,
        "base_hp": 90,
        "attack": 25,
        "defense": 8,
        "speed": 6,
        "exp_drop": 90,
        "rarity": "epic",
        "resistance": {"dark": 0.6},
        "attack_type": "Magician",
        "boss": True
    },

    "wyvern": {
        #note Hidden Stats
        #note Weakness: ice Resistance: fire Rarity: epic
        #note attack type: Melee
        "name": "Wyvern",
        "base_lvl": 9,
        "base_hp": 140,
        "attack": 28,
        "defense": 10,
        "speed": 16,
        "exp_drop": 110,
        "rarity": "epic",
        "resistance": {"fire": 0.2, "ice": -0.2},
        "attack_type": "Melee",
        "boss": True
    },

    "demon_hound": {
        #note Hidden Stats
        #note Weakness: holy Resistance: fire Rarity: rare
        #note attack type: Melee
        "name": "Demon Hound",
        "base_lvl": 6,
        "base_hp": 100,
        "attack": 24,
        "defense": 7,
        "speed": 15,
        "exp_drop": 75,
        "rarity": "rare",
        "resistance": {"fire": 0.3, "holy": -0.3},
        "attack_type": "Melee",
        "boss": False
    },

    "ancient_guardian": {
        #note Hidden Stats
        #note Weakness: None Resistance: physical/magic Rarity: legendary
        #note attack type: Melee
        "name": "Ancient Guardian",
        "base_lvl": 10,
        "base_hp": 220,
        "attack": 35,
        "defense": 25,
        "speed": 4,
        "exp_drop": 150,
        "rarity": "legendary",
        "resistance": {"physical": 0.4, "magic": 0.2},
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

        # boss protection: prevent low level players from getting destroyed instantly
        if base.get("boss", False) and player_lvl < 5:
            continue

        enemy_lvl = base["base_lvl"] + scaled_player
        lvl_variation = random.randint(-1, 2)
        lvl = max(1, enemy_lvl + lvl_variation)

        hp = base["base_hp"] + (lvl * 8)

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
