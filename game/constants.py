import pygame


# --- CONSTANTES DA JANELA --- #
WINDOW_TITLE = "Jogo"
WINDOW_ICON = pygame.image.load("resources/assets/vida.png")  # temporário
FPS = 60

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960
LANE_WIDTH = WINDOW_WIDTH // 12


WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# --- CONSTANTES DE POSIÇÃO --- #
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2

LEFT_WALL_EDGE = LANE_WIDTH * 3
RIGHT_WALL_EDGE = WINDOW_WIDTH - LEFT_WALL_EDGE

# --- SPRITES --- #
MAP_SPRITE = pygame.image.load("resources/assets/map_p.jpg")
WALL_SPRITE = pygame.image.load("resources/assets/wall_piece.png")
PLAYER_SPRITE = pygame.transform.scale(
    pygame.image.load("resources/assets/teireza.png"),
    (LANE_WIDTH, LANE_WIDTH),
)
OBSTACLE_SPRITE = pygame.image.load("resources/assets/gota.png")

COLLECTIBLE_SPRITES = {
    "web": pygame.image.load("resources/assets/vida.png"),
    "skirt": pygame.image.load("resources/assets/saia de filó.png"),
    "needle": pygame.image.load("resources/assets/agulha.png"),
    "fabric": pygame.image.load("resources/assets/tecido.png"),
    "mockup": pygame.image.load("resources/assets/molde da saia.png")
}

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
    "LANE_WIDTH",
    "MAP_SPRITE",
    "PLAYER_SPRITE",
    "OBSTACLE_SPRITE",
    "WALL_SPRITE",
    "COLLECTIBLE_SPRITES"
]
