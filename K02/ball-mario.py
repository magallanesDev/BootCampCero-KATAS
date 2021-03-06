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

fuente1 = pg.font.Font(None, 30)
fuente2 = pg.font.Font(None, 60)


class Bola():
    def __init__(self, x, y, vx, vy, color, radio=10, contadorColision=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.anchura = radio*2
        self.altura = radio*2
        self.contadorColision = contadorColision

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.x < 0 or self.x > ANCHO:
            self.vx = -self.vx

        if self.y <= 0 or self.y >= ALTO:
            self.vy = -self.vy

        if self.y >= ALTO:  # hemos perdido y colocaremos la bola en el centro
            self.x = ANCHO // 2
            self.y = ALTO // 2
            self.vx = randint(5,10)*choice([-1,1])
            self.vy = randint(5,10)*choice([-1,1])
            return True
        return False


    def dibujar(self, lienzo):
        pg.draw.circle(lienzo, self.color, (self.x, self.y), self.anchura//2)

    def comprueba_colision(self, objeto):
        choqueX = self.x >= objeto.x and self.x <= objeto.x+objeto.anchura or \
            self.x+self.anchura >= objeto.x and self.x+self.anchura <= objeto.x + objeto.anchura
        choqueY = self.y >= objeto.y and self.y <= objeto.y+objeto.anchura or \
            self.y+self.anchura >= objeto.y and self.y+self.anchura <= objeto.y + objeto.anchura

        if choqueX and choqueY:  # para que haya colisión los dos choques tienen que ser True
            self.vy *= -1
            self.contadorColision += 5           
        

class Raqueta():
    def __init__(self, x=0, y=0):
        self.altura = 10
        self.anchura = 100
        self.color = (255, 255, 255)
        self.x = (ANCHO - self.anchura) // 2
        self.y = ALTO - self.altura - 15
        self.vx = 10
        self.vy = 0

    def dibujar(self, lienzo):
        rect = pg.Rect(self.x, self.y, self.anchura, self.altura)
        pg.draw.rect(lienzo, self.color, rect)

    def actualizar(self):
        teclas_pulsadas = pg.key.get_pressed()  # nos informa de las teclas que están pulsadas
        if teclas_pulsadas[pg.K_LEFT] and self.x > 0:
            raqueta.x -= raqueta.vx
        if teclas_pulsadas[pg.K_RIGHT] and self.x < ANCHO-self.anchura:
            raqueta.x += raqueta.vx



vidas = 3  # vidas al empezar el juego

raqueta = Raqueta()

bola = Bola(randint(0, ANCHO),
            randint(0, ALTO),
            choice([randint(-10,-5), randint(5, 10)]),
            choice([randint(-10,-5), randint(5, 10)]),
            (randint(0,255), randint(0,255), randint(0,255)))

   

game_over = False
while not game_over and vidas > 0:
    reloj.tick(50)
    # gestión de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True

    # modificación de estado
    raqueta.actualizar()
    pierdebola = bola.actualizar()
    if pierdebola:
        vidas -= 1
    strVidas = str(vidas)
    
    bola.comprueba_colision(raqueta)
    strPuntos = str(bola.contadorColision)

    texto1 = fuente1.render("Vidas:  {}".format(strVidas), True, (255, 255, 255))
    texto2 = fuente1.render("Puntos:  {}".format(strPuntos), True, (255, 255, 255))
      
    # gestión de la pantalla
    pantalla.fill(NEGRO)
    if vidas>0:
        bola.dibujar(pantalla)
        raqueta.dibujar(pantalla)
    pantalla.blit(texto1, (30,10))
    pantalla.blit(texto2, (650,10))


    # refrescamos pantalla
    pg.display.flip()
    if pierdebola:
        pg.time.delay(500)


pg.time.delay(3000)  # nos permite ver la puntuación obtenida    

pantalla.fill(NEGRO)
texto3 = fuente2.render("GAME OVER", True, (255, 255, 255))
pantalla.blit(texto3, (ANCHO//2 - texto3.get_width()//2, ALTO//2 - texto3.get_height()//2))
pg.display.flip()
pg.time.delay(3000)  # para que no desaparezca el GAME OVER inmediatamente

pg.quit()
sys.exit()
