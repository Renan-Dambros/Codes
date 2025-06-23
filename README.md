# Quiz Classroom Adventure 🎮

Um jogo educativo feito em Python + Pygame, onde o jogador percorre uma sala de aula, interage com um professor NPC, responde a quizzes e avança por diferentes fases de dificuldade.

## 📌 Como jogar

- Mova o personagem com as teclas **WASD** ou **Setas**.
- Interaja com o **Professor** chegando perto dele (a área de interação é pequena para maior precisão).
- Após acertar todas as perguntas, uma **porta** aparece no topo da sala, ao lado do quadro. Vá até ela para avançar para a próxima fase.
- Após completar as três fases (**easy**, **medium**, **hard**), o jogo termina com a tela de fim.

## 📜 Estrutura de fases

| Fase   | Nome          | Conteúdo                          |
|------- |-------------- |---------------------------------- |
| Fase 1 | Easy          | Perguntas fáceis                  |
| Fase 2 | Medium        | Perguntas de dificuldade média    |
| Fase 3 | Hard          | Perguntas difíceis                |

## 🐣 Easter Egg (Usando um código muito famoso)

- Isso ativa uma vantagem secreta no quiz!
- Também exibe a mensagem "Segredo Desbloqueado" piscando na tela.

## 🎶 Áudio

- O jogo tem músicas diferentes para o menu e para o gameplay.
- A música da fase só começa na **primeira fase** e permanece em loop até o fim do jogo.

## 🎨 Design da Sala de Aula

- Sala com **4 fileiras**, com **4 mesas em cada fileira**.
- Há espaço horizontal suficiente entre as mesas para o jogador circular.
- O **quadro** fica no topo da sala, e a **porta** aparece ao concluir o desafio do nível atual.

## 💡 Possíveis melhorias futuras:

- Adicionar mais fases com outras temáticas de sala.
- Sistema de tempo para responder perguntas.
- Implementar um sistema de score/ranking.
- Animações para o jogador e NPC.
- Adicionar mais efeitos sonoros (por exemplo: som ao abrir a porta, som de resposta errada/certa mais elaborados).
- Suporte a perguntas randomizadas de um banco de dados maior.
- Sistema de salvar progresso.
- Efeitos visuais adicionais ao completar fases.

## 🚀 Como rodar:

1. Instale o Pygame:

```bash
pip install pygame
```
2. Inicie com:
```bash
python -m src.main
```
