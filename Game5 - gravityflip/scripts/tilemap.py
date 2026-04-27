import pygame

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = []
        self.offgrid_tiles = []

    def load_map(self, map_index):
        self.map_generated = True
        if map_index == 0:
            from maps.map_0 import Map_0
            self.debug_map_info = Map_0(self)
        elif map_index == 1:
            from maps.map_1 import Map_1
            self.debug_map_info = Map_1(self)

        return self.map_generated

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
        
        for spawn_x, spawn_y, gravity in self.game.tilemap.player_spawn_points:
            if gravity == 1:
                pygame.draw.circle(surf, (255, 0, 0), (spawn_x - camera_x, spawn_y - camera_y), 5)
            else:
                pygame.draw.circle(surf, (255, 0, 0), (spawn_x - camera_x, spawn_y - camera_y), 5)


