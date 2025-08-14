import pygame

pygame.font.init()
pygame.mixer.init()  # Inicializar mixer de áudio


# --- CONSTANTES DA JANELA --- #
WINDOW_TITLE = "A Dona Aranha: Missão Filó"
WINDOW_ICON = pygame.image.load("resources/assets/mockup.png")  # temporário
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


# --- CONSTANTES DE ESTADO --- #
START_SCREEN = 0
PLAYING_GAME = 1
GAME_OVER = 2
GAME_WON = 3


# --- CONSTANTES DA TELA INICIAL --- #
WIDTH = 260
HEIGHT = 60


# --- ASSETS --- #
FONT_TITLE = pygame.font.Font("resources/fonts/ari-w9500-bold.ttf", 48)
FONT = pygame.font.Font("resources/fonts/ari-w9500.ttf", 24)

MAP_SPRITE = pygame.image.load("resources/assets/background.png")
LEFT_WALL_SPRITE = pygame.image.load("resources/assets/left_wall.png")
RIGHT_WALL_SPRITE = pygame.transform.flip(LEFT_WALL_SPRITE, True, False)
PLAYER_SPRITE = pygame.image.load("resources/assets/player.png")
OBSTACLE_SPRITE = pygame.image.load("resources/assets/obstacle.png")
SKIRT_SPRITE = pygame.image.load("resources/assets/skirt.png")
MAIN_MENU_SPRITE = pygame.image.load("resources/assets/menu.png")

COLLECTIBLE_SPRITES = {
    "web": pygame.image.load("resources/assets/web.png"),
    "needle": pygame.image.load("resources/assets/needle.png"),
    "fabric": pygame.image.load("resources/assets/fabric.png"),
    "mockup": pygame.image.load("resources/assets/mockup.png"),
}

# --- ÁUDIO --- #
BACKGROUND_MUSIC = (
    "resources/sound/Dona Aranha - Instrumental (audio-extractor.net).mp3"
)

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
    "FONT",
    "FONT_TITLE",
    "SKIRT_SPRITE",
    "MAP_SPRITE",
    "PLAYER_SPRITE",
    "OBSTACLE_SPRITE",
    "LEFT_WALL_SPRITE",
    "RIGHT_WALL_SPRITE",
    "COLLECTIBLE_SPRITES",
    "BACKGROUND_MUSIC",
    "START_SCREEN",
    "PLAYING_GAME",
    "GAME_OVER",
    "GAME_WON",
    "MAIN_MENU_SPRITE",
]
