import pygame as pg
import sys
from random import randint

def rebotaX(x):
    if x <= 0 or x >= ANCHO:
        return -1  # cambiamos el signo
    else:
        return 1

def rebotaY(y):
    if y <= 0 or y >= ALTO:
        return -1
    
    return 1  # nos podemos ahorrar el ELSE


ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
ANCHO = 800
ALTO = 600

pg.init()
pantalla = pg.display.set_mode((ANCHO, ALTO))
reloj = pg.time.Clock()

# Bola 1
x = ANCHO//2 # para que no tenga decimales
y = ALTO//2
vx = -8
vy = -8

# Bola 2
x2 = randint(0, ANCHO)
y2 = randint(0, ALTO)
vx2 = randint(5, 15)
vy2 = randint(5, 15)


game_over = False
while not game_over:
    reloj.tick(60)  # por si queremos reducir la velocidad de la pelota
    # gestión de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True

    # gestión de la pantalla
    pantalla.fill(NEGRO)
    pg.draw.circle(pantalla, ROJO, (x, y), 10)
    pg.draw.circle(pantalla, VERDE, (x2, y2), 10)

    x += vx
    y += vy
    x2 += vx2
    y2 += vy2

    vy *= rebotaY(y)
    vx *= rebotaX(x)
    vy2 *= rebotaY(y2)
    vx2 *= rebotaX(x2)

    # refrescamos pantalla
    pg.display.flip()

pg.quit()
sys.exit()
