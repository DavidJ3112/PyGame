import pygame
import scripts.utils as UTILS
import scripts.movement as MOVEMENT
from scripts.tilemap import Tilemap
from scripts import debug as DEBUG

#todo gravity count (3 flips per checkpoint)
#todo save states

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption('Gravity Flip')

        self.SCREEN_RATIO = {"screen_x": 640, "screen_y": 640}
        self.screen = pygame.display.set_mode((self.SCREEN_RATIO["screen_x"], self.SCREEN_RATIO["screen_y"]))

        self.my_font = pygame.font.SysFont('arial', 30)

        self.clock = pygame.time.Clock()
        self.FPS = 24

        self.player_facing = 1
        self.player_movement_state_x = 'idle'
        self.player_movement_state_y = 'idle'

        self.BG = (255, 255, 255)
        self.MAX_ACCELERATION = 2
        self.PLAYER_ACCELERATION = 0.1
        self.GRAVITY = 0.1
        self.DAMPING = 0.99
        self.tile_size = 16
        self.jump_height = 1.3
        self.WALL_JUMP_X_BOOST = 60
        self.dubble_jump_used = False
        self.wallhit = False

        self.vel_y = 0
        self.gravity_state = 1
        self.camera_smoothing = 0.1

        self.last_gravity_state = self.gravity_state
        self.last_player_movement_state_x = self.player_movement_state_x
        self.last_player_movement_state_y = self.player_movement_state_y
        self.last_player_facing = self.player_facing

        self.x, self.y = self.x_start, self.y_start = (self.SCREEN_RATIO["screen_x"] // 2, self.SCREEN_RATIO["screen_y"] // 2)
        self.PLAYER_MAX_SPEED = 7.5

        self.new_x = self.x

        self.assets = {
            'decor': UTILS.load_images('tiles/decor'),
            'grass': UTILS.load_images('tiles/grass'),
            'large_decor': UTILS.load_images('tiles/large_decor'),
            'spawners': UTILS.load_images('tiles/spawners'),
            'stone': UTILS.load_images('tiles/stone'),
            'player': UTILS.load_image('entities/player/0.png')
        }

        self.player_sprite = self.assets['player'][0]
        self.player_rect = self.player_sprite.get_rect(center=(self.x, self.y))
        
        self.map_generated = False
        self.tilemap = Tilemap(self, tile_size=16)
        self.MAP_INDEX = 0
        self.map_generated = self.tilemap.load_map(self.MAP_INDEX)

        self.x_start, self.y_start = self.tilemap.player_spawn_points[0]

        self.camera_x = 0
        self.camera_y = 0

    def run(self):
        running = True

        while running:
            self.screen.fill(self.BG)
            delta_time = max(0.001, min(0.1, self.clock.tick(self.FPS) / 1000))

            self.camera_target_x = self.x - self.SCREEN_RATIO["screen_x"] // 2
            self.camera_target_y = self.y - self.SCREEN_RATIO["screen_y"] // 2

            self.camera_x += (self.camera_target_x - self.camera_x) * self.camera_smoothing 
            self.camera_y += (self.camera_target_y - self.camera_y) * self.camera_smoothing 

            self.tilemap.render(self.screen, self.camera_x, self.camera_y)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.gravity_state *= -1
                    
                    if event.key == pygame.K_0:
                        self.y -= 50 * self.gravity_state
                    
                    if not self.dubble_jump_used and event.key == pygame.K_SPACE:
                        MOVEMENT.jump(self)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            running = False

            self.keys = pygame.key.get_pressed()
            if not self.wallhit:
                if self.keys[pygame.K_a]:
                    self.new_x += -self.PLAYER_MAX_SPEED
                    self.player_facing = -1
                    self.player_movement_state_x = 'moving_left'
                if self.keys[pygame.K_d]:
                    self.new_x += self.PLAYER_MAX_SPEED
                    self.player_facing = 1
                    self.player_movement_state_x = 'moving_right'

            if self.dubble_jump_used and self.keys[pygame.K_SPACE]:
                MOVEMENT.jump(self)

            new_x = self.x + (self.new_x - self.x) * self.PLAYER_ACCELERATION
            if f"{new_x:.0f}" == f"{self.x:.0f}":
                self.player_movement_state_x = 'idle'

            self.player_rect.center = (self.x, self.y)
            self.player_rect = self.player_sprite.get_rect(center=(self.x, self.y + 0.25 * self.gravity_state))
            self.collision_result = MOVEMENT.check_collision(self, self.tilemap, self.gravity_state, self.tile_size, self.player_rect)
            self.player_rect = self.player_sprite.get_rect(center=(self.x, self.y))

            self.x, self.wallhit = MOVEMENT.move(self, new_x)
            MOVEMENT.gravity(self, delta_time)

            self.player_sprite = UTILS.player_sprite(self)

            if self.collision_result == 'kill':
                self.x = self.x_start
                self.new_x = self.x_start
                self.y = self.y_start
                self.vel_y = 0
                self.gravity_state = 1

            screen_player_rect = self.player_rect.copy()
            screen_player_rect.x -= self.camera_x
            screen_player_rect.y -= self.camera_y
            self.screen.blit(self.player_sprite, screen_player_rect)

            if self.map_generated:
                DEBUG.DebugPrinter.map_info(self.tilemap.debug_map_info)
                self.map_generated = False

            DEBUG.DebugPrinter.debug_info(self, debug_type = "NONE")

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()

    pygame.quit()