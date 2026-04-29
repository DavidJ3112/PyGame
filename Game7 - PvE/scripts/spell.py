# spells.py
# Centralized spell definitions to keep Game class clean
# Now with a proper spell catalog instead of sad fireball monopoly

spells = {
    "fireball": {
        "name": "Fire Ball",
        "mp_cost": 5,
        "enemy_dmg": 25,
        "cast_time": 1.2,
        "cooldown": 2.5,
        "range": 300,
        "aoe_radius": 40,
        "accuracy": 0.85,
        "projectile_speed": 8,
        "damage_type": "fire",
        "burn_chance": 0.3,
        "burn_duration": 3,
        "self_damage": 0
    },

    "ice_shard": {
        "name": "Ice Shard",
        "mp_cost": 6,
        "enemy_dmg": 20,
        "cast_time": 1.0,
        "cooldown": 2.0,
        "range": 280,
        "aoe_radius": 0,
        "accuracy": 0.9,
        "projectile_speed": 10,
        "damage_type": "ice",
        "slow_chance": 0.4,
        "slow_duration": 2,
        "self_damage": 0
    },

    "lightning_bolt": {
        "name": "Lightning Bolt",
        "mp_cost": 8,
        "enemy_dmg": 30,
        "cast_time": 1.5,
        "cooldown": 3.0,
        "range": 350,
        "aoe_radius": 0,
        "accuracy": 0.8,
        "projectile_speed": 14,
        "damage_type": "electric",
        "stun_chance": 0.25,
        "stun_duration": 1,
        "self_damage": 0
    },

    "poison_dart": {
        "name": "Poison Dart",
        "mp_cost": 4,
        "enemy_dmg": 10,
        "cast_time": 0.8,
        "cooldown": 1.5,
        "range": 320,
        "aoe_radius": 0,
        "accuracy": 0.95,
        "projectile_speed": 12,
        "damage_type": "poison",
        "poison_damage": 5,
        "poison_duration": 4,
        "self_damage": 0
    },

    "arcane_blast": {
        "name": "Arcane Blast",
        "mp_cost": 10,
        "enemy_dmg": 40,
        "cast_time": 2.0,
        "cooldown": 4.0,
        "range": 250,
        "aoe_radius": 60,
        "accuracy": 0.75,
        "projectile_speed": 6,
        "damage_type": "arcane",
        "self_damage": 0
    },

    "heal": {
        "name": "Heal",
        "mp_cost": 6,
        "enemy_dmg": 0,
        "heal_amount": 25,
        "cast_time": 1.5,
        "cooldown": 3.0,
        "range": 0,
        "aoe_radius": 0,
        "damage_type": "holy",
        "self_damage": 0
    },

    "meteor": {
        "name": "Meteor",
        "mp_cost": 15,
        "enemy_dmg": 55,
        "cast_time": 3.0,
        "cooldown": 6.0,
        "range": 400,
        "aoe_radius": 90,
        "accuracy": 0.7,
        "projectile_speed": 4,
        "damage_type": "fire",
        "burn_chance": 0.6,
        "burn_duration": 5,
        "self_damage": 0
    },

    "wind_slash": {
        "name": "Wind Slash",
        "mp_cost": 5,
        "enemy_dmg": 18,
        "cast_time": 0.6,
        "cooldown": 1.8,
        "range": 260,
        "aoe_radius": 0,
        "accuracy": 0.9,
        "projectile_speed": 16,
        "damage_type": "wind",
        "knockback": 15,
        "self_damage": 0
    },

    "earth_spike": {
        "name": "Earth Spike",
        "mp_cost": 7,
        "enemy_dmg": 28,
        "cast_time": 1.8,
        "cooldown": 3.5,
        "range": 240,
        "aoe_radius": 30,
        "accuracy": 0.8,
        "projectile_speed": 5,
        "damage_type": "earth",
        "stun_chance": 0.2,
        "stun_duration": 1,
        "self_damage": 0
    },

    "shadow_bolt": {
        "name": "Shadow Bolt",
        "mp_cost": 9,
        "enemy_dmg": 35,
        "cast_time": 1.3,
        "cooldown": 3.0,
        "range": 330,
        "aoe_radius": 0,
        "accuracy": 0.85,
        "projectile_speed": 11,
        "damage_type": "dark",
        "lifesteal": 0.2,
        "self_damage": 0
    },

    "holy_light": {
        "name": "Holy Light",
        "mp_cost": 10,
        "enemy_dmg": 20,
        "heal_amount": 20,
        "cast_time": 2.0,
        "cooldown": 4.0,
        "range": 300,
        "aoe_radius": 50,
        "accuracy": 0.8,
        "projectile_speed": 7,
        "damage_type": "holy",
        "self_damage": 0
    },

    "chain_lightning": {
        "name": "Chain Lightning",
        "mp_cost": 12,
        "enemy_dmg": 22,
        "cast_time": 1.6,
        "cooldown": 4.5,
        "range": 340,
        "aoe_radius": 0,
        "accuracy": 0.9,
        "projectile_speed": 13,
        "damage_type": "electric",
        "chain_targets": 3,
        "self_damage": 0
    },

    "blood_pact": {
        "name": "Blood Pact",
        "mp_cost": 0,
        "enemy_dmg": 45,
        "cast_time": 2.5,
        "cooldown": 6.0,
        "range": 280,
        "aoe_radius": 0,
        "accuracy": 0.75,
        "projectile_speed": 6,
        "damage_type": "blood",
        "self_damage": 15
    },

    "frost_nova": {
        "name": "Frost Nova",
        "mp_cost": 11,
        "enemy_dmg": 15,
        "cast_time": 1.4,
        "cooldown": 5.0,
        "range": 0,
        "aoe_radius": 120,
        "accuracy": 1.0,
        "projectile_speed": 0,
        "damage_type": "ice",
        "slow_chance": 1.0,
        "slow_duration": 3,
        "self_damage": 0
    },

    "inferno_pulse": {
        "name": "Inferno Pulse",
        "mp_cost": 14,
        "enemy_dmg": 50,
        "cast_time": 2.2,
        "cooldown": 5.5,
        "range": 260,
        "aoe_radius": 80,
        "accuracy": 0.78,
        "projectile_speed": 5,
        "damage_type": "fire",
        "burn_chance": 0.5,
        "burn_duration": 4,
        "self_damage": 5
    }
}

def get_spell(name: str):
    return spells.get(name)


def all_spells():
    return spells
