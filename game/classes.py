import random as rd
import pygame as pg

gotap_sprite = pg.image.load("projeto-ip/sprites/gota p.png")
gotam_sprite = pg.image.load("projeto-ip/sprites/gota m.png")
gotag_sprite = pg.image.load("projeto-ip/sprites/gota g.png")

class gota:
    def __init__(self, tipo):
        if tipo == 1:
            self.tipo = 'gotap'
        elif tipo == 2:
            self.tipo = 'gotam'
        else:
            self.tipo = 'gotag'
        
    def posicao_gota(self):
        if self.tipo == 'gotap':
            sprite_height = gotap_sprite.get_height()
            return (rd.randint(0, 800 - sprite_height), 0, gotap_sprite)
        elif self.tipo == 'gotam':
            sprite_height = gotam_sprite.get_height()
            return (rd.randint(0, 800 - sprite_height), 0, gotam_sprite)
        else:
            sprite_height = gotag_sprite.get_height()
            return (rd.randint(0, 800 - sprite_height), 0, gotag_sprite)

        