import pygame
from src.states.game import GameState

class MenuState:
    def __init__(self, game):
        self.game = game
        self.bg = pygame.transform.scale(game.assets.images["fundo1"], game.screen.get_size())
        self.font = game.assets.fonts["default"]
        
        # Novo tamanho maior para o botão
        button_width = 200
        button_height = 60
        self.play_button = pygame.Rect(
            (game.screen.get_width() // 2) - (button_width // 2),
            (game.screen.get_height() // 2),
            button_width,
            button_height
        )

        pygame.mixer.music.load(self.game.assets.sounds["menu"])
        pygame.mixer.music.play(-1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    self.game.state = GameState(self.game, "easy")

    def update(self):
        pass

    def render(self):
        self.game.screen.blit(self.bg, (0, 0))

        # Fundo verde do botão
        pygame.draw.rect(self.game.screen, (0, 150, 0), self.play_button)

        # Contorno do botão (opcional, só pra dar acabamento)
        pygame.draw.rect(self.game.screen, (255, 255, 255), self.play_button, 3)

        # Texto centralizado dentro do botão
        text = self.font.render("JOGAR", True, (255, 255, 255))
        text_x = self.play_button.centerx - text.get_width() // 2
        text_y = self.play_button.centery - text.get_height() // 2
        self.game.screen.blit(text, (text_x, text_y))

        pygame.display.flip()
