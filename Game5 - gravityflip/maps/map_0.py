import sys, os

BASE_DIR = os.path.dirname(__file__)
PARENT = os.path.abspath(os.path.join(BASE_DIR, '..'))
ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))

sys.path.extend([PARENT, ROOT])

from general_scripts.ANSI import ANSI

def Map_0(self):
    self.player_spawn_points = [(100, 296, 1), (400, 296, 1), (100, 100, -1), (400, 100, -1)]

    for i in range(10):
        self.tile_map.append({'type': 'grass', 'variant': 1, 'gravity': 1, 'player_kill': False, 'pos': (3 + i, 20)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'player_kill': False, 'pos': (3 + i, 21)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'player_kill': False, 'pos': (3 + i, 22)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'player_kill': False, 'pos': (3 + i, 23)})
        self.tile_map.append({'type': 'grass', 'variant': 1, 'gravity': 1, 'player_kill': False, 'pos': (20 + i, 20)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'player_kill': False, 'pos': (20 + i, 21)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'player_kill': False, 'pos': (20 + i, 22)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'player_kill': False, 'pos': (20 + i, 23)})

        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'player_kill': False, 'pos': (3 + i, 0)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'player_kill': False, 'pos': (3 + i, 1)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'player_kill': False, 'pos': (3 + i, 2)})
        self.tile_map.append({'type': 'grass', 'variant': 1, 'gravity': -1, 'player_kill': False, 'pos': (3 + i, 3)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'player_kill': False, 'pos': (20 + i, 0)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'player_kill': False, 'pos': (20 + i, 1)})
        self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'player_kill': False, 'pos': (20 + i, 2)})
        self.tile_map.append({'type': 'grass', 'variant': 1, 'gravity': -1, 'player_kill': False, 'pos': (20 + i, 3)})

    for i in range(420):
        self.tile_map.append({'type': 'death_zones', 'variant': 0, 'gravity': 1, 'player_kill': True, 'pos': (i-220, 60)})

    debug_map_info = (
        f"{ANSI.GREEN}Map 0 loaded with {len(self.tile_map)} tiles and {len(self.offgrid_tiles)} offgrid tiles.{ANSI.RESET}"
        f"{ANSI.NEW_LINE}{ANSI.CYAN}Player spawn points: {', '.join([f'({x}, {y}, {gravity})' for x, y, gravity in self.player_spawn_points])}{ANSI.RESET}"
    )

    return debug_map_info