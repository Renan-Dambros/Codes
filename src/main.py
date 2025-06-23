# main.py

import pygame
from src.states.menu import MenuState

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("CodeQuest: A Jornada do Programador")
        self.clock = pygame.time.Clock()
        self.running = True

        from src.utils.asset_loader import AssetLoader
        self.assets = AssetLoader()
        self.assets.load_all()

        self.state = MenuState(self)

    def run(self):
        while self.running:
            self.state.handle_events()
            self.state.update()
            self.state.render()
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

if __name__ == "__main__":
    Game().run()
