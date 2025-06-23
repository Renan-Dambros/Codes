def get_level_data(level):
    WIDTH, HEIGHT = 1920, 1080
    TILE_SIZE = 30

    # Gera paredes ao redor da tela igual no código antigo
    walls = []

    for x in range(0, WIDTH, TILE_SIZE):
        walls.append([x, 0])  # Topo
        walls.append([x, HEIGHT - TILE_SIZE])  # Base

    for y in range(TILE_SIZE, HEIGHT - TILE_SIZE, TILE_SIZE):
        walls.append([0, y])  # Esquerda
        walls.append([WIDTH - TILE_SIZE, y])  # Direita

    return {
        "bg": "chao",  # Mantém o fundo como antes
        "player_start": [WIDTH // 2, HEIGHT // 2],
        "npc": [300, 300],
        "walls": walls,
        "doors": []
    }
