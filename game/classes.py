import random as rd
import pygame as pg

gota_sprite = pg.image.load("projeto-ip/sprites/gota.png")

class Gota:
    def __init__(self, tamanho):
        self.sprite = pg.transform.scale(gota_sprite, (tamanho, tamanho))
        self.tamanho = self.sprite.get_width()
            
    def posicao_gota(self, lado):
        if lado == 2:
            gota_x = 520
        else:
            gota_x = 240
        
        gota_y = 0

        return (gota_x, gota_y, self.sprite)
    
class Coletavel:
    SPRITES = [
        pg.image.load("projeto-ip/sprites/saia de filó.png"),
        pg.image.load("projeto-ip/sprites/vida.png"),
        pg.image.load("projeto-ip/sprites/agulha.png")
    ]

    def __init__(self, tipo, x, y):
        self.tipo = tipo
        self.sprite = Coletavel.SPRITES[tipo]
        self.x = x
        self.y = y

    def desenhar(self, surface):
        surface.blit(self.sprite, (self.x, self.y))
        
        

        