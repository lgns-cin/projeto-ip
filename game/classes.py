import random

from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame import transform

from .constants import *


class Obstacle(Sprite):
    """
    Classe que representa obstáculos que caem com aceleração não-nula.
    """

    def __init__(self, scale: float, x: int, accel: float, base_damage: int):
        super().__init__()

        self.image = transform.scale_by(OBSTACLE_SPRITE.convert_alpha(), scale)
        self.rect = self.image.get_rect()

        self.rect.midbottom = (
            x,
            -self.rect.height,
        )  # Criando obstáculo fora da tela para o spawn não ser perceptível

        self.speed = 1
        self.accel = accel

        self.base_damage = base_damage

    def update(self, *args, **kwargs):
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

        if texture not in COLLECTIBLE_SPRITES.values(): # por precaução
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

        return None # não deve acontecer


class Wall(Sprite):
    """
    Classe que representa uma parede com movimento de scroll infinito.
    """

    # Velocidade compartilhada por todas as instâncias de Wall

    def __init__(
        self,
        x: int,
        y: int,
        initial_speed: int,
        is_left: bool
    ):
        super().__init__()

        self.image = LEFT_WALL_SPRITE.convert_alpha() if is_left else RIGHT_WALL_SPRITE.convert_alpha()
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


__all__ = [
    "Obstacle",
    "Collectible",
    "Wall",
]
