import sys, os

parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
sys.path.append(parent_dir)

from init import *


class Load_Data:
    def __init__(self) -> None:
        key = SaveLoad.generate_key_from_string("PvZ_Skeered")
        config_path = SaveLoad.get_save_path(name="config", folder_type="Configs")
        save_path = SaveLoad.get_save_path(name="save", folder_type="Saves")
        statistics_path = SaveLoad.get_save_path(name="statistics", folder_type="Saves")
        self.config = SaveLoad.load(config_path, log=False)
        self.save = SaveLoad.load(save_path, key=key, encrypted=False, log=False)
        self.statistics = SaveLoad.load(
            statistics_path, key=key, encrypted=False, log=False
        )

    def LoadData(self, game):
        if self.statistics:
            game.statistics = self.statistics
        else:
            game.statistics = {}

        if self.save:
            game.save_data = self.save
        else:
            game.save_data = {
                "unlocked_seeds": 0,
                "current_level": 1,
                "coin_count": 0,
                "shop": {
                    ## --- EXTRA SEED SLOTS ---
                    "seed_slot_7": {
                        "unlocked": False,
                        "price": 750,
                        "enabled": True,
                        "req": None,
                    },
                    "seed_slot_8": {
                        "unlocked": False,
                        "price": 5000,
                        "enabled": False,
                        "req": "seed_slot_7",
                    },
                    "seed_slot_9": {
                        "unlocked": False,
                        "price": 20000,
                        "enabled": False,
                        "req": "seed_slot_8",
                    },
                    "seed_slot_10": {
                        "unlocked": False,
                        "price": 80000,
                        "enabled": False,
                        "req": "seed_slot_9",
                    },
                    ## --- EXTRA DEFENSES ---
                    "pool_cleaner": {
                        "unlocked": False,
                        "price": 1000,
                        "enabled": True,
                        "req": "level_3_1",
                    },
                    "garden_rake": {
                        "unlocked": False,
                        "price": 200,
                        "enabled": True,
                        "req": None,
                        "uses": 3,
                    },
                    "roof_cleaner": {
                        "unlocked": False,
                        "price": 3000,
                        "enabled": True,
                        "req": "level_5_1",
                    },
                    ## --- UPGRADES ---
                    #!$ Available after Level 3-4
                    "gatling_pea": {
                        "unlocked": False,
                        "price": 5000,
                        "enabled": False,
                        "req": "level_3_4",
                    },
                    "twin_sunflower": {
                        "unlocked": False,
                        "price": 5000,
                        "enabled": False,
                        "req": "level_3_4",
                    },
                    #!$ Available after Level 4-4
                    "gloom_shroom": {
                        "unlocked": False,
                        "price": 7500,
                        "enabled": False,
                        "req": "level_4_4",
                    },
                    "cattail": {
                        "unlocked": False,
                        "price": 10000,
                        "enabled": False,
                        "req": "level_4_4",
                    },
                    #!$ Available after Level 5-1
                    "spikerock": {
                        "unlocked": False,
                        "price": 7500,
                        "enabled": False,
                        "req": "level_5_1",
                    },
                    "gold_magnet": {
                        "unlocked": False,
                        "price": 3000,
                        "enabled": False,
                        "req": "level_5_1",
                    },
                    #!$ Available after Level 5-10
                    "winter_melon": {
                        "unlocked": False,
                        "price": 10000,
                        "enabled": False,
                        "req": "level_5_10",
                    },
                    "cob_cannon": {
                        "unlocked": False,
                        "price": 20000,
                        "enabled": False,
                        "req": "level_5_10",
                    },
                },
                "unlocked_slots": {
                    f"seedslot{i}": (True if i <= 6 else False) for i in range(1, 11)
                },
            }

        if self.config:
            game.config = self.config
        else:
            game.config = {}


class Save_Data:
    @staticmethod
    def Save_Data(config, save, statistics):
        key = SaveLoad.generate_key_from_string("PvZ_Skeered")
        config_path = SaveLoad.get_save_path(name="config", folder_type="Configs")
        save_path = SaveLoad.get_save_path(name="save", folder_type="Saves")
        statistics_path = SaveLoad.get_save_path(name="statistics", folder_type="Saves")

        SaveLoad.save(config_path, config, log=False)
        SaveLoad.save(save_path, save, key=key, encrypt=False, log=False)
        SaveLoad.save(statistics_path, statistics, key=key, encrypt=False, log=False)
