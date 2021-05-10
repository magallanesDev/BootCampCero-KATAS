from arkanoid import ANCHO, ALTO, FPS
import pygame as pg
import random
from enum import Enum


class Marcador(pg.sprite.Sprite):
    plantilla = "{}"

    class Justificado():
        izquierda = "I"
        derecha = "D"
        centrado = "C"

    def __init__(self, x, y, justificado=None, fontsize=50, color=(255,255,255)):
        super().__init__()
        self.fuente = pg.font.Font(None, fontsize)
        self.text = ""
        self.color = color
        self.x = x
        self.y = y
        if not justificado:
            self.justificado = Marcador.Justificado.izquierda
        else:
            self.justificado = justificado
        
        self.image = None  # se podrían quitar estas dos líneas. Los informamos abajo en el método update
        self.rect = None

    
    def update(self, dt):
        self.image = self.fuente.render(self.plantilla.format(self.text), True, self.color)
        if self.justificado == Marcador.Justificado.izquierda:
            self.rect = self.image.get_rect(topleft=(self.x,self.y))       
        elif self.justificado == Marcador.Justificado.derecha:
            self.rect = self.image.get_rect(topright=(self.x,self.y))
        else:
            self.rect = self.image.get_rect(midtop=(self.x,self.y))


class Ladrillo(pg.sprite.Sprite):
    disfraces = ["greenTile.png", "redTile.png", "redTileBreak.png"]

    def __init__(self, x, y, esDuro=False):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.esDuro = esDuro
        self.imagen_actual = 1 if esDuro else 0  # otra forma de poner el if (operador ternario)
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.numGolpes = 0
        

    def cargaImagenes(self):
        imagenes = []  # variable local, sólo de este método. Es una lista vacia
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./images/{}".format(fichero)))
        return imagenes

    def update(self, dt):
        if self.esDuro and self.numGolpes == 1:
            self.imagen_actual = 2
            self.image = self.imagenes[self.imagen_actual]
            
    def desaparece(self):
        self.numGolpes += 1
        return (self.numGolpes > 0 and not self.esDuro) or (self.numGolpes > 1 and self.esDuro)
        # si es True es que desaparece
        
         
class Raqueta(pg.sprite.Sprite):
    disfraces = ['electric00.png', 'electric01.png', 'electric02.png']
    def __init__(self, x, y):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0  # imagen en primera posición en la lista
        self.milisegundos_para_cambiar = 1000 // FPS * 5  # para que cambie cada 5 fotogramas
        self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(centerx = x, bottom = y)
        self.vx = 7
    
    def cargaImagenes(self):
        imagenes = []  # variable local, sólo de este método. Es una lista vacia
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./images/{}".format(fichero)))
        return imagenes
    
    def update(self, dt):
            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_LEFT]:
                self.rect.x -= self.vx
            if teclas_pulsadas[pg.K_RIGHT]:
                self.rect.x += self.vx
            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right >= ANCHO:
                self.rect.right = ANCHO

            self.milisegundos_acumulados += dt
            if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
                self.imagen_actual += 1  # pasamos a la siguiente imagen
                if self.imagen_actual >= len(self.disfraces):
                    self.imagen_actual = 0  # volvemos a la primera imagen
                self.milisegundos_acumulados = 0
            self.image = self.imagenes[self.imagen_actual]


class Bola(pg.sprite.Sprite):  # heredamos de la clase Sprite

    disfraces = ['ball1.png', 'ball2.png', 'ball3.png', 'ball4.png', 'ball5.png']
    
    class Estado(Enum):  # ponemos la clase Estado dentro de la clase Bola por ordenarlo mejor. 
                         # funcionaría igual sin el Enum, lo hace para que conozcamos la librería
        viva = 0
        agonizando = 1
        muerta = 2
    
    def __init__(self, x, y):
        # pg.sprite.Sprite.__init__(self)  # invocamos la función constructora de la clase heredada Sprite
        super().__init__()  # otra forma de hacer lo de la línea de arriba
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.image = self.imagenes[self.imagen_actual]
        self.milisegundos_acumulados = 0
        self.milisegundos_para_cambiar = 1000 // FPS * 10
        self.rect = self.image.get_rect(center=(x,y))  # el get_rect() nos da el rectángulo 30x30 (tamaño imagen) que envuelve la imagen y lo centra en (x,y)
        # tanto image como rect actúan como dos instancias
        self.xOriginal = x
        self.yOriginal = y
        self.estoyViva = True
        self.estado = Bola.Estado.viva

        self.vx = random.randint(5, 10) * random.choice([-1, 1])
        self.vy = random.randint(5, 10) * random.choice([-1, 1])

    def cargaImagenes(self):
        imagenes = []  # variable local, sólo de este método. Es una lista vacia
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./images/{}".format(fichero)))
        return imagenes

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False)  # método que comprueba colisiones y devuelve una lista con los objetos golpeados
        if len(candidatos) > 0:
            self.vy *= -1
        return candidatos

    def update(self, dt):
        if self.estado == Bola.Estado.viva:
            self.rect.x += self.vx
            self.rect.y += self.vy
            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1
            if self.rect.top <= 0:
                self.vy *= -1
            if self.rect.bottom >= ALTO:
                self.estado = Bola.Estado.agonizando
                self.rect.bottom = ALTO

        elif self.estado == Bola.Estado.agonizando:
            self.milisegundos_acumulados += dt
            if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
                self.imagen_actual += 1
                self.milisegundos_acumulados = 0
                if self.imagen_actual >= len(self.disfraces):
                    self.estado = Bola.Estado.muerta
                    self.imagen_actual = 0
                self.image = self.imagenes[self.imagen_actual]

        else:
            self.rect.center = (self.xOriginal, self.yOriginal)
            self.vx = random.randint(5, 10) * random.choice([-1, 1])
            self.vy = random.randint(5, 10) * random.choice([-1, 1])
            self.estado = Bola.Estado.viva
     