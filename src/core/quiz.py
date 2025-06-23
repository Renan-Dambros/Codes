import json
import os

class Quiz:
    def __init__(self, level):
        file = os.path.join('data', f'level{level}.json')
        with open(file, encoding='utf-8') as f:
            self.questions = json.load(f)
        self.current = 0
        self.score = 0
        self.selected = 0
        self.finished = False

    def select_next(self, direction):
        n = len(self.questions[self.current]['opcoes'])
        self.selected = (self.selected + direction) % n

    def answer(self):
        if self.selected == self.questions[self.current]['resposta']:
            self.score += 1
        self.current += 1
        self.selected = 0
        if self.current >= len(self.questions):
            self.finished = True

    def reset(self):
        self.current = 0
        self.score = 0
        self.selected = 0
        self.finished = False
