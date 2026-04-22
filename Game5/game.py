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
        self.MAX_ACCELERATION = 4
        self.GRAVITY = 0.1
        self.DAMPING = 0.99
        self.tile_size = 16
        self.jumphight = 16

        self.vel_y = 0
        self.gravity_state = 1

        self.x = self.SCREEN_RATIO["screen_x"] // 2
        self.y = self.SCREEN_RATIO["screen_y"] // 2

        self.x = 0
        self.y = 0

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

                    if event.key == pygame.K_SPACE:
                        self.y = MOVEMENT.jump(self, self.jumphight, self.y, self.gravity_state)

                    if event.key == pygame.K_ESCAPE:
                        running = False

            keys = pygame.key.get_pressed()

            new_x = self.x
            if keys[pygame.K_a]:
                new_x -= 5
            if keys[pygame.K_d]:
                new_x += 5

            self.x = MOVEMENT.move(self, new_x)

            MOVEMENT.gravity(self, delta_time)

            self.player_rect.center = (self.x, self.y)
            self.screen.blit(self.player_sprite, self.player_rect)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()