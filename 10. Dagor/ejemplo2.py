from dagor import JuegoD10, JugadorD10, JugadorD10Aleatorio
from dagor import JugadorD10Estrategico


class JugadorD10SiempreTiraUno(JugadorD10):

    def heuristica(self, posicion):
        return self.triunfo(posicion) == self.simbolo

    def tira(self, posicion):
        posibles = self.posiciones_siguientes(posicion)
        for p in posibles:
            if self.heuristica(p):
                return p
        return posibles[0]


jugador1 = JugadorD10SiempreTiraUno('OnlyOne')
jugador2 = JugadorD10Estrategico('Smart')
juego = JuegoD10(jugador1, jugador2)
juego.inicia(veces=100)
