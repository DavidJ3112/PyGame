import pygame
import os
import pygame

BASE_IMG_PATH = os.path.join(os.path.dirname(__file__), '..', 'sprites', 'images')

def load_image(image):
    sprite = pygame.image.load(os.path.join(BASE_IMG_PATH, image))
    rect: pygame.Rect = sprite.get_rect()
    return(sprite, rect)

def load_images(path):
    images = []
    full_path = os.path.join(BASE_IMG_PATH, path)

    for img_name in sorted(os.listdir(full_path)):
        img_path = os.path.join(full_path, img_name)
        sprite = pygame.image.load(img_path).convert_alpha()
        images.append(sprite)

    return images


def player_sprite(self):
    if self.gravity_state != self.last_gravity_state:
        if self.gravity_state == 1:
            self.last_gravity_state = self.gravity_state
            self.player_sprite = pygame.transform.flip(self.player_sprite, False, True)
        else:
            self.last_gravity_state = self.gravity_state
            self.player_sprite = pygame.transform.flip(self.player_sprite, False, True)

    if self.player_facing != self.last_player_facing:
        if self.player_facing == 1:
            self.last_player_facing = self.player_facing
            self.player_sprite = pygame.transform.flip(self.player_sprite, True, False)
        elif self.player_facing == -1:
            self.last_player_facing = self.player_facing
            self.player_sprite = pygame.transform.flip(self.player_sprite, True, False)

    return self.player_sprite