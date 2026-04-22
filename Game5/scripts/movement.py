import pygame

def move(self, x):
    new_rect = self.player_sprite.get_rect(center=(x, self.y))

    for tile in self.tilemap.tile_map:
        tile_rect = pygame.Rect(
            tile['pos'][0] * self.tile_size,
            tile['pos'][1] * self.tile_size,
            self.tile_size,
            self.tile_size
        )

        if new_rect.colliderect(tile_rect):
            return self.x

    for tile in self.tilemap.offgrid_tiles:
        if tile.get('gravity', 1) != self.gravity_state:
            continue

        tile_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], self.tile_size, self.tile_size)
        if new_rect.colliderect(tile_rect):
            return self.x
    
    return x

def gravity(self, delta_time):
    self.vel_y += self.GRAVITY * self.gravity_state
    self.vel_y *= self.DAMPING
    self.vel_y = max(-self.MAX_ACCELERATION, min(self.MAX_ACCELERATION, self.vel_y))
    
    new_y = self.y + self.vel_y * delta_time * 60
    new_rect = self.player_sprite.get_rect(center=(self.x, new_y))
    
    for tile in self.tilemap.tile_map:
        tile_rect = pygame.Rect(
            tile['pos'][0] * self.tile_size,
            tile['pos'][1] * self.tile_size,
            self.tile_size,
            self.tile_size
        )
        
        if new_rect.colliderect(tile_rect):
            self.vel_y = 0
            return
    
    for tile in self.tilemap.offgrid_tiles:
        if tile.get('gravity', 1) != self.gravity_state:
            continue
        
        tile_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], self.tile_size, self.tile_size)
        if new_rect.colliderect(tile_rect):
            self.vel_y = 0
            return
    
<<<<<<< HEAD
    self.y = new_y

def jump(self, jumphight, y, gravity_state):
    y += jumphight * -gravity_state
    return y
=======
    self.y = new_y
>>>>>>> 1326d861f98ef8f62d1441627de72b03da835905
