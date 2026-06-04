import pygame
import os
import pygame

BASE_IMG_PATH = os.path.join(os.path.dirname(__file__), '..', "Content", "Sprites")

class utils:
    @staticmethod
    def load_image(image):
        sprite = pygame.image.load(os.path.join(BASE_IMG_PATH, image))
        rect: pygame.Rect = sprite.get_rect()
        return(sprite, rect)

    @staticmethod
    def load_images(path):
        images = []
        full_path = os.path.join(BASE_IMG_PATH, path)

        for img_name in sorted(os.listdir(full_path)):
            img_path = os.path.join(full_path, img_name)
            sprite = pygame.image.load(img_path).convert_alpha()
            images.append(sprite)
        
        return images
    
    @staticmethod
    def load_images_dict(path):
        """
        Loads all images in a folder into a dictionary.
        Keys are the filenames without extensions (e.g., 'Peashooter', 'Sunflower').
        """
        images_dict = {}
        full_path = os.path.join(BASE_IMG_PATH, path)

        if not os.path.exists(full_path):
            print(f"WARNING: Path not found: {full_path}")
            return images_dict

        for img_name in os.listdir(full_path):
            # Skip folders or hidden files
            if os.path.isdir(os.path.join(full_path, img_name)) or img_name.startswith('.'):
                continue
                
            img_path = os.path.join(full_path, img_name)
            
            # Extract the name without extension (e.g., "Peashooter.png" -> "Peashooter")
            name_key = os.path.splitext(img_name)[0]
            
            try:
                sprite = pygame.image.load(img_path).convert_alpha()
                images_dict[name_key] = sprite
            except pygame.error as e:
                print(f"Failed to load image {img_name}: {e}")
        
        return images_dict