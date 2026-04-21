class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {}
        self.offgrid_tiles = []

        for i in range (10):
            self.tile_map[str(3+i) + ';10'] = {'type': 'grass', 'variant': 1, 'gravity': 1, 'pos': (3 + i, 10)}
            self.tile_map[str(3+i) + ';40'] = {'type': 'grass', 'variant': 1, 'gravity': -1, 'pos': (3 + i, 40)}
    
    def render(self, surf):
        for tile in self.offgrid_tiles:
            img = self.game.assets[tile['type']][tile['variant']]
            surf.blit(img, tile['pos'])

        for loc in self.tile_map:
            tile = self.tile_map[loc]
            img = self.game.assets[tile['type']][tile['variant']]
            surf.blit(img,(tile['pos'][0] * self.tile_size,tile['pos'][1] * self.tile_size))


