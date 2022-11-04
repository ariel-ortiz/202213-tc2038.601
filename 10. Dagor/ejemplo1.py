from dagor import JuegoD10, JugadorD10Interactivo, JugadorD10Estrategico
from dagor import JugadorD10Aleatorio

jugador1 = JugadorD10Estrategico('Cosa 1')
jugador2 = JugadorD10Estrategico('Cosa 2')
juego = JuegoD10(jugador1, jugador2)
juego.inicia(veces=1000)
