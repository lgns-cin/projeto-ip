import random
import pygame

from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame import transform

from .constants import *


class Obstacle(Sprite):
    """
    Classe que representa obstáculos que caem com aceleração não-nula.
    Velocidade é inversamente proporcional ao tamanho.
    """

    def __init__(self, scale: float, x: int, base_damage: int, game_speed: float = 2):
        super().__init__()

        self.scale = scale
        self.image = transform.scale_by(OBSTACLE_SPRITE.convert_alpha(), scale)
        self.rect = self.image.get_rect()

        self.rect.midbottom = (
            x,
            -self.rect.height,
        )  # Criando obstáculo fora da tela para o spawn não ser perceptível

        # Velocidade suavemente proporcional ao tamanho
        # Gotas menores caem um pouco mais rápido, mas não de forma extrema
        # Fórmula: velocidade diminui conforme o tamanho aumenta, mas de forma suave
        speed_multiplier = 1.3 - (
            scale * 0.4
        )  # Varia de ~0.9 (grande) a ~1.1 (pequena)
        speed_multiplier = max(
            0.7, min(1.3, speed_multiplier)
        )  # Limitar entre 0.7x e 1.3x

        self.base_speed = game_speed * speed_multiplier
        self.speed = self.base_speed

        # Aceleração mínima e constante para todas as gotas
        self.accel = 0.1

        self.base_damage = base_damage

    def update(self, *args, **kwargs):
        # Obter velocidade do jogo atual se fornecida
        game_speed = kwargs.get("speed", 2)

        # Recalcular velocidade base se a velocidade do jogo mudou
        speed_multiplier = 1.3 - (self.scale * 0.4)
        speed_multiplier = max(0.7, min(1.3, speed_multiplier))
        self.base_speed = game_speed * speed_multiplier

        self.speed += self.accel
        self.rect.y += self.speed

        if self.rect.y > WINDOW_HEIGHT:
            self.kill()

    def get_damage(self):
        return self.base_damage


class Collectible(Sprite):
    """
    Classe que representa um objeto coletável.
    """

    def __init__(self, texture: Surface, x: int):
        super().__init__()

        if texture not in COLLECTIBLE_SPRITES.values():  # por precaução
            texture = random.choice(list(COLLECTIBLE_SPRITES.values()))

        self.image = texture
        self.rect = self.image.get_rect()

        self.rect.center = (x, -self.rect.height)

    def update(self, *args, **kwargs):
        self.rect.y += kwargs.get("speed")

        if self.rect.y > WINDOW_HEIGHT:
            self.kill()

    def get_type(self):
        for sprite_name in COLLECTIBLE_SPRITES.keys():
            if self.image == COLLECTIBLE_SPRITES.get(sprite_name):
                return sprite_name

        return None  # não deve acontecer


class Wall(Sprite):
    """
    Classe que representa uma parede com movimento de scroll infinito.
    """

    # Velocidade compartilhada por todas as instâncias de Wall

    def __init__(self, x: int, y: int, initial_speed: int, is_left: bool):
        super().__init__()

        self.image = (
            LEFT_WALL_SPRITE.convert_alpha()
            if is_left
            else RIGHT_WALL_SPRITE.convert_alpha()
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shared_speed = initial_speed

    def set_speed(self, new_speed):
        """Define uma nova velocidade para todas as paredes."""
        self.shared_speed = max(0, new_speed)  # Não permitir velocidade negativa

    def get_speed(self):
        """Retorna a velocidade atual das paredes."""
        return self.shared_speed

    def update(self, *args, **kwargs):
        """
        Atualiza o movimento da parede criando efeito de scroll infinito.
        """

        if "speed" in kwargs:
            self.set_speed(kwargs["speed"])

        # Usar velocidade compartilhada da classe
        self.rect.y += self.shared_speed

        # Reposicionar se saiu da tela (padrão infinito)
        if self.rect.top >= WINDOW_HEIGHT:
            wall_height = self.image.get_height()
            self.rect.y -= wall_height * ((WINDOW_HEIGHT // wall_height) + 2)


class Button:
    def __init__(self, text: str, center: tuple[int, int], size: tuple[int, int]):
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = center
        self.text = text
        self.font = FONT  # usa fonte default
        self.base_color = (30, 30, 30)
        self.hover_color = (60, 60, 60)
        self.text_color = (255, 255, 255)

    def draw(self, surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None) -> None:
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()  # fallback (procedural)
        is_hover = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(
            surface,
            self.hover_color if is_hover else self.base_color,
            self.rect  # cantos retos; acrescente border_radius se quiser arredondar
        )
        label = self.font.render(self.text, True, self.text_color)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def was_clicked(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


__all__ = ["Obstacle", "Collectible", "Wall", "Button"]
