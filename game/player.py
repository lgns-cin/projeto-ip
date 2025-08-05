import pygame as pg
from pygame.locals import *

class Player:
    def __init__(self, x, y):
        self.sprite = pg.image.load("resources/assets/player.png")
        self.x = x
        self.y = y
        self.vel = 5
        self.pulando = False
        self.destino_x = x
        self.vel_pulo = 30  # velocidade do pulo

    def iniciar_pulo(self, destino):
        if not self.pulando:
            self.pulando = True
            self.destino_x = destino

    def mover(self, keys):
        # Inicia o pulo se não estiver pulando
        if not self.pulando:
            if keys[K_LEFT] and self.x != 266:
                self.iniciar_pulo(266)
            elif keys[K_RIGHT] and self.x != 533:
                self.iniciar_pulo(533)
        # Executa o pulo animado
        if self.pulando:
            if self.x < self.destino_x:
                self.x += self.vel_pulo
                if self.x > self.destino_x:
                    self.x = self.destino_x
            elif self.x > self.destino_x:
                self.x -= self.vel_pulo
                if self.x < self.destino_x:
                    self.x = self.destino_x
            if self.x == self.destino_x:
                self.pulando = False

        if keys[K_UP]:
            self.y -= self.vel
        if keys[K_DOWN]:
            self.y += self.vel

    def desenhar(self, surface):
        surface.blit(self.sprite, (self.x, self.y))
