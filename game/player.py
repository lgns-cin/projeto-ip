from pygame.sprite import Sprite
from pygame.constants import K_SPACE, K_LEFT, K_RIGHT, K_a, K_d
from pygame import transform

from .constants import *


class Player(Sprite):
    """
    Classe que representa o personagem jogável, que deve responder a inputs e interagir com coletáveis e obstáculos.
    """

    def __init__(self):
        super().__init__()

        self.image = PLAYER_SPRITE  # textura predefinida
        self.rect = self.image.get_rect()
        self.leftmost = LEFT_WALL_EDGE + (self.rect.width // 2)
        self.rightmost = RIGHT_WALL_EDGE - (self.rect.width // 2)

        # Iniciar na parede direita
        self.rect.centerx = self.rightmost
        self.rect.centery = CENTER_Y
        self.facing_left = False  # False = sprite original (patas para a direita), True = sprite invertido (patas para a esquerda)

        self.mid_jump = False
        self.target_pos = -1

        # Parâmetros do salto
        self.jump_config = {
            "speed": 20,  # número de frames da animação do salto
            "height": LANE_WIDTH * 3,  # altura máxima do salto
            "flip_threshold": 0.75,  # momento para inverter sprite (75% do salto)
        }

        # Estado atual do salto
        self.jump_state = {
            "start_x": 0,
            "start_y": 0,
            "progress": 0.0,  # De 0 a 1 (0% a 100% do salto)
            "sprite_flipped": False,  # Se já inverteu o sprite durante o salto atual
        }

        self.hp = 100

    def update(self, **kwargs):
        keys = kwargs.get("keys")

        if self.detect_jump(keys):
            self.jump()

        ...  # Lógica pra receber dano, coletar pontos, etc.

    def detect_jump(self, keys):
        """Detecta se o jogador quer iniciar um salto e configura os parâmetros.

        Controles disponíveis:
        - Barra de espaço: pula automaticamente para a parede oposta
        - Setas/A-D: direcionais para escolher a direção do salto
        """
        if not self.mid_jump:

            right_keys = [K_RIGHT, K_d]
            left_keys = [K_LEFT, K_a]
            jump_keys = [K_SPACE, *right_keys, *left_keys]

            # Verificar se alguma tecla de salto foi pressionada
            if key_pressed := any(keys[key] for key in jump_keys):
                is_right_direction = key_pressed and any(
                    keys[key] for key in right_keys
                )
                is_left_direction = key_pressed and any(keys[key] for key in left_keys)

                # Condições específicas para saltos direcionais
                valid_directional_jump = (
                    is_left_direction
                    and self.rect.centerx
                    >= self.rightmost  # Esquerda na parede direita
                    or is_right_direction
                    and self.rect.centerx <= self.leftmost  # Direita na parede esquerda
                )

                if keys[K_SPACE] or valid_directional_jump:
                    self.start_jump()

        return self.mid_jump

    def start_jump(self):
        """Inicia um novo salto para a parede oposta automaticamente."""

        # Determinar direção baseada na posição atual
        if self.rect.centerx >= self.rightmost:
            # Está na parede direita, salta para a esquerda
            target_position = self.leftmost
        elif self.rect.centerx <= self.leftmost:
            # Está na parede esquerda, salta para a direita
            target_position = self.rightmost
        else:
            # Se estiver no meio (durante um salto), não faz nada
            return

        self.mid_jump = True
        self.target_pos = target_position
        self.jump_state["start_x"] = self.rect.centerx
        self.jump_state["start_y"] = self.rect.centery
        self.jump_state["progress"] = 0.0
        self.jump_state["sprite_flipped"] = False

    def flip_sprite_if_needed(self):
        """
        Inverte o sprite baseado na posição de destino da aranha para que as patas sempre toquem a parede.
        """

        if self.target_pos == self.leftmost and not self.facing_left:
            self.image = transform.flip(self.image, True, False)
            self.facing_left = True

        elif self.target_pos == self.rightmost and self.facing_left:
            self.image = transform.flip(self.image, True, False)
            self.facing_left = False

    def calculate_jump_position(self):
        """Calcula a posição atual da aranha durante o salto usando movimento parabólico."""
        progress = self.jump_state["progress"]

        # Movimento horizontal linear
        new_x = int(
            self.jump_state["start_x"]
            + (self.target_pos - self.jump_state["start_x"]) * progress
        )

        # Movimento vertical parabólico (arco do salto)
        # Fórmula: y = -4h * t * (t - 1) onde h é a altura máxima e t é o progresso
        height_offset = -4 * self.jump_config["height"] * progress * (progress - 1)
        new_y = int(self.jump_state["start_y"] - height_offset)

        return new_x, new_y

    def should_flip_sprite(self):
        """Verifica se é hora de inverter o sprite durante o salto."""
        return (
            self.jump_state["progress"] >= self.jump_config["flip_threshold"]
            and not self.jump_state["sprite_flipped"]
        )

    def complete_jump(self):
        """Finaliza o salto posicionando a aranha exatamente no destino."""
        self.rect.centerx = self.target_pos
        self.rect.centery = self.jump_state["start_y"]
        self.mid_jump = False
        self.jump_state["progress"] = 0.0

    def jump(self):
        """Executa um frame do salto, atualizando posição e sprite conforme necessário."""
        # Incrementar progresso do salto
        self.jump_state["progress"] += 1 / self.jump_config["speed"]

        # Inverter sprite no momento apropriado
        if self.should_flip_sprite():
            self.flip_sprite_if_needed()
            self.jump_state["sprite_flipped"] = True

        # Verificar se o salto foi completado
        if self.jump_state["progress"] >= 1.0:
            self.complete_jump()
        else:
            # Calcular e aplicar nova posição a cada momento do salto
            new_x, new_y = self.calculate_jump_position()
            self.rect.centerx = new_x
            self.rect.centery = new_y
