from arkanoid import ANCHO, ALTO, FPS, levels
from arkanoid.entities import Marcador, Bola, Raqueta, Ladrillo
import pygame as pg


class Scene():
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.todoGrupo = pg.sprite.Group()
        self.reloj = pg.time.Clock()

    def maneja_eventos(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                return True
        return False

    def reset(self):
        pass

    def bucle_principal(self):
        pass


    
class Game(Scene):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.vidas = 30
        self.puntuacion = 0
        self.grupoJugador = pg.sprite.Group()
        self.grupoLadrillos = pg.sprite.Group()
        
        self.level = 0
        self.disponer_ladrillos(levels[self.level])

        self.cuentaPuntos = Marcador(10,10)
        self.cuentaVidas = Marcador(790, 10, "D")
        self.cuentaVidas.plantilla = "Vidas: {}"
        self.cuentaVidas.text = self.vidas
        
        
        self.fondo = pg.image.load("./images/background.png")

        self.bola = Bola(ANCHO//2, ALTO//2)
        self.todoGrupo.add(self.bola)

        self.raqueta = Raqueta(x = ANCHO//2, y = ALTO - 40)
        self.grupoJugador.add(self.raqueta)
        
        self.todoGrupo.add(self.grupoJugador, self.grupoLadrillos)
        self.todoGrupo.add(self.cuentaPuntos, self.cuentaVidas)

    def disponer_ladrillos(self, level):
        for fila, cadena in enumerate(level): 
            for columna, caracter in enumerate(cadena):
                if caracter in 'XD':  # buscamos si el caracter es X o D (si el caracter está en la cadena 'XD')
                    x = 5 + (100 * columna)
                    y = 5 + (40 * fila)
                    ladrillo = Ladrillo(x, y, caracter == 'D')
                    self.grupoLadrillos.add(ladrillo)
    
    def bucle_principal(self):
        game_over = False  # la variable game_over sólo se usará en este método por eso no le ponemos el self
        reloj = pg.time.Clock()

        while not game_over and self.vidas > 0:
            dt = reloj.tick(FPS)

            if self.maneja_eventos():
                break
           
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True
            
            self.cuentaPuntos.text = self.puntuacion
            self.cuentaVidas.text = self.vidas
            self.bola.prueba_colision(self.grupoJugador)
            tocados = self.bola.prueba_colision(self.grupoLadrillos)
            for ladrillo in tocados:
                self.puntuacion += 5
                if ladrillo.desaparece():
                    self.grupoLadrillos.remove(ladrillo)
                    self.todoGrupo.remove(ladrillo)
                    if len(self.grupoLadrillos) == 0:
                        self.level += 1
                        self.disponer_ladrillos(levels[self.level])
                        self.todoGrupo.add(self.grupoLadrillos)

            self.todoGrupo.update(dt)
            if self.bola.estado == Bola.Estado.muerta:
                self.vidas -= 1

            self.pantalla.blit(self.fondo, (0,0))
            self.todoGrupo.draw(self.pantalla)

            pg.display.flip()
        
        # if not game_over:
            ################


class Portada():
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.instrucciones = Marcador(ANCHO//2, ALTO//2, 'center', 50, (255, 255, 0))
        self.instrucciones.text = "PULSA ESPACIO PARA JUGAR"
        self.todoGrupo = pg.sprite.Group()
        self.todoGrupo.add(self.instrucciones)
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True

            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_SPACE]:
                game_over = True

            self.todoGrupo.update(dt)
            self.pantalla.fill((0, 0, 0))
            self.todoGrupo.draw(self.pantalla)

            pg.display.flip()