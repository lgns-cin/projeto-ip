import pygame as pg
from pygame.locals import *

class Player:
    def __init__(self, x, y):
        self.sprite = pg.image.load("projeto-ip/resources/assets/player.png")
        self.x = x
        self.y = y
        self.vel = 5  # velocidade do player

    def mover(self, keys):
        if keys[K_LEFT]:
            self.x -= self.vel
        if keys[K_RIGHT]:
            self.x += self.vel
        if keys[K_UP]:
            self.y -= self.vel
        if keys[K_DOWN]:
            self.y += self.vel

    def desenhar(self, surface):
        surface.blit(self.sprite, (self.x, self.y))
