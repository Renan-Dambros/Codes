import pygame
import random

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, image, questions, dialogs=None, difficulty="easy"):
        super().__init__()
        self.image = pygame.transform.scale(image, (55, 65))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.questions = questions
        self.current_question = None
        self.invisible_area = pygame.Rect(x - 20, y - 20, self.rect.width + 40, self.rect.height + 40)
        self.dialogs = dialogs or {}
        self.difficulty = difficulty
        self.dialog_state = "before"  # Pode ser 'before', 'quiz', ou 'after'
        self.select_new_question()

    def select_new_question(self):
        if self.questions:
            self.current_question = random.choice(self.questions)
            return True
        return False

    def get_dialog(self):
        return self.dialogs.get(self.difficulty, {}).get(self.dialog_state, "")

    def get_invisible_area(self):
        return self.invisible_area

    def check_answer(self, selected_option):
        return selected_option == self.current_question["correct_answer"]
