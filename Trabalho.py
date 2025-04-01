import pygame
import random
import pause  # Importa o código da tela de pausa

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CodeQuest: A Jornada do Programador")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (200, 0, 0)

# Fonte
font = pygame.font.Font(None, 36)

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
    
    def update(self, keys, npcs):
        old_x, old_y = self.rect.x, self.rect.y
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        
        # Impedir que o jogador saia da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        
        # Verificar colisão com NPCs
        if pygame.sprite.spritecollide(self, npcs, False):
            self.rect.x, self.rect.y = old_x, old_y  # Reverter posição se houver colisão

# Classe para NPCs que dão desafios
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, question, answer):
        super().__init__()
        self.image = pygame.Surface((50, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.question = question
        self.answer = answer
        # Aumentando um pouco a área invisível ao redor do NPC
        self.invisible_area = pygame.Rect(x - 20, y - 20, self.rect.width + 40, self.rect.height + 40)
    
    def get_invisible_area(self):
        return self.invisible_area

# Função principal do jogo (código principal do jogo de Trabalho.py)
def game_loop():
    # Criar instâncias do jogador e NPC
    player = Player()
    npc = NPC(300, 300, "Qual é o resultado de 2 + 2?", "4")

    # Grupo de sprites
    all_sprites = pygame.sprite.Group()
    npcs = pygame.sprite.Group()
    all_sprites.add(player, npc)
    npcs.add(npc)

    running = True
    question_active = False
    user_answer = ""

    while running:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause.pause(screen, font)  # Pausar o jogo
            elif event.type == pygame.KEYDOWN and question_active:
                if event.key == pygame.K_RETURN:
                    if user_answer == npc.answer:
                        print("Resposta correta! Você pode avançar.")
                    else:
                        print("Resposta errada. Tente novamente!")
                    user_answer = ""
                    question_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                else:
                    user_answer += event.unicode
        
        # Movimento do jogador
        player.update(keys, npcs)
        
        # Verificar se o jogador entrou na área invisível
        if npc.get_invisible_area().colliderect(player.rect) and not question_active:
            question_active = True
        
        # Verificar se o jogador saiu da área invisível
        if not npc.get_invisible_area().colliderect(player.rect) and question_active:
            question_active = False
        
        # Desenhar os sprites
        all_sprites.draw(screen)
        
        # Mostrar a pergunta
        if question_active:
            question_surface = font.render(npc.question, True, BLACK)
            screen.blit(question_surface, (WIDTH // 2 - question_surface.get_width() // 2, 50))
            answer_surface = font.render(user_answer, True, BLACK)
            screen.blit(answer_surface, (WIDTH // 2 - answer_surface.get_width() // 2, 100))
        
        pygame.display.flip()
        pygame.time.delay(30)

    pygame.quit()

# Inicializa o Pygame e executa o jogo
pygame.init()
game_loop()
