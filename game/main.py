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

        self.logical_size = WINDOW_SIZE

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

        # Variável para controle de volume
        self.music_volume = pygame.mixer.music.get_volume() if pygame.mixer.get_init() else 1.0
        self._pre_mute_volume = self.music_volume

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

        description_4 = FONT.render("A Dona Aranha deixou tudo cair!!! Você ajudará Teireza a recuperar os", False, "white")
        description_rect_4 = description_4.get_rect()
        description_rect_4.center = (CENTER_X, CENTER_Y + 24)
        description.append((description_4, description_rect_4))

        description_5 = FONT.render("materiais de costura para que ela possa produzir os presentes de sua amiga.", False, "white")
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
        subtext_rect.center = (CENTER_X + 30, CENTER_Y + 50)

        game_surface.blit(end_text, text_rect)
        game_surface.blit(end_subtext, subtext_rect)

        return game_surface

    def display_surface(self, surface):
        """
        Exibe a surface do jogo na tela, escalando e centralizando se necessário.
        Também define self.viewport para mapear mouse físico -> coordenadas lógicas.
        """
        from pygame import transform, Rect

        # Limpa a tela física
        self.screen.fill("black")

        # Garante a base lógica
        self.logical_size = WINDOW_SIZE  # (WINDOW_WIDTH, WINDOW_HEIGHT)

        screen_w, screen_h = self.screen.get_width(), self.screen.get_height()
        base_w, base_h = self.logical_size

        if screen_w == base_w and screen_h == base_h:
            # Modo janela 1:1
            self.screen.blit(surface, (0, 0))
            self.viewport = Rect(0, 0, base_w, base_h)
        else:
            # Fullscreen / janela redimensionada: letterbox com escala
            scale = min(screen_w / base_w, screen_h / base_h)
            new_w = int(base_w * scale)
            new_h = int(base_h * scale)
            x = (screen_w - new_w) // 2
            y = (screen_h - new_h) // 2

            scaled_surface = transform.scale(surface, (new_w, new_h))
            self.screen.blit(scaled_surface, (x, y))

            # >>> viewport visível (centralizada e escalada)
            self.viewport = Rect(x, y, new_w, new_h)


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

    def load_background_music(self):
        """Carrega e toca a música de fundo do jogo."""
        try:
            pygame.mixer.music.load(BACKGROUND_MUSIC)
            pygame.mixer.music.play(-1)  # -1 significa loop infinito
            pygame.mixer.music.set_volume(0.3)  # Volume inicial
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
                        rodando = evento.key

                        if evento.key == pygame_constants.K_F11:
                            self.toggle_fullscreen()
                        elif rodando:
                            if self.state == START_SCREEN:
                                self.reset_game()
                                self.state = PLAYING_GAME
                            elif self.state == PLAYING_GAME:
                                # <<< Tecla P pausa o jogo >>>
                                if evento.key == pygame_constants.K_ESCAPE:
                                    self.pause_menu()
                            elif self.state == GAME_OVER or self.state == GAME_WON:
                                self.load_background_music()  # Reinicia a música ao voltar do game over
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
                self.game_speed *= 1.00005

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
        def scale_with_aspect(image: pygame.Surface, target_w: int, target_h: int) -> tuple[pygame.Surface, pygame.Rect]:
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
        def pre_start_blink(cached_bg: pygame.Surface, cached_bg_rect: pygame.Rect, center_x: int, center_y: int, buttons: list[object]) -> None:
            duration_ms = 1000
            interval_ms = 120
            start = pygame.time.get_ticks()
            visible = True
            while pygame.time.get_ticks() - start < duration_ms:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit(); raise SystemExit
                self.screen.fill((18, 18, 18))
                if visible:
                    cached_bg.set_alpha(255)
                    self.screen.blit(cached_bg, cached_bg_rect)

                title = FONT_TITLE.render("A Dona Aranha", True, (255, 255, 255))
                self.screen.blit(title, title.get_rect(center=(center_x, center_y - 140)))
                subt = FONT.render(f"Enter para jogar • Volume: {vol_pct}", True, (180, 180, 180))
                self.screen.blit(subt, subt.get_rect(center=(center_x, center_y - 90)))
                for b in buttons:
                    b.draw(self.screen)

                pygame.display.flip()
                pygame.time.delay(interval_ms)
                visible = not visible

        # --- controle de volume (garante campos) ---
        if not hasattr(self, "music_volume"):
            self.music_volume = pygame.mixer.music.get_volume() if pygame.mixer.get_init() else 1.0
            self._pre_mute_volume = self.music_volume

        def _set_vol(v: float):
            v = max(0.0, min(1.0, float(v)))
            if pygame.mixer.get_init():
                pygame.mixer.music.set_volume(v)
            self.music_volume = v

        def _vol_down(): _set_vol(self.music_volume - 0.05)
        def _vol_up():   _set_vol(self.music_volume + 0.05)
        def _toggle_mute():
            if self.music_volume > 0.0:
                self._pre_mute_volume = self.music_volume
                _set_vol(0.0)
            else:
                _set_vol(self._pre_mute_volume if getattr(self, "_pre_mute_volume", 0.0) > 0.0 else 0.5)

        # cria botões uma vez; o centro é atualizado a cada frame
        buttons = [
            Button("Começar", (0, 0), (260, 60)),
            Button("Vol -",   (0, 0), (120, 60)),
            Button("Vol +",   (0, 0), (120, 60)),
            Button("Mutar",   (0, 0), (260, 60)),
            Button("Sair",    (0, 0), (260, 60)),
        ]

        # cache para não reescalar sempre
        last_size = (None, None)
        cached_bg = None
        cached_bg_rect = None

        # parâmetros da onda (opacidade)
        wave_hz = 0.5  # 0.5 Hz → ciclo ~2 s
        alpha_min, alpha_max = 120, 255
        alpha_span = alpha_max - alpha_min

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if event.type == pygame.KEYDOWN:
                    # iniciar
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        pre_start_blink(cached_bg, cached_bg_rect, center_x, center_y, buttons)
                        self.state = START_SCREEN
                        self.game_speed = LANE_WIDTH // 10
                        self.player = Player(self.game_speed)
                        self.score = {"web": 0, "skirt": 0, "needle": 0, "fabric": 0, "mockup": 0}
                        return
                    # sair
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); raise SystemExit
                    # fullscreen
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    # atalhos de volume
                    if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        _vol_down()
                    if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                        _vol_up()
                    if event.key == pygame.K_m:
                        _toggle_mute()

                # cliques
                if buttons[0].was_clicked(event):  # Start
                    pre_start_blink(cached_bg, cached_bg_rect, center_x, center_y, buttons)
                    self.state = START_SCREEN
                    self.game_speed = LANE_WIDTH // 10
                    self.player = Player(self.game_speed)
                    self.score = {"web": 0, "skirt": 0, "needle": 0, "fabric": 0, "mockup": 0}
                    return
                if buttons[1].was_clicked(event):  # Vol -
                    _vol_down()
                if buttons[2].was_clicked(event):  # Vol +
                    _vol_up()
                if buttons[3].was_clicked(event):  # Mutar
                    _toggle_mute()
                if buttons[4].was_clicked(event):  # Quit
                    pygame.quit(); raise SystemExit

            # tamanho atual e centralização
            w, h = self.screen.get_size()
            center_x, center_y = w // 2, h // 2

            # posicionamento
            gap = 70
            buttons[0].rect.center = (center_x, center_y - 10)            # Start
            buttons[1].rect.center = (center_x - 70, center_y + 60)      # Vol -
            buttons[2].rect.center = (center_x + 70, center_y + 60)      # Vol +
            buttons[3].rect.center = (center_x,        center_y + 130)    # Mutar
            buttons[4].rect.center = (center_x,        center_y + 200)    # Quit

            # fundo proporcional (reescala quando w/h mudar)
            if (w, h) != last_size:
                cached_bg, cached_bg_rect = scale_with_aspect(MAIN_MENU_SPRITE, w, h)
                last_size = (w, h)

            # wave de opacidade
            t = pygame.time.get_ticks() / 1000.0
            wave01 = 0.5 * (1.0 + math.sin(2.0 * math.pi * wave_hz * t))
            cached_bg.set_alpha(int(alpha_min + alpha_span * wave01))

            # desenhar
            self.screen.fill((18, 18, 18))
            self.screen.blit(cached_bg, cached_bg_rect)

            title = FONT_TITLE.render("A Dona Aranha", True, (255, 255, 255))
            self.screen.blit(title, title.get_rect(center=(center_x, center_y - 140)))

            vol_pct = int(round(self.music_volume * 100))
            subt = FONT.render(f"Enter para jogar • Volume: {vol_pct}", True, (180, 180, 180))
            self.screen.blit(subt, subt.get_rect(center=(center_x, center_y - 90)))

            for b in buttons:
                b.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)

    def pause_menu(self):
        """Overlay de pausa com Retomar / Vol- / Vol+ / Mutar / Menu."""
        from pygame import Surface, SRCALPHA

        clock = time.Clock()

        # snapshot do frame atual (congelado)
        backdrop = self.render_game_screen()  # sua função que desenha o jogo em Surface(WINDOW_SIZE)

        # Centro em coordenadas lógicas
        base_w, base_h = self.logical_size
        cx, cy = base_w // 2, base_h // 2

        # Botões (usam coordenadas lógicas)
        buttons = [
            Button("Retomar",        (cx,        cy - 10), (260, 60)),
            Button("Volume -",       (cx - 70,  cy + 60), (120, 60)),
            Button("Volume +",       (cx + 70,  cy + 60), (120, 60)),
            Button("Mutar/Desmutar", (cx,        cy + 130), (260, 60)),
            Button("Menu",           (cx,        cy + 200), (260, 60)),
        ]

        # Volume helpers
        if not hasattr(self, "music_volume"):
            try:
                self.music_volume = pygame.mixer.music.get_volume()
            except Exception:
                self.music_volume = 1.0
        self._pre_mute_volume = getattr(self, "_pre_mute_volume", self.music_volume)

        def set_vol(v: float):
            v = max(0.0, min(1.0, float(v)))
            try:
                pygame.mixer.music.set_volume(v)
            except Exception:
                pass
            self.music_volume = v

        def vol_down(): set_vol(self.music_volume - 0.1)
        def vol_up():   set_vol(self.music_volume + 0.1)
        def toggle_mute():
            if self.music_volume > 0.0:
                self._pre_mute_volume = self.music_volume
                set_vol(0.0)
            else:
                set_vol(self._pre_mute_volume if self._pre_mute_volume > 0 else 0.5)

        paused = True
        while paused:
            for ev in event.get():
                if ev.type == pygame_constants.QUIT:
                    pygame.quit(); raise SystemExit
                if ev.type == pygame_constants.KEYDOWN:
                    if ev.key in (pygame_constants.K_ESCAPE, pygame_constants.K_SPACE, pygame_constants.K_RETURN):
                        paused = False  # retomar
                    elif ev.key == pygame_constants.K_F11:
                        self.toggle_fullscreen()  # viewport será atualizada no próximo display_surface
                    elif ev.key in (pygame_constants.K_MINUS, pygame_constants.K_KP_MINUS):
                        vol_down()
                    elif ev.key in (pygame_constants.K_EQUALS, pygame_constants.K_PLUS, pygame_constants.K_KP_PLUS):
                        vol_up()
                    elif ev.key == pygame_constants.K_m:
                        toggle_mute()
                elif ev.type == pygame_constants.MOUSEBUTTONDOWN and ev.button == 1:
                    # <<< clique convertido para coordenadas lógicas >>>
                    lpos = self.to_logical(ev.pos)
                    if buttons[0].rect.collidepoint(lpos):  # Retomar
                        paused = False
                    elif buttons[1].rect.collidepoint(lpos):  # Vol -
                        vol_down()
                    elif buttons[2].rect.collidepoint(lpos):  # Vol +
                        vol_up()
                    elif buttons[3].rect.collidepoint(lpos):  # Mutar
                        toggle_mute()
                    elif buttons[4].rect.collidepoint(lpos):  # Menu
                        self.state = START_SCREEN
                        self.start()  # reiniciar o jogo
                        return

            # ---- desenhar overlay na resolução LÓGICA ----
            surface = backdrop.copy()  # Surface(WINDOW_SIZE)
            overlay = Surface(self.logical_size, SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surface.blit(overlay, (0, 0))

            vol_pct = int(round(self.music_volume * 100))
            title = FONT_TITLE.render("Pausado", True, "white")
            sub =   FONT.render(f"Volume: {vol_pct}%", True, (200, 200, 200))
            surface.blit(title, title.get_rect(center=(cx, cy - 120)))
            surface.blit(sub,   sub.get_rect(center=(cx, cy - 70)))

            # Hover: mouse lógico
            mouse_logical = self.to_logical(pygame.mouse.get_pos())
            for b in buttons:
                # seu Button.draw(surface, mouse_pos=None) pode aceitar mouse_pos opcional;
                # se não aceitar, internamente ele usará pygame.mouse.get_pos(); nesse caso,
                # você pode adaptar o Button para receber mouse_pos. Aqui fica genérico:
                try:
                    b.draw(surface, mouse_pos=mouse_logical)
                except TypeError:
                    b.draw(surface)

            # ---- apresenta usando o MESMO pipeline do jogo ----
            self.display_surface(surface)
            display.flip()
            clock.tick(60)

    def to_logical(self, phys_pos: tuple[int, int]) -> tuple[int, int]:
        """
        Converte coordenadas físicas (monitor) para lógicas (mundo do jogo),
        usando self.viewport definida em display_surface(...).
        """
        if not hasattr(self, "viewport"):
            return phys_pos
        vx, vy, vw, vh = self.viewport
        if vw == 0 or vh == 0:
            return phys_pos
        lx = (phys_pos[0] - vx) * self.logical_size[0] / vw
        ly = (phys_pos[1] - vy) * self.logical_size[1] / vh
        return int(lx), int(ly)
