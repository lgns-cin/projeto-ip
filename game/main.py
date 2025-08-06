import random

from classes import *
from player import Player
from constants import *

from pygame import *
from pygame.sprite import Group


class Game:
    """
    Classe que representa o jogo, responsável por iniciá-lo e coordenar seus estados.
    """

    def __init__(self):
        display.set_caption(WINDOW_TITLE)
        display.set_icon(WINDOW_ICON)

        self.screen = display.set_mode(WINDOW_SIZE)
        self.fullscreen = False

        self.clock = time.Clock()

        self.player = Player()

        self.background = Group()
        self.collectibles = Group()
        self.obstacles = Group()

    def toggle_fullscreen(self):
        if self.fullscreen:
            # Mudando pro tamanho original
            self.screen = display.set_mode(WINDOW_SIZE)
        else:
            # Mudando a resolução da tela antes de mudar para tela cheia
            display_size = display.get_desktop_sizes().pop()
            self.screen = display.set_mode(display_size)

            display.toggle_fullscreen()

        self.fullscreen = not self.fullscreen

    def start(self):
        rodando = True

        while rodando:
            # Atualizar relógio
            self.clock.tick(FPS)

            # Analisar eventos
            for evento in event.get():
                match evento.type:
                    case constants.QUIT:
                        rodando = False

                    case constants.KEYDOWN:
                        rodando = evento.key != K_ESCAPE

                        if evento.key == K_F11:
                            self.toggle_fullscreen()

            # Lógica de spawn de itens e etc. (aqui está só um teste)
            if len(self.obstacles) == 0:
                scale = 0.5 + random.random()                          # 0.5-1.5
                pos_x = random.randint(LEFT_WALL, RIGHT_WALL) # 270-540
                accel = 0.25 + random.random()                          # 0.25-1.25

                new_obstacle = Obstacle(OBSTACLE_SPRITE, scale, pos_x, accel)
                self.obstacles.add(new_obstacle)

            # Atualizar estados
            keys = key.get_pressed()
            ...
            self.obstacles.update()
            self.player.update(keys=keys)

            # Renderizar: fundo -> coletáveis -> jogador -> obstáculos -> parede?
            self.screen.fill("black")
            self.screen.blit(self.player.image, self.player.rect)

            self.obstacles.draw(self.screen)

            self.screen.blit(MAP_SPRITE, (0, 0)) # Teste
            ...

            # Atualizar display
            display.flip()


if __name__ == "__main__":
    pygame.init()
    Game().start()