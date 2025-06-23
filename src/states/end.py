import pygame

class EndState:
    def __init__(self, game):
        self.game = game
        self.font = self.game.assets.fonts["default"]
        self.button_rect = pygame.Rect(0, 0, 100, 50)  # Botão "Sair"
        self.running = True

        # Centralizar botão horizontalmente e posicionar abaixo do texto
        self.button_rect.centerx = self.game.WIDTH // 2
        self.button_rect.top = 260  # Logo abaixo do texto que estará em y=200

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.game.running = False

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((0, 0, 0))
        title_text = self.font.render("Parabéns! Você completou o jogo!", True, (255, 255, 255))
        self.game.screen.blit(title_text, (self.game.WIDTH // 2 - title_text.get_width() // 2, 200))

        pygame.draw.rect(self.game.screen, (150, 0, 0), self.button_rect)
        button_text = self.font.render("Sair", True, (255, 255, 255))
        self.game.screen.blit(button_text, (self.button_rect.centerx - button_text.get_width() // 2,
                                            self.button_rect.centery - button_text.get_height() // 2))

        pygame.display.flip()
