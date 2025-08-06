from pygame.sprite import Sprite
from pygame.constants import *

from constants import *


class Player(Sprite):
    """
    Classe que representa o personagem jogável, que deve responder a inputs e interagir com coletáveis e obstáculos.
    """

    def __init__(self):
        super().__init__()

        self.image = PLAYER_SPRITE       # textura predefinida
        self.rect = self.image.get_rect()

        # Levando em conta a distância ao centro do sprite
        self.leftmost = LEFT_WALL + (self.rect.width // 2)
        self.rightmost  = RIGHT_WALL - (self.rect.width // 2)

        self.rect.center = (self.rightmost, CENTER_Y)

        self.mid_jump = False
        self.target_pos = -1
        self.speed = 30

        self.hp = 100

    def update(self, **kwargs):
        keys = kwargs.get("keys")

        if self.detect_jump(keys):
            self.jump()

        ... # Lógica pra receber dano, coletar pontos, etc.

    def detect_jump(self, keys):
        if not self.mid_jump:
            if keys[K_LEFT] and self.rect.centerx >= self.rightmost:
                self.mid_jump = True
                self.target_pos = self.leftmost

            if keys[K_RIGHT] and self.rect.centerx <= self.leftmost:
                self.mid_jump = True
                self.target_pos = self.rightmost

        return self.mid_jump

    def jump(self):
        if self.rect.centerx < self.target_pos:
            self.rect.centerx = min(self.target_pos, self.rect.centerx + self.speed)
        elif self.rect.centerx > self.target_pos:
            self.rect.centerx = max(self.target_pos, self.rect.centerx - self.speed)
        else: # self.rect.centerx == self.destino
            self.mid_jump = False