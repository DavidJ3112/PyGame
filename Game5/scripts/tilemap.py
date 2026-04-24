import pygame

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = []
        self.offgrid_tiles = []

    def load_map(self, map_index):
        if map_index == 0:
            from maps.map_0 import Map_0
            Map_0(self)

    def render(self, surf, camera_x, camera_y):
        for tile in self.offgrid_tiles:
            img = self.game.assets[tile['type']][tile['variant']]
            surf.blit(img, (tile['pos'][0] - camera_x, tile['pos'][1] - camera_y))

        for tile in self.tile_map:
            img = self.game.assets[tile['type']][tile['variant']]
            if tile['gravity'] == 1:
                surf.blit(img, (tile['pos'][0] * self.tile_size - camera_x, tile['pos'][1] * self.tile_size - camera_y))

            if tile['gravity'] == -1:
                img = pygame.transform.rotate(img, 180)
                surf.blit(img, (tile['pos'][0] * self.tile_size - camera_x, tile['pos'][1] * self.tile_size - camera_y))


