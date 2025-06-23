# src/states/dificuldade.py

import pygame
from src.states.game import GameState

class DifficultyState:
    def __init__(self, game):
        self.game = game
        self.font = game.assets.fonts["default"]
        self.buttons = {
            "Fácil": pygame.Rect(860, 300, 200, 60),
            "Médio": pygame.Rect(860, 400, 200, 60),
            "Difícil": pygame.Rect(860, 500, 200, 60)
        }

    def handle_events(self):
        difficulty_map = {
            "fácil": "easy",
            "médio": "medium",
            "difícil": "hard"
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for difficulty, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        selected = difficulty.lower()
                        mapped_difficulty = difficulty_map.get(selected, "easy")  # Default para easy se der problema
                        self.game.state = GameState(self.game, mapped_difficulty)
                        return

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((30, 30, 30))
        title = self.font.render("Escolha a Dificuldade", True, (255, 255, 255))
        self.game.screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 200))

        for text, rect in self.buttons.items():
            pygame.draw.rect(self.game.screen, (0, 0, 0), rect)
            label = self.font.render(text, True, (255, 255, 255))
            self.game.screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))
