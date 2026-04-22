import pygame
import os

BASE_IMG_PATH = os.path.join(os.path.dirname(__file__), '..', 'sprites')

def load_image(image):
    sprite = pygame.image.load(os.path.join(BASE_IMG_PATH, image))
    rect: pygame.Rect = sprite.get_rect()
    return(sprite, rect)

def load_images(path):
    images = []
    full_path = os.path.join(BASE_IMG_PATH, 'images', path)

    for img_name in sorted(os.listdir(full_path)):
        img_path = os.path.join(full_path, img_name)
        sprite = pygame.image.load(img_path).convert_alpha()
        images.append(sprite)

    return images