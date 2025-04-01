import pygame

def draw_button(screen, text, x, y, width, height, color, font):
    """Função para desenhar um botão com o texto dado."""
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

def start_pause(screen, WIDTH, HEIGHT):
    paused = True
    font = pygame.font.Font(None, 36)
    button_width, button_height = 200, 50

    while paused:
        screen.fill((255, 255, 255))  # Cor de fundo da tela de pausa
        
        # Desenhando botões
        draw_button(screen, "Continuar", WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height - 10, button_width, button_height, (0, 128, 0), font)
        draw_button(screen, "Sair", WIDTH // 2 - button_width // 2, HEIGHT // 2 + 10, button_width, button_height, (200, 0, 0), font)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Aperte ESC para retomar o jogo
                    paused = False
                elif event.key == pygame.K_q:  # Aperte Q para sair do jogo
                    pygame.quit()
                    quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Verifica se o botão de "Continuar" foi clicado
                if (WIDTH // 2 - button_width // 2 <= mouse_x <= WIDTH // 2 + button_width // 2) and \
                   (HEIGHT // 2 - button_height - 10 <= mouse_y <= HEIGHT // 2 - 10):
                    paused = False
                
                # Verifica se o botão de "Sair" foi clicado
                elif (WIDTH // 2 - button_width // 2 <= mouse_x <= WIDTH // 2 + button_width // 2) and \
                     (HEIGHT // 2 + 10 <= mouse_y <= HEIGHT // 2 + 10 + button_height):
                    pygame.quit()
                    quit()

        pygame.display.flip()
        pygame.time.Clock().tick(30)
