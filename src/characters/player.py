# src/characters/player.py

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, assets, pos):
        super().__init__()
        self.images_down = [pygame.transform.scale(assets[f"chv{i}"], (40, 60)) for i in [1, 5, 1, 6]]
        self.images_up = [pygame.transform.scale(assets[f"chv{i}"], (40, 60)) for i in [2, 7, 2, 8]]
        self.images_left = [pygame.transform.scale(assets[f"chv{i}"], (40, 60)) for i in [3, 9, 3, 10]]
        self.images_right = [pygame.transform.scale(assets[f"chv{i}"], (40, 60)) for i in [4, 11, 4, 12]]

        self.image = self.images_down[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 5
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_delay = 7
        self.direction = "down"

    def update(self, keys, walls):
        old_pos = self.rect.topleft
        moved = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"
            moved = True
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = "up"
            moved = True
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = "down"
            moved = True

        if moved:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_delay:
                self.animation_index = (self.animation_index + 1) % 4
                self.animation_timer = 0
        else:
            self.animation_index = 0
            self.animation_timer = 0

        if self.direction == "down":
            self.image = self.images_down[self.animation_index]
        elif self.direction == "up":
            self.image = self.images_up[self.animation_index]
        elif self.direction == "left":
            self.image = self.images_left[self.animation_index]
        elif self.direction == "right":
            self.image = self.images_right[self.animation_index]

        if pygame.sprite.spritecollideany(self, walls):
            self.rect.topleft = old_pos
