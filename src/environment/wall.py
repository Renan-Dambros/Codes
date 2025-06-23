import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
