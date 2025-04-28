import pygame
import sys
import inicio
import dificuldade
import Trabalho

inicio.start()

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CodeQuest: A Jornada do Programador")

# Estados do jogo
STATE_INICIO = "inicio"
STATE_DIFICULDADE = "dificuldade"
STATE_JOGO = "jogo"
game_state = STATE_INICIO  # Começa na tela de início
difficulty = None  # Variável para armazenar a dificuldade escolhida

# Loop principal
running = True
while running:
    screen.fill((255, 255, 255))  # Fundo branco

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == STATE_INICIO:
                game_state = inicio.handle_events(event)  # Tela de início
            elif game_state == STATE_DIFICULDADE:
                game_state, difficulty = dificuldade.handle_events(event)  # Escolha de dificuldade
            elif game_state == STATE_JOGO:
                Trabalho.handle_events(event)  # Jogo em si

    if game_state == STATE_INICIO:
        inicio.draw(screen)
    elif game_state == STATE_DIFICULDADE:
        dificuldade.draw(screen)
    elif game_state == STATE_JOGO:
        Trabalho.draw(screen, difficulty)

    pygame.display.flip()
