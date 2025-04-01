import pygame
import sys

# Função para reproduzir a música de fundo
def play_music():
    pygame.mixer.music.load("musica.mpeg")  # Coloque o arquivo de áudio na mesma pasta do script
    pygame.mixer.music.set_volume(0.5)  # Define o volume (de 0.0 a 1.0)
    pygame.mixer.music.play(-1, 0.0)  # Reproduz o áudio em loop

# Função para parar a música
def stop_music():
    pygame.mixer.music.stop()

# Inicialização do Pygame
pygame.init()

# Carregar o áudio de fundo
play_music()

# Configurações da tela
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CodeQuest: A Jornada do Programador")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Fonte
font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)

# Definir o botão
button_width, button_height = 300, 100
button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2, button_width, button_height)

# Função para desenhar a tela inicial
def draw_start_screen():
    screen.fill(WHITE)

    # Texto do título
    title_surface = font.render("CodeQuest: A Jornada do Programador", True, BLUE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 4))

    # Desenhar o botão "Iniciar"
    pygame.draw.rect(screen, BLUE, button_rect)
    start_text = button_font.render("Iniciar", True, WHITE)
    screen.blit(start_text, (button_rect.centerx - start_text.get_width() // 2, button_rect.centery - start_text.get_height() // 2))

    pygame.display.flip()

# Função para executar o código do jogo (Trabalho.py)
def start_game():
    stop_music()  # Para a música ao executar o jogo
    import Trabalho  # Aqui, você importa o código do jogo (Trabalho.py)

# Loop principal do menu inicial
def start():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    start_game()  # Chama a função para iniciar o jogo

        draw_start_screen()

# Iniciar o jogo
start()
