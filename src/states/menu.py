import pygame
from src.states.game import GameState

class MenuState:
    def __init__(self, game):
        self.game = game
        self.bg = pygame.transform.scale(game.assets.images["fundo1"], game.screen.get_size())
        self.font = game.assets.fonts["default"]
        self.play_button = pygame.Rect(game.screen.get_width()//2 - 50, game.screen.get_height()//2, 100, 40)

        pygame.mixer.music.load(self.game.assets.sounds["menu"])
        pygame.mixer.music.play(-1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    # Vai direto pro easy
                    self.game.state = GameState(self.game, "easy")

    def update(self):
        pass

    def render(self):
        self.game.screen.blit(self.bg, (0, 0))
        text = self.font.render("JOGAR", True, (255, 255, 255))
        self.game.screen.blit(text, (self.play_button.centerx - text.get_width()//2, self.play_button.centery - text.get_height()//2))
