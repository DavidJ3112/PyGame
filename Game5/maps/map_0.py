def Map_0(self):
    self.player_spawn_points = [(100, 296), (100, 300), (300, 100), (300, 300)]

    print(f"Map 0 loaded, spawn point: {self.player_spawn_points[0]}")

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

    for i in range(40):
        self.tile_map.append({'type': 'grass', 'variant': 0, 'gravity': 1, 'player_kill': True, 'pos': (i, 39)})