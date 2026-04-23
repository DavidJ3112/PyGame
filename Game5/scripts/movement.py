import pygame

def check_collision(tilemap, gravity_state, tile_size, rect):
    for tile in tilemap.tile_map:
        tile_rect = pygame.Rect(
            tile['pos'][0] * tile_size,
            tile['pos'][1] * tile_size,
            tile_size,
            tile_size
        )
        if rect.colliderect(tile_rect):
            return True
    
    for tile in tilemap.offgrid_tiles:
        if tile.get('gravity', 1) != gravity_state:
            continue
        
        tile_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], tile_size, tile_size)
        if rect.colliderect(tile_rect):
            return True
    
    return False

def move(self, x):
    new_rect = self.player_sprite.get_rect(center=(x, self.y))
    
    if check_collision(self.tilemap, self.gravity_state, self.tile_size, new_rect):
        return self.x
    
    return x

def gravity(self, delta_time):
    self.vel_y += self.GRAVITY * self.gravity_state
    self.vel_y = max(-self.MAX_ACCELERATION, min(self.MAX_ACCELERATION, self.vel_y))
    
    new_y = self.y + self.vel_y * delta_time * 60
    new_rect = self.player_sprite.get_rect(center=(self.x, new_y))
    
    if check_collision(self.tilemap, self.gravity_state, self.tile_size, new_rect):
        self.vel_y = 0
        return
    
    self.vel_y *= self.DAMPING
    self.y = new_y

def jump(self):
    if is_on_ground(self):
        self.vel_y = self.jump_height * -self.gravity_state

def is_on_ground(self):
    offset = 2
    check_y = self.y + (offset * self.gravity_state)
    ground_rect = self.player_sprite.get_rect(center=(self.x, check_y))
    return check_collision(self.tilemap, self.gravity_state, self.tile_size, ground_rect)