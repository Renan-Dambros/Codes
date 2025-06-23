# src/states/pause.py

import pygame

class PauseState:
    def __init__(self, game, previous_state):
        self.game = game
        self.previous_state = previous_state
        self.font = self.game.assets.fonts["default"]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.state = self.previous_state
            elif event.type == pygame.QUIT:
                self.game.running = False

    def update(self):
        pass

    def render(self):
        self.previous_state.render()
        s = pygame.Surface((self.game.WIDTH, self.game.HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.game.screen.blit(s, (0, 0))

        text = self.font.render("PAUSADO - Pressione ESC para voltar", True, (255, 255, 255))
        self.game.screen.blit(text, (self.game.WIDTH // 2 - text.get_width() // 2, 300))
