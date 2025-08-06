import pygame


# --- CONSTANTES DA JANELA --- #
WINDOW_TITLE = "Jogo"
WINDOW_ICON = pygame.image.load("resources/assets/vida.png")  # temporário
FPS = 60

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960
LANE_WIDTH = WINDOW_WIDTH / 12


WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# --- CONSTANTES DE POSIÇÃO --- #
CENTER_X = WINDOW_WIDTH / 2
CENTER_Y = WINDOW_HEIGHT / 2

LEFT_WALL_EDGE = LANE_WIDTH * 3
RIGHT_WALL_EDGE = WINDOW_WIDTH - LEFT_WALL_EDGE

# --- SPRITES --- #
MAP_SPRITE = pygame.image.load("resources/assets/map_p4.png")
WALL_SPRITE = pygame.image.load("resources/assets/wall_piece.png")

# Carregar e redimensionar player sprite para o tamanho da lane
PLAYER_SPRITE = pygame.transform.scale(
    pygame.image.load("resources/assets/teireza.png"),
    (int(LANE_WIDTH), int(LANE_WIDTH)),
)

OBSTACLE_SPRITE = pygame.image.load("resources/assets/gota.png")

__all__ = [
    "WINDOW_TITLE",
    "WINDOW_ICON",
    "FPS",
    "WINDOW_WIDTH",
    "WINDOW_HEIGHT",
    "WINDOW_SIZE",
    "CENTER_X",
    "CENTER_Y",
    "LEFT_WALL_EDGE",
    "RIGHT_WALL_EDGE",
    "MAP_SPRITE",
    "PLAYER_SPRITE",
    "OBSTACLE_SPRITE",
    "WALL_SPRITE",
    "LANE_WIDTH",
]
