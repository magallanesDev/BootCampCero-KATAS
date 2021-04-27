import pygame as pg
import sys

ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
ANCHO = 800
ALTO = 600

pg.init()
pantalla = pg.display.set_mode((ANCHO, ALTO))

game_over = False
x = ANCHO//2 # para que no tenga decimales
y = ALTO//2
vx = -8
vy = -8
reloj = pg.time.Clock()

while not game_over:
    reloj.tick(60)  # por si queremos reducir la velocidad de la pelota
    # gestión de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True

    # gestión de la pantalla
    pantalla.fill(NEGRO)
    pg.draw.circle(pantalla, ROJO, (x, y), 10)
    x += vx
    y += vy

    if y <= 0 or y>= ALTO:
        vy = -vy
    
    if x <= 0 or x>= ANCHO:
        vx = -vx

    # refrescamos pantalla
    pg.display.flip()

pg.quit()
sys.exit()
