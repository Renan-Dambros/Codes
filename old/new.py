import pygame
import sys
import json

# Configurações gerais
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
FONT_NAME = 'freesansbold.ttf'

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carregar quizzes de um arquivo JSON ou dicionário interno
QUIZZES = {
    1: [
        {"pergunta": "O que significa 'IDE'?", "opcoes": ["Integrated Development Environment", "Internal Design Editor", "Initial Data Entry"], "resposta": 0},
        {"pergunta": "Qual linguagem é usada para desenvolvimento web backend?", "opcoes": ["HTML", "CSS", "Python"], "resposta": 2}
    ],
    2: [
        {"pergunta": "O que faz o método .append() em Python?", "opcoes": ["Adiciona um item ao final da lista", "Remove um item da lista", "Retorna o tamanho da lista"], "resposta": 0},
        {"pergunta": "Qual estrutura repete um bloco enquanto condição for verdadeira?", "opcoes": ["if", "while", "def"], "resposta": 1}
    ],
    3: [
        {"pergunta": "O que é POO?", "opcoes": ["Programação Orientada a Objetos", "Processamento Orientado a Operações", "Plataforma Operacional Otimizada"], "resposta": 0},
        {"pergunta": "Em Python, como definimos uma classe?", "opcoes": ["class MinhaClasse:", "def MinhaClasse:", "object MinhaClasse:"], "resposta": 0}
    ],
    4: [
        {"pergunta": "O que faz o comando 'git commit'?", "opcoes": ["Envia mudanças para o repositório remoto", "Salva mudanças no repositório local", "Clona um repositório"], "resposta": 1},
        {"pergunta": "Qual comando inicializa um repositório Git?", "opcoes": ["git start", "git init", "git begin"], "resposta": 1}
    ]
}

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CodeQuest: A Jornada do Programador")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, 24)

        # Estados do jogo: menu, jogando, quiz, pausa
        self.state = 'menu'
        self.level = 1
        self.quiz = None

        # Música
        self.music_menu = None
        self.music_game = None
        self.music_pause = None
        self.load_music()
        self.play_music('menu')

    def load_music(self):
        # Carregue seus arquivos de música aqui
        # Exemplo: 'assets/menu.ogg', 'assets/game.ogg', 'assets/pause.ogg'
        self.music_menu = 'assets/musica.mpeg'
        self.music_game = 'assets/musica.mpeg'
        self.music_pause = 'assets/musica.mpeg'

    def play_music(self, section):
        pygame.mixer.music.stop()
        path = getattr(self, f"music_{section}")
        if path:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.state == 'menu':
                self.handle_menu_events(event)
            elif self.state == 'jogando':
                self.handle_game_events(event)
            elif self.state == 'quiz':
                self.handle_quiz_events(event)
            elif self.state == 'pausa':
                self.handle_pause_events(event)

    def update(self):
        # Atualizações específicas de cada estado (se necessário)
        pass

    def draw(self):
        self.screen.fill(WHITE)
        if self.state == 'menu':
            self.draw_menu()
        elif self.state == 'jogando':
            self.draw_game()
        elif self.state == 'quiz':
            self.draw_quiz()
        elif self.state == 'pausa':
            self.draw_pause()

    # ---------------- MENU ----------------
    def draw_menu(self):
        title = self.font.render("CodeQuest: A Jornada do Programador", True, BLACK)
        start = self.font.render("Pressione ENTER para iniciar", True, BLACK)
        self.screen.blit(title, (100, 200))
        self.screen.blit(start, (100, 300))

    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.state = 'jogando'
            self.play_music('game')

    # ---------------- JOGO ----------------
    def draw_game(self):
        text = self.font.render(f"Sala {self.level} - Fale com o NPC e responda o quiz", True, BLACK)
        instr = self.font.render("Aperte Q para iniciar o quiz quando estiver na porta", True, BLACK)
        self.screen.blit(text, (50, 50))
        self.screen.blit(instr, (50, 100))

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.state = 'pausa'
                self.play_music('pause')
            if event.key == pygame.K_q:
                self.start_quiz()

    # ---------------- QUIZ ----------------
    def start_quiz(self):
        if self.level in QUIZZES:
            self.quiz = Quiz(self.level)
            self.state = 'quiz'

    def draw_quiz(self):
        if self.quiz:
            self.quiz.draw(self.screen)

    def handle_quiz_events(self, event):
        if self.quiz and self.quiz.handle_event(event):
            if self.quiz.finalizado:
                if self.quiz.vitorias >= len(QUIZZES[self.level]):
                    self.level += 1
                self.state = 'jogando'
                self.quiz = None

    # ---------------- PAUSA ----------------
    def draw_pause(self):
        pause_text = self.font.render("PAUSADO", True, BLACK)
        resume = self.font.render("Pressione R para retomar", True, BLACK)
        self.screen.blit(pause_text, (350, 200))
        self.screen.blit(resume, (300, 300))

    def handle_pause_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.state = 'jogando'
            self.play_music('game')


class Quiz:
    def __init__(self, level):
        self.questions = QUIZZES[level]
        self.current = 0
        self.vitorias = 0
        self.finalizado = False
        self.selected = 0
        self.font = pygame.font.Font(FONT_NAME, 20)

    def draw(self, surface):
        q = self.questions[self.current]
        pergunta = self.font.render(q['pergunta'], True, BLACK)
        surface.blit(pergunta, (50, 150))
        for idx, opc in enumerate(q['opcoes']):
            color = BLACK if idx != self.selected else (0, 100, 200)
            opc_text = self.font.render(f"{idx+1}. {opc}", True, color)
            surface.blit(opc_text, (70, 200 + idx * 30))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = max(0, self.selected - 1)
            elif event.key == pygame.K_DOWN:
                self.selected = min(len(self.questions[self.current]['opcoes']) - 1, self.selected + 1)
            elif event.key == pygame.K_RETURN:
                # Verificar resposta
                correto = self.questions[self.current]['resposta']
                if self.selected == correto:
                    self.vitorias += 1
                self.current += 1
                self.selected = 0
                if self.current >= len(self.questions):
                    self.finalizado = True
                return True
        return False


if __name__ == '__main__':
    game = Game()
    game.run()
