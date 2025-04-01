import pygame

# Função para tela de pausa
def pause(screen, font):
    pause_screen = True
    continue_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 50, 200, 50)
    quit_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 50, 200, 50)
    clock = pygame.time.Clock()

    while pause_screen:
        screen.fill((255, 255, 255))  # Fundo branco

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen = False  # Fechar a tela de pausa
                elif event.key == pygame.K_SPACE:
                    pause_screen = False  # Fechar a tela de pausa

            # Verificar se o clique é sobre os botões
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):  # Se clicado no botão "Continuar"
                    pause_screen = False
                if quit_button.collidepoint(event.pos):  # Se clicado no botão "Sair"
                    pygame.quit()
                    exit()

        # Desenho dos botões
        pygame.draw.rect(screen, (0, 255, 0), continue_button)  # Botão "Continuar" (verde)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)  # Botão "Sair" (vermelho)

        # Texto dos botões
        continue_text = font.render("Continuar", True, (0, 0, 0))
        quit_text = font.render("Sair", True, (0, 0, 0))

        # Desenhar os textos sobre os botões
        screen.blit(continue_text, (continue_button.x + 50, continue_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 80, quit_button.y + 10))

        pygame.display.flip()  # Atualiza a tela

        clock.tick(60)  # Limitar para 60 quadros por segundo
