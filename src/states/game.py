import pygame
import json
import random
from src.characters.player import Player
from src.states.pause import PauseState
from src.states.end import EndState

BASE_WIDTH = 800
BASE_HEIGHT = 600

class GameState:
    DIFFICULTY_ORDER = ["easy", "medium", "hard"]

    KONAMI_CODE = [
        pygame.K_UP, pygame.K_UP,
        pygame.K_DOWN, pygame.K_DOWN,
        pygame.K_LEFT, pygame.K_RIGHT,
        pygame.K_LEFT, pygame.K_RIGHT,
        pygame.K_b, pygame.K_a
    ]

    def __init__(self, game, difficulty, easter_egg_active=False):
        self.game = game
        self.difficulty = difficulty
        self.questions_answered = 0
        self.game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        self.load_level()
        self.show_door_message_timer = 0

        self.konami_progress = 0
        self.easter_egg_active = easter_egg_active
        self.secret_message_timer = 0

        # Carregar sons
        self.hover_sound = pygame.mixer.Sound("assets/sounds/hover.mp3")
        self.correct_sound = pygame.mixer.Sound("assets/sounds/correct.mp3")
        self.wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.mp3")

        # Tocar música da fase (somente se ainda não estiver tocando)
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("assets/sounds/game.mp3")
            pygame.mixer.music.play(-1)  # Loop infinito

        self.last_hovered_option = None

    def load_level(self):
        TILE_SIZE = 30

        with open(f"data/{self.difficulty}.json", encoding="utf-8") as f:
            self.questions = json.load(f)["questions"]

        self.bg = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        floor = self.game.assets.images["chao"]
        floor = pygame.transform.scale(floor, (TILE_SIZE, TILE_SIZE))
        for x in range(0, BASE_WIDTH, TILE_SIZE):
            for y in range(0, BASE_HEIGHT, TILE_SIZE):
                self.bg.blit(floor, (x, y))

        # Jogador nasce no meio da 3ª fileira (entre as mesas)
        # Considerando mesas começam em y=200 e espaçamento vertical = 70
        # Mesa tem 40px de altura e largura 60px
        # 3ª fileira começa em y=200 + 2*70 = 340, o jogador nasce próximo de y=340 + 45
        player_x = 150 + (120 * 1.5)  # Meio horizontal da fileira 3 (com espaçamento horizontal 120)
        player_y = 340 + 45  # ligeiramente abaixo da 3ª fileira

        self.player = Player(self.game.assets.images, [player_x, player_y])

        self.npc = pygame.sprite.Sprite()
        self.npc.image = pygame.transform.scale(self.game.assets.images["prof"], (55, 65))
        self.npc.rect = self.npc.image.get_rect(topleft=(BASE_WIDTH // 2, 100))
        # Área de interação menor: jogador precisa chegar bem perto do professor
        self.npc_area = pygame.Rect(self.npc.rect.x + 10, self.npc.rect.y + 20,
                                    self.npc.rect.width - 20, self.npc.rect.height - 30)

        self.walls = pygame.sprite.Group()
        wall_img = pygame.transform.scale(self.game.assets.images["parede"], (TILE_SIZE, TILE_SIZE))

        for x in range(0, BASE_WIDTH, TILE_SIZE):
            top = pygame.sprite.Sprite()
            top.image = wall_img
            top.rect = wall_img.get_rect(topleft=(x, 0))
            bottom = pygame.sprite.Sprite()
            bottom.image = wall_img
            bottom.rect = wall_img.get_rect(topleft=(x, BASE_HEIGHT - TILE_SIZE))
            self.walls.add(top, bottom)

        for y in range(TILE_SIZE, BASE_HEIGHT - TILE_SIZE, TILE_SIZE):
            left = pygame.sprite.Sprite()
            left.image = wall_img
            left.rect = wall_img.get_rect(topleft=(0, y))
            right = pygame.sprite.Sprite()
            right.image = wall_img
            right.rect = wall_img.get_rect(topleft=(BASE_WIDTH - TILE_SIZE, y))
            self.walls.add(left, right)

        self.objects = pygame.sprite.Group()

        table_img = pygame.transform.scale(self.game.assets.images["mesa"], (60, 40))
        board_img = pygame.transform.scale(self.game.assets.images["quadro"], (300, 60))

        # Criar 4 fileiras e 4 mesas por fileira com espaçamento horizontal aumentado (distância horizontal maior que 60)
        start_x = 150
        horizontal_spacing = 120  # mesa 60 + 60 de espaço entre mesas na horizontal
        start_y = 200
        vertical_spacing = 70  # espaçamento vertical entre fileiras (mantido)

        for row in range(4):
            y = start_y + row * vertical_spacing
            for col in range(4):
                x = start_x + col * horizontal_spacing
                table = pygame.sprite.Sprite()
                table.image = table_img
                table.rect = table_img.get_rect(topleft=(x, y))
                self.objects.add(table)

        self.board = pygame.sprite.Sprite()
        self.board.image = board_img
        self.board.rect = board_img.get_rect(topleft=(250, 30))
        self.objects.add(self.board)

        self.door = None
        self.current_question = None
        self.showing_question = False
        self.selected_option = None
        self.feedback = ""
        self.feedback_timer = 0

    def spawn_door(self):
        door_img = pygame.transform.scale(self.game.assets.images["porta"], (60, 80))
        self.door = pygame.sprite.Sprite()
        self.door.image = door_img
        # Porta aparece sempre à esquerda do quadro (board) no topo
        door_x = self.board.rect.left - 70  # 10px à esquerda do quadro (60 largura da porta + 10 de espaçamento)
        door_y = self.board.rect.top + 10
        self.door.rect = door_img.get_rect(topleft=(door_x, door_y))
        self.show_door_message_timer = 180

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        screen_w, screen_h = self.game.screen.get_size()
        scale_w = screen_w / BASE_WIDTH
        scale_h = screen_h / BASE_HEIGHT
        scale = min(scale_w, scale_h)
        offset_x = (screen_w - BASE_WIDTH * scale) / 2
        offset_y = (screen_h - BASE_HEIGHT * scale) / 2

        game_mouse_x = (mouse_pos[0] - offset_x) / scale
        game_mouse_y = (mouse_pos[1] - offset_y) / scale
        game_mouse_pos = (game_mouse_x, game_mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == self.KONAMI_CODE[self.konami_progress]:
                    self.konami_progress += 1
                    if self.konami_progress == len(self.KONAMI_CODE):
                        self.easter_egg_active = True
                        self.konami_progress = 0
                        self.secret_message_timer = 300
                else:
                    self.konami_progress = 0

                if event.key == pygame.K_ESCAPE:
                    self.game.state = PauseState(self.game, self)

            elif event.type == pygame.MOUSEBUTTONDOWN and self.showing_question:
                for opt, rect in self.option_rects.items():
                    if rect.collidepoint(game_mouse_pos):
                        self.selected_option = opt
                        self.check_answer()

    def check_answer(self):
        if self.selected_option is not None:
            correct = self.selected_option == self.current_question["correct_answer"]
            self.feedback = "Correto!" if correct else "Errado!"
            self.feedback_timer = 30

            if correct:
                self.correct_sound.play()
                if self.current_question in self.questions:
                    self.questions.remove(self.current_question)
                self.current_question = None
                self.showing_question = False
                self.selected_option = None

                if len(self.questions) == 0 and not self.door:
                    self.spawn_door()
            else:
                self.wrong_sound.play()

    def update(self):
        keys = pygame.key.get_pressed()

        if not self.showing_question:
            all_walls = pygame.sprite.Group(self.walls, self.objects)
            self.player.update(keys, all_walls)

        if not self.showing_question and self.npc_area.colliderect(self.player.rect):
            if not self.current_question and self.questions:
                self.current_question = random.choice(self.questions)
                self.showing_question = True
                self.selected_option = None
                if self.easter_egg_active:
                    self.selected_option = self.current_question["correct_answer"]

        if self.door and self.player.rect.colliderect(self.door.rect):
            current_index = self.DIFFICULTY_ORDER.index(self.difficulty)
            if current_index + 1 < len(self.DIFFICULTY_ORDER):
                next_difficulty = self.DIFFICULTY_ORDER[current_index + 1]
                self.game.state = GameState(self.game, next_difficulty, easter_egg_active=self.easter_egg_active)
            else:
                self.game.state = EndState(self.game)

        if self.feedback_timer > 0:
            self.feedback_timer -= 1

        if self.show_door_message_timer > 0:
            self.show_door_message_timer -= 1

        if self.secret_message_timer > 0:
            self.secret_message_timer -= 1

    def render(self):
        self.game_surface.blit(self.bg, (0, 0))
        self.game_surface.blit(self.npc.image, self.npc.rect)
        self.walls.draw(self.game_surface)
        self.objects.draw(self.game_surface)

        if self.door:
            self.game_surface.blit(self.door.image, self.door.rect)
            small_font = pygame.font.Font(None, 20)  # Tamanho 20 pixels, bem menor que o padrão
            msg = "Vá para a porta para avançar"
            text_surf = small_font.render(msg, True, (255, 255, 255))
            text_x = self.board.rect.left + (self.board.rect.width // 2) - (text_surf.get_width() // 2)
            text_y = self.board.rect.top + (self.board.rect.height // 2) - (text_surf.get_height() // 2)
            self.game_surface.blit(text_surf, (text_x, text_y))


        self.game_surface.blit(self.player.image, self.player.rect)

        if self.showing_question and self.current_question:
            self.draw_question()

        if self.feedback_timer > 0:
            font = self.game.assets.fonts["default"]
            color = (0, 255, 0) if self.feedback == "Correto!" else (255, 0, 0)
            surface = font.render(self.feedback, True, color)
            self.game_surface.blit(surface, (BASE_WIDTH // 2 - surface.get_width() // 2, 80))

        if self.secret_message_timer > 0:
            font = self.game.assets.fonts["default"]
            alpha = 255 if (self.secret_message_timer // 10) % 2 == 0 else 100
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)
            text_surface = font.render("Segredo Desbloqueado", True, (0, 255, 0))
            s = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            s.blit(text_surface, (0, 0))
            s.set_alpha(alpha)
            self.game_surface.blit(s, (BASE_WIDTH // 2 - s.get_width() // 2 + offset_x, 120 + offset_y))

        screen_w, screen_h = self.game.screen.get_size()
        scale_w = screen_w / BASE_WIDTH
        scale_h = screen_h / BASE_HEIGHT
        scale = min(scale_w, scale_h)

        scaled_surf = pygame.transform.smoothscale(self.game_surface, (int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale)))

        offset_x = (screen_w - scaled_surf.get_width()) // 2
        offset_y = (screen_h - scaled_surf.get_height()) // 2

        self.game.screen.fill((0, 0, 0))
        self.game.screen.blit(scaled_surf, (offset_x, offset_y))
        pygame.display.flip()

    def draw_question(self):
        font = self.game.assets.fonts["default"]
        question = self.current_question
        self.option_rects = {}

        s = pygame.Surface((BASE_WIDTH, BASE_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.game_surface.blit(s, (0, 0))

        wrapped_question_lines = self.wrap_text(question["question"], font, BASE_WIDTH - 40)
        y = 150
        for line in wrapped_question_lines:
            text = font.render(line, True, (255, 255, 255))
            self.game_surface.blit(text, (BASE_WIDTH // 2 - text.get_width() // 2, y))
            y += text.get_height() + 5

        mouse_pos = pygame.mouse.get_pos()
        screen_w, screen_h = self.game.screen.get_size()
        scale_w = screen_w / BASE_WIDTH
        scale_h = screen_h / BASE_HEIGHT
        scale = min(scale_w, scale_h)
        offset_x = (screen_w - BASE_WIDTH * scale) / 2
        offset_y = (screen_h - BASE_HEIGHT * scale) / 2
        game_mouse_x = (mouse_pos[0] - offset_x) / scale
        game_mouse_y = (mouse_pos[1] - offset_y) / scale
        game_mouse_pos = (game_mouse_x, game_mouse_y)

        y += 30
        for opt, label in question["options"].items():
            wrapped_lines = self.wrap_text(label, font, 460)
            height = (font.get_height() + 5) * len(wrapped_lines) + 20
            rect = pygame.Rect(150, y, 500, height)
            self.option_rects[opt] = rect

            hovering = rect.collidepoint(game_mouse_pos)
            if hovering and self.last_hovered_option != opt:
                self.hover_sound.play()
                self.last_hovered_option = opt
            if not hovering and self.last_hovered_option == opt:
                self.last_hovered_option = None

            if self.easter_egg_active and opt == question["correct_answer"]:
                color = (0, 180, 0)
            else:
                color = (150, 150, 150) if hovering else (100, 100, 100)

            pygame.draw.rect(self.game_surface, color, rect)

            line_y = y + 10
            for line in wrapped_lines:
                opt_txt = font.render(f"{opt}: {line}", True, (255, 255, 255))
                self.game_surface.blit(opt_txt, (rect.x + 20, line_y))
                line_y += font.get_height() + 5

            y += height + 15

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + ("" if current_line == "" else " ") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line != "":
                    lines.append(current_line)
                current_line = word
        if current_line != "":
            lines.append(current_line)
        return lines
