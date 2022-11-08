from dagor import JuegoOrugas, JugadorOrugasInteractivo
from dagor import JugadorOrugasAleatorio

jugador1 = JugadorOrugasAleatorio('Cosa 1')
jugador2 = JugadorOrugasAleatorio('Cosa 2')
juego = JuegoOrugas(jugador1, jugador2, 10, 10)
juego.inicia(veces=100)
