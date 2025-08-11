import random

import pygame.font

from .classes import *
from .player import Player
from .constants import *

from pygame import display, time, event, key, constants as pygame_constants
from pygame.sprite import Group


class Game:
    """
    Classe que representa o jogo, responsável por iniciá-lo e coordenar seus estados.
    """

    def __init__(self):
        display.set_caption(WINDOW_TITLE)
        display.set_icon(WINDOW_ICON)

        self.screen = display.set_mode(WINDOW_SIZE)
        self.fullscreen = False

        self.clock = time.Clock()
        self.state = START_SCREEN

        self.game_speed = LANE_WIDTH // 10

        self.player = Player(self.game_speed)
        self.score = {
            "web":    0,
            "skirt":  0,
            "needle": 0,
            "fabric": 0,
            "mockup": 0
        }

        self.background = Group()
        self.collectibles = Group()
        self.obstacles = Group()
        self.walls = Group()

        # Criar paredes nas bordas
        self.create_walls()

    def toggle_fullscreen(self):
        if self.fullscreen:
            # Voltar ao modo janela
            self.screen = display.set_mode(WINDOW_SIZE)
        else:
            # Ir para tela cheia - deixar o pygame decidir a melhor resolução
            self.screen = display.set_mode((0, 0), pygame_constants.FULLSCREEN)

        self.fullscreen = not self.fullscreen

    def render_game(self):
        """
        Renderiza todos os elementos do jogo em uma surface virtual.
        """
        from pygame import Surface

        # Criar surface virtual do tamanho do jogo
        game_surface = Surface(WINDOW_SIZE)
        game_surface.fill("black")
        game_surface.blit(MAP_SPRITE, (0, 0))

        # Desenhar todos os elementos
        self.walls.draw(game_surface)
        self.collectibles.draw(game_surface)
        game_surface.blit(self.player.image, self.player.rect)
        self.obstacles.draw(game_surface)

        return game_surface

    def display_game(self, game_surface):
        """
        Exibe a surface do jogo na tela, escalando se necessário.
        """
        from pygame import transform

        # Limpar tela real
        self.screen.fill("black")

        # Obter dimensões da tela atual
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        if screen_w == WINDOW_WIDTH and screen_h == WINDOW_HEIGHT:
            # Modo janela: copiar diretamente
            self.screen.blit(game_surface, (0, 0))
        else:
            # Tela cheia: escalar mantendo proporção e centralizar
            scale_x = screen_w / WINDOW_WIDTH
            scale_y = screen_h / WINDOW_HEIGHT
            scale = min(scale_x, scale_y)

            new_w = int(WINDOW_WIDTH * scale)
            new_h = int(WINDOW_HEIGHT * scale)

            # Centralizar
            x = (screen_w - new_w) // 2
            y = (screen_h - new_h) // 2

            # Escalar e desenhar
            scaled_surface = transform.scale(game_surface, (new_w, new_h))
            self.screen.blit(scaled_surface, (x, y))

    def create_walls(self):
        """
        Cria as paredes nas bordas esquerda e direita usando padrão de repetição.
        """
        # Obter dimensões da sprite da parede
        wall_width = WALL_SPRITE.get_width()
        wall_height = WALL_SPRITE.get_height()

        # Criar um padrão que se repete verticalmente
        # Cobrir a altura da tela + margem extra para o scroll
        num_wall_pieces = (WINDOW_HEIGHT // wall_height) + 2

        # Criar parede esquerda
        left_wall_x = LEFT_WALL_EDGE - wall_width
        for i in range(num_wall_pieces):
            y_pos = i * wall_height
            left_wall = Wall(left_wall_x, y_pos, self.game_speed)
            self.walls.add(left_wall)

        # Criar parede direita
        right_wall_x = RIGHT_WALL_EDGE
        for i in range(num_wall_pieces):
            y_pos = i * wall_height
            right_wall = Wall(right_wall_x, y_pos, self.game_speed)
            self.walls.add(right_wall)

    def start(self):
        rodando = True

        while rodando:
            # Atualizar relógio
            self.clock.tick(FPS)

            # Analisar eventos
            for evento in event.get():
                match evento.type:
                    case pygame_constants.QUIT:
                        rodando = False

                    case pygame_constants.KEYDOWN:
                        rodando = evento.key != pygame_constants.K_ESCAPE

                        if evento.key == pygame_constants.K_F11:
                            self.toggle_fullscreen()
                        elif rodando and self.state != PLAYING_GAME:
                            self.game_speed = LANE_WIDTH // 10
                            self.player = Player(self.game_speed)
                            self.state = PLAYING_GAME

            if self.state == START_SCREEN:
                self.screen.fill("white") # teste
                ...
            elif self.state == PLAYING_GAME:
                # Lógica de spawn de coletáveis e obstáculos
                self.create_obstacles()
                self.create_collectibles()

                # Atualizar estados
                keys = key.get_pressed()
                ...
                self.obstacles.update()
                self.collectibles.update(speed = self.game_speed)
                self.walls.update(speed = self.game_speed)

                self.player.update(
                    keys = keys,
                    # speed = self.game_speed,
                    # obstacles = self.obstacles,
                    # collectibles = self.collectibles
                    game = self
                )

                # Renderização
                game_surface = self.render_game()
                self.display_game(game_surface)
                ...

                # Aumentar a velocidade do jogo gradualmente
                self.game_speed *= 1.000005

                if self.player.hp <= 0:
                    self.state = GAME_OVER
            elif self.state == GAME_OVER:
                self.screen.fill("black") # Teste
                ...

            # Atualizar display
            display.flip()

    def create_obstacles(self):
        # teste
        if len(self.obstacles) == 0:
            scale = 0.5 + random.random()  # 0.5-1.5
            pos_x = random.randint(LEFT_WALL_EDGE, RIGHT_WALL_EDGE)
            accel = 0.25 + random.random()  # 0.25-1.25
            damage = (1 + int(self.game_speed * scale / LANE_WIDTH)) * 10

            new_obstacle = Obstacle(scale, pos_x, accel, damage)
            self.obstacles.add(new_obstacle)

    def create_collectibles(self):
        # teste
        if len(self.collectibles) < 2:
            pos_x = random.randint(LEFT_WALL_EDGE, RIGHT_WALL_EDGE)
            texture = random.choice(list(COLLECTIBLE_SPRITES.values()))

            new_collectible = Collectible(texture, pos_x)
            self.collectibles.add(new_collectible)