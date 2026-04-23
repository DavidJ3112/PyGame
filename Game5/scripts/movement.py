import pygame

def check_collision(self, tilemap, gravity_state, tile_size, rect):
    for tile in tilemap.tile_map:
        tile_rect = pygame.Rect(
            tile['pos'][0] * tile_size,
            tile['pos'][1] * tile_size,
            tile_size,
            tile_size
        )

        if rect.colliderect(tile_rect):
            self.dubble_jump_used = False
            if tile.get('player_kill', False):
                return 'kill'
            return 'collision'
    
    for tile in tilemap.offgrid_tiles:
        if tile.get('gravity', 1) != gravity_state:
            continue
        
        tile_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], tile_size, tile_size)
        if rect.colliderect(tile_rect):
            return True
    
    return False

def move(self, x):
    new_rect = self.player_sprite.get_rect(center=(x, self.y))
    
    collision = check_collision(self, self.tilemap, self.gravity_state, self.tile_size, new_rect)
    if collision == 'collision':
        return self.x, True
    
    return x, False

def gravity(self, delta_time):
    self.vel_y += self.GRAVITY * self.gravity_state
    self.vel_y = max(-self.MAX_ACCELERATION, min(self.MAX_ACCELERATION, self.vel_y))
    
    new_y = self.y + self.vel_y * delta_time * 60
    new_rect = self.player_sprite.get_rect(center=(self.x, new_y))
    
    collision = check_collision(self, self.tilemap, self.gravity_state, self.tile_size, new_rect)
    if collision == 'collision':
        self.vel_y = 0
        return
    
    self.vel_y *= self.DAMPING
    self.y = new_y

def jump(self):
    if self.dubble_jump_used:
        if is_on_ground(self, offset=10):
            self.vel_y = self.jump_height * -self.gravity_state
    else:
        self.vel_y = self.jump_height * -self.gravity_state
        if self.wallhit:
            self.new_x += self.WALL_JUMP_X_BOOST * (1 if self.keys[pygame.K_d] else -1 if self.keys[pygame.K_a] else 0)
        self.dubble_jump_used = True

def is_on_ground(self, offset):
    check_y = self.y + (offset * self.gravity_state)
    ground_rect = self.player_sprite.get_rect(center=(self.x, check_y))
    return check_collision(self, self.tilemap, self.gravity_state, self.tile_size, ground_rect)