import pygame as pg  # para escribir menos después, lo importamos como pg
import sys

def fin_juego():
    pg.quit()
    sys.exit()

pg.init()
pantalla = pg.display.set_mode((600, 400))
pg.display.set_caption("Kata 02")

game_over = False

while not game_over:
    # gestión de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True

    # gestión del estado
    print("Hola mundo")

    # refrescar pantalla
    pantalla.fill((0, 255, 0))
    pg.display.flip()


fin_juego()



