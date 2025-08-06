import pygame


# --- CONSTANTES DA JANELA --- #
WINDOW_TITLE = "Jogo"
WINDOW_ICON = pygame.image.load("resources/assets/vida.png")  # temporário
FPS = 60

WINDOW_WIDTH = 810
WINDOW_HEIGHT = 810

WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# --- CONSTANTES DE POSIÇÃO --- #
CENTER_X = WINDOW_WIDTH / 2
CENTER_Y = WINDOW_HEIGHT / 2

LEFT_WALL = 270
RIGHT_WALL = 540

# --- SPRITES --- #
MAP_SPRITE = pygame.image.load("resources/assets/map_p3.png")

PLAYER_SPRITE = pygame.image.load("resources/assets/player.png")
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
    "LEFT_WALL",
    "RIGHT_WALL",
    "MAP_SPRITE",
    "PLAYER_SPRITE",
    "OBSTACLE_SPRITE",
]
