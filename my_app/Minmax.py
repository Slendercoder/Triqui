import numpy as np
import copy

class triqui:

    def estado_inicial(self):
        return np.matrix([[0]*3]*3)

    def jugador(self, estado):
        num_Os = np.count_nonzero(estado==1)
        num_Xs = np.count_nonzero(estado==2)
        # print("Cantidad O:", num_Os, " Cantidad X:", num_Xs)
        if num_Os < num_Xs:
            return 1
        else:
            return 2

    def acciones_aplicables(self, estado):
        # Devuelve una lista de parejas que representan las casillas vacías
        indices = []
        if np.count_nonzero(estado==0)>0:
            for x in range(3):
                for y in range(3):
                    if estado[y, x] == 0:
                        indices.append((x, y))

        return indices

    def transicion(self, estado, indice):
        # Devuelve el tablero incluyendo una O o X en el indice,
        # dependiendo del jugador que tiene el turno
        # Input: estado, que es una np.matrix(3x3)
        #        indice, de la forma (x,y)
        # Output: estado, que es una np.matrix(3x3)

        s = copy.deepcopy(estado)
        x = indice[0]
        y = indice[1]
        s[y, x] = self.jugador(estado)

        return s

    def test_objetivo(self, estado):
        # Devuelve True/False dependiendo si el juego se acabó
        # Input: estado, que es una np.matrix(3x3)
        # Output: True/False
        # print("Determinando si no hay casillas vacías...")
        if np.count_nonzero(estado==0)==0:
            return True
        else:
            # print("Buscando triqui horizontal...")
            for y in range(3):
                num_Os = np.count_nonzero(estado[y,:]==1)
                num_Xs = np.count_nonzero(estado[y,:]==2)
                # print("Cantidad O:", num_Os, " Cantidad X:", num_Xs)
                if (num_Os==3) or (num_Xs==3):
                    return True

            # print("Buscando triqui vertical...")
            for x in range(3):
                num_Os = np.count_nonzero(estado[:,x]==1)
                num_Xs = np.count_nonzero(estado[:,x]==2)
                # print("Cantidad O:", num_Os, " Cantidad X:", num_Xs)
                if (num_Os==3) or (num_Xs==3):
                    return True

            # print("Buscando triqui diagonal...")
            if (estado[0,0]==1) and (estado[1,1]==1) and (estado[2,2]==1):
                return True
            elif (estado[0,0]==2) and (estado[1,1]==2) and (estado[2,2]==2):
                return True

            # print("Buscando triqui transversal...")
            if (estado[2,0]==1) and (estado[1,1]==1) and (estado[0,2]==1):
                return True
            elif (estado[2,0]==2) and (estado[1,1]==2) and (estado[0,2]==2):
                return True

        return None

    def utilidad(self, estado):
        # Devuelve la utilidad del estado donde termina el juego
        # Input: estado, que es una np.matrix(3x3)
        # Output: utilidad, que es un valor -1, 0, 1
        ob = self.test_objetivo(estado)
        if ob:
            # Determina quién ganó la partida o si hay empate
            # print("Buscando triqui horizontal...")
            for y in range(3):
                num_Os = np.count_nonzero(estado[y,:]==1)
                num_Xs = np.count_nonzero(estado[y,:]==2)
                # print("Cantidad O:", num_Os, " Cantidad X:", num_Xs)
                if num_Os==3:
                    return -1
                elif num_Xs==3:
                    return 1

            # print("Buscando triqui vertical...")
            for x in range(3):
                num_Os = np.count_nonzero(estado[:,x]==1)
                num_Xs = np.count_nonzero(estado[:,x]==2)
                # print("Cantidad O:", num_Os, " Cantidad X:", num_Xs)
                if num_Os==3:
                    return -1
                elif num_Xs==3:
                    return 1

            # print("Buscando triqui diagonal...")
            if (estado[0,0]==1) and (estado[1,1]==1) and (estado[2,2]==1):
                return -1
            if (estado[0,0]==2) and (estado[1,1]==2) and (estado[2,2]==2):
                return 1

            # print("Buscando triqui transversal...")
            if (estado[2,0]==1) and (estado[1,1]==1) and (estado[0,2]==1):
                return -1
            if (estado[2,0]==2) and (estado[1,1]==2) and (estado[0,2]==2):
                return 1

            if np.count_nonzero(estado==0)==0:
                return 0

        return None

def min_value(juego, estado):
    if juego.test_objetivo(estado):
        return juego.utilidad(estado)
    else:
        acciones = juego.acciones_aplicables(estado)
        return min([
            max_value(juego, juego.transicion(estado, a))\
            for a in acciones
        ])

def max_value(juego, estado):
    if juego.test_objetivo(estado):
        return juego.utilidad(estado)
    else:
        acciones = juego.acciones_aplicables(estado)
        return max([
            min_value(juego, juego.transicion(estado, a))\
            for a in acciones
        ])

def minimax_decision(juego, estado):

    # Retorna la acción optima en el estado, para el jugador que lleva el turno
    acciones = juego.acciones_aplicables(estado)

    # Determina qué jugador tiene el turno
    if juego.jugador(estado)==2: # Juegan las X (MAX)
        indice = np.argmax([
            min_value(juego, juego.transicion(estado, a))\
            for a in acciones
        ])
    else: # Juegan las O (MIN)
        indice = np.argmin([
            max_value(juego, juego.transicion(estado, a))\
            for a in acciones
        ])

    # print("El computador juega en:", acciones[indice])
    # print("Tablero resultado:\n", juego.transicion(estado, acciones[indice]))
    return acciones[indice]

def jugar_minmax(juego, estado):

    return juego.transicion(estado, minimax_decision(juego, estado))
