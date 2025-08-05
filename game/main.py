import pygame as pg
from pygame.locals import *
from classes import Gota
from classes import Coletavel
import functions as fn
import random as rd
from player import Player

pg.init()

# Game window setup
win = pg.display.set_mode((800, 600))
map_sprite = pg.image.load("resources/assets/map_p2.png")
map_sprite = pg.transform.scale(map_sprite, (800, 600))
player = Player(266, 500)

sair = False
nova_gota = False
nova_gota2 = False
coletaveis = False
gota_caindo = False

coletaveis_lista = []
lista_y = []

printou = False

while not sair:
    win.blit(map_sprite, (0, 0))

    keys = pg.key.get_pressed()
    player.mover(keys)
    player.desenhar(win)

    if not coletaveis:
        for i in range(4):
            coletaveis_lista.append([])
            sorteio_x = rd.randint(1, 2)

            if sorteio_x == 1:
                x_arbitrario = 266
            else:
                x_arbitrario = 533

            if not lista_y:
                lista_y = fn.gerar_y_coletaveis()
                        
            coletaveis_lista[i].append(i)
            coletaveis_lista[i].append(x_arbitrario)
            coletaveis_lista[i].append(lista_y[i])
        
    coletaveis = True

    for i in range(4):
        Coletavel(coletaveis_lista[i][0], coletaveis_lista[i][1], coletaveis_lista[i][2]).desenhar(win)

    pg.time.Clock().tick(30)

    # Randomly generate a new Gota if not already present
    tamanho_gota = rd.randint(50, 100)
    
    if not nova_gota:
        gota_x, gota_y, gota_sprite = Gota(tamanho_gota).posicao_gota(rd.randint(1, 2))
        nova_gota = True

    win.blit(gota_sprite, (gota_x, gota_y))

    gota_y += 10

    if nova_gota2 and not gota_caindo:
        gota_x2, gota_y2, gota_sprite2 = Gota(tamanho_gota).posicao_gota(rd.randint(1, 2))
        gota_caindo = True

    if nova_gota2:
        win.blit(gota_sprite2, (gota_x2, gota_y2))

        gota_y2 += 10
        
        if gota_y2 >= 600:
            nova_gota2 = False
            gota_caindo = False

    if (gota_y >= 300) and (not nova_gota2):
        nova_gota2 = True

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
            elif event.key == K_F11:  # Pressione F11 para alternar tela cheia
                if win.get_flags() & FULLSCREEN:
                    win = pg.display.set_mode((800, 600))
                else:
                    win = pg.display.set_mode((800, 600), FULLSCREEN)