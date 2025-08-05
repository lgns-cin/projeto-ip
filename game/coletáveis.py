import pygame.image as image
import pygame.transform as transform
from pygame.sprite import Sprite
from pygame import Surface


class Coletável(Sprite):

    def __init__(self, textura: Surface, escala: float):
        super().__init__()

        self.image = transform.scale_by(textura, escala)
        self.rect = self.image.get_rect()

    ... # Vou testar mais coisas depois