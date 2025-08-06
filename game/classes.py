from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame import transform

from constants import *


class Obstacle(Sprite):
    """
    Classe que representa obstáculos que caem com aceleração não-nula.
    """

    def __init__(self, texture: Surface, scale: float, x: int, accel: float):
        super().__init__()

        self.image = transform.scale_by(texture, scale)
        self.rect = self.image.get_rect()

        self.rect.midbottom = (x, -self.rect.height) # Criando obstáculo fora da tela para o spawn não ser perceptível

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