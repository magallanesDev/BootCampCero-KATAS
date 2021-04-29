import pygame as pg
import sys
from random import randint, choice

ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
ANCHO = 800
ALTO = 600

pg.init()
pantalla = pg.display.set_mode((ANCHO, ALTO))
reloj = pg.time.Clock()


class Bola():
    def __init__(self, x, y, vx, vy, color, radio=10):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radio = radio

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.x < 0 or self.x > ANCHO:
            self.vx = -self.vx

        if self.y <= 0 or self.y >= ALTO:
            self.vy = -self.vy
    
    def dibujar(self, lienzo):
        pg.draw.circle(lienzo, self.color, (self.x, self.y), self.radio)
        
class Raqueta():
    def __init__(self, x=0, y=0):
        self.altura = 10
        self.anchura = 100
        self.color = (255, 255, 255)
        self.x = (ANCHO - self.anchura) // 2
        self.y = ALTO - self.altura

    def dibujar(self, lienzo):
        rect = pg.Rect(self.x, self.y, self.anchura, self.altura)
        pg.draw.rect(lienzo, self.color, rect)


raqueta = Raqueta()

bola = Bola(randint(0, ANCHO),
            randint(0, ALTO),
            choice([randint(-10,-5), randint(5, 10)]),
            choice([randint(-10,-5), randint(5, 10)]),
            (randint(0,255), randint(0,255), randint(0,255)))
    

game_over = False
while not game_over:
    reloj.tick(50)
    # gestión de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True

    # modificación de estado
    bola.actualizar()
        
    # gestión de la pantalla
    pantalla.fill(NEGRO)
    bola.dibujar(pantalla)
    raqueta.dibujar(pantalla)
        
    # refrescamos pantalla
    pg.display.flip()

pg.quit()
sys.exit()
