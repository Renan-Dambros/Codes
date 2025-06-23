# src/utils/asset_loader.py

import pygame
import os

class AssetLoader:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_all(self):
        img_path = "assets/images"
        snd_path = "assets/sounds"
        fnt_path = "assets/fonts/freesansbold.ttf"

        # Carrega imagens
        for file in os.listdir(img_path):
            name, ext = os.path.splitext(file)
            if ext in [".png", ".jpg"]:
                self.images[name] = pygame.image.load(os.path.join(img_path, file)).convert_alpha()

        # Fonte padrão
        self.fonts["default"] = pygame.font.Font(fnt_path, 32)

        # Sons opcionais
        if os.path.exists(snd_path):
            for file in os.listdir(snd_path):
                name, ext = os.path.splitext(file)
                if ext == ".mp3":
                    self.sounds[name] = os.path.join(snd_path, file)
