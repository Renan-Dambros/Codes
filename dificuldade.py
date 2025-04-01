import pygame
import sys
import Trabalho  # Importa o código principal do jogo

# Inicialização do Pygame
pygame.init()

# Configuração da tela
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Escolha a Dificuldade")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Fonte
font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)

# Definição dos botões
button_width, button_height = 300, 100
easy_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 3 - 50, button_width, button_height)
medium_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 50, button_width, button_height)
hard_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 1.5 - 50, button_width, button_height)

# Função para desenhar a tela de dificuldade
def draw_difficulty_screen():
    screen.fill(WHITE)

    title_surface = font.render("Escolha a Dificuldade", True, BLUE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 6))

    pygame.draw.rect(screen, BLUE, easy_button)
    easy_text = button_font.render("Fácil", True, WHITE)
    screen.blit(easy_text, (easy_button.centerx - easy_text.get_width() // 2, easy_button.centery - easy_text.get_height() // 2))

    pygame.draw.rect(screen, BLUE, medium_button)
    medium_text = button_font.render("Médio", True, WHITE)
    screen.blit(medium_text, (medium_button.centerx - medium_text.get_width() // 2, medium_button.centery - medium_text.get_height() // 2))

    pygame.draw.rect(screen, BLUE, hard_button)
    hard_text = button_font.render("Difícil", True, WHITE)
    screen.blit(hard_text, (hard_button.centerx - hard_text.get_width() // 2, hard_button.centery - hard_text.get_height() // 2))

    pygame.display.flip()

# Função para iniciar a tela de dificuldade
def start_difficulty():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    print("Modo Fácil selecionado")
                    running = False
                    Trabalho.start_game("facil")  # Inicia o jogo no modo fácil
                elif medium_button.collidepoint(event.pos):
                    print("Modo Médio selecionado")
                    running = False
                    Trabalho.start_game("medio")  # Inicia o jogo no modo médio
                elif hard_button.collidepoint(event.pos):
                    print("Modo Difícil selecionado")
                    running = False
                    Trabalho.start_game("dificil")  # Inicia o jogo no modo difícil

        draw_difficulty_screen()
