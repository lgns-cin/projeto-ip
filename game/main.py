import random
import pygame
import math

from .classes import *
from .player import Player
from .constants import *

from pygame import display, time, event, key, constants as pygame_constants
from pygame.sprite import Group
from pygame import Surface
import pygame.mixer


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
        self.score = {"web": 0, "skirt": 0, "needle": 0, "fabric": 0, "mockup": 0}

        # Sistema de spawn melhorado
        self.spawn_config = {
            "obstacle_timer": 0,
            "obstacle_interval": 120,  # frames entre spawns de obstáculos
            "collectible_timer": 0,
            "collectible_interval": 180,  # frames entre spawns de coletáveis
            "max_obstacles": 3,  # máximo de obstáculos na tela
            "max_collectibles": 2,  # máximo de coletáveis na tela
        }

        self.background = Group()
        self.collectibles = Group()
        self.obstacles = Group()
        self.walls = Group()

        # Inicializar e tocar música de fundo
        self.load_background_music()

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

        description = []

        description_1 = FONT.render("Cansada de ver sua amiga barata sendo chamada de mentirosa", False, "white")
        description_rect_1 = description_1.get_rect()
        description_rect_1.center = (CENTER_X, CENTER_Y - 48)
        description.append((description_1, description_rect_1))

        description_2 = FONT.render("por não ter 7 saias de filó, a aranha Teireza decidiu costurar", False, "white")
        description_rect_2 = description_2.get_rect()
        description_rect_2.center = (CENTER_X, CENTER_Y - 24)
        description.append((description_2, description_rect_2))

        description_3 = FONT.render("novas saias para que ela completasse sua coleção. Mas... Ops!", False, "white")
        description_rect_3 = description_3.get_rect()
        description_rect_3.center = (CENTER_X, CENTER_Y)
        description.append((description_3, description_rect_3))

        description_4 = FONT.render("A Dona Aranha deixou tudo cair!!! Você ajudará Teireza a recuperar", False, "white")
        description_rect_4 = description_4.get_rect()
        description_rect_4.center = (CENTER_X, CENTER_Y + 24)
        description.append((description_4, description_rect_4))

        description_5 = FONT.render("de costura para que ela possa produzir os presentes de sua amiga.", False, "white")
        description_rect_5 = description_5.get_rect()
        description_rect_5.center = (CENTER_X, CENTER_Y + 48)
        description.append((description_5, description_rect_5))

        description_6 = FONT.render("Suba pelas paredes e tome cuidado para a chuva não a derrubar!", False, "white")
        description_rect_6 = description_6.get_rect()
        description_rect_6.center = (CENTER_X, CENTER_Y + 96)
        description.append((description_6, description_rect_6))

        subtitle = FONT.render("Aperte qualquer botão para começar", False, "white")
        subtitle_rect = subtitle.get_rect()
        subtitle_rect.center = (CENTER_X, CENTER_Y + 120)

        game_surface.blits(description)
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

        skirt_text = FONT.render(f"{self.score.get('skirt')}", False, "white")
        self.render_icon_with_text(
            surface, skirt_text, SKIRT_SPRITE, RIGHT_WALL_EDGE + 2 * x_offset, y_offset
        )

        needle_text = FONT.render(f"{self.score.get('needle')}", False, "white")
        self.render_icon_with_text(
            surface, needle_text, COLLECTIBLE_SPRITES.get("needle"), x_offset, y_offset
        )

        x_offset += COLLECTIBLE_SPRITES.get("needle").get_width() + LANE_WIDTH // 6

        web_text = FONT.render(f"{self.score.get('fabric')}", False, "white")
        self.render_icon_with_text(
            surface, web_text, COLLECTIBLE_SPRITES.get("fabric"), x_offset, y_offset
        )

        x_offset += COLLECTIBLE_SPRITES.get("fabric").get_width() + LANE_WIDTH // 6

        web_text = FONT.render(f"{self.score.get('mockup')}", False, "white")
        self.render_icon_with_text(
            surface, web_text, COLLECTIBLE_SPRITES.get("mockup"), x_offset, y_offset
        )

    def render_icon_with_text(
        self, surface: Surface, text: Surface, icon: Surface, x_offset, y_offset
    ):
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

        text_str = f"E a chuva derrubou :( A aranha teceu {self.score.get('skirt')} saias e coletou {self.score.get('web')} teias"
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

        text_str = (
            f"Parabéns! Você venceu! A aranha teceu {self.score.get('skirt')} saias"
        )
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
                                self.reset_game()
                                self.state = PLAYING_GAME
                            elif self.state == GAME_OVER:
                                self.load_background_music()  # Reinicia a música ao voltar do game over
                                self.state = START_SCREEN

    def reset_game(self):
        """Reseta o estado do jogo para uma nova partida."""
        self.game_speed = LANE_WIDTH // 10
        self.player = Player(self.game_speed)
        self.score = {"web": 0, "skirt": 0, "needle": 0, "fabric": 0, "mockup": 0}

        # Reset dos timers de spawn
        self.spawn_config = {
            "obstacle_timer": 0,
            "obstacle_interval": 120,
            "collectible_timer": 0,
            "collectible_interval": 180,
            "max_obstacles": 3,
            "max_collectibles": 2,
        }

        # Limpar grupos de sprites
        self.obstacles.empty()
        self.collectibles.empty()

        # Reiniciar música de fundo
        self.load_background_music()

    def load_background_music(self):
        """Carrega e toca a música de fundo do jogo."""
        try:
            pygame.mixer.music.load(BACKGROUND_MUSIC)
            pygame.mixer.music.play(-1)  # -1 significa loop infinito
        except pygame.error as e:
            print(f"Erro ao carregar música de fundo: {e}")

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
                                self.reset_game()
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
                self.obstacles.update(speed=self.game_speed)
                self.collectibles.update(speed=self.game_speed)
                self.walls.update(speed=self.game_speed)

                self.player.update(
                    keys=keys,
                    # speed = self.game_speed,
                    # obstacles = self.obstacles,
                    # collectibles = self.collectibles
                    game=self,
                )

                # Renderização
                game_surface = self.render_game_screen()
                self.display_surface(game_surface)

                # Aumentar a velocidade do jogo gradualmente
                self.game_speed *= 1.00015

                # Condição de fim por derrota
                if self.player.hp <= 0:
                    pygame.mixer.music.stop()  # Para a música quando perde
                    self.state = GAME_OVER

                # Condição de fim por vitória
                if self.score["skirt"] >= 6:
                    pygame.mixer.music.stop()  # Para a música quando vence
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
        """
        Sistema inteligente de spawn de obstáculos com timer e variedade.
        """
        self.spawn_config["obstacle_timer"] += 1

        # Verificar se é hora de spawnar e se não excedeu o limite
        if (
            self.spawn_config["obstacle_timer"]
            >= self.spawn_config["obstacle_interval"]
            and len(self.obstacles) < self.spawn_config["max_obstacles"]
        ):

            # Reset do timer
            self.spawn_config["obstacle_timer"] = 0

            # Reduzir intervalo gradualmente para aumentar dificuldade
            if self.spawn_config["obstacle_interval"] > 60:  # mínimo de 1 segundo
                self.spawn_config["obstacle_interval"] -= 1

            # Gerar propriedades da gota
            scale = random.uniform(0.3, 1.5) + (self.game_speed / 100)  # Tamanho variado, aumenta com o decorrer do jogo

            # Escolher posição em uma das 3 lanes válidas
            lane = random.randint(1, 3)
            lane_center = LEFT_WALL_EDGE + (lane - 0.5) * LANE_WIDTH
            pos_x = int(lane_center)

            # Dano baseado no tamanho
            damage = int(15 * scale + random.randint(5, 15))

            new_obstacle = Obstacle(scale, pos_x, damage, self.game_speed)
            self.obstacles.add(new_obstacle)

    def create_collectibles(self):
        """
        Sistema inteligente de spawn de coletáveis com probabilidades balanceadas.
        """
        self.spawn_config["collectible_timer"] += 1

        # Verificar se é hora de spawnar e se não excedeu o limite
        if (
            self.spawn_config["collectible_timer"]
            >= self.spawn_config["collectible_interval"]
            and len(self.collectibles) < self.spawn_config["max_collectibles"]
        ):

            # Reset do timer
            self.spawn_config["collectible_timer"] = 0

            # Escolher posição em uma das 3 lanes válidas
            lane = random.randint(1, 3)
            lane_center = LEFT_WALL_EDGE + (lane - 0.5) * LANE_WIDTH
            pos_x = int(lane_center)

            # Probabilidades balanceadas para diferentes tipos
            collectible_odds = {
                "needle": 30,
                "fabric": 25,
                "mockup": 20,
                "web": 15,
            }

            # Escolher tipo baseado nas probabilidades
            collectible_types = list(collectible_odds.keys())
            odds = list(collectible_odds.values())
            chosen_type = random.choices(collectible_types, weights=odds)[0]

            texture = COLLECTIBLE_SPRITES[chosen_type]
            new_collectible = Collectible(texture, pos_x)
            self.collectibles.add(new_collectible)

    def menu_loop(self) -> None:
        clock = pygame.time.Clock()

        # --- helper: escala com proporção e centraliza ---
        def scale_with_aspect(
            image: pygame.Surface, target_w: int, target_h: int
        ) -> tuple[pygame.Surface, pygame.Rect]:
            iw, ih = image.get_size()
            r_img = iw / ih
            r_tgt = target_w / target_h
            if r_tgt > r_img:
                new_h = target_h
                new_w = int(new_h * r_img)
            else:
                new_w = target_w
                new_h = int(new_w / r_img)
            # usa scale no upscale (mais nítido), smoothscale no downscale
            upscale = new_w > iw or new_h > ih
            scaler = pygame.transform.scale if upscale else pygame.transform.smoothscale
            scaled = scaler(image, (new_w, new_h))
            rect = scaled.get_rect(center=(target_w // 2, target_h // 2))
            return scaled, rect

        # --- helper: piscada de 1s no fundo antes de iniciar ---
        def pre_start_blink(
            cached_bg: pygame.Surface,
            cached_bg_rect: pygame.Rect,
            center_x: int,
            center_y: int,
            buttons: list[object],
        ) -> None:
            duration_ms = 1000
            interval_ms = 120
            start = pygame.time.get_ticks()
            visible = True
            while pygame.time.get_ticks() - start < duration_ms:
                # permite fechar a janela durante a piscada
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit

                self.screen.fill((18, 18, 18))
                if visible:
                    cached_bg.set_alpha(255)
                    self.screen.blit(cached_bg, cached_bg_rect)

                # redesenha UI (título, subtítulo, botões) por cima
                title = FONT_TITLE.render("A Dona Aranha", True, (255, 255, 255))
                self.screen.blit(
                    title, title.get_rect(center=(center_x, center_y - 140))
                )
                subt = FONT.render(
                    "Pressione Enter ou clique em Start", True, (180, 180, 180)
                )
                self.screen.blit(subt, subt.get_rect(center=(center_x, center_y - 90)))
                for b in buttons:
                    b.draw(self.screen)

                pygame.display.flip()
                pygame.time.delay(interval_ms)
                visible = not visible

        # cria botões uma vez; o centro é atualizado a cada frame
        buttons = [
            Button("Start", (0, 0)),
            Button("Quit", (0, 0)),
        ]

        # cache para não reescalar sempre
        last_size = (None, None)
        cached_bg = None
        cached_bg_rect = None

        # parâmetros da onda (opacidade)
        wave_hz = 0.5  # 0.5 Hz → ciclo de ~2 s
        alpha_min = 120  # mínimo de opacidade
        alpha_max = 255  # máximo de opacidade
        alpha_span = alpha_max - alpha_min

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        # piscada de 1s e inicia
                        pre_start_blink(
                            cached_bg, cached_bg_rect, center_x, center_y, buttons
                        )
                        self.state = START_SCREEN
                        self.game_speed = LANE_WIDTH // 10
                        self.player = Player(self.game_speed)
                        self.score = {
                            "web": 0,
                            "skirt": 0,
                            "needle": 0,
                            "fabric": 0,
                            "mockup": 0,
                        }
                        self.load_background_music()  # Reinicia a música
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                # cliques
                if buttons[0].was_clicked(event):
                    pre_start_blink(
                        cached_bg, cached_bg_rect, center_x, center_y, buttons
                    )
                    self.state = START_SCREEN
                    self.game_speed = LANE_WIDTH // 10
                    self.player = Player(self.game_speed)
                    self.score = {
                        "web": 0,
                        "skirt": 0,
                        "needle": 0,
                        "fabric": 0,
                        "mockup": 0,
                    }
                    self.load_background_music()  # Reinicia a música
                    return
                if buttons[1].was_clicked(event):
                    pygame.quit()
                    raise SystemExit

            # tamanho atual e centralização
            w, h = self.screen.get_size()
            center_x = w // 2
            center_y = h // 2

            gap = 70
            buttons[0].rect.center = (center_x, center_y - 10)
            buttons[1].rect.center = (center_x, center_y - 10 + gap)

            # reescala o fundo apenas quando w/h mudar
            if (w, h) != last_size:
                cached_bg, cached_bg_rect = scale_with_aspect(MAIN_MENU_SPRITE, w, h)
                last_size = (w, h)

            # --- efeito wave de opacidade no fundo ---
            t = pygame.time.get_ticks() / 1000.0
            # seno em [0..1]
            wave01 = 0.5 * (1.0 + math.sin(2.0 * math.pi * wave_hz * t))
            alpha = int(alpha_min + alpha_span * wave01)
            cached_bg.set_alpha(alpha)

            # desenha
            self.screen.fill((18, 18, 18))
            self.screen.blit(cached_bg, cached_bg_rect)

            title = FONT_TITLE.render("A Dona Aranha", True, (255, 255, 255))
            self.screen.blit(title, title.get_rect(center=(center_x, center_y - 140)))

            subt = FONT.render(
                "Pressione Enter ou clique em Start", True, (180, 180, 180)
            )
            self.screen.blit(subt, subt.get_rect(center=(center_x, center_y - 90)))

            for b in buttons:
                b.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)
