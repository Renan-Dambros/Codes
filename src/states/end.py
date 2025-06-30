import pygame

class EndState:
    def __init__(self, game):
        self.game = game
        self.font = self.game.assets.fonts["default"]
        self.running = True
        self.diploma_image = pygame.transform.scale(
            self.game.assets.images["diploma"], 
            (self.game.WIDTH, self.game.HEIGHT)
        )
        pygame.mixer.music.stop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                screen_w, screen_h = self.game.screen.get_size()
                scale = min(screen_w / self.game.WIDTH, screen_h / self.game.HEIGHT)
                offset_x = (screen_w - self.game.WIDTH * scale) / 2
                offset_y = (screen_h - self.game.HEIGHT * scale) / 2

                game_mouse_x = (mouse_x - offset_x) / scale
                game_mouse_y = (mouse_y - offset_y) / scale

                if self.button_rect.collidepoint(game_mouse_x, game_mouse_y):
                    self.game.running = False

    def update(self):
        pass

    def render(self):
        screen_w, screen_h = self.game.screen.get_size()
        scale = min(screen_w / self.game.WIDTH, screen_h / self.game.HEIGHT)

        game_surface = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
        game_surface.blit(self.diploma_image, (0, 0))

        congrats_text = self.font.render("Parabéns! Você foi aprovado!", True, (0, 0, 0))
        text_x = (self.game.WIDTH - congrats_text.get_width()) // 2
        text_y = self.game.HEIGHT // 3
        game_surface.blit(congrats_text, (text_x, text_y))

        button_width, button_height = 150, 50
        button_x = (self.game.WIDTH - button_width) // 2
        button_y = text_y + congrats_text.get_height() + 50
        self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        pygame.draw.rect(game_surface, (150, 0, 0), self.button_rect)
        button_text = self.font.render("Sair", True, (255, 255, 255))
        text_x = self.button_rect.centerx - button_text.get_width() // 2
        text_y = self.button_rect.centery - button_text.get_height() // 2
        game_surface.blit(button_text, (text_x, text_y))

        scaled_surf = pygame.transform.smoothscale(
            game_surface,
            (int(self.game.WIDTH * scale), int(self.game.HEIGHT * scale))
        )

        offset_x = (screen_w - scaled_surf.get_width()) // 2
        offset_y = (screen_h - scaled_surf.get_height()) // 2

        self.game.screen.fill((0, 0, 0))
        self.game.screen.blit(scaled_surf, (offset_x, offset_y))
        pygame.display.flip()
