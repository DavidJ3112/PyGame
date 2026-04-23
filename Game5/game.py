import pygame
import scripts.utils as UTILS
import scripts.movement as MOVEMENT
from scripts.tilemap import Tilemap

#todo gravity count (3 flips per checkpoint)
#todo normal jumping
#todo save states

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption('Gravity Flip')

        self.SCREEN_RATIO = {"screen_x": 640, "screen_y": 640}
        self.screen = pygame.display.set_mode((self.SCREEN_RATIO["screen_x"], self.SCREEN_RATIO["screen_y"]))

        self.clock = pygame.time.Clock()
        self.FPS = 24

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

        self.x =self.x_start = self.SCREEN_RATIO["screen_x"] // 2
        self.y = self.y_start = self.SCREEN_RATIO["screen_y"] // 2
        self.PLAYER_MAX_SPEED = 7.5

        self.new_x = self.x

        self.assets = {
            'decor': UTILS.load_images('tiles/decor'),
            'grass': UTILS.load_images('tiles/grass'),
            'large_decor': UTILS.load_images('tiles/large_decor'),
            'spawners': UTILS.load_images('tiles/spawners'),
            'stone': UTILS.load_images('tiles/stone'),
            'player': UTILS.load_image('player.png')
        }

        self.player_sprite = self.assets['player'][0]
        self.player_rect = self.player_sprite.get_rect(center=(self.x, self.y))
        
        self.tilemap = Tilemap(self, tile_size=16)

    def run(self):
        running = True

        while running:
            delta_time = max(0.001, min(0.1, self.clock.tick(self.FPS) / 1000))

            self.screen.fill(self.BG)
            
            self.tilemap.render(self.screen)

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
                if self.keys[pygame.K_d]:
                    self.new_x += self.PLAYER_MAX_SPEED

            if self.dubble_jump_used and self.keys[pygame.K_SPACE]:
                MOVEMENT.jump(self)

            new_x = self.x + (self.new_x - self.x) * self.PLAYER_ACCELERATION


            self.x, self.wallhit = MOVEMENT.move(self, new_x)
            MOVEMENT.gravity(self, delta_time)

            self.player_rect.center = (self.x, self.y)

            if MOVEMENT.check_collision(self, self.tilemap, self.gravity_state, self.tile_size, self.player_rect) == 'kill':
                self.x = self.x_start
                self.y = self.y_start
                self.vel_y = 0
                self.gravity_state = 1

            self.screen.blit(self.player_sprite, self.player_rect)

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()

    pygame.quit()