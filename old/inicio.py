import pygame
import dificuldade

def start():
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("CodeQuest: A Jornada do Programador")
    
    font = pygame.font.Font(None, 72)
    title_text_1 = font.render("CodeQuest: A Jornada", True, (255, 255, 255))
    title_text_2 = font.render("do Programador", True, (255, 255, 255))
    
    button_font = pygame.font.Font(None, 48)
    button_text = button_font.render("Iniciar", True, (255, 255, 255))
    
    button_width = button_text.get_width() + 40
    button_height = button_text.get_height() + 20
    button_rect = pygame.Rect(0, 0, button_width, button_height)
    button_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)
    
    background = pygame.image.load("fundo1.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(title_text_1, (WIDTH // 2 - title_text_1.get_width() // 2, HEIGHT // 4 - 50))
        screen.blit(title_text_2, (WIDTH // 2 - title_text_2.get_width() // 2, HEIGHT // 4))
        
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            button_color = (0, 100, 255)  # Azul mais claro no hover
        else:
            button_color = (0, 0, 255)  # Azul normal
        
        pygame.draw.rect(screen, button_color, button_rect, border_radius=20)
        screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                dificuldade.start_difficulty()
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    start()