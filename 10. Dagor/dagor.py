# ============================================================================
#   Dagor: Framework para juegos de estrategia.
#   Inspirado en el proyecto Gamesman elaborado por Dan Garcia de
#   UC Berkeley.
#   https://people.eecs.berkeley.edu/~ddgarcia/teaching/CS3Gamesman/
#   Copyright © 2016 Ariel Ortiz Ramírez, Tecnologico de Monterrey, CEM.
#
#   Este programa es software libre. Puede redistribuirlo y/o modificarlo
#   bajo los términos de la Licencia Pública General de GNU tal como está
#   publicada por la Free Software Foundation, bien de la versión 3 de dicha
#   Licencia o bien (según su elección) de cualquier versión posterior.
#
#   Este programa se distribuye con la esperanza de que sea útil, pero
#   SIN NINGUNA GARANTÍA, incluso sin la garantía MERCANTIL implícita o
#   sin garantizar la CONVENIENCIA PARA UN PROPÓSITO PARTICULAR. Véase
#   la Licencia Pública General de GNU para más detalles.
#
#   Usted debería haber recibido una copia de la Licencia Pública General
#   junto con este programa. Si no ha sido así, consulte
#   <http://www.gnu.org/licenses>.
# ============================================================================

from abc import ABCMeta, abstractmethod
import datetime
import platform
from random import choice, randint
import sys
import time
import traceback


DAGOR_VERSION = (1, 0, 3)


# ---------------------------------------------------------
class TiroInvalido(Exception):
    '''Excepción para indicar que un jugador intentó realizar un tiro
    no permitido dada la posición actual.'''
    pass


# ---------------------------------------------------------
class TiemploLimiteExcedido(Exception):
    '''Excepción para indicar que el tiro de un jugador excedió el
    tiempo estipulado.'''
    pass


# ---------------------------------------------------------
class Juego:
    '''Clase abstracta de la que deben heredar todos las clases que
    representan juegos.'''

    __metaclass__ = ABCMeta

    @abstractmethod
    def posicion_inicial(self): pass

    @abstractmethod
    def imprime_posicion(self): pass

    @abstractmethod
    def posiciones_siguientes(self, posicion): pass

    @abstractmethod
    def juego_terminado(self, posicion): pass

    @abstractmethod
    def triunfo(self, jugador, posicion): pass

    @abstractmethod
    def pre_tiro(self): pass

    @abstractmethod
    def post_tiro(self): pass

    @abstractmethod
    def imprime_resultado(self): pass

    @staticmethod
    def encabezado_aplicacion():
        print('Dagor: Framework para juegos de estrategia, '
              f'versión {".".join([str(x) for x in DAGOR_VERSION])}\n'
              'Licencia GPLv3. © 2016, 2022 por Ariel Ortiz, '
              'Tecnológico de Monterrey, Estado de México.\n')

    @staticmethod
    def valida_tipo_argumento(jugador, tipo_jugador):
        if not isinstance(jugador, tipo_jugador):
            mensaje = ('Argumento {!r} es de tipo {}, debería ser de tipo {}.'
                       .format(jugador, jugador.__class__.__name__,
                               tipo_jugador.__name__))
            raise TypeError(mensaje)

    def __init__(self, jugador1, jugador2):
        '''Crea e inicializa un nuevo juego con dos jugadores.'''
        jugador1._contrario = jugador2
        jugador1._juego = self
        jugador2._contrario = jugador1
        jugador2._juego = self
        self._jugador1 = jugador1
        self._jugador2 = jugador2
        self._jugador_actual = None

    def simbolo_contrario(self, simbolo):
        return (self._jugador2.simbolo
                if self._jugador1.simbolo == simbolo
                else self._jugador1.simbolo)

    def alterna_jugador(self):
        self._jugador_actual = (
            self._jugador1 if self._jugador_actual == self._jugador2
            else self._jugador2)

    def info_inicio_juego(self):
        mensaje = self.__class__.__name__
        print(mensaje)
        print('{}'.format(len(mensaje) * '='))
        print(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'))
        nodo = platform.node()
        if nodo:
            print('Computadora: {}'.format(nodo))
        print('Jugador 1: {}'.format(self._jugador1))
        print('Jugador 2: {}'.format(self._jugador2))
        print('')

    def resumen_de_encuentro(
            self,
            veces,
            juegos_ganados_jugador1,
            juegos_ganados_jugador2,
            juegos_empatados):

        if veces > 1:
            print('')
            print('RESUMEN DEL ENCUENTRO')
            print('----------------------------------'
                  '-----------------------------------')
            print('Juegos jugados: {}'.format(veces))
            print('Juegos ganados por {}: {}'.format(
                self._jugador1,
                juegos_ganados_jugador1))
            print('Juegos ganados por {}: {}'.format(
                self._jugador2,
                juegos_ganados_jugador2))
            print('Juegos empatados: {}'.format(juegos_empatados))
            print('-----------------------------------'
                  '----------------------------------')

    def descalifica(self):
        print('')
        print('***********************************'
              '**********************************')
        print('Jugador {}'.format(self._jugador_actual))
        print('Descalificado por producir un error.')
        traceback.print_exc(file=sys.stdout)
        print('')
        self.alterna_jugador()
        print('Jugador {}'.format(self._jugador_actual))
        print('Gana por default.')
        print('***********************************'
              '**********************************')

    def inicia(self, veces=1, delta_max=0):
        '''Inicia un encuentro entre los dos jugadores provistos al momento
        en el que se creó el juego. El encuentro tendrá un cierto número
        de juegos determinado por el valor del parámetro veces. Cada jugador
        tira primero de manera alternada en todos los juegos del encuentro.
        Si delta_max tiene un valor mayor a cero arroja la excepción de
        TiemploLimiteExcedido si el tiempo que tarda el tiro de algún
        jugador excede delta_max segundos. Al final despliega un resumen
        del encuentro si veces es mayor a 1.'''

        juegos_ganados_jugador1 = 0
        juegos_ganados_jugador2 = 0
        juegos_empatados = 0

        self.encabezado_aplicacion()
        self.info_inicio_juego()

        try:
            for i in range(veces):

                if veces > 1:
                    print('-------------------- JUEGO #{} --------------------'
                          .format(i + 1))

                self._jugador_actual = (
                    self._jugador1 if i % 2 == 0
                    else self._jugador2)
                self._posicion = self.posicion_inicial()
                self.imprime_posicion()
                self._num_tiro = 0

                while True:
                    self._num_tiro += 1
                    self.pre_tiro()
                    posibles = self.posiciones_siguientes(self._posicion)
                    tiempo_inicio = time.time()
                    tiro = self._jugador_actual.tira(self._posicion)
                    tiempo_fin = time.time()
                    delta = tiempo_fin - tiempo_inicio
                    if delta_max and delta > delta_max:
                        mensaje = (f'Permitido: {delta_max} s, '
                                   f'utilizado: {delta:.2f} s.')
                        raise TiemploLimiteExcedido(mensaje)

                    if tiro not in posibles:
                        raise TiroInvalido(tiro)
                    self._posicion = tiro
                    self.post_tiro()
                    self.imprime_posicion()
                    if self.juego_terminado(self._posicion):
                        break
                    self.alterna_jugador()

                self.imprime_resultado()

                if (not self.triunfo(self._jugador1, self._posicion)
                        and not self.triunfo(self._jugador2, self._posicion)):
                    juegos_empatados += 1
                elif self.triunfo(self._jugador1, self._posicion):
                    juegos_ganados_jugador1 += 1
                else:
                    juegos_ganados_jugador2 += 1

            self.resumen_de_encuentro(
                veces,
                juegos_ganados_jugador1,
                juegos_ganados_jugador2,
                juegos_empatados)

            return ('normal',
                    juegos_ganados_jugador1,
                    juegos_ganados_jugador2,
                    juegos_empatados)

        except BaseException:
            self.descalifica()
            return ('default',
                    1 if self._jugador_actual == self._jugador1 else 0,
                    1 if self._jugador_actual == self._jugador2 else 0,
                    0)

# ----------------------------------------------------------


class JuegoD10(Juego):
    '''Clase que representa un juego de D10 (Destino 10).'''

    def __init__(self, jugador1, jugador2):
        '''Crea e inicializa un nuevo juego de D10 con dos jugadores.'''
        self.valida_tipo_argumento(jugador1, JugadorD10)
        self.valida_tipo_argumento(jugador2, JugadorD10)
        super(JuegoD10, self).__init__(jugador1, jugador2)

    def posicion_inicial(self):
        return (self._jugador_actual.nombre, 0)

    def imprime_posicion(self):
        suma = self._posicion[1]
        print(' _' * 10)
        print('| ' * 10 + '|')
        print('|*' * suma + '| ' * (10 - suma) + '|')
        print('|_' * 10 + '|')
        print('Total {}'.format(suma))
        print('')

    def posiciones_siguientes(self, posicion):
        turno = self.simbolo_contrario(posicion[0])
        suma = posicion[1]
        resultado = []
        if (suma <= 9):
            resultado.append((turno, suma + 1))
        if (suma <= 8):
            resultado.append((turno, suma + 2))
        return tuple(resultado)

    def juego_terminado(self, posicion):
        return (self.triunfo(self._jugador1, posicion)
                or self.triunfo(self._jugador2, posicion))

    def triunfo(self, jugador, posicion):
        return (posicion[1] == 10
                and jugador.simbolo == self.simbolo_contrario(posicion[0]))

    def pre_tiro(self):
        self._suma_actual = self._posicion[1]

    def post_tiro(self):
        print('')
        print('[{}] Jugador {} tira {}'.format(
            self._num_tiro,
            self._jugador_actual.nombre,
            self._posicion[1] - self._suma_actual))

    def imprime_resultado(self):
        print('>>>>>> GANADOR: {} <<<<<<<'.format(self._jugador_actual))
        print('')

# ----------------------------------------------------------


def dibuja_tablero(t):
    rens = len(t)
    cols = len(t[0])
    print('')
    print('  {}'.format(' '.join([' {} '.format(r) for r in range(cols)])))
    for r, row in enumerate(t):
        print('{} {}'.format(r, '|'.join(
            [' {} '.format(c)
             for c in row])))
        if r < len(t) - 1:
            print('  ' + '+'.join(
                ['-' * 3 for c in row]))
    print('')

# ----------------------------------------------------------


class JuegoSuperGato(Juego):
    '''Clase que representa un juego de SuperGato.'''

    @property
    def renglones(self):
        return self._renglones

    @property
    def columnas(self):
        return self._columnas

    def __init__(self, jugador1, jugador2, renglones, columnas):
        '''Crea e inicializa un nuevo juego de SuperGato con dos jugadores y
        un tablero del tamaño indicado por renglones y columnas.'''
        self.valida_tipo_argumento(jugador1, JugadorSuperGato)
        self.valida_tipo_argumento(jugador2, JugadorSuperGato)
        self.valida_tipo_argumento(renglones, int)
        self.valida_tipo_argumento(columnas, int)

        jugador1._simbolo = 'X'
        jugador2._simbolo = 'O'
        super(JuegoSuperGato, self).__init__(jugador1, jugador2)

        if not (3 <= renglones <= 10 and 3 <= columnas <= 10):
            mensaje = (
                'Número de renglones y/o columnas fuera de rango: ({}, {})'
                .format(renglones, columnas))
            raise ValueError(mensaje)

        self._renglones = renglones
        self._columnas = columnas

    def posicion_inicial(self):
        return (self._jugador_actual.simbolo,
                ((' ',) * self._columnas,) * self._renglones)

    def imprime_posicion(self):
        dibuja_tablero(self._posicion[1])

    def posiciones_siguientes(self, posicion):
        turno_actual = posicion[0]
        turno_siguiente = self.simbolo_contrario(turno_actual)
        tablero = posicion[1]
        resultado = []
        for r in range(self._renglones):
            for c in range(self._columnas):
                if tablero[r][c] == ' ':
                    a = [list(ren) for ren in tablero]
                    a[r][c] = turno_actual
                    a = tuple([tuple(ren) for ren in a])
                    resultado.append((turno_siguiente, a))
        return tuple(resultado)

    def juego_terminado(self, posicion):

        def empate():
            for r in self._posicion[1]:
                for c in r:
                    if c == ' ':
                        return False
            return True

        return (self.triunfo(self._jugador1, posicion)
                or self.triunfo(self._jugador2, posicion)
                or empate())

    def triunfo(self, jugador, posicion):
        t = posicion[1]
        s = jugador.simbolo
        for r in range(self._renglones):
            for c in range(self._columnas):
                if ((r + 2 < self._renglones
                     and s == t[r][c] == t[r + 1][c] == t[r + 2][c])
                    or
                    (c + 2 < self._columnas
                     and s == t[r][c] == t[r][c + 1] == t[r][c + 2])):
                    return True
        return False

    def pre_tiro(self):
        self._tablero_previo = self._posicion[1]

    def post_tiro(self):

        def tiro():
            tp = self._tablero_previo
            tn = self._posicion[1]
            for r in range(self._renglones):
                for c in range(self._columnas):
                    if tp[r][c] != tn[r][c]:
                        return '{}{}'.format(r, c)

        print('[{}] Jugador {} tira {}'.format(
            self._num_tiro,
            self._jugador_actual.simbolo,
            tiro()))

    def imprime_resultado(self):
        ganador = (self._jugador1
                   if self.triunfo(self._jugador1, self._posicion)
                   else (self._jugador2
                         if self.triunfo(self._jugador2, self._posicion)
                         else None))
        if ganador:
            print('>>>>>> GANADOR: {} <<<<<<<'.format(ganador))
        else:
            print('>>>>>> EMPATE <<<<<<<')
        print('')

# ----------------------------------------------------------


class JuegoOrugas(Juego):
    '''Clase que representa un juego de Orugas.'''

    @property
    def renglones(self):
        return self._renglones

    @property
    def columnas(self):
        return self._columnas

    def __init__(self, jugador1, jugador2, renglones, columnas):
        '''Crea e inicializa un nuevo juego de Orugas con dos jugadores y
        un tablero del tamaño indicado por renglones y columnas.'''
        self.valida_tipo_argumento(jugador1, JugadorOrugas)
        self.valida_tipo_argumento(jugador2, JugadorOrugas)
        self.valida_tipo_argumento(renglones, int)
        self.valida_tipo_argumento(columnas, int)

        jugador1._simbolo = 'B'
        jugador2._simbolo = 'N'
        super(JuegoOrugas, self).__init__(jugador1, jugador2)

        if not (4 <= renglones <= 10 and 4 <= columnas <= 10):
            mensaje = (
                'Número de renglones y/o columnas fuera de rango: ({}, {})'
                .format(renglones, columnas))
            raise ValueError(mensaje)

        self._renglones = renglones
        self._columnas = columnas

    def posicion_inicial(self):

        def coloca_al_azar(simbolo):
            while True:
                r = randint(0, self._renglones - 1)
                c = randint(0, self._columnas - 1)
                if a[r][c] == ' ':
                    a[r][c] = simbolo
                    return

        a = [[' ' for _c in range(self._columnas)]
             for _r in range(self._renglones)]
        coloca_al_azar(self._jugador1.simbolo)
        coloca_al_azar(self._jugador2.simbolo)
        a = tuple([tuple(ren) for ren in a])
        return (self._jugador_actual.simbolo, a)

    def imprime_posicion(self):
        dibuja_tablero(self._posicion[1])

    def posiciones_siguientes(self, posicion):

        def busca_posicion(delta_r, delta_c):
            rm = r + delta_r if r + delta_r < rens else 0
            cm = c + delta_c if c + delta_c < cols else 0
            if tablero[rm][cm] == ' ':
                a = [list(ren) for ren in tablero]
                a[r][c] = turno_actual.lower()
                a[rm][cm] = turno_actual
                a = tuple([tuple(ren) for ren in a])
                resultado.append((turno_siguiente, a))

        turno_actual = posicion[0]
        turno_siguiente = self.simbolo_contrario(turno_actual)
        tablero = posicion[1]
        resultado = []
        rens = self._renglones
        cols = self._columnas
        for r in range(self._renglones):
            for c in range(self._columnas):
                if tablero[r][c] == turno_actual:
                    busca_posicion(-1, 0)
                    busca_posicion(1, 0)
                    busca_posicion(0, -1)
                    busca_posicion(0, 1)

        return tuple(resultado)

    def juego_terminado(self, posicion):
        return not self.posiciones_siguientes(posicion)

    def triunfo(self, jugador, posicion):
        s = self.simbolo_contrario(jugador.simbolo)
        return s == posicion[0] and self.juego_terminado(posicion)

    def pre_tiro(self):
        pass

    def post_tiro(self):

        def tiro():
            t = self._posicion[1]
            for r in range(self._renglones):
                for c in range(self._columnas):
                    if t[r][c] == s:
                        return '{}{}'.format(r, c)

        s = self._jugador_actual.simbolo
        print('[{}] Jugador {} tira {}'.format(self._num_tiro, s, tiro()))

    def imprime_resultado(self):
        ganador = (self._jugador1
                   if self.triunfo(self._jugador1, self._posicion)
                   else self._jugador2)
        print('>>>>>> GANADOR: {} <<<<<<<'.format(ganador))
        print('')

# ----------------------------------------------------------


class Jugador:
    '''Clase abstracta de la cual deben heredar todos las
    clases que representan un jugador.'''

    __metaclass__ = ABCMeta

    @abstractmethod
    def heuristica(self, posicion):
        '''Función heurística que puede utilizar un jugador para
        rankear la posición enviada como argumento.'''
        pass

    @abstractmethod
    def tira(self, posicion):
        '''Invocada por el juego para determinar el tiro de este
        jugador. Debe devolver un tiro válido a partir de la posición
        enviada como argumento.'''
        pass

    def __init__(self, nombre):
        '''Inicializa un jugador con el nombre enviado como argumento.'''
        self._nombre = nombre
        self._simbolo = None
        self._contrario = None
        self._juego = None

    def posiciones_siguientes(self, posicion):
        '''Devuelve todas todas las posiciones posibles que puede
        haber en un juego posteriores a la posición enviada como
        argumento.'''
        return self._juego.posiciones_siguientes(posicion)

    def triunfo(self, posicion):
        '''Devuelve el símbolo del jugador que resulta ganador en la
        posición enviada como argumento, o None si no hay un jugador
        ganador.'''
        if self._juego.triunfo(self, posicion):
            return self.simbolo
        elif self._juego.triunfo(self._contrario, posicion):
            return self._contrario.simbolo
        else:
            return None

    @property
    def nombre(self):
        '''El nombre de este jugador.'''
        return self._nombre

    @property
    def simbolo(self):
        '''El símbolo (o nombre si el símbolo no existe) de este jugador.'''
        return self._simbolo or self._nombre

    @property
    def contrario(self):
        '''Referencia al objeto jugador contrario a este jugador.'''
        return self._contrario

    @property
    def juego(self):
        '''Referencia al object juego de este jugador.'''
        return self._juego

    def __str__(self):
        '''Convierte este jugador a una cadena de caracteres.
           El formato usado es:

               "nombre (alias simbolo) [clase]"
        '''
        return '{}{} [{}]'.format(
            self._nombre,
            " (alias '{}')".format(self._simbolo) if self._simbolo else '',
            self.__class__.__name__)

# ----------------------------------------------------------


class JugadorD10(Jugador):
    '''Toda clase que represente un jugador del juego D10
    debe heredar de esta clase.

    La posición que maneja un juego de D10 es una tupla
    de la siguiente forma:

        (J, S)

    En donde:

        J: turno actual (nombre del jugador que se indicó al
           momento de crearlo)
        S: suma hasta el momento (0 al 10)

    Por ejemplo:

        ('Alfa', 5)

    Esta posición indica que el jugador actual es Alfa y que
    la suma actual es 5.'''
    pass

# ----------------------------------------------------------


class JugadorD10Aleatorio(JugadorD10):
    '''Jugador de D10 que tira de manera aleatoria.'''

    def heuristica(self, posicion):
        '''Devuelve True si posicion resulta en un tiro ganador para este
        Jugador. De otra forma regresa False.'''
        return self.triunfo(posicion) == self.simbolo

    def tira(self, posicion):
        '''Busca si se tiene un tiro ganador, sino selecciona cualquier
        tiro válido al azar.'''
        posibles = self.posiciones_siguientes(posicion)
        for p in posibles:
            if self.heuristica(p):
                return p
        return choice(posibles)

# ----------------------------------------------------------


class JugadorD10Estrategico(JugadorD10):
    '''Jugador de D10 que tira con una estrategia.'''

    def heuristica(self, posicion):
        '''Busca tirar en la posición que le garantice un triunfo siempre.'''
        return posicion[1] in [1, 4, 7, 10]

    def tira(self, posicion):
        '''Busca el mejor tiro posible, de lo contrario tira un 1.'''
        posibles = self.posiciones_siguientes(posicion)
        for p in posibles:
            if self.heuristica(p):
                return p
        return posibles[0]

# ----------------------------------------------------------


class JugadorD10Interactivo(JugadorD10):
    '''Jugador de D10 controlado a partir de una interfaz
    de usuario en modo texto.'''

    def heuristica(self, posicion):
        '''Vacío. Los jugadores interactivos no requieren tener una función
        heurística.'''
        pass

    def tira(self, posicion):
        '''Realiza el tiro a partir de la selección hecha por el usuario
        desde la entrada estándar. Se cicla hasta que el usuario realice
        un tiro válido.'''
        suma_actual = posicion[1]
        posibles = self.posiciones_siguientes(posicion)
        while True:
            entrada = input(
                'Jugador {}, teclea tu tiro (1 o 2): '.format(self.simbolo))
            try:
                opcion = int(entrada)
            except ValueError:
                opcion = 0
            for p in posibles:
                if p[1] == suma_actual + opcion:
                    return p
            print('Tiro inválido.')

# ----------------------------------------------------------


class JugadorSuperGato(Jugador):
    '''Toda clase que represente un jugador del juego de SuperGato
    debe heredar de esta clase.

    La posición que maneja un juego de SuperGato es una tupla
    de la siguiente forma:

        (J, T)

    En donde:

        J: turno actual (símbolo del jugador asignado por la clase
           de JuegoSuperGato: X y O)
        T: Tablero, una tupla de renglones (que a su vez son tuplas)
           con los símbolos de los jugadores en los lugares donde
           han tirado y espacios en los lugares disponibles.

    Por ejemplo:

        ('O', (('X', 'O', ' '), (' ', ' ', ' '), ('X', ' ', ' ')))

    Esta posición indica que el jugador actual es 'O' y que
    el tablero en este momento es:

     X | O |
    ---+---+---
       |   |
    ---+---+---
     X |   |
    '''
    pass

# ----------------------------------------------------------


class JugadorSuperGatoAleatorio(JugadorSuperGato):
    '''Jugador de SuperGato que tira de manera aleatoria.'''

    def heuristica(self, posicion):
        '''Devuelve True si posicion resulta en un tiro ganador para este
        Jugador. De otra forma regresa False.'''
        return self.triunfo(posicion) == self.simbolo

    def tira(self, posicion):
        '''Busca si se tiene un tiro ganador, sino selecciona cualquier
        tiro válido al azar.'''
        posibles = self.posiciones_siguientes(posicion)
        for p in posibles:
            if self.heuristica(p):
                return p
        return choice(posibles)

# ----------------------------------------------------------


def _ren_col(op, tablero):
    '''Determina si la cadena op corresponde a una coordenada de tipo 'RC'
    (renglón, columna) que está dentro de los límites del tablero y en lugar
    desocupado. En caso afrimativo devuelve una tupla con el valor numérico
    del renglón y la columna correspondiente. En caso negativo devuelve
    None.'''
    if len(op) == 2 and op[0].isdigit() and op[1].isdigit():
        r = int(op[0])
        c = int(op[1])
        if (r < len(tablero)
            and c < len(tablero[0])
                and tablero[r][c] == ' '):
            return r, c
        else:
            return None
    else:
        return None

# ----------------------------------------------------------


class JugadorSuperGatoInteractivo(JugadorSuperGato):
    '''Jugador de SuperGato controlado a partir de una interfaz
    de usuario en modo texto.'''

    def heuristica(self, posicion):
        '''Vacío. Los jugadores interactivos no requieren tener una función
        heurística.'''
        pass

    def tira(self, posicion):
        '''Realiza el tiro a partir de la selección hecha por el usuario
        desde la entrada estándar. Se cicla hasta que el usuario realice
        un tiro válido.'''
        tablero = posicion[1]
        posibles = self.posiciones_siguientes(posicion)
        while True:
            entrada = input(
                'Jugador {}, teclea tu tiro: '.format(self.simbolo))
            tiro_valido = _ren_col(entrada, tablero)
            if tiro_valido:
                print('')
                r, c = tiro_valido
                for p in posibles:
                    if p[1][r][c] == self.simbolo:
                        return p
            else:
                print('Tiro inválido.')

# ----------------------------------------------------------


class JugadorSuperGatoEstrategico(JugadorSuperGato):
    '''Jugador de SuperGato que tira con una estrategia.'''

    def heuristica(self, posicion):
        '''Busca tirar en la posición que considera más adecuada. Devuelve un
        puntaje muy alto (1000) si posicion resulta en un tiro ganador.
        Devuelve un puntaje muy bajo (-1000) si posicion resulta en un tiro
        en el que el contrario pudiera ganar inmediatamente en su siguiente
        turno. En otro caso evalúa cada lugar del tablero. Por cada símbolo
        del jugador en el tablero se suma 1 punto por cada lugar vacío
        contiguo y 10 por cada símbolo contiguo de este mismo jugador.'''
        if self.triunfo(posicion) == self.simbolo:
            return 1000

        posibles = self.posiciones_siguientes(posicion)
        contrario = self.contrario.simbolo
        for p in posibles:
            if self.triunfo(p) == contrario:
                return -1000

        puntaje = 0
        t = posicion[1]
        s = self.simbolo
        rens = self.juego.renglones
        cols = self.juego.columnas
        for r in range(rens):
            for c in range(cols):

                if t[r][c] == s:

                    # Verificar localidad de arriba
                    if r > 0:
                        if t[r - 1][c] == s:
                            puntaje += 10
                        elif t[r - 1][c] == ' ':
                            puntaje += 1

                    # Verificar localid de abajo
                    if r < rens - 1:
                        if t[r + 1][c] == s:
                            puntaje += 10
                        elif t[r + 1][c] == ' ':
                            puntaje += 1

                    # Verificar localidad de la izquierda
                    if c > 0:
                        if t[r][c - 1] == s:
                            puntaje += 10
                        elif t[r][c - 1] == ' ':
                            puntaje += 1

                    # Verificar localidad de la derecha
                    if c < cols - 1:
                        if t[r][c + 1] == s:
                            puntaje += 10
                        elif t[r][c + 1] == ' ':
                            puntaje += 1
        return puntaje

    def tira(self, posicion):
        '''Busca el mejor tiro entre todos los posibles.'''
        posibles = self.posiciones_siguientes(posicion)
        mp = posibles[0]
        mh = self.heuristica(mp)
        for p in posibles[1:]:
            h = self.heuristica(p)
            if h > mh:
                mh = h
                mp = p
        return mp

# ----------------------------------------------------------


class JugadorOrugas(Jugador):
    '''Toda clase que represente un jugador del juego de Orugas
    debe heredar de esta clase.

    La posición que maneja un juego de Orugas es una tupla
    de la siguiente forma:

        (J, T)

    En donde:

        J: turno actual (símbolo del jugador asignado por la clase
           de JuegoOrugas: B y N [blanco y negro])
        T: Tablero, una tupla de renglones (que a su vez son tuplas)
           con los símbolos de los jugadores en los lugares donde
           han tirado y espacios en los lugares disponibles. La cabeza
           de la oruga es el símbolo en mayúscula y el cuerpo es el
           símbolo en minúsculas.

    Por ejemplo:

        ('B', (('n', 'n', ' ', ' '), (' ', 'B', 'b', ' '),
               (' ', ' ', 'b', ' '), ('N', ' ', ' ', ' ')))

    Esta posición indica que el jugador actual es 'B' y que
    el tablero en este momento es:

     n | n |   |
    ---+---+---+---
       | B | b |
    ---+---+---+---
       |   | b |
    ---+---+---+---
     N |   |   |
    '''
    pass

# ----------------------------------------------------------


class JugadorOrugasAleatorio(JugadorOrugas):
    '''Jugador de Orugas que tira de manera aleatoria.'''

    def heuristica(self, posicion):
        '''Devuelve True si posicion resulta en un tiro ganador para este
        Jugador. De otra forma regresa False.'''
        return self.triunfo(posicion) == self.simbolo

    def tira(self, posicion):
        '''Busca si se tiene un tiro ganador, sino selecciona cualquier
        tiro válido al azar.'''
        posibles = self.posiciones_siguientes(posicion)
        for p in posibles:
            if self.heuristica(p):
                return p
        return choice(posibles)

# ----------------------------------------------------------


class JugadorOrugasInteractivo(JugadorOrugas):
    '''Jugador de Orugas controlado a partir de una interfaz
    de usuario en modo texto.'''

    def heuristica(self, posicion):
        '''Vacío. Los jugadores interactivos no requieren tener una función
        heurística.'''
        pass

    def tira(self, posicion):
        '''Realiza el tiro a partir de la selección hecha por el usuario
        desde la entrada estándar. Se cicla hasta que el usuario realice
        un tiro válido.'''
        tablero = posicion[1]
        posibles = self.posiciones_siguientes(posicion)
        while True:
            entrada = input(
                'Jugador {}, teclea tu tiro: '.format(self.simbolo))
            tiro_valido = _ren_col(entrada, tablero)
            if tiro_valido:
                r, c = tiro_valido
                for p in posibles:
                    if p[1][r][c] == self.simbolo:
                        print('')
                        return p
            print('Tiro inválido.')
