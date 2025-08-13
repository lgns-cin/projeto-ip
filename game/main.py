import random
import pygame

from .classes import *
from .player import Player
from .constants import *

from pygame import display, time, event, key, constants as pygame_constants
from pygame.sprite import Group
from pygame import Surface


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

    def render_start_screen(self):
        """
        Renderiza todos os elementos da tela inicial em uma surface virtual.
        """

        game_surface = Surface(WINDOW_SIZE)
        game_surface.fill("black")

        title = FONT_TITLE.render("A Dona Aranha", False, "white")
        title_rect = title.get_rect()
        title_rect.center = (CENTER_X, CENTER_Y)

        subtitle = FONT.render("Press any key to start", False, "white")
        subtitle_rect = subtitle.get_rect()
        subtitle_rect.center = (CENTER_X, CENTER_Y + 50)

        game_surface.blit(title, title_rect)
        game_surface.blit(subtitle, subtitle_rect)

        return game_surface

    def render_game_screen(self):
        """
        Renderiza todos os elementos do jogo em uma surface virtual.
        """

        # Criar surface virtual do tamanho do jogo
        game_surface = Surface(WINDOW_SIZE)
        game_surface.fill("black")
        game_surface.blit(MAP_SPRITE, (240, 0))

        # Desenhar todos os elementos
        self.collectibles.draw(game_surface)
        game_surface.blit(self.player.image, self.player.rect)
        self.obstacles.draw(game_surface)
        self.walls.draw(game_surface)
        self.render_gui(game_surface)

        return game_surface

    def render_gui(self, surface):
        x_offset = LANE_WIDTH // 12
        y_offset = LANE_WIDTH // 12

        hp_text = FONT.render(f"Vida: {self.player.hp}", False, "white")
        hp_text_rect = hp_text.get_rect()
        hp_text_rect.topright = (WINDOW_WIDTH - x_offset, y_offset)
        surface.blit(hp_text, hp_text_rect)

        skirt_text = FONT.render(f"{self.score.get("skirt")}", False, "white")
        self.render_icon_with_text(surface, skirt_text, SKIRT_SPRITE, RIGHT_WALL_EDGE + 2*x_offset, y_offset)

        needle_text = FONT.render(f"{self.score.get("needle")}", False, "white")
        self.render_icon_with_text(surface, needle_text, COLLECTIBLE_SPRITES.get("needle"), x_offset, y_offset)

        x_offset += COLLECTIBLE_SPRITES.get("needle").get_width() + LANE_WIDTH // 6

        web_text = FONT.render(f"{self.score.get("fabric")}", False, "white")
        self.render_icon_with_text(surface, web_text, COLLECTIBLE_SPRITES.get("fabric"), x_offset, y_offset)

        x_offset += COLLECTIBLE_SPRITES.get("fabric").get_width() + LANE_WIDTH // 6

        web_text = FONT.render(f"{self.score.get("mockup")}", False, "white")
        self.render_icon_with_text(surface, web_text, COLLECTIBLE_SPRITES.get("mockup"), x_offset, y_offset)


    def render_icon_with_text(self, surface: Surface, text: Surface, icon: Surface, x_offset, y_offset):
        offset = (x_offset, y_offset)
        surface.blit(icon, offset)

        text_offset = (x_offset + icon.get_width(), y_offset)
        surface.blit(text, text_offset)

    def render_game_over_screen(self):
        """
        Renderiza todos os elementos da tela de fim de jogo em uma surface virtual.
        """

        game_surface = Surface(WINDOW_SIZE)
        game_surface.fill("black")

        text_str = f"E a chuva derrubou :( A aranha teceu {self.score.get("skirt")} saias e coletou {self.score.get("web")} teias"
        end_text = FONT.render(text_str, False, "red")
        text_rect = end_text.get_rect()
        text_rect.center = (CENTER_X, CENTER_Y)

        game_surface.blit(end_text, text_rect)

        return game_surface
    
    def render_game_won_screen(self):
        """
        Renderiza todos os elementos da tela de vitória em uma surface virtual.
        """

        game_surface = Surface(WINDOW_SIZE)
        game_surface.fill("black")

        text_str = f"Parabéns! Você venceu! A aranha teceu {self.score.get("skirt")} saias"
        end_text = FONT.render(text_str, False, "green")
        text_rect = end_text.get_rect()
        text_rect.center = (CENTER_X, CENTER_Y)
        subtext_str = f"Agora a barata possui as 7 saias de filó !"
        end_subtext = FONT.render(subtext_str, False, "green")
        subtext_rect = end_text.get_rect()
        subtext_rect.center = (CENTER_X + 20, CENTER_Y + 50)

        game_surface.blit(end_text, text_rect)
        game_surface.blit(end_subtext, subtext_rect)

        return game_surface

    def display_surface(self, surface):
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
            self.screen.blit(surface, (0, 0))
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
            scaled_surface = transform.scale(surface, (new_w, new_h))
            self.screen.blit(scaled_surface, (x, y))

    def create_walls(self):
        """
        Cria as paredes nas bordas esquerda e direita usando padrão de repetição.
        """
        # Obter dimensões da sprite da parede
        wall_width = LEFT_WALL_SPRITE.get_width()
        wall_height = LEFT_WALL_SPRITE.get_height()

        # Criar um padrão que se repete verticalmente
        # Cobrir a altura da tela + margem extra para o scroll
        num_wall_pieces = (WINDOW_HEIGHT // wall_height) + 2

        # Criar parede esquerda
        left_wall_x = LEFT_WALL_EDGE - wall_width
        for i in range(num_wall_pieces):
            y_pos = i * wall_height
            left_wall = Wall(left_wall_x, y_pos, self.game_speed, is_left=True)
            self.walls.add(left_wall)

        # Criar parede direita
        right_wall_x = RIGHT_WALL_EDGE
        for i in range(num_wall_pieces):
            y_pos = i * wall_height
            right_wall = Wall(right_wall_x, y_pos, self.game_speed, is_left=False)
            self.walls.add(right_wall)

    def start(self):
        menu_loop = False
        rodando = True

        while rodando:
            if not menu_loop and self.state != PLAYING_GAME:
                self.menu_loop()
                menu_loop = True

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
                        elif rodando:
                            if self.state == START_SCREEN:
                                self.game_speed = LANE_WIDTH // 10
                                self.player = Player(self.game_speed)
                                self.state = PLAYING_GAME
                            elif self.state == GAME_OVER or self.state == GAME_WON:
                                menu_loop = False
                                continue  # Reiniciar o jogo
                                
            if self.state == START_SCREEN:
                start_screen_surface = self.render_start_screen()
                self.display_surface(start_screen_surface)
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
                game_surface = self.render_game_screen()
                self.display_surface(game_surface)

                # Aumentar a velocidade do jogo gradualmente
                self.game_speed *= 1.00001

                # Condição de fim por derrota
                if self.player.hp <= 0:
                    self.state = GAME_OVER

                # Condição de fim por vitória
                if self.score["skirt"] >= 6:
                    self.state = GAME_WON

            elif self.state == GAME_OVER:
                game_over_surface = self.render_game_over_screen()
                self.display_surface(game_over_surface)
                ...

            elif self.state == GAME_WON:
                game_won_surface = self.render_game_won_screen()
                self.display_surface(game_won_surface)

            # Atualizar display
            display.flip()

    def create_obstacles(self):
        # teste
        if len(self.obstacles) == 0:
            scale = 0.5 + random.random()  # 0.5-1.5
            pos_x = random.randint(LEFT_WALL_EDGE, RIGHT_WALL_EDGE)
            accel = 0.25  # 0.25-1.25
            damage = int(20 * scale)

            new_obstacle = Obstacle(scale, pos_x, accel, damage)
            self.obstacles.add(new_obstacle)

    def create_collectibles(self):
        # teste
        if len(self.collectibles) < 2:
            pos_x = random.randint(LEFT_WALL_EDGE, RIGHT_WALL_EDGE)
            texture = random.choice(list(COLLECTIBLE_SPRITES.values()))

            new_collectible = Collectible(texture, pos_x)
            self.collectibles.add(new_collectible)

    def menu_loop(self) -> None:
        clock = pygame.time.Clock()

        # helper local: escala mantendo proporção e centraliza (sem blur no upscale)
        def scale_with_aspect(image: pygame.Surface, target_w: int, target_h: int) -> tuple[pygame.Surface, pygame.Rect]:
            img_w, img_h = image.get_size()
            img_ratio = img_w / img_h
            target_ratio = target_w / target_h

            if target_ratio > img_ratio:
                # tela mais "larga": encaixa pela altura
                new_h = target_h
                new_w = int(new_h * img_ratio)
            else:
                # tela mais "alta": encaixa pela largura
                new_w = target_w
                new_h = int(new_w / img_ratio)

            # escolha do scaler: nítido ao ampliar, suave ao reduzir
            upscale = (new_w > img_w) or (new_h > img_h)
            scaler = pygame.transform.scale if upscale else pygame.transform.smoothscale
            scaled = scaler(image, (new_w, new_h))

            rect = scaled.get_rect(center=(target_w // 2, target_h // 2))
            return scaled, rect

        # cria botões uma vez; o centro será atualizado a cada frame
        buttons = [
            Button("Start", (0, 0)),
            Button("Quit",  (0, 0)),
        ]

        # cache opcional para evitar reescalar todo frame
        last_size = (None, None)
        cached_bg = None
        cached_bg_rect = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
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
                        return  # Start com Enter/Espaço
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()  # o próximo frame já recentra e reescala
                # cliques nos botões
                if buttons[0].was_clicked(event):
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
                    return  # Start
                if buttons[1].was_clicked(event):
                    pygame.quit()
                    raise SystemExit

            # tamanho atual da janela
            w, h = self.screen.get_size()
            center_x = w // 2
            center_y = h // 2

            # recentra os botões
            gap = 70
            buttons[0].rect.center = (center_x, center_y - 10)
            buttons[1].rect.center = (center_x, center_y - 10 + gap)

            # --- Fundo mantendo proporção (letterbox/pillarbox se necessário) ---
            # reescala só quando o tamanho mudar (performance)
            if (w, h) != last_size:
                cached_bg, cached_bg_rect = scale_with_aspect(MAIN_MENU_SPRITE, w, h)
                last_size = (w, h)

            # pinta o "fundo" por baixo (barras laterais ou topo/rodapé, se sobrar espaço)
            self.screen.fill((18, 18, 18))
            # desenha a imagem centralizada, com proporção preservada
            self.screen.blit(cached_bg, cached_bg_rect)

            # --- Título ---
            title = FONT_TITLE.render("A Dona Aranha", True, (255, 255, 255))
            self.screen.blit(title, title.get_rect(center=(center_x, center_y - 140)))

            # --- Subtítulo ---
            subt = FONT.render("Pressione Enter ou clique em Start", True, (180, 180, 180))
            self.screen.blit(subt, subt.get_rect(center=(center_x, center_y - 90)))

            # --- Botões ---
            for b in buttons:
                b.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)
