import pygame as pg
import sys
import random
ANCHO = 800
ALTO = 600
FPS = 60

class Marcador():
    def __init__(self, x, y, fontsize=25, color=(255,255,255)):
        self.fuente = pg.font.SysFont("Arial", fontsize)
        self.x = x
        self.y = y
        self.color = color
    def dibuja(self, text, lienzo):
        image = self.fuente.render(str(text), True, self.color)
        lienzo.blit(image, (self.x, self.y))

class Bola(pg.sprite.Sprite):  # heredamos de la clase Sprite
    def __init__(self, x, y):
        # pg.sprite.Sprite.__init__(self)  # invocamos la función constructora de la clase heredada Sprite
        super().__init__()  # otra forma de hacer lo de la línea de arriba
        self.image = pg.image.load('./images/ball1.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))  # el get_rect() nos da el rectángulo 30x30 (tamaño imagen) que envuelve la imagen y lo centra en (x,y)

        # tanto image como rect actúan como dos instancias

        self.vx = random.randint(5, 10) * random.choice([-1, 1])
        self.vy = random.randint(5, 10) * random.choice([-1, 1])

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.vy *= -1

class Game():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.botes = 0
        self.cuentaGolpes = Marcador(10,10)

        self.ballGroup = pg.sprite.Group()  # creamos un grupo de bolas
        for i in range(random.randint(1, 10)):  # 10 bolas máximo
            bola = Bola(random.randint(0, ANCHO), random.randint(0, ALTO))
            self.ballGroup.add(bola)

        # self.bola = Bola(ANCHO//2, ALTO//2)  # el atributo bola de la clase Game es a su vez una instancia de la clase Bola 
                                               # (comentamos la línea xk ya definimos un grupo de bolas)

    def bucle_principal(self):
        game_over = False  # la variable game_over sólo se usará en este método por eso no le ponemos el self
        reloj = pg.time.Clock()
        while not game_over:
            reloj.tick(FPS)

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True

            # self.ball.update()
            self.ballGroup.update()

            self.pantalla.fill((0,0,0))
            self.cuentaGolpes.dibuja('Hola', self.pantalla)

            # self.pantalla.blit(self.bola.image, self.bola.rect.topleft)  # blit funciona con la esquina sup. izq.
            self.ballGroup.draw(self.pantalla)

            pg.display.flip()


if __name__ == '__main__':
    pg.init()
    game = Game()  # primero instanciamos
    game.bucle_principal()  # después llamamos al método




        







