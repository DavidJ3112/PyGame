import pygame

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = []
        self.offgrid_tiles = []

        for i in range(10):
            self.tile_map.append({'type': 'grass', 'variant': 1, 'gravity': 1, 'pos': (3 + i, 20)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'pos': (3 + i, 21)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'pos': (3 + i, 22)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'pos': (3 + i, 23)})
            self.tile_map.append({'type': 'grass', 'variant': 1, 'gravity': 1, 'pos': (20 + i, 20)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'pos': (20 + i, 21)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'pos': (20 + i, 22)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': 1, 'pos': (20 + i, 23)})

            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'pos': (3 + i, 0)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'pos': (3 + i, 1)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'pos': (3 + i, 2)})
            self.tile_map.append({'type': 'grass', 'variant': 1, 'gravity': -1, 'pos': (3 + i, 3)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'pos': (20 + i, 0)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'pos': (20 + i, 1)})
            self.tile_map.append({'type': 'stone', 'variant': 1, 'gravity': -1, 'pos': (20 + i, 2)})
            self.tile_map.append({'type': 'grass', 'variant': 1, 'gravity': -1, 'pos': (20 + i, 3)})
    
    def render(self, surf):
        for tile in self.offgrid_tiles:
            img = self.game.assets[tile['type']][tile['variant']]
            surf.blit(img, tile['pos'])

        for tile in self.tile_map:
            img = self.game.assets[tile['type']][tile['variant']]
            if tile['gravity'] == 1:
                surf.blit(img, (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

            if tile['gravity'] == -1:
                img = pygame.transform.rotate(img, 180)
                surf.blit(img, (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))


