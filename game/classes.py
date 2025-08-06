from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame import transform

from .constants import *


class Obstacle(Sprite):
    """
    Classe que representa obstáculos que caem com aceleração não-nula.
    """

    def __init__(self, texture: Surface, scale: float, x: int, accel: float):
        super().__init__()

        self.image = transform.scale_by(texture, scale)
        self.rect = self.image.get_rect()

        self.rect.midbottom = (
            x,
            -self.rect.height,
        )  # Criando obstáculo fora da tela para o spawn não ser perceptível

        self.speed = 1
        self.accel = accel

    def update(self, *args, **kwargs):
        self.speed += self.accel
        self.rect.y += self.speed

        if self.rect.y > WINDOW_HEIGHT:
            self.kill()


# Não é funcional, apenas um teste
class Collectable(Sprite):
    """
    Classe que representa um objeto coletável.
    """

    def __init__(self, textura: Surface, x: int):
        super().__init__()

        self.image = textura
        self.rect = self.image.get_rect()

        self.rect.center = (x, -self.rect.height)

        self.speed = 1

    def update(self, *args, **kwargs):
        self.rect.y += self.speed

        if self.rect.y > WINDOW_HEIGHT:
            self.kill()


class Wall(Sprite):
    """
    Classe que representa uma parede com movimento de scroll infinito.
    """

    def __init__(self, x: int, y: int):
        super().__init__()

        self.image = WALL_SPRITE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs):
        """
        Atualiza o movimento da parede criando efeito de scroll infinito.
        """
        # Mover parede para baixo
        self.rect.y += 2

        # Reposicionar se saiu da tela (padrão infinito)
        if self.rect.top >= WINDOW_HEIGHT:
            wall_height = self.image.get_height()
            self.rect.y -= wall_height * ((WINDOW_HEIGHT // wall_height) + 2)


__all__ = [
    "Obstacle",
    "Collectable",
    "Wall",
]
