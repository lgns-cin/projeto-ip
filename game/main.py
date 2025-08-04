import pygame as pg
from pygame.locals import *
from classes import gota

import random as rd

pg.init()

# Game window setup
win = pg.display.set_mode((800, 600))
map_sprite = pg.image.load("projeto-ip/sprites/map.png")
map_sprite = pg.transform.scale(map_sprite, (800, 600))

sair = False

nova_gota = False

while not sair:
    win.blit(map_sprite, (0, 0))

    pg.time.Clock().tick(60)

    escolher_gota = rd.randint(1, 3)
    
    if not nova_gota:
        gota_x, gota_y, gota_sprite = gota(escolher_gota).posicao_gota()
        nova_gota = True

    gota_y += 10

    win.blit(gota_sprite, (gota_x, gota_y))

    if gota_y >= 600:
        nova_gota = False

    pg.display.flip()
    win.fill((0))

    for event in pg.event.get():
        if event.type == QUIT:
            sair = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sair = True