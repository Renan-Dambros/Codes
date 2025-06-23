import pygame
import random
import json
import os

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CodeQuest: A Jornada do Programador")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Fontes
question_font = pygame.font.Font(None, 48)
options_font = pygame.font.Font(None, 36)
feedback_font = pygame.font.Font(None, 42)

# Carrega a imagem do chão
floor_image = pygame.image.load("chao.jpg").convert()
floor_image = pygame.transform.scale(floor_image, (30, 30))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images_down = [
            pygame.transform.scale(pygame.image.load("chv1.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv5.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv1.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv6.png").convert_alpha(), (40, 60))
        ]
        self.images_up = [
            pygame.transform.scale(pygame.image.load("chv2.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv7.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv2.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv8.png").convert_alpha(), (40, 60))
        ]
        self.images_left = [
            pygame.transform.scale(pygame.image.load("chv3.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv9.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv3.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv10.png").convert_alpha(), (40, 60))
        ]
        self.images_right = [
            pygame.transform.scale(pygame.image.load("chv4.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv11.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv4.png").convert_alpha(), (40, 60)),
            pygame.transform.scale(pygame.image.load("chv12.png").convert_alpha(), (40, 60))
        ]

        self.image = self.images_down[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_delay = 7
        self.direction = "down"

    def update(self, keys, npcs, walls):
        old_x, old_y = self.rect.x, self.rect.y
        moved = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"
            moved = True
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = "up"
            moved = True
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = "down"
            moved = True

        if moved:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_delay:
                if self.direction == "left":
                    self.animation_index = (self.animation_index + 1) % len(self.images_left)
                elif self.direction == "right":
                    self.animation_index = (self.animation_index + 1) % len(self.images_right)
                elif self.direction == "up":
                    self.animation_index = (self.animation_index + 1) % len(self.images_up)
                elif self.direction == "down":
                    self.animation_index = (self.animation_index + 1) % len(self.images_down)
                self.animation_timer = 0
        else:
            self.animation_index = 0
            self.animation_timer = 0

        if self.direction == "down":
            self.image = self.images_down[self.animation_index % len(self.images_down)]
        elif self.direction == "up":
            self.image = self.images_up[self.animation_index % len(self.images_up)]
        elif self.direction == "left":
            self.image = self.images_left[self.animation_index % len(self.images_left)]
        elif self.direction == "right":
            self.image = self.images_right[self.animation_index % len(self.images_right)]

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if pygame.sprite.spritecollide(self, npcs, False):
            self.rect.x, self.rect.y = old_x, old_y

        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x, self.rect.y = old_x, old_y

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, questions):
        super().__init__()
        image = pygame.image.load("prof.png").convert_alpha()
        self.image = pygame.transform.scale(image, (55, 65))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.questions = questions
        self.current_question = None
        self.invisible_area = pygame.Rect(x - 20, y - 20, self.rect.width + 40, self.rect.height + 40)
        self.select_new_question()

    def select_new_question(self):
        if self.questions:
            self.current_question = random.choice(self.questions)
            return True
        return False

    def get_invisible_area(self):
        return self.invisible_area

    def check_answer(self, selected_option):
        return selected_option == self.current_question["correct_answer"]

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("parede.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def load_questions(difficulty):
    # Mapeia os nomes em português para inglês se necessário
    file_map = {
        "facil": "easy",
        "medio": "medium",
        "dificil": "hard"
    }
    
    # Usa o nome original se não estiver no mapa
    filename = f"{file_map.get(difficulty, difficulty)}.json"
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                questions = data.get("questions", [])
                print(f"Loaded {len(questions)} questions from {filename}")
                return questions
        else:
            print(f"Error: File {filename} not found in directory: {os.getcwd()}")
            print("Looking for files named: easy.json, medium.json, hard.json")
    except Exception as e:
        print(f"Error loading {filename}: {str(e)}")
    return []

def draw_question_screen(question, selected_option=None):
    # Fundo semi-transparente
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    screen.blit(s, (0, 0))
    
    # Desenha a pergunta
    question_text = question_font.render(question["question"], True, WHITE)
    screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 150))
    
    # Desenha as opções
    option_rects = {}
    y_position = 250
    for option, text in question["options"].items():
        # Retângulo de fundo da opção
        option_rect = pygame.Rect(WIDTH // 2 - 200, y_position, 400, 50)
        option_rects[option] = option_rect
        
        # Cor de fundo (diferente se selecionada)
        color = BLUE if option == selected_option else GRAY
        pygame.draw.rect(screen, color, option_rect, border_radius=10)
        
        # Texto da opção
        option_text = options_font.render(f"{option}: {text}", True, BLACK)
        screen.blit(option_text, (option_rect.x + 20, option_rect.centery - option_text.get_height() // 2))
        
        y_position += 70
    
    return option_rects

def game_loop(difficulty):
    print(f"Jogo iniciado no modo: {difficulty}")
    
    questions = load_questions(difficulty)
    if not questions:
        print(f"Não foi possível carregar perguntas para a dificuldade {difficulty}")
        return

    player = Player()
    npc = NPC(300, 300, questions)

    all_sprites = pygame.sprite.Group()
    npcs = pygame.sprite.Group()
    walls = pygame.sprite.Group()

    all_sprites.add(player, npc)
    npcs.add(npc)

    TILE_SIZE = 30

    # Adiciona paredes ao redor da tela
    for x in range(0, WIDTH, TILE_SIZE):
        wall_top = Wall(x, 0)
        wall_bottom = Wall(x, HEIGHT - TILE_SIZE)
        walls.add(wall_top, wall_bottom)
        all_sprites.add(wall_top, wall_bottom)

    for y in range(TILE_SIZE, HEIGHT - TILE_SIZE, TILE_SIZE):
        wall_left = Wall(0, y)
        wall_right = Wall(WIDTH - TILE_SIZE, y)
        walls.add(wall_left, wall_right)
        all_sprites.add(wall_left, wall_right)

    running = True
    question_active = False
    selected_option = None
    feedback = ""
    feedback_timer = 0
    option_rects = {}

    while running:
        # Desenha o chão
        for x in range(0, WIDTH, 30):
            for y in range(0, HEIGHT, 30):
                screen.blit(floor_image, (x, y))

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = True
                    while paused:
                        for e in pygame.event.get():
                            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                                paused = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

            if question_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for option, rect in option_rects.items():
                        if rect.collidepoint(mouse_pos):
                            selected_option = option
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and selected_option:
                        if npc.check_answer(selected_option):
                            feedback = "Resposta correta! Pode avançar."
                            feedback_color = GREEN
                            question_active = False
                            npc.select_new_question()
                        else:
                            feedback = "Resposta incorreta! Tente novamente."
                            feedback_color = RED
                        feedback_timer = 90  # 3 segundos (90 frames)
                        selected_option = None

        player.update(keys, npcs, walls)

        if npc.get_invisible_area().colliderect(player.rect) and not question_active and not feedback_timer:
            question_active = True
            selected_option = None

        all_sprites.draw(screen)

        if question_active and npc.current_question:
            option_rects = draw_question_screen(npc.current_question, selected_option)
            
            # Instruções
            instructions = options_font.render("Clique em uma opção e pressione Enter", True, WHITE)
            screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 100))

        if feedback_timer > 0:
            feedback_surface = feedback_font.render(feedback, True, feedback_color)
            screen.blit(feedback_surface, (WIDTH // 2 - feedback_surface.get_width() // 2, 100))
            feedback_timer -= 1

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()

def start_game(difficulty):
    print(f"Jogo iniciado no modo: {difficulty}")
    game_loop(difficulty)

if __name__ == "__main__":
    start_game("medio")