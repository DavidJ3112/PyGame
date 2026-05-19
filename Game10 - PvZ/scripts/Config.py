import sys, os

parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
sys.path.append(parent_dir)

from init import *


class Configs:
    @staticmethod
    def Get_LawnConfigs():
        lawn_size: dict[str, tuple[int, int]] = {
            "glitched": (5, 9),
            "normal": (5, 9),
            "night": (5, 9),
            "pool": (6, 9),
            "fog": (6, 9),
            "roof": (5, 9),
        }

        lawn_properties: dict[str, dict] = {
            "glitched": {
                "night": False,
                "watered_rows": (3,),
                "watered_cols": (0,),
                "watered_tiles": ((3, 4), (5, 1)),
                "tilted_rows": (0,),
                "tilted_cols": (),
                "tilted_tiles": ((3, 4),),
                "tile_skin": "glitched",
            },
            "normal": {
                "night": False,
                "watered_rows": (),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (),
                "tilted_tiles": (),
                "tile_skin": "grass",
            },
            "night": {
                "night": True,
                "watered_rows": (),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (),
                "tilted_tiles": (),
                "tile_skin": "grass",
            },
            "pool": {
                "night": False,
                "watered_rows": (2, 3),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (),
                "tilted_tiles": (),
                "tile_skin": "grass",
            },
            "fog": {
                "night": True,
                "watered_rows": (2, 3),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (),
                "tilted_tiles": (),
                "tile_skin": "grass",
            },
            "roof": {
                "night": False,
                "watered_rows": (),
                "watered_cols": (),
                "watered_tiles": (),
                "tilted_rows": (),
                "tilted_cols": (0, 1),
                "tilted_tiles": (),
                "tile_skin": "roof",
            },
        }

        return lawn_size, lawn_properties

    @staticmethod
    def Get_Defaults(Key):
        if Key == "active_seeds":
            return {
                "seedslot1": None,
                "seedslot2": None,
                "seedslot3": None,
                "seedslot4": None,
                "seedslot5": None,
                "seedslot6": None,
                "seedslot7": None,
                "seedslot8": None,
                "seedslot9": None,
                "seedslot10": None,
            }
