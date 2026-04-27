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
            return 'kill'
        return None


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
            if x > self.x:  # moving right
                x = tile_rect.left - self.player_rect.width / 2
            elif x < self.x:  # moving left
                x = tile_rect.right + self.player_rect.width / 2

            self.wallhit = True
            return x, True

    self.wallhit = False
    return x, False

def gravity(self, delta_time):
    self.vel_y += self.GRAVITY * self.gravity_state
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
            if self.vel_y > 0:  # falling down
                new_y = tile_rect.top - self.player_rect.height / 2
                self.dubble_jump_used = False
            elif self.vel_y < 0:  # jumping up
                new_y = tile_rect.bottom + self.player_rect.height / 2

            self.vel_y = 0
            self.y = new_y
            return

    self.vel_y *= self.DAMPING
    self.y = new_y

def jump(self):
    if self.dubble_jump_used:
        if is_on_ground(self, offset=10):
            self.vel_y = self.jump_height * -self.gravity_state
    else:
        self.vel_y = self.jump_height * -self.gravity_state
        self.dubble_jump_used = True

def is_on_ground(self, offset):
    check_y = self.y + (offset * self.gravity_state)
    ground_rect = self.player_sprite.get_rect(center=(self.x, check_y))
    return check_collision(self, self.tilemap, self.gravity_state, self.tile_size, ground_rect)